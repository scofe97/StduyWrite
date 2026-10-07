# 사실 출처: go1.25.1 src/net/http/transport.go:1484, src/net/http/transport.go:2065, src/net/http/transport.go:2355, src/net/http/transport.go:1052
# 타입 스펙: type-state
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "PERSISTCONN LIFECYCLE AND STATE TRANSITIONS",
      "persistConn 생명주기와 연결 풀 상태 전이",
      "연결 생성부터 활성 I/O, Body 소비 완료 후 유휴 풀 보관 및 재사용/만료 폐기",
      "Body 를 EOF 까지 읽고 닫아야 유휴 풀로 회수되며 그렇지 않으면 연결이 폐기됩니다")

CY = 210
BH = 82
BW = 160

X_START = 36
X1 = 140    # DIAL
X2 = 380    # ACTIVE
X3 = 630    # IDLE (focal)
X4 = 860    # CLOSED
X_END = 934

def draw_state(cx, cy, w, h, name, sub, note, c, focal=False):
    x = cx - w // 2
    y = cy - h // 2
    fill = f"{c}1A" if focal else PAPER2
    sw = 1.4 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=c, sw=sw, r=8)
    d.t(cx, cy - 20, name, 13, c, fam=MONO, weight=600)
    d.t(cx, cy - 3, sub, 11, INK, fam=KR)
    d.line(x + 10, cy + 8, x + w - 10, cy + 8, RULE, 0.7)
    d.t(cx, cy + 23, note, 10, ACC if focal else SOFT, fam=KR)

# 시작점
d.o.append(f'<circle cx="{X_START}" cy="{CY}" r="5" fill="{INK}"/>')
d.arrow([(X_START + 6, CY), (X1 - BW // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X_START + X1 - BW // 2) // 2, CY - 10, "getConn()", 10, MUTED, fam=MONO)

# State 1: DIAL
draw_state(X1, CY, BW, BH, "DIAL", "소켓 생성·루프 기동", "readLoop·writeLoop", INFO)

# Transition 1 -> 2
d.arrow([(X1 + BW // 2 + 2, CY), (X2 - BW // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X1 + BW // 2 + X2 - BW // 2) // 2, CY - 12, "핸드셰이크 완료", 10, INK, fam=KR)

# State 2: ACTIVE
draw_state(X2, CY, BW, BH, "ACTIVE", "요청/응답 스트림", "RoundTrip I/O", OK)

# Transition 2 -> 3 (Body EOF + Close)
d.arrow([(X2 + BW // 2 + 2, CY), (X3 - BW // 2 - 4, CY)], c=ACC, m="acc", sw=1.3)
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY - 18, "Body EOF + Close()", 10, ACC, fam=KR, weight=600)
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY - 6, "tryPutIdleConn()", 9, SOFT, fam=MONO)

# State 3: IDLE (focal)
draw_state(X3, CY, BW, BH, "IDLE", "유휴 풀 보관", "idleLRU 대기", ACC, focal=True)

# Transition 3 -> 2 (재사용 루프 - 위쪽 호선)
d.path(f"M {X3} {CY - BH // 2 - 2} C {X3} 100, {X2} 100, {X2} {CY - BH // 2 - 6}",
       c=OK, sw=1.3, m="ok")
d.t((X2 + X3) // 2, 88, "후속 요청 매칭 (queueForIdleConn)", 10, OK, fam=KR, weight=600)

# Transition 3 -> 4 (IdleConnTimeout 만료)
d.arrow([(X3 + BW // 2 + 2, CY), (X4 - BW // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X3 + BW // 2 + X4 - BW // 2) // 2, CY - 14, "IdleConnTimeout 만료", 10, WARN, fam=KR)
d.t((X3 + BW // 2 + X4 - BW // 2) // 2, CY - 2, "또는 서버 FIN", 9, SOFT, fam=KR)

# State 4: CLOSED
draw_state(X4, CY, 120, BH, "CLOSED", "소켓 닫힘", "고루틴 종료", BAD)

# Transition 2 -> 4 (Body 미완료 Close / 취소 - 아래쪽 호선)
d.path(f"M {X2} {CY + BH // 2 + 2} C {X2} 340, {X4} 340, {X4} {CY + BH // 2 + 6}",
       c=BAD, sw=1.2, m="bad", dash="4 3")
d.t((X2 + X4) // 2, 354, "Body 조기 종료 (earlyCloseFn) · 미종료 누수 폐기", 10, BAD, fam=KR)

# 종료점
d.arrow([(X4 + 120 // 2 + 2, CY), (X_END - 10, CY)], c=MUTED, m="ar")
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="7" fill="none" stroke="{BAD}" stroke-width="1.3"/>')
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="3.5" fill="{BAD}"/>')

# 하단 정보 바: 조건 비교
d.box(X_START, 394, W - X_START * 2, 36, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(X_START + 16, 417, "재사용 핵심 조건:", 11, INK, fam=KR, anchor="start", weight=600)
d.t(X_START + 130, 417, "① Response.Body 를 io.EOF 까지 읽음", 11, OK, fam=KR, anchor="start")
d.t(X_START + 370, 417, "② Body.Close() 호출 완료", 11, OK, fam=KR, anchor="start")
d.t(X_START + 560, 417, "③ MaxIdleConnsPerHost 여유 슬롯 존재", 11, INFO, fam=KR, anchor="start")

# 범례
d.legend(450, [
    ("생성 및 대기", INFO),
    ("스트림 통신 중", OK),
    ("유휴 풀 보관 (focal)", ACC),
    ("만료 경고", WARN),
    ("소켓 폐기 · 연결 단절", BAD),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.persistconn-state.svg"))
d.save(out_path)
