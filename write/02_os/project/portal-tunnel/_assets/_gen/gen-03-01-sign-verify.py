# 사실 출처: SEC 2 v2 §2.4.1 · FIPS 180-4 · FIPS 202 · EIP-191 · EIP-55 · RFC 8812 §3.2 · portal/identity/secp256k1.go:107-179 · portal/identity/siwe.go:73-90
# 타입 스펙: type-data-flow
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 500
d = D(
    W, H,
    "DATA FLOW · DIGITAL SIGNATURE & VERIFICATION",
    "전자서명과 공개키 복구 검증 파이프라인 (Sign -> Wire -> ecrecover)",
    "송신자가 개인키로 서명(r,s,v)을 생성해 전송하면 수신자가 동일 해시에서 공개키를 복원해 주소를 대조합니다",
    lead="서버가 공개키를 미리 보관하지 않아도 서명 자체에서 발신자 신원을 수학적으로 복원합니다"
)

LABEL_W = 120
NSTEP = 6
SLOT = 142
Y0 = 84
HEAD = 52
LANE = 132
NW = 116
NH = 64

STEPS = [
    ("01", "메시지 준비", False),
    ("02", "해시 계산", False),
    ("03", "개인키 서명", False),
    ("04", "네트워크 전송", False),
    ("05", "공개키 복구", True),
    ("06", "주소 대조", False),
]

LANES = [
    ("송신자", "터널·지갑"),
    ("수신자", "릴레이·서버"),
]

def cx(j):
    return LABEL_W + j * SLOT + SLOT // 2

def nx(j):
    return cx(j) - NW // 2

def lane_top(k):
    return Y0 + HEAD + k * LANE

def ny(k):
    return lane_top(k) + 16

# 1. 배경 레인 띠와 구분선
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

# 4. 연결 화살표 (직각 연결)
y_tnl = ny(0) + NH // 2
y_rly = ny(1) + NH // 2

# (1) 송신자: Step 0 (메시지) -> Step 1 (해시)
d.arrow([(nx(0) + NW, y_tnl), (nx(1), y_tnl)], INFO, "info", 1.2)

# (2) 송신자: Step 1 (해시) -> Step 2 (서명)
d.arrow([(nx(1) + NW, y_tnl), (nx(2), y_tnl)], INFO, "info", 1.2)

# (3) 송신자: Step 2 (서명) -> Step 3 (전송 패키징)
d.arrow([(nx(2) + NW, y_tnl), (nx(3), y_tnl)], INFO, "info", 1.2)

# (4) 송신자 -> 수신자: Step 3 (송신 패키징) -> Step 3 (수신 해시)
d.arrow([(cx(3), ny(0) + NH), (cx(3), ny(1))], INFO, "info", 1.4)

# (5) 수신자: Step 3 (수신 해시) -> Step 4 (공개키 복구 - Focal)
d.arrow([(nx(3) + NW, y_rly), (nx(4), y_rly)], ACC, "acc", 1.6)

# (6) 수신자: Step 4 (공개키 복구) -> Step 5 (주소 대조)
d.arrow([(nx(4) + NW, y_rly), (nx(5), y_rly)], OK, "ok", 1.4)

# 5. 노드 정의 (k, j, title, sub, tool, c, focal)
NODES = [
    # Step 0: 평문 메시지 (TNL)
    (0, 0, "평문 페이로드", "SIWE 요청 명세", "임의 바이트 M", INFO, False),
    # Step 1: 해시 다이제스트 (TNL)
    (0, 1, "해시 지문 생성", "EIP-191 접두+M", "Keccak256(접두+M)", INFO, False),
    # Step 2: 개인키 서명 (TNL)
    (0, 2, "ECDSA 서명", "secp256k1 개인키", "65B (r || s || v)", INFO, False),
    # Step 3: 송신 패키징 (TNL)
    (0, 3, "페이로드 송신", "원문 M + 65B 서명", "HTTP Body 전송", INFO, False),
    # Step 3: 수신 및 해시 (RLY)
    (1, 3, "수신 동일 해시", "동일 접두+M 결합", "Keccak256(접두+M)", INFO, False),
    # Step 4: 공개키 복구 (RLY) - Focal
    (1, 4, "ecrecover 복원", "서명(r,s,v) 역연산", "64B 비압축 공개키", ACC, True),
    # Step 5: 주소 대조 (RLY)
    (1, 5, "주소 일치 검증", "Keccak 뒤 20B 추출", "EIP-55 주소 일치", OK, False),
]

for k, j, title, sub, tool, c, focal in NODES:
    x, y = nx(j), ny(k)
    tool_sz = 8.5
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
        d.t(x + NW // 2, y + 18, title, 11, ACC, KR, "middle", 600)
        d.t(x + NW // 2, y + 37, sub, 10, INK, KR, "middle", 500)
        d.t(x + NW // 2, y + 53, tool, tool_sz, MUTED, MONO, "middle")
    else:
        d.box(x, y, NW, NH, fill=PAPER2, stroke=c, sw=1.1, r=6)
        d.t(x + NW // 2, y + 18, title, 11, c, KR, "middle", 600)
        d.t(x + NW // 2, y + 37, sub, 10, INK, KR, "middle")
        d.t(x + NW // 2, y + 53, tool, tool_sz, MUTED, MONO, "middle")

# 6. 범례
legend_y = H - 36
d.legend(legend_y, [
    ("송신자 서명 생성 파이프라인", INFO),
    ("수신자 공개키 복구 역연산 (Focal)", ACC),
    ("주소 일치 및 인증 성공", OK),
])

out_path = Path(__file__).parent.parent / "03-01-sign-verify.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
