# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 같은 재고 10 개에 같은 요청 세 개가 동시에 올 때 읽기와 쓰기를 나눈 차감과 조건부 원자 차감이 남기는 재고 값을 행마다 맞대 놓는다.
# 사실 출처: 추출본 v1.txt 3816~3850행(과판매는 나쁘다·차감 시점이 중요하다·주문 성공 뒤 품절 통지는 안 된다), Redis 문서 Transactions(GET·SET 분리 시 두 클라이언트가 같은 10 을 읽어 11 로 쓰는 경쟁 조건), Redis 문서 DECRBY·INCRBY(수량만큼 빼고 되돌림),
#   MySQL 8.4 문서 InnoDB Locks Set by Different SQL Statements(UPDATE ... WHERE 는 만난 레코드에 배타 잠금)·UPDATE(실제로 바뀐 행 수를 돌려줌). 재고 10 개와 요청 수량 4 는 문서용 예시다.
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 88, 열 폭 [140, 100, 346, 346], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "BYTEBYTEGO · 07-03 §7",
      "재고 10 개에 4 개씩 세 요청이 겹치면 분리된 차감만 과판매한다",
      "읽기와 쓰기를 나눈 차감과 재고가 요청 수량 이상일 때만 빼는 원자 차감의 재고 값을 요청마다 맞댑니다.",
      "재고와 수량은 문서용 예시이고 세 요청은 같은 순간에 도착합니다")

cols = [("요청", 140), ("수량", 100), ("읽기와 쓰기를 나눈 차감", 346), ("조건부 원자 차감", 346)]
X0, Y0, HH, RH = 12, 104, 40, 88
x = X0
xs = []
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, KR, "middle", 600)
    x += w

rows = [
    (("요청 A", ""), ("4", ""), ("읽기 10 → 쓰기 6", "읽기 모두 끝난 뒤 쓰기"), ("10 → 6", "성공"), INK, OK),
    (("요청 B", ""), ("4", ""), ("읽기 10 → 쓰기 6", "읽기 모두 끝난 뒤 쓰기"), ("6 → 2", "성공"), INK, OK),
    (("요청 C", ""), ("4", ""), ("읽기 10 → 쓰기 6", "읽기 모두 끝난 뒤 쓰기"), ("2 → 거절", "2 < 4"), INK, WARN),
    (("저장된 재고", "판매 수량"), ("합 12", ""), ("6 · 판매 12", "재고 10 에서 과판매 2"), ("2 · 판매 8", "과판매 없음"), INK, OK),
]
FOCAL = (3, 2)  # 분리된 차감이 남기는 결과 칸: 재고 10 개에 12 개를 판다.
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    for k, cell in enumerate(row[:4]):
        cx0, w = xs[k]
        if (r, k) == FOCAL:
            d.tone(cx0, y, w, RH, ACC, 0, "14", 1.4)
        elif k == 2:
            d.tone(cx0, y, w, RH, BAD, 0, "18", 1.2)
        elif k == 3:
            d.tone(cx0, y, w, RH, row[5], 0, "18", 1.2)
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
        a, b = cell
        if (r, k) == FOCAL:
            col = ACC
        elif k == 2:
            col = BAD
        elif k == 3:
            col = row[5]
        else:
            col = INK
        if b:
            d.t(cx0 + w / 2, y + 36, a, 13, col, fam(a), "middle", 600 if k in (0, 2, 3) else 400)
            d.t(cx0 + w / 2, y + 60, b, 13, MUTED, fam(b), "middle")
        else:
            d.t(cx0 + w / 2, y + 48, a, 13, col, fam(a), "middle", 600 if k in (0, 2, 3) else 400)

d.legend(H - 56, [("과판매 경로", BAD), ("성공", OK), ("거절", WARN), ("이 절의 초점", ACC)])
d.save("07-03.stock-grid.svg")
