# 09-02 개요 — 두 시계 특성(§1), NTP 동기화 한계(§2), 순서 역전 위험(§3), 신뢰 구간(§4), 프로세스 일시 중단(§5)의 전체 체계 지도.
# 사실 출처: 09-02 서두(L13~L19), §1(L23~L35), §2(L37~L47), §3(L49~L57), §4(L59~L67), §5(L69~L88)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
PY1 = 152
CH1 = 196
PY2 = 362
CH2 = 196
LEG = 582
H = LEG + 56

d = D(W, H, "09-02 · CHAPTER OVERVIEW", "불신뢰 시계와 분산 시스템 시간 문제 전체 지도",
      "두 시계의 특성(§1)에서 출발해 NTP 동기화 한계(§2), 타임스탬프 순서 역전(§3), 신뢰 구간 대기(§4), 프로세스 일시 중단(§5)의 체계를 조망한다.",
      "단조 vs 벽시계 · NTP 드리프트와 지연 · LWW 순서 역전 · TrueTime 신뢰 구간 · 프로세스 일시 중단")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "분산 시스템 현실: 노드별 독립 발진기와 가변 네트워크 지연으로 절대 공통 시각 부재", 12, INK, KR, "middle", 600)

GAP = 20
X0 = 24
CW1 = 264

row1_cards = [
    ("§1", "두 종류의 시계", "단조 vs 벽시계",
     [("벽시계 (Time-of-Day)", "1970 UTC 기점 · 뒤로 점프"),
      ("단조 시계 (Monotonic)", "항상 증가 · 경과 시간 측정 · 로컬 전용"),
      ("용도 혼동 시 버그", "이벤트 순서 판단에 벽시계 오용")],
     INFO, False),
    ("§2", "동기화 한계", "NTP 드리프트와 지연",
     [("쿼츠 발진기 드리프트", "최대 200 ppm · 30초마다 6 ms 오차"),
      ("네트워크 왕복 지연", "인터넷 최소 35 ms 오차 · 혼잡 스파이크"),
      ("가상화 환경 시계 점프", "VM 재개 시 시계가 앞으로 뜀")],
     WARN, False),
    ("§3", "순서 위험", "타임스탬프 인과 역전",
     [("클럭 스큐 3 ms 이내", "인과적으로 나중 쓰기가 작은 타임스탬프"),
      ("LWW 충돌 해소 결함", "나중 쓰기 x=2 조용히 유실 (오류 없음)"),
      ("근본 대안: 논리 시계", "단조 카운터로 이벤트 상대 순서 추적")],
     ACC, True),
]

for col, (sec, title, role, items, card_c, is_focal) in enumerate(row1_cards):
    x = X0 + col * (CW1 + GAP)
    y = PY1
    
    if is_focal:
        d.box(x, y, CW1, CH1, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW1, CH1, PAPER2, RULE, 0.9)
    
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 50, y + 42, role, 11.5, SOFT, KR, "start")
    d.line(x + 12, y + 52, x + CW1 - 12, y + 52, RULE, 0.8)
    
    iy0 = y + 74
    for idx, (head, sub) in enumerate(items):
        iy = iy0 + idx * 42
        d.box(x + 12, iy - 14, CW1 - 24, 36, PAPER, RULE, 0.6)
        d.t(x + 20, iy, head, 12, INK, KR, "start", 600)
        d.t(x + 20, iy + 15, sub, 11.5, MUTED, KR, "start")

# Row 1 수평 연결 화살표
for col in range(2):
    x1 = X0 + col * (CW1 + GAP) + CW1
    x2 = x1 + GAP
    y = PY1 + 24
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.2)

# Row 2 (2 cards, width = 406 each)
CW2 = 406
row2_cards = [
    ("§4", "신뢰 구간으로서의 시계", "시계 읽기 = 불확실성 구간 표현",
     [("시계 읽기의 본질", "특정 시점이 아닌 [earliest, latest] 불확실성 구간"),
      ("TrueTime · ClockBound", "두 구간 비중첩 시 선후 보장 · GPS·원자시계 운용"),
      ("의도적 커밋 대기", "신뢰 구간 폭만큼 대기해 이후 트랜잭션과 비중첩 보장")],
     OK),
    ("§5", "프로세스 일시 중단", "비결정적 정지와 리스 만료 위험",
     [("임의 지점의 긴 정지", "GC STW · VM 라이브 마이그레이션 · I/O 대기"),
      ("리스 만료 오판단", "정지 중 리스 만료 인지 불가 · 타 노드로 리더십 이전"),
      ("리더라 믿고 쓰기", "만료된 리스로 쓰기 수행")],
     BAD),
]

for col, (sec, title, role, items, card_c) in enumerate(row2_cards):
    x = X0 + col * (CW2 + GAP)
    y = PY2
    
    d.box(x, y, CW2, CH2, PAPER2, RULE, 0.9)
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 50, y + 42, role, 11.5, SOFT, KR, "start")
    d.line(x + 12, y + 52, x + CW2 - 12, y + 52, RULE, 0.8)
    
    iy0 = y + 74
    for idx, (head, sub) in enumerate(items):
        iy = iy0 + idx * 42
        d.box(x + 12, iy - 14, CW2 - 24, 36, PAPER, RULE, 0.6)
        d.t(x + 20, iy, head, 12, INK, KR, "start", 600)
        d.t(x + 20, iy + 15, sub, 11.5, MUTED, KR, "start")

# §3에서 §4 및 §5로의 연결 화살표
x_s3 = X0 + 2 * (CW1 + GAP) + CW1 / 2
d.arrow([(x_s3 - 50, PY1 + CH1), (x_s3 - 50, PY2 - 8), (X0 + CW2 / 2, PY2 - 8), (X0 + CW2 / 2, PY2)], OK, "ok", 1.2)
d.arrow([(x_s3 + 50, PY1 + CH1), (x_s3 + 50, PY2 - 8), (X0 + CW2 + GAP + CW2 / 2, PY2 - 8), (X0 + CW2 + GAP + CW2 / 2, PY2)], BAD, "bad", 1.2)

d.legend(LEG, [
    ("인과 역전 위험 (focal)", ACC),
    ("시계 기초", INFO),
    ("물리적 한계", WARN),
    ("신뢰 구간 대기", OK),
    ("동작 정지 위험", BAD),
])

d.save("09-02.chapter-overview.svg")
