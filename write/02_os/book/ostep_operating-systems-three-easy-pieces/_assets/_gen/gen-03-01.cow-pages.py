# 03-01 「Linux 에서 fork 의 비용」 — fork 직후 부모와 자식이 같은 물리 페이지를 읽기 전용으로 함께 쓰다가 부모가 쓰는 순간 그 페이지만 복사되어 자식의 값은 그대로 남는 세 시점.
# 본문 근거: 이 노트 「1. fork 로 프로세스 복제하기」 — Linux 에서 fork 의 비용.
# 값 근거: x = 100, 200 은 설명용으로 고른 값이다.
# 공식 근거: fork(2) 의 copy-on-write 문장, OSTEP 23장의 copy-on-write 설명(읽기 전용 표시, 쓰면 trap, 새 페이지를 잡아 쓴 프로세스에 매핑).
# 타입 스펙: type-process — 부모·자식의 페이지 테이블과 물리 메모리가 세 시점에서 바뀌는 과정.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 920, 632
d = D(W, H, "OSTEP · 03-01 §1",
      "쓰는 순간 그 페이지만 복사되어 자식의 값은 그대로다",
      "fork 직후 부모와 자식이 같은 물리 페이지를 읽기 전용으로 함께 쓰다가 "
      "부모가 쓰는 순간 그 페이지만 복사되어 자식의 값은 그대로 남는 세 시점",
      lead="같은 부모, 자식, 물리 메모리를 세 시점에서 본 모습입니다.")

X0, PW, PG = 20, 268, 24
Y_T, PH = 100, 440

# 부모/자식/물리 메모리 Y 좌표 (모두 4의 배수)
Y_P_BOX, H_PT = 160, 72
Y_P_ENT, H_ENT = 188, 34
Y_MEM_BOX, H_MEM = 290, 146
Y_TOP_PG, H_PG_SPLIT = 314, 42
Y_BOT_PG = 382
Y_FULL_PG, H_FULL_PG = 314, 112
Y_C_BOX = 460
Y_C_ENT = 468

stages = [
    ("1. fork 직후", "같은 물리 페이지 공유", "shared"),
    ("2. 부모가 x 에 200 을 쓰려 함", "읽기 전용 쓰기 → trap · 복사", "cow"),
    ("3. 그 뒤", "부모는 새 페이지 · 자식은 원래 페이지", "after"),
]

