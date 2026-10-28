# 01-05 §2 — 잊힐 권리와 불변 로그가 부딪히는 자리. 법이 설계의 기초에 영향을 준다는 절의 핵심 충돌만 그린다.
# 옛 도식의 「1장 종합 — 5개 트레이드오프 축」은 본문·README 의 네 축과 어긋나서 뺐다. 네 축은 §4 본문이 말로 맡는다.
# 옛 도식의 데이터 최소화 줄도 뺐다.
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

W = 880
BY, BH, BW = 120, 96, 304
LX, RX = 16, 560
MX = 440
OY = BY + BH + 52
OH, OW = 56, 408
LEG = OY + OH + 76
H = LEG + 56

d = D(W, H, "01-05 · LAW AND DESIGN", "잊힐 권리와 불변 로그의 충돌",
      "법이 요구하는 삭제와 설계가 전제하는 추가 전용 기록이 같은 데이터를 두고 부딪힌다. 충돌이 열어 두는 두 질문이 새 엔지니어링 과제가 된다.",
      "삭제 요구와 불변 기록이 만나는 자리")

d.box(LX, BY, BW, BH, PAPER2, INFO, 1.2)
d.t(LX + BW / 2, BY + 40, "잊힐 권리", 16, INK, KR, "middle", 600)
d.t(LX + BW / 2, BY + 68, "GDPR", 13, MUTED, MONO, "middle")

d.box(RX, BY, BW, BH, PAPER2, INFO, 1.2)
d.t(RX + BW / 2, BY + 40, "불변 로그", 16, INK, KR, "middle", 600)
d.t(RX + BW / 2, BY + 68, "append-only", 13, MUTED, MONO, "middle")

cy = BY + BH / 2
d.arrow([(LX + BW + 4, cy), (MX - 40, cy)], MUTED, "ar", 1.6)
d.arrow([(RX - 4, cy), (MX + 40, cy)], MUTED, "ar", 1.6)
d.box(MX - 36, cy - 16, 72, 32, PAPER2, ACC, 1.6)
d.t(MX, cy + 5, "충돌", 14, ACC, KR, "middle", 600)

d.box(LX, OY, OW, OH, PAPER, RULE, 1.0)
d.t(LX + OW / 2, OY + 33, "파일 한가운데 삭제", 13, INK, KR, "middle")
d.box(W - 16 - OW, OY, OW, OH, PAPER, RULE, 1.0)
d.t(W - 16 - OW + OW / 2, OY + 33, "파생 데이터셋 삭제 · ML 학습 데이터", 13, INK, KR, "middle")

d.arrow([(MX, cy + 20), (MX, OY - 24)], MUTED, "ar", 1.4)
d.arrow([(LX + OW / 2, OY - 24), (LX + OW / 2, OY - 4)], MUTED, "ar", 1.4)
d.arrow([(W - 16 - OW / 2, OY - 24), (W - 16 - OW / 2, OY - 4)], MUTED, "ar", 1.4)
d.line(LX + OW / 2, OY - 24, W - 16 - OW / 2, OY - 24, MUTED, 1.4)

d.t(MX, OY + OH + 32, "새 엔지니어링 과제", 14, ACC, KR, "middle", 600)
d.legend(LEG, [("충돌 지점", ACC), ("충돌하는 요구", INFO)])
d.save("01-05.data-law-society.svg")
