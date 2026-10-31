# 07-01 §4 핫스팟 우회 — 타임스탬프 단독 키의 핫 샤드 쏠림과 센서 ID 접두어 복합 키 쓰기 분산 비교.
# 사실 출처: 07-01 본문 §2(L42)·§4(L64~L70), DDIA 2판 7장 "Sharding by Key Range" (PDF 9쪽: one shard per month, others sit idle, prefix with sensor ID).
# 원서·본문에 구체 시각·월·센서 번호가 없어 값은 넣지 않는다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 564
LEG = H - 46

d = D(W, H, "07-01 · §4 HOTSPOT AVOIDANCE", "타임스탬프 단독 키 핫스팟과 센서 복합 키 분산",
      "타임스탬프 단독 키는 현재 시간 샤드로 모든 쓰기가 몰리지만, 센서 ID를 접두어로 둔 복합 키는 여러 샤드로 균등 분산된다.",
      "단독 타임스탬프 쓰기 쏠림 · 과거 샤드 조회만 · 센서 ID 접두어 복합 키 · 샤드별 쓰기 분산 · 조회 합산 트레이드오프")

PW = 398
PH = 344
Y_PANEL = 104
XL = 36
XR = 446

SW = 114
SH = 124
SGAP = 12
SPAD_X = 16
Y_SHARDS = Y_PANEL + 160

# 1. 좌측: 타임스탬프 단독 키 (병목·쏠림)
d.box(XL, Y_PANEL, PW, PH, PAPER2, WARN, 1.2)
d.chip(XL + 46, Y_PANEL + 20, "단독 키", WARN, 11)
d.t(XL + 92, Y_PANEL + 24, "타임스탬프 단독 키 패턴", 13, INK, KR, "start", 600)
d.line(XL + 16, Y_PANEL + 38, XL + PW - 16, Y_PANEL + 38, RULE, 0.8)

# 쓰기 요청 박스
d.box(XL + 16, Y_PANEL + 48, PW - 32, 44, PAPER, RULE, 0.9)
d.t(XL + 28, Y_PANEL + 65, "센서 측정값 쓰기 (측정 즉시)", 12, MUTED, KR, "start")
d.t(XL + 28, Y_PANEL + 83, "key = timestamp", 11.5, WARN, MONO, "start")

# 쏠림 화살표 3개 (모두 샤드 3으로 수렴)
# 화살표 시작: y = Y_PANEL + 92 = 196, 샤드 3 상단: y = Y_SHARDS = 264
d.path(f"M {XL + 73} 196 L {XL + 73} 226 L {XL + 285} 226 L {XL + 285} 264", WARN, 1.3, m="warn")
d.path(f"M {XL + 199} 196 L {XL + 199} 242 L {XL + 315} 242 L {XL + 315} 264", WARN, 1.5, m="warn")
d.arrow([(XL + 345, 196), (XL + 345, 264)], WARN, "warn", 1.3)

# 샤드 3개 가로 배치
# 샤드 1 (과거 유휴)
sx1 = XL + SPAD_X
d.box(sx1, Y_SHARDS, SW, SH, PAPER, RULE, 0.8)
d.chip(sx1 + SW / 2, Y_SHARDS + 16, "샤드 1", MUTED, 11)
d.t(sx1 + SW / 2, Y_SHARDS + 48, "과거 달", 11.5, MUTED, KR, "middle")
d.t(sx1 + SW / 2, Y_SHARDS + 76, "조회만", 11.5, MUTED, KR, "middle")
d.t(sx1 + SW / 2, Y_SHARDS + 104, "쓰기 0%", 11.5, SOFT, KR, "middle")

# 샤드 2 (과거 유휴)
sx2 = sx1 + SW + SGAP
d.box(sx2, Y_SHARDS, SW, SH, PAPER, RULE, 0.8)
d.chip(sx2 + SW / 2, Y_SHARDS + 16, "샤드 2", MUTED, 11)
d.t(sx2 + SW / 2, Y_SHARDS + 48, "과거 달", 11.5, MUTED, KR, "middle")
d.t(sx2 + SW / 2, Y_SHARDS + 76, "조회만", 11.5, MUTED, KR, "middle")
d.t(sx2 + SW / 2, Y_SHARDS + 104, "쓰기 0%", 11.5, SOFT, KR, "middle")

# 샤드 3 (핫 샤드 과부하)
sx3 = sx2 + SW + SGAP
d.tone(sx3, Y_SHARDS, SW, SH, WARN, 6, "22", 1.4)
d.chip(sx3 + SW / 2, Y_SHARDS + 16, "샤드 3", WARN, 11)
d.t(sx3 + SW / 2, Y_SHARDS + 48, "이달의 샤드", 12, WARN, KR, "middle", 600)
d.t(sx3 + SW / 2, Y_SHARDS + 76, "핫 샤드 과부하", 12, WARN, KR, "middle", 600)
d.t(sx3 + SW / 2, Y_SHARDS + 104, "쓰기 100%", 12, WARN, KR, "middle", 600)

