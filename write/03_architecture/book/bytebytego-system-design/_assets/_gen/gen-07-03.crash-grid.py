# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 서버가 멈춘 지점이고 열은 PSP·지갑·원장에 남은 값이며 마지막 열이 그 어긋남을 찾는 방법이다.
# 사실 출처: 추출본 v1.txt 3790~3830행(PSP 성공 뒤 지갑, 지갑 성공 뒤 원장 순서). 멈춘 지점별 값은 그 순서에서 도출한 값이고 금액 20.00 USD 는 §1 예시와 같다.
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 88, 열 폭 [200, 140, 140, 140, 292], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 596
d = D(W, H, "BYTEBYTEGO · 07-03 §2",
      "멈춘 지점마다 PSP·지갑·원장의 값이 어긋나는 모양이 다르다",
      "주문 PO-A 20.00 USD 를 처리하다 서버가 멈췄을 때 세 곳에 남는 값과 그 어긋남을 찾는 방법입니다.",
      "금액은 문서용 예시이고 멈춘 지점은 저장 순서에서 도출했습니다")

cols = [("멈춘 지점", 200), ("PSP", 140), ("지갑", 140), ("원장", 140), ("남은 일", 292)]
X0, Y0, HH, RH = 12, 104, 40, 88
x = X0
xs = []
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, KR, "middle", 600)
    x += w

rows = [
    (("PSP 호출 중", "응답을 못 받음"), ("결과 모름", ""), ("0", ""), ("없음", ""), ("같은 키로 다시 호출", "멱등 키"), WARN),
    (("PSP 성공 뒤", "지갑 갱신 전"), ("20.00 청구", ""), ("0", ""), ("없음", ""), ("PSP 결과 확인 뒤", "지갑 갱신 재시도"), BAD),
    (("지갑 갱신 뒤", "원장 추가 전"), ("20.00 청구", ""), ("+20.00", ""), ("없음", ""), ("잔액 ≠ 원장", "대사로 발견"), BAD),
    (("원장 추가 뒤", ""), ("20.00 청구", ""), ("+20.00", ""), ("20.00", ""), ("세 곳 일치", ""), OK),
]
FOCAL = (2, 3)  # 지갑은 올랐는데 원장이 비어 있는 칸.
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
            d.t(cx0 + w / 2, y + 36, a, 13, col, fam(a), "middle", 600 if k in (0, 4) else 400)
            d.t(cx0 + w / 2, y + 60, b, 13, MUTED, fam(b), "middle")
        else:
            d.t(cx0 + w / 2, y + 48, a, 13, col, fam(a), "middle", 600 if (k == 4 or (r, k) == FOCAL) else 400)

d.legend(H - 56, [("재시도", WARN), ("어긋남", BAD), ("일치", OK), ("이 절의 초점", ACC)])
d.save("07-03.crash-grid.svg")
