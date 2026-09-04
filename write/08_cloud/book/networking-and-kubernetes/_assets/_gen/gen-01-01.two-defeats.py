# 01-01.two-defeats — NCP 의 몰락과 OSI 의 패배는 다른 사건이다
# 본문 요구: "§1 의 NCP 가 무너진 것과 OSI 가 진 것은 다른 사건입니다" + "쪼갰느냐가 아니라
#           몇 조각으로 어떻게 쪼갰느냐, 누가 먼저 돌아가게 만들었느냐" — 두 사건을 축으로 가른다.
# 타입 스펙: type-dp-security-matrix.md — 행은 두 사건(NCP·OSI), 열은 설계·진 이유·지금 남은 것.
#           같은 열에서 두 행이 갈리는 자리가 판정이다. NCP 는 "남은 것" 칸이 비어 흐리고(사라짐)
#           OSI 는 그 칸만 살아 focal 이다 — 본문의 "사라진 것은 계층 분리라는 발상이 아니라
#           그 발상을 구현한 프로토콜들"이 그 한 칸에 걸린다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 504
d = D(W, H, "NCP vs OSI · TWO DIFFERENT DEFEATS",
      "무너진 이유가 서로 다른 두 사건",
      "NCP 는 쪼개지 않아서 무너졌고, OSI 는 쪼갠 방식과 구현 속도에서 밀렸다. 남은 것도 다르다.",
      lead="둘 다 졌지만 진 이유가 다르다 — 하나는 설계가, 하나는 구현이 문제였다")

LX, LW, CX, CW = 32, 176, [224, 480, 736], 240
HEAD = ["설계", "진 이유", "지금 남은 것"]
ROWS = [
    (172, "NCP", "1970 · ARPANET", WARN,
     [(["하나가 전부 떠맡음"], INFO),
      (["네트워크 종류가", "다양해지자 못 버팀"], INFO),
      (["없다 — TCP/IP 로 대체"], SOFT)]),
    (292, "OSI", "1984 · ISO 7498", INFO,
     [(["일곱 계층으로 쪼갬"], INFO),
      (["구현이 복잡하고 비효율적", "먼저 돌아간 쪽에 밀림"], INFO),
      (["계층 용어 L3 · L7"], ACC)]),
]
RH = 104

for cx, h in zip(CX, HEAD):
    d.t(cx + CW // 2, 148, h, 12, SOFT, KR, "middle", 600)

for y, name, sub, nc, cells in ROWS:
    d.box(LX, y, LW, RH, PAPER2, nc, 1.1, 6)
    d.t(LX + LW // 2, y + 44, name, 16, nc, KR, "middle", 600)
    d.t(LX + LW // 2, y + 70, sub, 11, MUTED, MONO)
    for cx, (lines, c) in zip(CX, cells):
        if c is ACC:
            d.tone(cx, y, CW, RH, ACC, 6, "12", 1.4)
        else:
            d.box(cx, y, CW, RH, PAPER2, RULE, 0.9, 6)
        base = y + 52 if len(lines) == 1 else y + 44
        for i, ln in enumerate(lines):
            d.t(cx + CW // 2, base + i * 24, ddx.fit(ln, 12, CW - 24, ln), 12, c, KR)

d.t(LX + 4, 436, "쪼갰느냐가 아니라 몇 조각으로 어떻게 쪼갰느냐, 그리고 그 조각을 누가 먼저 돌아가게 만들었느냐가 갈랐다",
    12, MUTED, KR, "start")
d.legend(448, [("사실", INFO), ("사라진 것", SOFT), ("살아남은 것", ACC)])
d.save("01-01.two-defeats.svg")
print("ok two-defeats")
