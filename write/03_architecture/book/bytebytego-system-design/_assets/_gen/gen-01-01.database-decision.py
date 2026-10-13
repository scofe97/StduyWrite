# 타입 스펙: type-flowchart — 데이터 모양(구조화·반구조화·비구조화)에서 시작해 던지는 질문을 거쳐 데이터베이스 범주 12종으로 가르는 결정 트리. 마름모 없이 질문 상자를 쓴 가지(분기 3·9·1).
# 사실 출처: 추출본 v1.txt 577~640행(구조화 SQL 테이블 · 반구조화 JSON·XML · 비구조화 Blob, 범주 12종 나열)과 쪽 20 그림의 질문 라벨(ACID 트랜잭션 OLTP · 분석 OLAP · 사전 · 캐시 · 2차원 키-값 · 시계열 · 감사 이력 · 위치 · 개체 관계 · 중첩 객체 · 전문 검색 · 파일).
# Layout conventions: 열 3(그룹 x=24·폭 180 / 질문 x=300·폭 252 / 범주 x=648·폭 220), 행 stride 48(첫 행 y=128, 12행), 버스 x=252. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W = 920
ROW0, STRIDE, RH = 128, 48, 36
rows = [
    # (그룹 인덱스, 질문, 범주)
    (0, "ACID 트랜잭션 · OLTP", "관계형"),
    (0, "분석 · OLAP", "컬럼형"),
    (1, "사전식 조회", "키-값"),
    (1, "캐시", "인메모리"),
    (1, "2차원 키-값", "와이드 컬럼"),
    (1, "시계열", "시계열"),
    (1, "감사 이력", "불변 원장"),
    (1, "위치 · 지리 개체", "지리 공간"),
    (1, "개체 관계", "그래프"),
    (1, "중첩 객체 · XML · JSON", "문서"),
    (1, "전문 검색", "텍스트 검색"),
    (2, "파일 · 이미지 · 영상", "Blob"),
]
groups = [("구조화", "SQL 테이블 스키마", INFO), ("반구조화", "JSON · XML", WARN), ("비구조화", "Blob", OK)]
H = ROW0 + 11 * STRIDE + RH + 20 + 44
d = D(W, H, "BYTEBYTEGO · 01-01 §5",
      "데이터 모양에서 데이터베이스 범주까지",
      "데이터가 어떤 모양인지 먼저 정하고, 그 모양에 던질 질문이 범주를 고릅니다",
      "범주 12종")

GX, GW, QX, QW, CX, CW, BUS = 24, 180, 300, 252, 648, 220, 252
d.t(GX + GW / 2, 108, "데이터 모양", 12, SOFT, KR, "middle", 600)
d.t(QX + QW / 2, 108, "던지는 질문", 12, SOFT, KR, "middle", 600)
d.t(CX + CW / 2, 108, "범주", 12, SOFT, KR, "middle", 600)

# 그룹별 행 범위
span = {}
for i, (g, q, c) in enumerate(rows):
    lo, hi = span.get(g, (i, i))
    span[g] = (min(lo, i), max(hi, i))

for gi, (name, sub, col) in enumerate(groups):
    lo, hi = span[gi]
    y_top = ROW0 + lo * STRIDE
    y_bot = ROW0 + hi * STRIDE + RH
    gh = 56
    gy = (y_top + y_bot) / 2 - gh / 2   # 그룹 상자 중심을 행 범위의 중점에 맞춘다
    d.tone(GX, gy, GW, gh, col, 6, "14", 1.3)
    d.t(GX + GW / 2, gy + 24, name, 13, col, KR, "middle", 600)
    d.t(GX + GW / 2, gy + 44, sub, 12, MUTED, KR)
    gcy = gy + gh / 2
    for i in range(lo, hi + 1):
        qy = ROW0 + i * STRIDE + RH / 2
        pts = [(GX + GW + 2, gcy), (BUS, gcy), (BUS, qy), (QX - 6, qy)]
        if abs(gcy - qy) < 0.5:
            pts = [(GX + GW + 2, gcy), (QX - 6, qy)]
        d.arrow(pts, col, {INFO: "info", WARN: "warn", OK: "ok"}[col], 1.2)

for i, (g, q, c) in enumerate(rows):
    y = ROW0 + i * STRIDE
    col = groups[g][2]
    d.box(QX, y, QW, RH, PAPER2, RULE, 0.9, 4)
    d.t(QX + QW / 2, y + 23, q, 13, INK, KR, "middle")
    d.arrow([(QX + QW + 2, y + RH / 2), (CX - 6, y + RH / 2)], MUTED, "ar", 1.2)
    d.tone(CX, y, CW, RH, col, 4, "12", 1.1)
    d.t(CX + CW / 2, y + 23, c, 13, col, KR if c != "Blob" else MONO, "middle", 600)

d.legend(H - 44, [("구조화", INFO), ("반구조화", WARN), ("비구조화", OK)])
d.save("01-01.database-decision.svg")
