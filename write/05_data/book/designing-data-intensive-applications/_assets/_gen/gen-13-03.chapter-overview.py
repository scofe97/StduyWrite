# 13-03 개요 — 파생 함수(§1) → 코드·상태 분리(§2) → 쓰기·읽기 경로(§3) → 클라이언트 푸시(§4) → 읽기 이벤트화(§5) 전체 지도.
# 사실 출처: 13-03 본문 서두(L16~L18), §1(L24~L30), §2(L32~L40), §3(L42~L53), §4(L55~L65), §5(L67~L77), 원서 Ch.13 p.19~28
# 2026-10-31 검증: 배너 중립화(INFO 범례색 제거), 라벨을 본문 어휘로(반응형 플로우·MV·컨슈머 오프셋 추적·부정 방지 분산 라우팅 교체)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 244
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "13-03 · CHAPTER OVERVIEW", "데이터플로우 중심 애플리케이션 설계 전체 지도",
      "파생 함수(§1), 코드·상태 분리(§2), 쓰기·읽기 경로(§3), 클라이언트 푸시(§4), 읽기 이벤트화(§5)의 체계.",
      "표준·커스텀 파생 함수 · 수동적 공유 변수 · 쓰기·읽기 경로 경계 이동 · 클라이언트 푸시 · 스트림-테이블 조인")

# 상단 공통 전제 배너
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 23, "데이터베이스 = 수동적 변수 아닌 상태 변경의 흐름 → 애플리케이션 코드와 UI까지 스트림의 일부", 12, INK, KR, "middle", 600)

X0 = 24
CW = 156
GAP = 13

cards = [
    ("§1", "파생 함수", "표준·커스텀 코드",
     [("CREATE INDEX", "표준 함수 DB 내장"),
      ("도메인 특화", "커스텀 파생 로직"),
      ("Unix 파이프", "상태 스트림 합성")],
     INFO, False),
    ("§2", "코드·상태 분리", "수동적 변수 넘어",
     [("스테이트리스", "로직과 상태 분리"),
      ("공유 변수 한계", "변경 알림 부재·폴링"),
      ("데이터플로우 관점", "CDC·액터·트리거·증분 뷰")],
     WARN, False),
    ("§3", "쓰기·읽기 경로", "경로 경계 이동",
     [("쓰기 경로", "즉시 평가·사전 계산"),
      ("읽기 경로", "지연 평가·요청 시 실행"),
      ("경계 이동 도구", "캐시·인덱스·구체화 뷰")],
     ACC, True),
    ("§4", "클라이언트 푸시", "쓰기 경로 연장",
     [("로컬 상태 캐시", "UI는 모델의 구체화 뷰"),
      ("능동적 푸시", "SSE·WebSocket 연결"),
      ("재접속 따라잡기", "놓친 메시지 수신")],
     OK, False),
    ("§5", "읽기 이벤트화", "멀티 샤드 조인",
     [("스트림-테이블 조인", "일회성 읽기·영구 구독"),
      ("인과 추적성", "본 정보 → 결정 재구성"),
      ("멀티 샤드", "라우팅·샤딩·조인 재사용")],
     INFO, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 14, y + 46, role, 11, SOFT, KR, "start")

    d.line(x + 10, y + 58, x + CW - 10, y + 58, RULE, 0.8)

    # 3개 항목
    iy0 = y + 80
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 52
        d.box(x + 8, iy - 14, CW - 16, 44, PAPER, RULE, 0.6)
        d.t(x + 14, iy + 2, head, 12, INK, KR, "start", 600)
        d.t(x + 14, iy + 20, sub, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("핵심 경로 (focal)", ACC),
    ("클라이언트 연장", OK),
    ("아키텍처·인프라", INFO),
    ("전통 모델 한계", WARN),
])

d.save("13-03.chapter-overview.svg")
