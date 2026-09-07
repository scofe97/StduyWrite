# 타입 스펙: type-architecture — 같은 라우터 넷을 두 가지 제어 배선으로 나란히 놓는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.1 Figure 5.1 · Figure 5.2
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 652
d = D(W, H, "SECTION 5.1 · WHO COMPUTES THE TABLE",
      "표를 채우는 배선이 둘입니다",
      "라우터마다 제어와 논리적 중앙 제어를 같은 라우터 넷 위에 나란히 그린 비교. 왼쪽은 라우팅 컴포넌트끼리 대화하고, 오른쪽은 컨트롤러만 대화하며 제어 에이전트는 시키는 대로만 한다.",
      "데이터 평면은 양쪽이 같습니다. 다른 것은 표를 누가 계산하느냐입니다")

BW, BH = 150, 60
d.box(20, 130, 460, 330, f"{INK}05", RULE, 1.0, 10)
d.box(500, 130, 480, 330, f"{INK}05", RULE, 1.0, 10)
d.t(250, 118, "라우터마다 제어 — Figure 5.1", 12, INK, KR, "middle", 600)
d.t(740, 118, "논리적 중앙 제어 — Figure 5.2", 12, INK, KR, "middle", 600)


def router(x, y, name, sub, c):
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(x + BW / 2, y + 25, name, 12, INK, MONO, "middle", 600)
    d.t(x + BW / 2, y + 44, sub, 11, c, KR)


L = [(80, 250), (270, 250), (80, 360), (270, 360)]
for i, (x, y) in enumerate(L):
    router(x, y, f"라우터 {i + 1}", "라우팅 컴포넌트", ACC)
# 라우팅 컴포넌트끼리의 대화 — 제어 평면이 라우터 안에 흩어져 있다
d.line(230, 280, 270, 280, ACC, 1.6)
d.line(230, 390, 270, 390, ACC, 1.6)
d.line(155, 310, 155, 360, ACC, 1.6)
d.line(345, 310, 345, 360, ACC, 1.6)

R = [(565, 250), (755, 250), (565, 360), (755, 360)]
for i, (x, y) in enumerate(R):
    router(x, y, f"라우터 {i + 1}", "제어 에이전트 CA", INFO)
d.t(250, 174, "제어 평면이 라우터 안에 흩어져 있습니다", 11, MUTED, KR)
d.t(250, 192, "따로 놓인 상자가 없습니다", 11, SOFT, KR)

d.tone(610, 150, 250, 56, ACC, 7, "12", 1.5)
d.t(735, 174, "원격 컨트롤러", 12, ACC, KR, "middle", 600)
d.t(735, 192, "표를 계산해 내려보냅니다", 11, MUTED, KR)
for dpath in ("M 705 206 L 705 228 L 640 228 L 640 250",
              "M 765 206 L 765 228 L 830 228 L 830 250",
              "M 675 206 L 675 228 L 522 228 L 522 390 L 565 390",
              "M 795 206 L 795 228 L 948 228 L 948 390 L 905 390"):
    d.path(dpath, INFO, 1.3, m="info", dash="5 5")

d.t(250, 486, "제어 컴포넌트끼리 직접 이야기합니다", 11, ACC, KR)
d.t(740, 486, "CA 끼리는 이야기하지 않습니다", 11, INFO, KR)

d.t(20, 522, "왼쪽은 OSPF 와 BGP 가 수십 년간 쓴 방식이고, 오른쪽은 SDN 이 택한 방식입니다.", 11, MUTED, KR, "start")
d.t(20, 542, "\"논리적\"이라 부르는 까닭은 컨트롤러가 장애 대비와 성능 때문에 실제로는 여러 서버로 구현되기 때문입니다.",
     11, MUTED, KR, "start")

d.legend(568, [("제어 평면의 대화", ACC), ("컨트롤러가 내리는 지시", INFO), ("데이터 평면 장비", MUTED)])
d.t(960, 616, "KUROSE-ROSS 9E FIG 5.1 · FIG 5.2", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.control-models.svg"
d.save(out)
print("→", out)
