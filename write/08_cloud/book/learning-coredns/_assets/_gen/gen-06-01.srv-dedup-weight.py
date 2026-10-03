# 06-01 §6 — 가중치는 중복 제거 전에 엔드포인트 수로 나누므로, 대상 이름이 겹치면 응답의 합이 100 에 못 미친다.
# 소스 근거: plugin/backend_lookup.go 의 SRV 함수 — 첫 루프에서 우선순위별 가중치 합을 내고(주석 "we may drop duplicate
#            SRV records latter on"), 둘째 루프에서 isDuplicate(dup, srv.Target, "", srv.Port) 로 같은 대상·포트를 거른다.
# 값 근거: 원서 Example 6-5(엔드포인트 넷 · SRV 넷 · 각 25)와 Example 6-7(hostname: myhost · SRV 한 줄 · 25).
# 타입 스펙: type-process — 엔드포인트 → 대상 이름 → 가중치 계산 → 중복 제거가 열로 진행하고 경우 둘이 같은 단계를 지난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 400
d = D(W, H, "LEARNING COREDNS · 06-01 §6",
      "가중치를 나눈 뒤에 중복을 거른다",
      "CoreDNS 는 같은 우선순위 엔드포인트 수로 100 을 먼저 나누고, 그다음 대상 이름과 포트가 같은 SRV 를 거른다. "
      "그래서 넷이 같은 이름 myhost 를 가진 Example 6-7 은 한 줄만 남고 그 가중치는 25 다.",
      "주황 칸이 합이 100 이 아닌 응답입니다")

COLS = [(20, 170, "원서 예"), (200, 100, "엔드포인트"), (310, 200, "대상 이름"),
        (520, 150, "가중치 계산"), (680, 180, "중복 제거 · 응답")]
rows = [
    (("Example 6-5", "대상이 서로 다름"), ("넷", ""), ("10-5-104-3 외 셋", "서로 다른 이름"),
     ("100 ÷ 4 = 25", "넷 모두"), ("SRV 넷 · 각 25", "합 100")),
    (("Example 6-7", "hostname: myhost"), ("넷", ""), ("myhost", "넷이 같은 이름"),
     ("100 ÷ 4 = 25", "넷 모두"), ("SRV 한 줄 · 25", "합 25")),
]

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = 132 + i * 92
    for k, (x, w, _) in enumerate(COLS):
        main, sub = cells[k]
        focal = (i == 1 and k == 4)
        if focal:
            d.tone(x, y, w, 80, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 80, PAPER2, RULE, 1.0, 6)
        ascii_main = not any("가" <= ch <= "힣" for ch in main)
        d.t(x + 12, y + 34, main, 14 if not ascii_main else 13, ACC if focal else INK,
            MONO if ascii_main else KR, "start", 600)
        if sub:
            d.t(x + 12, y + 58, sub, 12, MUTED, KR, "start")
        if k < 4:
            nx = COLS[k + 1][0]
            d.path(f"M {x + w + 1} {y + 40} L {nx - 2} {y + 40}", SOFT, 1.1, m="soft")

d.t(20, 336, "소스 주석 · 중복 SRV 를 나중에 버리면 가중치가 어긋날 수 있다", 13, MUTED, KR, "start")
d.legend(352, [("합이 100 이 아닌 응답", ACC)])
d.save("06-01.srv-dedup-weight.svg")
