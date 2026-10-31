# 12-01 §3 — 로그 기반 메시지 브로커의 토픽 파티션, 단조 증가 오프셋, 컨슈머 그룹 순차 읽기 데이터플로우.
# 사실 출처: 12-01 §3(L60~L66), 원서 Ch.12 Figure 12-3(PDF p.12 "Producers send messages by appending them to a topic partition file, and consumers read these files sequentially")
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 516
H = LEG + 56

d = D(W, H, "12-01 · §3 LOG-BASED MESSAGE BROKER", "토픽 파티션과 오프셋 기반 순차 읽기 구조",
      "프로듀서가 토픽의 각 파티션 끝에 메시지를 추가(append)하고, 컨슈머 그룹의 클라이언트가 파티션별 오프셋을 순차적으로 읽는 아키텍처.",
      "토픽 샤딩(파티션) · 단조 증가 오프셋 · 프로듀서 추가(append) · 컨슈머 그룹 파티션 할당과 오프셋 진도")

# 1. 왼쪽: 프로듀서 클라이언트 박스
d.t(88, 106, "프로듀서 (발행)", 12, INK, KR, "middle", 600)
# 프로듀서 1
d.box(24, 120, 128, 52, PAPER2, RULE, 1.0)
d.t(88, 142, "프로듀서 클라이언트", 12, INK, KR, "middle", 600)
d.t(88, 158, "Producer Client 1", 11, MUTED, MONO, "middle")

# 프로듀서 2
d.box(24, 276, 128, 52, PAPER2, RULE, 1.0)
d.t(88, 298, "프로듀서 클라이언트", 12, INK, KR, "middle", 600)
d.t(88, 314, "Producer Client 2", 11, MUTED, MONO, "middle")

# 2. 중앙: 토픽과 파티션 로그 구조
d.t(436, 106, "브로커 저장소: 토픽별 append-only 파티션 로그", 12, INK, KR, "middle", 600)

# 토픽 A 영역 (파티션 0, 파티션 1)
d.box(180, 120, 480, 120, PAPER2, RULE, 0.8)
d.t(196, 144, "토픽 A", 12, INFO, KR, "start", 600)

# 토픽 A 파티션 0: 오프셋 1..10 + [11 추가]
d.t(210, 172, "파티션 0", 12, MUTED, KR, "start")
OX0 = 268
CW = 28
CH = 26
STRIDE = 32
for o in range(1, 11):
    x = OX0 + (o - 1) * STRIDE
    d.box(x, 158, CW, CH, PAPER, RULE, 0.8, r=3)
    d.t(x + CW / 2, 175, str(o), 11, INK, MONO, "middle")
# 추가 예정 셀 11
x_app1 = OX0 + 10 * STRIDE
d.box(x_app1, 158, CW, CH, PAPER, OK, 1.0, r=3)
d.t(x_app1 + CW / 2, 175, "11", 11, OK, MONO, "middle")
d.t(x_app1 + CW / 2, 196, "추가 (append)", 11, OK, KR, "middle")

# 토픽 A 파티션 1: 오프셋 1..8
d.t(210, 222, "파티션 1", 12, MUTED, KR, "start")
for o in range(1, 9):
    x = OX0 + (o - 1) * STRIDE
    d.box(x, 208, CW, CH, PAPER, RULE, 0.8, r=3)
    d.t(x + CW / 2, 225, str(o), 11, INK, MONO, "middle")

# 프로듀서 1 -> 토픽 A 파티션 0 추가 직각 화살표 (토픽 상단 외곽 통과)
d.arrow([(152, 136), (170, 136), (170, 114), (x_app1 + CW / 2, 114), (x_app1 + CW / 2, 154)], OK, m="ok")

# 토픽 B 영역 (파티션 0, 파티션 1, 파티션 2)
d.box(180, 252, 480, 232, PAPER2, RULE, 0.8)
d.t(196, 276, "토픽 B", 12, INFO, KR, "start", 600)

# 토픽 B 파티션 0: 오프셋 1..4 (컨슈머가 4까지 읽음)
d.t(210, 304, "파티션 0", 12, MUTED, KR, "start")
for o in range(1, 5):
    x = OX0 + (o - 1) * STRIDE
    c = ACC if o == 4 else INFO
    d.tone(x, 290, CW, CH, c, 3, "22" if o == 4 else "10", 1.2 if o == 4 else 0.8)
    d.t(x + CW / 2, 307, str(o), 11, c, MONO, "middle")

