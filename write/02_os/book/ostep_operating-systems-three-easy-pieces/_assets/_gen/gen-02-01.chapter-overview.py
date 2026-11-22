# 02-01 개념도 — 프로세스 한 개가 적재에서 회수까지 일생을 거치고, 시분할이 그 일생을 받치며, 운영체제가 PCB 와 프로세스 목록으로 일생을 추적한다.
# 본문 요구(02-01 「학습 목표」 개념도 문단): 가운데 줄은 적재(§3) → 실행 중 세 상태(§4) → zombie → 부모의 회수(§5),
#           위 띠는 시분할이 만드는 CPU 환상(§1), 아래 띠는 PCB 와 프로세스 목록(§5), 곁가지는 프로세스 API(§2).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 4장 §4.1~§4.5 (VERSION 1.10).
# 타입 스펙: type-state — 대상 하나(프로세스)가 국면을 차례로 지나고 종료(zombie 와 회수)가 정상 경로만큼 중요한 생애 지도.
#             고른 이유: 이 장의 줄기는 인과나 절 목록이 아니라 한 프로세스의 일생이다. 일생 한 줄에 실행 중 세 상태의 순환을
#             한 덩어리로 얹고, 위아래에 일생을 받치는 띠를 둔다. 스펙에 이 모양의 공식은 없어 좌표는 직접 잡았다.
#             (옛 판의 6행 × 3열 격자 공식 열 x = 60 + j·340 은 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 696


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "STATE · 02-01 OVERVIEW",
      "프로세스는 적재에서 회수까지 일생을 거치고 운영체제가 목록으로 추적한다",
      "02-01 의 키워드 개념도. 가운데 줄은 프로세스 한 개의 일생이다. 디스크의 프로그램이 적재되어 main 에서 시작하고, 실행 중에는 Ready 와 Running 과 Blocked 를 오가다 끝나면 zombie 로 남고, 부모가 wait 로 회수한다. "
      "위 띠는 물리 CPU 몇 개를 번갈아 돌리는 시분할이 CPU 가 끝없이 있는 듯한 환상을 만들고 Ready 와 Running 사이의 오감을 낳는 까닭이다. "
      "아래 띠는 운영체제가 프로세스마다 PCB 를 두고 프로세스 목록으로 묶어 상태를 추적하는 방법이다. 오른쪽 위 곁가지는 프로세스 API 다.",
      lead="화살표 옆 글자는 두 요소의 관계, 칩은 그 요소를 다루는 절입니다. 가운데 줄이 일생이고 위아래 띠가 일생을 받칩니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.chip(x + 24, y + 14, sec, c if c != MUTED else MUTED, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


def head(y, cap, x2):
    d.t(24, y, cap, 13, MUTED, KR, "start", 600)
    d.line(24, y + 8, x2, y + 8, RULE, 0.8)


# 구역 머리
head(108, "왜 이렇게 하나", 232)
head(236, "프로세스의 일생", 232)
head(508, "운영체제의 추적", 232)

# 위 띠 — 시분할이 만드는 환상
TY = 132
node(24, TY, 160, 72, "물리 CPU 몇 개", "수십 · 수백 프로세스", INFO, "§1")
node(248, TY, 160, 72, "시분할", "돌리다 멈추기를 되풀이", INFO, "§1")
node(480, TY, 180, 72, "CPU 환상", "끝없이 있는 듯한", ACC, "§1")
d.arrow([(186, TY + 36), (246, TY + 36)], INFO, "info", 1.5)
d.t(216, TY + 26, "번갈아", 13, MUTED, KR, "middle", 600)
d.arrow([(410, TY + 36), (478, TY + 36)], INFO, "info", 1.5)
d.t(444, TY + 26, "겉보기에", 13, MUTED, KR, "middle", 600)

# 곁가지 — 프로세스 API
node(712, TY, 240, 72, "프로세스 API", "생성 · 대기 · 소멸 · 제어 · 상태", MUTED, "§2")

# 가운데 줄 — 일생
LY = 336
node(24, 294, 176, 84, "프로그램 적재", "디스크 → 주소 공간", INFO, "§3", "스택 · 힙 · 표준 입출력")

# 실행 중 세 상태 (한 덩어리)
d.box(248, 252, 328, 220, "#161B22", RULE, 1.0, 8)
d.chip(272, 266, "§4", INFO, 11)
d.t(412, 292, "실행 중 세 상태", 14, INFO, KR, "middle", 600)
for x, y, name in ((264, 314, "Ready"), (472, 314, "Running"), (472, 412, "Blocked")):
    d.tone(x, y, 88, 44, INFO, 6, "14", 1.1)
    d.t(x + 44, y + 28, name, 14, INFO, MONO, "middle", 600)
d.arrow([(356, 328), (468, 328)], INFO, "info", 1.4)
d.t(412, 322, "scheduled", 13, MUTED, MONO, "middle", 600)
d.arrow([(468, 344), (356, 344)], INFO, "info", 1.4)
d.t(412, 364, "descheduled", 13, MUTED, MONO, "middle", 600)
d.arrow([(516, 360), (516, 410)], INFO, "info", 1.4)
d.t(508, 390, "I/O 시작", 13, MUTED, KR, "end", 600)
d.arrow([(470, 434), (308, 434), (308, 362)], INFO, "info", 1.4)
d.t(392, 424, "I/O 완료", 13, MUTED, KR, "middle", 600)

d.arrow([(202, LY), (246, LY)], INFO, "info", 1.5)
d.t(224, LY - 10, "시작", 13, MUTED, KR, "middle", 600)

# 시분할 → 세 상태
d.arrow([(328, 206), (328, 250)], INFO, "info", 1.5)
d.t(340, 232, "Ready 와 Running 을 오가며", 13, MUTED, KR, "start", 600)

# 세 상태 → zombie → 회수
d.arrow([(578, LY), (638, LY)], INFO, "info", 1.5)
d.t(608, LY - 10, "끝나면", 13, MUTED, KR, "middle", 600)
node(640, 300, 120, 72, "zombie", "끝났지만 정리 전", INFO, "§5")
d.arrow([(762, LY), (830, LY)], INFO, "info", 1.5)
d.t(796, LY - 10, "wait()", 13, MUTED, MONO, "middle", 600)
node(832, 300, 120, 72, "부모가 회수", "반환값 · 정리", INFO, "§5")

# 곁가지 → 회수
d.arrow([(892, TY + 74), (892, 298)], SOFT, "soft", 1.3, "4 3")
d.t(884, 256, "대기 기능", 13, MUTED, KR, "end", 600)

# 아래 띠 — 추적
BY = 540
node(24, BY, 180, 72, "PCB", "프로세스마다 하나", OK, "§5")
node(296, BY, 656, 72, "프로세스 목록", "시스템의 모든 프로세스 정보", OK, "§5")
d.arrow([(206, BY + 36), (294, BY + 36)], OK, "ok", 1.4)
d.t(250, BY + 26, "묶어", 13, MUTED, KR, "middle", 600)
d.arrow([(412, BY - 2), (412, 474)], OK, "ok", 1.4)
d.t(424, 512, "상태를 추적", 13, MUTED, KR, "start", 600)
d.arrow([(700, 374), (700, BY - 2)], OK, "ok", 1.4)
d.t(712, 460, "칸을 차지", 13, MUTED, KR, "start", 600)

d.legend(H - 40, [("프로세스의 일생과 시분할", INFO), ("추적 장치", OK), ("핵심 환상", ACC), ("곁가지", MUTED)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01 overview")
