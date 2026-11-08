# 45-01 「4. 메시지 하나에서 멈추는 인증」 — 사이트가 개인 키로 서명해 보낸 메시지는 서명이 맞지만, 공격자가 그 메시지를 복사해 두었다가 그대로 다시 보내도 받는 쪽은 서명 확인을 통과시키고 새것인지는 알지 못한다.
# 본문 근거: 이 노트 「복사해 다시 보내는 재전송 공격」 절.
# 값 근거: 개념 도식이라 값은 기호다. M 은 서명한 메시지, sig(M) 은 그 서명이다. 측정한 값을 싣지 않았다.
# 공식 근거: OSTEP 57장 §57.3 의 재전송 설명 — 개인 키로 암호화해 보낸 쪽은 사이트이고, 공개 키로 푸는 쪽이 사용자다. 매번 새 값으로 막는 방법은 짝 편(45-02)의 도전 응답이 다룬다.
# 타입 스펙: type-sequence — 참여자 셋(사이트 · 공격자 · 사용자)의 시간순 메시지. 정상 메시지, 복사, 재전송을 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, BAD, INFO, KR, MONO

W, H = 880, 524
LW, LH, LY = 180, 44, 96
X_C, X_A, X_S = 120, 440, 760
d = D(W, H, "OSTEP · 45-01 §4",
      "서명이 맞는 복사본을 다시 보내도 받는 쪽은 새것인지 모른다",
      "사이트가 개인 키로 서명한 메시지 M 과 그 서명 sig(M) 을 사용자에게 보내고 사용자가 공개 키로 서명을 확인한다. 이 메시지가 지나가는 길목의 공격자가 M 과 sig(M) 을 복사해 둔다. "
      "공격자가 같은 M 과 sig(M) 을 그대로 사용자에게 다시 보내면 서명이 맞으므로 확인을 통과하지만, 사용자는 이 메시지가 새것인지 알지 못한다. 막으려면 메시지마다 다른 값을 넣어야 한다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def msg(x1, x2, y, label, lx, c=INK, mk="ar", dash=None, sub=None):
    sgn = 1 if x2 > x1 else -1
    d.arrow([(x1 + 10 * sgn, y), (x2 - 12 * sgn, y)], c, mk, 1.5, dash)
    d.t(lx, y - 9, label, 12, c, kr(label), "middle", 600)
    if sub:
        d.t(lx, y + 18, sub, 12, MUTED, kr(sub))


for x, name, sub in ((X_C, "사이트", "개인 키로 서명해 보냄"), (X_A, "공격자", "길목에서 엿봄"), (X_S, "사용자", "공개 키로 서명을 확인")):
    d.box(x - LW / 2, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x, LY + 20, name, 13, INK, KR, "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, KR)
    d.line(x, LY + LH + 6, x, 468, RULE, 1.0, "3 6")

# 1. 정상 메시지
msg(X_C, X_S, 188, "M + sig(M)", 280, INFO, "info", None, "서명한 메시지")
# 2. 공격자가 복사
d.path(f"M {X_A + 10} 240 L {X_A + 58} 240 L {X_A + 58} 264 L {X_A + 13} 264", MUTED, 1.4, m="ar")
d.t(X_A + 68, 248, "M · sig(M) 복사", 12, MUTED, kr("복사"), "start", 600)
# 3. 사용자가 메시지대로 처리
d.chip(X_S, 320, "메시지대로 처리", MUTED, 12, 8)
# 4. 재전송
msg(X_A, X_S, 388, "M + sig(M) 그대로 재전송", 600, BAD, "bad", None, "복사본의 서명도 유효")
d.chip(X_S, 440, "서명 OK · 새것인지 모름", BAD, 12, 8)
d.chip(240, 440, "막는 방법: 메시지마다 다른 값", ACC, 12, 8)

d.legend(484, [("정상 메시지", INFO), ("복사한 재전송", BAD), ("사용자의 처리", SOFT), ("막는 방법", ACC)])
d.save("45-01.replay.svg")
