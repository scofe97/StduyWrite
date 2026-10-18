# 타입 스펙: type-layers
# 사실 출처: docs/maintainer/architecture.md §Package Boundaries, docs/src/routes/architecture/+page.md §Package Layout
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480
d = D(W, H,
      "PORTAL-TUNNEL · PACKAGE LAYOUT AND BOUNDARIES",
      "portal-tunnel 패키지 계층 구조와 소유권 경계",
      "CLI 표면에서 SDK, 릴레이 도메인 런타임, 공유 와이어 타입으로 이어지는 4단계 계층",
      lead="엔트리포인트와 SDK와 도메인 서브시스템의 책임 분리 및 공유 타입 경계")

# 좌측 방향 표시 (고수준 표면 ↑ / 저수준 공유 기반 ↓)
d.t(48, 128, "사용자 표면", 11, SOFT, fam=KR, anchor="middle")
d.arrow([(48, 142), (48, 224)], SOFT, "soft", 1.2)
d.arrow([(48, 256), (48, 338)], SOFT, "soft", 1.2)
d.t(48, 354, "공유 기반", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 824
layers = [
    ("L1", "cmd/ (Surface CLI & UI)", ["cmd/portal-tunnel · cmd/relay-server · frontend"],
     "사용자 표면", "CLI 진입점 및 관리 웹 UI",
     PAPER2, RULE, INK),
    ("L2", "sdk/ (Client SDK Facade)", ["exposure.go · listener.go · reverse_transport.go"],
     "클라이언트 SDK", "sdk.Exposure · 리스너 · 프록시",
     f"{ACC}14", ACC, ACC),
    ("L3", "portal/ (Domain Runtime)", ["transport · keyless · identity · acme", "discovery · overlay · cache"],
     "도메인 런타임", "SNI 라우팅 · 키리스 서명 · 임대 등록소",
     PAPER2, RULE, INK),
    ("L4", "types/ · utils/ (Shared)", ["paths.go · types.go · APIEnvelope · 암호/네트워크"],
     "공유 계약·유틸", "공통 DTO 규약 및 저수준 헬퍼",
     PAPER2, RULE, INK),
]

y0 = 104
h_layer = 64
gap = 16

for i, (tag, name, path_lines, role, note, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 태그
    d.box(LX + 16, y + 18, 32, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 32, y + 36, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 계층 이름 및 경로
    if len(path_lines) == 1:
        d.t(LX + 64, y + 28, name, 13, text_col, fam=MONO, anchor="start", weight=600)
        d.t(LX + 64, y + 48, path_lines[0], 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    else:
        d.t(LX + 64, y + 22, name, 12.5, text_col, fam=MONO, anchor="start", weight=600)
        d.t(LX + 64, y + 38, path_lines[0], 10, MUTED, fam=MONO, anchor="start")
        d.t(LX + 64, y + 53, path_lines[1], 10, MUTED, fam=MONO, anchor="start")

    # 역할 칩
    d.chip(LX + 500, y + 32, role, stroke if is_focal else INFO, size=11)

    # 설명 노트
    d.t(LX + LW - 18, y + 36, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(424, [
    ("표준 패키지 계층", MUTED),
    ("클라이언트 SDK (Focal)", ACC),
    ("계층별 역할 구분", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "00-02-packages.svg"))
d.save(out)
print(f"saved: {out}")
