# 타입 스펙: type-sequence — 참여자 셋(relay ACME 매니저 · DNS Provider · ACME CA), 와일드카드 인증서 발급·DNS-01 검증·갱신 시퀀스.
# 사실 출처: RFC 8555 §8.4, portal/acme/acme.go:127,186,264, portal/acme/certificate.go:41,84,
#   portal/acme/maintenance.go:44,210, portal/acme/embedded/provider.go:194, portal/acme/cloudflare/provider.go:87.
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

    def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x-10} {y-8} L {x-46} {y-8} L {x-46} {y+8} L {x-13} {y+8}", c, 1.4, m="ar")
        s.t(x - 54, y - 2, label, 11, c, _kr(label), "end", 600)
        if sub:
            s.t(x - 54, y + 12, sub, 10, MUTED, _kr(sub), "end")

W, H = 960, 780
d = SeqKR(W, H, "PORTAL-TUNNEL · ACME DNS-01 ISSUANCE & RENEWAL",
          "ACME DNS-01 발급과 갱신 — 주문·TXT 게시·검증·원자적 저장",
          "릴레이 매니저가 lego 클라이언트를 통해 와일드카드 주문을 넣고, DNS 제공자에 TXT 챌린지를 게시한 뒤 CA 검증을 거쳐 인증서를 발급받아 저장하며 백그라운드 루프가 갱신을 관리합니다.",
          "DNS-01 챌린지 검증을 거쳐 와일드카드 인증서를 발급받고 주기적으로 갱신합니다")

NAMES = (
    ("relay ACME 매니저", "portal/acme (lego)"),
    ("DNS Provider", "API 제공자 또는 embedded DNS"),
    ("ACME CA", "Let's Encrypt")
)
d.LX = {"manager": 150, "dns": 500, "ca": 810}
KEYS = ["manager", "dns", "ca"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 110, 100, 220, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, KR, "middle", 600)
    d.t(x, 136, sub, 10, MUTED, KR)

d.lane_top = 144
d.rails(H - 80)

# 1. ACME Order
d.msg("manager", "ca", "주문 요청 (root, *.root)", 184, INFO, "info", sub="client.Certificate.Obtain")
d.msg("ca", "manager", "DNS-01 챌린지 (토큰·키 인가)", 224, INFO, "info", sub="keyAuth 계산")

# 2. Publish TXT Record
d.msg("manager", "dns", "TXT 레코드 게시 요청", 268, ACC, "acc", sub="_acme-challenge.<root>")
d.selfmsg("dns", "TXT 레코드 등록", 308, ACC, sub="API 호출 또는 인메모리 존 갱신")

# 3. Challenge Ready & CA Validation
d.msg("manager", "ca", "챌린지 완료 알림 (검증 요청)", 352, MUTED, "ar")
d.msg("ca", "dns", "DNS TXT 조회 (_acme-challenge.<root>)", 396, WARN, "warn")
d.msg("dns", "ca", "TXT 챌린지 다이제스트 응답", 436, OK, "ok")

# 4. Issuance
d.selfmsg_left("ca", "도메인 제어권 검증 완료", 476, OK)
d.msg("ca", "manager", "인증서 번들 발급 (Leaf + Chain)", 516, OK, "ok")

# 5. Atomic Storage
d.selfmsg("manager", "인증서 원자적 파일 저장", 558, OK, sub="fullchain.pem · privatekey.pem")

# 6. Periodic Maintenance Loop
d.selfmsg("manager", "maintenanceLoop 주기적 검사", 610, MUTED, sub="24시간 주기 · 만료 30일 전 자동 재발급")
d.msg("manager", "ca", "만료 임박 시 갱신 재주문", 654, INFO, "info", sub="동일한 DNS-01 검증 파이프라인 수행")

d.legend(H - 52, [
    ("ACME 주문·갱신", INFO),
    ("DNS 레코드 조작", ACC),
    ("CA DNS 질의", WARN),
    ("검증·발급 완료", OK)
])

out_path = _HERE.parent / "02-05-dns01.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
