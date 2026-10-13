# 타입 스펙: type-process — bpf() 적재부터 verifier 검증, JIT 컴파일, 이벤트 부착, 맵 요약 전달까지 eBPF 실행 5단계
# 사실 출처: 원문 ebpf1.txt 364-418(bpf() 시스템 콜·검증기 안전성 검사·JIT 네이티브 실행·BPF 맵 요약 전달)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 390
d = D(W, H, "LEARNING EBPF · 01-01 §4", "eBPF 프로그램 적재부터 실행까지 5단계 흐름",
      "바이트코드가 검증기를 거쳐 네이티브 코드로 변환된 뒤 이벤트마다 실행됩니다",
      "bpf() 적재 · verifier 검사 · JIT 네이티브 실행 · BPF 맵 요약")

Y_TOP, H_CARD, W_CARD, GAP, X0 = 104, 160, 152, 20, 40
steps = [
    ("01 적재", "bpf() 시스템 콜", "재부팅 불필요", "한도 4,096 · 1,000,000", INFO),
    ("02 검증", "verifier", "멈춤·끝없는 루프 검사", "통과한 것만 적재", ACC),
    ("03 JIT 컴파일", "JIT 컴파일러", "네이티브 기계어", "CPU 직접 실행", OK),
    ("04 이벤트 부착", "kprobe · XDP", "실행 중 프로세스도", "이벤트마다 실행", OK),
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

    d.t(cx, Y_TOP + 64, c1, 12, col, MONO if "-" in c1 or "." in c1 or "(" in c1 else KR, "middle", 600)
    d.t(cx, Y_TOP + 90, c2, 12, INK, KR, "middle")
    d.t(cx, Y_TOP + 116, c3, 11, MUTED, KR, "middle")

    if i < len(steps) - 1:
        ax = x + W_CARD
        d.arrow([(ax + 2, Y_TOP + H_CARD / 2), (ax + GAP - 2, Y_TOP + H_CARD / 2)], MUTED, "ar", 1.2)

d.legend(336, [
    ("적재", INFO),
    ("verifier 검증", ACC),
    ("커널 안 실행", OK),
])
d.save("01-01.ebpf-load-process.svg")
