# 타입 스펙: type-data-flow — 단계마다 누가 무엇을 하는지. 화살표 아래 라벨이 그 구간의 링크 프로토콜이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.1 Figure 6.1 과 그 본문의 여섯 링크 열거 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, WARN, KR, MONO

W, H = 1000, 432
d = D(W, H, "SECTION 6.1 · SIX LINK-LAYER HOPS",
      "한 경로가 여섯 칸으로 나뉩니다",
      "무선 호스트에서 서버까지 데이터그램이 지나는 여섯 링크. 칸마다 링크 계층 프로토콜이 다르고, 프레임은 칸마다 새로 만들어진다.",
      "원문이 열거한 여섯 링크 그대로입니다")

NODES = [("무선 호스트", "host"), ("WiFi AP", "ap"), ("스위치", "switch"),
         ("라우터", "router"), ("라우터", "router"), ("스위치", "switch"), ("서버", "host")]
LINKS = ["WiFi", "이더넷", "원문 미지정", "원문 미지정", "이더넷", "이더넷"]
LINK_C = [WARN, INFO, MUTED, MUTED, INFO, INFO]

BW, BH, STRIDE, X0, NY = 96, 48, 136, 42, 116
cx = [X0 + i * STRIDE + BW / 2 for i in range(7)]

for i, (name, kind) in enumerate(NODES):
    x = X0 + i * STRIDE
    d.box(x, NY, BW, BH, PAPER2, RULE, 0.9)
    d.t(cx[i], NY + 21, name, 12, INK, KR, "middle", 600)
    d.t(cx[i], NY + 38, kind, 10, MUTED, MONO)

# 링크 여섯 — 노드 사이 화살표 + 그 아래 프로토콜 라벨
for i in range(6):
    x1, x2 = cx[i] + BW / 2 + 4, cx[i + 1] - BW / 2 - 6
    d.arrow([(x1, NY + 24), (x2, NY + 24)], LINK_C[i], "ar", 1.5)
    mid = (cx[i] + cx[i + 1]) / 2
    d.t(mid, NY + 76, f"링크 {i + 1}", 10, SOFT, MONO)
    d.t(mid, NY + 94, LINKS[i], 11, LINK_C[i], KR, "middle", 600)
    d.line(mid, NY + 30, mid, NY + 62, RULE, 0.8, "3 5")

d.line(24, 244, W - 48, 244, RULE, 0.8)

# 아래 띠 — 데이터그램은 그대로, 프레임은 칸마다 새로
d.t(24, 274, "칸마다 무엇이 바뀌고 무엇이 그대로인가", 12, INK, KR, "start", 600)

FY, FH, FW = 292, 52, 214
for i, (lab, proto) in enumerate([("WiFi 프레임", "802.11"), ("이더넷 프레임", "802.3"), ("이더넷 프레임", "802.3")]):
    x = 24 + i * 246
    d.box(x, FY, FW, FH, PAPER2, RULE, 0.9)
    d.t(x + 12, FY + 20, lab, 11, INK, KR, "start", 600)
    d.t(x + FW - 12, FY + 20, proto, 10, MUTED, MONO, "end")
    d.tone(x + 12, FY + 28, FW - 24, 16, ACC, 3, "14", 1.0)
    d.t(x + FW / 2, FY + 40, "같은 데이터그램", 10, ACC, KR)
    if i < 2:
        d.arrow([(x + FW + 4, FY + 26), (x + 240, FY + 26)], MUTED, "ar", 1.3)

d.box(768, FY, 208, FH, PAPER2, f"{ACC}55", 1.4, 6)
d.t(872, FY + 22, "헤더는 매번 새로 붙고", 11, MUTED, KR)
d.t(872, FY + 40, "안의 데이터그램은 그대로", 11, ACC, KR, "middle", 600)

d.t(24, 372, "링크 3 과 링크 4 는 원문이 프로토콜을 밝히지 않습니다. "
             "\"a link between the link-layer switch and the router, a link between the two routers\" 라고만 적습니다.",
     11, MUTED, KR, "start")

d.legend(388, [("칸을 건너도 그대로인 것", ACC), ("무선 링크", WARN), ("유선 이더넷", INFO), ("원문 미지정", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-01.six-hops.svg"
d.save(out)
print("→", out)
