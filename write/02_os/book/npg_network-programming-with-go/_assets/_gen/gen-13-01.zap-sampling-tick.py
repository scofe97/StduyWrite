# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Listing 13-11, zapcore.NewSamplerWithOptions
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 940, 560
d = D(W, H, "ZAP SAMPLING TICK · PROCESS",
      "1초 틱 단위 동일 메시지 샘플링 동작 (first=1, thereafter=3)",
      "NewSamplerWithOptions 는 한 틱(1초) 안에서 동일한 레벨과 메시지를 가진 엔트리의 "
      "처음 1개를 기록하고, 이후에는 매 3번째(thereafter) 중복 엔트리만 통과시켜 CPU 와 I/O 부하를 줄입니다.",
      lead="i=5 에서 1초 수면으로 틱이 갱신되어 카운터가 리셋됩니다.")

# 상단 설정 배너
d.box(36, 110, W - 72, 44, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(56, 137, "샘플러 설정:", 11, INFO, KR, "start", 600)
d.t(140, 137, "NewSamplerWithOptions(core, time.Second, 1, 3)", 11, INK, MONO, "start", 600)
d.t(610, 137, "동일 메시지: \"debug message\"", 11, SOFT, KR, "start")

# 1. 첫째 틱 (Tick 1: i=0 ~ 4)
T1_Y = 176
d.box(36, T1_Y, W - 72, 140, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(56, T1_Y + 24, "틱 1 (0.0초 ~ 1.0초)", 12, OK, KR, "start", 600)
d.t(210, T1_Y + 24, "루프 반복 i=0 ~ 4 (동일 메시지 5회 호출)", 11, SOFT, KR, "start")

cols = [
    ("i=0", "1회차 (first)", "기록 (출력)", OK, True),
    ("i=1", "2회차 (중복 1)", "버림 (드롭)", BAD, False),
    ("i=2", "3회차 (중복 2)", "버림 (드롭)", BAD, False),
    ("i=3", "4회차 (중복 3)", "기록 (출력)", ACC, True),
    ("i=4", "5회차 (중복 4)", "버림 (드롭)", BAD, False),
]

col_w = 150
gap = 20
x0 = 56

for j, (it, rep, act, col, is_rec) in enumerate(cols):
    cx = x0 + j * (col_w + gap)
    cy = T1_Y + 44
    d.tone(cx, cy, col_w, 76, col, 4, "15" if is_rec else "08", 1.2 if is_rec else 0.8)
    d.t(cx + col_w / 2, cy + 22, it, 11, INK, MONO, "middle", 600)
    d.t(cx + col_w / 2, cy + 42, rep, 11, SOFT, KR, "middle")
    d.t(cx + col_w / 2, cy + 62, act, 11, col, KR, "middle", 600)

# 중간 경계 배너: time.Sleep(time.Second)
SY = 332
d.box(36, SY, W - 72, 34, fill=PAPER, stroke=WARN, sw=1.1, r=4)
d.t(W / 2, SY + 22, "경계: if i == 5 { time.Sleep(time.Second) } → 1초 경과로 틱 갱신 및 카운터 초기화", 11, WARN, KR, "middle", 600)

# 2. 둘째 틱 (Tick 2: i=5 ~ 9)
T2_Y = 380
d.box(36, T2_Y, W - 72, 140, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(56, T2_Y + 24, "틱 2 (1.0초 ~ 2.0초)", 12, OK, KR, "start", 600)
d.t(210, T2_Y + 24, "루프 반복 i=5 ~ 9 (새 틱에서 카운트 새로 시작)", 11, SOFT, KR, "start")

cols2 = [
    ("i=5", "1회차 (first)", "기록 (출력)", OK, True),
    ("i=6", "2회차 (중복 1)", "버림 (드롭)", BAD, False),
    ("i=7", "3회차 (중복 2)", "버림 (드롭)", BAD, False),
    ("i=8", "4회차 (중복 3)", "기록 (출력)", ACC, True),
    ("i=9", "5회차 (중복 4)", "버림 (드롭)", BAD, False),
]

for j, (it, rep, act, col, is_rec) in enumerate(cols2):
    cx = x0 + j * (col_w + gap)
    cy = T2_Y + 44
    d.tone(cx, cy, col_w, 76, col, 4, "15" if is_rec else "08", 1.2 if is_rec else 0.8)
    d.t(cx + col_w / 2, cy + 22, it, 11, INK, MONO, "middle", 600)
    d.t(cx + col_w / 2, cy + 42, rep, 11, SOFT, KR, "middle")
    d.t(cx + col_w / 2, cy + 62, act, 11, col, KR, "middle", 600)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.zap-sampling-tick.svg"
d.save(str(svg_path))
print("ok 13-01 zap-sampling-tick")
