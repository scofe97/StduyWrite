# 12-04 개요 — 이벤트 시간 vs 처리 시간, 지각 이벤트 처리, exactly-once 4대 전략, 12장 스트림 처리 종합과 배치의 연속성 전체 지도.
# 사실 출처: 12-04 본문 서두(L13~L18), §1(L26~L42), §2(L44~L54), §3(L56~L80), §4(L82~L102), DDIA 2판 Ch.12 (PDF p.40~56). 칸 라벨은 본문 낱말.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 252
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "12-04 · CHAPTER OVERVIEW", "시간 추론과 내결함성·12장 종합 전체 지도",
      "이벤트 시간 vs 처리 시간(§1), 지각 이벤트 처리(§2), exactly-once 4대 전략(§3), 12장 스트림 처리 종합과 배치의 연속성(§4)으로 이어지는 체계를 조망한다.",
      "시간 왜곡 방지 · 지각 이벤트 제어 · 4대 복구 기법 · 스트림-배치 연속성")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "스트림 처리 핵심 과제: 끝없는 데이터 흐름에서 시간 왜곡을 방지하고 장애 시 정확히 한 번 처리를 보장", 12, INK, KR, "middle", 600)

CW = 194
GAP = 14
X0 = 28

cards = [
    ("§1", "시간 추론", "이벤트 시간 vs 처리 시간",
     [("처리 시간 왜곡", "재시작 시 인위적 스파이크"),
      ("이벤트 시간", "타임스탬프 결정론적 재처리"),
      ("클럭 오프셋", "기기-서버 3타임스탬프 보정")],
     INFO),
    ("§2", "지각 이벤트", "윈도우 마감과 워터마크",
     [("전략 1 무시·드롭", "임계치 초과 지각치 폐기"),
      ("전략 2 수정값", "지각치 포함 윈도우 재계산"),
      ("워터마크 마커", "특정 시각 이전 완료 통지")],
     WARN),
    ("§3", "내결함성 보장", "Exactly-Once 4대 전략",
     [("마이크로배치", "소블록 단위 일괄 가시화"),
      ("체크포인트", "주기적 상태 스냅샷 복구"),
      ("원자적 커밋 · 멱등성", "단일 트랜잭션 · 오프셋 중복 방지")],
     OK),
    ("§4", "12장 종합", "스트림과 배치의 연속성",
     [("브로커 패러다임", "AMQP 큐 vs Kafka 로그"),
      ("출처 및 처리 패턴", "CDC 변경로그 · 실시간 조인"),
      ("패러다임 통합", "배치는 스트림의 특수 케이스")],
     ACC),
]

for i, (sec, title, sub, items, c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    d.box(x, PY, CW, PH, PAPER2, c, 1.2)
    d.chip(x + 28, PY + 18, sec, c, 11)
    d.t(x + CW / 2 + 10, PY + 22, title, 12.5, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 42, sub, 11, MUTED, KR, "middle")
    d.line(x + 8, PY + 52, x + CW - 8, PY + 52, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = PY + 64 + j * 58
        d.box(x + 6, iy, CW - 12, 50, PAPER, RULE, 0.8)
        d.t(x + CW / 2, iy + 19, h_txt, 11.5, INK, KR, "middle", 600)
        d.t(x + CW / 2, iy + 37, d_txt, 11, MUTED, KR, "middle")

    if i < len(cards) - 1:
        arr_x = x + CW + 1
        arr_y = PY + PH / 2
        d.arrow([(arr_x, arr_y), (arr_x + GAP - 2, arr_y)], MUTED, "ar", 1.4)

d.legend(LEG, [
    ("시간 추론 (§1)", INFO),
    ("지각 이벤트 (§2)", WARN),
    ("내결함성 (§3)", OK),
    ("12장 종합 (§4)", ACC)
])

d.save("12-04.chapter-overview.svg")
