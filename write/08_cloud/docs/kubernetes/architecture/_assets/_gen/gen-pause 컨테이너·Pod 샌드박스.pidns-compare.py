"""shareProcessNamespace false vs true 네임스페이스 포함 범위와 PID 1 비교.

# 타입 스펙: type-nested
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, INK, MUTED, RULE, ACC, OK, INFO, KR, MONO

W, H = 880, 540
d = D(
    W, H,
    "NESTED · PID NAMESPACE",
    "shareProcessNamespace 설정에 따른 PID 네임스페이스와 PID 1 차이",
    "좌측 pod-isolated(false)에서는 pause, app, sidecar 가 각자 PID 1 인 별도 PID 네임스페이스를 쓰고, 우측 pod-shared(true)에서는 하나의 PID 네임스페이스 pid:[4026533505] 를 공유해 /pause(NSpid 1961 1)가 PID 1 이 된다.",
    lead="kind v1.35 실측: 두 모드 모두 net·ipc·uts 는 공유하고 mnt 는 분리하며, pid 네임스페이스 경계만 달라집니다",
)


def ring(x, y, w, h, title, sub, stroke, fill, title_c, sw=1.2):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    d.t(x + 16, y + 24, title, 13, title_c, KR if any("가" <= c <= "힣" for c in title) else MONO, "start", 600)
    if sub:
        d.t(x + w - 16, y + 24, sub, 12, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "end")


def proc_card(x, y, w, h, name, nspid, role, stroke=RULE, role_c=MUTED):
    d.box(x, y, w, h, PAPER, stroke, 1.0, 6)
    d.t(x + 12, y + 21, name, 12, INK, MONO, "start", 600)
    d.t(x + w - 12, y + 21, role, 12, role_c, KR if any("가" <= c <= "힣" for c in role) else MONO, "end", 600)
    d.t(x + 12, y + 40, nspid, 11, MUTED, MONO, "start")


# ── 좌측: pod-isolated (false) ────────────────────────────────────────
LX, LY, LW, LH = 24, 96, 404, 376
ring(LX, LY, LW, LH, "pod-isolated (false)", "10.244.0.5", "rgba(191,192,192,0.40)", "rgba(255,255,255,0.02)", INK, 1.1)
d.t(LX + 16, LY + 44, "net:[4026533298] · ipc:[...3500] · uts:[...3499]", 11, INFO, MONO, "start")

iso_items = [
    ("pid:[...3501] · mnt:[...3498]", "/pause", "NSpid 1959 1", "PID 1", OK),
    ("pid:[...3507] · mnt:[...3506]", "java /tmp/App.java", "NSpid 1997 1", "PID 1", INFO),
    ("pid:[...3512] · mnt:[...3511]", "sleep 3600", "NSpid 2089 1", "PID 1", MUTED),
]
for idx, (ns, cmd, nspid, role, c) in enumerate(iso_items):
    ry = LY + 60 + idx * 100
    ring(LX + 16, ry, LW - 32, 88, ns, "독립", c, f"{c}10", c, 1.0)
    proc_card(LX + 28, ry + 32, LW - 56, 48, cmd, nspid, role, RULE, c)

# ── 우측: pod-shared (true) ───────────────────────────────────────────
RX, RY, RW, RH = 452, 96, 404, 376
ring(RX, RY, RW, RH, "pod-shared (true)", "10.244.0.6", "rgba(191,192,192,0.40)", "rgba(255,255,255,0.02)", INK, 1.1)
d.t(RX + 16, RY + 44, "net:[4026533396] · ipc:[...3504] · uts:[...3503]", 11, INFO, MONO, "start")

# 공용 PID 네임스페이스 고리 (focal 1곳: ACC)
PX, PY, PW, PH = RX + 16, RY + 60, RW - 32, 296
ring(PX, PY, PW, PH, "공유 pid:[4026533505]", "공용 PID 1", ACC, f"{ACC}14", ACC, 1.4)

shr_items = [
    ("/pause", "NSpid 1961 1 · mnt:[...3502]", "PID 1 · 회수", OK),
    ("java /tmp/App.java", "NSpid 2020 7 · mnt:[...3509]", "PID 7", INFO),
    ("sleep 3600", "NSpid 2115 35 · mnt:[...3514]", "PID 35", MUTED),
]
for idx, (cmd, nspid, role, c) in enumerate(shr_items):
    cy = PY + 40 + idx * 80
    proc_card(PX + 12, cy, PW - 24, 64, cmd, nspid, role, c if idx == 0 else RULE, c)

d.legend(492, [("Pod 공용 net·ipc·uts", INFO), ("샌드박스 앵커", OK), ("공유 PID (focal)", ACC), ("독립 PID", MUTED)])

out = _HERE.parent / "pause 컨테이너·Pod 샌드박스.pidns-compare.svg"
d.save(str(out))
print("saved:", out)
