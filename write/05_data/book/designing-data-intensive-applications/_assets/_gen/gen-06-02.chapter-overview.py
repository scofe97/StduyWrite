# 06-02 개요 — 노드 장애 처리(팔로워 복구·리더 failover)와 복제 로그 세 방식의 구현 전체 지도.
# 사실 출처: 06-02 서두(L17~L21), §1(L25~L30), §2(L34~L50), §3(L56~L63)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "06-02 · CHAPTER OVERVIEW", "노드 장애 처리와 복제 로그 전체 지도",
      "팔로워 장애의 catch-up 복구, 리더 장애의 failover와 위험 함정, 복제 로그 세 방식의 구현과 결합도 비교를 조망한다.",
      "팔로워 catch-up 복구 · 리더 failover 단계와 함정 · statement·WAL·logical 복제 로그 구현")

# 상단 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "목표: 결함·계획된 유지보수로 노드가 내려가도 시스템 전체는 계속 동작", 12, INK, KR, "middle", 600)

CW = 252
GAP = 26
X0 = 36

cards = [
    ("§1", "팔로워 장애 복구", "로컬 로그 기반 catch-up",
     [("로컬 변경 로그", "마지막 처리 트랜잭션 식별"),
      ("끊긴 동안의 변경", "리더에 요청·적용해 따라잡음"),
      ("복구 부하와 로그 보관", "리더 디스크 고갈 · 백업 복원")],
     INFO),
    ("§2", "리더 장애와 failover", "승격 재구성과 네 함정",
     [("failover 세 단계", "장애 판정 · 선출 · 재구성"),
      ("데이터 정합성 위험", "쓰기 폐기 · 외부 시스템 불일치"),
      ("분산 시스템 함정", "split brain · 펜싱 · 타임아웃")],
     ACC),
    ("§3", "복제 로그 구현", "결합도와 운영 트레이드오프",
     [("statement 기반", "SQL 전송 · 비결정 함수 취약"),
      ("WAL shipping", "디스크 바이트 · 저장엔진 강결합"),
      ("logical(row) 로그", "행 단위 변경 · 결합도 분리 · CDC")],
     WARN),
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

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 58

        if is_focal and j == 0:
            d.tone(x + 12, iy, CW - 24, 48, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 1:
            d.tone(x + 12, iy, CW - 24, 48, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 12, iy, CW - 24, 48, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 48, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 failover (focal)", ACC), ("팔로워 복구", INFO), ("복제 로그 구현", WARN), ("결합도 분리 · CDC", OK)])
d.save("06-02.chapter-overview.svg")