for i, (ttl, sub, mode) in enumerate(stages):
    x = X0 + i * (PW + PG)
    cx = x + PW // 2          # 134
    lx = x + 16               # 왼쪽 칸 시작 (w=112)
    rx = x + 140              # 오른쪽 칸 시작 (w=112)
    lcx = lx + 56             # 왼쪽 칸 중심 (+72)
    rcx = rx + 56             # 오른쪽 칸 중심 (+196)
    bw = 112

    # 시점 패널 틀 + 제목
    d.box(x, Y_T, PW, PH, PAPER2, RULE, 1.0)
    d.t(cx, Y_T + 26, ttl, 13, INK, KR, "middle", 600)
    d.t(cx, Y_T + 46, sub, 12, MUTED, KR)

    if i < 2:
        d.arrow([(x + PW + 2, Y_T + 20), (x + PW + PG - 2, Y_T + 20)], SOFT, "soft", 1.3)

    # 1) 부모 페이지 테이블
    d.box(x + 8, Y_P_BOX, PW - 16, H_PT, PAPER, RULE, 0.9)
    d.t(cx, Y_P_BOX + 18, "부모 페이지 테이블", 12, MUTED, KR, "middle", 600)

    if mode in ("shared", "cow"):
        d.tone(lx, Y_P_ENT, bw, H_ENT, WARN, 6, "14", 1.2)
        d.t(lcx, Y_P_ENT + 21, "x · 읽기 전용", 12, WARN, KR, "middle", 600)
    else:
        d.tone(lx, Y_P_ENT, bw, H_ENT, ACC, 6, "14", 1.4)
        d.t(lcx, Y_P_ENT + 21, "x", 13, ACC, MONO, "middle", 600)

    d.box(rx, Y_P_ENT, bw, H_ENT, PAPER2, RULE, 0.9)
    d.t(rcx, Y_P_ENT + 21, "다른 페이지", 12, MUTED, KR)

    # 2) 물리 메모리 구획
    d.o.append(f'<rect x="{x + 8}" y="{Y_MEM_BOX}" width="{PW - 16}" height="{H_MEM}" rx="6" fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 3"/>')
    d.t(cx, Y_MEM_BOX + 15, "물리 메모리", 12, SOFT, KR, "middle", 600)

    if mode == "shared":
        d.box(lx, Y_FULL_PG, bw, H_FULL_PG, PAPER2, RULE, 1.0)
        d.t(lcx, Y_FULL_PG + 48, "물리 페이지", 12, MUTED, KR)
        d.t(lcx, Y_FULL_PG + 70, "x = 100", 14, INK, MONO, "middle", 600)
    elif mode == "cow":
        d.tone(lx, Y_TOP_PG, bw, H_PG_SPLIT, ACC, 6, "14", 1.4)
        d.t(lcx, Y_TOP_PG + 17, "새 물리 페이지", 12, ACC, KR, "middle", 600)
        d.t(lcx, Y_TOP_PG + 34, "그 페이지만 복사", 12, MUTED, KR)

        d.tone(lx, Y_BOT_PG, bw, H_PG_SPLIT, OK, 6, "14", 1.0)
        d.t(lcx, Y_BOT_PG + 17, "원래 페이지", 12, MUTED, KR)
        d.t(lcx, Y_BOT_PG + 34, "x = 100", 13, OK, MONO, "middle", 600)

        # 원래 페이지 -> 새 물리 페이지 복사 화살표
        d.arrow([(lcx, Y_BOT_PG - 2), (lcx, Y_TOP_PG + H_PG_SPLIT + 2)], ACC, "acc", 1.4)
        d.t(lcx + 8, Y_TOP_PG + H_PG_SPLIT + 17, "복사", 12, ACC, KR, "start", 600)
    else:
        d.tone(lx, Y_TOP_PG, bw, H_PG_SPLIT, ACC, 6, "14", 1.4)
        d.t(lcx, Y_TOP_PG + 17, "새 페이지", 12, ACC, KR, "middle", 600)
        d.t(lcx, Y_TOP_PG + 34, "x = 200", 13, ACC, MONO, "middle", 600)

        d.tone(lx, Y_BOT_PG, bw, H_PG_SPLIT, OK, 6, "14", 1.2)
        d.t(lcx, Y_BOT_PG + 17, "원래 페이지", 12, MUTED, KR)
        d.t(lcx, Y_BOT_PG + 34, "x = 100", 13, OK, MONO, "middle", 600)

    # 쓰지 않은 페이지 (세 시점 내내 공통)
    d.box(rx, Y_FULL_PG, bw, H_FULL_PG, PAPER2, RULE, 1.0)
    d.t(rcx, Y_FULL_PG + 50, "쓰지 않은", 12, MUTED, KR)
    d.t(rcx, Y_FULL_PG + 68, "페이지", 12, MUTED, KR)

    # 부모 -> 물리 메모리 / 커널(trap) 연결
    if mode == "shared":
        d.arrow([(lcx, Y_P_BOX + H_PT + 2), (lcx, Y_FULL_PG - 2)], MUTED, "ar", 1.3)
    elif mode == "cow":
        d.arrow([(lcx, Y_P_BOX + H_PT + 2), (lcx, 254)], WARN, "warn", 1.3)
        d.t(lcx + 8, 248, "200 쓰기", 12, WARN, KR, "start", 600)
        d.tone(lx, 256, bw, 28, INFO, 6, "14", 1.2)
        d.t(lcx, 274, "커널 (trap)", 12, INFO, KR, "middle", 600)
        d.arrow([(lcx, 286), (lcx, Y_TOP_PG - 2)], ACC, "acc", 1.3)
    else:
        d.arrow([(lcx, Y_P_BOX + H_PT + 2), (lcx, Y_TOP_PG - 2)], ACC, "acc", 1.4)

    d.arrow([(rcx, Y_P_BOX + H_PT + 2), (rcx, Y_FULL_PG - 2)], MUTED, "ar", 1.3)

    # 3) 자식 페이지 테이블
    d.box(x + 8, Y_C_BOX, PW - 16, H_PT, PAPER, RULE, 0.9)
    if mode in ("shared", "cow"):
        d.tone(lx, Y_C_ENT, bw, H_ENT, WARN, 6, "14", 1.2)
        d.t(lcx, Y_C_ENT + 21, "x · 읽기 전용", 12, WARN, KR, "middle", 600)
    else:
        d.tone(lx, Y_C_ENT, bw, H_ENT, OK, 6, "14", 1.2)
        d.t(lcx, Y_C_ENT + 21, "x", 13, OK, MONO, "middle", 600)

    d.box(rx, Y_C_ENT, bw, H_ENT, PAPER2, RULE, 0.9)
    d.t(rcx, Y_C_ENT + 21, "다른 페이지", 12, MUTED, KR)
    d.t(cx, Y_C_BOX + 58, "자식 페이지 테이블", 12, MUTED, KR, "middle", 600)

    # 자식 -> 물리 메모리 연결
    if mode == "shared":
        d.arrow([(lcx, Y_C_BOX - 2), (lcx, Y_FULL_PG + H_FULL_PG + 2)], MUTED, "ar", 1.3)
    elif mode == "cow":
        d.arrow([(lcx, Y_C_BOX - 2), (lcx, Y_BOT_PG + H_PG_SPLIT + 2)], MUTED, "ar", 1.3)
    else:
        d.arrow([(lcx, Y_C_BOX - 2), (lcx, Y_BOT_PG + H_PG_SPLIT + 2)], OK, "ok", 1.4)

    d.arrow([(rcx, Y_C_BOX - 2), (rcx, Y_FULL_PG + H_FULL_PG + 2)], MUTED, "ar", 1.3)

d.t(X0, Y_T + PH + 24, "자식이 먼저 써도 같음 — 쓴 쪽이 사본을 받음", 12, MUTED, KR, "start")
d.legend(H - 40, [("읽기 전용", WARN), ("커널 (trap)", INFO), ("새로 복사된 페이지", ACC), ("원래 값 유지", OK)])
d.save("03-01.cow-pages.svg")
print("ok 03-01 cow-pages")
