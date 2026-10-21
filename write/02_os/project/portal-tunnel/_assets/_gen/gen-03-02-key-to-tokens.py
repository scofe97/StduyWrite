# 사실 출처: portal/identity/secp256k1.go:107,125,152 · portal/identity/siwe.go:29,76 · portal/identity/register_challenge.go:16-18,35,75,91 · portal/identity/lease_token.go:17-18,28,74,80,84,128,133 · portal/lease.go:29-31,803 · types/paths.go:30 · docs/maintainer/architecture.md:73-89
# 타입 스펙: type-data-flow
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 520
d = D(
    W, H,
    "DATA FLOW · IDENTITY & TOKEN DELEGATION",
    "개인키에서 인가 토큰으로의 데이터 흐름 (Key -> SIWE -> Verify -> JWT)",
    "개인키에서 주소를 도출하고 SIWE 서명으로 증명한 뒤 릴레이가 목적별 ES256K JWT 2종을 분리 발급합니다",
    lead="secp256k1 개인키 하나에서 시작해 임대 제어와 리버스 세션 권한을 안전하게 격리합니다"
)

LABEL_W = 112
NSTEP = 6
SLOT = 144
Y0 = 84
HEAD = 48
LANE = 96
NW = 126
NH = 68

STEPS = [
    ("01", "키·주소 생성", False),
    ("02", "챌린지 교환", False),
    ("03", "메시지 서명", False),
    ("04", "서명 검증", True),
    ("05", "토큰 발급", False),
    ("06", "인가 집행", False),
]

LANES = [
    ("터널 에이전트", "SDK 신원"),
    ("릴레이 서버", "제어 평면"),
    ("인가 엔드포인트", "접근 통제"),
]

def cx(j):
    return LABEL_W + j * SLOT + SLOT // 2

def nx(j):
    return cx(j) - NW // 2

def lane_top(k):
    return Y0 + HEAD + k * LANE

def ny(k):
    return lane_top(k) + 14

# 1. 배경 레인 띠와 구분선 (x=LABEL_W부터 시작해 라벨 영역 충돌 방지)
for k in range(len(LANES)):
    fill_bg = PAPER2 if k % 2 == 0 else PAPER
    d.o.append(f'<rect x="{LABEL_W}" y="{lane_top(k)}" width="{W - LABEL_W - 12}" height="{LANE}" fill="{fill_bg}" opacity="0.6"/>')
    d.line(12, lane_top(k), W - 12, lane_top(k), RULE, 0.8)

d.line(12, lane_top(len(LANES)), W - 12, lane_top(len(LANES)), RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(len(LANES)), RULE, 0.8)

# 2. 단계 머리 (Step headers)
for j, (num, lab, focal) in enumerate(STEPS):
    c = ACC if focal else MUTED
    bg = f"{ACC}33" if focal else f"{PAPER2}"
    border = ACC if focal else RULE
    d.o.append(f'<rect x="{cx(j) - 16}" y="{Y0 + 4}" width="32" height="16" rx="8" fill="{bg}" stroke="{border}" stroke-width="0.8"/>')
    d.t(cx(j), Y0 + 16, num, 10, c, MONO, "middle", 600)
    d.t(cx(j), Y0 + 36, lab, 11, c, KR, "middle", 600 if focal else 400)

