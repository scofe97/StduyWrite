# 타입 스펙: type-process — bpf() 적재부터 verifier 검증, JIT 컴파일, 이벤트 부착, 맵 요약 전달까지 eBPF 실행 흐름
# 사실 출처: 《Learning eBPF》 Ch.1 10~12쪽(동적 적재·verifier 10쪽, JIT·커널 안 필터링 11~12쪽), 본문 §4(156~162행: bpf() 로 실행 중 커널에 적재·적재 전 검사 후 통과한 것만 적재·JIT·파일 열기 시스템 콜 부착·맵 요약)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 390
d = D(W, H, "LEARNING EBPF · 01-01 §4", "eBPF 프로그램 적재부터 실행·맵 집계 흐름",
      "검증기와 JIT 컴파일을 거친 네이티브 실행 및 맵 요약 집계 흐름",
      "bpf() 적재 · verifier 검사 · JIT 네이티브 실행 · BPF 맵 요약")

Y_TOP, H_CARD, W_CARD, GAP, X0 = 104, 160, 152, 20, 40
steps = [
    ("01 적재 요청", "bpf() 시스템 콜", "재부팅 불필요", "실행 중 커널 대상", INFO),
    ("02 검증", "verifier", "멈춤·루프·침범 검사", "통과한 것만 적재", ACC),
    ("03 JIT 컴파일", "JIT 컴파일러", "네이티브 기계어", "CPU 직접 실행", OK),
    ("04 이벤트 부착", "파일 열기 시스템 콜", "실행 중 프로세스도", "이벤트마다 실행", OK),
    ("05 맵에 요약", "BPF 맵", "요약 통계 기록", "필요한 데이터만 전달", OK),
]

for i, (num_title, c1, c2, c3, col) in enumerate(steps):
    x = X0 + i * (W_CARD + GAP)
    cx = x + W_CARD / 2
    if col == ACC:
        d.tone(x, Y_TOP, W_CARD, H_CARD, ACC, r=6, op="14", sw=1.3)
    else:
        d.box(x, Y_TOP, W_CARD, H_CARD, PAPER2, RULE, 0.9, 6)

    d.t(cx, Y_TOP + 24, num_title, 13, col, KR, "middle", 600)
    d.line(x + 10, Y_TOP + 36, x + W_CARD - 10, Y_TOP + 36, RULE, 0.6)

    d.t(cx, Y_TOP + 64, c1, 12, col, KR if any("가" <= ch <= "힣" for ch in c1) else MONO, "middle", 600)
    d.t(cx, Y_TOP + 90, c2, 12, INK, KR, "middle")
    d.t(cx, Y_TOP + 116, c3, 12, MUTED, KR, "middle")

    if i < len(steps) - 1:
        ax = x + W_CARD
        d.arrow([(ax + 2, Y_TOP + H_CARD / 2), (ax + GAP - 2, Y_TOP + H_CARD / 2)], MUTED, "ar", 1.2)

d.legend(336, [
    ("적재 요청", INFO),
    ("verifier 검증", ACC),
    ("커널 안 실행", OK),
])
d.save("01-01.ebpf-load-process.svg")
