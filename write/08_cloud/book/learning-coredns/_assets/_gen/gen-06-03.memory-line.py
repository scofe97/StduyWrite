# 06-03 §4 — 메모리 추정식 두 개를 파드+서비스 수 축에 그리고, 170Mi 상한과 만나는 점을 찍는다.
# 근거: coredns/deployment kubernetes/Scaling_CoreDNS.md — "MB required (default settings) = (Pods + Services) / 1000 + 54",
#       "MB required (w/ autopath) = (Pods + Services) / 250 + 56", 실측표의 마지막 점 158200(2026-10-03 확인).
#       16,000 → 70 은 원서 예제, 116,000 → 170 과 28,500 → 170 은 두 식을 170 에 대해 푼 값이다.
# 타입 스펙: type-line — 두 직선의 기울기 차이와 상한선과의 교점이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, BAD, INFO, KR, MONO

W, H = 880, 572
d = D(W, H, "LEARNING COREDNS · 06-03 §4",
      "170Mi 는 기본 설정에서 116,000 개까지 버틴다",
      "기본 설정 식은 1,000 개마다 1MiB 씩, autopath 를 켠 식은 250 개마다 1MiB 씩 오른다. "
      "두 직선이 170Mi 상한과 만나는 점이 각 설정에서 상한이 버티는 규모의 추정치다.",
      "주황 점이 기본 설정에서 상한과 만나는 자리입니다")

X0, X1, Y0, Y1 = 110, 830, 430, 140
NMAX, VMAX = 160000, 300


def fx(n):
    return X0 + n * (X1 - X0) / NMAX


def fy(v):
    return Y0 - v * (Y0 - Y1) / VMAX


for v in (0, 100, 200, 300):
    d.line(X0, fy(v), X1, fy(v), RULE, 0.6)
    d.t(X0 - 12, fy(v) + 4, str(v), 12, SOFT, MONO, "end")
for n, lab in ((0, "0"), (40000, "40k"), (80000, "80k"), (120000, "120k"), (160000, "160k")):
    d.t(fx(n), Y0 + 22, lab, 12, SOFT, MONO)
d.t(X0 - 12, Y1 - 16, "MiB", 12, SOFT, MONO, "end")
d.t(X1, Y0 + 44, "파드 + 서비스 수", 12, SOFT, KR, "end")

d.line(X0, fy(170), X1, fy(170), BAD, 1.2, "6 4")
d.t(X1, fy(170) - 8, "limit 170Mi", 12, BAD, MONO, "end")
d.line(X0, fy(70), X1, fy(70), SOFT, 1.0, "3 5")
d.t(X1, fy(70) - 8, "request 70Mi", 12, SOFT, MONO, "end")

d.path(f"M {fx(0)} {fy(54)} L {fx(NMAX)} {fy(NMAX / 1000 + 54)}", INFO, 1.8)
n_top = (VMAX - 56) * 250
d.path(f"M {fx(0)} {fy(56)} L {fx(n_top)} {fy(VMAX)}", MUTED, 1.6, dash="6 4")

d.line(fx(158200), Y0, fx(158200), Y0 + 8, SOFT, 1.0)
d.t(fx(158200), Y0 - 8, "실측표 끝 158,200", 12, SOFT, KR, "end")

d.o.append(f'<circle cx="{fx(16000)}" cy="{fy(70)}" r="5" fill="{INFO}"/>')
d.t(fx(16000) + 10, fy(70) + 20, "원서 예제 · 16,000 개 → 70", 12, INFO, KR, "start")

d.o.append(f'<circle cx="{fx(28500)}" cy="{fy(170)}" r="5" fill="{MUTED}"/>')
# 200 눈금선과 겹치지 않게 점의 오른쪽 아래에 둔다
d.t(fx(28500) + 14, fy(170) + 22, "autopath · 28,500 개", 12, MUTED, KR, "start")

d.o.append(f'<circle cx="{fx(116000)}" cy="{fy(170)}" r="6" fill="{ACC}"/>')
d.t(fx(116000) + 10, fy(170) + 26, "116,000 개 → 170Mi", 13, ACC, KR, "start", 600)
d.t(fx(116000) + 10, fy(170) + 46, "기본 설정의 한계 추정", 12, MUTED, KR, "start")

d.t(20, 504, "식은 캐시 30MB · 버퍼 5MB 를 품은 추정 · 실제 사용량은 따로 잰다", 13, MUTED, KR, "start")

d.legend(528, [("기본 설정 식", INFO), ("autopath 식", MUTED), ("상한", BAD), ("상한과 만나는 점", ACC)])
d.save("06-03.memory-line.svg")
