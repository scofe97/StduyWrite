# 타입 스펙: type-architecture — 가운데 BPF 명령어 집합(RFC 9669), 왼쪽 위 거버넌스, 아래 두 실행 환경(Windows · Linux), 오른쪽 아래 Linux 새 기능, 오른쪽 위 사용자 도구. focal 은 명령어 집합.
# 사실 출처: RFC 9669(2024-10) 초록·§1, 재단 헌장 L9~11·L46~48, eBPF for Windows v1.7.0 README L32~50(네이티브·JIT·인터프리터)·docs/GettingStarted.md L153~159(ebpfcore.sys · eBPFSvc),
#   Linux v7.2 include/uapi/linux/bpf.h L993(BPF_TOKEN_CREATE)·L1048(BPF_MAP_TYPE_ARENA)·L1663~1671(signature), 버전은 본문 §3 연표와 같다(kptr 5.19 · bpf_obj_new 6.2 · arena 6.9 · token 6.9 · 서명 6.18).
# Layout conventions: 존 3개(거버넌스 · Windows · Linux, Linux 안에 하위 존 하나). 연결선은 직각, 모든 좌표 4의 배수. 첫 선을 먼저 그린 뒤 상자를 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 616
d = D(W, H, "LEARNING EBPF · 11-01",
      "명령어 집합 하나를 표준이 정하고 두 운영체제가 각자의 검증기로 받는다",
      "IETF 의 RFC 9669 가 가운데에서 Windows(PREVAIL + bpf2c)와 Linux(verifier + JIT)를 잇고, 새 커널 기능은 Linux 쪽에 쌓이며 도구가 그 위에 놓인다.",
      "가운데는 표준, 아래는 실행 환경, 오른쪽 위는 사용자 도구")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def node(x, y, w, h, c, title, sub=None, focal=False, size=13):
    d.tone(x, y, w, h, c, 6, "1F" if focal else "12", 1.6 if focal else 1.2)
    if sub:
        d.t(x + w // 2, y + 24, title, 13, INK, fam(title), "middle", 600)
        d.t(x + w // 2, y + 44, sub, 12, MUTED, fam(sub))
    else:
        d.t(x + w // 2, y + h // 2 + 5, title, size, INK, fam(title), "middle", 600)


def zone(x, y, w, h, label, c):
    d.box(x, y, w, h, PAPER2, c, 1.0, 8)
    d.t(x + 16, y + 20, label, 9, SOFT, MONO, "start")


# 연결선 먼저
d.arrow([(312, 164), (368, 164)], INFO, "info", 1.5)
d.arrow([(400, 192), (400, 212), (232, 212), (232, 232)], WARN, "warn", 1.5)
d.arrow([(560, 192), (560, 232)], OK, "ok", 1.5)
d.arrow([(792, 236), (792, 144)], MUTED, "ar", 1.4)

# 거버넌스
zone(24, 92, 288, 112, "GOVERNANCE", INFO)
node(40, 116, 256, 36, INFO, "eBPF Foundation · BSC")
node(40, 160, 256, 36, INFO, "IETF BPF WG")
d.chip(340, 146, "표준", INFO, 12)

# 가운데
node(372, 108, 216, 84, ACC, "BPF 명령어 집합", "RFC 9669", True)

# 사용자 도구
node(648, 96, 288, 44, MUTED, "Cilium · Falco · Tetragon · bpftrace", size=12)

# Windows
zone(24, 236, 416, 292, "WINDOWS", WARN)
node(44, 268, 180, 44, WARN, "PREVAIL")
node(240, 268, 180, 44, WARN, "bpf2c")
node(44, 332, 180, 44, WARN, "uBPF JIT")
node(240, 332, 180, 44, WARN, "ebpfcore.sys")
d.arrow([(224, 290), (236, 290)], MUTED, "ar", 1.4)
d.arrow([(330, 312), (330, 328)], MUTED, "ar", 1.4)
d.arrow([(224, 354), (236, 354)], MUTED, "ar", 1.4)
d.box(44, 400, 376, 112, PAPER, WARN, 0.9, 6)
d.t(60, 420, "프로그램 유형", 11, SOFT, KR, "start")
for k, nm in enumerate(["XDP", "bind", "cgroup/sock_addr", "sock_ops", "netevent", "process"]):
    node(60 + (k % 2) * 176, 428 + (k // 2) * 28, 160, 24, WARN, nm, size=11)

# Linux
zone(472, 236, 464, 292, "LINUX", OK)
node(492, 268, 200, 44, OK, "verifier + JIT")
node(708, 268, 200, 44, OK, "bpf()")
d.box(492, 332, 424, 184, PAPER, OK, 0.9, 6)
d.t(508, 352, "새 커널 기능", 11, SOFT, KR, "start")
node(508, 364, 192, 40, ACC, "서명 필드 6.18", focal=True)
node(708, 364, 192, 40, OK, "kptr 5.19")
node(508, 412, 192, 40, OK, "bpf_obj_new 6.2")
node(708, 412, 192, 40, OK, "arena 6.9")
node(508, 460, 192, 40, OK, "BPF token 6.9")

d.legend(H - 56, [("거버넌스", INFO), ("명령어 집합", ACC), ("Windows", WARN), ("Linux", OK), ("사용자 도구", MUTED)])
d.save("11-01.chapter-overview.svg")
