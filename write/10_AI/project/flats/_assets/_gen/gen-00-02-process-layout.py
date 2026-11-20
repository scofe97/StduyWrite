# 사실 출처: docs/design.md 「Process layout」 · cmd/flats/main.go:14-22 · internal/config/config.go:82,84 · internal/runtime/worker.go:52
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "ARCHITECTURE · COMPONENT BOUNDARIES",
    "flats serve 프로세스 구조와 격리 경계",
    "단일 Go 바이너리가 메타데이터와 관리 서버를 직접 품고, 동적 서버 플랫은 독립 워커로 격리합니다",
    "flats serve (127.0.0.1:7878 관리 / 7879 콘텐츠) ── Unix Socket ──> flats worker 서브프로세스"
)

# 배경 구획 (Zone)
def zone(x, y, w, h, label, sub=""):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 11, SOFT, KR, "start", 600)
    if sub:
        d.t(x + 16, y + 37, sub, 9, MUTED, MONO, "start")

# 1. flats serve 메인 프로세스 영역
zone(20, 104, 566, 400, "flats serve 메인 데몬 (단일 롱러닝 프로세스)", "launchd / systemd 관리 · host.data_dir lock")

# 1-1. management server (좌측 상단 관리 표면)
MGT_X, MGT_Y, MGT_W, MGT_H = 34, 150, 226, 140
d.tone(MGT_X, MGT_Y, MGT_W, MGT_H, INFO, 6, "14", 1.2)
d.t(MGT_X + 16, MGT_Y + 26, "management server (관리 서버)", 13, INFO, KR, "start", 600)
d.t(MGT_X + 16, MGT_Y + 50, "127.0.0.1:7878 리스너 바인딩", 11, INK, MONO, "start")
d.t(MGT_X + 16, MGT_Y + 70, "REST API (/api) + 웹 콘솔 (/)", 10, MUTED, KR, "start")
d.t(MGT_X + 16, MGT_Y + 90, "MCP 엔드포인트 (/mcp, 36개 도구)", 10, MUTED, KR, "start")
d.t(MGT_X + 16, MGT_Y + 112, "HostGuard: DNS rebinding 방어", 9, SOFT, MONO, "start")

# 1-2. provider manager (좌측 하단 네트워크 제공자)
PRV_X, PRV_Y, PRV_W, PRV_H = 34, 308, 226, 180
d.tone(PRV_X, PRV_Y, PRV_W, PRV_H, INFO, 6, "14", 1.1)
d.t(PRV_X + 16, PRV_Y + 24, "provider manager (제공자 관리)", 12, INFO, KR, "start", 600)
d.t(PRV_X + 16, PRV_Y + 44, "8대 네트워크 제공자 수명주기 총괄", 10, INK, KR, "start")
d.t(PRV_X + 16, PRV_Y + 64, "local (127.0.0.1:7879 루프백)", 10, MUTED, MONO, "start")
d.t(PRV_X + 16, PRV_Y + 82, "tailscale / tailscale-funnel", 10, MUTED, MONO, "start")
d.t(PRV_X + 16, PRV_Y + 100, "portal (역방향 터널 릴레이)", 10, MUTED, MONO, "start")
d.t(PRV_X + 16, PRV_Y + 118, "zrok / cloudflare-quick", 10, MUTED, MONO, "start")
d.t(PRV_X + 16, PRV_Y + 136, "netbird / netbird-expose", 10, MUTED, MONO, "start")
d.t(PRV_X + 16, PRV_Y + 158, "internal/expose/provider/manager.go:207", 8.5, SOFT, MONO, "start")

# 1-3. core.Service (중앙 핵심 허브)
CORE_X, CORE_Y, CORE_W, CORE_H = 330, 150, 240, 140
d.tone(CORE_X, CORE_Y, CORE_W, CORE_H, ACC, 6, "14", 1.2)
d.t(CORE_X + 16, CORE_Y + 26, "core.Service (핵심 도메인)", 13, ACC, KR, "start", 600)
d.t(CORE_X + 16, CORE_Y + 50, "수명주기 · Draft · Version · Deploy", 11, INK, KR, "start")
d.t(CORE_X + 16, CORE_Y + 70, "승인 큐 동결 (approval: pending)", 11, MUTED, KR, "start")
d.t(CORE_X + 16, CORE_Y + 90, "미리보기 개설 및 사이트 라우팅", 10, MUTED, KR, "start")
d.t(CORE_X + 16, CORE_Y + 112, "internal/core/service.go:114", 9, SOFT, MONO, "start")

# 1-4. store (SQLite 메타데이터 영속화)
STORE_X, STORE_Y, STORE_W, STORE_H = 330, 308, 240, 88
d.tone(STORE_X, STORE_Y, STORE_W, STORE_H, OK, 6, "14", 1.1)
d.t(STORE_X + 16, STORE_Y + 24, "store (SQLite 메타데이터)", 12, OK, KR, "start", 600)
d.t(STORE_X + 16, STORE_Y + 44, "flats.db (WAL 모드)", 10, INK, MONO, "start")
d.t(STORE_X + 16, STORE_Y + 60, "modernc.org/sqlite", 9, SOFT, MONO, "start")
d.t(STORE_X + 16, STORE_Y + 76, "버전 번호 · 해시 · 승인 레코드 영속화", 9, MUTED, KR, "start")

