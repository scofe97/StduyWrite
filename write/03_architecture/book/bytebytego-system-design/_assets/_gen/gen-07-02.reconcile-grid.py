# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 같은 주문 번호의 행을 내부 주문 기록·PSP 정산 파일·원장 세 곳에서 나란히 놓고 판정 열로 일치와 불일치를 가른다.
# 사실 출처: 추출본 v1.txt 3283~3290행(주문 $200 은 전자상거래 사이트·PSP·원장 세 곳에 기록되고 원장은 차변 200 대변 200 의 복식부기), 3310~3318행(컷오프 00:00:00,
#   내부 23:59:55 대 외부 00:00:30, 다음 날 PSP 기록에서 찾으면 임시 불일치가 해소), 3402~3412행($10 결제). ORD 번호와 01-01·01-02 날짜, 행 3·4 의 시나리오는 문서용 예시다.
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 88, 열 폭 [120, 216, 216, 216, 152], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "BYTEBYTEGO · 07-02 §3",
      "같은 주문의 세 기록을 맞추면 어긋난 행이 드러난다",
      "주문 번호마다 내부 주문 기록, PSP 정산 파일, 원장의 금액과 시각을 나란히 놓고 판정합니다.",
      "판정은 임시 기간이 지난 뒤의 값이고 금액·날짜는 문서용 예시이며 컷오프는 00:00:00 입니다")

cols = [("주문 번호", 120), ("내부 주문 기록", 216), ("PSP 정산 파일", 216), ("원장", 216), ("판정", 152)]
X0, Y0, HH, RH = 12, 104, 40, 88
x = X0
xs = []
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, KR, "middle", 600)
    x += w

rows = [
    (("ORD-1001", ""), ("200.00 USD", "주문 1건"), ("200.00 USD", "정산 1행"), ("차변 200.00", "대변 200.00"), ("일치", ""), OK),
    (("ORD-1002", ""), ("10.00 USD", "01-01 23:59:55"), ("10.00 USD", "01-02 00:00:30"), ("10.00 USD", "01-01"), ("해소", "다음 파일에서 해소"), OK),
    (("ORD-1003", ""), ("10.00 USD", "주문 1건"), ("10.00 USD × 2", "정산 2행"), ("10.00 USD", "1건"), ("건수 불일치", "PSP 중복 · 조사"), BAD),
    (("ORD-1004", ""), ("10.00 USD", "주문 1건"), ("없음", "정산 0행"), ("10.00 USD", "1건"), ("확정 불일치", "PSP 에 없음 · 조사"), BAD),
]
FOCAL = (2, 2)  # 행 3 의 PSP 열: 같은 주문이 정산 파일에 두 번 있다.
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    c = row[-1]
    for k, cell in enumerate(row[:-1]):
        cx0, w = xs[k]
        last = (k == len(cols) - 1)
        if (r, k) == FOCAL:
            d.tone(cx0, y, w, RH, ACC, 0, "14", 1.4)
        elif last:
            d.tone(cx0, y, w, RH, c, 0, "18", 1.2)
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
        a, b = cell
        col = ACC if (r, k) == FOCAL else (c if last else INK)
        if b:
            d.t(cx0 + w / 2, y + 36, a, 13, col, fam(a), "middle", 600 if (k in (0, 4) or (r, k) == FOCAL) else 400)
            d.t(cx0 + w / 2, y + 60, b, 13, MUTED, fam(b), "middle")
        else:
            d.t(cx0 + w / 2, y + 48, a, 13, col, fam(a), "middle", 600)

d.legend(H - 56, [("일치·해소", OK), ("조사", BAD), ("이 절의 초점", ACC)])
d.save("07-02.reconcile-grid.svg")
