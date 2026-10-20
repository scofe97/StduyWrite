# 타입 스펙: type-line — Kafka 장애 지속 시간에 따른 메모리 버퍼 점유 건수 변화 (가상 시나리오).
# 사실 출처: 요약 §4.20, 조사 보고서 행 11·12, 본문 4절(가상 시나리오: 유입 속도 초당 50,000건, 메모리 버퍼 상한 100,000건, 2.0초 만에 상한 도달 후 초과분 디스크 WAL 격리, 복구 후 0건으로 해소).
# Layout conventions: x 축 = 경과 시간 0~5초(X0=120, X1=860, 초당 148px), y 축 = 점유 건수 0~100,000건(Y0=400, Y1=200, 25k당 50px). 상한선 점선 y=200. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, KR, MONO, RULE

W, H = 960, 508
d = D(W, H, "SYSTEM DESIGN COURSE · 02-01 §4",
      "장애 동안 버퍼에 쌓인 건수와 상한",
      "초당 5만 건 유입 시 2초 만에 상한 100,000건에 도달하며, 초과분은 디스크 WAL 로 격리됩니다.",
      "가상 시나리오: 유입 속도 50,000 msg/s · 버퍼 상한 100,000건")

X0, X1 = 120, 860
Y0, Y1 = 400, 200

# Y축 그리드 및 라벨 (0, 25k, 50k, 75k, 100k)
y_ticks = [
    (0, "0", Y0),
    (25000, "25,000", 350),
    (50000, "50,000", 300),
    (75000, "75,000", 250),
    (100000, "100,000", 200),
]

for val, lab, y in y_ticks:
    if val < 100000:
        d.line(X0, y, X1, y, RULE, 0.6)
    d.t(X0 - 16, y + 4, lab, 12, SOFT, MONO, "end")

d.t(X0 - 16, Y1 - 24, "건수", 13, SOFT, KR, "end")
d.t(X1, Y0 + 44, "경과 시간 (초)", 13, SOFT, KR, "end")

# X축 눈금 및 라벨 (0 ~ 5초)
x_ticks = [
    (0, "0초 (장애 시작)", 120),
    (1, "1초", 268),
    (2, "2초", 416),
    (3, "3초", 564),
    (4, "4초 (복구 시작)", 712),
    (5, "5초 (완료)", 860),
]

for sec, lab, x in x_ticks:
    d.line(x, Y0, x, Y0 + 8, RULE, 1.0)
    d.t(x, Y0 + 24, lab, 13 if sec in (0, 4, 5) else 12, SOFT, KR if "초" in lab else MONO, "middle")

# 메모리 상한선 (100,000건 점선)
d.line(X0, 200, X1, 200, BAD, 1.2, dash="6 4")
d.t(X1, 188, "메모리 상한 100,000건", 13, BAD, KR, "end", 600)

# 상단 구간 밴드
d.tone(120, 116, 296, 28, INFO, 4, "08", 0.8)
d.t(268, 134, "급증 구간 (50,000건/초)", 13, INFO, KR, "middle")

d.tone(416, 116, 296, 28, WARN, 4, "08", 0.8)
d.t(564, 134, "상한 유지 · 디스크 WAL 격리", 13, WARN, KR, "middle")

d.tone(712, 116, 148, 28, OK, 4, "08", 0.8)
d.t(786, 134, "복구 및 해소", 13, OK, KR, "middle")

# 데이터 라인
# 0s -> 2s: 상승 (120, 400) -> (416, 200)
d.line(120, 400, 416, 200, INFO, 2.2)

# 2s -> 4s: 수평 유지 (416, 200) -> (712, 200)
d.line(416, 200, 712, 200, WARN, 2.2)

# 4s -> 5s: 하강 (712, 200) -> (860, 400)
d.line(712, 200, 860, 400, OK, 2.2)

# 데이터 점 및 콜아웃
d.o.append(f'<circle cx="120" cy="400" r="4" fill="{INFO}"/>')
d.o.append(f'<circle cx="268" cy="300" r="4" fill="{INFO}"/>')
d.t(268 - 14, 290, "50,000건", 13, INFO, MONO, "end")

# 2.0초 상한 도달점 (초점)
d.o.append(f'<circle cx="416" cy="200" r="6" fill="{ACC}"/>')
d.t(416, 172, "2.0초: 상한 100,000건 도달", 13, ACC, KR, "middle", 600)

d.o.append(f'<circle cx="564" cy="200" r="4" fill="{WARN}"/>')
d.t(564, 226, "초과분 로컬 SSD fsync 기록", 13, MUTED, KR, "middle")

# 4.0초 복구 시점
d.o.append(f'<circle cx="712" cy="200" r="5" fill="{OK}"/>')
d.t(712, 172, "4.0초: 복구 감지", 13, OK, KR, "middle", 600)

# 5.0초 해소 완료점
d.o.append(f'<circle cx="860" cy="400" r="4" fill="{OK}"/>')
d.t(860 + 12, 396, "0건 복귀", 13, OK, KR, "start")

d.legend(H - 44, [
    ("버퍼 점유", INFO),
    ("상한 100k", BAD),
    ("2초 도달 (초점)", ACC),
    ("초과분 격리", WARN),
    ("복구 해소", OK),
])

out_path = str(ASSETS_DIR / "02-01.buffer-occupancy.svg")
d.save(out_path)
print(f"saved: {out_path}")
