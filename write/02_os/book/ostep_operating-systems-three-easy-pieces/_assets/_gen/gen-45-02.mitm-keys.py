# 45-02 §2 — 서명 없는 Diffie-Hellman 에서 중간자가 양쪽에 자기 값을 보내면 클라이언트 키(6)와 서버 키(10)가 갈린다. 서버가 서명하면 클라이언트가 그 불일치를 알아챈다.
# 본문 근거: 이 노트 §2 「중간자와 서버의 서명」의 소절 「서명 없는 키 교환은 중간자에게 뚫린다」.
# 검증 근거: 2026-11-08 Python 3.14.4 로 작은 소수 n=23, g=5, 비밀 a=6, b=15, m1=3, m2=9 를 계산 —
#            A=8, B=19, M1=10, M2=11. 클라이언트 키 M1^a mod n = 6 = A^m1 mod n, 서버 키 M2^b mod n = 10 = B^m2 mod n, 정상 연결의 키 B^a = A^b = 2.
#            정답 4 의 실험과 같은 구조(클라이언트는 M1 을, 서버는 M2 를 받는다)이고 소수만 작게 바꿨다.
# 공식 근거: RFC 9846 §4.5.2 — 서명은 Transcript-Hash(Handshake Context, Certificate) 를 덮는다.
# 타입 스펙: type-sequence — 참여자 셋(클라이언트 · 중간자 · 서버)의 시간순 메시지. 틀로 서명이 없을 때와 서버가 서명할 때를 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, BAD, KR, MONO

W, H = 880, 632
LW, LH, LY = 216, 44, 96
X_C, X_M, X_S = 156, 440, 724
LANES = ((X_C, "클라이언트", "비밀 a = 6"), (X_M, "중간자", "비밀 m1 = 3 · m2 = 9"), (X_S, "서버", "비밀 b = 15"))
d = D(W, H, "OSTEP · 45-02 §2",
      "서명이 없으면 중간자는 양쪽과 따로 키를 나눈다",
      "작은 소수 n=23, g=5 로 계산한 예다. 클라이언트가 A=8 을 보내면 중간자가 가로채 자기 값 M2=11 을 서버에 보낸다. 서버가 B=19 로 답하면 중간자가 자기 값 M1=10 을 클라이언트에 보낸다. "
      "클라이언트 키는 6, 서버 키는 10 으로 서로 다르고 중간자는 둘 다 안다. 서버가 핸드셰이크 기록에 서명하면 M1 이 든 기록과 서명이 맞지 않아 클라이언트가 서명 검증에 실패한다.",
      "양쪽은 서로 키를 나눈 줄 알지만 키는 6 과 10 으로 다르다")


def msg(x1, x2, y, label, c=INK, mk="ar", dash=None, sub=None):
    sgn = 1 if x2 > x1 else -1
    d.arrow([(x1 + 10 * sgn, y), (x2 - 12 * sgn, y)], c, mk, 1.5, dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, KR if any("가" <= ch <= "힣" for ch in label) else MONO, "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 18, sub, 12, MUTED, KR)


def frame(y1, y2, name, w=96):
    d.o.append(f'<rect x="24" y="{y1}" width="832" height="{y2 - y1}" rx="4" fill="{INK}08" stroke="{SOFT}" stroke-width="0.9"/>')
    d.o.append(f'<rect x="24" y="{y1}" width="{w}" height="22" rx="2" fill="#0D1117" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(24 + w / 2, y1 + 16, name, 12, MUTED, KR, "middle", 600)


for x, name, sub in LANES:
    d.box(x - LW / 2, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x, LY + 20, name, 13, INK, KR, "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, KR)
    d.line(x, LY + LH + 6, x, H - 24, RULE, 1.0, "3 6")

# 서명이 없을 때
frame(160, 464, "서명 없음")
msg(X_C, X_M, 208, "A = 8", INK, "ar", None, "클라이언트가 g^a mod n 을 보냄")
msg(X_M, X_S, 268, "M2 = 11", ACC, "acc", None, "중간자가 자기 값으로 바꿔 보냄")
msg(X_S, X_M, 328, "B = 19", MUTED, "ar", "5 4", "서버가 g^b mod n 으로 답함")
msg(X_M, X_C, 388, "M1 = 10", ACC, "acc", "5 4", "중간자가 자기 값으로 바꿔 답함")
d.chip(X_C, 436, "키 6", INK, 12, 8)
d.chip(X_M, 436, "키 6 과 10 둘 다 앎", ACC, 12, 8)
d.chip(X_S, 436, "키 10", INK, 12, 8)

# 서버가 서명할 때
frame(480, 616, "서버가 서명", 108)
msg(X_M, X_C, 544, "M1 + 서버의 서명", MUTED, "ar", "5 4", "서명은 B 가 든 기록에 대한 것")
d.chip(X_C, 584, "서명 검증 실패", BAD, 12, 8)
d.chip(X_M, 584, "개인 키가 없어 새 서명 불가", MUTED, 12, 8)

d.save("45-02.mitm-keys.svg")
