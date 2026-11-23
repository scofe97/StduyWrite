# 타입 스펙: type-architecture
# 2절 Agent 를 떼어도 남는 요청 통로 — 빌드 지시는 Controller 에서 Agent 로, 요청은 Agent 에서 접근 제어를 거쳐 Controller 로
"""01-01 Agent → Controller 요청 통로 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-01.agent-to-controller.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, WARN, BAD, INFO, KR, MONO)

W, H = 960, 440

d = D(
    W, H,
    "JENKINS · AGENT TO CONTROLLER REQUEST PATH",
    "Agent 를 떼어도 남는 요청 통로",
    "Controller 가 Agent 에 빌드를 지시하고 Agent 는 파일 내용과 명령 실행을 Controller 에 요청할 수 있으며 접근 제어가 요청을 통과시키거나 막는다",
    lead="빌드를 Agent 로 옮겨도 Agent 에서 Controller 로 오는 요청은 접근 제어에서 통과하거나 막힌다"
)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
    han = sum(1 for c in label if "가" <= c <= "힣")
    lw = han * 13.0 + (len(label) - han) * 8.2 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 6}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 20, y + 20, label, 13, MUTED, fam(label), "start", 600)


zone(24, 100, 912, 284, "분산 프로세스로 본 Controller·Agent")

# 화살표를 먼저(상자 뒤)
d.arrow([(250, 172), (710, 172)], INFO, "info", 1.5)
d.t(480, 160, "빌드 지시", 13, INFO, KR, "middle", 600)

# Agent 의 요청 하나가 접근 제어로
d.arrow([(710, 296), (560, 296)], WARN, "warn", 1.5)
d.t(635, 262, "파일 내용 ·", 13, WARN, KR, "middle", 600)
d.t(635, 280, "명령 실행 요청", 13, WARN, KR, "middle", 600)

# 접근 제어에서 두 갈래: 통과 / 막힘
d.arrow([(400, 268), (250, 268)], OK, "ok", 1.5)
d.t(325, 254, "통과", 13, OK, KR, "middle", 600)
d.t(325, 290, "Controller 역할 대상", 13, MUTED, KR)
d.path("M 400 332 H 336", BAD, 1.5)
d.line(324, 326, 336, 338, BAD, 1.8)
d.line(324, 338, 336, 326, BAD, 1.8)
d.t(368, 318, "막힘", 13, BAD, KR, "middle", 600)
d.t(325, 356, "그 밖의 Callable", 13, MUTED, KR)

# 양 끝 상자
d.box(44, 140, 206, 212, PAPER2, INFO, 1.2, 6)
d.t(147, 172, "Controller", 14, INK, MONO, "middle", 600)
d.t(147, 196, "제어 쪽 프로세스", 13, MUTED, KR)

d.box(710, 140, 206, 212, PAPER2, INFO, 1.2, 6)
d.t(813, 172, "Agent", 14, INK, MONO, "middle", 600)
d.t(813, 196, "작업 쪽 프로세스", 13, MUTED, KR)

# focal: 접근 제어
d.tone(400, 232, 160, 124, ACC, r=6, op="12", sw=1.4)
d.t(480, 270, "Agent → Controller", 13, ACC, MONO, "middle", 600)
d.t(480, 290, "접근 제어", 14, ACC, KR, "middle", 600)
d.t(480, 330, "2.326 부터 항상 켜짐", 12, INK, KR)

d.legend(396, [
    ("빌드 지시", INFO),
    ("Agent 의 요청", WARN),
    ("접근 제어", ACC),
    ("통과", OK),
    ("막힘", BAD),
])

out = pathlib.Path(__file__).resolve().parent.parent / "01-01.agent-to-controller.svg"
d.save(str(out))
print("saved", out)
