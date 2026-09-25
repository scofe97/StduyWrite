# 07-01 학습 목표 뒤 — 생존 확인의 두 채널을 교차시킨 네 조합.
# 타입 스펙: type-quadrant — 두 축(진단 채널 · 서비스 채널)의 성공 여부로 평면을 넷으로
#           가르고, 각 칸이 서로 다른 원인 부위를 가리킨다. 축이 둘이라 quadrant 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, WARN, KR, MONO

W, H = 880, 440
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 07-01",
      "ping 과 서비스, 두 채널의 네 조합",
      "진단 채널(ICMP)과 서비스 채널(TCP)은 중간 장비가 다르게 다룰 수 있다. 네 칸 중 대각선만 직관과 맞는다.",
      "대각선이 아닌 두 칸이 이 편과 앞 편이 다루는 자리다")

# 축
AX, AY, CW, CH, GAP = 150, 110, 340, 124, 16
d.t(AX + CW / 2, 96, "서비스 채널 (curl · nc) 성공", 12, SOFT, KR, "middle", 600)
d.t(AX + CW + GAP + CW / 2, 96, "서비스 채널 실패", 12, SOFT, KR, "middle", 600)
d.t(140, AY + CH / 2, "ping 성공", 12, SOFT, KR, "end", 600)
d.t(140, AY + CH + GAP + CH / 2, "ping 실패", 12, SOFT, KR, "end", 600)

cells = [
    (0, 0, OK,   "정상", "두 채널이 다 산다", ""),
    (1, 0, WARN, "포트·프로세스를 본다", "경로는 성립하는데 종단이 안 받는다", "08편 — refused · 리스너 없음"),
    (0, 1, BAD,  "ICMP 가 막혔다", "서버는 멀쩡한데 모니터링이 죽었다고 한다", "15편 — 이 편 §2"),
    (1, 1, MUTED,"경로를 본다", "두 채널이 함께 죽었으면 아래층이다", "04·05편 — 라우팅·블랙홀"),
]
for cx, cy, c, title, sub, note in cells:
    x = AX + cx * (CW + GAP)
    y = AY + cy * (CH + GAP)
    if c is MUTED:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    else:
        d.tone(x, y, CW, CH, c, 8, "10", 1.2)
    d.t(x + 18, y + 34, title, 15, c if c is not MUTED else INK, KR, "start", 600)
    d.t(x + 18, y + 62, sub, 12, MUTED, KR, "start")
    if note:
        d.t(x + 18, y + 96, note, 11, SOFT, KR, "start")

d.t(24, 412, "ping 은 서비스의 생사가 아니라 ICMP 의 생사를 알려 준다 — 최종 판정은 서비스 채널로",
    12, ACC, KR, "start", 600)
d.save("07-01.two-channels.svg")
