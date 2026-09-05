# 02-01 §4 — 캡처 필터가 파이프라인의 어디에 서는가. 커널에서 걸러지므로 버린 프레임은 파일에 없다.
# 타입 스펙: type-data-flow — 단계마다 *누가* 무엇을 하는지. 레인은 실행 주체(하드웨어 · 커널 ·
#           사용자 공간)이고 칸 사이를 건너가는 것은 프레임 자체다.
#           축약: §2 공식의 label_col_w 140 · right_pad 28 은 그대로 쓰고, step_slot_w 는 112→176,
#           lane_h 는 80→112 로 올린다(한글 3줄 노드). 헤더 띠는 제목 블록 아래(y=96)에서 시작한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, SLOT_W, RIGHT_PAD = 140, 176, 28
HEADER_TOP, HEADER_H, LANE_H, LEGEND_H = 96, 36, 112, 96
STEPS = [("01", "수신"), ("02", "거르기"), ("03", "쓰기"), ("04", "읽기")]
LANES = [("하드웨어", "NIC"), ("커널", "KRN"), ("사용자 공간", "USR")]
NODE_W, NODE_H = 156, 76

W = LABEL_W + len(STEPS) * SLOT_W + RIGHT_PAD          # 140 + 704 + 28 = 872
H = HEADER_TOP + HEADER_H + len(LANES) * LANE_H + LEGEND_H
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01 §4",
      "캡처 필터가 서는 자리",
      "프레임이 NIC 에서 파일까지 가는 네 단계. 캡처 필터는 커널 단계에서 매칭하므로 여기서 걸러진 프레임은 디스크에 남지 않고, 디스플레이 필터는 파일이 생긴 뒤부터 작동한다.",
      "두 번째 칸에서 버려진 것은 오른쪽 두 칸 어디에도 나타나지 않습니다")

def step_cx(j): return LABEL_W + 10 + j * SLOT_W + NODE_W / 2
def lane_top(k): return HEADER_TOP + HEADER_H + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

# 헤더 — 단계 번호 칩과 이름
for j, (num, label) in enumerate(STEPS):
    cx = step_cx(j)
    d.o.append(f'<rect x="{cx - 48}" y="{HEADER_TOP + 6}" width="20" height="18" rx="9" '
               f'fill="{ACC if j == 1 else PAPER2}" stroke="{ACC if j == 1 else RULE}" stroke-width="1"/>')
    d.t(cx - 38, HEADER_TOP + 20, num, 9, PAPER if j == 1 else SOFT, MONO)
    d.t(cx - 20, HEADER_TOP + 20, label, 12, ACC if j == 1 else MUTED, KR, "start", 600)

# 레인 라벨과 구분선
for k, (name, key) in enumerate(LANES):
    d.line(0, lane_top(k), W - RIGHT_PAD, lane_top(k), RULE, 0.8)
    d.t(16, lane_mid(k) - 4, name, 12, SOFT, KR, "start", 600)
    d.t(16, lane_mid(k) + 14, key, 9, SOFT, MONO, "start")
d.line(0, lane_top(len(LANES)), W - RIGHT_PAD, lane_top(len(LANES)), RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(len(LANES)), RULE, 0.8)

def node(j, k, title, sub, tool, focal=False, c=None):
    x, y = step_cx(j) - NODE_W / 2, lane_mid(k) - NODE_H / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, NODE_W, NODE_H, c, 8)
    else:
        d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(x + NODE_W / 2, y + 24, title, 13, col, KR, "middle", 600)
    d.t(x + NODE_W / 2, y + 43, sub, 11, MUTED, KR)
    d.t(x + NODE_W / 2, y + 62, tool, 10, MUTED, MONO)

# 연결선 먼저 — 세로로 내려갈 때는 아래 변에서 나가 위 변으로 들어간다(architecture 포트 규칙)
d.arrow([(step_cx(0), lane_mid(0) + NODE_H / 2), (step_cx(0), lane_mid(1)),
         (step_cx(1) - NODE_W / 2 - 4, lane_mid(1))], MUTED, "ar", 1.4)
d.arrow([(step_cx(1) + 44, lane_mid(1) + NODE_H / 2), (step_cx(1) + 44, lane_mid(2)),
         (step_cx(2) - NODE_W / 2 - 4, lane_mid(2))], ACC, "acc", 1.6)
d.arrow([(step_cx(2) + NODE_W / 2, lane_mid(2)), (step_cx(3) - NODE_W / 2 - 4, lane_mid(2))],
        MUTED, "ar", 1.4)
d.arrow([(step_cx(1) - 44, lane_mid(1) + NODE_H / 2), (step_cx(1) - 44, lane_mid(1) + NODE_H / 2 + 32)],
        BAD, "bad", 1.2, dash="4,3")

node(0, 0, "NIC 수신", "promiscuous 가 여기서 갈립니다", "en0 · eth0")
node(1, 1, "캡처 필터", "커널이 BPF 로 매칭합니다", "tcp port 22", focal=True)
node(2, 2, "dumpcap", "snaplen 만큼 잘라 씁니다", "dumpcap -w", c=OK)
node(3, 2, "pcapng 파일", "디스플레이 필터는 여기부터", "Wireshark", c=INFO)

d.t(step_cx(1) - 52, lane_mid(1) + NODE_H / 2 + 48, "버린 프레임은 파일에 없습니다", 11, BAD, KR, "end")
d.legend(H - LEGEND_H + 24,
         [("걸러 내는 지점", ACC), ("잡아 쓰는 쪽", OK), ("저장된 파일", INFO), ("버려짐", BAD)])
d.save("02-01.capture-filter-position.svg")
