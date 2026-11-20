# 사실 출처: docs/design.md 「Process layout」 · internal/runtime/manager.go:30-95,256-285 · internal/core/service.go:430-500 · docs/internal/docs-app.md
# 타입 스펙: type-architecture
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 580
d = D(
    W, H,
    "PROCESS HIERARCHY · ISOLATION TOPOLOGY",
    "flats serve 부모 데몬과 flats worker 자식 프로세스 트리",
    "단일 serve 데몬이 포트를 독점 바인딩하고 각 flat·preview·문서는 독립 worker 프로세스로 격리 구동합니다",
    lead="방문자 ──> 127.0.0.1:7879 (serve 프록시) ──> Unix Sockets (<data>/run/w*.sock) ──> flats worker 셋"
)

# 구획 헬퍼
def zone(x, y, w, h, label, sub=""):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, label, 11, SOFT, KR, "start", 600)
    if sub:
        d.t(x + 14, y + 36, sub, 9, MUTED, MONO, "start")

# 1. 좌측 상단: 방문자 진입
zone(24, 104, 196, 172, "클라이언트", "HTTP Client")
d.box(38, 142, 168, 118, PAPER2, RULE, 1.0)
d.t(48, 172, "방문자", 12, INK, KR, "start", 600)
d.t(48, 196, "HTTP GET", 11, MUTED, MONO, "start")
d.t(48, 220, "127.0.0.1:7879", 12, OK, MONO, "start", 600)

# 2. 우측 상단: flats serve 메인 프로세스
zone(238, 104, 738, 172, "flats serve (PID <pid>)", "launchd / systemd")

# 2-1. core.Service & 7879 리스너
d.box(254, 142, 220, 118, PAPER2, RULE, 1.0)
d.t(268, 166, "core.Service 라우터", 12, ACC, KR, "start", 600)
d.t(268, 190, "포트 7879", 11, INK, KR, "start")
d.t(268, 210, "오리진 인스턴스 매핑", 10, MUTED, KR, "start")
d.t(268, 232, "instance.ServeHTTP", 10, SOFT, MONO, "start")

# 2-2. runtime.Manager
d.box(490, 142, 220, 118, PAPER2, RULE, 1.0)
d.t(504, 166, "runtime.Manager", 12, OK, MONO, "start", 600)
d.t(504, 190, "자식 수명 관리", 11, INK, KR, "start")
d.t(504, 210, "<data>/run/ (0700)", 10, MUTED, MONO, "start")
d.t(504, 232, "in.sock 다이얼 프록시", 10, SOFT, KR, "start")

# 2-3. management & store
d.box(726, 142, 234, 118, PAPER2, RULE, 1.0)
d.t(740, 166, "management / store", 12, INFO, MONO, "start", 600)
d.t(740, 190, "REST / MCP (127.0.0.1:7878)", 11, INK, KR, "start")
d.t(740, 210, "HostGuard 방어", 10, MUTED, KR, "start")
d.t(740, 232, "flats.db (WAL)", 10, SOFT, MONO, "start")

# 진입 화살표
d.arrow([(206, 201), (254, 201)], OK, "ok", 1.4)
d.arrow([(474, 201), (490, 201)], MUTED, "ar", 1.2)
d.arrow([(710, 201), (726, 201)], RULE, "soft", 1.0)

# 3. 하단 구역: flats worker 자식 프로세스 셋
zone(24, 306, 952, 214, "flats worker 풀", "독립 OS 프로세스 · fd 3")

# 3-1. Worker 1: Live 서버 flat
d.tone(38, 344, 300, 160, ACC, 6, "10", 1.1)
d.t(54, 370, "Worker 1: Live flat", 13, ACC, KR, "start", 600)
d.t(54, 394, "소켓: run/w<hex>.sock", 11, INK, MONO, "start")
d.t(54, 418, "DB: flats/<slug>/data/db.sqlite", 10, MUTED, MONO, "start")
d.t(54, 442, "코드: flats/<slug>/v<n>/", 10, MUTED, MONO, "start")
d.t(54, 468, "PID 격리 · VM당 64 MiB", 10, SOFT, KR, "start")

# 3-2. Worker 2: 미리보기 flat (Preview)
d.tone(350, 344, 300, 160, WARN, 6, "10", 1.1)
d.t(366, 370, "Worker 2: Preview flat", 13, WARN, KR, "start", 600)
d.t(366, 394, "소켓: run/w<hex>.sock", 11, INK, MONO, "start")
d.t(366, 418, "오리진: <slug>-<rand>", 10, MUTED, MONO, "start")
d.t(366, 442, "임시 dataDir 격리", 10, MUTED, KR, "start")
d.t(366, 468, "24h 유휴 시 만료", 10, SOFT, KR, "start")

# 3-3. Worker 3: 문서 편집기 flat (Docs)
d.tone(662, 344, 300, 160, INFO, 6, "10", 1.1)
d.t(678, 370, "Worker 3: Docs 앱", 13, INFO, KR, "start", 600)
d.t(678, 394, "소켓: run/w<hex>.sock", 11, INK, MONO, "start")
d.t(678, 418, "DB: flats/<slug>/data/db.sqlite", 10, MUTED, MONO, "start")
d.t(678, 442, "docs/<hash> (내장)", 10, MUTED, MONO, "start")
d.t(678, 468, "fd 3r: 앱 디렉토리", 10, SOFT, KR, "start")

# Manager -> Workers 소켓 전달 화살표 (대칭 분기)
d.arrow([(530, 260), (530, 290), (188, 290), (188, 344)], ACC, "acc", 1.2)
d.arrow([(600, 260), (600, 344)], WARN, "warn", 1.2)
d.arrow([(670, 260), (670, 290), (812, 290), (812, 344)], INFO, "info", 1.2)

d.legend(540, [
    ("Live 서비스 트래픽", ACC),
    ("미리보기 격리 트래픽", WARN),
    ("문서 런타임 트래픽", INFO),
    ("관리 / 메타데이터", MUTED)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02-process-tree.svg"))
d.save(out)
print(f"saved: {out}")
