# 02-01 §4 — CPU 1 사이클을 1초로 늘렸을 때의 지연, 로그 눈금 가로 막대.
# 타입 스펙: type-bar — 범주별 수치 비교. 범주 이름이 길어 가로 막대로 눕힌다.
#           축약: 원서 표 2.2(p.6) 16행 중 자릿수가 달라지는 대표 9행만 그린다(나머지는 본문 표).
#           값이 범위인 행(SSD·회전 디스크·TCP 재전송)은 막대 끝을 범위 띠로 그린다.
import sys, math; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 632
LX, PX, PW = 24, 232, 640           # 라벨 열 · 그림 영역 시작 · 폭
Y0, ROW, BAR = 132, 40, 22
MIN, HOUR, DAY, YEAR = 60, 3600, 86400, 31_557_600
LO, HI = 0, 12                      # 10^0 초 ~ 10^12 초

def px(sec): return PX + PW * (math.log10(sec) - LO) / (HI - LO)

ROWS = [  # (이벤트, 실제 지연, 환산 표기, 환산 초 하한, 상한)
    ("CPU 1 사이클", "0.3 ns", "1초", 1, 1),
    ("L1 캐시 접근", "0.9 ns", "3초", 3, 3),
    ("L3 캐시 접근", "10 ns", "33초", 33, 33),
    ("메인 메모리(DRAM)", "100 ns", "6분", 6 * MIN, 6 * MIN),
    ("SSD I/O", "10–100 μs", "9–90시간", 9 * HOUR, 90 * HOUR),
    ("회전 디스크 I/O", "1–10 ms", "1–12개월", YEAR / 12, YEAR),
    ("인터넷 SF→뉴욕", "40 ms", "4년", 4 * YEAR, 4 * YEAR),
    ("TCP 타이머 재전송", "1–3 s", "105–317년", 105 * YEAR, 317 * YEAR),
    ("물리 시스템 재부팅", "5 m", "3만 2천 년", 32_000 * YEAR, 32_000 * YEAR),
]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §4",
       "한 사이클을 1초로 늘리면",
       "원서 표 2.2 의 대표 아홉 행을 로그 눈금 가로 막대로 그렸다. 눈금 하나가 열 배이고, 막대 끝의 띠는 값의 범위다.",
       "가로축 로그 눈금 — 사람의 시간 단위로 표시")

TICKS = [(1, "1초"), (MIN, "1분"), (HOUR, "1시간"), (DAY, "1일"), (YEAR, "1년"), (1000 * YEAR, "천 년")]
ybot = Y0 + len(ROWS) * ROW
for sec, lab in TICKS:
    x = px(sec)
    d.line(x, Y0 - 8, x, ybot, RULE, 0.8)
    d.t(x, Y0 - 16, lab, 12, SOFT, KR, "middle")
d.t(LX, Y0 - 16, "이벤트 · 실제 지연", 12, SOFT, KR, "start")

for i, (name, real, scaled, lo, hi) in enumerate(ROWS):
    y = Y0 + i * ROW
    focal = name.startswith("메인 메모리")
    c = ACC if focal else MUTED
    d.t(LX, y + 16, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(PX - 12, y + 16, real, 12, SOFT, MONO, "end")
    x0, x1 = PX, max(px(lo), PX + 4)
    if focal: d.tone(x0, y + 4, x1 - x0, BAR - 8, ACC, 3)
    else: d.box(x0, y + 4, x1 - x0, BAR - 8, PAPER2, MUTED, 1.0, 3)
    if hi > lo:
        d.tone(px(lo), y + 4, px(hi) - px(lo), BAR - 8, INFO, 3)
    end = max(px(hi), x1)
    if end > PX + PW - 96:   # 오른쪽 끝 막대는 라벨을 막대 안쪽 끝에 붙인다
        d.t(end - 10, y + 16, scaled, 13, INK, KR, "end", 600)
    else:
        d.t(end + 8, y + 16, scaled, 13, ACC if focal else INK, KR, "start", 600)

d.legend(ybot + 28, [("환산한 시간", MUTED), ("값의 범위", INFO), ("본문이 짚는 행 — 메모리 6분", ACC)])
d.save("02-01.time-scale-log.svg")
