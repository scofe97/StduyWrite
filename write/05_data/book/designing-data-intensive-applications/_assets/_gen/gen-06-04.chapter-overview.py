# 06-04 개요 — 멀티리전 지리 분산, 복제 토폴로지, sync engine과 local-first의 세 절을 조망하는 전체 지도.
# 사실 출처: 06-04 서두(L17~L23), §1(L27~L37), §2(L43~L56), §3(L60~L73)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "06-04 · CHAPTER OVERVIEW", "다중 리더 복제 전체 지도",
      "멀티리전 지리 분산, 복제 토폴로지 통신 구조, sync engine과 local-first의 세 절을 조망한다.",
      "로컬 쓰기 처리 · 비동기 복제 전파 · 토폴로지 단일 실패점과 추월 · 기기마다 로컬 DB")

# 상단 배너: 공통 전제 축
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "공통 전제: 복수 노드의 로컬 쓰기 수용과 비동기 양방향 복제 전파", 12, INK, KR, "middle", 600)

CW = 252
GAP = 26
X0 = 36

cards = [
    ("§1", "멀티리전 다중 리더", "리전마다 리더",
     [("인터리전 지연 은닉", "쓰기를 로컬 리전에서 처리"),
      ("리전 독립성 확보", "리전 장애·단절에도 독립 동작"),
      ("약한 일관성 대가", "잔액 음수·유일성 제약 미보장")],
     INFO),
    ("§2", "복제 토폴로지", "통신 경로와 인과 순서",
     [("원형·성형 구조", "단일 노드 장애 시 복제 중단"),
      ("전체 연결 구조", "단일 실패점 없는 내고장성"),
      ("메시지 추월 위험", "version vector 인과 순서 보정")],
     ACC),
    ("§3", "sync engine과 local-first", "기기·탭 단위 극단 확장",
     [("로컬 DB 리더 동작", "UI 즉각 응답 및 오프라인 지속"),
      ("비동기 동기화 엔진", "갱신을 다른 기기에 비동기 복제"),
      ("로컬 중심 소프트웨어", "서비스 종료 뒤에도 작동하는 앱")],
     OK),
]

FOCAL = 1

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 28, PY + 24, sec, card_c, 12)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if i == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("지리 분산", INFO), ("토폴로지·인과 (focal)", ACC), ("local-first", OK), ("장애·제약 한계", WARN)])
d.save("06-04.chapter-overview.svg")
