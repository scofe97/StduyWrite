# 04-05 개요 — 분석용 컬럼 지향 저장의 다섯 최적화 단계 지도.
# 사실 출처: 본문 §1(컬럼 지향 레이아웃), §2(bitmap 압축), §3(행 전체 정렬), §4(벡터화 실행), §5(data cube 집계)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-05 · CHAPTER OVERVIEW", "분석용 컬럼 지향 저장 기술 체계",
      "fact 데이터를 효율적으로 다루기 위해 컬럼 분리 저장에서 시작해 비트맵 압축·행 전체 정렬·벡터화 실행·집계 큐브로 이어지는 최적화 여정을 조망한다.",
      "컬럼 분리 저장 · 비트맵 압축 · 행 단위 정렬 · 벡터화 실행 · 집계 큐브")

CW = 156
GAP = 15
X0 = 20

cards = [
    ("§1", "컬럼 지향 저장", "필요 컬럼만 로드",
     [("fact_sales 저장", "100개 이상 속성"),
      ("개별 컬럼 분리", "date · product 등"),
      ("위치 기반 재조립", "k번째 행 일치")],
     ACC),
    ("§2", "비트맵 인코딩", "값별 비트맵 압축",
     [("distinct 값별 분리", "행마다 1비트 할당"),
      ("희소 비트 압축", "run-length 인코딩"),
      ("비트 연산 필터링", "OR · AND 고속 처리")],
     INFO),
    ("§3", "정렬과 일괄 쓰기", "긴 반복 압축과 적재",
     [("행 전체 단위 정렬", "첫 정렬 키 긴 반복"),
      ("날짜 범위 스캔", "필요 블록만 탐색"),
      ("로그 구조 쓰기", "메모리 버퍼 병합")],
     INFO),
    ("§4", "벡터화 실행", "배치 단위 CPU 가속",
     [("컬럼 값 배치 전달", "연산자 인자 전달"),
      ("SIMD 병렬 처리", "타이트한 루프 실행"),
      ("압축 데이터 직접 연산", "메모리 복사 절감")],
     OK),
    ("§5", "데이터 큐브", "사전 계산 집계 격자",
     [("2차원 교차 집계", "date · product 집계"),
      ("행·열 소계 추출", "특정 질의 즉시 반환"),
      ("질의 유연성 한계", "원본 유지 및 보조")],
     WARN),
]

FOCAL = 0

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)
    
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)
    
    # 카드 헤더
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 11, SOFT, KR, "middle")
    d.line(x + 10, PY + 56, x + CW - 10, PY + 56, RULE, 0.8)
    
    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64
        
        if is_focal and j == 1:
            d.tone(x + 10, iy, CW - 20, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 11.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, ACC, KR, "middle")
        elif i == 4 and j == 2:
            d.tone(x + 10, iy, CW - 20, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 11.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, WARN, KR, "middle")
        elif i == 3 and j == 1:
            d.tone(x + 10, iy, CW - 20, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 11.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, OK, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, MUTED, KR, "middle")

# 카드 간 연결 화살표
for i in range(4):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.2)

d.legend(LEG, [("핵심 저장 모델", ACC), ("압축·정렬 메커니즘", INFO), ("CPU 벡터 연산", OK), ("사전 집계·제약", WARN)])
d.save("04-05.chapter-overview.svg")
