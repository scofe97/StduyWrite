# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 구성요소마다 임계 경로의 안과 밖, 실행 방식, 하는 일을 같은 열에 나란히 놓아 경로 안의 주문 관리자와 매칭 엔진이 단일 스레드와 CPU 고정을 받고 나머지가 버스 구독이나 자기 루프로 돕는 모양을 보인다.
# 사실 출처: ByteByteGo system-design-101 low-latency-stock-exchange.md(커밋 b28380a: 임계 경로 = 주문 관리자 입구 → 필수 위험 점검 → 체결 → 주문 관리자 출구, 주문 관리자·매칭 엔진은 단일 스레드이고 각각 CPU 하나에 고정, 나머지는 이벤트 버스를 구독),
#   design-stock-exchange.md(시장 데이터 흐름과 보고 흐름은 임계 경로 밖), 단일 서버 그림의 구성요소(Order Manager·Matching Engine·Market Data Publisher·Reporter·Logging·Aggregated Risk Check·Position Keeper).
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 64, 열 폭 [184, 148, 232, 316], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 548
d = D(W, H, "BYTEBYTEGO · 09-02 §6",
      "주문 관리자와 매칭 엔진은 각각 단일 스레드이고 CPU 하나에 고정된다",
      "나머지 구성요소는 공유 메모리 이벤트 버스를 구독하거나 자기 루프로 돕습니다.",
      "경로 안과 밖의 구분은 같은 서버 안의 구성요소 기준입니다")

cols = [("구성요소", 184), ("임계 경로", 148), ("실행 방식", 232), ("하는 일", 316)]
X0, Y0, HH, RH = 12, 100, 40, 64
x = X0
xs = []
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, fam(nm), "middle", 600)
    x += w

rows = [
    ("주문 관리자", "안", "단일 스레드 · CPU 고정", "주문 입구 · 위험 점검 · 체결 출구", True),
    ("매칭 엔진", "안", "단일 스레드 · CPU 고정", "호가창에서 매수 · 매도를 맞춤", True),
    ("시장 데이터 발행", "밖", "애플리케이션 루프", "봉차트 · 호가창을 데이터 서비스로", False),
    ("Reporter", "밖", "버스 구독", "체결 필드를 DB 에 기록", False),
    ("그 밖의 구성요소", "밖", "버스 구독", "로깅 · 포지션", False),
]
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    focal = row[4]
    for k, val in enumerate(row[:4]):
        cx0, w = xs[k]
        if focal:
            d.tone(cx0, y, w, RH, ACC, 0, "14", 1.4)
            col = ACC if k == 1 else INK
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
            col = INFO if k == 1 else INK
        d.t(cx0 + w / 2, y + 38, val, 13, col, fam(val), "middle", 600 if k < 2 else 400)

d.legend(H - 56, [("임계 경로 안", ACC), ("임계 경로 밖", INFO)])
d.save("09-02.critical-path.svg")
