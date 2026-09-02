# 04-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 680
d = D(W, H, "LEARNING COREDNS · 04-01",
      "존 데이터를 어디에 둘지가 관리 방식을 정한다",
      "4장의 절 여섯을 읽는 순서로 이은 지도. 1절이 네 갈래의 지도이고, "
      "2~4절이 파일 계열, 5~6절이 파일이 아닌 두 갈래다.",
      "3절의 auto 가 이 장이 3장에 더하는 핵심입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "네 갈래를 먼저 본다", "무엇이 다른지가 선택 기준"),
    ("§2", "file — 가장 익숙한 길", "존 하나에 파일 하나"),
    ("§3", "auto — 디렉터리를 읽는다", "파일만 놓으면 존이 는다"),
    ("§4", "auto 와 Git", "존 데이터에 이력이 붙는다"),
    ("§5", "hosts — 존이 아닌 몇 줄", "SOA 가 없어 전송도 못 한다"),
    ("§6", "route53 — AWS 에서 당긴다", "보조 서버처럼 동기화한다"),
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
    x, y = pos(i); focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(620, [("3장에 이 장이 더하는 것", ACC)])
d.save("04-01.chapter-overview.svg")
