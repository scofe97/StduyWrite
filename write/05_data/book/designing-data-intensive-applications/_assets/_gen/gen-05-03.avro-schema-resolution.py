# 05-03 §2 — Avro의 태그 없는 32바이트 값 바이너리와 writer 스키마 및 reader 스키마 해소 과정.
# 사실 출처: 05-03 본문 §2(L73~L75), 원서 Figure 5-4(PDF p.13, 32바이트 · 1337 은 zigzag varint f2 14), Figure 5-6(PDF p.14, reader 는 userID·favoriteNumber·userName·interests).
# 가운데 바이트는 Figure 5-4 의 3필드 writer 레코드, 오른쪽은 Figure 5-6 의 reader. Figure 5-6 writer 의 photoURL 은 무시 규칙 칸에만 예로 든다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
H = 524
LEG = 468

d = D(W, H, "05-03 · AVRO SCHEMA RESOLUTION", "Avro writer 스키마와 reader 스키마 해소 과정",
      "태그와 타입 없이 순수 값만 32바이트로 직렬화하고, 디코딩 시 두 스키마의 필드명 매칭으로 차이를 번역한다.",
      "writer 스키마 직렬화 · 32바이트 값 스트림 · reader 스키마 필드명 매칭 및 기본값 보충")

X0 = 24
COL_W = 260
MID_W = 272
GAP = 16

LX = X0
CX = LX + COL_W + GAP
RX = CX + MID_W + GAP

# 좌측: writer 스키마
S_H = 216
d.box(LX, PY, COL_W, S_H, PAPER2, INFO, 1.2)
d.chip(LX + 34, PY + 20, "인코딩", INFO, 11)
d.t(LX + 68, PY + 24, "writer 스키마", 12.5, INK, MONO, "start", 600)
d.line(LX + 10, PY + 34, LX + COL_W - 10, PY + 34, RULE, 0.8)

w_fields = [
    ("userName: string", "필드 1 · 길이 접두사 문자열"),
    ("favoriteNumber: union", "필드 2 · long 또는 null"),
    ("interests: array<string>", "필드 3 · 문자열 배열")
]
for i, (fn, fdesc) in enumerate(w_fields):
    fy = PY + 46 + i * 52
    d.box(LX + 10, fy, COL_W - 20, 44, PAPER, RULE, 0.8)
    d.t(LX + 18, fy + 19, fn, 11.5, INK, MONO, "start", 600)
    d.t(LX + 18, fy + 35, fdesc, 11.5, SOFT, KR, "start")

# 중앙: 32바이트 바이너리 데이터
d.box(CX, PY, MID_W, S_H, PAPER2, ACC, 1.4)
d.chip(CX + 34, PY + 20, "32B", ACC, 11)
d.t(CX + 66, PY + 24, "순수 값 바이트 스트림", 12.5, INK, KR, "start", 600)
d.line(CX + 10, PY + 34, CX + MID_W - 10, PY + 34, RULE, 0.8)

bin_blocks = [
    ("0c 4d 61 72 74 69 6e", "길이 6 + 'Martin' (7B)"),
    ("02 f2 14", "union 분기 1 + 1337 (3B)"),
    ("04 16 .. 0e .. 00", "배열 크기 2 + 두 문자열 (22B)")
]
for i, (bhex, bdesc) in enumerate(bin_blocks):
    by = PY + 46 + i * 52
    d.box(CX + 10, by, MID_W - 20, 44, PAPER, RULE, 0.8)
    d.t(CX + MID_W / 2, by + 19, bhex, 11.5, ACC, MONO, "middle", 600)
    d.t(CX + MID_W / 2, by + 35, bdesc, 11.5, MUTED, KR, "middle")

# 우측: reader 스키마
d.box(RX, PY, COL_W, S_H, PAPER2, OK, 1.2)
d.chip(RX + 34, PY + 20, "디코딩", OK, 11)
d.t(RX + 68, PY + 24, "reader 스키마 (Fig 5-6)", 12.5, INK, MONO, "start", 600)
d.line(RX + 10, PY + 34, RX + COL_W - 10, PY + 34, RULE, 0.8)

r_fields = [
    ("userID: long", "writer 에 없음 · 기본값으로 채움", OK),
    ("favoriteNumber: union", "이름으로 매칭", ACC),
    ("userName: string", "이름으로 매칭 · 순서 바뀜", ACC),
    ("interests: array<string>", "이름으로 매칭", ACC)
]
for i, (fn, fdesc, col) in enumerate(r_fields):
    fy = PY + 42 + i * 42
    d.box(RX + 10, fy, COL_W - 20, 38, PAPER, RULE, 0.8)
    d.t(RX + 18, fy + 16, fn, 11.5, INK, MONO, "start", 600)
    d.t(RX + 18, fy + 31, fdesc, 11.5, col, KR, "start")

# 수평 화살표 연결 (인코딩 & 스키마 해소 번역)
d.arrow([(LX + COL_W + 2, PY + 108), (CX - 4, PY + 108)], SOFT, "soft", 1.4)
d.arrow([(CX + MID_W + 2, PY + 108), (RX - 4, PY + 108)], ACC, "acc", 1.4)

# 하단: 스키마 해소 4대 번역 규칙
RULE_Y = PY + S_H + 20
RW_CARD = 196
RGAP = 16

rules = [
    ("필드명 매칭", [
        "순서 달라도 이름 매칭",
        "필드명이 해소의 기준"
    ], ACC),
    ("미지 필드 무시", [
        "writer 에만 있는 필드",
        "예: Fig 5-6 의 photoURL"
    ], WARN),
    ("기본값 보충", [
        "reader 에만 있는 필드",
        "reader 스키마의 기본값"
    ], OK),
    ("동일 스키마 전제", [
        "디코딩에도 writer 스키마",
        "값만 있어 스키마 없인 불가"
    ], INFO)
]

for i, (r_title, r_items, r_col) in enumerate(rules):
    rx = X0 + i * (RW_CARD + RGAP)
    d.box(rx, RULE_Y, RW_CARD, 100, PAPER2, r_col, 1.1 if r_col in (ACC, WARN) else 0.9)
    d.chip(rx + 28, RULE_Y + 18, "규칙", r_col, 11.5)
    d.t(rx + 48, RULE_Y + 22, r_title, 12, INK, KR, "start", 600)
    d.line(rx + 8, RULE_Y + 32, rx + RW_CARD - 8, RULE_Y + 32, RULE, 0.8)
    
    for j, item in enumerate(r_items):
        iy = RULE_Y + 42 + j * 24
        d.t(rx + 14, iy + 12, f"· {item}", 11.5, MUTED, KR, "start")

d.legend(LEG, [("스키마 해소 엔진", ACC), ("writer 스키마 직렬화", INFO), ("reader 기본값 보충", OK), ("미지 필드 무시", WARN)])
d.save("05-03.avro-schema-resolution.svg")
