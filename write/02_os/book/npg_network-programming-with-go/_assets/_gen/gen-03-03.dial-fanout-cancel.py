# 03-03 다중 다이얼 동시 실행과 컨텍스트 일괄 취소 (Fan-out & Cancel)
# 사실 출처: NPG Ch.3 Listing 3-8 (dial_fanout_test.go, p.20-22)
# 타입 스펙: type-gantt — 10개 Dialer 의 시간축 막대와 첫 성공 시점의 cancel() 절단선
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 530
d = D(W, H, "NPG CHAPTER 3 — DIAL FAN-OUT GANTT",
      "다중 다이얼 경합과 컨텍스트 일괄 취소",
      "첫 연결 성공 즉시 cancel() 로 나머지 다이얼 중단",
      "첫 연결 성공 즉시 cancel() 로 나머지 다이얼 일괄 중단")

# Timeline geometry
x_label = 30
x_bar_start = 140
x_cancel = 380
x_end = 760
y_start = 115
row_h = 32

# Time axis header
d.line(x_bar_start, y_start - 10, x_end, y_start - 10, RULE, 1.0)
d.t(x_bar_start, y_start - 18, "시작", 11, SOFT, KR, "start")
d.t(x_cancel, y_start - 18, "첫 응답 시점", 11, OK, KR, "middle", 600)
d.t(x_end, y_start - 18, "시간 경과 →", 11, SOFT, KR, "end")

# 10 Dialer rows (Listing 3-8: 10 dialers with IDs 1..10)
for i in range(10):
    dialer_id = i + 1
    is_winner = (i == 2)
    ry = y_start + i * row_h
    
    # Left Label: 모든 레인은 Dialer 1..10 그대로 유지
    d.t(x_label, ry + 16, f"Dialer {dialer_id}", 11, INK, MONO, "start", 400)
    
    # Task bar
    bar_w = x_cancel - x_bar_start
    if is_winner:
        # Winning bar: 막대 강조 + '첫 응답 (예시)'
        d.box(x_bar_start, ry + 4, bar_w, 20, fill=f"{OK}22", stroke=OK, sw=1.5, r=4)
        d.t(x_bar_start + bar_w / 2, ry + 17, "첫 응답 (예시)", 11, OK, KR, "middle", 600)
        # response channel send (shifted right of cancel line)
        d.arrow([(x_cancel, ry + 14), (x_cancel + 22, ry + 14)], c=OK, m="ok", sw=1.2)
        d.chip(x_cancel + 75, ry + 14, "<-res 전송", OK, 11)
    else:
        # Canceled bar
        d.box(x_bar_start, ry + 4, bar_w, 20, fill=f"{MUTED}15", stroke=RULE, sw=1.0, r=4)
        # Cut indicator
        d.line(x_cancel, ry + 4, x_cancel, ry + 24, BAD, 2.0)

# Vertical Cancel Line across all rows
d.line(x_cancel, y_start - 10, x_cancel, y_start + 10 * row_h, BAD, 1.8, dash="4 3")
d.chip(x_cancel, y_start + 10 * row_h + 15, "cancel() 호출", BAD, 11)

# Legend
d.legend(480, [("첫 응답", OK), ("취소 중단", BAD), ("경합 구간", MUTED)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-03.dial-fanout-cancel.svg"))
d.save(out)
print(f"saved: {out}")
