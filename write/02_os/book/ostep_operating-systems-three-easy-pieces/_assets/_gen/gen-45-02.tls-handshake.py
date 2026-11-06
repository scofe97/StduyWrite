# 45-02 ### 1 — 클라이언트는 지원 목록과 키 교환 값을 보내고, 서버는 선택과 키 교환 값으로 답한 뒤 그 이후 메시지를 암호화해 인증서·서명을 보내며, 양쪽이 확인값을 주고받는다.
# 본문 근거: 이 노트 ### 1 「TLS 는 연결마다 새 대칭 키를 인증된 Diffie-Hellman 으로 만든다」.
# 검증 근거: openssl 3.6.4 s_client -msg 로 메시지 순서를 실측 — ClientHello, ServerHello, EncryptedExtensions, Certificate, CertificateVerify, Finished(서버), Finished(클라이언트).
# 공식 근거: RFC 9846 §2(핸드셰이크 세 단계: Key Exchange·Server Parameters·Authentication, "Everything after this phase is encrypted"), §4.4~§4.5. OSTEP 57장 §57.5.
# 타입 스펙: type-swimlane — 두 레인(클라이언트 쪽·서버 쪽), 레인 사이 세로 전달.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 440
d = D(W, H, "OSTEP · 45-02 §1",
      "TLS 핸드셰이크는 키 교환, 서버 매개변수, 인증의 세 단계로 흐른다",
      "클라이언트가 지원 목록과 키 교환 값을 보내면 서버가 선택한 값과 자기 키 교환 값으로 답하고, 이 뒤의 메시지는 암호화된다. "
      "서버는 이어서 서버 매개변수와 인증서와 서명과 확인값을 보내고, 클라이언트는 인증서와 서명을 확인한 뒤 자기 확인값을 보낸다.",
      "서버의 서명까지 확인해야 믿을 수 있는 통로가 서고, 비밀번호는 그 안에서 보냅니다")

BW, BH, PITCH, X0 = 148, 72, 172, 16
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
    if isinstance(sub, tuple):
        d.t(x + BW / 2, by + 24, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 44, sub[0], 12, MUTED, KR)
        d.t(x + BW / 2, by + 62, sub[1], 12, MUTED, KR)
    else:
        d.t(x + BW / 2, by + 30, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 52, sub, 12, MUTED, KR)
    return x + BW / 2, by


def hflow(col, y):
    x = X0 + col * PITCH
    d.path(f"M {x + BW + 2} {y + 40 + BH / 2} L {x + PITCH - 2} {y + 40 + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "클라이언트 쪽")
lane(B_Y, "서버 쪽")

a0x, a0y = box(0, A_Y, "지원 목록과 키 교환 값", "ClientHello", INFO)
b1x, b1y = box(1, B_Y, "선택과 키 교환 값", "ServerHello", INFO)
b2x, b2y = box(2, B_Y, "서버 매개변수", "EncryptedExtensions", SOFT)
b3x, b3y = box(3, B_Y, "인증서와 서명", ("Certificate", "CertificateVerify"), OK)
b4x, b4y = box(4, B_Y, "서버 확인값", "Finished", OK)
a3x, a3y = box(3, A_Y, "인증서·서명 확인", "미리 가진 CA 키", OK)
a4x, a4y = box(4, A_Y, "클라이언트 확인값", "Finished", OK)

# 클라이언트 → 서버 (ClientHello 에서 ServerHello 로, 레인 사이 틈으로 꺾어 내려감)
d.arrow([(a0x, a0y + BH + 3), (a0x, GAP_Y), (b1x, GAP_Y), (b1x, b1y - 3)], MUTED, "ar", 1.4)
# 서버 쪽 흐름
hflow(1, B_Y); hflow(2, B_Y); hflow(3, B_Y)
# 서버 → 클라이언트 (서명 확인, 확인값)
d.arrow([(b3x, b3y - 3), (b3x, a3y + BH + 3)], MUTED, "ar", 1.4)
d.arrow([(b4x, b4y - 3), (b4x, a4y + BH + 3)], MUTED, "ar", 1.4)
d.path(f"M {X0 + 3 * PITCH + BW + 2} {A_Y + 40 + BH / 2} L {X0 + 4 * PITCH - 2} {A_Y + 40 + BH / 2}", MUTED, 1.4, m="ar")

d.chip(b2x, B_Y + 22, "이 뒤의 메시지는 암호화", ACC, 12)
d.chip((X0 + 1 * PITCH + X0 + 2 * PITCH + BW) / 2, A_Y + 40 + BH / 2, "클라이언트는 비밀번호를 뒤에 보냄", ACC, 12)

d.legend(400, [("키 교환", INFO), ("서버 매개변수", SOFT), ("인증과 확인값", OK), ("핵심 전환", ACC)])
d.save("45-02.tls-handshake.svg")
