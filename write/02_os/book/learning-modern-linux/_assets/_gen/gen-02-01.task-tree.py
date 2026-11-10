# 02-01 §3 — 세션에서 태스크까지, 이름 다섯이 한 구조체로 모인다.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 계층과 task_struct 자원 공유 구조.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, OK, WARN, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §3",
      "세션에서 태스크까지 — 계층 사다리와 자원 공유",
      "위는 세션·그룹·프로세스·스레드의 식별 계층이고, 아래는 task_struct 가 자원을 공유하거나 복사하는 구조다.",
      "식별 계층 사다리(위)와 커널 task_struct 의 공유 vs 복사 구조(아래)")

# 1. 상단: 식별 계층 사다리 (SID -> PGID -> PID -> TID)
ladder = [
    ("세션", "SID 6756", "제어 터미널(tty) 연결"),
    ("프로세스 그룹", "PGID 6756", "시그널(SIGINT) 전달"),
    ("프로세스 (TGID)", "PID 6756", "자원 격리 및 통계"),
    ("스레드", "TID 6756", "스케줄링 실행 단위"),
]

LX = 30
LW = 185
LH = 62
LGAP = 23
LY = 98

for i, (name, id_code, desc) in enumerate(ladder):
    x = LX + i * (LW + LGAP)
    d.box(x, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + LW / 2, LY + 20, name, 13, INK, KR, "middle", 600)
    d.t(x + LW / 2, LY + 38, id_code, 11, INFO, MONO, "middle", 600)
    d.t(x + LW / 2, LY + 52, desc, 11, MUTED, KR, "middle")
    if i < len(ladder) - 1:
        ax = x + LW
        d.arrow([(ax + 3, LY + LH / 2), (ax + LGAP - 4, LY + LH / 2)], MUTED, "ar", 1.2)

# 구분 라벨
d.line(30, 180, W - 30, 180, RULE, 0.8)
d.t(30, 198, "커널 안 task_struct — 스레드는 공유, fork 는 복사", 12, INK, KR, "start", 600)

# 2. 하단 좌측: 멀티스레드 프로세스 (자원 공유)
PX1, PY1, PW1, PH1 = 30, 212, 510, 268
d.box(PX1, PY1, PW1, PH1, PAPER2, RULE, 1.0, 8)
d.t(PX1 + 16, PY1 + 24, "멀티스레드 프로세스 (PID 7100)", 13, INK, KR, "start", 600)
d.chip(PX1 + 420, PY1 + 22, "스레드 간 한 벌 공유", OK, 11)

# 태스크 1
T1_X, T1_Y, TW, TH = PX1 + 20, PY1 + 46, 175, 94
d.box(T1_X, T1_Y, TW, TH, PAPER, ACC, 1.2, 6)
d.t(T1_X + TW / 2, T1_Y + 22, "task_struct [메인]", 12, ACC, KR, "middle", 600)
d.t(T1_X + TW / 2, T1_Y + 42, "TID: 7100 (pid)", 11, INK, MONO, "middle")
d.t(T1_X + TW / 2, T1_Y + 60, "TGID: 7100 (tgid)", 11, MUTED, MONO, "middle")
d.t(T1_X + TW / 2, T1_Y + 78, "개별 레지스터 · 스택", 11, MUTED, KR, "middle")

# 태스크 2
T2_X, T2_Y = T1_X, T1_Y + 110
d.box(T2_X, T2_Y, TW, TH, PAPER, ACC, 1.2, 6)
d.t(T2_X + TW / 2, T2_Y + 22, "task_struct [스레드]", 12, ACC, KR, "middle", 600)
d.t(T2_X + TW / 2, T2_Y + 42, "TID: 7101 (pid)", 11, INK, MONO, "middle")
d.t(T2_X + TW / 2, T2_Y + 60, "TGID: 7100 (tgid)", 11, MUTED, MONO, "middle")
d.t(T2_X + TW / 2, T2_Y + 78, "개별 레지스터 · 스택", 11, MUTED, KR, "middle")

# 공유 자원 블록
RES_X, RES_Y, RW, RH = PX1 + 270, PY1 + 54, 220, 192
d.tone(RES_X, RES_Y, RW, RH, OK, 6, "10", 1.2)
d.t(RES_X + RW / 2, RES_Y + 24, "공유 커널 자원 (한 벌)", 13, OK, KR, "middle", 600)

