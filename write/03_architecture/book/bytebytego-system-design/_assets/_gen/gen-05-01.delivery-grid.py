# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 전달 보장 세 방식을 생산자·소비자 커밋 순서·장애 지점·재시작 위치·결과의 다섯 열로 견준다.
# 사실 출처: Kafka 4.3 설계 문서 Message Delivery Semantics https://kafka.apache.org/43/design/design/#message-delivery-semantics (읽고 위치를 저장한 뒤 처리하면 최대 한 번, 처리한 뒤 위치를 저장하면 최소 한 번, 트랜잭션으로 출력과 위치를 함께 쓰면 정확히 한 번), 생산자 설정 https://kafka.apache.org/43/configuration/producer-configs/. 오프셋 10·11·12·13 은 본문 예시 값.
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 112, 열 폭 [136, 176, 176, 144, 128, 160], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "BYTEBYTEGO · 05-01 §3",
      "커밋 시점이 유실·중복·한 벌을 가른다",
      "소비자가 오프셋 10·11·12 를 받아 처리하다 장애가 났을 때 재시작 위치와 결과가 방식마다 다릅니다",
      "오프셋 10~13 은 예시 값입니다")

cols = [("방식", 136), ("생산자", 176), ("소비자 순서", 176), ("장애 지점", 144), ("재시작", 128), ("결과", 160)]
X0, Y0, HH, RH = 12, 104, 40, 112
x = X0
xs = []
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 12, MUTED, KR, "middle", 600)
    x += w

rows = [
    (("최대 한 번", ""), ("재시도 0", "유실 허용"), ("commit 13", "→ 처리"), ("10 처리 직후", ""), ("offset 13", ""), ("11 · 12 유실", ""), BAD),
    (("최소 한 번", ""), ("재전송", "중복 가능"), ("처리 →", "commit 13"), ("commit 직전", ""), ("offset 10", ""), ("10~12 재처리", ""), WARN),
    (("정확히 한 번", ""), ("생산자 ID · 순번", "transactional.id"), ("출력 + offset 13", "한 트랜잭션"), ("트랜잭션 중간", ""), ("offset 10", ""), ("abort · 1벌만 보임", ""), OK),
]
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    c = row[-1]
    for k, cell in enumerate(row[:-1]):
        cx0, w = xs[k]
        last = (k == len(cols) - 1)
        if last:
            d.tone(cx0, y, w, RH, c, 0, "18", 1.2)
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
        a, b = cell
        fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
        if b:
            d.t(cx0 + w / 2, y + 48, a, 12, c if last else INK, fam(a), "middle", 600 if k in (0, 5) else 400)
            d.t(cx0 + w / 2, y + 72, b, 12, MUTED, fam(b), "middle")
        else:
            d.t(cx0 + w / 2, y + 60, a, 12, c if last else INK, fam(a), "middle", 600 if k in (0, 5) else 400)

d.legend(H - 56, [("유실", BAD), ("중복", WARN), ("한 벌", OK)])
d.save("05-01.delivery-grid.svg")
