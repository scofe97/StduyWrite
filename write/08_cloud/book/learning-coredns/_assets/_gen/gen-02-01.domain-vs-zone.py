# 02-01 §2 — 도메인은 서브트리 전체이고, 존은 그 도메인에서 위임해 준 서브도메인을 뺀 나머지다.
# 원문 근거: "A domain is a group of nodes in a particular subtree of the namespace",
#            "A zone is a domain minus the subdomains that have been delegated elsewhere",
#            "if there's no further delegation below cs.berkeley.edu, the domain cs.berkeley.edu
#             and the zone cs.berkeley.edu are effectively the same",
#            edu 도메인은 EDUCAUSE 가 운영하며 berkeley.edu·umich.edu 를 위임하고 edu 존을 직접 관리한다.
# 타입 스펙: type-nested — 포함으로 계층을 보이고, 링 사이의 띠 하나가 곧 그 층의 존이다.
# 2026-09-23 개정: 존을 글로 설명하던 하단 문장을 걷고, berkeley.edu 존인 띠 자체를 칠해 보이게 했다.
#                  테두리 위 라벨 knockout 사각형이 shape-overlap 을 내서 라벨을 상자 안으로 옮겼다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 02-01 §2",
      "도메인은 통째, 존은 위임하고 남은 만큼",
      "바깥 사각형이 도메인이고, 링과 링 사이의 띠 하나가 그 도메인의 존이다. "
      "berkeley.edu 도메인은 cs.berkeley.edu 를 품지만 berkeley.edu 존은 그 안쪽을 품지 않는다. "
      "위임한 쪽 존에는 cs.berkeley.edu 를 어디서 찾는지 알려 주는 NS 와, 필요하면 그 서버 주소인 글루만 남는다.",
      "칠한 띠만큼이 berkeley.edu 존입니다")

# 링 stride — 바깥에서 안으로 좌우 32px, 위 48px(라벨 두 줄 자리), 아래 32px 씩 줄인다
EDU = (40, 96, 800, 344)
BERK = (72, 144, 736, 264)
CS = (104, 240, 672, 136)

# edu 도메인 — 무채색 링
d.box(*EDU, PAPER, RULE, 0.9, 8)
d.t(EDU[0] + 18, EDU[1] + 22, "edu 도메인", 12, SOFT, MONO, "start", 600)
d.t(EDU[0] + EDU[2] - 18, EDU[1] + 22, "edu 존 · EDUCAUSE 관리", 12, MUTED, KR, "end")

# berkeley.edu 도메인 — 칠한 부분이 곧 berkeley.edu 존
d.tone(*BERK, ACC, 8, "14", 1.4)
d.t(BERK[0] + 18, BERK[1] + 24, "berkeley.edu 도메인", 12, ACC, MONO, "start", 600)
d.t(BERK[0] + 18, BERK[1] + 48, "berkeley.edu 존 · Berkeley IT 관리", 14, ACC, KR, "start", 600)
d.chip(BERK[0] + BERK[2] - 130, BERK[1] + 64, "cs 로 가는 NS · 글루만 남음", ACC)

# cs.berkeley.edu — 위임받아 따로 관리. 하위 위임이 없으니 도메인 = 존
d.box(*CS, PAPER2, INFO, 1.4, 8)
d.t(CS[0] + 18, CS[1] + 24, "cs.berkeley.edu 도메인 = 존", 12, INFO, MONO, "start", 600)
d.t(CS[0] + CS[2] / 2, CS[1] + 72, "CS 학과 관리 · 하위 위임 없음", 14, INK, KR, "middle", 600)
d.t(CS[0] + CS[2] / 2, CS[1] + 98, "Berkeley IT 관여 없음", 12, MUTED)

d.legend(460, [("berkeley.edu 존 · 위임하고 남은 띠", ACC), ("위임받은 존", INFO)])
d.save("02-01.domain-vs-zone.svg")
