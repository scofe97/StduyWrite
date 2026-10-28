# 00-00 서문 — 책의 철학과 2판 변경점. 서문이 짚는 네 갈래를 한 장으로 모은 지도.
# 옛 도식(손으로 쓴 680 폭)은 문장·불릿으로 채워져 있었다. 라벨만 남기고 본문에 없는 문구(It depends)는 뺐다.
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, KR, MONO

W = 880
CW, GAP, X0 = 200, 16, 16
HY, HH = 196, 44                 # 갈래 머리
CY0, CSTRIDE, CH = 260, 44, 36   # 칩 첫 줄·stride·높이
BUS = 172

branches = [
    ("핵심 철학", [("제품보다 원리", INFO), ("상황에 따라 다르다", INFO), ("학문 정밀성", INFO), ("산업 실용성", INFO)]),
    ("누가 읽는가", [("백엔드·아키텍트", INFO), ("데이터·클라우드", INFO), ("시스템 디자인 면접", INFO), ("버즈워드 너머", INFO)]),
    ("2판에서 바뀐 것", [("+ AI/ML", OK), ("+ 클라우드 네이티브", OK), ("+ sync engine", OK), ("+ GraphQL·GDPR", OK), ("− MapReduce", BAD)]),
    ("규모", [("~60쪽 증가", INFO), ("10장 재작성", INFO), ("Riccomini 공저", INFO)]),
]
FOCAL = 0

n = max(len(c) for _, c in branches)
LEG = CY0 + n * CSTRIDE + 16
H = LEG + 56

d = D(W, H, "00-00 · PREFACE", "DDIA 2판 서문 한눈에 보기",
      "서문은 책의 철학, 대상 독자, 2판에서 바뀐 것, 규모 네 갈래로 읽힌다. 철학 갈래가 핵심 논점이다.",
      "철학 · 독자 · 2판 변경 · 규모")

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

d.legend(LEG, [("추가", OK), ("폐기", BAD), ("핵심 논점", ACC)])
d.save("00-00.preface-overview.svg")
