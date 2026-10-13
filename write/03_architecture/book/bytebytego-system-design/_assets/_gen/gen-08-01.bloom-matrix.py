# 타입 스펙: type-dp-security-matrix — 비트 10칸 필터에 URL 두 개를 해시 셋으로 넣은 뒤 같은 URL 은 칸이 모두 1 이라 있을 수 있음, 다른 URL 은 칸 하나가 0 이라 없음이 확정되는 비교 행렬(격자 문법을 비교 행렬로 쓴다). 행은 URL·동작, 열은 칸 번호, 칸 안 글자는 해시 함수.
# 사실 출처: 추출본 v1.txt 1152~1200행, PDF 쪽 45 그림(비트 벡터 1 0 1 0 0 1 1 0 0 1, www.myweb1.com 이 A·B·C 로 0·2·5, www.myweb2.com 이 5·6·9, www.myweb3.com 조회에서 한 칸이 0). 칸 위치는 그림을 읽은 설명용 값이며 실제 해시 출력이 아니다. myweb3 의 B 칸은 7 로 읽었다.
# Layout conventions: 라벨 열 x=12·폭 208, 칸 폭 64·stride 68(x=240+68k), 행 stride 44(y=124 부터). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

M = 10
ADD = {"www.myweb1.com": {"A": 0, "B": 2, "C": 5}, "www.myweb2.com": {"A": 5, "B": 6, "C": 9}}
bits = [0] * M
for pos in ADD.values():
    for p in pos.values():
        bits[p] = 1
assert bits == [1, 0, 1, 0, 0, 1, 1, 0, 0, 1], bits
Q = {"www.myweb1.com": {"A": 0, "B": 2, "C": 5}, "www.myweb3.com": {"A": 6, "B": 7, "C": 9}}
assert all(bits[p] for p in Q["www.myweb1.com"].values())
assert not all(bits[p] for p in Q["www.myweb3.com"].values()) and bits[7] == 0

W, H = 960, 484
d = D(W, H, "BYTEBYTEGO · 08-01 §4",
      "칸 하나가 0 이면 그 URL 은 없다",
      "두 URL 이 5 번 칸을 함께 켜서 있다는 답은 틀릴 수 있고, 없다는 답은 틀리지 않습니다",
      "비트 10칸 · 해시 A B C · 칸 위치는 설명용 값")

X0, CW, CS = 240, 64, 68
HY = 100
d.t(12, HY + 20, "칸 번호", 12, SOFT, KR, "start")
for i in range(M):
    d.t(X0 + i * CS + CW / 2, HY + 20, str(i), 12, MUTED, MONO)
hcol = {"A": INFO, "B": OK, "C": WARN}


def row(y, label, pos, kind):
    d.t(12, y + 25, label, 12, INK, MONO if label[0] in "wA" else KR, "start", 600)
    for i in range(M):
        d.box(X0 + i * CS, y, CW, 36, PAPER2, RULE, 0.8, 4)
    for h, p in pos.items():
        x = X0 + p * CS
        d.tone(x, y, CW, 36, hcol[h], 4, "22", 1.1)
        d.t(x + CW / 2, y + 24, h, 13, hcol[h], MONO, "middle", 600)


y = 124
for url, pos in ADD.items():
    row(y, "추가 " + url, pos, "add")
    y += 44
by = y + 4
d.t(12, by + 25, "켜진 비트", 12, ACC, KR, "start", 600)
for i in range(M):
    x = X0 + i * CS
    if bits[i]:
        d.tone(x, by, CW, 36, ACC, 4, "14", 1.4)
        d.t(x + CW / 2, by + 24, "1", 14, ACC, MONO, "middle", 600)
    else:
        d.box(x, by, CW, 36, PAPER2, RULE, 0.8, 4)
        d.t(x + CW / 2, by + 24, "0", 14, MUTED, MONO)
y = by + 60
for url, pos in Q.items():
    row(y, "조회 " + url, pos, "query")
    ok = all(bits[p] for p in pos.values())
    zero = [p for p in pos.values() if not bits[p]]
    if ok:
        d.t(X0, y + 58, "세 칸이 모두 1 → 있을 수 있음", 13, WARN, KR, "start", 600)
    else:
        d.t(X0, y + 58, f"{zero[0]} 번 칸이 0 → 없음 확정", 13, BAD, KR, "start", 600)
    y += 80

d.legend(H - 44, [("해시 A", INFO), ("해시 B", OK), ("해시 C · 있을 수 있음", WARN), ("켜진 비트", ACC), ("없음 확정", BAD)])
d.save("08-01.bloom-matrix.svg")
