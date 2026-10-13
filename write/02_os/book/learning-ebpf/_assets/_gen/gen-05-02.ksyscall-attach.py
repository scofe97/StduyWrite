# 타입 스펙: type-process — SEC 이름이 아키텍처별 함수로 풀리고 매크로가 pt_regs 에서 pathname 을 꺼내 hello() 가 한 건을 perf 맵에 내보내는 네 단계와 출력. focal 은 매크로 안에 숨은 ctx.
# 사실 출처: 예제 저장소 chapter5/hello-buffer-config.bpf.c 22~44행, 추출본 src/ebpf5.txt 872행·894~918행(SEC·hello 본문)·1578~1582행(출력 `23664 501 bash Hello World`),
#   libbpf v1.8.0 src/libbpf.c 12445~12467행(arch_specific_syscall_pfx)·12621~12626행(`__%s_sys_%s`)·13011행(attach_ksyscall), src/bpf_tracing.h 876~884행(ctx 주석)·920행(BPF_KPROBE_SYSCALL).
# Layout conventions: 단계 상자 넷 y=108·h=124, 폭 192·stride 240(x=24·264·504·744), 둘째 줄 상자 y=300·h=80(x=504·744), 화살표 간격 48. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 468
d = D(W, H, "LEARNING EBPF · 05-02 §3",
      "ksyscall 섹션이 아키텍처별 함수에 붙고 매크로가 인자를 꺼낸다",
      "부착 때 libbpf 가 섹션 이름을 아키텍처별 커널 함수로 풀어 kprobe 를 걸고, execve 가 불릴 때마다 매크로가 pt_regs 에서 pathname 을 꺼내 hello() 가 이벤트 한 건을 output 맵에 내보낸다.",
      "위 줄은 부착 때와 실행 때, 아래 줄은 숨은 ctx 와 출력입니다")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def stage(x, title, lines, c):
    d.tone(x, 108, 192, 124, c, 6, "12", 1.2)
    d.t(x + 96, 136, title, 13, INK, fam(title), "middle", 600)
    for i, s in enumerate(lines):
        d.t(x + 96, 162 + 20 * i, s, 12, MUTED, fam(s), "middle")


stage(24, "SEC 이름", ["ksyscall/execve", "부착 때 libbpf 가 읽음"], INFO)
stage(264, "부착 함수", ["__x64_sys_execve", "__arm64_sys_execve", "아키텍처별 이름"], INFO)
stage(504, "BPF_KPROBE_SYSCALL", ["pt_regs → pathname", "execve 마다 실행"], OK)
stage(744, "hello() 본문", ["pid 23664 · uid 501", "comm bash", "my_config[501] 없음", "→ Hello World"], OK)

for x in (216, 456, 696):
    d.arrow([(x + 2, 170), (x + 44, 170)], MUTED, "ar", 1.5)

# 매크로 안의 ctx — focal
d.arrow([(600, 232), (600, 296)], ACC, "acc", 1.6)
d.tone(504, 300, 192, 80, ACC, 6, "14", 1.6)
d.t(600, 332, "ctx", 14, INK, MONO, "middle", 600)
d.t(600, 356, "매크로 안에 선언", 12, MUTED, KR, "middle")

# hello() → perf 맵
d.arrow([(840, 232), (840, 296)], MUTED, "ar", 1.5)
d.chip(840, 264, "bpf_perf_event_output", MUTED, 11)
d.tone(744, 300, 192, 80, MUTED, 6, "10", 1.1)
d.t(840, 332, "output", 14, INK, MONO, "middle", 600)
d.t(840, 356, "PERF_EVENT_ARRAY", 12, MUTED, MONO, "middle")
d.arrow([(698, 340), (740, 340)], ACC, "acc", 1.6)

d.legend(H - 56, [("부착 때", INFO), ("실행 때", OK), ("숨은 ctx", ACC), ("출력 맵", MUTED)])
d.save("05-02.ksyscall-attach.svg")
