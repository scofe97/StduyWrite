# 02-01 §2 — 도메인은 서브트리 전체이고, 존은 그 도메인에서 위임해 준 서브도메인을 뺀 나머지다.
# 원문 근거: "A domain is a group of nodes in a particular subtree of the namespace",
#            "A zone is a domain minus the subdomains that have been delegated elsewhere",
#            "if there's no further delegation below cs.berkeley.edu, the domain cs.berkeley.edu
#             and the zone cs.berkeley.edu are effectively the same",
#            edu 도메인은 EDUCAUSE 가 운영하며 berkeley.edu·umich.edu 를 위임하고 edu 존을 직접 관리한다.
# 타입 스펙: type-nested — 포함으로 계층을 보이고, 링 사이의 띠 하나가 곧 그 층의 존이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING COREDNS · 02-01 §2",
      "도메인은 통째, 존은 위임하고 남은 만큼",
      "바깥 사각형이 도메인이고, 링과 링 사이의 띠 하나가 그 도메인의 존이다. "
      "위임할 때마다 안쪽 사각형이 하나 생기고 그만큼이 바깥 존에서 빠져나간다.",
      "띠 하나가 관리 주체 하나에 대응합니다")

rings = [
    (40, 96, 800, 344, "edu 도메인", "edu 존 · EDUCAUSE 가 직접 관리", MUTED),
    (72, 132, 736, 272, "berkeley.edu 도메인", "berkeley.edu 존 · Berkeley IT 부서", MUTED),
    (104, 168, 672, 200, "cs.berkeley.edu 도메인", "", ACC),
]
for i, (x, y, w, h, label, band, color) in enumerate(rings):
    if color is ACC:
        d.tone(x, y, w, h, ACC, 8, "0A", 1.4)
    else:
        d.box(x, y, w, h, PAPER, RULE, 0.9 + i * 0.2, 8)
    d.o.append(f'<rect x="{x + 14}" y="{y - 8}" width="{len(label) * 8 + 20}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 12, ACC if color is ACC else SOFT, MONO, "start", 600)
    if band:
        d.t(x + w - 20, y + 26, band, 13, MUTED, KR, "end")

d.t(440, 236, "위임이 없으면 도메인과 존이 같다", 15, ACC, KR, "middle", 600)
d.t(440, 262, "cs.berkeley.edu 아래로 더 위임하지 않는 한", 13, MUTED)
d.t(440, 300, "CS 학과가 이 안의 노드를 직접 관리하고", 13, MUTED)
d.t(440, 324, "Berkeley IT 는 더 이상 관여하지 않는다", 13, MUTED)

d.t(440, 476, "berkeley.edu 도메인은 cs.berkeley.edu 를 품지만, berkeley.edu 존은 품지 않는다", 14, INK, KR, "middle", 600)
d.t(440, 500, "위임한 쪽에는 \"어디로 가면 찾을 수 있는지\"만 남는다", 13, MUTED)

d.legend(524, [("위임받아 따로 관리되는 도메인", ACC)])
d.save("02-01.domain-vs-zone.svg")
