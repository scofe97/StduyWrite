# 04-01 개요 — 단순 append-only 로그, 인메모리 해시 인덱스, 인덱스 trade-off 의 흐름을 조망하는 세 절의 지도.
# 사실 출처: 04-01 서두(L25~L27), §1(L35~L55), §2(L59~L75), §3(L79~L88)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-01 · CHAPTER OVERVIEW", "OLTP 저장과 인덱스 기초 전체 지도",
      "가장 단순한 append-only 로그에서 출발해 인메모리 해시 인덱스를 거쳐 인덱스의 근본 trade-off에 이르는 저장 엔진 설계 여정을 조망한다.",
      "순차 추가 저장 · 바이트 offset 색인 · 읽기 가속과 쓰기 비용 절충")

CW = 252
GAP = 26
X0 = 36

cards = [
    ("§1", "append-only 로그", "순차 추가 저장 기초",
     [("db_set 추가", "파일 끝 추가 · 효율적 쓰기"),
      ("옛 값 보존", "마지막 등장이 최신 값"),
      ("db_get 조회", "전체 파일 O(n) 스캔 한계")],
     INFO),
    ("§2", "인메모리 해시 인덱스", "바이트 offset 색인",
     [("키-offset 매핑", "RAM 해시 맵으로 위치 추적"),
      ("seek 1회 직접 조회", "캐시 적중 시 디스크 I/O 없음"),
      ("네 가지 구조 한계", "공간 · 비영속 · 메모리 · 범위")],
     ACC),
    ("§3", "인덱스 trade-off", "읽기 가속과 쓰기 비용",
     [("파생 추가 구조", "원본 데이터 무영향 · 재구축 가능"),
      ("쓰기 오버헤드", "데이터 쓰기마다 인덱스 갱신"),
      ("수동 인덱스 선택", "전형적 쿼리 패턴 기준")],
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
    
    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)
    
    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64
        
        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif i == 1 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 2 and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
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

d.legend(LEG, [("핵심 인덱스 (focal)", ACC), ("저장·조회 기초", INFO), ("설계 trade-off", OK), ("구조 한계·비용", WARN)])
d.save("04-01.chapter-overview.svg")
