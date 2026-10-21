# 타입 스펙: type-process
# 사실 출처: cmd/portal-tunnel/main.go:137, cmd/portal-tunnel/agent/manager.go:378, portal/identity/client_identity.go:41, cmd/portal-tunnel/tunnel/runtime.go:75,162,214,241, sdk/expose.go:657
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 980, 490
d = D(
    W, H,
    "PORTAL-TUNNEL · EXPOSE & AGENT ASSEMBLY PROCESS",
    "터널 조립과 서비스 준비 완료 흐름",
    "CLI 단일 실행과 Agent 다중 루프가 동일한 tunnel.Spec 과 런타임으로 합류하는 과정",
    lead="모든 터널은 동일한 Spec 검증과 sdk.Expose 파이프라인을 공유합니다"
)

# 6단계 열 정의
STEPS = [
    ("1", "진입 파싱"),
    ("2", "사양 검증"),
    ("3", "신원 확인"),
    ("4", "릴레이 연결"),
    ("5", "핸들러 구성"),
    ("6", "준비 완료"),
]

COLS = [150, 285, 420, 555, 690, 825]
NODE_W = 118
NODE_H = 56

# 4개 레인 정의 (y0, mid)
LANES = [
    ("CLI EXPOSE", 125, 125 + NODE_H // 2),
    ("AGENT RUN", 195, 195 + NODE_H // 2),
    ("RUNTIME CORE", 265, 265 + NODE_H // 2),
    ("PORTAL SDK", 345, 345 + NODE_H // 2),
]

# 배경 레인 구분선 및 라벨
for name, y_top, y_mid in LANES:
    d.line(16, y_top - 6, W - 16, y_top - 6, RULE, 0.5, dash="2,4")
    d.t(75, y_mid + 4, name, 9.5, MUTED, fam=MONO, anchor="middle", weight=600)

# 단계 열 헤더
for idx, (num, label) in enumerate(STEPS):
    cx = COLS[idx] + NODE_W // 2
    focal = (idx == 1)
    chip_c = ACC if focal else MUTED
    d.box(cx - 10, 92, 20, 16, fill=PAPER2, stroke=chip_c, sw=1.0, r=8)
    d.t(cx, 103, num, 8.5, ACC if focal else INK, fam=MONO, weight=600)
    d.t(cx, 117, label, 9.5, ACC if focal else SOFT, fam=KR, weight=500)

# 커넥터 라우팅 (Single-bend right-angle, z-order 규칙으로 노드 앞서 출력)
def route_down(src_x, src_y, dst_cx, dst_top, c=MUTED, marker="ar", sw=1.2):
    path_d = f"M {src_x} {src_y} H {dst_cx - 8} Q {dst_cx} {src_y} {dst_cx} {src_y + 8} V {dst_top}"
    d.path(path_d, c=c, sw=sw, m=marker)

def route_up(src_x, src_y, dst_cx, dst_bottom, c=MUTED, marker="ar", sw=1.2):
    path_d = f"M {src_x} {src_y} H {dst_cx - 8} Q {dst_cx} {src_y} {dst_cx} {src_y - 8} V {dst_bottom}"
    d.path(path_d, c=c, sw=sw, m=marker)

# 1. CLI expose -> Spec 검증 (L0,C0 -> L2,C1)
route_down(COLS[0] + NODE_W, LANES[0][2], COLS[1] + NODE_W // 2, LANES[2][1] - 4, MUTED, "ar", 1.2)

# 2. Agent run -> Spec 검증 (L1,C0 -> L2,C1)
route_down(COLS[0] + NODE_W, LANES[1][2], COLS[1] + NODE_W // 2, LANES[2][1] - 4, WARN, "warn", 1.2)

# 3. Spec 검증 -> 신원 로드 (L2,C1 -> L2,C2, 수평 focal-out)
d.arrow([(COLS[1] + NODE_W, LANES[2][2]), (COLS[2] - 4, LANES[2][2])], ACC, "acc", 1.4)

# 4. 신원 로드 -> sdk.Expose (L2,C2 -> L3,C3)
route_down(COLS[2] + NODE_W, LANES[2][2], COLS[3] + NODE_W // 2, LANES[3][1] - 4, MUTED, "ar", 1.2)

# 5. sdk.Expose -> 핸들러 라우팅 (L3,C3 -> L2,C4)
route_up(COLS[3] + NODE_W, LANES[3][2], COLS[4] + NODE_W // 2, LANES[2][1] + NODE_H + 4, MUTED, "ar", 1.2)

# 6. 핸들러 라우팅 -> service ready (L2,C4 -> L3,C5)
route_down(COLS[4] + NODE_W, LANES[2][2], COLS[5] + NODE_W // 2, LANES[3][1] - 4, OK, "ok", 1.2)

# 노드 사양
# (col_idx, lane_idx, title, sub, tool, in_chip, out_chip, focal, tone_c)
nodes = [
    # 0A. CLI Expose
    (0, 0, "portal expose", "플래그 파싱", "main.go:137", None, "FL", False, None),
    # 0B. Agent multi-tunnel
    (0, 1, "portal agent", "config.toml 루프", "manager.go:378", "FL", "TB", False, WARN),
    # 1. Spec Validation (FOCAL)
    (1, 2, "tunnel.Spec 검증", "대상·경로 충돌", "runtime.go:75", "FL", "TB", True, ACC),
    # 2. Identity LoadOrCreate
    (2, 2, "신원 로드·생성", "secp256k1 키", "client_identity.go:41", "TB", "ID", False, None),
    # 3. SDK Expose
    (3, 3, "sdk.Expose", "릴레이 연결·임대", "runtime.go:214", "ID", "LS", False, None),
    # 4. Proxy / HTTP routes
    (4, 2, "핸들러 라우팅", "Proxy / RunHTTP", "runtime.go:241", "LS", "WB", False, None),
    # 5. Ready Log
    (5, 3, "service ready", "public_url 알림", "expose.go:657", "WB", None, False, OK),
]

for col_idx, lane_idx, title, sub, tool, in_c, out_c, focal, tone_c in nodes:
    x = COLS[col_idx]
    y = LANES[lane_idx][1]
    
    # 노드 사각형
    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, r=5, op="20", sw=1.5)
    elif tone_c:
        d.tone(x, y, NODE_W, NODE_H, tone_c, r=5, op="14", sw=1.0)
    else:
        d.box(x, y, NODE_W, NODE_H, fill=PAPER2, stroke=RULE, sw=0.9, r=5)
    
    # 역할 배지
    lane_keys = ["CLI", "AGT", "TUN", "SDK"]
    badge = lane_keys[lane_idx]
    badge_c = ACC if focal else (tone_c if tone_c else MUTED)
    d.box(x + 4, y + 4, 18, 9, fill=PAPER, stroke=badge_c, sw=0.5, r=2)
    d.t(x + 13, y + 10.5, badge, 6, badge_c, fam=MONO, weight=600)
    
    # 텍스트
    t_color = ACC if focal else (tone_c if tone_c else INK)
    d.t(x + NODE_W // 2, y + 21, title, 9.5, t_color, fam=KR, weight=600)
    d.t(x + NODE_W // 2, y + 33, sub, 8.5, MUTED, fam=KR, weight=400)
    d.t(x + NODE_W // 2, y + 44, tool, 7.5, SOFT, fam=MONO)
    
    # 페이로드 칩
    if in_c:
        d.box(x + 4, y + NODE_H - 10, 13, 7, fill=PAPER, stroke=MUTED, sw=0.5, r=2)
        d.t(x + 10.5, y + NODE_H - 4.5, in_c, 5, MUTED, fam=MONO, weight=600)
    if out_c:
        d.box(x + NODE_W - 17, y + NODE_H - 10, 13, 7, fill=PAPER, stroke=MUTED, sw=0.5, r=2)
        d.t(x + NODE_W - 10.5, y + NODE_H - 4.5, out_c, 5, MUTED, fam=MONO, weight=600)

d.legend(430, [
    ("단일 CLI 경로", MUTED),
    ("Agent 다중 루프", WARN),
    ("Spec 검증 피벗", ACC),
    ("서비스 개방 완료", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-02-expose-assembly.svg"))
d.save(out_path)
print("saved:", out_path)
