# 02-02 판단을 만드는 학습 과정 — 현상에서 판단 수정까지 여섯 단계가 한 줄로 이어지고,
# 검색·AI 는 가설을 세운 뒤에야 끼어든다. 그림의 초점은 순서가 아니라 그 진입 지점이다.
# 타입 스펙: type-flowchart — 왼쪽에서 오른쪽으로 흐르는 단계 열, 아래에서 점선으로 합류하는 보조 입력.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 800, 330
X0, BW, BH, GAP, Y = 24, 108, 58, 20, 112

d = D(W, H, "11_CAREER · GREEDYCON · KANG DAEMYUNG",
      "판단을 만드는 학습 과정",
      "현상에서 판단 수정까지 여섯 단계가 한 줄로 이어진다. 검색과 AI 는 가설을 세운 뒤에 들어온다. "
      "예상과 반증 조건을 먼저 적어야 실제 결과와의 차이가 보이고, 그 차이를 기록할 때 경험이 지식으로 남는다.",
      lead="검색과 AI 는 가설 뒤에 씁니다")

STEPS = [
    ("1 현상", "관찰한 문제",        False),
    ("2 예상", "결과 한 줄",         False),
    ("3 가설", "원인 하나 · 반증 조건", True),
    ("4 실험", "작게 재현",          False),
    ("5 근거", "반복 · 문서 · 운영", False),
    ("6 판단 수정", "차이 기록",      False),
]

def x(k): return X0 + k * (BW + GAP)

for k, (name, sub, focal) in enumerate(STEPS):
    xx = x(k)
    if focal:
        d.tone(xx, Y, BW, BH, ACC, 6)
    elif k == len(STEPS) - 1:
        d.tone(xx, Y, BW, BH, OK, 6)
    else:
        d.box(xx, Y, BW, BH, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else (OK if k == len(STEPS) - 1 else INK)
    d.t(xx + BW / 2, Y + 24, name, 13, col, KR, "middle", 600)
    d.t(xx + BW / 2, Y + 43, sub, 11, SOFT, KR)
    if k < len(STEPS) - 1:
        d.arrow([(xx + BW, Y + BH / 2), (x(k + 1) - 3, Y + BH / 2)], MUTED, "ar", 1.3)

# 검색·AI — 가설 뒤 합류
AX, AY, AW, AH = x(2) + BW / 2 - 70, Y + BH + 56, 140, 40
d.tone(AX, AY, AW, AH, INFO, 6)
d.t(AX + AW / 2, AY + 18, "검색 · AI", 12, INFO, KR, "middle", 600)
d.t(AX + AW / 2, AY + 33, "반례 · 재현 방법 · 비용 · 문서", 11, SOFT, KR)
# 가설에서 내려가 AI 로, AI 에서 실험 사이 corridor 로 점선 합류
mx = x(2) + BW + GAP / 2
d.arrow([(AX + AW / 2, AY), (AX + AW / 2, Y + BH + 30), (mx, Y + BH + 30), (mx, Y + BH / 2 + 10)], INFO, "info", 1.2, "3 3")
d.t(AX + AW + 10, AY + 24, "가설 뒤 질문", 11, MUTED, KR, "start")

# 판단 수정에서 다음 현상으로 돌아가는 고리 (위쪽 ㄷ자)
lx, rx = x(0) + BW / 2, x(5) + BW / 2
d.arrow([(rx, Y), (rx, Y - 26), (lx, Y - 26), (lx, Y - 4)], SOFT, "soft", 1.1, "4 3")
d.t((lx + rx) / 2, Y - 32, "다음 현상", 11, SOFT, MONO)

d.legend(H - 56, [("초점 — AI 가 들어오는 자리", ACC), ("보조 입력", INFO), ("기록으로 남는 단계", OK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "02-02.judgment-loop.svg"))
