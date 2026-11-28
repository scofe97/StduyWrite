"""kubelet -> CRI -> pause -> app 컨테이너 생성 및 합류 시퀀스.

# 타입 스펙: type-sequence
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO


def _fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class PauseSeq(Seq):
    def lanes(s, names, y0=96, lane_w=160):
        s.LX = {}
        n = len(names)
        margin = 40
        span = (s.w - margin * 2) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = margin + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _fam(nm), "middle", 600)
            s.t(x, y0 + 38, sub, 11, MUTED, _fam(sub))
        s.lane_top = y0 + 48
        return s.LX

    def act(s, who, y_top, h):
        x = s.LX[who]
        s.o.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_top + h}" stroke="rgba(245,245,243,0.08)" stroke-width="8"/>')
        s.o.append(f'<line x1="{x - 4}" y1="{y_top}" x2="{x - 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')
        s.o.append(f'<line x1="{x + 4}" y1="{y_top}" x2="{x + 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 8 * d} {y} L {x2 - 10 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _fam(label), "middle", 600)
        if sub:
            s.t(mx, y + 16, sub, 11, MUTED, _fam(sub), "middle")

    def state_box(s, who, line1, line2, y, c, w=196):
        x = s.LX[who]
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 20}" width="{w}" height="40" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y - 3, line1, 12, c, _fam(line1), "middle", 600)
        s.t(x, y + 13, line2, 11, MUTED, _fam(line2), "middle")


W, H = 880, 568
d = PauseSeq(
    W, H,
    "CRI · POD SANDBOX SEQUENCE",
    "kubelet 의 Pod 샌드박스 생성과 앱 컨테이너 합류",
    "RunPodSandbox 로 containerd 가 만든 netns net:[4026533298] 에 pause(PID 1959)가 합류하고 ipc:[4026533500]·uts:[4026533499] 를 연 뒤, CreateContainer·StartContainer 로 앱(PID 1997→2526)이 합류하고 재시작 뒤에도 pause 와 IP 가 유지되는 흐름.",
    lead="pod-isolated 실측: containerd 가 만든 netns 에 pause 가 합류해 ipc·uts 를 열고, 앱이 이들에 합류합니다",
)

d.lanes([
    ("kubelet", "노드 에이전트"),
    ("CRI", "containerd 2.2"),
    ("pause", "pause:3.10"),
    ("app", "temurin:21-jdk"),
])
d.rails(496)

d.act("kubelet", 160, 320)
d.act("CRI", 168, 124)

# 1. RunPodSandbox -> pause 생성
d.msg("kubelet", "CRI", "RunPodSandbox", 176, INFO, "info", sub="net·ipc: POD / pid: CONTAINER")
d.msg("CRI", "pause", "clone /pause", 216, INFO, "info", sub="PID 1959 · NSpid 1959 1")
d.state_box("pause", "net:[4026533298] 합류", "10.244.0.5 · ipc:[...3500]", 260, OK, w=192)
d.msg("CRI", "kubelet", "sandbox 27f0a452", 288, MUTED, "ar", dash="4 3")

# 2. CreateContainer -> namespace 합류
d.act("CRI", 320, 132)
d.msg("kubelet", "CRI", "CreateContainer", 328, INFO, "info", sub="pod 27f0a452")
gap_pa = (d.LX["pause"] + d.LX["app"]) / 2
d.msg("CRI", "app", "net·ipc·uts 합류", 364, OK, "ok", sub="pid:[...3507] · mnt:[...3506]", lx=gap_pa)
d.msg("CRI", "kubelet", "container 1e94e814", 396, MUTED, "ar", dash="4 3")

# 3. StartContainer -> app 실행
d.msg("kubelet", "CRI", "StartContainer", 432, ACC, "acc", sub="1e94e814")
d.act("app", 440, 28)
d.msg("CRI", "app", "exec java", 448, ACC, "acc", sub="PID 1997 · NSpid 1997 1", lx=gap_pa)

# 4. 앱 재시작 시 앵커 유지
d.state_box("pause", "PID 1959 유지", "10.244.0.5 · net:[...3298]", 488, OK, w=196)
d.state_box("app", "재시작 1997→2526", "1e94→a46d · pid:[...3508]", 488, MUTED, w=196)

d.legend(524, [("CRI 호출", INFO), ("앵커 유지", OK), ("앱 실행", ACC), ("응답", MUTED)])

out = _HERE.parent / "pause 컨테이너·Pod 샌드박스.sandbox-flow.svg"
d.save(str(out))
print("saved:", out)
