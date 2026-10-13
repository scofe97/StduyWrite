# 타입 스펙: type-process — 같은 두 서버 줄을 시각 네 칸에 반복해 그리고, 발급된 ID 를 칸마다 옮겨 발급 순서로 읽으면 마지막 칸에서 값이 내려가는 것을 보인다.
# 사실 출처: 추출본 v2.txt 1958~1965행(다음 ID = 이전 ID + k, 서버 1: 1·3·5, 서버 2: 2·4·6 은 PDF 쪽 112 그림), 장면(A 에 몰린 뒤 B 가 처음 받음)은 k = 2 규칙으로 산출한 예시.
# Layout conventions: 행 이름 열 x=24, 시각 칸 폭 148 · stride 180(x=200 부터), 서버 줄 y=116·180 높이 48, 발급 순서 줄 y=300. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, WARN, MUTED, INK, SOFT, PAPER, RULE, KR, MONO

W, H = 960, 472
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §2",
      "서버마다 k 씩 올리면 ID 가 시간순으로 오르지 않는다",
      "k = 2 인 두 서버에서 A 가 1 · 3 · 5 를 내준 뒤 B 가 처음 받으면 나중에 만든 ID 2 가 먼저 만든 5 보다 작다.",
      "서버 A 는 홀수 · 서버 B 는 짝수")

X0, CW, ST = 200, 148, 180
RA, RB, RO = 116, 180, 300
for i in range(4):
    d.t(X0 + ST * i + CW / 2, 104, f"t{i + 1}", 13, SOFT, MONO, "middle", 600)
d.t(24, RA + 30, "서버 A", 14, INK, KR, "start", 600)
d.t(24, RB + 30, "서버 B", 14, INK, KR, "start", 600)
d.t(24, RO + 30, "발급 순서", 14, INK, KR, "start", 600)
d.t(24, RA + 50, "+2", 12, MUTED, MONO, "start")
d.t(24, RB + 50, "+2", 12, MUTED, MONO, "start")

ISSUE = ((0, 1), (0, 3), (0, 5), (1, 2))  # (서버, ID)
for i in range(4):
    x = X0 + ST * i
    for r, y in ((0, RA), (1, RB)):
        d.box(x, y, CW, 48, PAPER, RULE, 0.8, 6)
for i, (srv, v) in enumerate(ISSUE):
    x = X0 + ST * i
    y = RA if srv == 0 else RB
    c = INFO if srv == 0 else WARN
    d.tone(x, y, CW, 48, c, 6, "14", 1.4 if c == ACC else 1.2)
    d.t(x + CW / 2, y + 31, str(v), 16, c, MONO, "middle", 600)

for i, (srv, v) in enumerate(ISSUE):
    x = X0 + ST * i
    c = ACC if i == 3 else (INFO if srv == 0 else WARN)
    d.tone(x + 24, RO, 100, 48, c, 6, "14", 1.4 if c == ACC else 1.2)
    d.t(x + 74, RO + 31, str(v), 16, c, MONO, "middle", 600)
    if i < 3:
        d.arrow([(x + 128, RO + 24), (x + ST + 20, RO + 24)], MUTED, "ar", 1.5)
d.t(X0 + ST * 3 + 74, RO + 80, "5 → 2 내려감", 13, ACC, KR, "middle", 600)

d.legend(H - 56, [("서버 A", INFO), ("서버 B", WARN), ("순서 역전", ACC)])
d.save("07-01.multi-master-k.svg")
