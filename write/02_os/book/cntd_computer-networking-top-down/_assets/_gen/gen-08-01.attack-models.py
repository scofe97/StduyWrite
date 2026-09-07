# 타입 스펙: type-nested — 바깥에서 안으로 갈수록 침입자가 쥔 것이 늘고, 안쪽은 바깥쪽을 품는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.1 (책 563쪽) —
#   세 시나리오의 이름과 정의, 그리고 원문이 든 예(bob·alice 짐작, quick brown fox)는 원문 그대로.
#   품음 관계는 정의에서 따라 나오는 노트의 읽기이며 본문에 그렇게 적었다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 588
d = D(W, H, "SECTION 8.2.1 · THREE ATTACK SCENARIOS",
      "쥔 것이 늘수록 안쪽으로 들어옵니다",
      "안쪽 상자는 바깥 상자가 가진 것을 이미 가지고 있다. 그래서 안으로 갈수록 깨기가 쉬워진다.",
      "세 시나리오의 이름과 예는 원문 §8.2.1 의 것입니다")

# 중첩 — 상자 안에는 이름만 둔다. 설명을 안에 넣으면 안쪽 상자와 겹친다.
BANDS = [
    (24, 144, 480, 300, "암호문 단독 공격", "ciphertext-only", INFO, 172, 190),
    (64, 200, 400, 188, "기지 평문 공격", "known-plaintext", WARN, 228, 246),
    (104, 256, 320, 76, "선택 평문 공격", "chosen-plaintext", ACC, 284, 302),
]
for x, y, w, h, name, en, c, ty, ey in BANDS:
    d.tone(x, y, w, h, c, 10, "22" if c is ACC else "10", 1.5 if c is ACC else 1.2)
    d.t(x + 20, ty, name, 13, c, KR, "start", 600)
    d.t(x + 20, ey, en, 10, SOFT, MONO, "start")
d.arrow([(264, 424), (264, 348)], SOFT, "soft", 1.3, "5 5")
d.t(264, 470, "침입자가 쥔 것이 늘어나는 방향", 11, SOFT, KR)

# 설명은 오른쪽에 색으로 잇는다
PX, PW = 540, 436
ROWS = [
    (INFO, "가로챈 암호문만 있고 평문 내용은 모릅니다.", "앞 절의 통계 분석이 여기서 쓰입니다."),
    (WARN, "평문과 암호문의 대응 일부를 압니다.", "bob 과 alice 가 있다는 짐작이 맞은 경우입니다."),
    (ACC, "평문을 골라 그 암호문을 얻습니다.", "the quick brown fox … 를 보내게 하면 됩니다."),
]
RY, RH, RS = 144, 76, 88
for i, (c, l1, l2) in enumerate(ROWS):
    y = RY + i * RS
    d.box(PX, y, PW, RH, PAPER2, RULE, 1.0, 7)
    d.tone(PX, y, 8, RH, c, 3, "88", 0)
    d.t(PX + 24, y + 30, l1, 11, INK, KR, "start")
    d.t(PX + 24, y + 52, l2, 11, MUTED, KR, "start")

NY = RY + 3 * RS + 8
d.box(PX, NY, PW, 84, PAPER2, RULE, 1.0)
d.t(PX + 20, NY + 28, "원문이 남긴 단서", 12, INK, KR, "start", 600)
d.t(PX + 20, NY + 54, "더 정교한 기법에서는 선택 평문 공격이 가능하다는 것이", 11, ACC, KR, "start")
d.t(PX + 20, NY + 72, "곧 깨진다는 뜻은 아닙니다. 블록 암호로 넘어가는 다리입니다.", 11, ACC, KR, "start")

d.legend(504, [("암호문만", INFO), ("대응 일부까지", WARN), ("평문을 고를 수 있음", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.attack-models.svg"
d.save(out); print("→", out.name)
