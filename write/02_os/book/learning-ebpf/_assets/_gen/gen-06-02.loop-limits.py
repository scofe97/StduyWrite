# 타입 스펙: type-loop — 고리 셋을 가로 줄 셋으로 편다. 같은 바퀴를 반복해서 그려 verifier 가 따라가는 경로 길이를 보인다.
# 사실 출처: 예제 chapter6/hello-verifier.bpf.c 84~86행(i < 10)·89~91행(i < c), 추출본 src/ebpf6.txt 656~666행(10바퀴·한도),
#   669~677행(bpf_loop 설명), 커널 v7.2 include/linux/bpf.h 2386행(1,000,000), verifier.c 17367행(too large),
#   include/uapi/linux/bpf.h bpf_loop 설명(콜백이 1 이면 중단, nr_loops 상한 1 << 23), verifier.c 9766행(콜백 호출 지점으로 되돌아가 수렴하면 가지치기). 바퀴 수 외의 누적 수치는 싣지 않는다.
# Layout conventions: 줄 stride 80, 바퀴 칸 w=44 h=44 gap=8, 라벨 열 x=24 w=208, 끝 상자 x=776 w=160. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W = 960
Y0, STRIDE, BH = 124, 88, 44
# 거부 칸은 바퀴 수가 아니라 처리 명령 한도(BPF_COMPLEXITY_LIMIT_INSNS)라 "명령" 을 붙인다. 칸 폭 136 에 맞춰 100만으로 줄여 쓴다.
X0, BW, GAP = 248, 44, 8
EX, EW = 800, 136
LEG_Y = Y0 + 3 * STRIDE
H = LEG_Y + 56

d = D(W, H, "LEARNING EBPF · 06-02 §3",
      "루프 셋이 처리 한도에 닿는 방식",
      "상수 상한 루프는 바퀴 수만큼, 상한을 모르는 루프는 한도까지, bpf_loop 는 콜백을 수렴까지만 따라간다.",
      "칸 하나 = verifier 가 따라가는 한 바퀴")


def label(y, code, sub):
    d.t(24, y + 20, code, 13, INK, MONO, "start", 600)
    d.t(24, y + 40, sub, 13, MUTED, KR, "start")


# 줄 A — i < 10
yA = Y0
label(yA, "i < 10", "상한이 상수")
for k in range(10):
    x = X0 + k * (BW + GAP)
    d.tone(x, yA, BW, BH, INFO, 4, "12", 1.1)
    d.t(x + BW / 2, yA + 28, str(k), 12, INFO, MONO)
d.arrow([(X0 + 10 * (BW + GAP) - 4, yA + BH / 2), (EX - 4, yA + BH / 2)], OK, "ok", 1.5)
d.tone(EX, yA, EW, BH, OK, 6, "12", 1.2)
d.t(EX + EW / 2, yA + 28, "10바퀴 · 통과", 13, OK, KR, "middle", 600)

# 줄 B — i < c
yB = Y0 + STRIDE
label(yB, "i < c", "c 는 맵에서 읽은 값")
for k in range(8):
    x = X0 + k * (BW + GAP)
    d.tone(x, yB, BW, BH, INFO, 4, "12", 1.1)
    d.t(x + BW / 2, yB + 28, str(k), 12, INFO, MONO)
d.t(X0 + 8 * (BW + GAP) + 28, yB + 28, "· · ·", 13, MUTED, MONO)
d.arrow([(X0 + 8 * (BW + GAP) + 64, yB + BH / 2), (EX - 4, yB + BH / 2)], BAD, "bad", 1.5)
d.tone(EX, yB, EW, BH, BAD, 6, "12", 1.2)
d.t(EX + EW / 2, yB + 28, "100만 명령 · 거부", 13, BAD, KR, "middle", 600)

# 줄 C — bpf_loop
yC = Y0 + 2 * STRIDE
label(yC, "bpf_loop(N, cb)", "콜백 몸체")
d.tone(X0, yC, 3 * BW + 2 * GAP, BH, ACC, 4, "18", 1.4)
d.t(X0 + (3 * BW + 2 * GAP) / 2, yC + 28, "cb", 13, ACC, MONO, "middle", 600)
d.chip(X0 + 3 * BW + 2 * GAP + 96, yC + BH / 2, "수렴까지 검증", OK, 13)
d.arrow([(X0 + 3 * BW + 2 * GAP + 164, yC + BH / 2), (EX - 4, yC + BH / 2)], OK, "ok", 1.5)
d.tone(EX, yC, EW, BH, OK, 6, "12", 1.2)
d.t(EX + EW / 2, yC + 28, "횟수와 무관 · 통과", 13, OK, KR, "middle", 600)

d.legend(LEG_Y, [("따라간 바퀴", INFO), ("통과", OK), ("거부", BAD), ("콜백", ACC)])
d.save("06-02.loop-limits.svg")