# 결과 바닥 상자
Y_RES = Y_SHARDS + SH + 12
d.tone(XL + 16, Y_RES, PW - 32, 34, WARN, 4, "14", 0.9)
d.t(XL + PW / 2, Y_RES + 21, "이달의 샤드 쓰기 집중 · 수평 확장 무력화", 12, WARN, KR, "middle", 600)


# 2. 우측: 센서 ID 접두어 복합 키 (쓰기 분산 - FOCAL)
d.box(XR, Y_PANEL, PW, PH, PAPER2, ACC, 1.4)
d.chip(XR + 46, Y_PANEL + 20, "복합 키", ACC, 11)
d.t(XR + 92, Y_PANEL + 24, "센서 ID 접두어 복합 키 패턴", 13, INK, KR, "start", 600)
d.line(XR + 16, Y_PANEL + 38, XR + PW - 16, Y_PANEL + 38, RULE, 0.8)

# 쓰기 요청 박스
d.box(XR + 16, Y_PANEL + 48, PW - 32, 44, PAPER, RULE, 0.9)
d.t(XR + 28, Y_PANEL + 65, "센서 식별자를 접두어로 붙인 복합 키", 12, MUTED, KR, "start")
d.t(XR + 28, Y_PANEL + 83, "key = [sensor_id, timestamp]", 11.5, ACC, MONO, "start")

# 분산 화살표 3개 (각 샤드로 수직 분산)
rx1 = XR + SPAD_X
rx2 = rx1 + SW + SGAP
rx3 = rx2 + SW + SGAP

d.arrow([(rx1 + SW / 2, 196), (rx1 + SW / 2, 264)], OK, "ok", 1.3)
d.arrow([(rx2 + SW / 2, 196), (rx2 + SW / 2, 264)], OK, "ok", 1.3)
d.arrow([(rx3 + SW / 2, 196), (rx3 + SW / 2, 264)], OK, "ok", 1.3)

# 샤드 A
d.tone(rx1, Y_SHARDS, SW, SH, OK, 4, "12", 0.9)
d.chip(rx1 + SW / 2, Y_SHARDS + 16, "샤드 A", OK, 11)
d.t(rx1 + SW / 2, Y_SHARDS + 48, "센서 ID 구간", 11.5, INK, KR, "middle")
d.t(rx1 + SW / 2, Y_SHARDS + 76, "ID 안 시각 정렬", 11.5, MUTED, KR, "middle")
d.t(rx1 + SW / 2, Y_SHARDS + 104, "쓰기 분산", 11.5, OK, KR, "middle", 600)

# 샤드 B
d.tone(rx2, Y_SHARDS, SW, SH, OK, 4, "12", 0.9)
d.chip(rx2 + SW / 2, Y_SHARDS + 16, "샤드 B", OK, 11)
d.t(rx2 + SW / 2, Y_SHARDS + 48, "센서 ID 구간", 11.5, INK, KR, "middle")
d.t(rx2 + SW / 2, Y_SHARDS + 76, "ID 안 시각 정렬", 11.5, MUTED, KR, "middle")
d.t(rx2 + SW / 2, Y_SHARDS + 104, "쓰기 분산", 11.5, OK, KR, "middle", 600)

# 샤드 C
d.tone(rx3, Y_SHARDS, SW, SH, OK, 6, "16", 1.1)
d.chip(rx3 + SW / 2, Y_SHARDS + 16, "샤드 C", OK, 11)
d.t(rx3 + SW / 2, Y_SHARDS + 48, "센서 ID 구간", 11.5, INK, KR, "middle")
d.t(rx3 + SW / 2, Y_SHARDS + 76, "ID 안 시각 정렬", 11.5, MUTED, KR, "middle")
d.t(rx3 + SW / 2, Y_SHARDS + 104, "쓰기 분산", 11.5, OK, KR, "middle", 600)

# 결과 바닥 상자
d.tone(XR + 16, Y_RES, PW - 32, 34, OK, 4, "14", 0.9)
d.t(XR + PW / 2, Y_RES + 21, "많은 센서 동시 쓰기 · 쓰기 고르게 분산", 12, OK, KR, "middle", 600)


# 3. 하단 트레이드오프 배너
Y_TR = Y_PANEL + PH + 14
d.box(36, Y_TR, W - 72, 42, PAPER2, RULE, 0.9)
d.t(48, Y_TR + 18, "조회 트레이드오프", 11.5, SOFT, KR, "start", 600)
d.t(48, Y_TR + 33, "여러 센서 · 시간 구간 조회 → 센서별 범위 쿼리 + 클라이언트 합산", 11.5, INK, KR, "start")

# 하단 범례
d.legend(LEG, [
    ("단일 샤드 쓰기 쏠림 (핫스팟)", WARN),
    ("복합 키 분산 메커니즘", ACC),
    ("샤드별 쓰기 분산", OK),
])

d.save("07-01.hotspot-avoidance.svg")
