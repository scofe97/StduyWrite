# 01-04 개요 — 분산을 쓰는 아홉 이유에서 출발해 부분 실패와 그 파생 문제, 단일 노드 우선 권고로 이어지고, 마이크로서비스·서버리스와 클라우드 대 HPC 비교까지 절 순서로 놓은 편 전체 지도.
# 사실 출처: 01-04 서두(L28), §1(L38~L50), §2(L53~L65), §3(L67~L76), §4(L78~L111), §5(L113~L126)
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

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
C_Y = B_Y + B_H + 32
C_H = HEAD + 16 + 2 * CHIP_H + 8 + 16
LEG = C_Y + C_H + 16
H = LEG + 56

reasons = ["본질적 분산", "서비스 간 요청", "내결함성·고가용성",
           "확장성", "지연", "탄력성",
           "특화 하드웨어", "법적 준수", "지속 가능성"]
costs = ["느린 네트워크 호출", "더 많은 노드가 항상 빠르진 않음", "진단의 어려움", "서비스 간 일관성"]
single = ["CPU·메모리·디스크 향상", "DuckDB·SQLite·KùzuDB", "분산을 서두르지 않기"]
micro = ["마이크로서비스 — 팀이 독립적으로 일하게 함", "서버리스 — 사용량 기준 미터링 과금"]
hpc = ["HPC — 노드가 죽으면 전체 정지 후 재시작", "클라우드 — 부분 실패를 견디며 계속 응답"]

d = D(W, H, "01-04 · DISTRIBUTED VS SINGLE NODE", "분산의 이유·대가, 단일 노드 재부상, 분산 방식과 HPC 전체 지도",
      "분산을 쓰는 아홉 이유(§1)에서 출발해 부분 실패와 파생 문제(§2)를 거쳐 단일 노드 우선 권고(§3)로 이어지고, 마이크로서비스·서버리스(§4)와 클라우드 대 HPC(§5)까지 조망한다. 단일 노드 상자가 핵심 논점이다.",
      "분산의 아홉 이유 · 부분 실패와 파생 문제 · 단일 노드 재부상 · 분산 방식과 HPC")

d.box(PX, A_Y, PW, A_H, PAPER2, RULE, 1.0)
d.t(PX + 16, A_Y + 28, "분산을 쓰는 이유", 14, INK, KR, "start", 600)
d.chip(PX + PW - 32, A_Y + 24, "§1", INFO, 11)
for i, txt in enumerate(reasons):
    r, c = divmod(i, 3)
    x = PX + 16 + c * (A_CH_W + A_GAP)
    y = A_Y + HEAD + 16 + r * CSTR
    d.box(x, y, A_CH_W, CHIP_H, PAPER, RULE, 0.9)
    d.t(x + 16, y + 21, txt, 13, INK, KR, "start")

d.arrow([(PX + BW / 2, A_Y + A_H + 4), (PX + BW / 2, B_Y - 8)], MUTED, "ar", 1.6)

d.box(PX, B_Y, BW, B_H, PAPER2, WARN, 1.2)
d.t(PX + 16, B_Y + 28, "분산의 대가 — 부분 실패와 그 파생 문제", 14, INK, KR, "start", 600)
d.chip(PX + BW - 32, B_Y + 24, "§2", WARN, 11)
for j, txt in enumerate(costs):
    y = B_Y + HEAD + 16 + j * CSTR
    d.box(PX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(PX + 32, y + 21, txt, 13, INK, KR, "start")

d.arrow([(PX + BW + 4, B_Y + B_H / 2), (CX - 8, B_Y + B_H / 2)], MUTED, "ar", 1.6)

d.box(CX, B_Y, BW, B_H, PAPER2, ACC, 1.4)
d.o.append(f'<rect x="{CX}" y="{B_Y}" width="{BW}" height="{B_H}" rx="6" fill="{ACC}1F" stroke="none"/>')
d.t(CX + 16, B_Y + 28, "단일 노드의 재부상", 14, INK, KR, "start", 600)
d.chip(CX + BW - 32, B_Y + 24, "§3", ACC, 11)
for j, txt in enumerate(single):
    y = B_Y + HEAD + 16 + j * CSTR
    d.box(CX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(CX + 32, y + 21, txt, 13, INK, MONO if txt.isascii() or "·" in txt and "분산" not in txt and "CPU" not in txt else KR, "start")

d.box(PX, C_Y, BW, C_H, PAPER2, OK, 1.2)
d.t(PX + 16, C_Y + 28, "마이크로서비스와 서버리스", 14, INK, KR, "start", 600)
d.chip(PX + BW - 32, C_Y + 24, "§4", OK, 11)
for j, txt in enumerate(micro):
    y = C_Y + HEAD + 16 + j * CSTR
    d.box(PX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(PX + 32, y + 21, txt, 13, INK, KR, "start")

d.box(CX, C_Y, BW, C_H, PAPER2, OK, 1.2)
d.t(CX + 16, C_Y + 28, "클라우드 컴퓨팅 vs 슈퍼컴퓨팅(HPC)", 14, INK, KR, "start", 600)
d.chip(CX + BW - 32, C_Y + 24, "§5", OK, 11)
for j, txt in enumerate(hpc):
    y = C_Y + HEAD + 16 + j * CSTR
    d.box(CX + 16, y, BW - 32, CHIP_H, PAPER, RULE, 0.9)
    d.t(CX + 32, y + 21, txt, 13, INK, KR, "start")

d.legend(LEG, [("단일 노드부터 검토 (focal)", ACC), ("분산 동기", INFO), ("분산의 대가", WARN), ("분산 방식과 대안", OK)])
d.save("01-04.distributed-vs-single.svg")
