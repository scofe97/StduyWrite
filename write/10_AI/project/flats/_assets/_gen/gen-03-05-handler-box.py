# 사실 출처: internal/expose/portal/portal.go:156,316 · internal/expose/zrok/zrok.go:100,198-202 · internal/expose/cfquick/cfquick.go:118,225-228 · netbird/netbird.go:165,504-507
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "ARCHITECTURE · COMMON HANDLERBOX PATTERN",
    "4개 제공자의 공통 handlerBox 구조",
    "터널을 유지한 채 핸들러를 교체합니다",
    lead="Serve(slug, h) 재호출 시 set(h)로 원자적 교체"
)

# 3대 구역 정의
def zone(x, y, w, h, label, tag=""):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, label, 11, SOFT, KR, "start", 600)
    if tag:
        d.t(x + w - 14, y + 20, tag, 10, MUTED, MONO, "end")

zone(24, 100, 250, 420, "1. 네트워크 인입", "PROVIDERS")
zone(298, 100, 394, 420, "2. 공통 추상화: handlerBox", "SWAP PATTERN")
zone(716, 100, 260, 420, "3. flat 런타임", "HTTP TARGET")

# 1구역: 4개 네트워크 제공자 박스
providers = [
    ("Portal", "portal.go:156", "다중 릴레이", INFO),
    ("zrok", "zrok.go:100", "OpenZiti 오버레이", ACC),
    ("Cloudflare quick", "cfquick.go:118", "libtunnel", WARN),
    ("NetBird", "netbird.go:165", "WireGuard 피어", OK),
]

y_p = 136
for name, loc, desc, col in providers:
    d.box(40, y_p, 218, 54, PAPER2, RULE, 1.0)
    d.t(52, y_p + 20, name, 12, col, KR, "start", 600)
    d.t(246, y_p + 20, loc, 10, MUTED, MONO, "end")
    d.t(52, y_p + 38, desc, 10, SOFT, KR, "start")
    # 화살표 -> handlerBox로
    d.arrow([(258, y_p + 27), (314, y_p + 27)], SOFT, "ar", 1.0)
    y_p += 68

# 1구역 하단: 위조 헤더 제거 필터
d.tone(40, 424, 218, 72, ACC, 6, "10", 1.0)
d.t(52, 446, "publicHandler 가드", 11, ACC, KR, "start", 600)
d.t(52, 466, "Tailscale-User-* 제거", 10, SOFT, KR, "start")

# 2구역: handlerBox 상세
d.box(318, 136, 354, 164, PAPER2, ACC, 1.4)
d.t(334, 162, "type handlerBox struct", 13, ACC, MONO, "start", 600)
d.t(656, 162, "slug당 1개", 11, SOFT, KR, "end")

d.line(334, 174, 656, 174, RULE, 1.0)

d.t(334, 196, "mu sync.RWMutex", 11, INK, MONO, "start")
d.t(334, 216, "h  http.Handler", 11, INK, MONO, "start")
d.t(656, 206, "Portal: active 카운터 추가", 10, MUTED, KR, "end")

d.tone(330, 232, 330, 52, INFO, 4, "10", 1.0)
d.t(342, 252, "get() -> RLock() h 반환", 10, INFO, MONO, "start")
d.t(342, 270, "set(h) -> Lock() h 교체", 10, ACC, MONO, "start")

# 2구역 하단: Serve() 핸들러 교체 로직
d.box(318, 320, 354, 176, PAPER2, RULE, 1.0)
d.t(334, 344, "핸들러 교체 로직", 12, INK, KR, "start", 600)
d.t(334, 362, "공통 교체 패턴", 10, MUTED, KR, "start")

d.line(334, 372, 656, 372, RULE, 1.0)

d.t(334, 396, "if e != nil && !e.stopping {", 11, WARN, MONO, "start", 600)
d.t(354, 418, "e.handler.set(h)", 12, ACC, MONO, "start", 600)
d.t(354, 440, "return e.url, nil", 11, OK, MONO, "start")
d.t(334, 462, "}", 11, WARN, MONO, "start", 600)
d.t(334, 482, "터널 유지 · 핸들러 교체", 10, SOFT, KR, "start")

# handlerBox -> flat handler 화살표
d.arrow([(672, 218), (732, 218)], ACC, "ar", 1.4)
d.t(702, 208, "ServeHTTP", 10, ACC, MONO, "middle")

# 3구역: flat 런타임 핸들러
d.box(732, 136, 228, 164, PAPER2, OK, 1.2)
d.t(748, 162, "flat Live Handler", 13, OK, KR, "start", 600)
d.t(748, 184, "worker.ServeHTTP", 11, INK, MONO, "start")

d.line(748, 196, 944, 196, RULE, 1.0)

d.t(748, 218, "Unix 소켓 수납", 11, SOFT, KR, "start")
d.t(748, 238, "JS · WASI · 정적", 10, SOFT, KR, "start")
d.t(748, 258, "새 배포 시 갱신", 10, ACC, KR, "start")

# 3구역 하단: 수명주기 전이
d.tone(732, 320, 228, 176, PAPER2, 6, "10", 1.0)
d.t(748, 346, "Manager 수명주기", 12, INK, KR, "start", 600)
d.t(748, 380, "1. flat 워커 준비", 10, SOFT, KR, "start")
d.t(748, 412, "2. Net.Serve(slug, h)", 10, ACC, MONO, "start")
d.t(748, 444, "3. 활성 세션 swap", 10, OK, KR, "start")
d.t(748, 476, "4. 핸들러 교체 완료", 10, SOFT, KR, "start")

# 범례
d.legend(515, [
    ("네트워크 인입", INFO),
    ("handlerBox (Focal)", ACC),
    ("flat 런타임", OK),
    ("핸들러 스왑 분기", WARN),
])

out_path = Path(__file__).parent.parent / "03-05-handler-box.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