resources = [
    ("mm_struct (mm)", "가상 메모리 주소 공간", OK),
    ("files_struct (files)", "열린 파일 fd 테이블", OK),
    ("sighand_struct", "시그널 핸들러 테이블", OK),
]
for k, (rtitle, rdesc, rc) in enumerate(resources):
    ry = RES_Y + 42 + k * 46
    d.box(RES_X + 12, ry, RW - 24, 40, PAPER, RULE, 0.8, 4)
    d.t(RES_X + 20, ry + 16, rtitle, 11, rc, MONO, "start", 600)
    d.t(RES_X + 20, ry + 31, rdesc, 11, MUTED, KR, "start")

# 직교 화살표 연결 (스레드 -> 공유 자원)
mid_x = (T1_X + TW + RES_X) / 2
d.arrow([(T1_X + TW, T1_Y + TH / 2), (mid_x, T1_Y + TH / 2), (mid_x, RES_Y + 54), (RES_X - 4, RES_Y + 54)], OK, "ok", 1.2)
d.arrow([(T2_X + TW, T2_Y + TH / 2), (mid_x, T2_Y + TH / 2), (mid_x, RES_Y + 146), (RES_X - 4, RES_Y + 146)], OK, "ok", 1.2)

# 3. 하단 우측: fork 자식 프로세스 (자원 분리)
PX2, PY2, PW2, PH2 = 560, 212, 290, 268
d.box(PX2, PY2, PW2, PH2, PAPER2, RULE, 1.0, 8)
d.t(PX2 + 16, PY2 + 24, "자식 프로세스 (fork)", 13, INK, KR, "start", 600)
d.chip(PX2 + 220, PY2 + 22, "자원 복사", WARN, 11)

# 자식 태스크
T3_X, T3_Y, T3W, T3H = PX2 + 16, PY2 + 54, 120, 192
d.box(T3_X, T3_Y, T3W, T3H, PAPER, ACC, 1.2, 6)
d.t(T3_X + T3W / 2, T3_Y + 26, "task_struct", 12, ACC, KR, "middle", 600)
d.t(T3_X + T3W / 2, T3_Y + 52, "PID: 7105", 11, INK, MONO, "middle", 600)
d.t(T3_X + T3W / 2, T3_Y + 74, "TID: 7105", 11, MUTED, MONO, "middle")
d.t(T3_X + T3W / 2, T3_Y + 96, "PGID: 7100", 11, INFO, MONO, "middle")
d.t(T3_X + T3W / 2, T3_Y + 130, "부모와 같은 그룹,", 11, MUTED, KR, "middle")
d.t(T3_X + T3W / 2, T3_Y + 150, "새 task_struct", 11, MUTED, KR, "middle")

# 자식 복사 자원 블록
RES2_X, RES2_Y, R2W, R2H = PX2 + 150, PY2 + 54, 124, 192
d.tone(RES2_X, RES2_Y, R2W, R2H, WARN, 6, "10", 1.2)
d.t(RES2_X + R2W / 2, RES2_Y + 24, "독립 복사본", 12, WARN, KR, "middle", 600)

c_resources = [
    ("mm (COW)", "쓰기 시 복사"),
    ("files", "fd 복제본"),
    ("sighand", "핸들러 복사"),
]
for k, (ctitle, cdesc) in enumerate(c_resources):
    cry = RES2_Y + 42 + k * 46
    d.box(RES2_X + 8, cry, R2W - 16, 40, PAPER, RULE, 0.8, 4)
    d.t(RES2_X + R2W / 2, cry + 16, ctitle, 11, WARN, MONO, "middle", 600)
    d.t(RES2_X + R2W / 2, cry + 31, cdesc, 11, MUTED, KR, "middle")

d.arrow([(T3_X + T3W, T3_Y + T3H / 2), (RES2_X - 4, RES2_Y + R2H / 2)], WARN, "warn", 1.2)

# 범례 (y=496, H=560 -> margin = 560 - 518 = 42px > 24px)
d.legend(496, [
    ("식별 번호", INFO),
    ("task_struct", ACC),
    ("공유 자원 (스레드)", OK),
    ("복사 자원 (fork · COW)", WARN),
])

d.save("02-01.task-tree.svg")
print("ok 02-01.task-tree")
