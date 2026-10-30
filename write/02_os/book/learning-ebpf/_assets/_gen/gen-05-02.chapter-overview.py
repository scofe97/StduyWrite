# 타입 스펙: type-architecture — hello-buffer-config.bpf.c 의 부품 넷(헤더·전역과 맵·프로그램·라이선스)과 컴파일 두 단계(clang · llvm-strip)가 .bpf.o 로 모이는 지도. focal 은 프로그램 부품.
# 사실 출처: 예제 저장소 chapter5/hello-buffer-config.bpf.c·Makefile, 추출본 src/ebpf5.txt 681~689행(헤더 다섯)·783~800행(맵)·837~918행(SEC·프로그램)·1072행(라이선스)·1081~1136행(컴파일 옵션),
#   libbpf v1.8.0 src/bpf_tracing.h 8~35행(__TARGET_ARCH_*).
# Layout conventions: 밴드 둘(소스·컴파일), 열 x 는 24·252·476·720, 열 폭 216·212·232·216, 상자 높이 184, 컴파일 상자 x 는 24·464·708. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 536
d = D(W, H, "LEARNING EBPF · 05-02",
      "소스 한 파일이 부품 넷과 컴파일 두 단계를 거쳐 .bpf.o 가 된다",
      "hello-buffer-config.bpf.c 는 헤더 다섯, 전역 변수와 맵 둘, execve 에 붙는 프로그램, 라이선스 한 줄로 이뤄지고 clang 과 llvm-strip 을 거쳐 오브젝트 파일이 된다.",
      "부품마다 다룬 절 번호를 상자 제목에 붙였습니다")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


d.box(12, 96, 936, 232, PAPER2, RULE, 0.9, 8)
d.t(24, 114, "hello-buffer-config.bpf.c", 9, SOFT, MONO, "start")


def part(x, w, title, lines, c, focal=False):
    d.tone(x, 124, w, 184, c, 6, "14" if focal else "10", 1.6 if focal else 1.1)
    d.t(x + w / 2, 152, title, 14, ACC if focal else INK, fam(title), "middle", 600)
    for i, s in enumerate(lines):
        d.t(x + w / 2, 184 + 24 * i, s, 12, MUTED, fam(s), "middle")


part(24, 216, "헤더 다섯 · §1·§2",
     ['vmlinux.h', 'bpf/bpf_helpers.h', 'bpf/bpf_tracing.h', 'bpf/bpf_core_read.h', 'hello-buffer-config.h'], MUTED)
part(252, 212, "전역 변수와 맵 · §2·§3",
     ['char message[12]', 'output', 'PERF_EVENT_ARRAY', 'my_config', 'HASH · 10240'], INFO)
part(476, 232, "프로그램 · §3·§4",
     ['SEC("ksyscall/execve")', 'BPF_KPROBE_SYSCALL', 'hello(pathname)', 'pt_regs CO-RE 읽기'], ACC, True)
part(720, 216, "라이선스",
     ['SEC("license")', 'Dual BSD/GPL'], OK)

# 소스 → 컴파일
d.arrow([(224, 328), (224, 360)], MUTED, "ar", 1.5)
CY = 364
d.tone(24, CY, 400, 88, MUTED, 6, "10", 1.1)
d.t(224, CY + 32, "clang", 14, INK, MONO, "middle", 600)
d.t(224, CY + 56, "-target bpf -D __TARGET_ARCH_$(ARCH)", 12, MUTED, MONO, "middle")
d.t(224, CY + 76, "-O2 -g", 12, MUTED, MONO, "middle")
d.tone(464, CY, 204, 88, MUTED, 6, "10", 1.1)
d.t(566, CY + 32, "llvm-strip", 14, INK, MONO, "middle", 600)
d.t(566, CY + 56, "-g", 12, MUTED, MONO, "middle")
d.tone(708, CY, 228, 88, OK, 6, "14", 1.2)
d.t(822, CY + 32, "오브젝트 파일", 14, INK, KR, "middle", 600)
d.t(822, CY + 56, "hello-buffer-config.bpf.o", 12, MUTED, MONO, "middle")
d.arrow([(426, CY + 44), (460, CY + 44)], MUTED, "ar", 1.5)
d.arrow([(670, CY + 44), (704, CY + 44)], MUTED, "ar", 1.5)

d.legend(H - 56, [("헤더", MUTED), ("전역·맵", INFO), ("프로그램", ACC), ("라이선스·결과", OK)])
d.save("05-02.chapter-overview.svg")
