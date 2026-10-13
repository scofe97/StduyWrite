# 타입 스펙: type-process — 곱셈·나눗셈 사슬을 카드 슬롯(항목·값)으로 늘어놓고 화살표가 계산 순서를 나른다. 요청 수 사슬 한 줄, 저장량 사슬 한 줄. focal 은 피크 QPS.
# 사실 출처: 추출본 v2.txt 3585~3606행 — 일간 사용자 10,000,000 · 하루 검색 10 회 · 질의 20 바이트(4 단어 × 5 글자) · 검색당 요청 20 개 · 신규 질의 20 % · 피크 = 평균 × 2.
#   계산값은 계산식을 본문에 보인다: 10,000,000 × 10 × 20 ÷ 86,400 = 23,148.1 → 23,148 · × 2 = 46,296 · 10,000,000 × 10 × 20 B × 0.2 = 400,000,000 B = 0.4 GB.
# Layout conventions: 카드 폭 168·높이 76, x stride 196(24·220·416·612·808), 줄 y=124·232·360. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, INK, SOFT, KR, MONO

W, H = 1000, 548
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §1",
      "글자마다 요청이 가므로 평균 약 23,000 QPS 이고 하루 신규 질의는 0.4 GB 다",
      "사용자 수에 검색 횟수와 글자 수를 곱해 하루 요청을 구하고 86,400 초로 나누며, 저장량은 질의 크기와 신규 비율로 줄인다.",
      "면접 가정: 일간 사용자 1,000만 · 하루 10 회 · 질의 20 바이트 · 신규 20 %")

CW, CH = 168, 76
XS = (24, 220, 416, 612, 808)
RA, RB, RC = 124, 232, 360


def card(x, y, label, val, c, focal=False):
    d.tone(x, y, CW, CH, ACC if focal else c, 6, "12", 1.4 if focal else 1.0)
    d.t(x + 14, y + 28, label, 13, MUTED, KR, "start")
    d.t(x + 14, y + 58, val, 18, INK, MONO, "start", 600)


d.t(24, 108, "초당 요청 수", 13, SOFT, KR, "start", 600)
A = (("일간 사용자", "10,000,000"), ("하루 검색 횟수", "× 10"), ("검색당 요청 수", "× 20"),
     ("하루 초", "÷ 86,400"), ("평균 QPS", "= 23,148"))
for x, (lab, val) in zip(XS, A):
    card(x, RA, lab, val, INFO)
for i in range(4):
    d.arrow([(XS[i] + CW + 2, RA + 38), (XS[i + 1] - 6, RA + 38)], MUTED, "ar", 1.5)

card(XS[4], RB, "피크 QPS", "× 2 = 46,296", INFO, focal=True)
d.arrow([(XS[4] + CW // 2, RA + CH + 4), (XS[4] + CW // 2, RB - 6)], MUTED, "ar", 1.5)

d.t(24, 348, "하루 신규 저장량", 13, SOFT, KR, "start", 600)
C = (("일간 사용자", "10,000,000"), ("하루 검색 횟수", "× 10"), ("질의 크기", "× 20 B"),
     ("신규 비율", "× 20 %"), ("하루 신규 데이터", "= 0.4 GB"))
for x, (lab, val) in zip(XS, C):
    card(x, RC, lab, val, INFO)
for i in range(4):
    d.arrow([(XS[i] + CW + 2, RC + 38), (XS[i + 1] - 6, RC + 38)], MUTED, "ar", 1.5)

d.legend(H - 56, [("계산 단계", INFO), ("설계 기준이 되는 값", ACC)])
d.save("13-01.qps-calc.svg")
