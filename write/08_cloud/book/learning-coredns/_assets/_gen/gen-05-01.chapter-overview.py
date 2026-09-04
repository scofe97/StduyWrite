# 05-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 808
d = D(W, H, "LEARNING COREDNS · 05-01",
      "상태를 밖에 두어야 이름이 초 단위로 바뀐다",
      "5장의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 문제를 좁히고, "
      "4~6절이 CoreDNS 의 답이며, 7절이 그 답의 대안을 늘어놓는다.",
      "4절이 이 장의 답이 서는 자리입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "Checkout 은 주소를 어떻게 아나", "쪼개면 없던 호출이 생긴다"),
    ("§2", "이름으로 가는 사다리 다섯 칸", "앞 칸이 남긴 문제를 다음 칸이 푼다"),
    ("§3", "전통 DNS 의 전제가 깨진다", "등록은 빨라도 조회는 TTL 을 기다린다"),
    ("§4", "etcd — 상태를 밖에 둔다", "CoreDNS 는 무상태라 몇 대든 는다"),
    ("§5", "이름을 뒤집으면 키가 된다", "한 줄이 레코드 둘을 만든다"),
    ("§6", "문법 일곱 중 지금 남은 것", "둘은 사라지고 셋이 새로 붙었다"),
    ("§7", "etcd 말고 다른 길", "등록하는 주체가 누구인가"),
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
    focal = (i == 3)
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 648, "1절부터 3절까지가 \"왜 존 파일로는 안 되는가\"이고, 4절부터가 \"그래서 무엇을 하는가\"다", 13, MUTED, KR, "start")
d.t(20, 672, "7절은 etcd 가 유일한 답이 아니라는 것을 확인하고 6장으로 넘긴다", 13, MUTED, KR, "start")

d.legend(704, [("이 장의 답이 서는 절", ACC)])
d.save("05-01.chapter-overview.svg")
