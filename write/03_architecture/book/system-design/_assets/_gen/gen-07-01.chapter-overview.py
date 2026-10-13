# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §5.
# 사실 출처: 추출본 v2.txt 1914~2075행(요구사항 1922~1943 · 다중 마스터 1952~1965 · UUID 1966~1984 · 티켓 서버 1985~2002 · 스노플레이크 2003~2022 · 시계 2057~2062),
#   twitter-archive/snowflake 태그 snowflake-2010 IdWorker.scala L25~L36·L74~L79, RFC 9562 §5.7, RFC 5905 STEPT 125 ms.
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, MONO, KR

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01",
      "분산 유일 ID 를 일곱 절로 읽는다",
      "요구사항에서 출발해 네 가지 방식을 견주고 스노플레이크의 비트 배치와 시계 문제로 닫는다.",
      "64비트 숫자 · 시간순 · 초당 10,000개를 채우는 방식을 찾는 과정")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "요구사항", "64비트 · 10,000/초", INFO),
    ("§2", "다중 마스터", "+k · 순서 역전", INFO),
    ("§3", "UUID", "128비트 · v7", INFO),
    ("§4", "티켓 서버", "한 대 · 홀짝 두 대", INFO),
    ("§5", "스노플레이크", "1 · 41 · 5 · 5 · 12", ACC),
    ("§6", "ID 에서 시각", "297616116568", INFO),
    ("§7", "시계 어긋남", "125 ms · 후퇴 거절", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 4 else (1, i - 4)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 12, MUTED, fam(val), "start")

for i in range(6):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("07-01.chapter-overview.svg")
