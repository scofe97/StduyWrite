# 01-04 도입 — 분산을 쓰는 이유 아홉, 그 대가, 그래서 단일 노드부터 검토하라는 권고까지의 흐름 지도.
# 옛 도식은 이유·대가·단일 노드·클라우드 대 HPC 를 문장 불릿으로 채웠다. HPC 는 §5 본문이 맡고, 여기서는 도입 단락이
#   예고하는 세 걸음(이유 → 대가 → 단일 노드)만 라벨로 남겼다.
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

W = 880
PX, PW = 16, 848
HEAD = 44
CHIP_H, CSTR = 32, 40
A_Y = 104
A_CH_W, A_GAP = 266, 8
A_H = HEAD + 16 + 3 * CHIP_H + 2 * 8 + 16
B_Y = A_Y + A_H + 32
B_H = HEAD + 16 + 4 * CHIP_H + 3 * 8 + 16
BW = 408
CX = PX + BW + 32
LEG = B_Y + B_H + 16
H = LEG + 56

reasons = ["본질적 분산", "서비스 간 요청", "내결함성·고가용성",
           "확장성", "지연", "탄력성",
           "특화 하드웨어", "법적 준수", "지속 가능성"]
costs = ["부분 실패", "느린 네트워크 호출", "진단의 어려움", "서비스 간 일관성"]
single = ["CPU·메모리·디스크 향상", "DuckDB·SQLite·KùzuDB", "분산을 서두르지 않기"]

d = D(W, H, "01-04 · DISTRIBUTED VS SINGLE NODE", "분산을 쓰는 이유와 그 대가",
      "분산에는 아홉 가지 이유가 있지만 부분 실패 같은 대가가 따르므로, 단일 머신으로 유지할 수 있다면 분산을 서두르지 않는 쪽이 책의 권고다. 단일 노드 상자가 핵심 논점이다.",
      "이유 아홉 → 대가 → 단일 노드부터")

d.box(PX, A_Y, PW, A_H, PAPER2, RULE, 1.0)
d.t(PX + 16, A_Y + 28, "분산을 쓰는 이유", 14, INK, KR, "start", 600)
d.t(PX + PW - 16, A_Y + 28, "§1", 11, MUTED, MONO, "end")
for i, txt in enumerate(reasons):
    r, c = divmod(i, 3)
    x = PX + 16 + c * (A_CH_W + A_GAP)
    y = A_Y + HEAD + 16 + r * CSTR
    d.box(x, y, A_CH_W, CHIP_H, PAPER, RULE, 0.9)
    d.t(x + 16, y + 21, txt, 13, INK, KR, "start")

d.arrow([(PX + BW / 2, A_Y + A_H + 4), (PX + BW / 2, B_Y - 8)], MUTED, "ar", 1.6)

d.box(PX, B_Y, BW, B_H, PAPER2, WARN, 1.2)
d.t(PX + 16, B_Y + 28, "분산의 대가", 14, INK, KR, "start", 600)
d.t(PX + BW - 16, B_Y + 28, "§2", 11, MUTED, MONO, "end")
for j, txt in enumerate(costs):
    y = B_Y + HEAD + 16 + j * CSTR
    d.box(PX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(PX + 32, y + 21, txt, 13, INK, KR, "start")

d.arrow([(PX + BW + 4, B_Y + B_H / 2), (CX - 8, B_Y + B_H / 2)], MUTED, "ar", 1.6)

d.box(CX, B_Y, BW, B_H, PAPER2, ACC, 1.4)
d.o.append(f'<rect x="{CX}" y="{B_Y}" width="{BW}" height="{B_H}" rx="6" fill="{ACC}1F" stroke="none"/>')
d.t(CX + 16, B_Y + 28, "단일 노드의 재부상", 14, INK, KR, "start", 600)
d.t(CX + BW - 16, B_Y + 28, "§3", 11, MUTED, MONO, "end")
for j, txt in enumerate(single):
    y = B_Y + HEAD + 16 + j * CSTR
    d.box(CX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(CX + 32, y + 21, txt, 13, INK, MONO if txt.isascii() or "·" in txt and "분산" not in txt and "CPU" not in txt else KR, "start")

d.legend(LEG, [("분산의 대가", WARN), ("단일 노드부터 검토", ACC)])
d.save("01-04.distributed-vs-single.svg")
