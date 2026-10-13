# 타입 스펙: type-process — 키 8개의 해시 값이 % 4 로 서버 s0~s3 에 가고, s1 이 빠져 % 3 으로 바뀐 뒤 어느 서버로 가는지 열마다 위에서 아래로 따라간다.
# 사실 출처: 키 8개와 해시 값은 추출본 v2.txt 1333~1334행·PDF 72쪽 표(해시 18358617 · 26143584 · 18131146 · 35863496 · 34085809 · 27581703 · 38164978 · 22530351),
#   % 4 결과는 PDF 73쪽 그림(s0=key1·key3, s1=key0·key4, s2=key2·key6, s3=key5·key7)과 일치, % 3 번호는 PDF 73쪽 표와 일치.
#   번호 → 서버 대응(0→s0·1→s2·2→s3)과 이동 5 · 제자리 3 은 계산값이다(python3 로 열거 확인).
# Layout conventions: 셀 시작 x=148·폭 88·stride 100(8열), 행 stride 72(y=160·232·304·376), 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

HASH = [18358617, 26143584, 18131146, 35863496, 34085809, 27581703, 38164978, 22530351]
M4 = [h % 4 for h in HASH]
M3 = [h % 3 for h in HASH]
# s1 이 빠지면 남은 서버 s0·s2·s3 가 번호 0·1·2 를 차례로 받는다.
PHYS = {0: 0, 1: 2, 2: 3}
AFTER = [PHYS[n] for n in M3]
assert M4 == [1, 0, 2, 0, 1, 3, 2, 3]
assert M3 == [0, 0, 1, 2, 1, 0, 1, 0]
MOVED = [i for i in range(8) if AFTER[i] != M4[i]]
NEEDED = [i for i in range(8) if M4[i] == 1]
assert MOVED == [0, 3, 4, 5, 7] and NEEDED == [0, 4]

W, H = 1000, 568
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01 §1",
      "서버 s1 이 빠지면 키 8개 중 5개가 옮겨 간다",
      "hash % 4 의 번호가 hash % 3 의 번호로 바뀌면 s1 에 없던 키 셋도 다른 서버로 간다.",
      "열마다 같은 키가 해시 값에서 나머지 연산을 거쳐 서버로 가는 길")

X0, CW, STRIDE, CH = 148, 88, 100, 44
ROWS = {"key": 104, "hash": 160, "m4": 232, "m3": 304, "sv": 376}

d.t(16, ROWS["hash"] + 28, "hash", 13, MUTED, MONO, "start", 600)
d.t(16, ROWS["m4"] + 20, "% 4", 13, INK, MONO, "start", 600)
d.t(16, ROWS["m4"] + 38, "서버 번호", 13, MUTED, KR, "start")
d.t(16, ROWS["m3"] + 20, "% 3", 13, INK, MONO, "start", 600)
d.t(16, ROWS["m3"] + 38, "s1 제거 뒤", 13, MUTED, KR, "start")
d.t(16, ROWS["sv"] + 20, "서버", 13, INK, KR, "start", 600)
d.t(16, ROWS["sv"] + 38, "번호 0·1·2 →", 13, MUTED, KR, "start")

for i in range(8):
    x = X0 + i * STRIDE
    cx = x + CW / 2
    d.t(cx, ROWS["key"] + 24, f"key{i}", 14, INK, MONO, "middle", 600)
    d.box(x, ROWS["hash"], CW, CH, PAPER, RULE, 0.7, 4)
    d.t(cx, ROWS["hash"] + 28, str(HASH[i]), 13, MUTED, MONO, "middle")
    d.box(x, ROWS["m4"], CW, CH, PAPER2, RULE, 0.9, 4)
    d.t(cx, ROWS["m4"] + 28, f"s{M4[i]}", 14, INFO, MONO, "middle", 600)
    d.box(x, ROWS["m3"], CW, CH, PAPER2, RULE, 0.9, 4)
    d.t(cx, ROWS["m3"] + 28, str(M3[i]), 14, MUTED, MONO, "middle", 600)
    if i in NEEDED:
        c = WARN
    elif i in MOVED:
        c = ACC
    else:
        c = OK
    d.tone(x, ROWS["sv"], CW, CH, c, 4, "14", 1.4 if c == ACC else 1.0)
    d.t(cx, ROWS["sv"] + 28, f"s{AFTER[i]}", 14, c, MONO, "middle", 600)
    d.arrow([(cx, ROWS["hash"] + CH + 2), (cx, ROWS["m4"] - 6)], MUTED, "ar", 1.0)
    d.arrow([(cx, ROWS["m4"] + CH + 2), (cx, ROWS["m3"] - 6)], MUTED, "ar", 1.0)
    d.arrow([(cx, ROWS["m3"] + CH + 2), (cx, ROWS["sv"] - 6)], MUTED, "ar", 1.0)

Y_SUM = ROWS["sv"] + CH + 24
SUMS = (
    (OK, "제자리 3", "key1 · key2 · key6"),
    (WARN, "꼭 옮길 키 2", "key0 · key4"),
    (ACC, "불필요한 이동 3", "key3 · key5 · key7"),
)
for j, (c, a, b) in enumerate(SUMS):
    x = X0 + j * 260
    d.tone(x, Y_SUM, 240, 56, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, Y_SUM + 24, a, 13, c, KR, "start", 600)
    d.t(x + 14, Y_SUM + 44, b, 12, MUTED, MONO, "start")

d.legend(H - 44, [("제자리", OK), ("s1 에 있던 키", WARN), ("불필요한 이동", ACC), ("서버 번호", INFO)])
d.save("05-01.mod-n-remap-grid.svg")
