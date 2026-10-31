# 12-02 개요 — 듀얼 라이트 한계(§1), CDC(§2), 스키마 변경(§3), 이벤트 소싱 vs CDC(§4), 불변성(§5) 전체 지도.
# 사실 출처: 12-02 본문 서두(L16~L18), §1(L26~L39), §2(L42~L59), §3(L62~L67), §4(L70~L89), §5(L92~L105)
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

d = D(W, H, "12-02 · CHAPTER OVERVIEW", "데이터베이스와 스트림 아키텍처 전체 지도",
      "듀얼 라이트 한계(§1), CDC(§2), 스키마 변경(§3), 이벤트 소싱 비교(§4), 불변성(§5)의 체계.",
      "듀얼 라이트 레이스 컨디션 · 단일 리더 복제 로그 · 아웃박스 패턴 · 불변 이벤트 소싱 · 상태와 스트림 이중성")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "핵심 통찰: 데이터베이스 복제 로그를 스트림으로 추출해 파생 시스템을 일관되게 동기화", 12, INK, KR, "middle", 600)

X0 = 28
CW = 156
GAP = 12

cards = [
    ("§1", "듀얼 라이트", "동기화 한계",
     [("레이스 컨디션", "도착 순서 역전 불일치"),
      ("영구 불일치", "오류 없는 데이터 불일치"),
      ("부분 쓰기 실패", "분산 원자적 커밋 비용")],
     WARN, False),
    ("§2", "CDC 아키텍처", "단일 리더 추출",
     [("단일 리더 순서", "DB 복제 로그 순서 고정"),
      ("비동기 복제 스트림", "원본 쓰기 성능 격리"),
      ("로그 컴팩션", "키별 최신 이벤트만 남김")],
     ACC, True),
    ("§3", "스키마 변경", "공개 계약 관리",
     [("내부 스키마 노출", "하위 소비자 장애 유발"),
      ("아웃박스 패턴", "전용 발행 테이블 분리"),
      ("트랜잭션 원자성", "단일 커밋 경계 내 보장")],
     INFO, False),
    ("§4", "이벤트 소싱", "추상화 수준 비교",
     [("도메인 이벤트", "사용자 의도 직접 표현"),
      ("전체 이력 재생", "로그 재생으로 현재 상태"),
      ("최소 침습 CDC", "기존 뮤터블 DB 적용")],
     OK, False),
    ("§5", "불변성 활용", "장점과 삭제 한계",
     [("상태·이벤트 이중성", "적분과 미분의 대칭성"),
      ("다중 뷰 파생", "감사·복구·병렬 재구축"),
      ("크립토 슈레딩", "삭제 권리와 키 폐기")],
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
    ("핵심 메커니즘 (focal)", ACC),
    ("비교·도메인 모델", OK),
    ("패턴·구조", INFO),
    ("동기화 한계·위험", WARN),
])

d.save("12-02.chapter-overview.svg")
