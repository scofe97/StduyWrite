# 타입 스펙: type-architecture
# 1절 Node·Computer·Executor 의 관계 — Controller JVM 의 Executor 슬롯과 단일 Channel 너머 Agent 기계의 JVM·OS 자식 프로세스 분리
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, INFO, KR, MONO)

W, H = 960, 444

d = D(
    W, H,
    "JENKINS · CONTROLLER EXECUTOR & AGENT MACHINE",
    "Executor 슬롯과 Agent 기계의 일 나누기",
    "Controller JVM 안의 Node·Computer·Executor 슬롯 객체와 단일 Channel 너머 Agent 기계의 Agent JVM 및 OS 자식 프로세스 배치",
    lead="Controller JVM 의 Computer 가 쥔 Executor 슬롯과 단일 Channel 너머 Agent 기계의 프로세스 배치"
)


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
    tfam = KR if any("가" <= c <= "힣" for c in label) else MONO
    han = sum(1 for c in label if "가" <= c <= "힣")
    lw = han * 13.0 + (len(label) - han) * 8.2 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 6}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 20, y + 20, label, 13, MUTED, tfam, "start", 600)


def node_box(x, y, w, h, title, sub, stroke=RULE, sw=1.0, title_c=INK, sub_c=MUTED, fill=PAPER2):
    d.box(x, y, w, h, fill, stroke, sw, 6)
    tfam = KR if any("가" <= c <= "힣" for c in title) else MONO
    sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(x + w / 2, y + 26, title, 14, title_c, tfam, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 13, sub_c, sfam, "middle")


# ── Zones (좌: Controller JVM / 우: Agent 기계) ────────────────────────
zone(24, 108, 404, 252, "Controller JVM")
zone(564, 108, 372, 252, "Agent 기계")

# ── Arrows (z-order: behind boxes) ─────────────────────────────────────
# Node -> Computer
d.arrow([(108, 208), (108, 252)], INFO, "info", 1.3)
d.t(100, 234, "실행 상태", 13, MUTED, KR, "end")

# Computer -> Executor #0 (focal) & Executor #1
d.path("M 172 272 H 188 Q 196 272 196 264 V 184 Q 196 176 204 176 H 216", ACC, sw=1.4, m="acc")
d.arrow([(172, 284), (216, 284)], INFO, "info", 1.3)

# Executor #0, #1 -> 단일 Channel 합류 -> Agent JVM
d.path("M 396 176 H 408 Q 416 176 416 184 V 220 Q 416 228 424 228 H 428", ACC, sw=1.4)
d.path("M 396 284 H 408 Q 416 284 416 276 V 236 Q 416 228 424 228 H 428", INFO, sw=1.3)
d.arrow([(428, 228), (580, 228)], ACC, "acc", 1.6)
d.t(496, 212, "Channel", 13, ACC, MONO, "middle", 600)
d.t(496, 248, "빌드 Callable 전송", 13, MUTED, KR, "middle")

# Agent JVM -> OS 자식 프로세스 (JVM 밖)
d.path("M 712 216 H 736 Q 744 216 744 208 V 184 Q 744 176 752 176 H 776", OK, sw=1.3, m="ok")
d.path("M 712 240 H 736 Q 744 240 744 248 V 276 Q 744 284 752 284 H 776", OK, sw=1.3, m="ok")

# ── Controller JVM 내부 노드 ───────────────────────────────────────────
node_box(40, 144, 132, 64, "Node", "노드 설정 객체", RULE, 1.0)
node_box(40, 252, 132, 64, "Computer", "Executor 목록", INFO, 1.1)

# Focal 1곳: Executor #0 (Controller 쪽 슬롯 객체)
d.tone(216, 144, 180, 64, ACC, r=6, op="12", sw=1.4)
d.t(306, 170, "Executor #0", 14, ACC, MONO, "middle", 600)
d.t(306, 192, "Thread · 필요 시 시작", 13, INK, KR, "middle")

node_box(216, 252, 180, 64, "Executor #1", "Thread · 필요 시 시작", INFO, 1.1)

# ── Agent 기계 내부: Agent JVM (1개) 과 OS 자식 프로세스 (JVM 밖) ──────
d.box(580, 188, 132, 80, PAPER2, INFO, 1.2, 6)
d.t(646, 212, "Agent JVM", 14, INK, MONO, "middle", 600)
d.t(646, 232, "remoting.jar", 13, MUTED, MONO, "middle")
d.t(646, 254, "프로세스 1개", 13, INFO, KR, "middle")

node_box(776, 144, 144, 64, "OS 자식 #0", "sh · mvn 프로세스", OK, 1.1)
node_box(776, 252, 144, 64, "OS 자식 #1", "sh · mvn 프로세스", OK, 1.1)

# ── Legend ─────────────────────────────────────────────────────────────
d.legend(388, [
    ("핵심 경로", ACC),
    ("Controller · Agent 객체", INFO),
    ("OS 자식 프로세스", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.executor-slots.svg")
d.save(out_path)
print(f"saved: {out_path}")
