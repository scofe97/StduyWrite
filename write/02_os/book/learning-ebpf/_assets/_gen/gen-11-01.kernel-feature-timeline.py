# 타입 스펙: type-timeline — 릴리스 순번 축(5.3 ~ 6.18, 칸 하나 = 릴리스 하나). 같은 릴리스의 이벤트는 한 상자에 묶고 상자는 축 위아래로 엇갈려 붙인다. focal 은 6.18 서명 필드.
# 사실 출처: 5.3 유한 반복문 = 커밋 2589726d12a1 · 5.7 BPF LSM = BCC docs/kernel-versions.md(v0.37.0) · 5.17 bpf_loop = v5.17 bpf.h L4963 · 5.19 kptr = 병합 367590b7fccc(v5.19 bpf.h L5157 bpf_kptr_xchg),
#   5.19 BIG TCP IPv6 = 커밋 81fbc812132c · Cilium v1.20 "Kernel >= 5.19" · 6.2 bpf_obj_new_impl = v6.2 kernel/bpf/helpers.c L1768(v6.1 에 없음) · 6.3 HID-BPF = v6.3 include/linux/hid_bpf.h(v6.2 에 없음),
#   6.3 BIG TCP IPv4 = 커밋 b1a78b9b9886 · v6.3 if_link.h IFLA_GSO_IPV4_MAX_SIZE · 6.9 arena·token = v6.9 bpf.h(v6.8 에 없음) · 6.12 sched_ext = v6.12 kernel/sched/ext.c(v6.11 에 없음) · 6.18 서명 = v6.18 bpf.h L1617(v6.17 에 없음).
# Layout conventions: 축 y=252, x=60+순번*24(순번 0=5.3 … 35=6.18, 5.19=16 다음이 6.0=17). 상자는 축에서 48px 떨어진 위·아래 한 단, 상자 안에 이벤트 x 가 들어가도록 가로 위치를 정한다. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 432
d = D(W, H, "LEARNING EBPF · 11-01 §3",
      "5.3 의 반복문부터 6.18 의 서명 필드까지 한 칸이 릴리스 하나다",
      "5.19 다음은 6.0 이라 버전 숫자가 아니라 릴리스 순번으로 간격을 둔다. 6.9 에 arena 와 token, 6.18 에 서명 필드가 들어왔다.",
      "눈금 하나 = 릴리스 하나(5.3 ~ 6.18)")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


AX = 252
X0, ST = 60, 24
d.line(X0 - 24, AX, X0 + 35 * ST + 24, AX, MUTED, 1.2)
for i in range(36):
    d.line(X0 + i * ST, AX - 4, X0 + i * ST, AX + 4, SOFT, 0.8)

# (순번, 버전, [(이름, 색)…], 위(1)·아래(-1), 상자 왼쪽 x, 상자 폭, focal)
EV = [
    (0, "5.3", [("유한 반복문", INFO)], -1, 20, 80, False),
    (4, "5.7", [("BPF LSM", INFO)], 1, 124, 64, False),
    (14, "5.17", [("bpf_loop", INFO)], -1, 360, 72, False),
    (16, "5.19", [("kptr", OK), ("BIG TCP IPv6", WARN)], 1, 388, 100, False),
    (19, "6.2", [("bpf_obj_new", OK)], -1, 470, 92, False),
    (20, "6.3", [("HID-BPF", WARN), ("BIG TCP IPv4", WARN)], 1, 496, 100, False),
    (26, "6.9", [("arena", OK), ("BPF token", OK)], 1, 648, 76, False),
    (29, "6.12", [("sched_ext", WARN)], -1, 718, 76, False),
    (35, "6.18", [("서명 필드", ACC)], 1, 864, 68, True),
]
for idx, ver, names, side, bx, w, focal in EV:
    x = X0 + idx * ST
    h = 28 + 16 * len(names)
    top = AX - 48 - h if side > 0 else AX + 48
    assert bx <= x <= bx + w, (ver, x, bx, w)
    ya, yb = (top + h, AX) if side > 0 else (AX, top)
    d.line(x, ya, x, yb, ACC if focal else SOFT, 1.0)

for idx, ver, names, side, bx, w, focal in EV:
    x = X0 + idx * ST
    h = 28 + 16 * len(names)
    top = AX - 48 - h if side > 0 else AX + 48
    c0 = ACC if focal else names[0][1]
    d.o.append(f'<circle cx="{x}" cy="{AX}" r="{6 if focal else 4}" fill="{c0}" stroke="{PAPER}" stroke-width="1.5"/>')
    d.tone(bx, top, w, h, c0, 4, "22" if focal else "12", 1.6 if focal else 1.0)
    d.t(bx + w / 2, top + 18, ver, 11, c0, MONO, "middle", 600)
    for k, (nm, c) in enumerate(names):
        d.t(bx + w / 2, top + 36 + 16 * k, nm, 11, INK if len(names) == 1 else c, fam(nm), "middle", 400)

d.legend(H - 56, [("검증기", INFO), ("메모리 · 객체", OK), ("네트워크 · 장치 · 스케줄러", WARN), ("서명", ACC)])
d.save("11-01.kernel-feature-timeline.svg")
