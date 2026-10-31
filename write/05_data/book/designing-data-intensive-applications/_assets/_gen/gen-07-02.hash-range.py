# 07-02 §4 해시 범위 샤딩 — 16비트 해시값의 연속 범위 분할과 샤드 배정 구조.
# 사실 출처: 07-02 본문 §4(L64), DDIA 2판 7장 p.14 Figure 7-5 (타임스탬프 6개·해시값·샤드 경계는 그림 그대로, 화살표 x 는 값/65,536 비례로 검산) "Assigning a contiguous range of hash values to each shard"
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
BAR_X = 360
BAR_W = 480
BAR_Y = 370
BAR_H = 52
LEG = BAR_Y + BAR_H + 46
H = LEG + 56

d = D(W, H, "07-02 · §4 DATA FLOW", "16비트 해시 범위 할당과 샤드 매핑",
      "인접한 타임스탬프 키를 16비트 해시로 변환해 0부터 65,535 구간에 균등 분산하고, 연속된 해시 범위를 샤드 0부터 3에 할당한다.",
      "타임스탬프 키 입력 · 16비트 해시값 변환 · 연속 해시 범위 샤드 매핑 (Shard 0~3)")

# 상단 안내 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "해시값의 연속 범위를 샤드에 할당 · 샤드가 너무 커지면 범위를 분할해 새 샤드", 12, INK, KR, "middle", 600)

# 6개 샘플 데이터 (DDIA 2판 Figure 7-5 완전 일치)
samples = [
    ("\"2024-12-19 17:08:10\"", "7,372",  414),
    ("\"2024-12-19 17:08:11\"", "18,805", 498),
    ("\"2024-12-19 17:08:12\"", "50,537", 730),
    ("\"2024-12-19 17:08:13\"", "31,579", 591),
    ("\"2024-12-19 17:08:14\"", "62,253", 816),
    ("\"2024-12-19 17:08:15\"", "24,510", 539),
]

KEY_X = 32
KEY_W = 168
HASH_X = 224
HASH_W = 68

d.t(KEY_X + 10, 154, "파티션 키 (타임스탬프)", 12, SOFT, KR, "start", 600)
d.t(HASH_X + HASH_W / 2, 154, "16비트 해시", 12, SOFT, KR, "middle", 600)

for i, (k_str, h_val, tx) in enumerate(samples):
    y = 176 + i * 31
    # 키 박스
    d.box(KEY_X, y - 14, KEY_W, 26, PAPER2, RULE, 0.8)
    d.t(KEY_X + 10, y + 3, k_str, 11, INK, MONO, "start")

    # 키 -> 해시 화살표
    d.arrow([(KEY_X + KEY_W + 4, y), (HASH_X - 6, y)], MUTED, "ar", 1.2)

    # 해시 값
    d.tone(HASH_X, y - 14, HASH_W, 26, INFO, 4, "14", 0.9)
    d.t(HASH_X + HASH_W / 2, y + 4, h_val, 11, INFO, MONO, "middle", 600)

    # 해시 -> 샤드 직교 라우팅 화살표 (수평 -> 수직 단일 꺾임)
    d.arrow([(HASH_X + HASH_W + 4, y), (tx, y), (tx, BAR_Y - 2)], INFO, "info", 1.3)

# 하단 16비트 샤드 연속 범위 바
# 바 위에 두면 수직 화살표가 글자를 가로지르므로 바 왼쪽 빈자리에 둔다
d.t(KEY_X + 10, BAR_Y + 31, "연속 해시값 구간 샤드 배정", 12, INK, KR, "start", 600)

shards = [
    ("Shard 0", "0 ~ 16,383", 0),
    ("Shard 1", "16,384 ~ 32,767", 1),
    ("Shard 2", "32,768 ~ 49,151", 2),
    ("Shard 3", "49,152 ~ 65,535", 3),
]

SW = BAR_W / 4
for i, (s_name, s_range, idx) in enumerate(shards):
    sx = BAR_X + i * SW
    # 활성 샤드(키가 배정된 샤드 0, 1, 3)는 ACC, 빈 샤드 2는 PAPER2
    if idx in (0, 1, 3):
        d.tone(sx, BAR_Y, SW, BAR_H, ACC, 4, "18", 1.2)
        d.t(sx + SW / 2, BAR_Y + 22, s_name, 13, INK, KR, "middle", 600)
        d.t(sx + SW / 2, BAR_Y + 39, s_range, 11, ACC, MONO, "middle")
    else:
        d.box(sx, BAR_Y, SW, BAR_H, PAPER2, RULE, 0.9)
        d.t(sx + SW / 2, BAR_Y + 22, s_name, 13, MUTED, KR, "middle", 600)
        d.t(sx + SW / 2, BAR_Y + 39, s_range, 11, SOFT, MONO, "middle")

# 눈금 및 경계값 라벨
ticks = [
    (BAR_X, "0"),
    (BAR_X + SW, "16,383"),
    (BAR_X + SW * 2, "32,767"),
    (BAR_X + SW * 3, "49,151"),
    (BAR_X + SW * 4, "65,535"),
]
for tx, t_lab in ticks:
    d.line(tx, BAR_Y + BAR_H, tx, BAR_Y + BAR_H + 6, RULE, 1.0)
    d.t(tx, BAR_Y + BAR_H + 18, t_lab, 11, SOFT, MONO, "middle")

d.legend(LEG, [("키가 배정된 샤드", ACC), ("해시값 · 배정 경로", INFO), ("키가 없는 샤드", MUTED)])
d.save("07-02.hash-range.svg")
