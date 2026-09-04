# 06-04 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 744
d = D(W, H, "LEARNING COREDNS · 06-04",
      "명세 밖으로 나가면 이식성을 내준다",
      "6장 마지막 구간의 절 일곱을 읽는 순서로 이은 지도. 1~2절이 플러그인 문법이고, "
      "3~7절이 명세 밖 기능들이다.",
      "4절과 5절이 한 이야기의 문제와 답입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "문법 전체와 지금 남은 것", "셋이 사라졌고 예고는 하나였다"),
    ("§2", "파드 옵션이 메모리를 가른다", "가장 안전한 모드가 가장 비싸다"),
    ("§3", "와일드카드는 명세 밖 편의", "쓸모가 분명한 자리는 하나뿐"),
    ("§4", "점 다섯이 질의를 여섯으로", "짧은 이름의 값을 바깥 이름이 치른다"),
    ("§5", "autopath 가 반복을 옮긴다", "네트워크에서 서버 안으로"),
    ("§6", "존 전송과 바깥 노출", "AXFR 의 한계 넷과 k8s_external"),
    ("§7", "레코드를 좁히는 옵션들", "명세에서 가장 멀리 나간다"),
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
    focal = (i in (3, 4))
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 632, "기능마다 값을 두 번 센다 — 무엇을 얻는가, 그 대가로 무엇을 내주는가", 13, MUTED, KR, "start")
d.t(20, 656, "대가는 이식성이거나 메모리이거나 둘 다다", 13, MUTED, KR, "start")

d.legend(684, [("한 이야기로 이어지는 두 절", ACC)])
d.save("06-04.chapter-overview.svg")
