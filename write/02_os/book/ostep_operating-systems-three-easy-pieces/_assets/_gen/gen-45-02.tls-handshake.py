# 45-02 §3 — 클라이언트가 지원 목록과 키 교환 값을 보내고, 서버가 선택과 키 교환 값으로 답한 뒤 그 이후 메시지를 암호화해 인증서와 서명을 보내며, 양쪽이 확인값을 주고받는다.
# 본문 근거: 이 노트 §3 「핸드셰이크 세 단계와 클라이언트 인증」의 소절 「세 단계로 나뉜 핸드셰이크」.
# 검증 근거: 2026-11-08 openssl 3.6.4 s_client -msg 로 메시지 순서를 실측 — ClientHello, ServerHello, EncryptedExtensions, Certificate, CertificateVerify, Finished(서버), Finished(클라이언트).
#            협상값 TLSv1.3 · TLS_AES_256_GCM_SHA384 · 그룹 X25519MLKEM768 은 같은 실측의 출력(정답 3 과 각주 grp).
# 공식 근거: RFC 9846 §2(핸드셰이크 세 단계 Key Exchange·Server Parameters·Authentication, "Everything after this phase is encrypted"), §4.5.2(CertificateVerify).
# 타입 스펙: type-sequence — 참여자 둘(클라이언트 · 서버)의 시간순 메시지. 틀로 세 단계를 가르고 점선 경계로 암호화가 시작되는 자리를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, INFO, KR, MONO

W, H = 880, 732
LW, LH, LY = 200, 44, 96
X_C, X_S = 140, 740
d = D(W, H, "OSTEP · 45-02 §3",
      "핸드셰이크는 키 교환 뒤부터 암호화되고 서버의 서명으로 인증한다",
      "클라이언트가 ClientHello 로 지원 목록과 키 교환 값을 보내면 서버가 ServerHello 로 고른 암호 모음과 자기 키 교환 값을 답한다. 여기까지가 키 교환 단계이고 이 뒤의 메시지는 암호화된다. "
      "서버 매개변수 단계에서 서버가 EncryptedExtensions 를 보내고, 인증 단계에서 Certificate 와 CertificateVerify 와 Finished 를 보낸다. 클라이언트가 자기 Finished 를 보내면 끝난다. "
      "협상된 값은 TLS 1.3 이고 암호 모음은 TLS_AES_256_GCM_SHA384 이며 키 교환 그룹은 X25519MLKEM768 이다.",
      "서버만 서명하고, 클라이언트는 이 통로가 선 뒤에 비밀번호를 보낸다")


def msg(x1, x2, y, label, c=INK, mk="ar", dash=None, sub=None):
    sgn = 1 if x2 > x1 else -1
    d.arrow([(x1 + 10 * sgn, y), (x2 - 12 * sgn, y)], c, mk, 1.5, dash)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, MONO, "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 18, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def frame(y1, y2, name, w=84):
    d.o.append(f'<rect x="24" y="{y1}" width="832" height="{y2 - y1}" rx="4" fill="{INK}08" stroke="{SOFT}" stroke-width="0.9"/>')
    d.o.append(f'<rect x="24" y="{y1}" width="{w}" height="22" rx="2" fill="#0D1117" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(24 + w / 2, y1 + 16, name, 12, MUTED, KR, "middle", 600)


for x, name, sub in ((X_C, "클라이언트", "브라우저 · s_client"), (X_S, "서버", "인증서와 개인 키 보유")):
    d.box(x - LW / 2, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x, LY + 20, name, 13, INK, KR, "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, KR)
    d.line(x, LY + LH + 6, x, H - 24, RULE, 1.0, "3 6")

# 1 키 교환
frame(160, 304, "키 교환")
msg(X_C, X_S, 208, "ClientHello", INK, "ar", None, "supported_groups · key_share")
msg(X_S, X_C, 268, "ServerHello", INK, "ar", None, "TLS_AES_256_GCM_SHA384 · key_share")
d.line(24, 320, 856, 320, ACC, 1.0, "5 4")
d.chip(440, 320, "여기서부터 암호화", ACC, 12, 8)

# 2 서버 매개변수
frame(336, 412, "서버 매개변수", 108)
msg(X_S, X_C, 384, "EncryptedExtensions", MUTED, "ar", "5 4")

# 3 인증
frame(428, 712, "인증", 52)
msg(X_S, X_C, 476, "Certificate", MUTED, "ar", "5 4", "서버의 공개 키가 든 인증서")
msg(X_S, X_C, 536, "CertificateVerify", ACC, "acc", "5 4", "핸드셰이크 기록에 개인 키로 서명")
msg(X_S, X_C, 596, "Finished", MUTED, "ar", "5 4", "확인값")
msg(X_C, X_S, 656, "Finished", MUTED, "ar", "5 4", "확인값")
d.chip(X_C, 696, "비밀번호는 이 뒤에", OK, 12, 8)

d.save("45-02.tls-handshake.svg")
