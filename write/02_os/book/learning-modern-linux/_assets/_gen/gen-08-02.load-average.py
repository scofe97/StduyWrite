# 08-02 §2 — 같은 부하 평균이 CPU 수에 따라 CPU 하나에 걸린 몫이 달라진다.
# 1차 자료(procps-ng uptime(1)): "Load averages are not normalized for the number of CPUs in a system,
#       so a load average of 1 means a single CPU system is loaded all the time while on a 4 CPU system
#       it means it was idle 75% of the time."
# 실측: debian:12 컨테이너 `uptime; nproc` → load average 1.37, nproc 8 (2026-11-10).
# 앞 두 막대는 man page 의 예, 세 번째 막대는 실측값을 CPU 수로 나눈 값이다.
# 타입 스펙: type-bar — 범주별 수치(load ÷ CPU 수)를 막대 길이로 비교한다. 막대 길이가 값에 정비례하고
#           수치를 막대 끝에 적는다. 축약: 1·5·15분 세 구간의 시간 축은 본문 산문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 880, 400
BAR_X, BAR_MAX, BAR_H, STRIDE, Y0 = 280, 440, 36, 64, 112
ROWS = [
    ("CPU 1개 · load 1.00", 1.00, "man page 의 예 · 내내 바쁨", INFO, False),
    ("CPU 4개 · load 1.00", 0.25, "man page 의 예 · 75% 유휴", INFO, False),
    ("CPU 8개 · load 1.37", 0.17, "컨테이너 실측 · 1.37 ÷ 8", ACC, True),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §2",
      "부하 평균을 CPU 수로 나눈 몫",
      "부하 평균은 CPU 수로 정규화되지 않으므로 같은 값도 CPU 수에 따라 CPU 하나에 걸린 몫이 다르다. "
      "막대는 load 를 CPU 수로 나눈 값이다.",
      "값을 읽기 전에 그 기계의 CPU 수부터 확인합니다")

for i, (name, v, note, col, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    w = BAR_MAX * v
    if focal:
        d.tone(BAR_X, y, w, BAR_H, ACC, 4, "2E", 1.3)
    else:
        d.o.append(f'<rect x="{BAR_X}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{col}3A"/>')
    d.t(24, y + 15, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(24, y + 32, note, 12, MUTED, KR, "start")
    d.t(BAR_X + w + 12, y + 23, f"{v:.2f}", 13, col, MONO, "start", 600)

AY = Y0 + 3 * STRIDE - 12
d.line(BAR_X, AY, BAR_X + BAR_MAX, AY, RULE, 1)
for v in (0, 0.25, 0.5, 0.75, 1.0):
    x = BAR_X + BAR_MAX * v
    d.line(x, AY, x, AY + 6, RULE, 1)
    d.t(x, AY + 20, f"{v:.2f}", 11, SOFT, MONO)
d.t(BAR_X - 32, AY + 20, "load ÷ CPU 수", 12, SOFT, KR, "end")

d.legend(H - 48, [("man page 의 예", INFO), ("컨테이너 실측", ACC)])
d.save("08-02.load-average.svg")
print("ok 08-02.load-average")
