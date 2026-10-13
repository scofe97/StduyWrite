# 타입 스펙: type-process — 같은 서버 넷(Source · Replica1~3)을 다섯 단계 칸마다 같은 자리에 다시 그려, 칸 사이의 역할 변화가 곧 승격 절차가 되게 한다.
# 사실 출처: MySQL 9.7 Reference Manual 19.4.8 Switching Sources During Failover(Source 하나와 Replica 1·2·3 예시 · STOP REPLICA IO_THREAD · Has read all relay log ·
#   STOP REPLICA · RESET BINARY LOGS AND GTIDS · CHANGE REPLICATION SOURCE TO SOURCE_HOST='Replica1' · START REPLICA), 추출본 v2.txt 199~207행(승격 · 데이터 최신 아님),
#   PostgreSQL 18 문서 26.2.8(비동기 복제는 커밋된 트랜잭션을 잃을 수 있다)
# Layout conventions: type-process §2 구조(label_col 104 · step_slot 172 · node 폭 156 높이 44 · lane_h 60)를 따른다. 한글 13px 하한 때문에 slot 을 112 → 172 로 키웠고 viewBox 1000 은 계약 범위 안이다. 모든 좌표 4의 배수.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

LABEL_W, SLOT, PAD = 104, 172, 36
W = LABEL_W + 5 * SLOT + PAD   # 1000
HEAD, LANE_H = 120, 60
NODE_W, NODE_H = 156, 44
H = 548

d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-01 §4",
      "source 가 멈추면 Replica1 이 승격된다",
      "MySQL 의 장애 전환 예시: 부 서버가 릴레이 로그를 다 읽은 것을 확인하고, Replica1 을 새 source 로 올린 뒤 나머지 둘이 Replica1 을 따라가게 한다.",
      "같은 네 서버가 단계마다 맡은 역할만 바뀝니다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cx(j):
    return LABEL_W + 8 + j * SLOT + NODE_W // 2


def top(k):
    return HEAD + k * LANE_H


STEPS = ("평상시", "source 정지", "로그 소진 확인", "승격", "재지정")
ROWS = ("Source", "Replica1", "Replica2", "Replica3")
for j, st in enumerate(STEPS):
    d.t(cx(j), 108, st, 13, MUTED, KR, "middle", 600)
d.line(LABEL_W, HEAD, W - PAD, HEAD, RULE, 0.8)
for k, name in enumerate(ROWS):
    d.t(24, top(k) + LANE_H // 2 + 5, name, 13, MUTED, MONO, "start", 600)
    d.line(LABEL_W, top(k + 1), W - PAD, top(k + 1), RULE, 0.8)
d.t(24, top(4) + 24, "명령 · 주의", 13, MUTED, KR, "start", 600)

# (텍스트, 색) — None 색은 중립 상자
CELLS = [
    [("쓰기 수신", OK), ("정지", BAD), ("정지", None), ("정지", None), ("정지", None)],
    [("복제 중", INFO), ("중단", WARN), ("로그 소진", WARN), ("새 source", ACC), ("쓰기 수신", OK)],
    [("복제 중", INFO), ("중단", WARN), ("로그 소진", WARN), ("대기", None), ("Replica1 복제", INFO)],
    [("복제 중", INFO), ("중단", WARN), ("로그 소진", WARN), ("대기", None), ("Replica1 복제", INFO)],
]
for k, row in enumerate(CELLS):
    for j, (txt, c) in enumerate(row):
        x, y = cx(j) - NODE_W // 2, top(k) + 8
        if c is None:
            d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 0.9, 6)
            d.t(cx(j), y + 27, txt, 13, MUTED, kr(txt), "middle", 600)
        else:
            d.tone(x, y, NODE_W, NODE_H, c, 6, "12", 1.4 if c == ACC else 1.2)
            d.t(cx(j), y + 27, txt, 13, c, kr(txt), "middle", 600)

# 명령 줄
yc = top(4) + 8
d.chip(cx(1), yc + 12, "미복제 커밋 유실 가능", WARN, 12)
cmds = {
    2: ("STOP REPLICA IO_THREAD", "Has read all relay log"),
    3: ("STOP REPLICA", "RESET BINARY LOGS", "AND GTIDS"),
    4: ("STOP REPLICA", "CHANGE REPLICATION", "SOURCE TO", "SOURCE_HOST='Replica1'", "START REPLICA"),
}
for j, lines in cmds.items():
    for n, ln in enumerate(lines):
        d.t(cx(j), yc + 12 + n * 20, ln, 12, INK if n < len(lines) - (1 if j == 2 else 0) else MUTED, MONO, "middle")

d.legend(H - 56, [("복제 중", INFO), ("중단 · 확인", WARN), ("승격", ACC), ("쓰기 수신", OK), ("정지", BAD)])
d.save("01-01.replica-promotion.svg")
print("ok replica-promotion")
