# 11-02 §2 — 두 하이퍼바이저 구성과, 오버헤드가 생기는 자리인 guest exit.
# 타입 스펙: type-process — 구성 둘을 같은 슬롯으로 대조하고, 아래에 exit 가 처리되는 자리를 t1→t2→t3 로 옮겨 둔다.
#           축약: 주체(lane)가 없는 대조·단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 548
CW, CH, GAP, X0, Y = 424, 148, 32, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-02 §2",
       "두 구성과 guest exit",
       "Config A 는 베어메탈 위에서, Config B 는 호스트 OS 위에서 하이퍼바이저가 돈다. 어느 쪽이든 게스트가 하이퍼바이저로 빠져나간 시간이 CPU 오버헤드다.",
       "게스트 애플리케이션은 대개 프로세서에서 직접 실행됩니다 — 오버헤드는 빠져나갈 때 생깁니다")

CONFIGS = [
    ("Config A", "베어메탈 위 하이퍼바이저", "Xen", ["하드웨어 위 하이퍼바이저 직접 실행", "게스트 I/O 프록시 — dom0 의 QEMU"]),
    ("Config B", "호스트 OS 위 하이퍼바이저", "KVM", ["호스트 커널 모듈 + 유저 프로세스 QEMU", "호스트 자원 제어(cgroup) 병용"]),
]
for i, (name, tag, impl, body) in enumerate(CONFIGS):
    x = X0 + i * (CW + GAP)
    d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 14, INK, KR, "start", 600)
    d.t(x + CW - 16, Y + 30, impl, 13, SOFT, MONO, "end")
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    for j, line in enumerate(body):
        d.t(x + 16, Y + 82 + j * 20, line, 13, MUTED, KR, "start")

# guest exit — 처리 자리가 게스트 → 호스트 커널 → 유저 프로세스로 옮겨 갈수록 비용이 커진다
YE = Y + CH + 36
d.tone(X0, YE, 880, 164, ACC, 8)
d.t(X0 + 20, YE + 28, "guest exit — vCPU 의 게스트 이탈 (Config B)", 15, ACC, KR, "start", 600)

SW, SH, SG, SY = 264, 40, 24, YE + 48
STEPS = [("t1", "게스트 · vCPU 실행", MUTED), ("t2", "호스트 커널 · 일부 직접 처리", ACC), ("t3", "유저 프로세스 QEMU · 큰 비용", ACC)]
for k, (tt, lab, c) in enumerate(STEPS):
    sx = X0 + 20 + k * (SW + SG)
    d.box(sx, SY, SW, SH, PAPER2, c, 1.0, 6)
    d.t(sx + 12, SY + 25, tt, 11, SOFT, MONO, "start", 600)
    d.t(sx + 36, SY + 25, lab, 13, INK, KR, "start")
    if k < 2:
        d.arrow([(sx + SW + 4, SY + SH / 2), (sx + SW + SG - 6, SY + SH / 2)], ACC, "acc", 1.3)

d.t(X0 + 20, YE + 118, "exit 횟수 중 HLT 비중 큼 → idle 에 가까운 게스트", 13, MUTED, KR, "start")
d.t(X0 + 20, YE + 142, "I/O 명령 · 인터럽트 주입 많음 → 가상 NIC · 디스크 I/O 중", 13, MUTED, KR, "start")

d.legend(YE + 188, [("오버헤드가 생기는 자리", ACC), ("하이퍼바이저 구성", MUTED)])
d.save("11-02.hypervisor-config-guest-exit.svg")
