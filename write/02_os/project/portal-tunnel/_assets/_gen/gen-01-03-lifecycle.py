# 타입 스펙: type-sequence — 참여자 넷(tunnel SDK · relay API · relay SNI · 브라우저), 등록·리버스 연결·SNI 클레임·갱신·해제 시퀀스.
# 사실 출처: docs/src/routes/architecture/+page.md Control Plane Flow §1~§4,
#   Mermaid tlsStreamDiagram(43~62행), sdk/api_client.go:146,161,221,239,270,
#   portal/api_server.go:324,384,423,447,468,518, portal/transport/reverse_framing.go:16,64.
import pathlib
import sys

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
        # 양방향 화살표용 좌측 마커 등록
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

W, H = 960, 820
d = SeqKR(W, H, "PORTAL-TUNNEL · CONTROL PLANE LIFECYCLE",
          "터널 생명주기 — 등록·리버스 연결·SNI 클레임·갱신·해제",
          "SDK가 relay API에 SIWE 서명으로 등록해 토큰과 capability를 받고, /sdk/connect로 리버스 연결을 미리 2개 열어 둡니다. 브라우저 ClientHello가 SNI 라우터에 들어오면 0x02와 바인딩으로 세션을 클레임해 종단간 TLS로 전환합니다.",
          "등록·사전 연결 풀링·SNI 클레임 활성화가 한 흐름으로 이어집니다")

NAMES = (
    ("tunnel (SDK)", "아웃바운드 에이전트"),
    ("relay API", "컨트롤 플레인 HTTP"),
    ("relay SNI", "데이터 플레인 인그레스"),
    ("브라우저", "공개 클라이언트")
)
d.LX = {"tunnel": 120, "api": 370, "sni": 620, "browser": 840}
KEYS = ["tunnel", "api", "sni", "browser"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 90, 100, 180, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, KR)

d.lane_top = 144
d.rails(H - 80)

# 1. Register Challenge
d.msg("tunnel", "api", "POST /sdk/register/challenge", 184, MUTED, "ar")
d.msg("api", "tunnel", "SIWE 챌린지 (nonce·statement)", 222, MUTED, "ar")

# 2. Local Sign
d.selfmsg("tunnel", "secp256k1 개인키 서명", 262, ACC, "personal_sign")

# 3. Register
d.msg("tunnel", "api", "POST /sdk/register (서명 전송)", 304, OK, "ok")
d.msg("api", "tunnel", "access_token + capability 발급", 342, OK, "ok", sub="호스트 라우트 등록")

# 4. Reverse Endpoint
d.msg("tunnel", "api", "POST /sdk/reverse", 384, MUTED, "ar")
d.msg("api", "tunnel", "reverse_endpoint 응답", 422, MUTED, "ar")

# 5. Reverse Connect (Pre-warm x2)
d.msg("tunnel", "api", "GET /sdk/connect (리버스 연결 x2)", 464, INFO, "info", sub="X-Portal-Reverse-Capability 헤더")
d.msg("api", "tunnel", "HTTP/1.1 101 Switching Protocols", 502, INFO, "info", sub="소켓 hijack · 대기 큐 등록")

# 6. Inbound Browser Request & Claim
d.msg("browser", "sni", "TLS ClientHello (SNI 호스트)", 546, WARN, "warn")
d.msg("sni", "tunnel", "0x02 + 16바이트 binding 전송", 588, ACC, "acc", sub="세션 클레임 · 활성화")
d.bi_msg("tunnel", "browser", "종단간 암호화 트래픽 (패스스루)", 630, OK)

# 7. Renew
d.msg("tunnel", "api", "POST /sdk/renew (임대 연장)", 672, MUTED, "ar", sub="기존 스트림 유지")

# 8. Unregister
d.msg("tunnel", "api", "POST /sdk/unregister (종료)", 714, BAD, "bad", sub="진행 브리지 즉시 취소")

d.legend(H - 52, [
    ("등록·통신", OK),
    ("서명·바인딩", ACC),
    ("리버스 풀", INFO),
    ("외부 요청", WARN),
    ("종료", BAD)
])

out_path = _HERE.parent / "01-03-lifecycle.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
