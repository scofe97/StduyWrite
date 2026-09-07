# 타입 스펙: type-process — 평문이 왼쪽에서 들어가 오른쪽으로 나오는 한 방향 파이프라인.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2 Figure 8.2 (책 561쪽) —
#   평문·암호화 알고리즘·암호문·복호화 알고리즘·평문의 다섯 자리와 기호 K_A · K_B 는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 520
d = D(W, H, "SECTION 8.2 · CRYPTOGRAPHIC COMPONENTS",
      "알고리즘은 공개돼 있고 비밀은 열쇠에만 있습니다",
      "두 알고리즘 상자는 표준으로 출판돼 누구나 읽을 수 있다. 아래에서 꽂히는 열쇠 둘만 비밀이다.",
      "다섯 자리와 기호는 원문 Figure 8.2 의 것입니다")

BY, BH = 168, 84
STAGES = [(24, 168, "평문", "m", INK, False),
          (232, 200, "암호화 알고리즘", "공개 · 표준", INFO, False),
          (472, 176, "암호문", "K_A(m)", ACC, True),
          (688, 200, "복호화 알고리즘", "공개 · 표준", INFO, False),
          (928, 48, "평문", "m", INK, False)]
for x, w, name, sub, c, focal in STAGES:
    if focal:
        d.tone(x, BY, w, BH, c, 8, "18", 1.4)
    else:
        d.box(x, BY, w, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, BY + 34, name, 12, c, KR, "middle", 600)
    d.t(x + w / 2, BY + 58, sub, 11, MUTED, MONO)
for i in range(len(STAGES) - 1):
    x0 = STAGES[i][0] + STAGES[i][1]
    x1 = STAGES[i + 1][0]
    d.arrow([(x0 + 6, BY + BH / 2), (x1 - 6, BY + BH / 2)], MUTED, "ar", 1.4)

KY = BY + BH + 60
for x, w, key, who in ((232, 200, "K_A", "앨리스의 열쇠"), (688, 200, "K_B", "밥의 열쇠")):
    cx = x + w / 2
    d.tone(cx - 84, KY, 168, 56, OK, 6, "16", 1.3)
    d.t(cx, KY + 24, key, 13, OK, MONO, "middle", 600)
    d.t(cx, KY + 44, who, 11, MUTED, KR)
    d.arrow([(cx, KY - 6), (cx, BY + BH + 6)], OK, "ok", 1.4)

TY = 96
d.tone(472, TY, 176, 48, BAD, 6, "16", 1.3)
d.t(560, TY + 30, "트루디가 듣습니다", 11, BAD, KR)
d.arrow([(560, TY + 52), (560, BY - 6)], BAD, "bad", 1.3, "5 5")

NY = KY + 84
d.t(24, NY, "밥은 K_B(K_A(m)) = m 을 계산해 원래 평문을 얻습니다.", 12, INK, KR, "start", 600)
d.t(24, NY + 24, "대칭키 체계에서는 두 열쇠가 같고 둘 다 비밀입니다. 공개키 체계에서는 한쪽을 온 세상이 압니다.",
    11, MUTED, KR, "start")
d.legend(NY + 44, [("암호문", ACC), ("공개된 알고리즘", INFO), ("비밀인 열쇠", OK), ("침입자", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-01.crypto-components.svg"
d.save(out); print("→", out.name)
