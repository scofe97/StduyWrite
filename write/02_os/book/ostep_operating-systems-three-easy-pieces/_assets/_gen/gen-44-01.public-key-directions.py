# 44-01 ### 2 — 공개 키 암호는 키를 쓰는 방향에 따라 다른 것을 준다. 개인 키로 만든 서명은 누구나 공개 키로 확인해 작성자를 증명하고, 공개 키로 만든 암호문은 개인 키를 가진 쪽만 읽어 내용을 숨긴다.
# 본문 근거: 이 노트 ### 2 「공개 키 암호는 키를 둘로 나눈다」.
# 검증 근거: openssl 3.6.4 로 RSA 2048 키 쌍을 만들어, 개인 키 서명은 공개 키로 Verified OK, 메시지를 바꾸면 Verification failure, 다른 키 쌍의 공개 키로도 failure. 공개 키로 암호화한 12바이트 평문은 개인 키로만 복호됨.
# 공식 근거: OSTEP 56장(Reiher) §56.3 — 개인 키로 암호화하면 인증, 공개 키로 암호화하면 비밀 통신.
# 타입 스펙: type-swimlane — 두 레인(개인 키를 쓰는 방향·공개 키를 쓰는 방향).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 44-01 §2",
      "개인 키로 만들면 인증, 상대 공개 키로 만들면 비밀",
      "위 레인은 보내는 쪽이 개인 키로 서명을 만들고 받는 쪽이 공개 키로 검증해 작성자를 확인하지만 내용은 숨기지 못하는 흐름이다. "
      "아래 레인은 보내는 쪽이 받는 쪽의 공개 키로 암호문을 만들고 받는 쪽이 개인 키로 복호해 내용은 숨기지만 보낸 사람은 확인하지 못하는 흐름이다.",
      "서명은 작성자를 증명하지만 내용을 숨기지 못하고, 공개 키 암호문은 내용을 숨기지만 보낸 사람을 확인하지 못한다")

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


lane(A_Y, "개인 키로 만드는 방향 — 인증")
lane_steps(A_Y, [
    ("보내는 쪽", "개인 키 보관", SOFT),
    ("서명 만들기", "개인 키 사용", INFO),
    ("받는 쪽", "공개 키로 검증", SOFT),
    ("확인되는 것", "작성자", OK),
])
d.chip(750, A_Y + 16, "내용은 숨겨지지 않음", ACC, 12)

lane(B_Y, "공개 키로 만드는 방향 — 비밀")
lane_steps(B_Y, [
    ("보내는 쪽", "상대 공개 키 사용", SOFT),
    ("암호문 만들기", "공개 키 사용", INFO),
    ("받는 쪽", "개인 키로 복호", SOFT),
    ("지켜지는 것", "내용", OK),
])
d.chip(750, B_Y + 16, "작성자는 확인 안 됨", ACC, 12)

d.legend(392, [("키를 보관하거나 쓰는 쪽", SOFT), ("키로 만드는 연산", INFO), ("얻는 성질", OK), ("얻지 못하는 성질", ACC)])
d.save("44-01.public-key-directions.svg")