# 토픽 B 파티션 1: 오프셋 1..7 + [8 추가] (컨슈머가 5까지 읽음)
d.t(210, 356, "파티션 1", 12, MUTED, KR, "start")
for o in range(1, 8):
    x = OX0 + (o - 1) * STRIDE
    is_focal = (o == 5)
    c = ACC if is_focal else (INFO if o < 5 else MUTED)
    fill = PAPER if o > 5 else (ACC + "22" if is_focal else INFO + "10")
    stroke = ACC if is_focal else (INFO if o < 5 else RULE)
    d.box(x, 342, CW, CH, fill, stroke, 1.2 if is_focal else 0.8, r=3)
    d.t(x + CW / 2, 359, str(o), 11, c, MONO, "middle")
# 추가 예정 셀 8
x_app2 = OX0 + 7 * STRIDE
d.box(x_app2, 342, CW, CH, PAPER, OK, 1.0, r=3)
d.t(x_app2 + CW / 2, 359, "8", 11, OK, MONO, "middle")
d.t(x_app2 + CW / 2, 380, "추가 (append)", 11, OK, KR, "middle")

# 프로듀서 2 -> 토픽 B 파티션 1 추가 직각 화살표 (토픽 B 박스 상단 통로 y=246 통과)
d.arrow([(152, 292), (170, 292), (170, 246), (x_app2 + CW / 2, 246), (x_app2 + CW / 2, 338)], OK, m="ok")

# 토픽 B 파티션 2: 오프셋 1..12 (컨슈머가 9까지 읽음)
d.t(210, 420, "파티션 2", 12, MUTED, KR, "start")
for o in range(1, 13):
    x = OX0 + (o - 1) * STRIDE
    is_focal = (o == 9)
    c = ACC if is_focal else (INFO if o < 9 else MUTED)
    fill = PAPER if o > 9 else (ACC + "22" if is_focal else INFO + "10")
    stroke = ACC if is_focal else (INFO if o < 9 else RULE)
    d.box(x, 406, CW, CH, fill, stroke, 1.2 if is_focal else 0.8, r=3)
    d.t(x + CW / 2, 423, str(o), 11, c, MONO, "middle")

# 3. 오른쪽: 컨슈머 그룹 박스
CG_X = 684
CG_W = 172
d.t(CG_X + CG_W / 2, 238, "컨슈머 그룹 (구독)", 12, INK, KR, "middle", 600)
d.box(CG_X, 252, CG_W, 232, PAPER2, RULE, 1.0, r=6)

# 컨슈머 1 (B.0과 B.1 담당)
d.box(CG_X + 12, 268, CG_W - 24, 88, PAPER, RULE, 0.8, r=4)
d.t(CG_X + CG_W / 2, 288, "컨슈머 클라이언트 1", 12, INK, KR, "middle", 600)
d.t(CG_X + CG_W / 2, 308, "파티션 B.0 오프셋 = 4", 12, ACC, KR, "middle", 600)
d.t(CG_X + CG_W / 2, 328, "파티션 B.1 오프셋 = 5", 12, ACC, KR, "middle", 600)
d.t(CG_X + CG_W / 2, 344, "순차 읽기 (read)", 11, MUTED, KR, "middle")

# 컨슈머 2 (B.2 담당)
d.box(CG_X + 12, 376, CG_W - 24, 88, PAPER, RULE, 0.8, r=4)
d.t(CG_X + CG_W / 2, 398, "컨슈머 클라이언트 2", 12, INK, KR, "middle", 600)
d.t(CG_X + CG_W / 2, 420, "파티션 B.2 오프셋 = 9", 12, ACC, KR, "middle", 600)
d.t(CG_X + CG_W / 2, 442, "단일 컨슈머 독점 할당", 11, MUTED, KR, "middle")

# 파티션 읽기 직각 화살표들 — 각 파티션 행 사이 빈 틈을 통해 우회
# B.0 오프셋 4 (하단 y=316 -> y=324 통로 -> 컨슈머 1)
x_b0 = OX0 + 3 * STRIDE + CW / 2
d.arrow([(x_b0, 316), (x_b0, 324), (CG_X + 12, 324)], ACC, m="acc")

# B.1 오프셋 5 (하단 y=368 -> y=396 통로 -> 컨슈머 1 입구 y=340)
x_b1 = OX0 + 4 * STRIDE + CW / 2
d.arrow([(x_b1, 368), (x_b1, 396), (672, 396), (672, 340), (CG_X + 12, 340)], ACC, m="acc")

# B.2 오프셋 9 (하단 y=432 -> y=456 통로 -> 컨슈머 2 입구 y=420)
x_b2 = OX0 + 8 * STRIDE + CW / 2
d.arrow([(x_b2, 432), (x_b2, 456), (672, 456), (672, 420), (CG_X + 12, 420)], ACC, m="acc")

# 범례
d.legend(LEG, [
    ("프로듀서 추가 (append)", OK),
    ("처리 완료 오프셋", INFO),
    ("소비자 오프셋 (focal)", ACC),
    ("미처리 오프셋", MUTED)
])

d.save("12-01.log-partition-offset.svg")
