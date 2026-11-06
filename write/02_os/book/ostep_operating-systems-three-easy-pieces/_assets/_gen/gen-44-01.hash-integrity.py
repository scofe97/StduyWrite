# 44-01 ### 3 — 보내는 쪽은 평문의 암호 해시를 만들어 해시만 암호화한 뒤 평문과 함께 보내고, 받는 쪽은 해시를 복호하고 받은 평문의 해시를 다시 계산해 둘을 비교해 변조를 알아챈다.
# 본문 근거: 이 노트 ### 3 「암호 해시는 키 없이 지문을 만든다」.
# 검증 근거: openssl 3.6.4 로 'Transfer $100 ...' 과 '$101' 두 문장의 SHA-256 을 계산해 256비트 중 126비트가 달라짐을 확인. 서명한 문장을 바꾸면 Verification failure.
# 공식 근거: OSTEP 56장(Reiher) §56.4 및 각주 2 — 해시를 암호화하지 않으면 공격자가 메시지를 바꾸고 새 해시를 계산해 둘을 함께 바꿔치기한다.
# 타입 스펙: type-swimlane — 두 레인(보내는 쪽·받는 쪽), 아래 레인은 오른쪽에서 왼쪽으로 읽는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 44-01 §3",
      "해시만 암호화해 보내면 평문을 바꾼 흔적이 비교에서 드러난다",
      "위 레인은 보내는 쪽이 평문 P 의 암호 해시 S 를 계산해 S 만 암호화하고 P 와 함께 보내는 흐름이다. "
      "아래 레인은 오른쪽에서 왼쪽으로 읽으며 받는 쪽이 암호화된 S 를 복호하고 받은 P 에서 해시를 다시 계산해 두 값이 같은지 비교하는 흐름이다. 값이 다르면 변조로 본다.",
      "해시를 암호화해야 공격자가 평문과 해시를 함께 바꿔치기하지 못한다")

BW, BH, PITCH, X0 = 160, 76, 208, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def box(x, y, title, sub, c):
    d.tone(x, y, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, y + 32, title, 12.5, INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 56, sub, 12, MUTED, KR)


lane(A_Y, "보내는 쪽")
a = [("평문 P", "보낼 내용", SOFT), ("해시 S = H(P)", "키 없이 계산", INFO),
     ("S 만 암호화", "키 사용", INFO), ("P 와 암호화된 S", "함께 전송", ACC)]
for i, (t, s, c) in enumerate(a):
    x = X0 + i * PITCH
    box(x, A_Y + 40, t, s, c)
    if i < 3:
        d.path(f"M {x + BW + 2} {A_Y + 40 + BH / 2} L {x + PITCH - 2} {A_Y + 40 + BH / 2}", MUTED, 1.4, m="ar")

lane(B_Y, "받는 쪽 (오른쪽에서 왼쪽으로)")
b = [("S 복호", "키 사용", INFO), ("받은 P 로 H 계산", "S' 를 얻음", INFO),
     ("S 와 S' 비교", "같은지 확인", SOFT), ("다르면 변조", "P 를 믿지 않음", OK)]
for i, (t, s, c) in enumerate(b):
    x = X0 + (3 - i) * PITCH
    box(x, B_Y + 40, t, s, c)
    if i < 3:
        d.path(f"M {x - 2} {B_Y + 40 + BH / 2} L {x - PITCH + BW + 2} {B_Y + 40 + BH / 2}", MUTED, 1.4, m="ar")

# 보내는 쪽 마지막 상자에서 받는 쪽 첫 상자로 내려오는 전송 화살표
tx = X0 + 3 * PITCH + BW / 2
d.path(f"M {tx} {A_Y + 40 + BH + 2} L {tx} {B_Y + 40 - 2}", ACC, 1.6, m="acc")
d.chip(690, A_Y + 16, "아래 화살표 구간에서 P 가 바뀔 수 있음", ACC, 12)

d.legend(392, [("평문과 전송물", SOFT), ("키가 쓰이는 단계", INFO), ("전송 구간", ACC), ("변조를 걸러내는 결과", OK)])
d.save("44-01.hash-integrity.svg")
