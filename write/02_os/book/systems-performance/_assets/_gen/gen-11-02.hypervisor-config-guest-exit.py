# 11-02 §2 — 두 하이퍼바이저 구성과, 오버헤드가 생기는 자리인 guest exit.
# 타입 스펙: type-process — 구성 둘을 같은 슬롯으로 대조하고, 아래에 exit 가 오버헤드가 되는 과정을 둔다.
#           축약: 주체(lane)가 없는 대조·단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 512
CW, CH, GAP, X0, Y = 424, 148, 32, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-02 §2",
       "두 구성과 guest exit",
       "Config A 는 베어메탈 위에서, Config B 는 호스트 OS 위에서 하이퍼바이저가 돈다. 어느 쪽이든 게스트가 하이퍼바이저로 빠져나간 시간이 CPU 오버헤드다.",
       "게스트 애플리케이션은 대개 프로세서에서 직접 실행됩니다 — 오버헤드는 빠져나갈 때 생깁니다")

CONFIGS = [
    ("Config A", "베어메탈 위 하이퍼바이저", "Xen", ["하드웨어 위에 하이퍼바이저가 직접.", "게스트 I/O 는 dom0 이 돕습니다"]),
    ("Config B", "호스트 OS 위 하이퍼바이저", "KVM", ["호스트 커널 모듈로 동작.", "호스트 자원 제어를 함께 씁니다"]),
]
for i, (name, tag, impl, body) in enumerate(CONFIGS):
    x = X0 + i * (CW + GAP)
    d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 14, INK, KR, "start", 600)
    d.t(x + CW - 16, Y + 30, impl, 13, SOFT, MONO, "end")
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    for j, line in enumerate(body):
        d.t(x + 16, Y + 82 + j * 20, line, 13, MUTED, KR, "start")

# guest exit
YE = Y + CH + 44
d.tone(X0, YE, 880, 116, ACC, 8)
d.t(X0 + 20, YE + 30, "guest exit", 15, ACC, KR, "start", 600)
d.t(X0 + 20, YE + 56, "가상 CPU 가 게스트 안에서 실행을 멈추고 하이퍼바이저로 빠져나가는 이벤트입니다.", 13, MUTED, KR, "start")
d.t(X0 + 20, YE + 78, "그 밖에서 보낸 시간이 곧 CPU 오버헤드이고, 커널에서 처리하지 못해 유저 프로세스까지 가면 더 커집니다.", 13, MUTED, KR, "start")
d.t(X0 + 20, YE + 100, "halt 가 많으면 게스트가 idle 하고, I/O 명령·인터럽트 주입이 많으면 가상 NIC·디스크로 I/O 중입니다.", 13, ACC, KR, "start")

d.legend(YE + 140, [("오버헤드가 생기는 자리", ACC), ("하이퍼바이저 구성", MUTED)])
d.save("11-02.hypervisor-config-guest-exit.svg")
