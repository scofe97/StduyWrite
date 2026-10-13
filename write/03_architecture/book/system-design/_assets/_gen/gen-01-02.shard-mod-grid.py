# 타입 스펙: type-process — user_id 0~15 가 user_id % 4 로 샤드 0~3 에 갈리고, 샤드를 하나 더해 % 5 로 바꾸면 어느 id 가 제자리에 남고 어느 id 가 옮겨 가는지 같은 열에서 비교한다.
# 사실 출처: 샤드 4개·user_id % 4·샤드 0=0,4,8,12 / 1=1,5,9,13 / 2=2,6,10,14 / 3=3,7,11,15 는 추출본 v2.txt 467~471행과 PDF 29쪽 그림(user_id 0~15).
#   % 5 행과 남음 4·이동 12 는 계산값이다: 0~15 에서 i % 4 == i % 5 인 i 는 0,1,2,3 네 개뿐이다(python3 로 열거 확인).
# Layout conventions: 셀 시작 x=148·폭 44·stride 52(16열), 행 stride 80(y=108·188·268), 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 464
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-02 §6",
      "샤드를 4개에서 5개로 바꾸면 id 16개 중 12개가 옮겨 간다",
      "user_id % 4 는 0~3 번 샤드를 고르고, 같은 id 를 % 5 로 다시 나누면 0~3 만 제자리에 남는다.",
      "위 행이 현재 샤드 번호이고 아래 행이 샤드 하나 추가 뒤의 번호")

X0, CW, STRIDE = 148, 44, 52
ROWS = {"id": 108, "mod4": 188, "mod5": 268}
CH = 44

d.t(16, ROWS["id"] + 28, "user_id", 12, MUTED, MONO, "start", 600)
d.t(16, ROWS["mod4"] + 20, "% 4", 13, INK, MONO, "start", 600)
d.t(16, ROWS["mod4"] + 38, "샤드 4개", 13, MUTED, KR, "start")
d.t(16, ROWS["mod5"] + 20, "% 5", 13, INK, MONO, "start", 600)
d.t(16, ROWS["mod5"] + 38, "샤드 5개", 13, MUTED, KR, "start")

stay = 0
for i in range(16):
    x = X0 + i * STRIDE
    cx = x + CW / 2
    # id 행
    d.box(x, ROWS["id"], CW, CH, PAPER, RULE, 0.7, 4)
    d.t(cx, ROWS["id"] + 28, str(i), 14, INK, MONO, "middle", 600)
    # % 4 행
    d.box(x, ROWS["mod4"], CW, CH, PAPER2, RULE, 0.9, 4)
    d.t(cx, ROWS["mod4"] + 28, str(i % 4), 14, INFO, MONO, "middle", 600)
    # % 5 행 — 같은 번호면 남음, 다르면 이동
    same = (i % 4) == (i % 5)
    stay += same
    d.tone(x, ROWS["mod5"], CW, CH, OK if same else WARN, 4, "14", 1.2)
    d.t(cx, ROWS["mod5"] + 28, str(i % 5), 14, OK if same else WARN, MONO, "middle", 600)
    d.arrow([(cx, ROWS["id"] + CH + 2), (cx, ROWS["mod4"] - 6)], MUTED, "ar", 1.0)
    d.arrow([(cx, ROWS["mod4"] + CH + 2), (cx, ROWS["mod5"] - 6)], MUTED, "ar", 1.0)

assert stay == 4
# 요약 칩 둘: 남음 4 · 이동 12
Y_SUM = ROWS["mod5"] + CH + 36
d.tone(X0, Y_SUM, 208, 40, OK, 6, "12", 1.2)
d.t(X0 + 104, Y_SUM + 26, "제자리 4 (0~3)", 13, OK, KR, "middle", 600)
d.tone(X0 + 224, Y_SUM, 208, 40, ACC, 6, "12", 1.4)
d.t(X0 + 328, Y_SUM + 26, "이동 12 (4~15)", 13, ACC, KR, "middle", 600)

d.legend(H - 44, [("제자리", OK), ("다른 샤드로 이동", WARN), ("현재 샤드 번호", INFO), ("옮겨 간 수", ACC)])
d.save("01-02.shard-mod-grid.svg")
