# 12-03 개요 — 스트림 처리 핵심 연산 체계
# 사실 출처: 12-03 서두(L14~L20), §1(L26~L32), §2(L34~L44), §3(L46~L65), §4(L67~L84)
# 원서: DDIA 2nd Edition Ch. 12 "Processing Streams" (p.33~37, p.44~50)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 280
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "12-03 · CHAPTER OVERVIEW", "스트림 처리 핵심 연산 체계",
      "출력 대상 결정에서 시작해 활용 패턴·시간 윈도우 집계·스트림 조인으로 이어지는 처리 구조",
      "세 가지 출력 · 스트림 활용 3종 · 윈도우 분할 4종 · 스트림 조인 3종")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "공통 기반: 무한한 이벤트 스트림의 읽기 전용 소비 및 append-only 파생 스트림 생성", 12, INK, KR, "middle", 600)

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "세 가지 출력 유형", "결과 전달 대상",
     [("저장소 쓰기", "DB · 캐시 · 인덱스 동기화"),
      ("사람 알림", "이메일 · 푸시 · 대시보드"),
      ("새 파생 스트림", "소비 후 append-only 출력")],
     INFO),
    ("§2", "스트림 활용 유형", "목적별 처리 패턴",
     [("복합 이벤트 처리", "이벤트 패턴 탐지 · 규칙 매칭"),
      ("스트림 분석", "시간 윈도우 통계 · 집계 메트릭"),
      ("구체화 뷰 유지", "CDC 변경로그 구독 · 증분 갱신")],
     OK),
    ("§3", "윈도우 집계 유형", "무한 스트림의 유한 분할",
     [("텀블링 윈도우", "고정 길이 · 비중첩 1분 카운트"),
      ("호핑 윈도우", "고정 길이 · 중첩 5분/1분 hop"),
      ("슬라이딩 · 세션", "간격 버퍼 · 비활동 감지")],
     ACC),
    ("§4", "스트림 조인 3종", "지속적 상태 대조",
     [("스트림-스트림", "1시간 세션 ID 윈도우 조인"),
      ("스트림-테이블", "DB CDC 로컬 해시 조인"),
      ("테이블-테이블", "타임라인 캐시 · 구체화 뷰 유지")],
     WARN),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 12, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 11, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 66

        if is_focal and j == 0:
            d.tone(x + 8, iy, CW - 16, 54, ACC, 5, "20", 1.3)
            d.t(x + CW / 2, iy + 22, top_txt, 11, ACC, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif j == 0:
            d.tone(x + 8, iy, CW - 16, 54, card_c, 5, "14", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 11, card_c, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

# 범례
legend_items = [
    ("출력 유형 (§1)", INFO),
    ("활용 유형 (§2)", OK),
    ("윈도우 (§3, focal)", ACC),
    ("스트림 조인 (§4)", WARN),
]
d.line(24, LEG, W - 24, LEG, RULE, 0.8)
d.t(24, LEG + 22, "LEGEND", 8, SOFT, MONO, "start")
lx = 96
for lab, c in legend_items:
    d.o.append(f'<rect x="{lx}" y="{LEG + 12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(lx + 20, LEG + 22, lab, 11, MUTED, KR, "start")
    w_text = sum(11 if "가" <= ch <= "힣" else 7 for ch in lab)
    lx += 26 + w_text + 18

d.save("12-03.chapter-overview.svg")
