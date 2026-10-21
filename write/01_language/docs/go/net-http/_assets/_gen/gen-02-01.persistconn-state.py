# 사실 출처: go1.25.1 src/net/http/transport.go:1484, src/net/http/transport.go:2065, src/net/http/transport.go:2355, src/net/http/transport.go:2395, src/net/http/transport.go:1052, src/net/http/transport.go:1116
# 타입 스펙: type-state
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 500

d = D(W, H,
      "PERSISTCONN LIFECYCLE AND STATE TRANSITIONS",
      "persistConn 생명주기와 연결 풀 상태 전이",
      "연결 생성부터 활성 I/O, Body EOF 도달 후 유휴 풀 보관 및 재사용/만료 폐기",
      "Body 를 EOF 까지 읽어야 유휴 풀로 회수되며 EOF 전에 닫으면 연결이 폐기됩니다")

CY = 210
BH = 82
BW = 130

X_START = 24
X1 = 180    # DIAL
X2 = 410    # ACTIVE
X3 = 650    # IDLE (focal)
X4 = 872    # CLOSED
W4 = 100
X_END = 944

def draw_state(cx, cy, w, h, name, sub, note, c, focal=False):
    x = cx - w // 2
    y = cy - h // 2
    fill = f"{c}1A" if focal else PAPER2
    sw = 1.4 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=c, sw=sw, r=8)
    d.t(cx, cy - 20, name, 13, c, fam=MONO, weight=600)
    d.t(cx, cy - 3, sub, 11, INK, fam=KR)
    d.line(x + 10, cy + 8, x + w - 10, cy + 8, RULE, 0.7)
    d.t(cx, cy + 23, note, 11, ACC if focal else SOFT, fam=KR)

# 시작점
d.o.append(f'<circle cx="{X_START}" cy="{CY}" r="5" fill="{INK}"/>')
d.arrow([(X_START + 6, CY), (X1 - BW // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X_START + X1 - BW // 2) // 2, CY - 8, "getConn()", 10, MUTED, fam=MONO)

# State 1: DIAL
draw_state(X1, CY, BW, BH, "DIAL", "소켓 생성·루프 기동", "readLoop·writeLoop", INFO)

# Transition 1 -> 2
d.arrow([(X1 + BW // 2 + 2, CY), (X2 - BW // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X1 + BW // 2 + X2 - BW // 2) // 2, CY - 8, "핸드셰이크 완료", 11, INK, fam=KR)

# State 2: ACTIVE
draw_state(X2, CY, BW, BH, "ACTIVE", "요청/응답 스트림", "RoundTrip I/O", OK)

# Transition 2 -> 3 (Body EOF 도달 — Read 가 io.EOF 를 만나는 순간 회수된다)
d.arrow([(X2 + BW // 2 + 2, CY), (X3 - BW // 2 - 4, CY)], c=ACC, m="acc", sw=1.3)
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY - 8, "Body EOF 도달", 11, ACC, fam=KR, weight=600)
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY + 17, "tryPutIdleConn()", 10, SOFT, fam=MONO)

# State 3: IDLE (focal)
draw_state(X3, CY, BW, BH, "IDLE", "유휴 풀 보관", "idleLRU 대기", ACC, focal=True)

# Transition 3 -> 2 (재사용 루프 - 위쪽 호선, 꼭짓점 y≈117)
d.path(f"M {X3} {CY - BH // 2 - 2} C {X3} 100, {X2} 100, {X2} {CY - BH // 2 - 6}",
       c=OK, sw=1.3, m="ok")
d.t((X2 + X3) // 2, 109, "후속 요청 매칭 (queueForIdleConn)", 11, OK, fam=KR, weight=600)

# Transition 3 -> 4 (IdleConnTimeout 만료 또는 서버 FIN)
d.arrow([(X3 + BW // 2 + 2, CY), (X4 - W4 // 2 - 4, CY)], c=MUTED, m="ar")
d.t((X3 + BW // 2 + X4 - W4 // 2) // 2, CY - 8, "IdleConnTimeout", 10, WARN, fam=MONO)
d.t((X3 + BW // 2 + X4 - W4 // 2) // 2, CY + 18, "만료·서버 FIN", 11, SOFT, fam=KR)

# State 4: CLOSED
draw_state(X4, CY, W4, BH, "CLOSED", "소켓 닫힘", "고루틴 종료", BAD)

# Transition 2 -> 4 (EOF 전 Close / 풀 한도 초과 - 아래쪽 호선, 바닥 y≈318)
d.path(f"M {X2} {CY + BH // 2 + 2} C {X2} 340, {X4} 340, {X4} {CY + BH // 2 + 2}",
       c=BAD, sw=1.2, m="bad", dash="4 3")
d.t((X2 + X4) // 2, 336, "EOF 전 Close (earlyCloseFn) · 유휴 한도 초과", 11, BAD, fam=KR)

# Close 미호출: readLoop 가 waitForBodyRead 에서 막혀 ACTIVE 에 머문다 (자기 루프)
d.path(f"M {X2 - 25} {CY + BH // 2 + 2} C {X2 - 25} 300, {X2 - 75} 300, {X2 - 75} {CY + BH // 2 + 2}",
       c=WARN, sw=1.2, m="warn", dash="4 3")
d.t(X2 - 86, 296, "Close 미호출: ACTIVE 에 묶임 · 누수", 11, WARN, fam=KR, anchor="end")

# 종료점
d.arrow([(X4 + W4 // 2 + 2, CY), (X_END - 10, CY)], c=MUTED, m="ar")
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="7" fill="none" stroke="{BAD}" stroke-width="1.3"/>')
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="3.5" fill="{BAD}"/>')

# 하단 정보 바: 조건 비교
d.box(36, 394, W - 72, 36, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(36 + 16, 417, "재사용 핵심 조건:", 11, INK, fam=KR, anchor="start", weight=600)
d.t(36 + 130, 417, "1. Response.Body 를 io.EOF 까지 읽음 (Close 는 그 뒤 정리)", 11, OK, fam=KR, anchor="start")
d.t(36 + 520, 417, "2. MaxIdleConnsPerHost 여유 슬롯 존재", 11, INFO, fam=KR, anchor="start")

# 범례
d.legend(450, [
    ("생성 및 대기", INFO),
    ("스트림 통신 중", OK),
    ("유휴 풀 보관 (focal)", ACC),
    ("만료·누수 경고", WARN),
    ("소켓 폐기 · 연결 단절", BAD),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.persistconn-state.svg"))
d.save(out_path)
