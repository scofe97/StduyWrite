# 45-02 ### 2 — 확인하는 쪽이 매번 다른 도전값을 보내면 증명하는 쪽이 비밀과 도전값으로 응답을 계산해 보내고, 확인하는 쪽이 같은 계산으로 비교한다. 지난 응답은 새 도전값에서 거부된다.
# 본문 근거: 이 노트 ### 2 「로그인 뒤의 인증은 쿠키·도전 응답·인증 서버가 나눠 맡는다」.
# 검증 근거: HMAC-SHA256 으로 도전값 7731·9042 의 응답이 다르고, 새 도전값 9042 에 옳은 응답은 ACCEPT, 지난 응답은 REJECT. 키는 파일에서 읽고 출력하지 않음.
# 공식 근거: RFC 2104(HMAC). OSTEP 57장 §57.6.
# 타입 스펙: type-swimlane — 두 레인(확인하는 쪽·증명하는 쪽), 레인 사이 꺾인 전달.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 440
d = D(W, H, "OSTEP · 45-02 §2",
      "도전 응답은 매번 다른 도전값으로 지난 응답의 재사용을 막는다",
      "확인하는 쪽이 매번 다른 도전값을 보내면 증명하는 쪽은 미리 나눠 가진 비밀과 도전값으로 응답을 계산해 돌려준다. "
      "확인하는 쪽은 같은 비밀로 같은 계산을 해서 응답을 비교하고, 지난번 응답은 새 도전값에 맞지 않아 거부된다.",
      "도청자가 도전값과 응답을 모아도 새 도전값에 쓸 응답은 얻지 못합니다")

BW, BH, PITCH, X0 = 168, 72, 208, 24
LANE_X, LANE_W, LANE_H = 12, 856, 128
A_Y, B_Y = 96, 244
GAP_Y = 234


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def box(col, y, title, sub, c):
    x = X0 + col * PITCH
    by = y + 40
    d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == OK else 1.1)
    d.t(x + BW / 2, by + 30, title, 12.5, INK, KR, "middle", 600)
    d.t(x + BW / 2, by + 52, sub, 12, MUTED, KR)
    return x + BW / 2, by


lane(A_Y, "확인하는 쪽")
lane(B_Y, "증명하는 쪽")

a0x, a0y = box(0, A_Y, "새 도전값 선택", "매번 다른 숫자", SOFT)
b1x, b1y = box(1, B_Y, "응답 계산", "비밀과 도전값의 HMAC", INFO)
a2x, a2y = box(2, A_Y, "같은 계산으로 비교", "같은 비밀 사용", INFO)
a3x, a3y = box(3, A_Y, "통과 또는 거부", "지난 응답은 거부", OK)

# 도전값 전송: 확인하는 쪽 → 증명하는 쪽 (틈에서 꺾음)
d.arrow([(a0x, a0y + BH + 3), (a0x, GAP_Y), (b1x - 30, GAP_Y), (b1x - 30, b1y - 3)], MUTED, "ar", 1.4)
# 응답 전송: 증명하는 쪽 → 확인하는 쪽
d.arrow([(b1x + 30, b1y - 3), (b1x + 30, GAP_Y + 4), (a2x, GAP_Y + 4), (a2x, a2y + BH + 3)], MUTED, "ar", 1.4)
d.path(f"M {X0 + 2 * PITCH + BW + 2} {A_Y + 40 + BH / 2} L {X0 + 3 * PITCH - 2} {A_Y + 40 + BH / 2}", MUTED, 1.4, m="ar")

d.chip(a0x + 90, B_Y + 22, "도전값 전송", MUTED, 12)
d.chip(b1x + 150, B_Y + 22, "응답 전송", MUTED, 12)
d.chip((X0 + BW + X0 + 2 * PITCH) / 2, A_Y + 40 + BH / 2, "암호화 없이 보내도 됨", ACC, 12)

d.legend(400, [("확인하는 쪽의 선택", SOFT), ("비밀을 쓰는 계산", INFO), ("통과 또는 거부", OK), ("전송 방식", ACC)])
d.save("45-02.challenge-response.svg")
