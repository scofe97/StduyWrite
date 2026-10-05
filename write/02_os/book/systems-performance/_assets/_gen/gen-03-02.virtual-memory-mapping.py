# 03-02 §1 — 두 프로세스의 가상 주소 공간이 RAM 프레임과 스왑으로 매핑되는 모습(원서 그림 3.11 재구성).
# 타입 스펙: type-architecture — 프로세스 A · RAM · 프로세스 B · 스왑 장치 네 구성요소와 매핑 연결이다.
#           축약: 스왑 화살표는 다른 매핑과 겹치지 않게 B 열 오른쪽으로 돌린다. 페이지 하나를 행 하나로 두고 A 는 RAM 왼쪽 칸, B 는 오른쪽 칸으로 수평 매핑한다(대각선 금지).
#           "0 근처 무효"는 원서 각주 13(0x10000 같은 오프셋에서 시작) 근거. focal 은 아직 안 쓴 페이지(매핑 없음).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 620
AX, BXX, RX, CW = 64, 728, 400, 168      # A 열 · B 열 · RAM 열 x, 열 폭
RW = 160                                  # RAM 폭
Y0, RH, ST = 160, 40, 52

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02 §1",
       "가상 주소 공간이 RAM 과 스왑으로 매핑된다",
       "두 프로세스의 같은 가상 주소는 서로 다른 RAM 프레임으로 매핑된다. 아직 쓰지 않은 페이지는 매핑이 없고, 오래 쓰지 않은 페이지는 스왑으로 밀려나며, 0 근처는 일부러 비워 둔 무효 영역이다.",
       "실제 메모리는 처음 쓸 때 매핑됩니다")

d.t(AX + CW / 2, Y0 - 20, "프로세스 A · 가상 주소", 13, INK, KR, "middle", 600)
d.t(BXX + CW / 2, Y0 - 20, "프로세스 B · 가상 주소", 13, INK, KR, "middle", 600)
d.t(RX + RW / 2, Y0 - 20, "RAM · primary", 13, INFO, KR, "middle", 600)
d.box(RX - 8, Y0 - 8, RW + 16, 5 * ST - 12 + 16, PAPER, INFO, 1.0, 8)

# (A 페이지, A 상태, B 페이지, B 상태) — 상태: map / none / swap / bad
ROWS = [("스택", "map", "스택", "map"),
        ("힙 · 쓴 페이지", "map", "힙 · 오래 안 씀", "swap"),
        ("힙 · 아직 안 씀", "none", "코드", "map"),
        ("코드", "map", "힙 · 아직 안 씀", "none"),
        ("0 근처 · 무효", "bad", "0 근처 · 무효", "bad")]
HW = RW / 2 - 4
for i, (an, ast, bn, bst) in enumerate(ROWS):
    y = Y0 + i * ST
    for x, name, stt, side in ((AX, an, ast, "A"), (BXX, bn, bst, "B")):
        c = {"map": None, "none": ACC, "swap": WARN, "bad": BAD}[stt]
        if c: d.tone(x, y, CW, RH, c, 6)
        else: d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + CW / 2, y + 25, name, 13, c if c else INK, KR, "middle", 600 if c else 400)
    # RAM 칸 — A 는 왼쪽, B 는 오른쪽
    for stt, fx, who in ((ast, RX, "A"), (bst, RX + RW / 2 + 4, "B")):
        if stt == "map":
            d.box(fx, y, HW, RH, PAPER2, INFO, 1.0, 4)
            d.t(fx + HW / 2, y + 25, f"{who} 프레임", 12, INFO, KR)
    cy = y + RH / 2
    if ast == "map": d.arrow([(AX + CW + 4, cy), (RX - 6, cy)], MUTED, "ar", 1.4)
    if ast == "none": d.t((AX + CW + RX) / 2, cy + 5, "매핑 없음", 12, ACC, KR, "middle", 600)
    if bst == "map": d.arrow([(BXX - 4, cy), (RX + RW + 6, cy)], MUTED, "ar", 1.4)
    if bst == "none": d.t((RX + RW + BXX) / 2, cy + 5, "매핑 없음", 12, ACC, KR, "middle", 600)
    if bst == "swap":
        gx = BXX + CW + 32
        SY = Y0 + 5 * ST + 36
        d.arrow([(BXX + CW + 4, cy), (gx, cy), (gx, SY + 24), (RX + RW + 4, SY + 24)], WARN, "warn", 1.4)
        d.t((RX + RW + gx) / 2, SY + 16, "밀려남", 12, WARN, KR, "middle", 600)

SY = Y0 + 5 * ST + 36
d.tone(RX, SY, RW, 48, WARN, 6)
d.t(RX + RW / 2, SY + 21, "스왑 장치", 13, WARN, KR, "middle", 600)
d.t(RX + RW / 2, SY + 39, "secondary · 디스크", 12, MUTED, KR)

d.legend(SY + 76, [("아직 안 써서 매핑 없음", ACC), ("스왑으로 밀려남", WARN), ("무효 영역", BAD), ("RAM 프레임", INFO)])
d.save("03-02.virtual-memory-mapping.svg")
