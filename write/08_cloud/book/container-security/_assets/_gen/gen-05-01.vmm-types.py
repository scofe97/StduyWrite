# 타입 스펙: type-layers — 세 열(Type 1 · Type 2 · KVM)의 층 쌓기. 위에서 아래로 게스트 · VMM · 호스트 OS · 하드웨어 네 줄이 같은 높이에 맞춰져, VMM 이 하드웨어 바로 위 · 호스트 유저 공간 · 호스트 커널 안 어디에 앉는지가 가로로 비교된다. focal 은 호스트 커널 안에 든 KVM 모듈.
# 사실 출처: 노트 L97~L99(Type 1 · 하이퍼바이저는 베어메탈 위 · 밑에 OS 없음), L103~L107(Type 2 · macOS 위 VirtualBox 별도 애플리케이션 · 게스트 커널은 호스트와 다른 커널), L111~L115(KVM · 커널 모듈 · QEMU 와 함께 · 하드웨어 가속)
# Layout conventions: 층 h=56, stride 68(y=156·224·292·360), 열 폭 248 · stride 268(x=156·424·692), 왼쪽 행 이름 x=36, 열 머리 y=96 h=44. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, KR, MONO

W, H = 976, 492
CX = [156, 424, 692]
CWID = 248
ROW_Y0, ROW_H, ROW_STRIDE = 156, 56, 68


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def ry(i):
    return ROW_Y0 + i * ROW_STRIDE


d = D(W, H, "LAYERS · 05-01 §3",
      "VMM 의 자리는 하드웨어 바로 위, 호스트 유저 공간, 호스트 커널 안 셋으로 갈립니다",
      "세 열의 층 쌓기. Type 1 은 하드웨어 바로 위에 하이퍼바이저가 있고 호스트 OS 가 없다. "
      "Type 2 는 호스트 OS 커널 위 유저 공간에 VMM 애플리케이션이 있다. "
      "KVM 은 호스트 Linux 커널 안의 모듈이고 유저 공간의 QEMU 와 함께 쓰이는 경우가 많다.",
      lead="KVM 은 호스트 OS 가 있어 Type 2 처럼 보이지만 VMM 이 유저 공간이 아니라 커널 안에 있어 경계에 걸립니다.")

# 열 머리
HEADS = [("Type 1", "하이퍼바이저"), ("Type 2", "호스티드"), ("KVM", "경계에 있는 것")]
for j, (name, sub) in enumerate(HEADS):
    d.box(CX[j], 96, CWID, 44, "#161B22")
    d.t(CX[j] + 16, 123, name, 13, INK, MONO, "start", 600)
    d.t(CX[j] + CWID - 16, 123, sub, 12, MUTED, KR, "end")

# 행 이름
for i, name in enumerate(("게스트", "VMM", "호스트 OS", "하드웨어")):
    d.t(36, ry(i) + ROW_H / 2 + 5, name, 12, MUTED, kr(name), "start", 600)


def layer(i, j, title, sub=None, c=None, dashed=False, focal=False):
    x, y = CX[j], ry(i)
    fit(title, 13, CWID - 16)
    if sub:
        fit(sub, 12, CWID - 16)
    if dashed:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CWID}" height="{ROW_H}" rx="6" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="6 5"/>')
        col = SOFT
    elif focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CWID}" height="{ROW_H}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
        col = ACC
    elif c:
        d.tone(x, y, CWID, ROW_H, c, 6, "14", 1.1)
        col = c
    else:
        d.box(x, y, CWID, ROW_H)
        col = INK
    if sub:
        d.t(x + CWID / 2, y + 23, title, 13, col, kr(title), "middle", 600)
        d.t(x + CWID / 2, y + 43, sub, 12, MUTED, kr(sub), "middle")
    else:
        d.t(x + CWID / 2, y + 33, title, 13, col, kr(title), "middle", 600)


# Type 1
layer(0, 0, "게스트 OS 커널", "하이퍼바이저보다 낮은 권한", INFO)
layer(1, 0, "하이퍼바이저", "Hyper-V · Xen · ESXi", WARN)
layer(2, 0, "OS 없음", "베어메탈 위에서 직접", dashed=True)
layer(3, 0, "CPU · 메모리 · 장치")
# Type 2
layer(0, 1, "게스트 OS 커널", "호스트와 다른 커널", INFO)
layer(1, 1, "VMM 애플리케이션", "VirtualBox · Parallels · QEMU", WARN)
layer(2, 1, "호스트 OS 커널", "macOS")
layer(3, 1, "CPU · 메모리 · 장치")
# KVM
layer(0, 2, "게스트 OS 커널", "호스트 OS 를 거치지 않음", INFO)
layer(1, 2, "QEMU", "KVM 의 하드웨어 가속을 이용")
layer(2, 2, "KVM 모듈", "호스트 Linux 커널 안", focal=True)
layer(3, 2, "CPU · 메모리 · 장치")

d.legend(448, [("게스트 커널", INFO), ("VMM", WARN), ("경계에 있는 KVM", ACC)])
d.save(str(ASSETS / "05-01.vmm-types.svg"))
print("ok 05-01 vmm-types")
