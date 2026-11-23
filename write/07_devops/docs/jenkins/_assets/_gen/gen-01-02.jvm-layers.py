# 타입 스펙: type-deployment
# 3절 Agent 기계의 프로세스 겹(Agent JVM → 셸 → 빌드 JVM)과 옵션을 넣는 두 자리가 닿는 JVM
"""01-02 Agent 노드의 JVM 두 겹 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-02.jvm-layers.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC,  # noqa: E402
                INFO, KR, MONO)

W, H = 960, 528

d = D(
    W, H,
    "JENKINS · AGENT JVM LAYERS & OPTION PATHS",
    "Agent 기계의 프로세스 겹과 옵션이 닿는 길",
    "Controller 의 JVM Options 칸은 Launch agent 때 Agent JVM 의 명령줄에만 닿고, 노드 환경 변수는 빌드마다 셸을 거쳐 빌드 JVM 에 닿는다",
    lead="JVM Options 는 다시 연결해야 Agent JVM 에 반영되고, 노드 환경 변수는 다음 빌드부터 빌드 JVM 에 반영됩니다",
)


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
    lw = sum(12 * (1.0 if "가" <= c <= "힣" else 0.62) for c in label) + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw:.0f}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 20, y + 17, label, 12, SOFT, KR, "start", 600)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO


def node_box(x, y, w, h, title, sub, stroke=RULE, sw=1.0, title_c=INK, sub_c=MUTED, tone=None):
    if tone:
        d.tone(x, y, w, h, tone, r=6, op="12", sw=1.4)
    else:
        d.box(x, y, w, h, PAPER2, stroke, sw, 6)
    d.t(x + w / 2, y + 26, title, 14, title_c, fam(title), "middle", 600)
    d.t(x + w / 2, y + 48, sub, 13, sub_c, fam(sub), "middle")


# 행 좌표: stride 108
R1, R2, R3 = 144, 252, 360
BH = 64
CX = 600                      # Agent 기계 노드 중심 x
AX, AW = 472, 256             # Agent 기계 노드 x, 폭
CBX, CBW = 40, 232            # Controller 쪽 박스 x, 폭
MIDX = (288 + 440) // 2       # 두 존 사이 가운데 x

zone(24, 104, 264, 244, "Controller")
zone(440, 104, 496, 352, "Agent 기계")

# ── 화살표 (박스 뒤) ───────────────────────────────────────────────────
# 부모 → 자식 프로세스
d.arrow([(CX, R1 + BH), (CX, R2)], MUTED, "ar", 1.4)
d.t(CX + 12, R1 + BH + 28, "sh step 이 띄움", 13, MUTED, KR, "start")
d.arrow([(CX, R2 + BH), (CX, R3)], ACC, "acc", 1.4)
d.t(CX + 12, R2 + BH + 28, "mvn · gradle 실행", 13, MUTED, KR, "start")

# 길 A: JVM Options → Agent JVM (명령줄)
yA = R1 + 32
d.arrow([(CBX + CBW, yA), (AX, yA)], INFO, "info", 1.5)
d.t(MIDX, yA - 10, "java ‹JVM Options›", 12, INFO, MONO, "middle", 600)
d.t(MIDX, yA + 22, "다시 연결해야 반영", 13, MUTED, KR, "middle")

# 길 B: 노드 환경 변수 → 셸 (빌드마다)
yB = R2 + 32
d.arrow([(CBX + CBW, yB), (AX, yB)], ACC, "acc", 1.5)
d.t(MIDX, yB - 10, "buildEnvironment", 12, ACC, MONO, "middle", 600)
d.t(MIDX, yB + 22, "다음 빌드부터 반영", 13, MUTED, KR, "middle")

# ── Controller 쪽 설정 자리 ───────────────────────────────────────────
node_box(CBX, R1, CBW, BH, "JVM Options", "노드 설정 Advanced 칸", INFO, 1.1)
node_box(CBX, R2, CBW, BH, "노드 환경 변수", "JAVA_TOOL_OPTIONS", ACC, 1.1)

# ── Agent 기계의 프로세스 겹 ──────────────────────────────────────────
node_box(AX, R1, AW, BH, "Agent JVM", "remoting.jar", tone=INFO)
node_box(AX, R2, AW, BH, "셸", "sh -c …", MUTED, 1.0)
node_box(AX, R3, AW, BH, "빌드 JVM", "JAVA_TOOL_OPTIONS 읽음", tone=ACC, title_c=ACC)

# 수명 칩
d.chip(836, R1 + 32, "상시 실행", INFO, 13)
d.chip(836, R2 + 32, "step 마다 새로", MUTED, 13)
d.chip(836, R3 + 32, "빌드 동안만", ACC, 13)

d.legend(480, [
    ("JVM Options 길", INFO),
    ("환경 변수 길", ACC),
    ("부모 → 자식 프로세스", MUTED),
])

out_path = pathlib.Path(__file__).resolve().parent.parent / "01-02.jvm-layers.svg"
d.save(str(out_path))
print("saved", out_path)
