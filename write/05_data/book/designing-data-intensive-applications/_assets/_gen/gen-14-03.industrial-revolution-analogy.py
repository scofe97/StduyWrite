# 14-03 §2 — 산업혁명의 공해 극복과 정보화 시대의 데이터·프라이버시 과제 대응 유비.
# 사실 출처: 14-03 본문 §2(L40~L58), DDIA 2판 Ch.14 "Remembering the Industrial Revolution" (PDF p.14~15).
# 2026-10-31 검증: 시기(18~19세기·21세기)는 본문·원서에 없어 지움. 배너·하단 바는 범례 색과 겹쳐 중립 상자로.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Z1_Y = 150
ZH = 102
Z2_Y = 276
INSIGHT_Y = 394
INSIGHT_H = 36
LEG = 444
H = LEG + 52

d = D(W, H, "14-03 · §2 INDUSTRIAL REVOLUTION ANALOGY", "산업혁명의 공해 극복과 정보화 시대의 데이터 대응",
      "산업혁명이 기술 발전 뒤 매연·아동노동 공해를 규제로 길들였듯, 정보화 시대는 축적된 데이터 공해에 프라이버시 보호와 데이터 최소화로 맞서야 한다.",
      "기술 발전 · 공해와 어두운 면 · 제도적 안전장치 · 장기적 사회 이득의 4단계 유비 대응")

# 상단 배너
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 23, "역사적 유비: 산업혁명이 공해 규제로 사회적 이득을 얻었듯, 정보화 시대는 프라이버시 보호로 데이터 공해에 대응", 12, INK, KR, "middle", 600)

# Zone 1: 산업혁명
d.box(28, Z1_Y, W - 56, ZH, PAPER2, RULE, 1.0)
d.t(40, Z1_Y + 18, "산업혁명 — 성장과 공해, 오랜 시간 끝의 안전장치", 11, SOFT, KR, "start", 600)

s1_boxes = [
    ("1. 기술·농업 발전", "장기적 경제 성장", "생활 수준의 전반적 향상", INFO, INFO),
    ("2. 어두운 면과 공해", "매연 대기오염 · 폐수 오염", "가혹한 노동과 아동 노동", WARN, WARN),
    ("3. 안전장치 제도화", "환경 보호 규제 · 안전 규약", "아동노동 금지법 · 위생 검사", OK, OK),
    ("4. 장기적 사회 이득", "사업 비용은 상승", "이전으로 돌아가길 원치 않음", INFO, INFO),
]

BX0 = 38
BW = 188
BGAP = 18
BY1 = Z1_Y + 26
BH = 64

for i, (t_txt, s1_txt, s2_txt, stroke_c, title_c) in enumerate(s1_boxes):
    bx = BX0 + i * (BW + BGAP)
    d.box(bx, BY1, BW, BH, PAPER, stroke_c, 0.9)
    d.t(bx + BW / 2, BY1 + 20, t_txt, 12, title_c, KR, "middle", 600)
    d.t(bx + BW / 2, BY1 + 38, s1_txt, 11, MUTED, KR, "middle")
    d.t(bx + BW / 2, BY1 + 54, s2_txt, 11, SOFT, KR, "middle")
    if i < 3:
        ax = bx + BW
        d.arrow([(ax + 2, BY1 + BH / 2), (ax + BGAP - 2, BY1 + BH / 2)], MUTED, "ar", 1.2)

# 유비 대응 라벨 (세로 점선은 라벨을 관통해 지움)
for i, tag in enumerate(["기술 발전", "공해 유비 (≈)", "안전장치", "사회적 귀결"]):
    cx = BX0 + i * (BW + BGAP) + BW / 2
    d.t(cx, (Z1_Y + ZH + Z2_Y) / 2 + 4, tag, 11, WARN if i == 1 else SOFT, KR, "middle", 600 if i == 1 else 400)

# Zone 2: 정보화 시대
d.box(28, Z2_Y, W - 56, ZH, PAPER2, RULE, 1.0)
d.t(40, Z2_Y + 18, "정보화 시대 — 데이터라는 공해와 프라이버시라는 환경 과제", 11, SOFT, KR, "start", 600)

s2_boxes = [
    ("1. 정보 기술 발전", "인터넷 · 소프트웨어 자동화", "데이터 저장과 처리", INFO, INFO, False),
    ("2. 데이터 = 공해", "컴퓨터 생산 정보 곪으며 잔존", "감시 정상화 · 유출 위험 노출", ACC, ACC, True),
    ("3. 프라이버시 과제", "데이터 최소화 · 수집 억제", "GDPR 규제와 업계 자율 규제", OK, OK, False),
    ("4. 건강한 정보 경제", "사람을 인간으로 존중", "신뢰 확립 · 후손의 평가 부응", INFO, INFO, False),
]

BY2 = Z2_Y + 26

for i, (t_txt, s1_txt, s2_txt, stroke_c, title_c, is_focal) in enumerate(s2_boxes):
    bx = BX0 + i * (BW + BGAP)
    if is_focal:
        d.tone(bx, BY2, BW, BH, ACC, 6, "1C", 1.4)
        d.t(bx + BW / 2, BY2 + 20, t_txt, 12, ACC, KR, "middle", 600)
        d.t(bx + BW / 2, BY2 + 38, s1_txt, 11, ACC, KR, "middle")
        d.t(bx + BW / 2, BY2 + 54, s2_txt, 11, SOFT, KR, "middle")
    else:
        d.box(bx, BY2, BW, BH, PAPER, stroke_c, 0.9)
        d.t(bx + BW / 2, BY2 + 20, t_txt, 12, title_c, KR, "middle", 600)
        d.t(bx + BW / 2, BY2 + 38, s1_txt, 11, MUTED, KR, "middle")
        d.t(bx + BW / 2, BY2 + 54, s2_txt, 11, SOFT, KR, "middle")
    if i < 3:
        ax = bx + BW
        d.arrow([(ax + 2, BY2 + BH / 2), (ax + BGAP - 2, BY2 + BH / 2)], MUTED, "ar", 1.2)

# 하단 Schneier 인용 요약 바
d.box(28, INSIGHT_Y, W - 56, INSIGHT_H, PAPER2, RULE, 1.0)
d.t(W / 2, INSIGHT_Y + 23, "Schneier: 정보화 시대의 공해(데이터)와 환경 과제(프라이버시 보호)", 12, INK, KR, "middle")

d.legend(LEG, [
    ("데이터 공해 과제 (focal)", ACC),
    ("산업혁명 공해", WARN),
    ("제도적 안전장치", OK),
    ("기술 발전과 귀결", INFO),
])

d.save("14-03.industrial-revolution-analogy.svg")
