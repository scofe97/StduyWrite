# 타입 스펙: type-flowchart — bpf(BPF_PROG_LOAD, prog_type=CGROUP_SOCK) → expected_attach_type 이 0 인가 → 예: INET_SOCK_CREATE 로 채움 → bpf_prog_load_check_attach switch → 네 attach type 이면 return 0, 그 밖이면 -EINVAL. focal 은 채우는 상자.
# 사실 출처: 커널 v7.2 kernel/bpf/syscall.c L2705~2715(bpf_prog_load_fixup_attach_type: CGROUP_SOCK 에서 0 이면 BPF_CGROUP_INET_SOCK_CREATE),
#   L2765~2774(bpf_prog_load_check_attach 의 CGROUP_SOCK 분기: INET_SOCK_CREATE · INET_SOCK_RELEASE · INET4_POST_BIND · INET6_POST_BIND → return 0, default → -EINVAL),
#   L2997(fixup 호출)·L3085(check 호출), include/uapi/linux/bpf.h L1099~1102(열거형 첫 값 BPF_CGROUP_INET_INGRESS, UNSPEC 없음).
# Layout conventions: 윗줄 y=140 상자 h=64, 마름모 중심 (420,172) 반폭 112·반높이 44, 아랫줄 y=300, 끝줄 y=468. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 660
d = D(W, H, "LEARNING EBPF · 07-02 §4", "CGROUP_SOCK 적재는 attach type 을 채운 뒤 네 자리만 통과시킨다",
      "expected_attach_type 이 0 이면 bpf_prog_load_fixup_attach_type 이 BPF_CGROUP_INET_SOCK_CREATE 로 채우고, bpf_prog_load_check_attach 의 switch 가 네 값만 0 으로 통과시키고 나머지는 -EINVAL 로 거부한다.",
      "채우기가 먼저이고 검사가 뒤입니다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def box(x, y, w, title, sub, c, focal=False, h=64):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}1F" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, h, c, 6, "12", 1.2)
    d.t(x + w / 2, y + 28, title, 13, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 50, sub, 12, MUTED, kr(sub))


# 연결선 먼저
d.arrow([(256, 172), (304, 172)], MUTED, "ar", 1.5)                              # 적재 → 마름모
d.arrow([(532, 172), (592, 172)], ACC, "acc", 1.6)                                # 예 → 채우기
d.arrow([(420, 216), (420, 296)], MUTED, "ar", 1.5)                               # 아니오 → 검사
d.arrow([(740, 204), (740, 332), (664, 332)], ACC, "acc", 1.5)                    # 채운 뒤 → 검사
d.arrow([(540, 364), (540, 416), (240, 416), (240, 464)], OK, "ok", 1.6)          # 허용 네 자리
d.arrow([(540, 416), (752, 416), (752, 464)], BAD, "bad", 1.6)                    # 그 밖

box(24, 140, 232, "bpf(BPF_PROG_LOAD)", "prog_type = CGROUP_SOCK", INFO)
CX, CY = 420, 172
d.o.append(f'<polygon points="{CX-112},{CY} {CX},{CY-44} {CX+112},{CY} {CX},{CY+44}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(CX, CY - 2, "expected_attach_type", 11, INK, MONO, "middle", 600)
d.t(CX, CY + 16, "= 0 ?", 12, INK, MONO, "middle", 600)
d.chip(562, 154, "0", ACC, 12)
d.chip(420, 256, "그 밖의 값", MUTED, 12)
box(596, 140, 288, "채우기", "BPF_CGROUP_INET_SOCK_CREATE", ACC, True)

box(260, 300, 404, "bpf_prog_load_check_attach", "switch (CGROUP_SOCK)", MUTED)
d.tone(24, 468, 432, 88, OK, 6, "12", 1.2)
d.t(240, 496, "return 0", 13, OK, MONO, "middle", 600)
d.t(240, 518, "INET_SOCK_CREATE · INET_SOCK_RELEASE", 12, MUTED, MONO)
d.t(240, 538, "INET4_POST_BIND · INET6_POST_BIND", 12, MUTED, MONO)
box(568, 468, 368, "-EINVAL", "그 밖의 attach type", BAD, h=88)
d.chip(240, 440, "네 자리", OK, 12)

d.legend(H - 56, [("적재 호출", INFO), ("채우기", ACC), ("허용", OK), ("거부", BAD)])
d.save("07-02.cgroup-attach-check.svg")
