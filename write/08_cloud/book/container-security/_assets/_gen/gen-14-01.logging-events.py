# 타입 스펙: type-data-flow — 이벤트 일곱이 SIEM 한 곳으로 몰려 경보가 되고 차단으로 이어진다. 일곱째 실패한 동작이 정찰 신호라 focal. (semantic-patterns: Fan-in queue. 7행 fan-in 이라 §2 공식의 lanes≤4 한계를 넘어 stride 로 배치)
# 사실 출처: 노트 L126~L150(일곱 이벤트 표·평균 거의 200일·SIEM·사전 차단 13장)
# Layout conventions: 이벤트 상자 x=40 w=340 h=48, 행 stride 56(y=116+56i), 버스 x=412, SIEM → 경보 → 차단 가로 한 줄(행 3 중심). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 592
d = D(W, H, "CONTAINER SECURITY · 14-01 §3",
      "남겨야 할 컨테이너 이벤트 일곱은 SIEM 으로 모여 경보와 차단이 된다",
      "마지막 이벤트인 실패한 동작이 공격자의 정찰 신호다. 성공한 일만 기록하면 그 단계를 통째로 놓친다.",
      "컨테이너 이벤트 일곱이 SIEM 으로 모여 경보와 차단으로 이어지는 흐름")

ROW0, STRIDE, BH = 116, 56, 48
EV_X, EV_W = 40, 340
BUS_X = 412

EVENTS = [
    ("컨테이너 시작·종료",        "이미지 신원 · 호출한 사용자", False),
    ("시크릿 접근",               "누가 무엇을 읽었는가", False),
    ("권한 변경",                 "권한 상승의 신호", False),
    ("컨테이너 페이로드 변경",    "코드 주입 신호 · 13장 드리프트", False),
    ("인바운드·아웃바운드 연결",  "트래픽의 흐름", False),
    ("볼륨 마운트",               "나중에 민감한 마운트 분석", False),
    ("실패한 동작",               "연결 시도 · 파일 쓰기 · 권한 변경의 실패", True),
]
yc = [ROW0 + i * STRIDE + BH // 2 for i in range(7)]
for i, (name, sub, focal) in enumerate(EVENTS):
    y = ROW0 + i * STRIDE
    c = ACC if focal else MUTED
    if focal:
        d.tone(EV_X, y, EV_W, BH, ACC, 6, "1F", 1.6)
    else:
        d.box(EV_X, y, EV_W, BH, PAPER2, RULE, 0.9)
    d.t(EV_X + 12, y + 20, name, 13, INK, KR, "start", 600)
    d.t(EV_X + 12, y + 38, sub, 13, ACC if focal else MUTED, KR, "start")
    d.line(EV_X + EV_W, yc[i], BUS_X, yc[i], c, 1.6 if focal else 1.2)

# 버스: 일곱 줄이 한 곳으로
MID = yc[3]
d.line(BUS_X, yc[0], BUS_X, yc[6], MUTED, 1.2)
d.line(BUS_X, yc[3], BUS_X, yc[6], ACC, 1.6)    # 일곱째가 합류하는 구간
d.arrow([(BUS_X, MID), (456, MID)], MUTED, "ar", 1.6)

# SIEM → 경보 → 차단
SX, SW = 456, 148
d.tone(SX, MID - 40, SW, 80, INFO, 6, "14", 1.2)
d.t(SX + SW // 2, MID - 4, "SIEM", 16, INK, MONO, "middle", 600)
d.t(SX + SW // 2, MID + 18, "중앙 인사이트", 13, MUTED, KR, "middle")
AX, AW = 636, 120
d.arrow([(SX + SW, MID), (AX, MID)], MUTED, "ar", 1.6)
d.tone(AX, MID - 28, AW, 56, WARN, 6, "14", 1.2)
d.t(AX + AW // 2, MID + 5, "경보", 14, INK, KR, "middle", 600)
BX, BW = 788, 132
d.arrow([(AX + AW, MID), (BX, MID)], MUTED, "ar", 1.6)
d.tone(BX, MID - 28, BW, 56, OK, 6, "14", 1.2)
d.t(BX + BW // 2, MID - 2, "사전 차단", 14, INK, KR, "middle", 600)
d.t(BX + BW // 2, MID + 16, "13장 프로파일", 13, MUTED, KR, "middle")

# 위: 문제 — 식별까지 걸리는 시간
d.tone(SX, ROW0, 920 - SX, BH, BAD, 6, "14", 1.2)
d.t(SX + 12, ROW0 + 20, "침해 식별까지 평균 거의 200일", 13, INK, KR, "start", 600)
d.t(SX + 12, ROW0 + 38, "관찰 + 경보로 단축", 13, MUTED, KR, "start")

# 아래: 실패 미기록의 결과
d.tone(SX, ROW0 + 6 * STRIDE, 920 - SX, BH, BAD, 6, "14", 1.2)
d.t(SX + 12, ROW0 + 6 * STRIDE + 20, "실패 기록 없음", 13, INK, KR, "start", 600)
d.t(SX + 12, ROW0 + 6 * STRIDE + 38, "정찰 단계 통째 누락", 13, MUTED, KR, "start")

d.legend(H - 56, [("이벤트", MUTED), ("수집", INFO), ("경보", WARN), ("차단", OK), ("정찰 신호", ACC), ("놓치는 것", BAD)])
d.save("14-01.logging-events.svg")
