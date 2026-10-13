# 타입 스펙: type-layers — 위에서 아래로 쌓인 다섯 층(bpftrace · BCC · libbpf · bpf() · 커널)과 각 층에서 커널 쪽·사용자 공간 쪽을 쓰는 주체, 오른쪽 가장자리에 Go·Rust 라이브러리가 붙는 자리.
# 사실 출처: 추출본 ebpf10.txt 18~21행(양쪽을 짜야 하는 라이브러리, bpftrace 는 구분을 감춤), 25~35행(bpftrace), 255~301행(BCC), 361~384행(libbpf), 408~413행(다른 언어 라이브러리가 libbpf 를 감싸거나 재배치 제공).
#   층 안의 코드 문자열은 본문 §1 한 줄 스크립트(`tracepoint:… { @[comm] = count(); }`, kprobe:do_execve 는 v7.2 에 없음), 285~299행(BCC Python+C 문자열).
# Layout conventions: 층 높이 64, stride 76(y=104~408), 층 폭 620(x=100~720), 오른쪽 상자 x=776~944, 모든 좌표 4의 배수. accent 는 한 층(bpftrace)에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 10-01",
      "층마다 커널 쪽과 사용자 공간 쪽을 쓰는 주체가 다르다",
      "위로 갈수록 두 쪽의 경계를 도구가 감추고, 아래로 갈수록 프로그래머가 양쪽을 직접 짠다. Go·Rust 라이브러리는 libbpf 층과 bpf() 층에 붙는다.",
      "위는 추상화된 층, 아래는 커널")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


LX, LW, LH, STRIDE, Y0 = 100, 620, 64, 76, 104
rows = [
    ("01", "bpftrace 스크립트", "tracepoint:… { @[comm] = count(); }", ("커널·사용자 쪽 모두", "도구가 생성"), ACC),
    ("02", "BCC", "Python + C 문자열 · 실행 때 Clang", ("커널 쪽 C 문자열", "사용자 쪽 Python"), OK),
    ("03", "libbpf", "*.bpf.c 미리 컴파일 + 사용자 C + 스켈레톤", ("커널 쪽 *.bpf.c", "사용자 쪽 C"), OK),
    ("04", "bpf() syscall", "BPF_PROG_LOAD · BPF_MAP_CREATE", ("사용자 공간 → 커널", "경계 syscall"), MUTED),
    ("05", "커널", "verifier · JIT · 맵", ("커널 안", "검증 · 컴파일 · 저장"), MUTED),
]
for i, (idx, name, code, who, c) in enumerate(rows):
    y = Y0 + i * STRIDE
    d.tone(LX, y, LW, LH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(LX + 12, y + 18, idx, 9, SOFT, MONO, "start")
    d.t(LX + 48, y + 30, name, 15, INK, fam(name), "start", 600)
    d.t(LX + 48, y + 52, code, 12, MUTED, fam(code), "start")
    d.t(LX + LW - 12, y + 28, who[0], 12, MUTED, KR, "end")
    d.t(LX + LW - 12, y + 48, who[1], 12, MUTED, KR, "end")

# 왼쪽 방향 표지
d.arrow([(60, 464), (60, 112)], SOFT, "soft", 1.4)
d.chip(60, 292, "추상화", SOFT, 12)

# 오른쪽 Go·Rust 라이브러리 상자와 두 부착점
BX, BY, BW, BH = 776, Y0 + 2 * STRIDE, 168, STRIDE + LH
d.tone(BX, BY, BW, BH, INFO, 6, "12", 1.2)
d.t(BX + BW / 2, BY + 52, "Go · Rust", 15, INK, MONO, "middle", 600)
d.t(BX + BW / 2, BY + 76, "라이브러리", 13, MUTED, KR)
d.arrow([(BX - 2, Y0 + 2 * STRIDE + 32), (LX + LW + 6, Y0 + 2 * STRIDE + 32)], INFO, "info", 1.5)
d.arrow([(BX - 2, Y0 + 3 * STRIDE + 32), (LX + LW + 6, Y0 + 3 * STRIDE + 32)], INFO, "info", 1.5)

d.legend(H - 56, [("경계를 감춤", ACC), ("양쪽을 직접 작성", OK), ("경계 · 커널", MUTED), ("다른 언어", INFO)])
d.save("10-01.chapter-overview.svg")
