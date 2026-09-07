# 타입 스펙: type-data-flow — 메시지가 갈라져 각각 다른 재료를 지나고 하나의 봉투로 합쳐진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.5.1 Figure 8.19 · 8.20 · 8.21 (책 587~590쪽) —
#   세션 키 절차 다섯 단계와 서명 절차 네 단계, 그리고 둘을 겹치는 순서는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 604
d = D(W, H, "SECTION 8.5.1 · SECURING E-MAIL",
      "세 성질이 각각 다른 재료에서 나옵니다",
      "기밀성은 세션 키가, 인증과 무결성은 서명이 만든다. 셋을 다 얻으려면 겹쳐 쓴다.",
      "두 절차와 겹치는 순서는 원문 Figure 8.19~8.21 의 것입니다")

d.t(24, 122, "예비 봉투 — 인증과 무결성", 12, INFO, KR, "start", 600)
A = [(24, "원문 m", "평문", INK), (216, "H(m)", "해시", INFO), (408, "K_A-(H(m))", "앨리스 개인키로 서명", INFO)]
for x, name, sub, c in A:
    d.box(x, 144, 176, 72, PAPER2, RULE, 1.0, 7)
    d.t(x + 88, 174, name, 12, c, MONO if "(" in name else KR, "middle", 600)
    d.t(x + 88, 196, sub, 11, MUTED, KR)
for a in (200, 392):
    d.arrow([(a + 2, 180), (a + 14, 180)], MUTED, "ar", 1.2)
d.tone(624, 144, 352, 72, INFO, 7, "16", 1.3)
d.t(800, 174, "원문 + 서명 = 예비 봉투", 12, INFO, KR, "middle", 600)
d.t(800, 196, "여기까지가 발신자 인증과 무결성입니다", 11, MUTED, KR)
d.arrow([(588, 180), (620, 180)], INFO, "info", 1.4)

d.line(24, 252, 976, 252, RULE, 0.8)
d.t(24, 284, "바깥 봉투 — 기밀성", 12, OK, KR, "start", 600)
B = [(24, "예비 봉투", "이것을 하나의 메시지로 취급", OK),
     (216, "K_S 로 암호화", "무작위 대칭 세션 키", OK),
     (408, "K_B+(K_S)", "밥의 공개키로 세션 키를", ACC)]
for x, name, sub, c in B:
    if c is ACC:
        d.tone(x, 308, 176, 72, c, 7, "18", 1.4)
    else:
        d.box(x, 308, 176, 72, PAPER2, RULE, 1.0, 7)
    d.t(x + 88, 338, name, 12, c, MONO if "(" in name else KR, "middle", 600)
    d.t(x + 88, 360, sub, 10, MUTED, KR)
for a in (200, 392):
    d.arrow([(a + 2, 344), (a + 14, 344)], MUTED, "ar", 1.2)
d.tone(624, 308, 352, 72, ACC, 7, "16", 1.3)
d.t(800, 338, "암호문 + 암호화된 세션 키", 12, ACC, KR, "middle", 600)
d.t(800, 360, "이것이 밥에게 갑니다", 11, MUTED, KR)
d.arrow([(588, 344), (620, 344)], ACC, "acc", 1.4)

PY = 412
d.box(24, PY, 470, 104, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "공개키를 두 번 씁니다", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 474, PY + 40, RULE, 0.8)
d.t(44, PY + 64, "앨리스: 자기 개인키로 한 번, 밥의 공개키로 한 번", 11, MUTED, KR, "start")
d.t(44, PY + 86, "밥: 자기 개인키로 한 번, 앨리스의 공개키로 한 번", 11, MUTED, KR, "start")

d.box(514, PY, 462, 104, PAPER2, RULE, 1.0)
d.t(534, PY + 28, "남는 문제", 12, INK, KR, "start", 600)
d.line(534, PY + 40, 956, PY + 40, RULE, 0.8)
d.t(534, PY + 64, "서로의 공개키를 어떻게 얻습니까. 트루디가 밥인 척하고", 11, MUTED, KR, "start")
d.t(534, PY + 86, "자기 공개키를 내밀 수 있습니다. 답은 CA 인증입니다.", 11, MUTED, KR, "start")

d.legend(536, [("문서", INK), ("서명 쪽", INFO), ("대칭 암호화 쪽", OK), ("공개키가 나르는 것", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.secure-email.svg"
d.save(out); print("→", out.name)
