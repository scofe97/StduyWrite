# 타입 스펙: type-data-flow — 문서가 두 갈래로 흘러 한쪽은 서명이 되고, 받는 쪽에서 두 갈래가 다시 만난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.3.3 Figure 8.11 · Figure 8.12 (책 579쪽) —
#   해시에 서명한다는 것, 평문과 서명을 함께 보낸다는 것, 두 해시를 맞춰 본다는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 616
d = D(W, H, "SECTION 8.3.3 · CREATING AND VERIFYING A SIGNATURE",
      "문서가 아니라 해시에 서명합니다",
      "문서 전체를 개인키로 처리하면 비싸다. 해시가 훨씬 짧으므로 그것만 서명한다.",
      "두 흐름은 원문 Figure 8.11 과 8.12 의 것입니다")

d.t(24, 122, "밥이 만듭니다", 12, OK, KR, "start", 600)
SEND = [(24, 148, "원문 m", "평문 그대로", INK),
        (232, 148, "해시 H(m)", "고정 길이 지문", INFO),
        (440, 148, "K_B-(H(m))", "개인키로 서명", ACC)]
for x, y, name, sub, c in SEND:
    if c is ACC:
        d.tone(x, y, 176, 76, c, 7, "18", 1.4)
    else:
        d.box(x, y, 176, 76, PAPER2, RULE, 1.0, 7)
    d.t(x + 88, y + 32, name, 12, c, KR if "해시" in name or "원문" in name else MONO, "middle", 600)
    d.t(x + 88, y + 54, sub, 11, MUTED, KR)
for a, b in ((200, 232), (408, 440)):
    d.arrow([(a + 2, 186), (b - 4, 186)], MUTED, "ar", 1.3)

d.tone(672, 148, 280, 76, OK, 7, "14", 1.3)
d.t(812, 180, "평문 m 과 서명을 함께 보냅니다", 11, OK, KR)
d.t(812, 202, "서명한 다이제스트가 곧 디지털 서명입니다", 10, SOFT, KR)
d.arrow([(618, 186), (668, 186)], OK, "ok", 1.4)

d.line(24, 268, 976, 268, RULE, 0.8)
d.t(24, 300, "앨리스가 확인합니다", 12, INFO, KR, "start", 600)
VER = [(24, 328, "받은 서명", "K_B-(H(m))", ACC, 0),
       (232, 328, "밥의 공개키 적용", "→ 해시 하나", INFO, 0),
       (24, 428, "받은 평문 m", "그대로", INK, 1),
       (232, 428, "해시 함수 적용", "→ 해시 하나", INFO, 1)]
for x, y, name, sub, c, _ in VER:
    d.box(x, y, 176, 72, PAPER2, RULE, 1.0, 7)
    d.t(x + 88, y + 30, name, 12, c, KR, "middle", 600)
    d.t(x + 88, y + 52, sub, 11, MUTED, MONO if "→" in sub else KR)
d.arrow([(202, 364), (228, 364)], MUTED, "ar", 1.3)
d.arrow([(202, 464), (228, 464)], MUTED, "ar", 1.3)

d.tone(472, 356, 200, 116, ACC, 8, "18", 1.4)
d.t(572, 400, "두 해시가 같습니까", 12, ACC, KR, "middle", 600)
d.t(572, 428, "같으면 무결성과", 11, MUTED, KR)
d.t(572, 448, "작성자를 함께 확인", 11, MUTED, KR)
d.path("M 412 364 L 444 364 L 444 400 L 468 400", INFO, 1.4, m="info")
d.path("M 412 464 L 444 464 L 444 428 L 468 428", INFO, 1.4, m="info")

d.box(704, 356, 272, 116, PAPER2, RULE, 1.0)
d.t(724, 384, "왜 MAC 으로는 안 되나", 12, INK, KR, "start", 600)
d.line(724, 396, 956, 396, RULE, 0.8)
d.t(724, 420, "MAC 을 검증하려면 앨리스도", 11, MUTED, KR, "start")
d.t(724, 440, "같은 열쇠를 가져야 합니다.", 11, MUTED, KR, "start")
d.t(724, 460, "그러면 밥만의 것이 아닙니다.", 11, ACC, KR, "start")

d.legend(524, [("문서와 평문", INK), ("해시 연산", INFO), ("개인키가 만든 것", ACC), ("보내는 묶음", OK)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.digital-signature.svg"
d.save(out); print("→", out.name)
