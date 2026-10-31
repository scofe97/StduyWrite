# 02-02 개요 — 처리량·응답 시간의 정의에서 메타스테이블 실패, 처리 구간 분해, 백분위 분포와 꼬리 지연, 다중 호출 증폭과 SLO·SLA로 이어지는 성능 체계 지도.
# 사실 출처: 02-02 서두(L21~L29), §1(L33~L43), §2(L47~L58), §3(L63~L82), §4(L85~L102), §5(L106~L118)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "02-02 · CHAPTER OVERVIEW", "성능 metric과 응답 시간 분포 전체 지도",
      "처리량과 응답 시간 정의(§1), 메타스테이블 실패(§2), 지연과 처리 구간 분해(§3), 백분위 분포와 꼬리 지연(§4), 꼬리 지연 증폭과 SLO·SLA(§5)를 조망한다.",
      "기본 metric 정의 · 과부하 악순환 · 처리 구간 분해 · 백분위 분포 측정 · 꼬리 증폭과 목표 관리")

CW = 156
GAP = 16
X0 = 16

cards = [
    ("§1", "응답 시간과 처리량", "두 핵심 metric과 큐잉",
     [("응답 시간 metric", "사용자 경험 직결"),
      ("초당 처리량 metric", "서버 자원·비용 결정"),
      ("큐잉 지연 급증", "부하 증가 시 대기")],
     INFO),
    ("§2", "메타스테이블 실패", "과부하 악순환과 완화",
     [("retry storm 악순환", "타임아웃과 재전송"),
      ("과부하 고착 상태", "리부트 전 회복 불가"),
      ("과부하 완화 기법", "백오프 · 로드 셰딩")],
     WARN),
    ("§3", "지연과 응답 시간", "요청 처리 구간 분해",
     [("클라이언트 응답 시간", "전체 지연 포함 관측"),
      ("실제 서비스 시간", "서버 요청 처리 구간"),
      ("큐잉 및 네트워크 지연", "대기 시간과 전달 지연")],
     INFO),
    ("§4", "평균·중앙값·백분위", "응답 시간 분포 평가",
     [("산술 평균의 한계", "전형적 응답을 알 수 없음"),
      ("중앙값 p50 기준", "전형적 대기 시간 관측"),
      ("꼬리 지연 백분위", "p95 · p99 · p999")],
     ACC),
    ("§5", "꼬리 증폭과 SLO·SLA", "다중 호출과 성능 계약",
     [("꼬리 지연 증폭 현상", "병렬 호출 중 최장 대기"),
      ("SLO · SLA 목표 정의", "백분위 기반 성능 계약"),
      ("히스토그램 기반 집계", "백분위 평균은 무의미")],
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

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + CW / 2, PY + 20, sec, card_c, 11)
    d.t(x + CW / 2, PY + 42, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 58, role, 11.5, SOFT, KR, "middle")
    d.line(x + 12, PY + 68, x + CW - 12, PY + 68, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 76 + j * 60

        if is_focal and j == 1:
            d.tone(x + 10, iy, CW - 20, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, ACC, KR, "middle")
        elif i == 1 and j == 0:
            d.tone(x + 10, iy, CW - 20, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, WARN, KR, "middle")
        elif (i == 0 and j == 2) or (i == 2 and j == 0):
            d.tone(x + 10, iy, CW - 20, 52, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, INFO, KR, "middle")
        elif i == 4 and j == 1:
            d.tone(x + 10, iy, CW - 20, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, OK, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, MUTED, KR, "middle")

# 카드 간 연결 화살표
for i in range(4):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.2)

d.legend(LEG, [
    ("백분위 분포 (focal)", ACC),
    ("기본 metric·구간", INFO),
    ("과부하 악순환", WARN),
    ("목표 정의·계약", OK)
])

d.save("02-02.chapter-overview.svg")
