# 사실 출처: internal/qjs/NOTICE:9-27 · internal/qjs/runtime.go:18,21-26,33-35 · internal/runtime/protocol.go:27-30 · internal/runtime/js.go:81-92 · internal/runtime/worker.go:46-71 · internal/runtime/manager.go:250-251 · docs/design.md 「Process layout」
# 타입 스펙: type-layers
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "SANDBOX ARCHITECTURE · DEFENSE IN DEPTH LAYERS",
    "flats 샌드박스 격리 계층 — 스크립트에서 호스트 OS까지의 다층 방어",
    "사용자 스크립트를 wasm 선형 메모리·wazero·독립 worker로 격리합니다",
    lead="상위 계층의 자원 남용과 오류를 단계별로 차단합니다"
)

# 좌측 진행 화살표
d.t(48, 120, "실행 흐름 ↓", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 134), (48, 460)], SOFT, "soft", 1.2)
d.t(48, 476, "호스트 OS", 10, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 848
layers = [
    ("L1", "사용자 핸들러 스크립트", "server.js · export default { fetch }",
     "런타임 입력", "신뢰하지 않는 사용자 코드",
     "코드", WARN,
     PAPER2, RULE, INK),
    ("L2", "QuickJS 바이트코드 엔진", "qjs/runtime.go:18 //go:embed qjs.wasm",
     "JS 힙 갇힘", "JS 객체 할당을 wasm 선형 메모리에 가둠",
     "힙", INFO,
     PAPER2, RULE, INK),
    ("L3", "WebAssembly 선형 메모리", "runtime/protocol.go:28 DefaultMemoryPages=1024",
     "1024 pages (64 MiB)", "grow 초과 시 -1 반환 · 범위 밖 접근 시 Trap",
     "메모리", BAD,
     f"{ACC}14", ACC, ACC),
    ("L4", "wazero 순수 Go 런타임", "runtime/js.go:81-92 · qjs.New",
     "10s 타임아웃 · ReadOnlyDir", "CloseOnContextDone: true · 디렉터리 읽기 전용",
     "시간·FS", BAD,
     PAPER2, RULE, INK),
    ("L5", "flats worker 프로세스", "docs/design.md · runtime/worker.go",
     "OS 프로세스 격리", "버전별 독립 프로세스 · Unix 소켓 통신",
     "프로세스", OK,
     PAPER2, RULE, INK),
    ("L6", "운영자 OS 환경 (운영자 몫)", "manager.go:250 cmd.Env · :251 cmd.Dir",
     "flats 미적용", "운영자 계정 실행 · 상속 환경 비움",
     "호스트", WARN,
     PAPER2, RULE, INK),
]

y0 = 106
h_layer = 54
gap = 10

for i, (tag, name, path_txt, chip_txt, note, block_term, rej_col, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 좌측 태그 (L1 ~ L6)
    d.box(LX + 14, y + 13, 30, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 29, y + 31, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 1행: 계층 이름, 중간 검증 칩, 우측 막는 것 단어
    d.t(LX + 58, y + 22, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 380, y + 18, chip_txt, stroke if is_focal else INFO, size=11)
    d.chip(LX + LW - 64, y + 18, block_term, rej_col, size=11)

    # 2행: 코드 경로(좌), 핵심 정책 규칙(우)
    d.t(LX + 58, y + 42, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 42, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(496, [
    ("표준 격리 계층", MUTED),
    ("wasm 선형 메모리 상한 (Focal)", ACC),
    ("계층별 차단 통제 영역", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01-sandbox-layers.svg"))
d.save(out)
print(f"saved: {out}")
