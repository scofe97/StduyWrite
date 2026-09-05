# 08-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 734
d = D(W, H, "LEARNING COREDNS · 08-01",
      "무엇을 볼지 좁히는 손잡이가 도구마다 다르다",
      "8장의 절 일곱을 읽는 순서로 이은 지도. 1~4절이 정상 흐름을 보는 도구이고, "
      "5~7절이 잘못됐을 때 쓰는 도구다.",
      "주황이 손잡이가 없어 운영에서 금지된 자리입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "세는 것과 적는 것", "지표는 사건이 아니라 사건의 수"),
    ("§2", "로그 한 줄을 가른다", "큰따옴표 안이 요청, 밖이 응답"),
    ("§3", "좁히는 손잡이 셋", "이름 · 응답 종류 · 형식 문자열"),
    ("§4", "응답까지 보려면", "dnstap 은 형식을 바꿔 값을 낮춘다"),
    ("§5", "같은 오류가 쏟아질 때", "접되 너무 넓게 접지 않는다"),
    ("§6", "추적은 비싸다", "만 건에 한 건 · 시계를 의심한다"),
    ("§7", "손잡이가 없는 하나", "debug 는 운영 금지"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(len(cards) - 1):
    x1, y1 = pos(i)
    x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 6)
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 620, "도구를 고르는 일이 곧 그 값을 깎을 손잡이를 고르는 일이다", 13, MUTED, KR, "start")
d.t(20, 644, "원서 표 8-1 의 CoreDNS 지표 이름은 지금 거의 다 다른 이름이다", 13, MUTED, KR, "start")

d.legend(672, [("손잡이가 없는 도구", ACC)])
d.save("08-01.chapter-overview.svg")
