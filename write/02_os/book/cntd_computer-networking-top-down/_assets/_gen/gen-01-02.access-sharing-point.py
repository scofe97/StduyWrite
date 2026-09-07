# 01-02 §2 — 접속망을 가르는 실질 기준은 속도가 아니라 내 선이 어디서부터 남과 합쳐지는가다.
# 타입 스펙: type-data-flow — 단계마다 *누가* 무엇을 하는지. 레인은 접속 방식이고
#           칸 사이를 건너가는 것은 내 패킷이다. 강조 칸이 공유가 시작되는 자리다.
#           축약: §2 공식의 label_col_w 140 · right_pad 28 은 그대로, step_slot_w 는 200,
#           lane_h 는 112 로 올린다(한글 3줄 노드).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, SLOT_W, RIGHT_PAD = 148, 200, 28
HEADER_TOP, HEADER_H, LANE_H, LEGEND_H = 96, 36, 112, 104
STEPS = [("01", "집 안"), ("02", "동네"), ("03", "국사·헤드엔드"), ("04", "인터넷")]
LANES = [("DSL", "TELCO"), ("케이블", "HFC"), ("FTTH · PON", "FIBER")]
NODE_W, NODE_H = 168, 76

W = LABEL_W + len(STEPS) * SLOT_W + RIGHT_PAD
H = HEADER_TOP + HEADER_H + len(LANES) * LANE_H + LEGEND_H

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-02 §2",
      "공유가 시작되는 자리",
      "세 접속망이 집에서 인터넷까지 지나는 구간. 광고 속도가 같아도 체감이 갈리는 이유는 내 선이 어디서부터 이웃과 합쳐지는가에 있다.",
      "강조한 칸부터는 이웃과 나눠 씁니다 — 저녁에 느려지는지가 여기서 갈립니다")

def step_cx(j): return LABEL_W + 16 + j * SLOT_W + NODE_W / 2
def lane_top(k): return HEADER_TOP + HEADER_H + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for j, (num, label) in enumerate(STEPS):
    cx = step_cx(j)
    d.o.append(f'<rect x="{cx - 52}" y="{HEADER_TOP + 6}" width="20" height="18" rx="9" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx - 42, HEADER_TOP + 19, num, 9, MUTED, MONO)
    d.t(cx - 22, HEADER_TOP + 19, label, 11, MUTED, KR, "start", 600)

for k, (name, eyebrow) in enumerate(LANES):
    d.line(LABEL_W, lane_top(k), W - RIGHT_PAD, lane_top(k), RULE, 1.0)
    d.t(20, lane_mid(k) - 2, name, 12, INK, KR, "start", 600)
    d.t(20, lane_mid(k) + 15, eyebrow, 9, SOFT, MONO, "start")
d.line(LABEL_W, lane_top(3), W - RIGHT_PAD, lane_top(3), RULE, 1.0)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(3), RULE, 1.0)

def node(j, k, title, sub, shared=False):
    x, y = step_cx(j) - NODE_W / 2, lane_mid(k) - NODE_H / 2
    if shared: d.tone(x, y, NODE_W, NODE_H, ACC, 6)
    else: d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 1.0, 6)
    d.t(x + NODE_W / 2, y + 30, title, 11, ACC if shared else INK, KR, "middle", 600)
    d.t(x + NODE_W / 2, y + 52, sub, 11, MUTED, KR)

ROWS = [
    [("DSL 모뎀", "전화선 한 가닥", False), ("전용 구간", "내 선입니다", False),
     ("DSLAM", "여기서 합쳐집니다", True), ("ISP 라우터", "전화 회사가 ISP", False)],
    [("케이블 모뎀", "동축", False), ("동네 접점", "500~5,000 가구", True),
     ("CMTS · 헤드엔드", "브로드캐스트", True), ("ISP 라우터", "케이블 회사가 ISP", False)],
    [("ONT", "전용 광섬유", False), ("splitter", "100가구 미만", True),
     ("OLT", "패킷이 복제됩니다", True), ("ISP 라우터", "전화 회사가 ISP", False)],
]
for k, row in enumerate(ROWS):
    for j, (t, s, sh) in enumerate(row):
        node(j, k, t, s, sh)
    for j in range(3):
        x0 = step_cx(j) + NODE_W / 2
        x1 = step_cx(j + 1) - NODE_W / 2
        d.arrow([(x0, lane_mid(k)), (x1 - 4, lane_mid(k))], MUTED, "ar", 1.2)

d.t(LABEL_W, lane_top(3) + 28,
    "DSL 은 국사까지 내 선이라 공유가 늦게 시작되지만, 대신 국사에서 5~10마일 안에 있어야 합니다",
    11, MUTED, KR, "start")

d.legend(H - 62, [("이웃과 나눠 쓰는 구간", ACC), ("나 혼자 쓰는 구간", MUTED)])
d.save("01-02.access-sharing-point.svg")
