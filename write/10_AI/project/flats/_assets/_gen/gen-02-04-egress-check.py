# 사실 출처: internal/egress/client.go:23-31,35,72-86,106-136,162-188,211-228,275-290,300-344,357-359 · internal/runtime/js.go:430 · docs/external-api.md
# 타입 스펙: type-layers
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "OUTBOUND EGRESS · MULTI-LAYER DEFENSE",
    "외부 API 호출(egress) 다층 검증 계층",
    "JavaScript fetch 호출이 공인 IP 목적지에 도달하기까지의 단계별 통제",
    lead="모든 계층은 최소 권한과 사설망 차단 원칙을 적용하며 거부 시 guest 내부 정보를 감춘 채 즉시 실패합니다"
)

# 좌측 진행 화살표
d.t(48, 120, "검증 흐름 ↓", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 134), (48, 460)], SOFT, "soft", 1.2)
d.t(48, 476, "공인 서버", 10, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 848
layers = [
    ("L1", "게스트 스크립트 호출", "await fetch(url, options)",
     "런타임 진입", "절대 HTTP(S) URL · 스트리밍 배제",
     "URL오류", WARN,
     PAPER2, RULE, INK),
    ("L2", "Origin 허용 목록 대조", "internal/egress · MaxURL 8 KiB",
     "정확 일치", "스킴·도메인 대조 (사전 등록된 Origin ≤32개)",
     "ErrDenied", BAD,
     f"{ACC}14", ACC, ACC),
    ("L3", "요청 규격 및 동시성·레이트", "Body 1 MiB · Header 16 KiB",
     "한도 보호", "동시 5슬롯 · 초당 20회 · 핸들러당 16회",
     "ErrLimit", BAD,
     PAPER2, RULE, INK),
    ("L4", "DNS 해석 및 IP 검증", "net.LookupNetIP · publicIP(ip)",
     "SSRF 방어", "10/8 · 127/8 · 169.254/16 · 사설·메타데이터 차단",
     "사설IP차단", BAD,
     f"{ACC}14", ACC, ACC),
    ("L5", "검증 IP 고정 다이얼", "DialContext 고정 IP · TLS SNI 검증",
     "Rebinding 방어", "사전 검증 IP 연결 · Proxy 무시 · Timeout 5s",
     "연결실패", WARN,
     PAPER2, RULE, INK),
    ("L6", "응답 수신 및 리다이렉트 통제", "CheckRedirect · MaxResponseBody 4 MiB",
     "응답 통제", "3xx 자동 추적 차단 · 4 MiB 초과 차단 · Hop 제거",
     "ErrRedirect", WARN,
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

    # 1행: 계층 이름, 중간 검증 칩, 우측 거부 결과 단어
    d.t(LX + 58, y + 22, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 390, y + 18, chip_txt, stroke if is_focal else INFO, size=11)
    d.chip(LX + LW - 64, y + 18, block_term, rej_col, size=11)

    # 2행: 코드 경로(좌), 핵심 정책 규칙(우)
    d.t(LX + 58, y + 42, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 18, y + 42, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(496, [
    ("일반 검증 계층", MUTED),
    ("핵심 보안 방어선 (Origin / SSRF)", ACC),
    ("거부 시 반환 에러", BAD),
])

out_path = _HERE.parent / "02-04-egress-check.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
