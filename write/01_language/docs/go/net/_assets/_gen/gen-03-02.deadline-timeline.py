# 사실 출처: go doc net.Conn.SetDeadline, SetReadDeadline (go1.25.1)
# 타입 스펙: type-timeline
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 460

d = D(W, H,
      "NET.CONN DEADLINE TIMELINE",
      "SetDeadline 타임라인과 Read 블로킹 구간 비교",
      "1회 설정 시 마감 경과 후 바쁜 루프 발생과 매 Read 직전 갱신의 차이",
      "절대 시각 마감(deadline) 적용 방식에 따른 고루틴 대기 구간과 호출 횟수 대조")

# 시간축 파라미터 (0ms ~ 1000ms)
# x축: 0ms -> 200, 1000ms -> 880 (폭 680px, 100ms당 68px)
X0, X1000 = 200, 880
def tx(ms):
    return int(X0 + (ms / 1000.0) * (X1000 - X0))

# 눈금선 (y = 100 ~ 380)
for ms in range(0, 1001, 200):
    x = tx(ms)
    d.line(x, 108, x, 380, RULE, 0.8, "4 4")
    d.t(x, 100, f"{ms}ms", 11, SOFT, fam=MONO, anchor="middle")

# ── 케이스 1: 1회만 설정 (SetReadDeadline 1회) ──
Y1 = 148
d.box(24, Y1 - 20, 156, 92, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(102, Y1, "1회만 설정", 13, BAD, fam=KR, anchor="middle", weight=600)
d.t(102, Y1 + 20, "SetReadDeadline(t0+200ms)", 10, MUTED, fam=MONO, anchor="middle")
d.t(102, Y1 + 40, "1초간 19,936,237회 호출", 11, BAD, fam=KR, anchor="middle", weight=600)
d.t(102, Y1 + 58, "CPU 100% 바쁜 루프", 10, MUTED, fam=KR, anchor="middle")

# 0 ~ 200ms: 정상 블로킹 구간
d.tone(tx(0), Y1, tx(200) - tx(0), 48, OK, r=4, op="22", sw=1.2)
d.t(tx(100), Y1 + 28, "Read 대기 200ms", 11, OK, fam=KR, anchor="middle", weight=600)

# 200ms: 마감 시각 도달 핀
d.line(tx(200), Y1 - 12, tx(200), Y1 + 60, ACC, 1.4)
d.chip(tx(200), Y1 - 16, "마감 시각 t0+200ms", ACC, 10)

# 200 ~ 1000ms: 마감 경과 후 즉시 실패 구간 (바쁜 루프)
d.tone(tx(200), Y1, tx(1000) - tx(200), 48, BAD, r=4, op="20", sw=1.4)
d.t(tx(600), Y1 + 20, "마감 경과 상태 지속 · Read 즉시 반환 (0ms 대기)", 12, BAD, fam=KR, anchor="middle", weight=600)
d.t(tx(600), Y1 + 38, "os.ErrDeadlineExceeded (1,993만 회/초)", 11, INK, fam=MONO, anchor="middle")

# ── 케이스 2: 매 Read 직전 갱신 (idle timeout 200ms) ──
Y2 = 284
d.box(24, Y2 - 20, 156, 92, fill=PAPER2, stroke=OK, sw=1.2)
d.t(102, Y2, "매 Read 직전 갱신", 13, OK, fam=KR, anchor="middle", weight=600)
d.t(102, Y2 + 20, "conn.SetReadDeadline()", 10, MUTED, fam=MONO, anchor="middle")
d.t(102, Y2 + 40, "1초간 5회 호출", 11, OK, fam=KR, anchor="middle", weight=600)
d.t(102, Y2 + 58, "CPU 유휴 보존 (idle 200ms)", 10, MUTED, fam=KR, anchor="middle")

# 5개 구간 반복 (0~200, 200~400, 400~600, 600~800, 800~1000)
for i in range(5):
    t_start = i * 200
    t_end = (i + 1) * 200
    x_s = tx(t_start)
    x_e = tx(t_end)
    w_slot = x_e - x_s
    d.tone(x_s + 2, Y2, w_slot - 4, 48, INFO, r=4, op="18", sw=1.0)
    d.t(x_s + w_slot // 2, Y2 + 22, f"#{i+1} 대기 (200ms)", 11, INK, fam=KR, anchor="middle", weight=600)
    d.t(x_s + w_slot // 2, Y2 + 38, "타임아웃 감지", 10, MUTED, fam=KR, anchor="middle")
    # 갱신 핀
    d.line(x_s, Y2 - 8, x_s, Y2 + 52, OK, 1.2)

# 범례
d.legend(412, [
    ("정상 블로킹 대기 구간", OK),
    ("주기적 idle 갱신 구간", INFO),
    ("마감 시각 초과 지점", ACC),
    ("즉시 실패 바쁜 루프 (위험)", BAD)
])

out_name = "03-02.deadline-timeline.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
