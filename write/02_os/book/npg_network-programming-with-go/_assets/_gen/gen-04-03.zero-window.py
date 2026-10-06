# 타입 스펙: type-line
# 04-03 제로 윈도(Zero Window) 발생과 수신 버퍼 포화
# 사실 출처: NPG Ch.4 Listing 4-26, p.36-37
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 480
d = D(W, H, "LISTING 4-26 ZERO WINDOW",
      "수신 버퍼 포화와 제로 윈도",
      "애플리케이션 처리 지연과 제로 윈도 전개 과정",
      "앱 읽기 중단 시 윈도 축소 및 송신 차단")

x_left = 110
x_right = 780
y_top = 140
y_bot = 380

# 송신 차단 영역 (Zero Window Zone)
d.tone(580, y_top, 180, y_bot - y_top, WARN, r=0, op="08", sw=0.8)
d.line(580, y_top, 580, y_bot, WARN, 1.2, "3 4")

# X축, Y축
d.line(x_left, y_top, x_left, y_bot, RULE, 1.2)
d.arrow([(x_left, y_bot), (x_right, y_bot)], RULE, "ar", 1.2)

d.t(x_left - 12, y_top + 4, "최대 용량", 11, MUTED, KR, "end")
d.t(x_left - 12, y_bot + 4, "0 (Zero)", 11, MUTED, MONO, "end")
d.t(x_right + 8, y_bot + 4, "시간 경과", 11, MUTED, KR, "start")

# X축 눈금점
pts_t = [
    (140, "정상 읽기"),
    (270, "Read() 중단"),
    (430, "버퍼 급증"),
    (580, "윈도 0 도달"),
    (710, "송신 차단 지속"),
]

for tx, tlab in pts_t:
    d.line(tx, y_bot, tx, y_bot + 5, RULE, 1.0)
    d.t(tx, y_bot + 22, tlab, 11, INK if tx < 580 else WARN, KR, "middle")

# Series 1: 수신 버퍼 사용량 (BAD)
buf_pts = [(140, 350), (270, 320), (430, 230), (580, 160), (710, 160)]
p_buf = " ".join(f"{x},{y}" for x, y in buf_pts)
d.o.append(f'<polyline points="{p_buf}" fill="none" stroke="{BAD}" stroke-width="2.2" stroke-linejoin="round"/>')
for bx, by in buf_pts:
    d.o.append(f'<circle cx="{bx}" cy="{by}" r="4" fill="{BAD}"/>')

# Series 2: 광고 윈도 크기 (OK)
win_pts = [(140, 170), (270, 200), (430, 290), (580, 380), (710, 380)]
p_win = " ".join(f"{x},{y}" for x, y in win_pts)
d.o.append(f'<polyline points="{p_win}" fill="none" stroke="{OK}" stroke-width="2.2" stroke-linejoin="round"/>')
for wx, wy in win_pts:
    d.o.append(f'<circle cx="{wx}" cy="{wy}" r="4" fill="{OK}"/>')

# 제로 윈도 콜아웃
d.chip(616, 345, "Win = 0", WARN, 11)
d.t(664, 200, "송신측 전송 중단", 11, WARN, KR, "middle", 600)
d.t(664, 222, "프로브 패킷만 허용", 11, MUTED, KR, "middle")

d.legend(H - 46, [("수신 버퍼 사용량", BAD), ("광고 윈도 크기", OK), ("송신 차단 구간", WARN)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03.zero-window.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
