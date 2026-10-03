# 05-01 §5 — 등록 가중치가 SRV 응답 가중치로 바뀌는 계산을 경우 셋으로 따라간다.
# 소스 근거: plugin/backend_lookup.go 의 SRV 함수 — w1 := 100.0 / float64(w[serv.Priority]); w1 *= float64(serv.Weight);
#            weight := uint16(math.Floor(w1)). 97 의 결과는 python 으로 100.0/97*97 = 99.99999999999999 를 확인했다(2026-10-03).
# 타입 스펙: type-process — 등록값 → 합 → 백분율 → 버림의 단계가 열로 진행하고, 경우 셋이 같은 단계를 지난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 476
d = D(W, H, "LEARNING COREDNS · 05-01 §5",
      "백분율로 바꾼 뒤 소수점 아래를 버린다",
      "etcd 플러그인은 같은 우선순위 대상들의 가중치 합에 대한 백분율을 구하고 소수점 아래를 버린다. "
      "그래서 둘 이상이면 합이 100 에 못 미칠 수 있고, 하나여도 부동소수 오차로 99 가 나올 수 있다.",
      "주황 열이 실제 SRV 응답에 실리는 값입니다")

COLS = [(20, 170, "경우"), (200, 130, "등록 가중치"), (340, 110, "같은 우선순위 합"),
        (460, 210, "100 ÷ 합 × 값"), (680, 180, "버림 · 응답 가중치")]
rows = [
    (("대상 하나", "가중치 20"), ("20", ""), ("20", ""), ("100.0", ""), ("100", "")),
    (("대상 둘", "200 · 100"), ("200 / 100", ""), ("300", ""), ("66.67 / 33.33", ""), ("66 / 33", "합 99")),
    (("대상 하나", "가중치 97"), ("97", ""), ("97", ""), ("99.99999999999999", "부동소수 오차"), ("99", "100 이 아님")),
]
Y0, PITCH, RH = 132, 84, 74

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, ACC if k == 4 else SOFT, KR, "start", 600)

d.tone(676, Y0 - 4, 188, PITCH * 2 + RH + 8, ACC, 8, "12", 1.4)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    for k, (x, w, _) in enumerate(COLS):
        main, sub = cells[k]
        if k != 4:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        fam = KR if any("가" <= ch <= "힣" for ch in main) else MONO
        size = 13 if len(main) > 12 else 15
        col = ACC if k == 4 else INK
        if sub:
            d.t(x + 12, y + 30, main, size, col, fam, "start", 600)
            d.t(x + 12, y + 54, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 42, main, size, col, fam, "start", 600)
        if k < 4:
            nx = COLS[k + 1][0]
            end = nx - 8 if k == 3 else nx - 3   # 마지막 화살촉이 주황 테두리(676)에 묻히지 않게
            d.path(f"M {x + w + 2} {y + RH / 2} L {end} {y + RH / 2}", SOFT, 1.1, m="soft")

d.t(20, 414, "적용 관점 실습의 66 · 33 이 둘째 줄 · 비율은 거의 그대로라 대상 선택 영향은 작다", 13, MUTED, KR, "start")

d.legend(428, [("응답에 실리는 값", ACC)])
d.save("05-01.weight-recalc.svg")
