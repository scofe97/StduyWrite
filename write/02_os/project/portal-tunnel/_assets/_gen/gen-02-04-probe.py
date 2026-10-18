# 타입 스펙: type-sequence
# 사실 출처: sdk/mitm.go:25-65,125-231,348-449,
#   docs/src/routes/security-model/+page.md §MITM Self-Probe,
#   RFC 5705, RFC 8446 §7.5.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 14

class SeqProbe(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')
        s.o.insert(20, f'<marker id="bad_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{BAD}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        actual_mk = mk if mk != "ar" else ("ok" if c == OK else ("bad" if c == BAD else ("info" if c == INFO else "ar")))
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.4, m=actual_mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 10, MUTED, _kr(sub))

    def bi_msg(s, a, b, label, y, c=OK, mk_l="ok_left", mk_r="ok"):
        x1, x2 = s.LX[a], s.LX[b]
        s.o.append(f'<path d="M {x1 + 12} {y} L {x2 - 12} {y}" fill="none" stroke="{c}" stroke-width="1.4" marker-start="url(#{mk_l})" marker-end="url(#{mk_r})"/>')
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)

    def selfmsg(s, a, label, y, c=MUTED, sub=None, to_left=False):
        x = s.LX[a]
        dx = -46 if to_left else 46
        dd = -1 if to_left else 1
        mk = "ok" if c == OK else ("bad" if c == BAD else ("info" if c == INFO else "ar"))
        s.path(f"M {x + 10*dd} {y-8} L {x + dx} {y-8} L {x + dx} {y+8} L {x + 13*dd} {y+8}", c, 1.3, m=mk)
        tx = x + dx + (-8 if to_left else 8)
        anch = "end" if to_left else "start"
        s.t(tx, y - 2, label, 11, c, _kr(label), anch, 600)
        if sub:
            s.t(tx, y + 12, sub, 10, MUTED, _kr(sub), anch)

W, H = 960, 780
d = SeqProbe(
    W, H,
    "PORTAL-TUNNEL · MITM SELF-PROBE SEQUENCE",
    "중간자 자가 프로브 — 정직한 패스스루와 악의적 종단 대조",
    "클라이언트와 응답 수신부가 TLS exporter 값을 비교해 릴레이의 무단 종단을 검증합니다.",
    "정직한 중계(상단)는 세션이 하나여서 값이 같고, MITM 종단(하단)은 세션이 갈라져 값이 다릅니다"
)

NAMES = (
    ("tunnel (프로브 발신)", "probeTLSPassthrough"),
    ("relay (SNI 라우터)", "정직 중계 / MITM 종단"),
    ("tunnel (응답 수신)", "maybeHandleConn")
)
KEYS = ["probe", "relay", "responder"]
d.LX = {"probe": 140, "relay": 480, "responder": 820}

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 95, 96, 190, 44, PAPER2, RULE, 1.0)
    d.t(x, 116, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 132, sub, 10, MUTED, MONO)

d.lane_top = 140
d.rails(H - 60)

# 구획 박스: 케이스 1 (정직한 릴레이)
d.box(16, 154, W - 32, 260, fill="rgba(63,185,140,0.03)", stroke=OK, sw=0.9, r=6)
d.t(28, 174, "CASE 1: 정직한 릴레이 (TLS 바이너리 패스스루)", 11, OK, KR, "start", 600)

d.msg("probe", "relay", "1. TCP 연결 + reserveProbe(nonce)", 198, INFO, "info")
d.bi_msg("probe", "responder", "2. 단일 TLS 1.3 핸드셰이크 (패스스루)", 240, OK)
d.selfmsg("probe", "ExportKeyingMaterial (32B) -> E1", 280, OK, sub="Portal-MITM-Probe-v1")
d.msg("probe", "responder", "3. 16B nonce + 패딩(96~320B)", 322, MUTED, "ar")
d.selfmsg("responder", "ExportKeyingMaterial (32B) -> E1", 362, OK, sub="Peek(16) 확인 후 계산", to_left=True)
d.chip(W / 2, 394, "판정: E1 == E1 일치 -> 검증 통과 (패스스루)", OK, 11, 10)

# 구획 박스: 케이스 2 (악의적 릴레이)
d.box(16, 434, W - 32, 280, fill="rgba(240,97,109,0.03)", stroke=BAD, sw=0.9, r=6)
d.t(28, 454, "CASE 2: 악의적 릴레이 (중간자 TLS 종단 및 재암호화)", 11, BAD, KR, "start", 600)

d.msg("probe", "relay", "1. TCP 연결 + reserveProbe(nonce)", 478, INFO, "info")
d.bi_msg("probe", "relay", "2a. TLS 세션 A 종단 (복호화)", 518, WARN, mk_l="warn", mk_r="warn")
d.bi_msg("relay", "responder", "2b. TLS 세션 B 수립 (재암호화)", 518, WARN, mk_l="warn", mk_r="warn")
d.selfmsg("probe", "세션 A Exporter -> E_A (0x8F...)", 562, BAD, sub="비밀 키 A 도출")
d.msg("probe", "responder", "3. 프레임 중계 (평문 노출 위험)", 604, BAD, "bad", dash="4 3")
d.selfmsg("responder", "세션 B Exporter -> E_B (0x3C...)", 646, BAD, sub="비밀 키 B 도출", to_left=True)
d.chip(W / 2, 686, "판정: E_A != E_B 불일치 -> MITM 적발 (--ban-mitm 시 차단)", BAD, 11, 10)

p = str(_HERE.parent / "02-04-probe.svg")
d.save(p)
print(f"saved: {p}")
