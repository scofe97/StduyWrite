# 14-03 개요 — 행동 데이터의 자산·권력화와 독성 자산 위험(§1), 산업혁명 공해 유비와 프라이버시 과제(§2), 데이터 최소화 규제와 빅데이터 철학 충돌(§3), 14장에서 1장으로 이어지는 책 전체 종합(§4)을 아우르는 전체 지도.
# 사실 출처: 14-03 본문 서두(L13~L17), §1(L24~L38), §2(L40~L58), §3(L60~L72), §4(L74~L103), DDIA 2판 Ch.14 (PDF p.12~17).
# 2026-10-31 검증: 배너가 §1 범례 색(INFO)을 써서 중립 상자로. '회귀'는 본문에 없어 '엔지니어의 책임'으로.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 252
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "14-03 · CHAPTER OVERVIEW", "데이터의 권력·산업혁명의 교훈·책 종합 전체 지도",
      "데이터의 노동·권력화와 독성 위험(§1), 산업혁명 공해 유비(§2), 데이터 최소화 규제(§3), 14장에서 1장으로의 책 전체 종합(§4)으로 이어지는 체계를 조망한다.",
      "행동 데이터의 노동과 독성 위험 · 산업혁명 공해 유비 · 데이터 최소화 규제 · 14장에서 1장 책 전체 종합")

# 상단 공통 전제 배너
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 23, "데이터는 버려질 배기가스가 아니라 노동이자 권력이며, 동시에 독성 자산", 12, INK, KR, "middle", 600)

CW = 194
GAP = 14
X0 = 28

cards = [
    ("§1", "자산이자 권력", "노동과 독성 자산",
     [("데이터 배기가스 비판", "사용자 활동은 서비스 노동"),
      ("감시 능력의 가치화", "데이터 브로커 매매와 평가"),
      ("독성 자산 (새 우라늄)", "미래 정권 위험과 강제 제출")],
     INFO),
    ("§2", "산업혁명의 교훈", "공해 유비와 프라이버시",
     [("산업혁명의 어두운 면", "매연 · 수질 오염 · 가혹 노동"),
      ("정보화 시대의 공해", "데이터 = 공해, 곪으며 잔존"),
      ("환경 보호와 프라이버시", "사회적 규제로 길들인 장기 이득")],
     WARN),
    ("§3", "입법과 자율 규제", "데이터 최소화 vs 빅데이터",
     [("GDPR 최소화 원칙", "구체적 · 명시적 목적 한정"),
      ("빅데이터 철학 충돌", "수집 최대화와 미예견 탐색"),
      ("문화 전환과 자율 규제", "없는 데이터는 유출 불가")],
     OK),
    ("§4", "책 전체 종합", "14장에서 1장까지",
     [("1~13장 기술 목표", "신뢰성 · 확장성 · 유지보수성"),
      ("14장 한 걸음 물러서기", "차별 · 착취 · 감시 윤리 책임"),
      ("엔지니어의 책임", "사람을 인간으로 존중하는 세상")],
     ACC),
]

FOCAL = 3

for i, (sec, title, sub, items, c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)
    
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, c, 1.0)
        
    d.chip(x + 28, PY + 18, sec, c, 11)
    d.t(x + CW / 2 + 10, PY + 22, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 42, sub, 11, MUTED, KR, "middle")
    d.line(x + 8, PY + 52, x + CW - 8, PY + 52, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = PY + 64 + j * 58
        if is_focal and j == 2:
            d.tone(x + 6, iy, CW - 12, 50, ACC, 4, "20", 1.2)
            d.t(x + CW / 2, iy + 21, h_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, d_txt, 11, ACC, KR, "middle")
        elif is_focal:
            d.tone(x + 6, iy, CW - 12, 50, ACC, 4, "10", 0.9)
            d.t(x + CW / 2, iy + 21, h_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, d_txt, 11, MUTED, KR, "middle")
        elif i == 1 and j == 1:
            d.tone(x + 6, iy, CW - 12, 50, WARN, 4, "16", 0.9)
            d.t(x + CW / 2, iy + 21, h_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, d_txt, 11, WARN, KR, "middle")
        else:
            d.box(x + 6, iy, CW - 12, 50, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 21, h_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, d_txt, 11, MUTED, KR, "middle")

# 카드 간 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    cy = PY + PH / 2
    d.arrow([(x1 + 2, cy), (x2 - 3, cy)], MUTED, "ar", 1.2)

d.legend(LEG, [
    ("책 전체 종합 (focal)", ACC),
    ("자산·독성 위험", INFO),
    ("산업혁명 유비", WARN),
    ("데이터 최소화", OK),
])

d.save("14-03.chapter-overview.svg")
