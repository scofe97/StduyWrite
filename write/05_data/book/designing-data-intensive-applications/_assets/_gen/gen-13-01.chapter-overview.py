# 13-01 개요 — 전문 도구 조합(§1), 데이터플로우 추론(§2), 파생 vs 분산 트랜잭션(§3), 전순서의 한계(§4), 인과성 포착(§5) 전체 지도.
# 사실 출처: 13-01 본문 서두(L16~L18), §1(L27~L30), §2(L35~L40), §3(L45~L57), §4(L63~L71), §5(L76~L86)
# 타입 스펙: type-architecture
# 2026-10-31 검증(cc-ddia-dverify13): "단일 도구 불가피성"(뜻이 반대)·"비동기 일관성 허용 필요"(본문 L67 과 반대)·"단일 노드 분할 불가"·"전순서 대안과 보장" 을 본문 낱말로 바꾸고, §4 에 빠진 오프라인 클라이언트를 넣고, 배너를 §1 범례 색(INFO)에서 중립 상자로 바꿨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 34
PY = 146
PH = 244
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "13-01 · CHAPTER OVERVIEW", "데이터 통합과 전순서의 한계 전체 지도",
      "전문 도구 조합(§1)부터 데이터플로우 추론(§2), 파생 vs 분산 트랜잭션(§3), 전순서의 한계(§4), 인과성 포착(§5)의 흐름.",
      "단일 진실 공급원 · CDC 복제 로그 · 비동기 파생 데이터 · 전순서 브로드캐스트 한계 · 인과성 포착")

# 상단 공통 전제 배너
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 22, "단일 도구로 모든 접근 패턴 불가 → 여러 시스템으로 변환·파생", 12, INK, KR, "middle", 600)

X0 = 24
CW = 156
GAP = 13

cards = [
    ("§1", "전문 도구 조합", "단일 도구의 한계",
     [("저장 엔진 특화", "로그·B트리·컬럼"),
      ("OLTP와 검색 결합", "PostgreSQL·Elasticsearch"),
      ("다중 저장소 유지", "DW·캐시·파이프라인")],
     INFO, False),
    ("§2", "데이터플로우 추론", "단일 쓰기 순서 결정",
     [("System of Record", "쓰기 전순서 결정 주체"),
      ("CDC", "같은 순서로 변경 적용"),
      ("결정론적 재처리", "멱등성 기반 장애 복구")],
     ACC, True),
    ("§3", "파생 vs 트랜잭션", "동기화 트레이드오프",
     [("2PC 원자적 커밋", "참여자 장애 시 전체 중단"),
      ("비동기 로그 파생", "장애 국소화와 독립 복구"),
      ("읽기 최신성", "비동기 — 지연 가능")],
     WARN, False),
    ("§4", "전순서의 한계", "규모 확장 시 순서 미정",
     [("샤딩 로그·지리 분산", "샤드·DC 순서 부재"),
      ("서비스·오프라인 단말", "서비스·단말 간 순서 없음"),
      ("전순서 ≡ 합의", "순서 결정 분담 없음")],
     BAD, False),
    ("§5", "인과성 포착", "인과 의존성만 포착",
     [("임의 순서 허용", "비인과 동시 이벤트"),
      ("논리적 타임스탬프", "코디네이션 없는 정렬"),
      ("원인 이벤트 ID", "결정 전 본 상태 참조")],
     OK, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 26, y + 20, sec, card_c, 11)
    d.t(x + CW / 2 + 14, y + 24, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, y + 46, role, 11, SOFT, KR, "middle")

    d.line(x + 10, y + 56, x + CW - 10, y + 56, RULE, 0.8)

    # 3개 항목
    iy0 = y + 74
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 54
        if is_focal and i_idx == 1:
            d.tone(x + 8, iy - 8, CW - 16, 46, ACC, 4, "22", 1.2)
            d.t(x + CW / 2, iy + 10, head, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 27, sub, 11, ACC, KR, "middle")
        else:
            d.box(x + 8, iy - 8, CW - 16, 46, PAPER, RULE, 0.6)
            d.t(x + CW / 2, iy + 10, head, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 27, sub, 11, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(4):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + 24
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.2)

d.legend(LEG, [
    ("핵심 메커니즘 (focal)", ACC),
    ("동기화 트레이드오프", WARN),
    ("분산 확장 한계", BAD),
    ("인과성 대안", OK),
    ("전제", INFO),
])

d.save("13-01.chapter-overview.svg")
