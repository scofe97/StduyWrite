# 타입 스펙: type-sequence
# 사실 출처: docs/src/routes/keyless-tls/+page.md §Mermaid handshake,
#   portal/server.go:1026-1050, portal/keyless/client.go:140-153,
#   portal/keyless/signer.go:50-102, portal/keyless/bindings.go:32,69,
#   portal/transport/reverse_framing.go:16,64.
import pathlib
import sys
import os

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

    def bi_msg(s, a, b, label, y, c=OK):
        x1, x2 = s.LX[a], s.LX[b]
        s.o.append(f'<path d="M {x1 + 12} {y} L {x2 - 12} {y}" fill="none" stroke="{c}" stroke-width="1.5" marker-start="url(#ok_left)" marker-end="url(#ok)"/>')
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-8} L {x+46} {y-8} L {x+46} {y+8} L {x+13} {y+8}", c, 1.4, m="ar")
        s.t(x + 54, y - 2, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 54, y + 12, sub, 10, MUTED, _kr(sub), "start")

W, H = 960, 680
d = SeqKR(W, H, "PORTAL-TUNNEL · KEYLESS TLS HANDSHAKE",
          "Keyless TLS 핸드셰이크와 바인딩 서명 흐름",
          "브라우저의 ClientHello가 들어오면 Relay는 바인딩을 발급해 리버스 소켓으로 전달하고, Tunnel은 로컬에서 세션 키를 생성한 뒤 /v1/sign에서 단일 연결에 묶인 CertificateVerify 서명을 받아 핸드셰이크를 완성합니다.",
          "인증서 서명만 릴레이에 위임하고 트래픽 세션 키는 터널 내부에서 완성됩니다")

NAMES = (
    ("브라우저", "공개 클라이언트"),
    ("relay SNI", "인그레스 라우터"),
    ("relay /v1/sign", "온라인 서명기"),
    ("tunnel", "t13server 종단")
)
d.LX = {"browser": 120, "sni": 360, "signer": 600, "tunnel": 840}
KEYS = ["browser", "sni", "signer", "tunnel"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 84, 100, 168, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, KR)

d.lane_top = 144
d.rails(H - 72)

# 1. Browser ClientHello
d.msg("browser", "sni", "TLS ClientHello (SNI 호스트)", 184, INFO, "info")

# 2. Relay SNI Issue Binding
d.selfmsg("sni", "Issue(record.id, helloSpan)", 224, ACC, "16바이트 바인딩 생성")

# 3. Relay -> Tunnel: 0x02 + 16B binding over reverse connection
d.msg("sni", "tunnel", "0x02 + 16바이트 binding 전송", 270, OK, "ok", sub="리버스 연결 활성화")

# 4. Tunnel -> Browser: ServerHello (via SNI passthrough)
d.msg("tunnel", "browser", "ServerHello (ECDHE 키 교환)", 320, INFO, "info", sub="세션 키 터널 로컬 생성")

# 5. Tunnel -> Relay Signer: POST /v1/sign
d.msg("tunnel", "signer", "POST /v1/sign", 374, ACC, "acc", sub="핸드셰이크 원문 + binding + lease 토큰")

# 6. Relay Signer ValidateAndConsume
d.selfmsg("signer", "ValidateAndConsume", 418, WARN, "lease·hello 검증 및 1회성 소모")

# 7. Relay Signer -> Tunnel: CertificateVerify signature
d.msg("signer", "tunnel", "CertificateVerify 서명 응답", 468, OK, "ok")

# 8. Tunnel -> Browser: CertificateVerify + Finished
d.msg("tunnel", "browser", "CertificateVerify + Finished", 522, INFO, "info", sub="테넌트 TLS 핸드셰이크 완료")

# 9. Application Data
d.bi_msg("browser", "tunnel", "E2E TLS 암호문 전송 (바이너리 패스스루)", 576, OK)

# 범례
d.legend(632, [
    ("브라우저-터널 핸드셰이크", INFO),
    ("바인딩 및 활성화", OK),
    ("원격 서명 요청", ACC),
    ("검증 및 소모", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-03-keyless-sequence.svg"))
d.save(out)
print(f"saved: {out}")
