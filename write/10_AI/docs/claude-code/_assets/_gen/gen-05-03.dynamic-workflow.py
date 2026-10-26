"""Dynamic Workflows의 스크립트 기반 다중 서브에이전트 분기 및 결과 취합 의존 그래프."""
# 타입 스펙: type-dependency
# 사실 출처: 05-03.Background Tasks.md:164-200 · 원문 09-advanced-features/README.md (Dynamic Workflows 절)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 560
NW, NH = 160, 56

d = D(
    W, H,
    "DYNAMIC WORKFLOWS · DEPENDENCY GRAPH",
    "동적 워크플로의 서브에이전트 분기 및 취합 의존 그래프",
    "조율 스크립트에서 다중 서브에이전트로 작업을 분기하고 결과를 모으며 필요하면 상호 검증을 거치는 의존 관계",
    lead="스크립트가 서브에이전트로 작업을 나눠 보내고 결과를 다시 합치며, 필요하면 상호 검증을 끼워 넣습니다",
)

# 1. 노드 렌더 함수 (표준 패턴 준수: 160x56, rx=6, fan-in 뱃지 8px)
def draw_node(x, y, name, sub, fanin, leaf=False, highest=False, dashed=False):
    fill = f"{INK}08" if leaf else PAPER2
    stroke = INFO if highest else (MUTED if leaf else RULE)
    sw = 1.2 if highest else (1.0 if leaf else 0.8)
    if dashed:
        d.o.append(
            f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-dasharray="5 4"/>'
        )
    else:
        d.box(x, y, NW, NH, fill=fill, stroke=stroke, sw=sw, r=6)
    d.t(x + 14, y + 24, name, 12, INK, KR, "start", 600)
    fam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(x + 14, y + 43, sub, 11, MUTED, fam, "start")

    # Fan-in 뱃지 (우측 상단)
    bw = 32
    d.o.append(f'<rect x="{x + NW - bw - 8}" y="{y + 8}" width="{bw}" height="14" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + NW - bw // 2 - 8, y + 19, f"{fanin} in", 8, SOFT, MONO, "middle")

# 2. 노드 정의 (Rank별 배치)
# Rank 0 (y=108): 조율 스크립트
R0_Y = 108
draw_node(400, R0_Y, "조율 스크립트", "모델이 작성한 스크립트", 0)
d.t(576, R0_Y + 32, "시작 트리거 · ultracode", 11, MUTED, KR, "start")

# Rank 1 (y=228): 서브에이전트 3종
R1_Y = 228
draw_node(160, R1_Y, "서브에이전트 1", "관점 A 검토", 1)
draw_node(400, R1_Y, "서브에이전트 2", "관점 B 검토", 1)
draw_node(640, R1_Y, "서브에이전트 N", "관점 C 검토", 1)

# Rank 2 (y=348): 상호 검증기 (최고 집선 노드 3 in)
R2_Y = 348
draw_node(400, R2_Y, "상호 검증 (선택)", "독립 결과 대조", 3, highest=True, dashed=True)

# Rank 3 (y=436): 최종 보고서 (리프 노드)
R3_Y = 436
draw_node(400, R3_Y, "취합 결과", "결과 재결합", 1, leaf=True)

# 3. 전방 의존 간선 (Rank 0 -> Rank 1)
# 부착점 분산 (12px 이상 간격)
d.arrow([(456, R0_Y + NH), (456, 196), (240, 196), (240, R1_Y)], MUTED, "ar", 1.4)
d.arrow([(480, R0_Y + NH), (480, R1_Y)], MUTED, "ar", 1.4)
d.arrow([(504, R0_Y + NH), (504, 196), (720, 196), (720, R1_Y)], MUTED, "ar", 1.4)

# 4. 수렴 간선 (Rank 1 -> Rank 2: fan-in 3)
d.arrow([(240, R1_Y + NH), (240, 316), (456, 316), (456, R2_Y)], MUTED, "ar", 1.4, "5 4")
d.arrow([(480, R1_Y + NH), (480, R2_Y)], MUTED, "ar", 1.4, "5 4")
d.arrow([(720, R1_Y + NH), (720, 316), (504, 316), (504, R2_Y)], MUTED, "ar", 1.4, "5 4")

# 5. 리프 간선 (Rank 2 -> Rank 3)
d.arrow([(480, R2_Y + NH), (480, R3_Y)], MUTED, "ar", 1.4, "5 4")

# 7. 범례
d.legend(512, [
    ("의존 방향 (하향)", MUTED),
    ("최고 집선 노드 (3 in)", INFO),
    ("점선: 필요 시", SOFT),
])

d.save("05-03.dynamic-workflow.svg")
print("Saved 05-03.dynamic-workflow.svg")
