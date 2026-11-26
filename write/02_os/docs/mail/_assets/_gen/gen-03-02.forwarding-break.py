# 사실 출처: RFC 7208(SPF 전달 실패), RFC 6376(DKIM 본문 변형), RFC 7489(DMARC 실패), RFC 8617(ARC)
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

label_col_w = 132
step_slot_w = 164
right_pad = 28
n_steps = 5
n_lanes = 3
W = label_col_w + n_steps * step_slot_w + right_pad  # 980
header_h = 40
lane_h = 104
legend_h = 80
Y0 = 96
H = Y0 + header_h + n_lanes * lane_h + legend_h  # 528 -> 540
H = 540

lanes = [
    ("원 발송 도메인", "example.com (ORG)"),
    ("중간 포워더", "forwarder.org (FWD)"),
    ("최종 수신 MTA", "receiver.net (RCV)")
]

steps = [
    ("01", "최초 발송"),
    ("02", "포워더 수신"),
    ("03", "본문 변형"),
    ("04", "수신 직접 검증"),
    ("05", "ARC 증거 평가")
]
FOCAL_STEP = 4

def lane_top(k): return Y0 + header_h + k * lane_h
def lane_mid(k): return lane_top(k) + lane_h / 2
def step_cx(j): return label_col_w + j * step_slot_w + step_slot_w / 2
node_w, node_h = 148, 76
def node_x(j): return step_cx(j) - node_w / 2
def node_y(k): return lane_top(k) + (lane_h - node_h) / 2
legend_top = Y0 + header_h + n_lanes * lane_h

d = D(
    W, H,
    "DATA FLOW · FORWARDING BREAKAGE & ARC RESCUE",
    "전달 과정의 SPF·DKIM 붕괴와 ARC를 통한 인증 보존",
    "포워더를 거치며 발송 IP 변경과 본문 푸터 삽입으로 깨진 SPF·DKIM 증거를 중간 호스트가 봉인해 전달하고 수신자가 로컬 정책으로 평가합니다",
    "RFC 7208, RFC 6376, RFC 7489 및 RFC 8617 포워딩 환경 인증 검증 기준"
)

# ── 레인 배경 및 구분선 ──
for k in range(n_lanes):
    if k % 2 == 0:
        d.o.append(f'<rect x="{label_col_w}" y="{lane_top(k)}" width="{W - label_col_w}" height="{lane_h}" fill="rgba(245,245,245,0.02)"/>')
    d.line(0, lane_top(k), W, lane_top(k), "rgba(245,245,245,0.12)", 0.8)
d.line(0, legend_top, W, legend_top, "rgba(245,245,245,0.12)", 0.8)
d.line(label_col_w, Y0 + header_h, label_col_w, legend_top, "rgba(245,245,245,0.22)", 1.0)

# ── 헤더 스텝 칩 ──
for j, (num, lab) in enumerate(steps):
    focal = (j == FOCAL_STEP)
    fill = f"{ACC}33" if focal else "rgba(245,245,245,0.10)"
    border = ACC if focal else RULE
    d.o.append(f'<rect x="{step_cx(j) - 18}" y="{Y0 + 6}" width="36" height="18" rx="4" fill="{fill}" stroke="{border}" stroke-width="0.8"/>')
    d.t(step_cx(j), Y0 + 19, num, 10, ACC if focal else INK, MONO, "middle", 600)
    d.t(step_cx(j), Y0 + 34, lab, 11, ACC if focal else MUTED, KR, "middle", 500)

# ── 레인 라벨 (좌측 컬럼) ──
for k, (name, sub) in enumerate(lanes):
    d.t(label_col_w / 2, lane_mid(k) - 6, name, 12, INK, KR, "middle", 600)
    d.t(label_col_w / 2, lane_mid(k) + 12, sub, 10, MUTED, MONO, "middle")

# ── 노드 정의 ──
# (lane_idx, step_idx, title, sub, detail, in_chip, out_chip, color, is_focal)
nodes_def = [
    (0, 0, "원 메일 발송", "IP 198.51.100.1", "From: alice@example.com", "MAIL", "SIGN", OK, False),
    (1, 1, "포워더 수신 검증", "SPF·DKIM 통과", "AAR[i=1] 결과 기록", "PASS", "AAR", OK, False),
    (1, 2, "본문 변형 전달", "IP 변경 · 푸터 추가", "ARC-Seal[i=1] 부착", "MOD", "FWD", WARN, False),
    (2, 3, "수신 MTA 검증", "SPF fail · DKIM fail", "DMARC reject 위기", "FAIL", "REJ", BAD, False),
    (2, 4, "ARC 증거 평가", "AS 봉인 체인 확인", "(로컬 정책) 수락 가능", "ARC", "PASS", ACC, True),
]

for k, j, title, sub, detail, cin, cout, col, focal in nodes_def:
    nx, ny = node_x(j), node_y(k)
    bg = PAPER2
    sw = 1.6 if focal else 1.0
    d.box(nx, ny, node_w, node_h, bg, col, sw, r=6)
    
    # 노드 텍스트 (한글 11px 이상 엄격 준수)
    d.t(nx + node_w / 2, ny + 19, title, 12, INK, KR, "middle", 600)
    d.t(nx + node_w / 2, ny + 35, sub, 11, col if focal or col != OK else MUTED, KR if "·" in sub or "fail" not in sub else MONO, "middle")
    d.t(nx + node_w / 2, ny + 50, detail, 10 if "@" in detail else 11, MUTED, MONO if "@" in detail or "AAR" in detail or "Seal" in detail else KR, "middle")
    
    # 좌하단 입력 칩 / 우하단 출력 칩
    d.chip(nx + 26, ny + 64, cin, col if focal else MUTED, 9, pad=3)
    d.chip(nx + node_w - 26, ny + 64, cout, col, 9, pad=3)

# ── 노드 연결 화살표 (직각 꺾임) ──
# 1. ORG(0,0) -> FWD(1,1)
x1 = node_x(0) + node_w
y1 = lane_mid(0)
x2 = node_x(1)
y2 = lane_mid(1)
xmid = (x1 + x2) / 2
d.arrow([(x1, y1), (xmid, y1), (xmid, y2), (x2, y2)], INFO, "info", 1.4)

# 2. FWD(1,1) -> FWD(1,2) (같은 레인 수평 화살표)
x1 = node_x(1) + node_w
y1 = lane_mid(1)
x2 = node_x(2)
d.arrow([(x1, y1), (x2, y1)], OK, "ok", 1.4)

# 3. FWD(1,2) -> RCV(2,3)
x1 = node_x(2) + node_w
y1 = lane_mid(1)
x2 = node_x(3)
y2 = lane_mid(2)
xmid = (x1 + x2) / 2
d.arrow([(x1, y1), (xmid, y1), (xmid, y2), (x2, y2)], WARN, "warn", 1.4)

# 4. RCV(2,3) -> RCV(2,4) (같은 레인 수평 화살표)
x1 = node_x(3) + node_w
y1 = lane_mid(2)
x2 = node_x(4)
d.arrow([(x1, y1), (x2, y1)], ACC, "acc", 1.6)

# ── 범례 ──
d.legend(legend_top + 16, [
    ("정상 인증", OK),
    ("중계 변형", WARN),
    ("인증 붕괴", BAD),
    ("ARC 평가·수락", ACC),
    ("전달 흐름", INFO)
])

d.save(Path(__file__).parent.parent / "03-02.forwarding-break.svg")
