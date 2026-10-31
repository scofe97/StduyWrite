# 00-00 서문 — 책의 철학과 2판 변경점. 서문의 네 절(안내 철학·대상 독자·2판 변경점·참조 활용)을 한 장으로 모은 전체 지도.
# 사실 출처: 00-00 §1(L29~L50), §2(L53~L65), §3(L68~L91), §4(L93~L105)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, KR, MONO

W = 880
CW, GAP, X0 = 200, 16, 16
HY, HH = 196, 44                 # 갈래 머리
CY0, CSTRIDE, CH = 260, 44, 36   # 칩 첫 줄·stride·높이
BUS = 172

branches = [
    ("§1 안내 철학", [
        ("제품보다 원리", INFO),
        ("시스템이 내린 트레이드오프", INFO),
        ("학문적 정밀성", INFO),
        ("산업적 실용성", INFO),
    ]),
    ("§2 대상 독자", [
        ("백엔드 아키텍처", INFO),
        ("데이터·클라우드", INFO),
        ("시스템 디자인 면접", INFO),
        ("버즈워드 너머 이해", INFO),
    ]),
    ("§3 2판 변경점", [
        ("+ AI 뒷받침 데이터 시스템", OK),
        ("+ 클라우드 네이티브 아이디어", OK),
        ("+ sync engine", OK),
        ("+ GraphQL·GDPR", OK),
        ("− MapReduce", BAD),
    ]),
    ("§4 참조 활용", [
        ("본문 원전 탐색", INFO),
        ("오픈 액세스 무료 열람", INFO),
        ("아카이브 링크 복구", INFO),
        ("공식 참조·정오표", INFO),
    ]),
]
FOCAL = 0

n = max(len(c) for _, c in branches)
LEG = CY0 + n * CSTRIDE + 16
H = LEG + 56

d = D(W, H, "00-00 · PREFACE", "서문 안내 철학과 독자층·2판 변경점·참조 활용 전체 지도",
      "서문이 제시하는 안내 철학(§1), 대상 독자(§2), 2판 변경점(§3), 참조 활용법(§4)의 네 갈래를 조망한다. 제품 매뉴얼이 아닌 변하지 않는 원리를 다루는 철학 갈래가 핵심 논점이다.",
      "원리 중심 철학 · 대상 독자층 · 2판 변경점 · 원전과 참조 활용")

rx = W / 2
d.box(rx - 100, 104, 200, 44, PAPER2, RULE, 1.0)
d.t(rx, 132, "DDIA 2판 · 서문", 14, INK, KR, "middle", 600)

cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]
d.line(rx, 148, rx, BUS, RULE, 1.2)
d.line(cx[0], BUS, cx[-1], BUS, RULE, 1.2)
for i, (title, chips) in enumerate(branches):
    x = cx[i] - CW / 2
    d.line(cx[i], BUS, cx[i], HY, RULE, 1.2)
    if i == FOCAL:
        d.tone(x, HY, CW, HH, ACC, 6, "1F", 1.4)
    else:
        d.box(x, HY, CW, HH, PAPER2, RULE, 1.0)
    d.t(cx[i], HY + 28, title, 14, INK, KR, "middle", 600)
    d.line(cx[i], HY + HH, cx[i], CY0 - 8, RULE, 1.0)
    for j, (txt, c) in enumerate(chips):
        y = CY0 + j * CSTRIDE
        d.tone(x, y, CW, CH, c, 6, "14", 1.0)
        d.t(cx[i], y + 23, txt, 12, INK, MONO if txt[0] in "+−~" and not any('가' <= ch <= '힣' for ch in txt) else KR)

d.legend(LEG, [("핵심 논점 (focal)", ACC), ("서문 주제", INFO), ("2판 추가", OK), ("2판 폐기", BAD)])
d.save("00-00.preface-overview.svg")
