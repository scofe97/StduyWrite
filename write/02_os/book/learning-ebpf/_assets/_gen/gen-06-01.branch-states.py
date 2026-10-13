# 타입 스펙: type-tree — 뿌리 하나(조건 점프 30번), 가지 둘(이어지는 쪽 · 점프하는 쪽), 잎 둘(실패 · 꺼내지 못함).
# 사실 출처: 추출본 src/ebpf6.txt 477~491행(30: if r1 > 0xc goto pc+10, R1 umax_value=12, 34: *(u8 *)(r2 +0), R2 off=4 vs=16),
#   커널 v7.2 kernel/bpf/verifier.c 16088행(점프 목표를 push_stack), 17511행(pop_stack), kernel/bpf/cfg.c 120~121행(분기 목표 가지치기 지점).
#   41 = 30 + 1 + 10(pc+10). 34번에서 실패하면 검증이 끝나 push 된 사본은 꺼내지지 않는다(노트 §1).
# Layout conventions: 뿌리 w=288 h=48, 가지 w=320 h=64 중심 x=264·696, 잎 w=256 h=48. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, KR, MONO

W = 960
RX, RY, RW, RH = 336, 108, 288, 48
CY, CW, CH = 208, 320, 64
LCX, RCX = 264, 696
LY, LW, LH = 328, 256, 48
LEG_Y = LY + LH + 40
H = LEG_Y + 56

d = D(W, H, "LEARNING EBPF · 06-01 §1",
      "조건 점프 하나가 만드는 두 경로",
      "점프하는 쪽의 상태 사본은 스택에 들어가고, 이어지는 쪽이 먼저 끝까지 간다. 한 경로라도 걸리면 프로그램 전체가 거부된다.",
      "30번 명령에서 R1 의 상한 12 가 두 경로를 가른다")

# 뿌리
d.tone(RX, RY, RW, RH, ACC, 6, "18", 1.4)
d.t(RX + RW / 2, RY + 30, "30: if r1 > 0xc goto pc+10", 13, ACC, MONO, "middle", 600)

# 가지
d.tone(LCX - CW // 2, CY, CW, CH, INFO, 6, "12", 1.2)
d.t(LCX, CY + 28, "31 → 34", 13, INFO, MONO, "middle", 600)
d.t(LCX, CY + 48, "r1 ≤ 12 · 이어지는 쪽", 13, MUTED, KR)
d.tone(RCX - CW // 2, CY, CW, CH, WARN, 6, "12", 1.2)
d.t(RCX, CY + 28, "41 · 가지치기 지점", 13, WARN, KR, "middle", 600)
d.t(RCX, CY + 48, "r1 > 12 · push 된 사본", 13, MUTED, KR)

# 잎
d.tone(LCX - LW // 2, LY, LW, LH, BAD, 6, "12", 1.2)
d.t(LCX, LY + 30, "34: off=16 size=1", 13, BAD, MONO, "middle", 600)
d.tone(RCX - LW // 2, LY, LW, LH, WARN, 6, "12", 1.2)
d.t(RCX, LY + 30, "꺼내지 못함", 13, WARN, KR, "middle", 600)

# 간선 — 모두 직각
d.arrow([(RX + 40, RY + RH), (RX + 40, 184), (LCX, 184), (LCX, CY)], INFO, "info", 1.5)
d.arrow([(RX + RW - 40, RY + RH), (RX + RW - 40, 184), (RCX, 184), (RCX, CY)], WARN, "warn", 1.5)
d.arrow([(LCX, CY + CH), (LCX, LY)], BAD, "bad", 1.5)
d.arrow([(RCX, CY + CH), (RCX, LY)], WARN, "warn", 1.5)

d.legend(LEG_Y, [("갈래", INFO), ("push · 가지치기", WARN), ("실패", BAD), ("분기 명령", ACC)])
d.save("06-01.branch-states.svg")
