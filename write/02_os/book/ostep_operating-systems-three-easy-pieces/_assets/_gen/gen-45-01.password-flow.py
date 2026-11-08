# 45-01 「3. 솔트 붙은 느린 해시로 지키는 비밀번호」 — 사용자는 사이트 인증서로 공개 키를 얻어 ID·비밀번호를 암호화해 보내고, 사이트는 복호한 비밀번호에 저장된 솔트를 붙여 해시를 계산해 저장된 해시와 비교한다.
# 본문 근거: 이 노트 「비밀번호는 암호화한 통로로만 보낸다」 절.
# 값 근거: 2026-11-08 openssl 3.6.4 의 openssl passwd -6 -salt aaaaaaaa hunter2 가 $6$aaaaaaaa$n5EoGxOUiOpqF.… 를 두 번 같게 냈다. user1·hunter2 는 예시용 값이다.
# 공식 근거: NIST SP 800-63B-4 §3.1.1.2(암호화한 인증 통로로 요청하고, 솔트와 비용 계수를 쓰는 해시로 저장). OSTEP 57장 §57.2·§57.4.
# 타입 스펙: type-swimlane — 두 레인(사용자 쪽·사이트 쪽), 레인 사이 한 번의 전달.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 45-01 §3",
      "비밀번호는 암호화해 보내고 사이트는 솔트 붙은 해시로 비교한다",
      "위 레인은 사용자가 사이트 인증서를 확인해 공개 키를 얻고, user1 의 ID 와 비밀번호 hunter2 를 그 키로 암호화해 보내는 흐름이다. "
      "아래 레인은 사이트가 개인 키로 복호한 뒤 저장해 둔 솔트 aaaaaaaa 를 붙여 해시를 계산하고, 저장된 해시와 앞자리가 같은지 비교해 비밀번호를 아는 쪽임을 확인하는 흐름이다.",
      "사이트는 비밀번호 자체가 아니라 솔트와 해시를 저장합니다")

BW, BH, PITCH, X0 = 168, 76, 208, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def steps(y, x0, items):
    by = y + 40
    for i, (title, sub, c, fam) in enumerate(items):
        x = x0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == OK else 1.1)
        d.t(x + BW / 2, by + 32, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 12, MUTED, fam, "middle")
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "사용자 쪽")
steps(A_Y, X0, [
    ("사이트 인증서 확인", "server.crt: OK", SOFT, MONO),
    ("ID·비밀번호 암호화", "user1 · hunter2", INFO, MONO),
])
d.chip(600, A_Y + 52, "실제로는 TLS 통로 안에서 보냄", MUTED, 12)
d.chip(600, A_Y + 92, "도청자는 비밀번호를 읽지 못함", OK, 12)

lane(B_Y, "사이트 쪽")
x2 = X0 + PITCH
steps(B_Y, x2, [
    ("복호", "개인 키 사용", INFO, KR),
    ("솔트 붙여 해시", "salt = aaaaaaaa", INFO, MONO),
    ("저장된 해시와 비교", "n5EoGx… = n5EoGx…", OK, MONO),
])
# 레인 사이 전달
cx = x2 + BW / 2
d.arrow([(cx, A_Y + 40 + BH + 3), (cx, B_Y + 40 - 3)], MUTED, "ar", 1.4)
d.chip(cx + 74, B_Y + 22, "암호문 전송", MUTED, 12)
d.chip(x2 + 2 * PITCH + BW / 2, B_Y + 22, "확인되는 것은 이 메시지의 보낸 쪽", ACC, 12)

d.legend(392, [("보내는 쪽의 준비", SOFT), ("암호·해시 연산", INFO), ("통과", OK), ("한계 표시", ACC)])
d.save("45-01.password-flow.svg")
