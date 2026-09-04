# 06-03 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "LEARNING COREDNS · 06-03",
      "복제본 둘과 170Mi 는 어디서 온 값인가",
      "6장 후반부의 절 여섯을 읽는 순서로 이은 지도. 1~4절이 배포 자원이고, "
      "5절과 6절이 그 위에서 조정하는 일이다.",
      "4절이 이 편 제목의 두 숫자를 품고 있습니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "네 범주가 있어야 뜬다", "Corefile 하나로는 아무것도 안 뜬다"),
    ("§2", "접근권은 필요보다 넓다", "쓰지도 않는 권한이 둘 있다"),
    ("§3", "이름이 kube-dns 인 이유", "이름과 클러스터 IP 는 불변이다"),
    ("§4", "Deployment 의 판단들", "170Mi 도 호환에서 나온 값이다"),
    ("§5", "복제본을 늘리는 두 갈래", "노드 수로 재거나 CPU 로 재거나"),
    ("§6", "더 나은 Corefile", "옵션이 아니라 블록을 나눠 고친다"),
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

d.t(20, 504, "2절부터 4절까지가 \"왜 이 값인가\" 이고, 5절과 6절이 \"그래서 무엇을 고치나\" 다", 13, MUTED, KR, "start")
d.t(20, 528, "6절의 두 단계가 앞 편이 남긴 지적을 저자들이 직접 거두는 자리다", 13, MUTED, KR, "start")

d.legend(556, [("제목의 두 숫자가 있는 절", ACC)])
d.save("06-03.chapter-overview.svg")
