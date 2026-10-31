# 07-01 개요 — 키 하나가 샤드에 배정되는 길과 부하 쏠림, 키 범위 할당 및 샤드 분할 전체 지도.
# 사실 출처: 07-01 도입(L16~L18), §1(L28~L36), §2(L42~L44), §3(L50~L58), §4(L64~L70), §5(L76~L84). 칸 라벨은 각 절 본문 낱말.
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

d = D(W, H, "07-01 · CHAPTER OVERVIEW", "샤딩 개요와 키 범위 샤딩 전체 지도",
      "샤딩과 복제 결합(§1), 핫스팟과 스큐(§2), 키 범위 샤딩(§3), 핫스팟 우회(§4), 샤드 분할(§5)의 흐름을 조망한다.",
      "단일 노드 용량 한계 극복 · 부하 쏠림 위험 · 백과사전식 키 범위 · 복합 키 접두어 분산 · 임계치 초과 동적 분할")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "샤딩의 목적: 각 레코드는 하나의 샤드에 속하고 데이터와 쓰기 처리를 여러 노드에 분산", 12, INK, KR, "middle", 600)

CW = 152
GAP = 14
X0 = 34

cards = [
    ("§1", "샤딩과 복제", "수평 확장과 내결함성",
     [("단일 노드 용량 초과", "데이터·쓰기 수평 분산"),
      ("복제본 결합 배치", "장애 대응 사본 유지"),
      ("역할 겸임 구조", "리더·팔로워 겸임")],
     INFO),
    ("§2", "핫스팟과 스큐", "부하 쏠림 위험",
     [("스큐 상태 발생", "일부 노드에 부하 집중"),
      ("핫 키 현상", "인기 데이터 요청 폭주"),
      ("수평 확장 무력화", "나머지 노드 유휴 상태")],
     WARN),
    ("§3", "키 범위 샤딩", "백과사전식 구간 할당",
     [("연속 키 범위 배정", "최소~최대 경계 할당"),
      ("데이터 분포 적응", "밀도 맞춤 경계 조정"),
      ("정렬 순서 유지", "효율적 범위 스캔 지원")],
     INFO),
    ("§4", "핫스팟 우회", "복합 키 접두어 분산",
     [("타임스탬프 단독 키", "최신 샤드 쓰기 집중"),
      ("센서 식별자 접두어", "센서 ID 우선 정렬"),
      ("조회 합산 트레이드오프", "클라이언트 개별 질의")],
     ACC),
    ("§5", "샤드 분할", "동적 크기 리밸런싱",
     [("10 GB 임계치 도달", "크기 초과 감지"),
      ("하위 범위 분할", "두 개 연속 범위 분할"),
      ("새 파일 재작성", "고비용 · 과부하 위험")],
     OK),
]

FOCAL = 3

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 24, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 10, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 11.5, SOFT, KR, "middle")
    d.line(x + 10, PY + 56, x + CW - 10, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 54
        d.tone(x + 8, iy, CW - 16, 46, card_c, 4, "10", 0.8)
        d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
        d.t(x + CW / 2, iy + 34, bot_txt, 11.5, MUTED, KR, "middle")

# 하단 범례
d.legend(LEG, [
    ("구조 및 기본 개념", INFO),
    ("병목 및 위험 요소", WARN),
    ("핵심 우회 기법", ACC),
    ("샤드 분할", OK),
])

d.save("07-01.chapter-overview.svg")
