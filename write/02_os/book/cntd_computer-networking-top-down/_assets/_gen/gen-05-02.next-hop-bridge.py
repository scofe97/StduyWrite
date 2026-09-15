# 타입 스펙: type-architecture — 위는 AS1·AS2 존 안의 라우터와 연결, 아래는 1b 안에서 두 답이 한 줄로 모이는 fan-in.
#       축약: semantic-patterns 의 Fan-in 은 data-flow 를 권하지만, 위쪽 망 모양과 한 장에 두려고 architecture 로 그렸다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.2 NEXT-HOP 정의 · §5.4.3 뜨거운 감자에서 전달 표 항목을 만드는 절차
#       NEXT-HOP 은 "the IP address of the router interface that begins the AS-PATH" 이고,
#       그 주소는 광고를 받은 AS 에 속하지 않지만 그 주소를 담은 서브넷은 직접 붙어 있다.
# 노트의 읽기: 10.0.0.0/30 · 10.0.0.1 · 10.0.0.2 와 인터페이스 이름 I 는 원문에 없는 예시다.
#       원문은 "2a 의 가장 왼쪽 인터페이스 주소" 라고만 적어, 학습자가 "그래서 그게 어느 주소냐" 에서 막혔다.
# 2026-09-13: "1b 가 무엇을 어디서 받는지"와 "두 답을 합쳐 무엇이 나오는지"가 안 보인다는 지적으로 다시 그렸다.
#       같은 질문에서 "OSPF 와 iBGP 가 다른 것이냐"가 함께 나와, 1c→1b 사이에 둘을 나란히 흘렸다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, ACC, INFO, OK, KR, MONO

W, H = 1000, 656
d = D(W, H, "SECTION 5.4.2 · NEXT-HOP",
      "1b 는 두 답을 합쳐 전달 표 한 줄을 만듭니다",
      "1c 는 1b 에게 두 가지를 따로 보낸다. iBGP 로는 밖에서 배운 경로와 NEXT-HOP 주소를, OSPF 로는 AS 안의 링크 상태를 보낸다. 1b 는 NEXT-HOP 주소로 OSPF 가 계산한 길을 찾아 전달 표 항목 (x, I) 를 만든다.",
      "iBGP 는 '어느 출구로'를, OSPF 는 '그 출구까지 어떻게'를 줍니다. 둘은 NEXT-HOP 주소 하나에서 만납니다.")

# ── 위: 망 모양 ─────────────────────────────────────────────
d.box(24, 104, 600, 152, f"{INK}07", f"{MUTED}88", 1.2, 10)
d.box(760, 104, 216, 152, f"{INK}07", f"{MUTED}88", 1.2, 10)
d.t(40, 128, "AS1", 13, INK, MONO, "start", 600)
d.t(776, 128, "AS2", 13, INK, MONO, "start", 600)


def router(x, name, sub):
    d.box(x, 160, 120, 56, PAPER2, MUTED, 1.0, 7)
    d.t(x + 60, 184, name, 16, INK, MONO, "middle", 600)
    d.t(x + 60, 204, sub, 12, MUTED, KR)


# 같은 두 라우터 사이에 서로 다른 것이 두 줄로 흐른다 — 선을 먼저, 상자를 나중에
d.path("M 460 176 L 196 176", INFO, 1.6, m="info", dash="5 4")
d.t(328, 164, "iBGP · 밖에서 배운 경로", 12, INFO, KR)
d.path("M 460 204 L 196 204", OK, 1.6, m="ok")
d.t(328, 232, "OSPF · AS 안의 링크 상태", 12, OK, KR)

d.line(584, 188, 800, 188, MUTED, 1.4)
d.chip(692, 188, "10.0.0.0/30", ACC, 13, 7)

router(72, "1b", "내부 라우터")
router(464, "1c", "게이트웨이")
router(800, "2a", "게이트웨이")
d.t(620, 244, "10.0.0.1", 12, SOFT, MONO, "end")
d.t(764, 244, "10.0.0.2", 12, ACC, MONO, "start", 600)

# ── 아래: 1b 안에서 ────────────────────────────────────────
d.t(24, 296, "1b 안에서 일어나는 일", 13, INK, KR, "start", 600)

# A — BGP 표
d.tone(24, 320, 320, 104, INFO, r=8, op="0C", sw=1.0)
d.t(40, 346, "BGP 표", 13, INFO, KR, "start", 600)
d.t(328, 346, "어느 출구로?", 12, INFO, KR, "end")
d.t(40, 374, "접두어  x", 13, INK, MONO, "start")
d.t(172, 374, "AS-PATH  AS2 AS3", 13, MUTED, MONO, "start")
d.t(40, 402, "NEXT-HOP", 13, MUTED, MONO, "start")
d.t(124, 402, "10.0.0.2", 14, ACC, MONO, "start", 600)

# B — OSPF 가 계산한 길
d.tone(24, 448, 320, 104, OK, r=8, op="0C", sw=1.0)
d.t(40, 474, "OSPF 가 계산한 길", 13, OK, KR, "start", 600)
d.t(328, 474, "그 출구까지 어떻게?", 12, OK, KR, "end")
d.t(40, 502, "10.0.0.0/30", 13, INK, MONO, "start")
d.t(140, 502, "은 1c 에 붙어 있음", 12, MUTED, KR, "start")
d.t(40, 530, "첫 링크", 12, MUTED, KR, "start")
d.t(92, 530, "1c 쪽 인터페이스 I", 13, INK, KR, "start")

# fan-in 연결
d.path("M 344 372 L 372 372 L 372 420 L 396 420", INFO, 1.4, m="info")
d.path("M 344 500 L 372 500 L 372 452 L 396 452", OK, 1.4, m="ok")

# M — NEXT-HOP 으로 맞춰 봄
d.box(400, 384, 240, 104, PAPER2, MUTED, 1.0, 8)
d.t(520, 412, "NEXT-HOP 으로 맞춰 봄", 13, INK, KR, "middle", 600)
d.t(520, 442, "10.0.0.2 → 10.0.0.0/30", 13, ACC, MONO, "middle", 600)
d.t(520, 470, "두 표를 잇는 열쇠", 12, MUTED, KR)

d.path("M 640 436 L 692 436", ACC, 1.6, m="acc")

# C — 결과 (focal)
d.tone(696, 384, 280, 104, ACC, r=8, op="12", sw=1.4)
d.t(836, 412, "전달 표에 적는 한 줄", 13, INK, KR, "middle", 600)
d.t(836, 448, "(x, I)", 20, ACC, MONO, "middle", 600)
d.t(836, 474, "x 행 패킷은 인터페이스 I 로", 12, MUTED, KR)

d.t(24, 584, "iBGP 와 OSPF 는 같은 1c→1b 를 오가되 나르는 것이 다름 — 밖의 접두어 vs 안의 지도", 13, MUTED, KR, "start")

d.legend(608, [("iBGP 가 준 답", INFO), ("OSPF 가 준 답", OK), ("NEXT-HOP 주소와 결과", ACC)])
d.t(960, 648, "KUROSE-ROSS 9E §5.4.2 · §5.4.3 · FIG 5.10", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.next-hop-bridge.svg"
d.save(out)
print("→", out)