# 3. 레인 라벨
for k, (a, b) in enumerate(LANES):
    mid_y = lane_top(k) + LANE // 2
    d.t(LABEL_W // 2, mid_y - 4, a, 12, INK, KR, "middle", 600)
    d.t(LABEL_W // 2, mid_y + 14, b, 10, MUTED, KR, "middle")

# 4. 연결 화살표 (노드 이전에 렌더링)
# (1) 에이전트: Step 0 (키 생성) -> Step 1 (챌린지 요청)
y_tnl = ny(0) + NH // 2
d.arrow([(nx(0) + NW, y_tnl), (nx(1), y_tnl)], MUTED, "ar", 1.2)

# (2) 에이전트 -> 릴레이: Step 1 (챌린지 요청) -> Step 1 (챌린지 발급)
d.arrow([(cx(1), ny(0) + NH), (cx(1), ny(1))], INFO, "info", 1.2)

# (3) 릴레이 -> 에이전트: Step 1 (챌린지 발급) -> Step 2 (메시지 서명)
corr1_x = nx(1) + NW + 9
d.arrow([
    (nx(1) + NW, ny(1) + 20),
    (corr1_x, ny(1) + 20),
    (corr1_x, ny(0) + 20),
    (nx(2), ny(0) + 20)
], INFO, "info", 1.2)

# (4) 에이전트 -> 릴레이 (Focal): Step 2 (메시지 서명) -> Step 3 (서명 검증)
d.arrow([
    (cx(2), ny(0) + NH),
    (cx(2), ny(1) + NH // 2),
    (nx(3), ny(1) + NH // 2)
], ACC, "acc", 1.6)

# Focal 라벨 (Lane 1, Step 2의 빈 공간에 배치, 수직 화살표와 노드 3 사이)
focal_lbl = "SIWE 서명 전달"
focal_mx = 512
focal_my = ny(1) + NH // 2 - 14
d.o.append(f'<rect x="{focal_mx - 37}" y="{focal_my - 10}" width="74" height="18" rx="4" fill="{PAPER}" stroke="{ACC}" stroke-width="0.8"/>')
d.t(focal_mx, focal_my + 3, focal_lbl, 10, ACC, KR, "middle", 600)

# (5) 릴레이: Step 3 (서명 검증) -> Step 4 (토큰 발급)
y_rly = ny(1) + NH // 2
d.arrow([(nx(3) + NW, y_rly), (nx(4), y_rly)], OK, "ok", 1.4)

# (6) 릴레이 -> 에이전트: Step 4 (토큰 발급) -> Step 5 (리버스 세션)
corr4_x = nx(4) + NW + 9
d.arrow([
    (nx(4) + NW, ny(1) + 20),
    (corr4_x, ny(1) + 20),
    (corr4_x, y_tnl),
    (nx(5), y_tnl)
], OK, "ok", 1.2)

# (7) 릴레이 -> API: Step 4 (토큰 발급) -> Step 5 (임대 제어 API)
y_api = ny(2) + NH // 2
d.arrow([
    (nx(4) + NW, ny(1) + NH - 20),
    (corr4_x, ny(1) + NH - 20),
    (corr4_x, y_api),
    (nx(5), y_api)
], WARN, "warn", 1.2)

# 5. 노드 정의 (k, j, title, sub, tool, c, focal)
NODES = [
    # Step 0: 키·주소 생성 (TNL)
    (0, 0, "secp256k1 신원", "비압축 공개키 해시", "EVM 주소 도출", INFO, False),
    # Step 1: 챌린지 요청 (TNL)
    (0, 1, "챌린지 요청", "도메인·주소 제출", "POST /sdk/register/challenge", INFO, False),
    # Step 1: 챌린지 발급 (RLY)
    (1, 1, "SIWE 챌린지", "rch_* · Nonce 생성", "TTL 2분 · 12줄 규격", INFO, False),
    # Step 2: 메시지 서명 (TNL)
    (0, 2, "personal_sign", "EIP-191 프리픽스", "65B 서명 (r||s||v)", INFO, False),
    # Step 3: 서명 검증 (RLY) - Focal!
    (1, 3, "서명자 복원 검증", "메시지 바이트 대조", "ecrecover 주소 일치", ACC, True),
    # Step 4: 토큰 발급 (RLY)
    (1, 4, "ES256K JWT 발급", "go-jose + Relay 키", "Audience 분리 생성", OK, False),
    # Step 5: 리버스 세션 (TNL)
    (0, 5, "리버스 세션 수립", "aud: portal-reverse", "GET /sdk/connect", OK, False),
    # Step 5: 임대 제어 API (API)
    (2, 5, "임대 제어 API", "aud: portal-sdk", "/sdk/renew", WARN, False),
]

for k, j, title, sub, tool, c, focal in NODES:
    x, y = nx(j), ny(k)
    tool_sz = 6.8 if len(tool) > 22 else 9
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
        d.chip(x + NW // 2, y + 16, title, ACC, size=10)
        d.t(x + NW // 2, y + 36, sub, 10, INK, KR, "middle", 500)
        d.t(x + NW // 2, y + 54, tool, tool_sz, MUTED, MONO, "middle")
    else:
        d.box(x, y, NW, NH, fill=PAPER2, stroke=c, sw=1.1, r=6)
        d.t(x + NW // 2, y + 18, title, 11, c, KR, "middle", 600)
        d.t(x + NW // 2, y + 36, sub, 10, INK, KR, "middle")
        d.t(x + NW // 2, y + 54, tool, tool_sz, MUTED, MONO, "middle")

# 6. 범례 (Legend)
legend_y = H - 42
d.legend(legend_y, [
    ("신원 생성 및 챌린지", INFO),
    ("서명 검증 (핵심 전이)", ACC),
    ("리버스 세션 권한", OK),
    ("임대 제어 관리 권한", WARN),
])

out_path = Path(__file__).parent.parent / "03-02-key-to-tokens.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
