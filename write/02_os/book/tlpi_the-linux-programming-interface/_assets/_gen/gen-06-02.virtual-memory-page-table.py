# 06-02 §2 가상 메모리와 페이지 테이블 — 가상 페이지의 물리 메모리 매핑과 격리·공유
# 근거: TLPI 6.4 Figure 6-2, 06.txt 374-406, 440-475
# 타입 스펙: type-architecture — 두 프로세스의 가상 주소 공간이 각자의 페이지 테이블을 거쳐 물리 메모리 프레임에 대응하는 구조
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "TLPI · 06-02 §2",
      "가상 메모리와 페이지 테이블 매핑",
      "프로세스별 페이지 테이블을 통한 주소 변환: 물리 프레임 격리, 코드 공유, 미적재 페이지 폴트",
      "두 프로세스가 동일한 가상 주소(page 0, page 1)를 사용하더라도 페이지 테이블에 의해 물리 프레임이 안전하게 분리·공유되는 원리")

X_VA = 36
W_VA = 170

X_PT = 310
W_PT = 190

X_RAM = 640
W_RAM = 280

# -----------------
# 1. Process A 가상 메모리 (상단)
# -----------------
d.box(X_VA, 110, W_VA, 180, PAPER2, RULE, 1.0, 6)
d.t(X_VA + W_VA/2, 132, "프로세스 A 가상 공간", 12, INK, KR, "middle", 600)
va_a = [
    (148, "page 0 (코드)", INFO),
    (180, "page 1 (데이터)", OK),
    (212, "page 2 (스택)", WARN),
    (244, "page 3 (미적재)", SOFT),
]
for y, txt, c in va_a:
    d.box(X_VA + 12, y, W_VA - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(X_VA + W_VA/2, y + 17, txt, 11, c, MONO if "page" in txt else KR)

# -----------------
# 2. Process B 가상 메모리 (하단)
# -----------------
d.box(X_VA, 310, W_VA, 150, PAPER2, RULE, 1.0, 6)
d.t(X_VA + W_VA/2, 332, "프로세스 B 가상 공간", 12, INK, KR, "middle", 600)
va_b = [
    (348, "page 0 (코드)", INFO),
    (380, "page 1 (데이터)", BAD),
    (412, "page 2 (스택)", MUTED),
]
for y, txt, c in va_b:
    d.box(X_VA + 12, y, W_VA - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(X_VA + W_VA/2, y + 17, txt, 11, c, MONO if "page" in txt else KR)

# -----------------
# 3. 페이지 테이블 A (상단)
# -----------------
d.box(X_PT, 110, W_PT, 180, PAPER2, RULE, 1.0, 6)
d.t(X_PT + W_PT/2, 132, "프로세스 A 페이지 테이블", 12, INK, KR, "middle", 600)
pt_a = [
    (148, "page 0 → frame 2", ACC),
    (180, "page 1 → frame 4", OK),
    (212, "page 2 → frame 7", WARN),
    (244, "page 3 → 스왑 영역", SOFT),
]
for y, txt, c in pt_a:
    d.box(X_PT + 12, y, W_PT - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(X_PT + W_PT/2, y + 17, txt, 11, c, MONO)

# -----------------
# 4. 페이지 테이블 B (하단)
# -----------------
d.box(X_PT, 310, W_PT, 150, PAPER2, RULE, 1.0, 6)
d.t(X_PT + W_PT/2, 332, "프로세스 B 페이지 테이블", 12, INK, KR, "middle", 600)
pt_b = [
    (348, "page 0 → frame 2", ACC),
    (380, "page 1 → frame 5", BAD),
    (412, "page 2 → frame 1", MUTED),
]
for y, txt, c in pt_b:
    d.box(X_PT + 12, y, W_PT - 24, 26, PAPER, RULE, 0.8, 4)
    d.t(X_PT + W_PT/2, y + 17, txt, 11, c, MONO)

# -----------------
# 5. 물리 메모리 RAM (프레임 0~7)
# -----------------
d.box(X_RAM, 110, W_RAM, 320, PAPER2, RULE, 1.0, 6)
d.t(X_RAM + W_RAM/2, 132, "물리 메모리 RAM (페이지 프레임)", 12, INK, KR, "middle", 600)
frames = [
    (150, "frame 0 : 미사용 여유 프레임", PAPER, RULE, SOFT),
    (182, "frame 1 : 프로세스 B 스택", PAPER, RULE, MUTED),
    (214, "frame 2 : 공유 코드 세그먼트", ACC, ACC, INK),  # FOCAL
    (246, "frame 3 : 미사용 여유 프레임", PAPER, RULE, SOFT),
    (278, "frame 4 : 프로세스 A 데이터", PAPER, OK, OK),
    (310, "frame 5 : 프로세스 B 데이터", PAPER, BAD, BAD),
    (342, "frame 6 : 커널 예약 프레임", PAPER, RULE, SOFT),
    (374, "frame 7 : 프로세스 A 스택", PAPER, WARN, WARN),
]
for y, txt, fill, stroke, tc in frames:
    if fill == ACC:
        d.tone(X_RAM + 14, y, W_RAM - 28, 26, ACC, 4, "1F", 1.5)
        d.t(X_RAM + W_RAM/2, y + 17, txt, 11, tc, KR, "middle", 600)
    else:
        d.box(X_RAM + 14, y, W_RAM - 28, 26, fill, stroke, 0.9, 4)
        d.t(X_RAM + W_RAM/2, y + 17, txt, 11, tc, KR)

# 6. 디스크 스왑 영역 (상단 우측 하단)
d.box(X_RAM, 446, W_RAM, 48, PAPER, SOFT, 1.0, 6)
d.t(X_RAM + 18, 474, "디스크 스왑 영역", 12, SOFT, KR, "start", 600)
d.t(X_RAM + 140, 474, "미적재 페이지 폴트 대상", 11, SOFT, KR, "start")

# -----------------
# 직교 연결 화살표
# -----------------
# VA -> PT (수평 연결)
for y in (161, 193, 225, 257):
    d.arrow([(X_VA + W_VA, y), (X_PT, y)], MUTED, "ar", 1.2)
for y in (361, 393, 425):
    d.arrow([(X_VA + W_VA, y), (X_PT, y)], MUTED, "ar", 1.2)

# PT A -> RAM / Swap
# pt_a 0 (161) -> frame 2 (227)
d.arrow([(X_PT + W_PT, 161), (560, 161), (560, 227), (X_RAM, 227)], ACC, "acc", 1.6)

# pt_a 1 (193) -> frame 4 (291)
d.arrow([(X_PT + W_PT, 193), (545, 193), (545, 291), (X_RAM, 291)], OK, "ok", 1.4)

# pt_a 2 (225) -> frame 7 (387)
d.arrow([(X_PT + W_PT, 225), (530, 225), (530, 387), (X_RAM, 387)], WARN, "warn", 1.4)

# pt_a 3 (257) -> swap (470)
d.arrow([(X_PT + W_PT, 257), (515, 257), (515, 470), (X_RAM, 470)], SOFT, "soft", 1.4, dash="3 3")

# PT B -> RAM
# pt_b 0 (361) -> frame 2 (227)
d.arrow([(X_PT + W_PT, 361), (575, 361), (575, 227), (X_RAM, 227)], ACC, "acc", 1.6)

# pt_b 1 (393) -> frame 5 (323)
d.arrow([(X_PT + W_PT, 393), (590, 393), (590, 323), (X_RAM, 323)], BAD, "bad", 1.4)

# pt_b 2 (425) -> frame 1 (195)
d.arrow([(X_PT + W_PT, 425), (605, 425), (605, 195), (X_RAM, 195)], MUTED, "ar", 1.4)

# 범례 (너비 960에 맞춰 3항목 배치)
d.legend(524, [
    ("코드 공유 (Frame 2)", ACC),
    ("프로세스 전용 (Frame 1·4·5·7)", OK),
    ("스왑 영역 (페이지 폴트)", SOFT)
])

d.save("06-02.virtual-memory-page-table.svg")
print("ok 06-02.virtual-memory-page-table.svg")
