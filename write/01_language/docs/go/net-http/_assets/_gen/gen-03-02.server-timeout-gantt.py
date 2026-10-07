# 사실 출처: go1.25.1 src/net/http/server.go:1020, src/net/http/server.go:2135, src/net/http/server.go:3179, src/net/http/server.go:3225, go doc net/http.Server
# 타입 스펙: type-gantt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520

d = D(W, H,
      "HTTP SERVER TIMEOUT BOUNDARIES AND SHUTDOWN LIFECYCLE",
      "서버 타임아웃 경계와 Graceful Shutdown 간트",
      "요청 헤더·본문 수신, 핸들러 연산, 응답 쓰기, 유휴 대기 구간별 타임아웃과 Shutdown 동작",
      "서버 타임아웃은 소켓 데드라인으로 강제되며 Shutdown 은 새 연결 차단 후 유휴 전환을 대기합니다")

LX = 28
TX = 210
TW = 710

# 5개 구간 상대 비율 (총 710px)
# 0: 헤더 읽기(120), 1: 본문 읽기(130), 2: Handler 실행(160), 3: 응답 쓰기(140), 4: Keep-Alive 대기(160)
phase_widths = [120, 130, 160, 140, 160]
phase_x = [TX]
for w in phase_widths:
    phase_x.append(phase_x[-1] + w)

phases = [
    ("헤더 읽기", "readRequest"),
    ("본문 읽기", "Body.Read"),
    ("Handler 실행", "ServeHTTP"),
    ("응답 쓰기", "w.Write"),
    ("유휴 대기", "bufr.Peek"),
]

# 상단 단계 헤더 (Y = 100)
d.box(TX, 100, TW, 36, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
for i, (name, hook) in enumerate(phases):
    x1 = phase_x[i]
    x2 = phase_x[i+1]
    cx = (x1 + x2) // 2
    d.t(cx, 116, name, 11, INK, fam=KR, weight=600)
    d.t(cx, 129, hook, 9, SOFT, fam=MONO)
    if i > 0:
        d.line(x1, 100, x1, 440, RULE, 0.7, "2 3")

# 수직 구분선 끝
d.line(phase_x[-1], 100, phase_x[-1], 440, RULE, 0.7, "2 3")

# 타임아웃 바 정의 (라벨, 서브, 시작idx, 종료idx, 색상, 포컬여부, 설명)
bars = [
    ("ReadHeaderTimeout", "Server", 0, 1, INFO, False, "요청 헤더 수신 완료 제한"),
    ("ReadTimeout", "Server", 0, 2, WARN, False, "헤더부터 요청 본문 전체 수신 제한"),
    ("WriteTimeout", "Server", 1, 4, ACC, True, "헤더 수신 직후부터 Handler 실행 및 응답 완료까지 포괄 (focal)"),
    ("IdleTimeout", "Server", 4, 5, OK, False, "Keep-Alive 연결 풀 유휴 보관 한도"),
]

y_start = 152
row_h = 54

for r, (title, owner, s_idx, e_idx, col, focal, desc) in enumerate(bars):
    y = y_start + r * row_h
    # 좌측 식별 라벨
    d.t(LX, y + 20, title, 12, col if focal else INK, fam=MONO, anchor="start", weight=600 if focal else 400)
    d.t(LX, y + 36, owner, 10, SOFT, fam=KR, anchor="start")

    # 간트 바
    bx1 = phase_x[s_idx] + 2
    bx2 = phase_x[e_idx] - 2
    bw = bx2 - bx1
    fill = f"{col}22" if focal else f"{col}14"
    sw = 1.4 if focal else 1.0
    d.box(bx1, y + 6, bw, 32, fill=fill, stroke=col, sw=sw, r=5)

    # 바 내부 텍스트
    center_x = (bx1 + bx2) // 2
    d.t(center_x, y + 26, desc, 10, col if focal else INK, fam=KR, weight=600 if focal else 400)

# Shutdown 수명주기 배너 (Y = 376)
sy = 376
d.t(LX, sy + 20, "Server.Shutdown()", 12, BAD, fam=MONO, anchor="start", weight=600)
d.t(LX, sy + 36, "우아한 종료 (Graceful)", 10, SOFT, fam=KR, anchor="start")

# Shutdown 범위 박스: 활성 구간은 대기, 유휴 구간은 즉시 종료
# 0~4 단계: 활성 연결 -> 대기
bw_active = phase_x[4] - phase_x[0] - 2
d.box(phase_x[0] + 2, sy + 6, bw_active, 32, fill=f"{BAD}14", stroke=BAD, sw=1.1, r=5)
d.t(phase_x[0] + bw_active // 2, sy + 26, "활성 연결: Listener 닫기 후 진행 중인 요청 완료까지 대기 (또는 ctx 만료)", 10, BAD, fam=KR)

# 4~5 단계: 유휴 연결 -> 즉시 소켓 Close
bw_idle = phase_x[5] - phase_x[4] - 2
d.box(phase_x[4] + 2, sy + 6, bw_idle, 32, fill=f"{MUTED}22", stroke=MUTED, sw=1.0, r=5)
d.t(phase_x[4] + bw_idle // 2, sy + 26, "유휴 연결: 즉시 Close", 10, MUTED, fam=KR)

# 범례
d.legend(470, [
    ("헤더 읽기 타임아웃", INFO),
    ("요청 전체 타임아웃", WARN),
    ("핸들러 및 쓰기 타임아웃 (focal)", ACC),
    ("유휴 유지 타임아웃", OK),
    ("Shutdown 생명주기 제어", BAD),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.server-timeout-gantt.svg"))
d.save(out_path)
