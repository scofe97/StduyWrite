# 사실 출처: internal/expose/local/local.go:53-83 · internal/expose/tsnet/tsnet.go:740-767
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 520
d = D(
    W, H,
    "DATA FLOW · HOST ROUTING",
    "Host 라우팅과 Tailscale 신원",
    "Host 분기와 WhoIs 신원 주입"
)

def track(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 11, SOFT, KR, "start", 600)

track(20, 85, 960, 195, "1. 로컬 루프백 (7879)", ACC)
track(20, 295, 960, 205, "2. tailnet 노드 (:443)", INFO)

# 1. 로컬 경로
d.tone(36, 120, 210, 145, ACC, 6, "10", 1.0)
d.t(48, 140, "수신 Host 헤더", 11, ACC, KR, "start", 600)
d.box(46, 150, 190, 30, PAPER2, OK, 0.8)
d.t(54, 170, "try-pod-doc.localhost:7879", 9.5, OK, MONO, "start")
d.box(46, 185, 190, 30, PAPER2, BAD, 0.8)
d.t(54, 205, "evil.example:7879", 9.5, BAD, MONO, "start")
d.box(46, 220, 190, 30, PAPER2, WARN, 0.8)
d.t(54, 240, "a.b.localhost:7879", 9.5, WARN, MONO, "start")

d.tone(295, 120, 280, 145, ACC, 6, "14", 1.2)
d.t(310, 142, "local.Net.ServeHTTP", 12, ACC, MONO, "start", 600)
d.t(310, 168, "TrimSuffix(\".localhost\")", 10, INK, MONO, "start")
d.t(310, 192, "단일 라벨 검증", 10, MUTED, KR, "start")
d.t(310, 216, "Tailscale-User-* 삭제", 10, WARN, KR, "start")
d.t(310, 240, "hosts[label] 매핑", 10, OK, MONO, "start")

d.tone(630, 120, 330, 64, BAD, 6, "12", 1.0)
d.t(645, 142, "404 Not Found", 11, BAD, MONO, "start", 600)
d.t(645, 166, "\"unknown host; use http://<flat>.localhost:<port>\"", 8.5, INK, MONO, "start")

d.tone(630, 196, 330, 69, OK, 6, "14", 1.2)
d.t(645, 218, "e.h.ServeHTTP(w, r)", 11, OK, MONO, "start", 600)
d.t(645, 242, "try-pod-doc 핸들러 (독립 origin)", 10, INK, KR, "start")

d.arrow([(246, 192), (295, 192)], ACC, "acc")
d.arrow([(575, 152), (630, 152)], BAD, "bad")
d.t(602, 142, "불일치", 9, BAD, KR, "middle")
d.arrow([(575, 230), (630, 230)], OK, "ok")
d.t(602, 220, "매칭", 9, OK, KR, "middle")

# 2. tailnet 경로
d.tone(36, 330, 210, 150, INFO, 6, "14", 1.2)
d.t(48, 352, "tailnet 피어 요청 (예시)", 11, INFO, KR, "start", 600)
d.t(48, 374, "<slug>.<tailnet>.ts.net", 9, INK, MONO, "start")
d.box(46, 390, 190, 75, PAPER2, WARN, 0.8)
d.t(54, 412, "위조 시도 헤더:", 9, WARN, KR, "start")
d.t(54, 432, "Tailscale-User-Login:", 8.5, BAD, MONO, "start")
d.t(64, 450, "attacker", 9, BAD, MONO, "start")

d.tone(295, 330, 280, 150, INFO, 6, "14", 1.2)
d.t(310, 352, "tsnet.Net.identity", 12, INFO, MONO, "start", 600)
d.t(310, 378, "1. isIdentityHeader 삭제", 10, WARN, KR, "start")
d.t(310, 402, "2. lc.WhoIs(RemoteAddr)", 10, INK, MONO, "start")
d.t(310, 426, "3. !who.Node.IsTagged()", 10, MUTED, MONO, "start")
d.t(310, 450, "4. RFC 2047 Q-인코딩 주입", 10, OK, KR, "start")

d.tone(630, 330, 330, 150, OK, 6, "14", 1.2)
d.t(645, 352, "nd.handler.ServeHTTP(w, r)", 11, OK, MONO, "start", 600)
d.t(645, 376, "주입된 신원 헤더:", 10, INK, KR, "start")
d.box(645, 390, 300, 50, PAPER2, OK, 0.8)
d.t(655, 410, "Tailscale-User-Login: alice@tailnet", 9, OK, MONO, "start")
d.t(655, 428, "Tailscale-User-Name: Alice", 9, OK, MONO, "start")
d.t(645, 460, "decided_by 기록 및 전달", 9.5, SOFT, KR, "start")

d.arrow([(246, 405), (295, 405)], INFO, "info")
d.t(270, 395, ":443", 9, INFO, MONO, "middle")
d.arrow([(575, 405), (630, 405)], OK, "ok")
d.t(602, 395, "신원 확정", 9, OK, KR, "middle")

p = Path(__file__).parent.parent / "03-03-host-routing.svg"
d.save(p)
print(f"saved {p}")
