# 타입 스펙: type-process — 트윗 한 건이 팔로워 수만큼의 Redis 리스트 줄이 되고 그 수를 전달 속도로 나누면 걸리는 시간이 나온다. 칸마다 같은 자리(제목·계산·결과·부제)에 값이 반복되고 화살표가 읽는 순서를 나른다.
# 사실 출처: Timelines at Scale(Raffi Krikorian, QCon) 슬라이드 — Redis 리스트 항목 Tweet ID 8 bytes · User ID 8 bytes · Bits 4 bytes, RPUSHX 로 캐시된 타임라인에만 추가(그래서 쓰기 수는 상한이고 시간은 p50 으로 어림한 값), 수신자 키 기준으로 4k destinations 씩 pipeline, @ladygaga 31 million followers, timeline delivery ~300k deliveries/sec. https://www.infoq.com/presentations/Twitter-Timeline-Scalability/
#   20 B(8+8+4) 와 103 초(31,000,000 ÷ 300,000 ≈ 103.3) 는 이 생성기가 계산한 값이며 팔로워 수는 슬라이드 시점(2012)의 값이다.
# Layout conventions: 카드 폭 276·높이 212, 가로 stride 300(x=40+300k), 카드 y=112, 화살표는 카드 중앙 y=218. 3 카드. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

assert 8 + 8 + 4 == 20 and round(31_000_000 / 300_000) == 103

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 08-01 §1",
      "팔로워 3,100 만 명의 트윗은 쓰기가 최대 3,100 만 번이다",
      "트윗 한 건이 수신자마다 Redis 리스트에 20 바이트 한 줄을 쌓고, 초당 전달 속도가 걸리는 시간을 정합니다",
      "팔로워 수 · 전달 속도는 2012 년 강연 슬라이드의 값")

CW, CH, STRIDE, X0, Y0 = 276, 212, 300, 40, 112
cards = [
    ("1", "수신자 리스트 한 줄", "8 B + 8 B + 4 B = 20 B", "트윗 ID · 사용자 ID · 비트", "RPUSHX 한 번에 한 줄", INFO),
    ("2", "팔로워 31,000,000", "쓰기 최대 31,000,000 번", "4,000 곳씩 묶어 전송", "수신자 키마다 한 줄", INFO),
    ("3", "전달 300,000 건/초", "31,000,000 ÷ 300,000", "≈ 103 초 (p50 어림)", "트윗 하나가 퍼지는 시간", ACC),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, KR, "start")
    d.t(cx, Y0 + 52, title, 14, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 13, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 13, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("초점", ACC), ("한 건의 비용 단위", INFO)])
d.save("08-01.fanout-cost.svg")
