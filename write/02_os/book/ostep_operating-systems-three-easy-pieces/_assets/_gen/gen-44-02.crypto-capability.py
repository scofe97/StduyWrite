# 44-02 ### 4 — 발급자가 권한·대상·만료를 담은 구조에 비밀 키로 서명해 사용자에게 주고, 자원 쪽은 서명을 검증해 접근 목록 없이 허용한다. 사용자가 권한 칸을 고치면 서명이 맞지 않아 거절된다.
# 본문 근거: 이 노트 ### 4 「암호학적 capability 는 서명으로 위조를 막는다」.
# 검증 근거: openssl 3.6.4 로 'user=...;res=...;rights=read;exp=...' 에 HMAC-SHA256 태그를 붙여 ACCEPT, rights=write 나 user 를 바꾸면 REJECT. 같은 구조를 RSA 개인 키로 서명하면 공개 키만으로 Verified OK, 바꾸면 Verification failure.
# 공식 근거: OSTEP 56장(Reiher) §56.8, RFC 7519 — 클레임을 서명이나 MAC 으로 보호해 전달하는 JSON Web Token.
# 타입 스펙: type-swimlane — 두 레인(정상 사용·위조 시도).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 44-02 §4",
      "서명이 붙은 권한 구조는 고치면 검증에서 거절된다",
      "위 레인은 발급자가 권한 구조에 서명해 사용자에게 주고, 사용자가 자원 쪽에 내밀면 서명이 맞아 접근이 허용되는 흐름이다. "
      "아래 레인은 사용자가 권한 칸을 직접 고쳐 내밀면 서명이 맞지 않아 접근이 거절되는 흐름이다. 두 경우 모두 자원 쪽은 접근 목록을 따로 보관하지 않는다.",
      "자원 쪽은 서명만 검증하고 사용자별 상태는 들고 있지 않는다")

BW, BH, PITCH, X0 = 160, 76, 208, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 12, MUTED, KR)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "정상 사용")
lane_steps(A_Y, [
    ("발급자", "권한 구조에 서명", INFO),
    ("사용자", "구조를 들고 있음", SOFT),
    ("자원 쪽", "서명을 검증", INFO),
    ("접근 허용", "접근 목록 불필요", OK),
])

lane(B_Y, "위조 시도")
lane_steps(B_Y, [
    ("사용자", "권한 칸을 고침", ACC),
    ("자원 쪽", "서명을 검증", INFO),
    ("서명 불일치", "고친 내용과 안 맞음", INFO),
    ("접근 거절", "구조를 믿지 않음", OK),
])

d.legend(392, [("서명하거나 검증하는 단계", INFO), ("구조를 들고 있는 쪽", SOFT), ("허용·거절 결과", OK), ("위조가 일어나는 지점", ACC)])
d.save("44-02.crypto-capability.svg")
