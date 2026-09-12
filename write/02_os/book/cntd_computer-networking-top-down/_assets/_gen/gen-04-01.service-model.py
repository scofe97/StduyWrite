# 04-01 §2 — 원문 4.1.2 의 네트워크 서비스 모델. 줄 수 있었던 서비스 다섯과 인터넷이 실제로 고른 것(최선 노력)을 견준다.
# 인터넷 열은 원문이 "순서도 배달도 지연 상한도 최소 대역폭도 없다"고 적은 그대로다. ATM 열은 원문이 순서·지연 상한·최소 대역폭을
# 보장했다고 적은 세 칸을 채운다. 지연 상한이 있는 보장된 배달은 배달 자체를 품으므로 첫 행도 그 행에 포함으로 적고, 보안은 언급이 없어 비운다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 서비스, 열은 망. 02-01.tcp-udp-services 와 같은 골격이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 532
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §2",
      "줄 수 있었던 것과 고른 것",
      "원문 4.1.2. 네트워크 층이 줄 수 있었던 서비스 다섯과 인터넷이 고른 최선 노력을 견준다. 인터넷 열이 전부 비어 있는 것이 이 절의 요점이다.",
      "가장 적게 약속하는 쪽을 골랐습니다 — ATM 열은 원문이 적은 범위만")

C0, C0W = 24, 300
C1, C1W = 348, 296
C2, C2W = 668, 308
HY, RH, RS = 108, 40, 48
ROWS = [("보장된 배달",           "없음", "보장 — 지연 상한 행에 포함"),
        ("지연 상한이 있는 배달", "없음", "보장"),
        ("순서 보장 배달",        "없음", "보장"),
        ("보장된 최소 대역폭",    "없음", "보장"),
        ("보안",                  "없음", None)]

d.box(C0, HY, C0W, RH, PAPER2, RULE, 0.9)
d.t(C0 + C0W / 2, HY + 26, "줄 수 있었던 서비스", 13, INK, KR, "middle", 600)
d.tone(C1, HY, C1W, RH, ACC, 6, "12", 1.4)
d.t(C1 + C1W / 2, HY + 26, "인터넷 — 최선 노력", 13, ACC, KR, "middle", 600)
d.box(C2, HY, C2W, RH, PAPER2, RULE, 0.9)
d.t(C2 + C2W / 2, HY + 26, "ATM", 13, INK, KR, "middle", 600)

for i, (item, inet, atm) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    d.box(C0, y, C0W, RH, PAPER2, RULE, 0.9)
    d.t(C0 + 16, y + 26, item, 13, INK, KR, "start")
    d.tone(C1, y, C1W, RH, BAD, 6, "14", 1.1)
    d.t(C1 + C1W / 2, y + 26, inet, 13, BAD, KR)
    if atm:
        d.tone(C2, y, C2W, RH, OK, 6, "14", 1.1)
        d.t(C2 + C2W / 2, y + 26, atm, 13, OK, KR)
    else:
        d.box(C2, y, C2W, RH, PAPER2, RULE, 0.9)
        d.t(C2 + C2W / 2, y + 26, "원문 언급 없음", 12, SOFT, KR)

BY = HY + RH + 8 + 5 * RS + 16
d.line(24, BY, 976, BY, RULE, 0.8)
d.t(24, BY + 26, "원문의 말대로 최선 노력은 서비스가 없다는 말의 완곡어법처럼 보입니다. 하나도 배달하지 않는 망도 이 정의를 만족합니다.", 13, MUTED, KR, "start")
d.t(24, BY + 48, "그런데도 넉넉한 대역폭과 대역폭 적응형 애플리케이션(DASH)을 더하니 쓸 만했다는 것이 원문의 결론입니다.", 13, SOFT, KR, "start")

d.legend(H - 44, [("인터넷이 고른 것", ACC), ("약속하지 않음", BAD), ("ATM 이 보장한 것", OK)])
d.save("04-01.service-model.svg")
