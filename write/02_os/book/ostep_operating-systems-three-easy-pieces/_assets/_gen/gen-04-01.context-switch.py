# 04-01 「레지스터는 두 번 저장되고 두 번 복원된다」 — 하드웨어는 사용자 레지스터를 커널 스택에, 운영체제의 swtch 는 커널 레지스터를 프로세스 구조에 옮긴다.
# 본문 근거: 이 노트 「4. 문맥 교환이 레지스터를 옮기는 방식」.
# 값 근거: 개념 도식이라 값은 없다. 화살표 번호는 원서 그림 6.3 의 시간순이다.
# 공식 근거: OSTEP 6장 §6.3 — 타이머 인터럽트 때 사용자 레지스터는 하드웨어가 그 프로세스의 커널 스택에 저장하고, 운영체제가 A 에서 B 로 바꿀 때 커널 레지스터는 소프트웨어가 프로세스 구조 메모리에 저장한다.
# 타입 스펙: type-data-flow — 값이 레지스터와 메모리 사이를 어디로 움직이는지. 화살표마다 누가 옮기는지를 색으로 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, INFO, KR, MONO

W, H = 920, 592
d = D(W, H, "OSTEP · 04-01 §4",
      "A 에서 B 로 바꾸는 타이머 인터럽트 한 번에 저장 둘, 복원 둘이 일어난다",
      "프로세스 A 가 타이머 인터럽트로 끊기면 하드웨어가 A 의 사용자 레지스터를 A 의 커널 스택에 저장하고, 운영체제의 swtch 가 커널 레지스터를 A 의 프로세스 구조에 저장한다. "
      "이어서 swtch 가 B 의 프로세스 구조에서 커널 레지스터를 복원하고 B 의 커널 스택으로 바꾸며, return-from-trap 이 B 의 커널 스택에서 사용자 레지스터를 복원해 B 를 실행한다.")

BW, BH = 240, 56
LX, RX = 24, W - 48 - BW + 24   # 왼쪽·오른쪽 열 시작 x
CXL, CXR = 340, 580             # 가운데 상자 좌우

def mem(x, y, name, sub):
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, y + 24, name, 13, INK, MONO, "middle", 600)
    d.t(x + BW / 2, y + 44, sub, 12, MUTED, KR)

d.t(LX + BW / 2, 130, "A 쪽 커널 메모리", 12, MUTED, KR, "middle", 600)
d.t(RX + BW / 2, 130, "B 쪽 커널 메모리", 12, MUTED, KR, "middle", 600)
mem(LX, 150, "k-stack(A)", "사용자 레지스터 · PC")
mem(LX, 400, "proc_t(A)", "커널 레지스터(context)")
mem(RX, 150, "k-stack(B)", "사용자 레지스터 · PC")
mem(RX, 400, "proc_t(B)", "커널 레지스터(context)")

# 가운데: CPU 레지스터
d.tone(CXL, 244, CXR - CXL, 96, SOFT, 6, "22", 1.1)
d.t((CXL + CXR) / 2, 280, "CPU 레지스터", 14, INK, KR, "middle", 600)
d.t((CXL + CXR) / 2, 304, "지금 실행 중인 쪽의 값", 12, MUTED, KR)
d.t((CXL + CXR) / 2, 324, "A 가 쓰던 값 → B 가 쓸 값", 12, MUTED, KR)

ax, bx = LX + BW / 2, RX + BW / 2
# 1. 하드웨어가 A 의 사용자 레지스터를 k-stack(A) 에
d.arrow([(CXL, 266), (ax, 266), (ax, 206)], ACC, "acc", 1.6)
d.t(ax + 14, 252, "1. 하드웨어가 저장", 12, ACC, KR, "start", 600)
# 2. swtch 가 A 의 커널 레지스터를 proc_t(A) 에
d.arrow([(CXL, 318), (ax, 318), (ax, 398)], INFO, "info", 1.6)
d.t(ax + 14, 342, "2. swtch 가 저장", 12, INFO, KR, "start", 600)
# 3. swtch 가 proc_t(B) 에서 커널 레지스터를 복원
d.arrow([(bx, 400), (bx, 318), (CXR, 318)], INFO, "info", 1.6)
d.t(bx - 14, 342, "3. swtch 가 복원", 12, INFO, KR, "end", 600)
# 4. return-from-trap 이 k-stack(B) 에서 사용자 레지스터를 복원
d.arrow([(bx, 206), (bx, 266), (CXR, 266)], ACC, "acc", 1.6)
d.t(bx - 14, 252, "4. return-from-trap 이 복원", 12, ACC, KR, "end", 600)

# 가운데 아래: 커널 스택 전환
d.chip(bx - 200, 376, "3 번에서 스택이 k-stack(B) 로 바뀜", INFO, 12, 8)

d.legend(H - 56, [("하드웨어가 옮김", ACC), ("운영체제(swtch)가 옮김", INFO), ("CPU 레지스터", SOFT)])
d.save("04-01.context-switch.svg")
print("ok 04-01 context-switch")
