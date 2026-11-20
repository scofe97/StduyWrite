# 사실 출처: README.md:243-253 · docs/networking.md 「Providers」「Visibility」 · docs/network-provider-lifecycle.md 「Contract」「Host grants」 · internal/core/lifecycle.go:301-303,346-376,389-421,998-1065 · internal/expose/provider/manager.go:428-467,512-534,887-1001
# 타입 스펙: type-layers
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "NETWORK EXPOSURE · 6-LAYER VERIFICATION MODEL",
    "flat 네트워크 공개 검증 6계층",
    "호스트 허용에서 경로 준비까지 각 방어 계층을 순차 검증해야 외부 트래픽이 연결됩니다",
    lead="하위 계층 검증을 통과하지 못하면 외부에 공개되지 않습니다"
)

# 좌측 진행 화살표 (아래에서 위로 검증 단계 상승)
d.t(48, 480, "검증 통과 ↑", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 464), (48, 120)], SOFT, "soft", 1.2)
d.t(48, 106, "공개 URL", 10, SOFT, fam=KR, anchor="middle", weight=600)

LX, LW = 96, 848
# 레이어 목록: 상단(L6, 최종 결과)부터 하단(L1, 기초 전제) 순으로 배치
layers = [
    ("L6", "경로 준비 완료", "manager.go:562 · README.md:251",
     "state: ready", "비동기 리스너·인증서·릴레이 확립",
     "provider_not_ready", BAD,
     f"{OK}14", OK, OK),
    ("L5", "배포 버전 존재", "lifecycle.go:301,1046 · README.md:249",
     "LiveVersion > 0", "Website·Page 필수 (문서·디자인 면제)",
     "ErrConflict", BAD,
     PAPER2, RULE, INK),
    ("L4", "공개 전환 승인", "lifecycle.go:998 · docs/design.md",
     "set_visibility 승인", "웹 콘솔 파라미터 동결 후 승인 집행",
     "pending_approval", WARN,
     f"{ACC}14", ACC, ACC),
    ("L3", "flat 별 제공자 허용", "lifecycle.go:389 · README.md:231",
     "Networks 허용", "개별 flat 명시적 opt-in 부여",
     "provider_not_permitted", BAD,
     PAPER2, RULE, INK),
    ("L2", "제공자 백엔드 설정", "manager.go:536 · status detail",
     "configured: true", "바이너리 내 클라이언트 주입 여부",
     "ErrNotConfigured", BAD,
     PAPER2, RULE, INK),
    ("L1", "호스트 제공자 허용", "manager.go:428 · network.permitted",
     "HostAllows(id)", "호스트 설정 활성화 (로컬 루프백 항시 허용)",
     "provider_not_permitted", BAD,
     PAPER2, RULE, INK),
]

y0 = 100
h_layer = 54
gap = 8

for i, (tag, name, path_txt, chip_txt, note, block_term, rej_col, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC or stroke == OK)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 좌측 태그 (L6 ~ L1)
    d.box(LX + 14, y + 13, 30, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 29, y + 31, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 1행: 계층 이름, 중간 검증 칩, 우측 결여 시 오류 단어
    d.t(LX + 58, y + 22, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 390, y + 18, chip_txt, stroke if is_focal else INFO, size=11)
    d.chip(LX + LW - 92, y + 18, block_term, rej_col, size=11)

    # 2행: 코드 경로(좌), 핵심 정책 규칙(우)
    d.t(LX + 58, y + 42, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 42, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(486, [
    ("기본 방어 계층", MUTED),
    ("승인 집행 (Focal)", ACC),
    ("경로 준비 완료 (Live)", OK),
    ("결여 시 차단 오류", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02-grant-layers.svg"))
d.save(out)
print(f"saved: {out}")
