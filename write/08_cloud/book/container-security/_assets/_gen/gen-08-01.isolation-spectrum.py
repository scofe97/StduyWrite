# 타입 스펙: type-architecture — 세 갈래가 시스템 콜을 보내는 길. 보안 장치는 호스트 커널로 곧장, gVisor 는 Sentry 를 거쳐 호스트 커널로, VM 격리는 게스트 OS 를 거쳐 하이퍼바이저로 간다. 아래 축이 호스트 커널 공유에서 비공유로 간다. focal 은 보안 장치 열이 끝내 공유하는 호스트 커널.
# 사실 출처: 노트 L22(세 갈래와 커널 공유 여부), L143~L149(저수준 단속 · Dirty COW 못 막음), L155~L167(Sentry · seccomp 샌드박싱), L215(Kata QEMU), L227(Firecracker KVM), L247~L249(범주)
# Layout conventions: 열 3개(폭 272 · 간격 24 · x=60), 열 안 상자 폭 240(x+16), 행 stride 앱 y=168 · 장치 y=260 · 목표 y=380, 아래 축 y=508. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO, RULE

W, H = 984, 596
CW, GAP, X0 = 272, 24, 60
NW = CW - 32


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def node(d, x, y, w, h, title, subs, col=None, op="14", sw=1.2):
    fit(title, 13, w - 16)
    if col:
        d.tone(x, y, w, h, col, 6, op, sw)
    else:
        d.box(x, y, w, h)
    n = len(subs)
    tb = round(y + h / 2 - 9 * n + 5)
    d.t(x + w / 2, tb, title, 13, col or INK, kr(title), "middle", 600)
    for i, s in enumerate(subs):
        fit(s, 12, w - 16)
        d.t(x + w / 2, tb + 20 + 18 * i, s, 12, MUTED, kr(s), "middle")


d = D(W, H, "ARCHITECTURE · 08-01 INTRO",
      "격리 강화 수단은 시스템 콜이 호스트 커널에 닿는 길로 나뉩니다",
      "왼쪽에서 오른쪽으로 일반 컨테이너와 보안 장치, gVisor, VM 격리 세 열. 보안 장치는 시스템 콜이 호스트 커널로 곧장 가고, "
      "gVisor 는 Sentry 를 거쳐 호스트 커널로 가며, Kata·Firecracker·Unikernel 은 게스트 OS 를 거쳐 하이퍼바이저로 간다. 아래 축은 호스트 커널 공유에서 비공유로 이어진다.",
      lead="seccomp·AppArmor·SELinux 는 커널을 그대로 공유하고, VM 격리는 커널을 공유하지 않으며, gVisor 가 그 사이에 놓입니다.")

COLS = [
    dict(head="seccomp · AppArmor · SELinux", tag="일반 컨테이너 + 보안 장치",
         app="컨테이너 안 앱",
         dev=("프로파일 단속", ["syscall · capability", "파일 접근"], None),
         tgt=("호스트 커널", ["컨테이너와 공유", "Dirty COW 못 막음"], ACC)),
    dict(head="gVisor", tag="컨테이너와 VM 사이",
         app="컨테이너 안 앱",
         dev=("Sentry", ["syscall 가로채 재구현", "사용자 공간 커널"], INFO),
         tgt=("호스트 커널", ["Sentry 도 seccomp 로 샌드박싱"], None)),
    dict(head="Kata · Firecracker · Unikernel", tag="가상머신 격리",
         app="VM 안의 앱",
         dev=("게스트 OS", ["Kata: QEMU 가상머신", "Firecracker: KVM 기반"], None),
         tgt=("하이퍼바이저", ["호스트 커널과 비공유"], OK)),
]

ZY, ZH = 96, 372
AY, AH = 168, 52
DY, DH = 260, 80
TY, TH = 380, 72

# 열 구역(상자보다 먼저)
for i, c in enumerate(COLS):
    zx = X0 + i * (CW + GAP)
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{CW}" height="{ZH}" rx="8" fill="none" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="6 5"/>')

for i, c in enumerate(COLS):
    zx = X0 + i * (CW + GAP)
    bx, cx = zx + 16, zx + CW / 2
    fit(c["head"], 13, CW - 16)
    d.t(cx, 120, c["head"], 13, INK, kr(c["head"]), "middle", 600)
    d.t(cx, 140, c["tag"], 12, MUTED, KR, "middle")
    # 화살표(상자보다 먼저)
    d.arrow([(cx, AY + AH + 2), (cx, DY - 4)], MUTED, "ar", 1.4)
    d.t(cx + 12, AY + AH + 25, "syscall", 12, MUTED, MONO, "start")
    d.arrow([(cx, DY + DH + 2), (cx, TY - 4)], ACC if c["tgt"][2] == ACC else MUTED, "acc" if c["tgt"][2] == ACC else "ar", 1.8 if c["tgt"][2] == ACC else 1.4)
    node(d, bx, AY, NW, AH, c["app"], [])
    t, s, col = c["dev"]
    node(d, bx, DY, NW, DH, t, s, col)
    t, s, col = c["tgt"]
    node(d, bx, TY, NW, TH, t, s, col, "1F" if col == ACC else "14", 1.6 if col == ACC else 1.2)

# 아래 축: 호스트 커널 공유 → 비공유
AXY = 512
d.arrow([(X0, AXY), (X0 + 3 * CW + 2 * GAP, AXY)], MUTED, "ar", 1.4)
d.t(X0, AXY - 14, "호스트 커널 공유", 12, ACC, KR, "start", 600)
d.t(X0 + 3 * CW + 2 * GAP, AXY - 14, "호스트 커널 비공유", 12, OK, KR, "end", 600)

d.legend(H - 44, [("공유하는 호스트 커널", ACC), ("사용자 공간 커널", INFO), ("커널 비공유", OK)])
d.save(str(ASSETS / "08-01.isolation-spectrum.svg"))
print("ok 08-01 isolation-spectrum")
