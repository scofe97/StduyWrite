# 01-03.subnet-compare — 서브넷은 마스크가 자른 앞자리로 정해진다
# 본문 요구(00-03 §6 "마스크는 목록이 아니라 계산입니다"): "판정은 검색이 아니라 한 번의 대조"이고
#           내 주소와 목적지에 각각 마스크를 씌워 앞자리만 남긴 뒤 같은지만 본다. 그래서 위쪽은
#           대조에 쓰이는 값 셋(내 주소·마스크·남은 앞자리)을 점 표기와 이진 표기 두 벌로 나란히
#           놓고, 아래쪽은 그 대조를 실제 목적지 둘에 걸어 결과가 갈리는 것을 보인다.
#           이진 표기가 있어야 "/24 가 앞 24비트"라는 말이 눈으로 확인된다.
# 타입 스펙: type-dp-security-matrix.md — 행은 대조에 쓰이는 값, 열은 그 값을 읽는 두 표기.
#           아래 판정 블록이 격자의 결론 열에 해당한다 — 같은 앞자리면 안, 다르면 밖.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 516
LX, LW = 12, 240                # 행 이름
VX, VW, VC = 268, 220, 378      # 점 표기
BX, BW, BC = 504, 448, 504 + 448 / 2   # 이진 표기
Y0, ROW_H, STRIDE = 132, 58, 66

ROWS = [("내 주소",    "192.168.0.10",  "11000000.10101000.00000000.00001010", INFO),
        ("마스크 /24", "255.255.255.0", "11111111.11111111.11111111.00000000", INFO),
        ("→ 앞 24비트", "192.168.0",    "11000000.10101000.00000000",          OK)]

CASES = [("192.168.0.77", "같은 서브넷 — 안", "그 기계의 MAC 을 직접 묻는다",      OK,  "ok"),
         ("8.8.8.8",      "다른 서브넷 — 밖", "기본 게이트웨이의 MAC 을 적는다", BAD, "bad")]

d = D(W, H, "COMPARISON · 01-03 SUBNET",
      "서브넷은 마스크가 자른 앞자리로 정해진다",
      "서브넷 판단은 뺄셈이나 검색이 아니라 한 번의 대조다. 내 주소와 목적지 주소에 각각 "
      "마스크를 씌워 앞자리만 남기고 그 둘이 같은지만 본다.",
      lead="판단은 뺄셈이 아니라 한 번의 대조입니다.")

for i, (name, dotted, bits, c) in enumerate(ROWS):
    y = Y0 + STRIDE * i
    d.tone(LX, y, LW, ROW_H, c, 6, "10", 1.0)
    d.t(LX + 16, y + 35, name, 12, c, KR, "start", 600)
    d.box(VX, y, VW, ROW_H, PAPER2, RULE, 0.9)
    d.t(VC, y + 35, dotted, 13, INK, MONO)
    d.box(BX, y, BW, ROW_H, PAPER2, RULE, 0.9)
    d.t(BC, y + 35, bits, 11, MUTED, MONO)

d.line(LX, 338, W - 48, 338, RULE, 0.8)

for j, (dst, verdict, note, c, mk) in enumerate(CASES):
    y = 352 + 54 * j
    d.t(20, y + 22, "목적지", 10, SOFT, KR, "start")
    d.box(96, y, 200, 40, PAPER2, RULE, 0.9)
    d.t(196, y + 25, dst, 12, INK, MONO)
    d.path(f"M 310 {y+20} L 360 {y+20}", c, 1.4, m=mk)
    d.tone(372, y, 220, 40, c, 6, "16", 1.3)
    d.t(482, y + 25, verdict, 11, c, KR, "middle", 600)
    d.t(612, y + 25, note, 10, MUTED, KR, "start")

d.legend(472, [("같은 서브넷", OK), ("다른 서브넷", BAD), ("비트 표현", INFO)])
d.save("01-03.subnet-compare.svg")
print("ok subnet-compare")
