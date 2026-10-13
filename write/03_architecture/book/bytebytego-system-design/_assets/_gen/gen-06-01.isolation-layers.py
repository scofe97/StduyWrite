# 타입 스펙: type-layers — 같은 앱 셋을 베어메탈·가상 머신·컨테이너·VM 안의 컨테이너로 쌓은 네 스택. 층마다 커널이 몇 개인지와 같은 커널을 쓰는 앱 쌍을 센다.
# 사실 출처: Firecracker NSDI'20 논문 §2.1(컨테이너는 호스트 커널을 직접 호출하고 가상화는 게스트 커널을 둔다 · cgroups·namespaces·seccomp-bpf·chroot) · §2(Lambda 첫 설계: 계정 사이는 VM, 같은 고객의 함수는 VM 안 컨테이너)
#   · §4.3(2018년부터 EC2 베어메탈 위 Firecracker) https://www.usenix.org/system/files/nsdi20-paper-agache.pdf · Firecracker README v1.17.0(KVM 으로 microVM 생성)
#   · 커널 수 = 호스트 1 + 게스트 VM 수(VM 둘 → 3). 같은 커널 앱 쌍 = 앱 셋이 한 커널이면 C(3,2)=3, VM 이 앱1·앱2 / 앱3 으로 갈리면 (앱1, 앱2) 하나.
# Layout conventions: 열 폭 216·stride 232(x=24+232k), 바닥 y=420 기준 아래에서 위로 서버 32·커널 36·층 간격 4, VM 상자 폭 104. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 592
d = D(W, H, "BYTEBYTEGO · 06-01 §2",
      "같은 앱 셋을 어느 층에서 가르느냐가 커널 수를 정한다",
      "컨테이너는 호스트 커널을 나눠 쓰고 가상 머신은 VM 마다 게스트 커널을 하나 더 둡니다",
      "앱 1·2·3 을 같은 서버에 올린 네 가지 방식")

X0, CW, STRIDE, BOT = 24, 216, 232, 380
cols = ["베어메탈", "가상 머신", "컨테이너", "VM 안의 컨테이너"]
subs = ["프로세스 셋", "VM 둘", "컨테이너 셋", "VM 둘 안에 각각"]
for k, (nm, sb) in enumerate(zip(cols, subs)):
    x = X0 + k * STRIDE
    d.t(x + CW / 2, 108, nm, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, 128, sb, 12, MUTED, KR)


def server(x):
    d.box(x, BOT - 32, CW, 32, PAPER2, RULE, 0.9, 4)
    d.t(x + CW / 2, BOT - 12, "물리 서버", 12, MUTED, KR)


def kernel(x, label):
    d.tone(x, BOT - 72, CW, 36, WARN, 4, "14", 1.0)
    d.t(x + CW / 2, BOT - 49, label, 12, WARN, KR, "middle", 600)


def chips(x, y, labels, kind, w=64, tone=OK, two=True):
    for i, lb in enumerate(labels):
        cx = x + i * (w + 8)
        d.tone(cx, y, w, 44, tone, 4, "14", 1.0)
        if two:
            d.t(cx + w / 2, y + 18, kind, 12, tone, KR)
            d.t(cx + w / 2, y + 36, lb, 12, INK, KR, "middle", 600)
        else:
            d.t(cx + w / 2, y + 27, lb, 12, INK, KR, "middle", 600)


def vm(x, y, h, apps, guest_y, kind=None, runtime_y=None):
    d.tone(x, y, 104, h, INFO, 4, "10", 1.1)
    d.t(x + 8, y + 18, "VM", 12, INFO, MONO, "start", 600)
    d.tone(x + 4, guest_y, 96, 32, WARN, 4, "14", 1.0)
    d.t(x + 52, guest_y + 20, "게스트 커널", 12, WARN, KR, "middle", 600)
    if runtime_y is not None:
        d.box(x + 4, runtime_y, 96, 28, PAPER2, RULE, 0.9, 4)
        d.t(x + 52, runtime_y + 19, "런타임", 12, MUTED, KR)
    return x


# 1열 베어메탈: 앱 셋이 호스트 커널 하나를 같이 쓴다.
x = X0
server(x); kernel(x, "호스트 커널")
chips(x + 4, BOT - 72 - 48, ["앱 1", "앱 2", "앱 3"], "", 64, OK, False)

# 2열 가상 머신: VM1 에 앱 1·2, VM2 에 앱 3.
x = X0 + STRIDE
server(x); kernel(x, "호스트 커널 · KVM")
vy, vh = BOT - 72 - 4 - 112, 112
for j, apps in enumerate((["앱 1", "앱 2"], ["앱 3"])):
    vx = x + j * 112
    vm(vx, vy, vh, apps, vy + vh - 36)
    for i, lb in enumerate(apps):
        d.tone(vx + 4 + i * 48, vy + 28, 44, 40, OK, 4, "14", 1.0)
        d.t(vx + 26 + i * 48, vy + 53, lb, 12, INK, KR, "middle", 600)

# 3열 컨테이너: 호스트 커널 위에 런타임 하나, 컨테이너 셋.
x = X0 + 2 * STRIDE
server(x); kernel(x, "호스트 커널")
d.box(x, BOT - 72 - 4 - 36, CW, 36, PAPER2, RULE, 0.9, 4)
d.t(x + CW / 2, BOT - 72 - 4 - 14, "컨테이너 런타임", 12, MUTED, KR)
chips(x + 4, BOT - 72 - 4 - 36 - 4 - 48, ["앱 1", "앱 2", "앱 3"], "컨테이너", 64, OK, True)

# 4열 VM 안의 컨테이너: VM 마다 게스트 커널 위에 런타임과 컨테이너.
x = X0 + 3 * STRIDE
server(x); kernel(x, "호스트 커널 · KVM")
vy2, vh2 = BOT - 72 - 4 - 140, 140
for j, apps in enumerate((["앱 1", "앱 2"], ["앱 3"])):
    vx = x + j * 112
    vm(vx, vy2, vh2, apps, vy2 + vh2 - 36, runtime_y=vy2 + vh2 - 36 - 32)
    for i, lb in enumerate(apps):
        d.tone(vx + 4 + i * 48, vy2 + 28, 44, 40, OK, 4, "14", 1.0)
        d.t(vx + 26 + i * 48, vy2 + 53, lb, 12, INK, KR, "middle", 600)

# 값 두 줄: 커널 수와 같은 커널을 쓰는 앱 쌍.
rows = [
    ("커널 1개", "커널 3개 (1 + 2)", "커널 1개", "커널 3개 (1 + 2)"),
    ("같은 커널 앱 쌍 3", "같은 커널 앱 쌍 1", "같은 커널 앱 쌍 3", "같은 커널 앱 쌍 1"),
]
for r, vals in enumerate(rows):
    for k, v in enumerate(vals):
        x = X0 + k * STRIDE
        y = BOT + 24 + r * 44
        focal = r == 1 and k == 2
        if focal:
            d.tone(x, y, CW, 36, ACC, 4, "14", 1.4)
        else:
            d.tone(x, y, CW, 36, INFO, 4, "10", 0.9)
        d.t(x + CW / 2, y + 23, v, 12, ACC if focal else INFO, KR, "middle", 600)

# Lambda 가 거친 두 모양.
d.chip(X0 + 3 * STRIDE + CW / 2, BOT + 122, "Lambda 첫 설계", MUTED, 12)

d.legend(H - 44, [("커널", WARN), ("가상 머신 경계", INFO), ("앱 · 컨테이너", OK), ("이 편의 초점", ACC)])
d.save("06-01.isolation-layers.svg")
