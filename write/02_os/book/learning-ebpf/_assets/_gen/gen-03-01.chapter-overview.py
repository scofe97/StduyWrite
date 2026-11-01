# 타입 스펙: type-process — C 소스가 컴파일·검증·적재를 거쳐 BPF 식별자를 얻기까지의 생애주기
# 사실 출처: 《Learning eBPF》 Ch.3 1쪽 Figure 3-1(C → eBPF bytecode → machine code), 4쪽 hello.bpf.c, 6쪽 clang 플래그,
#   7쪽 llvm-objdump 12슬롯(xdp 섹션), 9쪽 bpftool prog load·prog list(540 · tag · xlated 96B · jited 148B). 본문 §1~§4
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 330
d = D(W, H, "LEARNING EBPF · 03-01",
      "C 소스부터 커널 적재까지 eBPF 프로그램의 여정",
      "clang 컴파일·bpftool 적재·검증·식별자 부여 과정",
      "C 소스 작성 · 바이트코드 컴파일 · verifier 검증과 적재 · 고정 경로와 식별자")

# 프로세스 단계 (sec, title, sub, color, mono, [sub2])
NW, NH = 148, 100
Y = 130
STEPS = [
    ("§2", "hello.bpf.c", "SEC(\"xdp\")", INFO, True),
    ("§3", "clang", "-target bpf -g -O2", ACC, True),
    ("§1·§3", "hello.bpf.o", "8바이트 슬롯 12개", INFO, True, "xdp 섹션"),
    ("§4", "bpftool prog load", "/sys/fs/bpf/hello", ACC, True, "verifier 통과"),
    ("§4", "ID 540", "xlated 96B", OK, True, "tag d35b94b4c0c10efb"),
]

XS = [36 + i * 156 for i in range(5)]

def font_for(text):
    return KR if any('가' <= ch <= '힣' for ch in str(text)) else MONO

for i, step in enumerate(STEPS):
    sec, title, sub, c, is_mono = step[:5]
    sub2 = step[5] if len(step) > 5 else None
    x = XS[i]
    d.tone(x, Y, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW//2, Y + 22, sec, 11, SOFT, MONO, "middle")
    d.t(x + NW//2, Y + 44, title, 13, c, MONO if is_mono else KR, "middle", 600)
    d.t(x + NW//2, Y + 64, sub, 12, MUTED, font_for(sub), "middle")
    if sub2:
        d.t(x + NW//2, Y + 84, sub2, 11, MUTED, font_for(sub2), "middle")
    if i < 4:
        d.arrow([(x + NW + 2, Y + NH//2), (XS[i+1] - 4, Y + NH//2)], MUTED, "ar", 1.4)

# 다음 편 예고 노드 (점선)
NEXT_X = XS[4] + 156
d.box(NEXT_X, Y, 108, NH, PAPER, WARN, 1.0, 6)
d.t(NEXT_X + 54, Y + 22, "03-02", 11, SOFT, MONO, "middle")
d.t(NEXT_X + 54, Y + 44, "JIT 148B", 12, MUTED, MONO, "middle", 600)
d.t(NEXT_X + 54, Y + 64, "XDP 부착", 12, MUTED, KR, "middle")
d.t(NEXT_X + 54, Y + 84, "다음 편", 11, SOFT, KR, "middle")
d.arrow([(XS[4] + NW + 2, Y + NH//2), (NEXT_X - 4, Y + NH//2)], WARN, "warn", 1.4, dash="3 3")

d.legend(H - 46, [
    ("소스 및 오브젝트", INFO),
    ("빌드 및 적재 도구", ACC),
    ("적재 완료 및 식별자", OK),
    ("후속 과정 예고", WARN),
])

d.save("03-01.chapter-overview.svg")
