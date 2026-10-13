# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다(행 = 가용성, 열 = 허용 비율·하루·한 달·1 년). level 어휘 대신 단위(시간·일 / 분 / 초 이하)로 셀 색을 정한다.
# 사실 출처: 추출본 v2.txt 591~600행·PDF 38쪽 표 2-3(하루 14.40 분 · 1.44 분 · 8.64 초 · 864 ms · 86.40 ms, 1 년 3.65 일 · 8.77 시간 · 52.60 분 · 5.26 분 · 31.56 초).
#   계산: 허용 중단 = (1 − 가용성) × 기간. 하루 86,400 s, 한 달 30 일 = 2,592,000 s(어림), 1 년 365.25 일 = 31,557,600 s(표 2-3 이 이 값으로 맞는다).
#   SLA 99.99% 행: AWS Compute SLA(Last Updated 2022-05-25) Region-Level 99.99%, GCP Compute Engine SLA(Last modified 2025-03-04) Instances in Multiple Zones >= 99.99%.
# Layout conventions(스펙 §2): left_pad 12 · comp_col_w 208 · role_col_w 148 · role_col_gap 16 · header_y 72→104(제목 영역 확보) · row_h 36 · row_stride 40.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

LP, CCW, GAP, RCW, RGAP = 12, 208, 12, 148, 16
NR = 4
W = LP + CCW + GAP + NR * RCW + (NR - 1) * RGAP + 48
HY, HH, RY0, RS, RH = 104, 52, 168, 40, 36
rows = [
    ("99%", "9 가 2 개", ["1%", "14.40 분", "7.2 시간", "3.65 일"]),
    ("99.9%", "9 가 3 개", ["0.1%", "1.44 분", "43.2 분", "8.77 시간"]),
    ("99.99%", "9 가 4 개", ["0.01%", "8.64 초", "4.32 분", "52.60 분"]),
    ("99.999%", "9 가 5 개", ["0.001%", "864 ms", "25.92 초", "5.26 분"]),
    ("99.9999%", "9 가 6 개", ["0.0001%", "86.4 ms", "2.59 초", "31.56 초"]),
]
cls = {  # 단위별 색
    "일": WARN, "시간": WARN, "분": INFO, "초": OK, "ms": OK,
}
H = RY0 + 4 * RS + RH + 92
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 02-01 §3",
      "9 하나가 늘면 허용 중단은 열 배 줄어든다",
      "가용성 99% 에서 99.9999% 까지 하루·한 달(30 일)·1 년의 허용 중단 시간이다. 99.99% 의 한 달 4.32 분이 리전 수준 SLA 가 가리키는 값이다.",
      "허용 중단 = (1 − 가용성) × 기간")

heads = [("허용 비율", "1 − 가용성"), ("하루", "86,400 s"), ("한 달", "2,592,000 s"), ("1 년", "31,557,600 s")]
d.box(LP, HY, CCW, HH, PAPER2, RULE, 0.9, 6)
d.t(LP + CCW / 2, HY + 24, "가용성", 13, INK, KR, "middle", 600)
d.t(LP + CCW / 2, HY + 42, "퍼센트", 12, MUTED, KR)
for j, (a, b) in enumerate(heads):
    x = LP + CCW + GAP + j * (RCW + RGAP)
    d.box(x, HY, RCW, HH, PAPER2, RULE, 0.9, 6)
    d.t(x + RCW / 2, HY + 24, a, 13, INK, KR, "middle", 600)
    d.t(x + RCW / 2, HY + 42, b, 11, MUTED, MONO)

for i, (name, hint, vals) in enumerate(rows):
    y = RY0 + i * RS
    d.box(LP, y, CCW, RH, PAPER2, RULE, 0.8, 4)
    d.t(LP + 12, y + 23, name, 13, INK, MONO, "start", 600)
    d.t(LP + CCW - 12, y + 23, hint, 12, MUTED, KR, "end")
    for j, v in enumerate(vals):
        x = LP + CCW + GAP + j * (RCW + RGAP)
        if j == 0:
            d.box(x, y, RCW, RH, PAPER2, RULE, 0.8, 4)
            d.t(x + RCW / 2, y + 23, v, 13, MUTED, MONO)
            continue
        unit = v.split(" ")[-1]
        c = cls[unit]
        focal = (i == 2 and j == 2)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{RCW}" height="{RH}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + RCW / 2, y + 23, v, 13, ACC, KR, "middle", 600)
        else:
            d.tone(x, y, RCW, RH, c, 4, "14", 1.0)
            d.t(x + RCW / 2, y + 23, v, 13, INK, KR)

d.legend(H - 56, [("일 · 시간 단위", WARN), ("분 단위", INFO), ("초 이하", OK), ("리전 SLA 수준 · 한 달", ACC)])
d.save("02-01.availability-grid.svg")
