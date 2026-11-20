# 사실 출처: internal/expose/provider/manager.go:740,923-939 · internal/expose/portal/portal.go:79-90,257-271,281-291,323-339,359-390,395-406,725-747
# 타입 스펙: type-sequence
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 780

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, size=11):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, size, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub), "middle")

    def selfmsg(s, a, label, y, c=MUTED, sub=None, to_left=False):
        x = s.LX[a]
        dx = -42 if to_left else 42
        d_arrow = -1 if to_left else 1
        s.path(f"M {x + 10 * d_arrow} {y - 10} L {x + dx} {y - 10} L {x + dx} {y + 10} L {x + 12 * d_arrow} {y + 10}", c, 1.4, m="ar")
        anchor = "end" if to_left else "start"
        tx = x + dx - 8 if to_left else x + dx + 8
        s.t(tx, y - 4, label, 11, c, _kr(label), anchor, 600)
        if sub:
            s.t(tx, y + 14, sub, 10, MUTED, _kr(sub), anchor)

d = SeqKR(
    W, H,
    "PORTAL · PUBLIC EXPOSURE SEQUENCE",
    "Portal 공개 노출 및 요청 라우팅 시퀀스",
    "운영자 승인부터 비동기 릴레이 등록, WaitReady 완료, 방문자 요청 수납 흐름",
    lead="운영자 승인 ──> servePublic ──> portal.Net.Serve ──> sdk.Expose ──> publicHandler"
)

lanes = d.lanes([
    ("운영자", "Console / CLI"),
    ("Core / Manager", "manager.go"),
    ("portal.Net", "portal.go"),
    ("Portal SDK / 릴레이", "expose.go / Relay"),
    ("방문자", "Public Client")
], y0=96, lane_w=140)

d.rails(746)

def sec(y, txt, c):
    w = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 16
    d.box(28, y - 13, w, 20, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.t(36, y + 2, txt, 11, c, fam=KR, anchor="start", weight=600)

# 1. 공개 승인 및 서빙 호출
sec(154, "1. 공개 승인 및 서빙 등록", INFO)
d.msg("운영자", "Core / Manager", "approve public", 190, OK, "ok", sub="승인 반영")
d.selfmsg("Core / Manager", "servePublic(req)", 228, INFO, sub="ExposureRequest")
d.msg("Core / Manager", "portal.Net", "Serve(slug, h, hidden)", 266, ACC, "acc", sub="호출")

# 2. 신원 로드 및 릴레이 등록
sec(304, "2. 신원 로드 및 릴레이 등록", WARN)
d.selfmsg("portal.Net", "loadIdentity(slug)", 330, WARN, sub="0600 키 고정")
d.msg("portal.Net", "Portal SDK / 릴레이", "sdk.Expose(id, relays, opts)", 368, ACC, "acc", sub="WithDiscovery(3)", size=10.5)
d.msg("portal.Net", "Core / Manager", "Serve 반환", 404, MUTED, "ar", dash="4 4", sub="즉시 반환")
d.selfmsg("Portal SDK / 릴레이", "릴레이 비동기 등록", 440, MUTED, sub="Lease 획득")

# 3. 준비 대기 및 주소 확정
sec(478, "3. 준비 대기 및 주소 확정", OK)
d.msg("Core / Manager", "portal.Net", "WaitReady(slug)", 504, MUTED, "ar", sub="준비 대기")
d.msg("Portal SDK / 릴레이", "portal.Net", "RelayReady", 540, OK, "ok", sub="https://<slug>.<relay>")
d.selfmsg("portal.Net", "pin / alias 저장", 576, OK, sub="<slug>.relay, .alias")
d.msg("portal.Net", "Core / Manager", "URL 반환", 612, OK, "ok", sub="Endpoint ready")

# 4. 방문자 요청 및 헤더 보호
sec(648, "4. 방문자 요청 및 헤더 보호", ACC)
d.msg("방문자", "Portal SDK / 릴레이", "GET /", 672, INK, "ar", sub="터널 수신")
d.msg("Portal SDK / 릴레이", "portal.Net", "publicHandler", 698, ACC, "acc", sub="Tailscale 헤더 제거")
d.msg("portal.Net", "Core / Manager", "siteHandler", 724, OK, "ok", sub="200 OK")

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-04-expose-sequence.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
