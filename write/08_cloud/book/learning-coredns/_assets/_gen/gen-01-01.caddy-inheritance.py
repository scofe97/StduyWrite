# 01-01 §2 — Caddy 를 포크하면서 물려받은 세 가지와 그것이 CoreDNS 에서 취한 모습.
# 원문 근거: "CoreDNS thus inherited the major advantages of Caddy: its simple configuration
#            syntax, its powerful plug-in-based architecture, and its foundation in Go."
# 타입 스펙: type-tree — 부모(Caddy) 에서 자식 셋으로 갈라지고 각 자식이 결과 하나를 갖는 2단 계보.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 940, 468
d = D(W, H, "LEARNING COREDNS · 01-01 §2",
      "Caddy 에서 물려받은 세 가지",
      "Miek Gieben 은 Caddy 의 아키텍처를 높이 사 그것을 포크해 CoreDNS 를 만들었다. "
      "물려받은 것은 단순한 설정 문법, 플러그인 기반 아키텍처, Go 기반 셋이며 아랫줄이 각각 CoreDNS 에서 취한 모습이다.",
      "이 셋이 곧 2절에서 4절까지의 뼈대입니다")

NW, NH = 200, 56
CX = [208, 468, 728]
ROOT_Y, MID_Y, LEAF_Y = 96, 216, 312
BUS_Y = 184

# 연결선 먼저
d.line(468, ROOT_Y + NH, 468, BUS_Y, MUTED, 1.0)
d.line(CX[0], BUS_Y, CX[2], BUS_Y, MUTED, 1.0)
for cx in CX:
    d.line(cx, BUS_Y, cx, MID_Y, MUTED, 1.0)
    d.line(cx, MID_Y + NH, cx, LEAF_Y, MUTED, 1.0)

# 루트
d.tone(468 - NW / 2, ROOT_Y, NW, NH, ACC, 6, "12", 1.4)
d.t(468, ROOT_Y + 26, "Caddy", 16, ACC, MONO, "middle", 600)
d.t(468, ROOT_Y + 46, "Go 웹 서버", 13, MUTED)

mids = [("단순한 설정 문법", "BIND 설정과 대비"),
        ("플러그인 아키텍처", "기능을 플러그인이 낸다"),
        ("Go 기반", "메모리 안전한 언어")]
leaves = [("Corefile", "몇 줄로 끝난다"),
          ("선택한 것만 실행", "안 켠 코드는 안 돈다"),
          ("메모리 접근 오류 없음", "버퍼 오버플로 차단")]
for i, cx in enumerate(CX):
    nm, sub = mids[i]
    d.box(cx - NW / 2, MID_Y, NW, NH, PAPER2, RULE, 1.0)
    d.t(cx, MID_Y + 26, nm, 14, INK, KR, "middle", 600)
    d.t(cx, MID_Y + 46, sub, 13, MUTED)
    nm, sub = leaves[i]
    d.box(cx - NW / 2, LEAF_Y, NW, NH, PAPER2, RULE, 0.8)
    d.t(cx, LEAF_Y + 26, nm, 14, INK, KR, "middle", 600)
    d.t(cx, LEAF_Y + 46, sub, 13, MUTED)

d.t(12, LEAF_Y + 30, "CoreDNS 에서", 12, SOFT, MONO, "start")
d.t(12, MID_Y + 30, "물려받은 것", 12, SOFT, KR, "start")
d.legend(400, [("포크의 출발점", ACC)])
d.save("01-01.caddy-inheritance.svg")
