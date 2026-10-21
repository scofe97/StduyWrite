# 타입 스펙: type-layers
# 사실 출처: cmd/relay-server/policy/mux.go:60-71,
#   cmd/relay-server/policy/source_limiter.go:38-48,
#   cmd/relay-server/policy/preauth.go:9-14,
#   cmd/relay-server/policy/ingress.go:21-29,
#   cmd/relay-server/policy/access.go:57-73,
#   docs/maintainer/architecture.md:91-138,
#   portal/identity/register_challenge.go:75-80,
#   portal/server.go:44-45,
#   portal/lease.go:35, 136-148.
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(W, H,
      "PORTAL-TUNNEL · RELAY ADMISSION & ROUTING POLICY LAYERS",
      "릴레이 정책 및 사전 인증 계층 구조",
      "신뢰 프록시 출발지 결정에서 사전 인증 예산, 서명 검증, 신원 접근 결정 및 임대 라우팅으로 이어지는 5계층 인가 파이프라인",
      lead="비용이 큰 암호 연산과 세션 수립 전에 발신지 예산과 검증된 신원 결정을 순차 검증하는 통제 계층")

# 좌측 방향 표시 (요청 유입 ↓)
d.t(48, 120, "요청 유입 ↓", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 134), (48, 450)], SOFT, "soft", 1.2)
d.t(48, 466, "데이터 전송", 10, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 848
layers = [
    ("L1", "출발지 주소 결정", "policy/ingress.go:29 SourceAddr",
     "신뢰 프록시 검증", "X-Forwarded-For 스푸핑 방지 · 소켓 peer fallback",
     "비신뢰 헤더 무시", WARN,
     PAPER2, RULE, INK),
    ("L2", "사전 인증 예산 차감", "policy/source_limiter.go:48 Allow(cost)",
     "토큰 버킷 (10/20, 600/200)", "서명 검증·JSON 디코딩 전 차감 · 전역/출발지 이중 버킷",
     "429 Retry-After", BAD,
     f"{ACC}14", ACC, ACC),
    ("L3", "역직렬화 및 서명 검증", "portal/identity/register_challenge.go:75",
     "EIP-4361 SIWE 검증", "secp256k1 서명 복구 · 챌린지 원문 바이트 일치",
     "400 / 403 거절", BAD,
     PAPER2, RULE, INK),
    ("L4", "신원 접근 인가 및 라우팅", "policy/access.go:68 Routable(key)",
     "단조 증가 Revision", "ServiceIdentityKey 기준 · Auto/Manual · Ban/Deny",
     "403 / 503 거절", BAD,
     PAPER2, RULE, INK),
    ("L5", "임대 런타임 및 전송 예산", "portal/server.go:44 · portal/lease.go:35",
     "BPS 대역폭 / 브리지 한도", "공개 인그레스 1024 · 검사 대기 128 · 임대 브리지 128",
     "503 한도 초과", BAD,
     PAPER2, RULE, INK),
]

y0 = 104
h_layer = 64
gap = 12

for i, (tag, name, path_txt, chip_txt, note, rej_txt, rej_col, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 좌측 태그 (L1 ~ L5)
    d.box(LX + 16, y + 18, 32, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 32, y + 36, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 1행: 계층 이름, 중간 검증 칩, 우측 거절 결과 배지
    d.t(LX + 64, y + 24, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.chip(LX + 380, y + 20, chip_txt, stroke if is_focal else INFO, size=11)
    d.chip(LX + LW - 80, y + 20, rej_txt, rej_col, size=11)

    # 2행: 코드 경로(좌), 핵심 정책 규칙(우, anchor=end)
    d.t(LX + 64, y + 48, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")
    d.t(LX + LW - 24, y + 48, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(496, [
    ("표준 인가·검증 계층", MUTED),
    ("사전 인증 예산 통제 (Focal)", ACC),
    ("계층별 차단·거절 결과", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-03-admission-layers.svg"))
d.save(out)
print(f"saved: {out}")
