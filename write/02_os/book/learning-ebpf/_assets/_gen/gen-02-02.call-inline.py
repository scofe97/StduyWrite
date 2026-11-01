# 타입 스펙: type-architecture — 좌우 두 구획(일반 함수 호출 vs 인라인)으로 같은 호출 지점 둘의 명령어 배치와 jump 를 대조한다.
# 사실 출처: 원서 Ch.2 16쪽 Figure 2-5 "Layout of noninlined and inlined function instructions"(왼쪽 jump 와 Jump back, 오른쪽 인라인 복사)
#   및 본문 163행(jump 로 본문에 갔다 호출한 자리 다음으로 돌아옴 · 인라인은 jump 없이 본문 명령어 복사), 정답 3 289행(지점이 둘이면 본문도 두 벌).
#   원서 그림은 호출 지점 하나를 그린다. 본문 289행의 "지점이 둘이면" 을 양쪽에 같게 적용해 호출 지점을 둘로 맞췄다.
# Layout conventions: 좌우 패널 폭 432, 높이 396, 좌 패널 x=32, 우 패널 x=496. 복귀선은 왼쪽 여백, jump 선은 오른쪽으로 보내 서로 건너지 않게 한다. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 02-02 §3",
      "비인라인은 본문 한 벌에 jump 하고 인라인은 지점마다 복사",
      "호출 지점이 둘일 때 일반 함수 호출은 두 지점 모두 jump 로 같은 본문 한 벌에 갔다 각자 다음 줄로 돌아오고, __always_inline 은 지점마다 본문 명령어가 복사되어 jump 가 없다.",
      "같은 호출 지점 둘 · 일반 함수 호출과 인라인의 명령어 배치")

# 좌우 존
Z1 = (32, 100, 432, 396)   # 일반 함수 호출
Z2 = (496, 100, 432, 396)  # 인라인
for (x, y, w, h) in (Z1, Z2):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
d.t(Z1[0] + 16, Z1[1] + 24, "일반 함수 호출 (비인라인)", 13, INK, KR, "start", 600)
d.t(Z1[0] + 16, Z1[1] + 42, "호출 지점은 jump · 본문은 한 벌", 12, MUTED, KR, "start")
d.t(Z2[0] + 16, Z2[1] + 24, "인라인", 13, INK, KR, "start", 600)
d.t(Z2[0] + 68, Z2[1] + 24, "__always_inline", 13, INK, MONO, "start", 600)
d.t(Z2[0] + 16, Z2[1] + 42, "호출 지점마다 본문 사본 · jump 없음", 12, MUTED, KR, "start")

# === 좌측 패널: 일반 함수 호출 ===
CX, CY, CW, CH = 76, 156, 216, 192          # 호출한 쪽
d.tone(CX, CY, CW, CH, INFO, 6, "08", 1.0)
d.t(CX + 12, CY + 20, "호출한 쪽", 12, INFO, KR, "start", 600)
ROWS = [("호출 1", "my_function()", INFO), ("복귀 1", "다음 줄 계속", OK),
        ("호출 2", "my_function()", INFO), ("복귀 2", "다음 줄 계속", OK)]
rowy = []
for i, (k, v, c) in enumerate(ROWS):
    y = CY + 30 + i * 40
    rowy.append(y + 16)
    d.tone(CX + 12, y, CW - 24, 32, c, 4, "16", 1.0)
    d.t(CX + 20, y + 21, k, 12, INK, KR, "start", 600)
    d.t(CX + 72, y + 21, v, 12, INFO if c == INFO else MUTED, MONO if c == INFO else KR, "start")

FX, FY, FW, FH = 76, 372, 216, 104          # 불린 함수
d.tone(FX, FY, FW, FH, WARN, 6, "08", 1.0)
d.t(FX + 12, FY + 20, "my_function", 12, WARN, MONO, "start", 600)
d.tone(FX + 12, FY + 28, FW - 24, 32, WARN, 4, "16", 1.0)
d.t(FX + FW/2, FY + 49, "본문 한 벌", 12, WARN, KR, "middle", 600)
d.tone(FX + 12, FY + 66, FW - 24, 32, OK, 4, "16", 1.0)
d.t(FX + FW/2, FY + 87, "끝 · 부른 자리 다음으로", 12, OK, KR, "middle", 600)
body_y, back_y = FY + 44, FY + 82

# jump — 호출 1·2 가 오른쪽 줄기에서 만나 본문 한 벌로
JX = 340
d.arrow([(CX + CW + 2, rowy[0]), (JX, rowy[0]), (JX, body_y), (FX + FW + 8, body_y)], WARN, "warn", 1.5)
d.line(CX + CW + 2, rowy[2], JX, rowy[2], WARN, 1.5)
d.chip(JX, 356, "jump", WARN, 12)

# 복귀 — 본문 끝에서 왼쪽 줄기를 타고 각 호출의 다음 줄로
RX = 52
d.arrow([(FX - 2, back_y), (RX, back_y), (RX, rowy[1]), (CX - 8, rowy[1])], OK, "ok", 1.5)
d.arrow([(RX, rowy[3]), (CX - 8, rowy[3])], OK, "ok", 1.5)

# === 우측 패널: 인라인 ===
ICX, ICY, ICW, ICH = 516, 156, 392, 320
d.tone(ICX, ICY, ICW, ICH, INFO, 6, "08", 1.0)
d.t(ICX + 16, ICY + 22, "호출한 쪽 · 본문 명령어 복사", 12, INFO, KR, "start", 600)
for n, by in ((1, ICY + 40), (2, ICY + 180)):
    d.tone(ICX + 16, by, ICW - 32, 120, WARN, 4, "16", 1.0)
    d.t(ICX + 28, by + 28, f"호출 {n} 자리", 13, INK, KR, "start", 600)
    d.t(ICX + 28, by + 60, f"my_function 본문 사본 {n}", 13, WARN, KR, "start", 600)
    d.t(ICX + 28, by + 92, "jump 없음", 12, MUTED, KR, "start")
    d.chip(ICX + ICW - 84, by + 28, f"사본 {n}", ACC, 11)

d.legend(H - 44, [("호출한 쪽", INFO), ("함수 본문", WARN), ("복귀", OK), ("인라인 사본", ACC)])
d.save("02-02.call-inline.svg")
