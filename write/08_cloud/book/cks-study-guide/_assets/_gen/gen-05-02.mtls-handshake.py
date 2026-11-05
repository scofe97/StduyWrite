# 05-02 §3 — mTLS 는 TLS 에 클라이언트 인증서 확인을 더해 양쪽이 서로의 신원을 확인한다.
# 본문 근거: 이 노트 ### 3 「3. mTLS 로 파드 사이 통신 지키기」.
# 검증 근거: 별도 실행 없음. 순서는 책의 mTLS 설명과 같은 책 container-security/11-01 의 TLS 핸드셰이크 도식
#            (서버가 요구하면 클라이언트 인증서 교환이 더해진다)을 따랐고, Istio 의 mTLS 모드는 PeerAuthentication 공식 레퍼런스로 대조.
# 타입 스펙: type-sequence — 두 파드 사이 메시지가 시간순으로 오가고, 확인 단계가 각 파드 안에서 일어난다.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 564
d = Seq(W, H, "CKS STUDY GUIDE · 05-02 §3",
        "mTLS 로 서로 확인하는 순서",
        "파드 A 가 파드 B 에 연결하면 B 가 자기 인증서와 A 의 인증서 요구를 함께 보내 A 가 CA 서명을 확인하고, "
        "A 가 인증서를 보내 B 가 같은 확인을 거친 뒤 암호화된 통신이 시작되는 순서를 두 파드 레인으로 그린 시퀀스 도식이다.",
        "서버만 증명하는 TLS 와 달리 mTLS 는 클라이언트도 증명해야 연결이 이어집니다")
LX = d.lanes([("파드 A", "클라이언트 · 인증서 보유"), ("파드 B", "서버 · 인증서 보유")], 104, 220)
d.rails(500)
A, B = LX["파드 A"], LX["파드 B"]


def msg(x1, x2, y, label, c=MUTED, mk="ar", sub=None):
    dr = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk)
    d.t((x1 + x2) / 2, y - 9, label, 12, c, KR, "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 18, sub, 11, MUTED, KR)


def check(x, y, label, c=INFO):
    w = 168
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 5, label, 12, INK, KR, "middle", 600)


msg(A, B, 196, "연결 요청")
msg(B, A, 252, "B 의 인증서 + A 의 인증서 요구", ACC, "acc", "B 의 신원과 공개키")
check(A, 304, "CA 서명 확인")
msg(A, B, 360, "A 의 인증서", ACC, "acc", "A 의 신원과 공개키")
check(B, 412, "CA 서명 확인")
msg(A, B, 468, "암호화된 통신", OK, "ok", "양쪽의 신원 확인 완료")

d.legend(516, [("TLS 에도 있는 단계", MUTED), ("mTLS 가 더하는 단계", ACC), ("확인 끝", OK)])
d.save("05-02.mtls-handshake.svg")
