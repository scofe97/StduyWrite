# 02-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 680
d = D(W, H, "LEARNING COREDNS · 02-01",
      "위임이 그은 경계가 질의 경로를 정한다",
      "2장 전반부의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 이름과 경계와 데이터라는 재료이고, "
      "4~5절이 그 재료를 들고 있는 서버와 리졸버, 6~7절이 실제 질의가 흐르는 경로다.",
      "2절의 도메인과 존 구분이 나머지 전부를 떠받칩니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "이름은 트리의 한 노드다", "레이블 63자, 경로가 곧 이름"),
    ("§2", "도메인과 존은 다르다", "위임하고 남은 만큼이 존"),
    ("§3", "데이터는 레코드에 담긴다", "클래스는 사실상 IN 하나"),
    ("§4", "권한은 존 단위로 붙는다", "주 서버도 보조 서버도 권한"),
    ("§5", "리졸버는 OS 안에 있다", "앱은 DNS 프로토콜을 모른다"),
    ("§6", "재귀는 누가 지는가", "재귀 질의와 반복 질의"),
    ("§7", "캐싱이 루트를 구한다", "TTL 만큼 사다리를 건너뛴다"),
]
def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(620, [("나머지를 떠받치는 구분", ACC)])
d.save("02-01.chapter-overview.svg")
