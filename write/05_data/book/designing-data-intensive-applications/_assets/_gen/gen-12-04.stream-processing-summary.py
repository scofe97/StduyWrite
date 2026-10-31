# 12-04 §4 — 12장 종합: 스트림 처리 전체 체계(브로커·CDC·조인·시간추론·내결함성)와 배치 처리의 연속성.
# 사실 출처: 12-04 본문 §4(L82~L102), DDIA 2판 Ch.12 "Summary" (PDF p.54~56).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Y1 = 156
CARD_H1 = 150
Y2 = Y1 + CARD_H1 + 16
CARD_H2 = 120
PANEL_Y = Y2 + CARD_H2 + 16
LEG = PANEL_Y + 54 + 18
H = LEG + 52

d = D(W, H, "12-04 · §4 CHAPTER SUMMARY", "12장 스트림 처리 전체 체계와 배치의 연속성",
      "브로커 인프라부터 데이터베이스 CDC, 윈도우 조인, 시간 추론, 내결함성에 이르는 12장 전체 스트림 처리 아키텍처와 배치와의 연속성을 종합한다.",
      "브로커 2대 축 · DB 스트림화 · 윈도우 조인 · 시간 추론 통제 · 배치-스트림 연속성")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "패러다임 통합: 배치는 스트림의 특수 케이스 (유한 입력 = 종료 신호를 받은 스트림 처리)", 11.5, INK, KR, "middle", 600)

# 상단 3개 카드 (Col 1~3, 상하 2줄 배치로 수평 충돌 방지)
CW1 = 264
GAP1 = 16
cards_top = [
    (28, Y1, "메시지 전달 인프라", "브로커 2대 아키텍처", INFO,
     [("AMQP/JMS", "파괴적 소비 · 메시지 단위 ACK"),
      ("로그 기반 브로커", "비파괴적 저장 · 오프셋 순차 재생")]),
    (28 + CW1 + GAP1, Y1, "데이터베이스 연계", "불변 로그와 상태 동기화", OK,
     [("변경 데이터 캡처 (CDC)", "DB 복제 로그 기반 파생 시스템 동기화"),
      ("이벤트 소싱", "불변 사실 기록 · 상태 구체화 뷰")]),
    (28 + (CW1 + GAP1) * 2, Y1, "연산 및 조인 패턴", "실시간 분석과 윈도우 조인", WARN,
     [("CEP 및 실시간 분석", "패턴 탐지 · 윈도우 집계 분석"),
      ("스트림 조인 3종", "스트림-스트림 · 테이블 조인 상태")]),
]

for (cx, cy, c_title, c_sub, c_color, items) in cards_top:
    d.box(cx, cy, CW1, CARD_H1, PAPER2, c_color, 1.2)
    d.t(cx + CW1 / 2, cy + 22, c_title, 12, INK, KR, "middle", 600)
    d.t(cx + CW1 / 2, cy + 39, c_sub, 11, MUTED, KR, "middle")
    d.line(cx + 10, cy + 48, cx + CW1 - 10, cy + 48, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = cy + 56 + j * 44
        d.box(cx + 8, iy, CW1 - 16, 38, PAPER, RULE, 0.8)
        d.t(cx + 14, iy + 16, h_txt, 11, c_color, KR, "start", 600)
        d.t(cx + 14, iy + 30, d_txt, 11, INK, KR, "start")

# 하단 2개 카드 (Col 1~2)
CW2 = 404
GAP2 = 16
cards_bot = [
    (28, Y2, "시간 추론 체계", "이벤트 시간과 윈도우 마감", INFO,
     [("이벤트 vs 처리 시간", "타임스탬프 결정론성 vs 처리 지연 왜곡"),
      ("지각 이벤트 제어", "워터마크 마커 · 폐기 vs 수정값 발행")]),
    (28 + CW2 + GAP2, Y2, "내결함성 보장", "Exactly-Once 달성 체계", ACC,
     [("4대 복구 기법", "마이크로배치 · 체크포인트 · 원자 커밋 · 멱등성"),
      ("상태 복구 메커니즘", "로컬 상태 분산 스냅샷 및 토픽 복제")]),
]

for (cx, cy, c_title, c_sub, c_color, items) in cards_bot:
    d.box(cx, cy, CW2, CARD_H2, PAPER2, c_color, 1.2)
    d.t(cx + CW2 / 2, cy + 22, c_title, 12, INK, KR, "middle", 600)
    d.t(cx + CW2 / 2, cy + 39, c_sub, 11, MUTED, KR, "middle")
    d.line(cx + 12, cy + 48, cx + CW2 - 12, cy + 48, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = cy + 56 + j * 28
        d.box(cx + 10, iy, CW2 - 20, 24, PAPER, RULE, 0.8)
        d.t(cx + 18, iy + 16, h_txt, 11, c_color, KR, "start", 600)
        d.t(cx + CW2 - 18, iy + 16, d_txt, 11, INK, KR, "end")

# 배치 vs 스트림 비교 패널
PW = (W - 56 - 16) / 2
d.box(28, PANEL_Y, PW, 46, PAPER2, RULE, 1.0)
d.t(28 + PW / 2, PANEL_Y + 18, "배치 처리 패러다임 (11장)", 11.5, INFO, KR, "middle", 600)
d.t(28 + PW / 2, PANEL_Y + 34, "유한 데이터셋 · 태스크 완료 후 출력 일괄 가시화", 11, MUTED, KR, "middle")

d.box(28 + PW + 16, PANEL_Y, PW, 46, PAPER2, RULE, 1.0)
d.t(28 + PW + 16 + PW / 2, PANEL_Y + 18, "스트림 처리 패러다임 (12장)", 11.5, OK, KR, "middle", 600)
d.t(28 + PW + 16 + PW / 2, PANEL_Y + 34, "무한 데이터 흐름 · 연속 출력 및 세밀한 상태 복구 체계", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("브로커 · 시간 추론", INFO),
    ("DB 연계", OK),
    ("연산 · 조인", WARN),
    ("내결함성", ACC)
])

d.save("12-04.stream-processing-summary.svg")
