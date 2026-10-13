# 타입 스펙: type-process — C 소스가 컴파일·검증·적재를 거쳐 BPF 식별자를 얻기까지의 생애주기
# 사실 출처: 본문 §3 llvm-objdump 12슬롯, §4 bpftool prog show id 540 (bytes_xlated 96, bytes_jited 148)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 380
d = D(W, H, "LEARNING EBPF · 03-01",
      "C 소스부터 커널 적재까지 eBPF 프로그램의 여정",
      "Clang 컴파일러로 바이트코드를 만들고 bpftool 로 커널에 적재하여 식별자를 부여받습니다",
      "C 소스 작성 · 바이트코드 컴파일 · bpftool 적재 및 고정 · 검증과 식별자 할당")

# 프로세스 단계 (x, y, w, h, title, sub, color, mono)
NW, NH = 148, 100
Y = 130
STEPS = [
    ("hello.bpf.c", "SEC(\"xdp\")", INFO, True),
    ("clang", "-target bpf -g -O2", OK, True),
    ("hello.bpf.o", "xdp 섹션 · 12슬롯", INFO, True),
    ("bpftool load", "/sys/fs/bpf/hello", ACC, True, "verifier 통과"),
    ("ID 540", "xlated 96B", OK, True, "tag d35b94b4c0c10efb"),
]

XS = [36 + i * 156 for i in range(5)]

for i, step in enumerate(STEPS):
    title, sub, c, is_mono = step[:4]
    sub2 = step[4] if len(step) > 4 else None
    x = XS[i]
    d.tone(x, Y, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW//2, Y + 22, f"0{i+1}", 11, SOFT, MONO, "middle")
    d.t(x + NW//2, Y + 44, title, 13, c, MONO if is_mono else KR, "middle", 600)
    d.t(x + NW//2, Y + 64, sub, 11, MUTED, MONO if any(ch in sub for ch in "()./-") else KR, "middle")
    if sub2:
        d.t(x + NW//2, Y + 84, sub2, 11, MUTED, MONO if any(ch in sub2 for ch in "()./-") or sub2.startswith("tag") else KR, "middle")
    if i < 4:
        d.arrow([(x + NW + 2, Y + NH//2), (XS[i+1] - 4, Y + NH//2)], MUTED, "ar", 1.4)

# 다음 편 예고 노드 (점선)
NEXT_X = XS[4] + 156
d.box(NEXT_X, Y, 130, NH, PAPER, RULE, 1.0, 6)
d.t(NEXT_X + 65, Y + 22, "다음 편", 11, SOFT, KR, "middle")
d.t(NEXT_X + 65, Y + 44, "JIT 148B", 12, MUTED, MONO, "middle", 600)
d.t(NEXT_X + 65, Y + 64, "XDP 부착", 11, MUTED, KR, "middle")
d.arrow([(XS[4] + NW + 2, Y + NH//2), (NEXT_X - 4, Y + NH//2)], WARN, "warn", 1.4, dash="3 3")

d.legend(H - 46, [
    ("소스 및 바이너리", INFO),
    ("컴파일 및 적재", OK),
    ("고정 파일시스템", ACC),
    ("후속 과정 예고", WARN),
])

d.save("03-01.chapter-overview.svg")
