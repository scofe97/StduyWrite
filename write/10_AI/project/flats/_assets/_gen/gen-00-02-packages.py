# 사실 출처: go list -f '{{.ImportPath}} {{.Imports}}' ./... · cmd/flats/main.go · internal/app/serve.go
# 타입 스펙: type-layers
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 600
d = D(
    W, H,
    "LAYERS · PACKAGE ARCHITECTURE",
    "flats 패키지 계층 구조와 의존 방향",
    "진입점부터 표면·조립 계층이 중앙 core 에 의존하는 단방향 아키텍처를 구성합니다",
    "cmd/flats ──> app ──> api / mcpx ──> core (12,594줄) ──> store / bundle / config"
)

# 계층 스택 (Layer Stack)
# X: 30, Width: 610 (메인 레이어 5개)
# X: 730, Width: 240 (우측 런타임 및 프로바이더 축)

LX, LW = 30, 610
RX, RW = 730, 240

layers = [
    ("L1 · ENTRY", "진입 계층 (Entry)", "cmd/flats (35줄) · internal/cli (3,546줄)",
     "바이너리 main · CLI 플래그 파싱 · WorkerMain 재실행 바인딩", INFO, 110, 64),
    ("L2 · ASSEMBLY", "조립 계층 (Assembly)", "internal/app (4,752줄)",
     "컴포넌트 수명주기 배선 · serve/config 명령 · graceful shutdown", INFO, 184, 64),
    ("L3 · SURFACES", "표면 계층 (Surfaces)", "api (1,638줄) · mcpx (2,321줄) · console (121줄)",
     "REST API · Streamable MCP (36 도구) · 임베디드 웹 콘솔", INFO, 258, 64),
    ("L4 · CORE DOMAIN", "핵심 도메인 (Core Domain)", "internal/core (12,594줄, 30개 파일)",
     "Service · 수명주기 FSM · 승인 큐 동결 · 라우팅 배포 (중앙 허브)", ACC, 340, 74),
    ("L5 · SUBSTRATE", "기반 계층 (Substrate)", "store (3,776줄) · bundle · config · slug · egress",
     "SQLite 영속화 (flats.db) · 아카이브 언팩 · DNS slug 규칙", OK, 424, 74),
]

for tag, title, pkgs, desc, color, y, h in layers:
    d.box(LX, y, LW, h, PAPER2, RULE, 1.0)
    # 태그
    d.t(LX + 16, y + 20, tag, 9, color, MONO, "start", 600)
    # 타이틀 & 패키지
    d.t(LX + 16, y + 40, title, 13, INK, KR, "start", 600)
    d.t(LX + 210, y + 40, pkgs, 10, color, MONO, "start")
    # 설명
    d.t(LX + 16, y + 56, desc, 10, MUTED, KR, "start")

# 우측 보조 축 1: 실행 런타임 (Execution Runtime)
d.box(RX, 184, RW, 138, PAPER2, RULE, 1.0)
d.t(RX + 14, 204, "SIDE · RUNTIME", 9, WARN, MONO, "start", 600)
d.t(RX + 14, 224, "실행 런타임 축", 13, INK, KR, "start", 600)
d.t(RX + 14, 244, "internal/runtime (3,767줄)", 10, WARN, MONO, "start")
d.t(RX + 14, 262, "internal/qjs (6,348줄)", 10, WARN, MONO, "start")
d.t(RX + 14, 280, "github.com/tetratelabs/wazero", 9, SOFT, MONO, "start")
d.t(RX + 14, 304, "QuickJS / WASI 워커 격리 관리", 10, MUTED, KR, "start")

# 우측 보조 축 2: 네트워크 제공자 (Network Providers)
d.box(RX, 340, RW, 158, PAPER2, RULE, 1.0)
d.t(RX + 14, 360, "SIDE · EXPOSE", 9, INFO, MONO, "start", 600)
d.t(RX + 14, 380, "네트워크 제공자 축", 13, INK, KR, "start", 600)
d.t(RX + 14, 400, "expose/provider (2,210줄)", 10, INFO, MONO, "start")
d.t(RX + 14, 418, "local (189줄) · portal (1,320줄)", 10, INFO, MONO, "start")
d.t(RX + 14, 436, "tsnet (2,258줄) · zrok (1,531줄)", 10, INFO, MONO, "start")
d.t(RX + 14, 454, "cfquick (780줄) · netbird 드라이버", 10, INFO, MONO, "start")
d.t(RX + 14, 480, "core.PrivateNet / PublicNet 구현", 10, MUTED, KR, "start")

# 메인 스택 하향 의존 화살표 (L1 -> L2 -> L3 -> L4 -> L5)
d.arrow([(LX + 70, 174), (LX + 70, 184)], INFO, "info", 1.4)
d.arrow([(LX + 70, 248), (LX + 70, 258)], INFO, "info", 1.4)
d.arrow([(LX + 70, 322), (LX + 70, 340)], ACC, "acc", 1.6)
d.arrow([(LX + 70, 414), (LX + 70, 424)], OK, "ok", 1.4)

# L3 -> L4 연결 라벨
d.t(LX + 95, 334, "import core", 8, ACC, MONO, "start")

# 우측 축 -> Core 단방향 의존 화살표
d.arrow([(RX, 250), (LX + LW + 2, 355)], WARN, "warn", 1.4)
d.t(675, 270, "import core", 8, WARN, MONO, "middle")

d.arrow([(RX, 420), (LX + LW + 2, 385)], INFO, "info", 1.4)
d.t(675, 425, "import core", 8, INFO, MONO, "middle")

# 범례
d.legend(H - 44, [
    ("진입·표면", INFO),
    ("핵심 허브 (core)", ACC),
    ("스토리지·기반 (store)", OK),
    ("런타임 및 워커", WARN)
])

out_path = Path(__file__).parent.parent / "00-02-packages.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