# 1-5. design instances (인-프로세스 핸들러)
DSN_X, DSN_Y, DSN_W, DSN_H = 330, 412, 240, 76
d.box(DSN_X, DSN_Y, DSN_W, DSN_H, PAPER2, RULE, 1.0)
d.t(DSN_X + 16, DSN_Y + 24, "design instances (인-프로세스)", 12, INK, KR, "start", 600)
d.t(DSN_X + 16, DSN_Y + 44, "캔버스 아트보드 핸들러 (internal/design)", 10, MUTED, KR, "start")
d.t(DSN_X + 16, DSN_Y + 62, "실시간 리비전 저장 및 SSE 브로드캐스트", 9, SOFT, KR, "start")

# 2. 격리 서브프로세스 영역 (워커 프로세스)
zone(660, 104, 320, 400, "격리 서브프로세스 (flats worker)", "re-exec · OS 프로세스 격리")

# 2-1. server flat worker
WRK1_X, WRK1_Y, WRK1_W, WRK1_H = 680, 150, 280, 150
d.tone(WRK1_X, WRK1_Y, WRK1_W, WRK1_H, WARN, 6, "14", 1.2)
d.t(WRK1_X + 16, WRK1_Y + 26, "flats worker (서버 플랫)", 13, WARN, KR, "start", 600)
d.t(WRK1_X + 16, WRK1_Y + 50, "QuickJS / WASI 런타임 구동", 11, INK, KR, "start")
d.t(WRK1_X + 16, WRK1_Y + 70, "핸들러 fetch(request, env) 실행", 10, MUTED, MONO, "start")
d.t(WRK1_X + 16, WRK1_Y + 90, "JS: env.DB / env.FILES 격리", 10, MUTED, MONO, "start")
d.t(WRK1_X + 16, WRK1_Y + 110, "10s 타임아웃 · 메모리 64MB 상한", 10, WARN, KR, "start")
d.t(WRK1_X + 16, WRK1_Y + 130, "internal/runtime/worker.go:52", 9, SOFT, MONO, "start")

# 2-2. docs app worker
WRK2_X, WRK2_Y, WRK2_W, WRK2_H = 680, 320, 280, 130
d.tone(WRK2_X, WRK2_Y, WRK2_W, WRK2_H, WARN, 6, "14", 1.1)
d.t(WRK2_X + 16, WRK2_Y + 26, "flats worker (문서 편집기)", 13, WARN, KR, "start", 600)
d.t(WRK2_X + 16, WRK2_Y + 50, "internal/apps/docs 내장 JS 앱", 11, INK, KR, "start")
d.t(WRK2_X + 16, WRK2_Y + 70, "실시간 마크다운 렌더링 엔진", 10, MUTED, KR, "start")
d.t(WRK2_X + 16, WRK2_Y + 90, "저장 즉시 반영 (배포 승인 없음)", 10, OK, KR, "start")
d.t(WRK2_X + 16, WRK2_Y + 112, "서버 플랫 워커와 동일 구조", 9, SOFT, KR, "start")

# 상호 연결 화살표
# management server -> core (API 호출)
d.arrow([(MGT_X + MGT_W, 195), (CORE_X, 195)], ACC, "acc", 1.4)
d.t((MGT_X + MGT_W + CORE_X) // 2, 187, "API 호출", 9, ACC, KR, "middle")

# core -> provider manager (Serve / Stop)
d.arrow([(CORE_X, 255), (295, 255), (295, 345), (PRV_X + PRV_W, 345)], INFO, "info", 1.4)
d.t(295, 247, "Serve / Stop", 8.5, INFO, MONO, "middle")

# core -> store (SQL 메타데이터)
d.arrow([(CORE_X + 100, CORE_Y + CORE_H), (CORE_X + 100, STORE_Y)], OK, "ok", 1.4)
d.t(CORE_X + 108, STORE_Y - 9, "SQL 메타데이터", 9, OK, KR, "start")

# core -> worker (Unix Socket Proxy)
d.arrow([(CORE_X + CORE_W, 225), (WRK1_X, 225)], WARN, "warn", 1.5)
d.t(623, 214, "Unix Socket", 9, WARN, MONO, "middle")
d.t(623, 202, "w<hex>.sock", 8, MUTED, MONO, "middle")

# 범례 (Legend)
d.legend(H - 44, [
    ("핵심 도메인 (core)", ACC),
    ("스토리지 (store)", OK),
    ("관리 및 네트워크 인터페이스", INFO),
    ("격리 워커 (worker)", WARN)
])

out_path = Path(__file__).parent.parent / "00-02-process-layout.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
