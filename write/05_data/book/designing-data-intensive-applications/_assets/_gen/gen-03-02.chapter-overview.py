# 타입 스펙: type-architecture — 정규화와 비정규화 축 위에 네 절의 핵심 대상과 기법을 배치한 개요 개념도.
# 사실 출처: 노트 L21(핵심 요약), L29(핵심 질문), L33~L57(§1 ID 참조), L65~L86(§2 trade-off), L90~L116(§3 다대다), L120~L146(§4 ID hydration)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W = 880
CW, CH = 196, 268
GAP = 16
X0 = 24
Y_SPEC = 104
H_SPEC = 28
Y_CARD = 148
LEG = Y_CARD + CH + 28
H = LEG + 56

d = D(W, H, "03-02 · CHAPTER OVERVIEW", "정규화·비정규화 축과 네 절의 설계 선택",
      "정규화(단일 저장·일관성)와 비정규화(복제·읽기 최적화)의 맞바꿈 축 위에 네 절의 핵심 대상과 기법을 배치한다. §2의 맞바꿈이 중심 기준이다.",
      "왼쪽은 단일 저장과 일관성, 오른쪽은 복제와 읽기 성능, 네 절은 이 축 위에서 최적점을 찾습니다.")

# 상단 스펙트럼 밴드
d.box(X0, Y_SPEC, W - X0 * 2, H_SPEC, PAPER2, RULE, 1.0)
d.t(X0 + 16, Y_SPEC + 18, "정규화", 12, OK, KR, "start", 600)
d.t(X0 + 64, Y_SPEC + 18, "단일 저장 · 일관성 보장", 11, MUTED, KR, "start")

d.t(W / 2, Y_SPEC + 18, "읽기 · 쓰기 trade-off 축", 12, ACC, KR, "middle", 600)

d.t(W - X0 - 64, Y_SPEC + 18, "복제 저장 · 읽기 최적화", 11, MUTED, KR, "end")
d.t(W - X0 - 16, Y_SPEC + 18, "비정규화", 12, WARN, KR, "end", 600)

d.arrow([(X0 + 200, Y_SPEC + 14), (X0 + 260, Y_SPEC + 14)], MUTED, "ar", 1.2)
d.arrow([(W - X0 - 200, Y_SPEC + 14), (W - X0 - 260, Y_SPEC + 14)], MUTED, "ar", 1.2)

# 네 절 카드 정의
sections = [
    {
        "sec": "§1 ID 참조",
        "sub": "단일 저장과 변경 안전성",
        "color": OK,
        "items": [
            ("핵심 대상", "지역명 (region_id)"),
            ("저장 방식", "불변 ID 단일 저장"),
            ("변경 장점", "이름 변경 시 1곳 수정"),
            ("읽기 비용", "조인으로 ID 해소"),
        ],
        "focal": False
    },
    {
        "sec": "§2 trade-off",
        "sub": "읽기 · 쓰기 비용 맞바꿈",
        "color": ACC,
        "items": [
            ("핵심 대상", "조직 로고 URL"),
            ("선택 기준", "OLTP vs 분석 시스템"),
            ("정규화", "사본 1개 · 빠른 쓰기"),
            ("비정규화", "사본 다수 · 빠른 읽기"),
        ],
        "focal": True
    },
    {
        "sec": "§3 다대다 관계",
        "sub": "연관 테이블 정규화",
        "color": INFO,
        "items": [
            ("핵심 대상", "사용자-조직 직위"),
            ("저장 구조", "연관 테이블 (positions)"),
            ("효율 쿼리", "양방향 보조 인덱스"),
            ("위험 방지", "양쪽 복제 불일치 차단"),
        ],
        "focal": False
    },
    {
        "sec": "§4 ID hydration",
        "sub": "타임라인 실용적 절충",
        "color": WARN,
        "items": [
            ("핵심 대상", "홈 타임라인 항목"),
            ("캐시 항목", "post_id · sender_id"),
            ("읽기 조인", "본문 · 프로필 병렬 조회"),
            ("절충 이유", "급변 통계 복제 회피"),
        ],
        "focal": False
    }
]

for i, s in enumerate(sections):
    x = X0 + i * (CW + GAP)
    c = s["color"]
    # 카드 외곽
    if s["focal"]:
        d.tone(x, Y_CARD, CW, CH, ACC, 6, "18", 1.4)
    else:
        d.box(x, Y_CARD, CW, CH, PAPER2, RULE, 1.0)

    # 절 헤더
    d.t(x + CW / 2, Y_CARD + 26, s["sec"], 14, c, KR, "middle", 600)
    d.t(x + CW / 2, Y_CARD + 46, s["sub"], 11, MUTED, KR, "middle")
    d.line(x + 12, Y_CARD + 58, x + CW - 12, Y_CARD + 58, RULE, 0.8)

    # 항목 슬롯 4개 (2줄 구성: tag + value)
    item_y0 = Y_CARD + 68
    item_stride = 48
    for j, (tag, val) in enumerate(s["items"]):
        iy = item_y0 + j * item_stride
        d.box(x + 10, iy, CW - 20, 42, PAPER, RULE, 0.8)
        d.t(x + 18, iy + 17, tag, 11, MUTED, KR, "start")
        d.t(x + 18, iy + 33, val, 12, INK, KR, "start")

d.legend(LEG, [
    ("핵심 — trade-off", ACC),
    ("정규화 단일 저장", OK),
    ("엔티티 연관 구조", INFO),
    ("비정규화 절충 · 캐시", WARN)
])

d.save("03-02.chapter-overview.svg")
