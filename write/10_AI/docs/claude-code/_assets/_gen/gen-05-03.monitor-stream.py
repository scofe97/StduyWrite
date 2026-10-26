"""Monitor 도구의 이벤트 스트림 감시와 세션 기상 흐름 데이터 플로우."""
# 타입 스펙: type-data-flow
# 사실 출처: 05-03.Background Tasks.md:110-161 · 원문 09-advanced-features/README.md:126-162
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 460
LABEL_W = 148
N_STEPS = 4
N_LANES = 3
STEP_W = (W - LABEL_W - 28) // N_STEPS  # 196
LANE_H = 80
Y_START = 100
HEADER_H = 34
Y_LANES = Y_START + HEADER_H  # 134

d = D(
    W, H,
    "MONITOR TOOL · EVENT STREAM FLOW",
    "Monitor 도구의 이벤트 스트림 감시와 세션 기상 흐름",
    "백그라운드 명령 stdout을 라인 버퍼링 파이프로 감시하여 매칭 이벤트 발생 시 세션을 깨우는 데이터 흐름",
    lead="불일치 출력은 토큰 소모 없이 무시하고 일치 로그 라인이 발생하는 즉시 세션을 깨웁니다",
)

# 1. 헤더 (단계 표시)
steps = [
    ("01", "EMIT", False),
    ("02", "BUFFER", False),
    ("03", "FILTER", False),
    ("04", "WAKE", True),
]

for j, (num, lab, focal) in enumerate(steps):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    c = ACC if focal else SOFT
    d.o.append(f'<rect x="{cx - 20}" y="{Y_START + 2}" width="40" height="16" rx="8" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, Y_START + 14, num, 9, c, MONO, "middle", 600)
    d.t(cx, Y_START + 28, lab, 10, ACC if focal else MUTED, MONO, "middle", 600)

# 2. 레인 구분선 및 라벨
lanes = [
    ("로그 소스", "SRC · tail -F", INFO),
    ("Monitor 파이프", "MON · grep", ACC),
    ("대화 세션", "SES · Claude", OK),
]

for k, (name, role_code, col) in enumerate(lanes):
    ly = Y_LANES + k * LANE_H
    if k % 2 == 1:
        d.o.append(f'<rect x="{LABEL_W}" y="{ly}" width="{W - LABEL_W - 16}" height="{LANE_H}" fill="#161B22" opacity="0.6"/>')
    d.line(16, ly, W - 16, ly, RULE, 0.8)
    d.t(LABEL_W // 2, ly + 28, role_code, 9, col, MONO, "middle", 600)
    d.t(LABEL_W // 2, ly + 46, name, 12, INK, KR, "middle", 600)

d.line(16, Y_LANES + N_LANES * LANE_H, W - 16, Y_LANES + N_LANES * LANE_H, RULE, 0.8)
d.line(LABEL_W, Y_START, LABEL_W, Y_LANES + N_LANES * LANE_H, RULE, 0.8)

# 3. 노드 정의 (lane, step, title, sub, focal, col)
NODE_W, NODE_H = 140, 50

nodes_data = [
    # Lane 0: 로그 소스
    (0, 0, "로그 스트림 방출", "tail -F server.log", False, INFO),
    # Lane 1: Monitor 파이프
    (1, 0, "감시 수명", "최대 30분 · -p 10분", False, SOFT),
    (1, 1, "라인 버퍼 통과", "--line-buffered", False, OK),
    (1, 2, "패턴 매칭 판정", "ERROR|FATAL", False, OK),
    (1, 3, "기상 이벤트 발송", "일치 라인 즉시 통지", True, ACC),
    # Lane 2: Claude 세션
    (2, 2, "유휴 대기 (조용)", "0 토큰 소모", False, SOFT),
    (2, 3, "세션 기상", "후속 작업 진행", False, OK),
]

for k, j, title, sub, focal, col in nodes_data:
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    x = cx - NODE_W // 2
    y = Y_LANES + k * LANE_H + (LANE_H - NODE_H) // 2

    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, r=6, op="18", sw=1.4)
        d.t(cx, y + 20, title, 12, ACC, KR, "middle", 600)
        d.t(cx, y + 36, sub, 11, INK, KR, "middle")
    else:
        d.box(x, y, NODE_W, NODE_H, fill=PAPER2, stroke=col, sw=0.9, r=6)
        d.t(cx, y + 20, title, 12, INK, KR, "middle", 600)
        fam = KR if any("가" <= c <= "힣" for c in sub) else MONO
        d.t(cx, y + 36, sub, 11, MUTED, fam, "middle")

# 4. 화살표
def node_pos(k, j):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    cy = Y_LANES + k * LANE_H + LANE_H // 2
    return cx, cy

# (0, 0) -> (1, 1) : 소스에서 라인버퍼로 (오른쪽으로 직각 연결)
x0, y0 = node_pos(0, 0)
x1, y1 = node_pos(1, 1)
x2, y2 = node_pos(1, 2)
x3, y3 = node_pos(1, 3)
x_s2, y_s2 = node_pos(2, 2)
x_s3, y_s3 = node_pos(2, 3)

d.arrow([(x0 + NODE_W // 2, y0), (x1 - NODE_W // 2 - 16, y0), (x1 - NODE_W // 2 - 16, y1), (x1 - NODE_W // 2, y1)], INFO, "info", 1.4)

# (1, 1) -> (1, 2) : 수평
d.arrow([(x1 + NODE_W // 2, y1), (x2 - NODE_W // 2, y1)], OK, "ok", 1.4)

# (1, 2) -> (2, 2) : 불일치 로그 무시 (수직 하강, 점선)
d.arrow([(x2, y2 + NODE_H // 2), (x_s2, y_s2 - NODE_H // 2)], SOFT, "soft", 1.2, "3 3")

# (1, 2) -> (1, 3) : 매칭 로그 (수평)
d.arrow([(x2 + NODE_W // 2, y1), (x3 - NODE_W // 2, y1)], ACC, "acc", 1.4)
d.t((x2 + x3) // 2, y1 - 8, "일치 감지", 11, ACC, KR, "middle")

# (1, 3) -> (2, 3) : 세션 기상 통지 (수직 하강)
d.arrow([(x3, y3 + NODE_H // 2), (x_s3, y_s3 - NODE_H // 2)], ACC, "acc", 1.5)

# 5. 범례
d.legend(406, [
    ("기상 통지 (Focal)", ACC),
    ("정상 스트림 흐름", OK),
    ("로그 소스", INFO),
    ("유휴 무시 경로", SOFT),
])

d.save("05-03.monitor-stream.svg")
print("Saved 05-03.monitor-stream.svg")
