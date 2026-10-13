# 타입 스펙: type-gantt — 알파벳 a~z 를 가로 축으로 펴고 샤드가 맡는 구간을 막대로, 막대 길이가 곧 맡는 글자 수다. focal 은 질의 수에 맞춘 배분 지도 행.
# 사실 출처: 추출본 v2.txt 3817~3836행(첫 글자 샤딩: 2 대 a~m · n~z, 3 대 a~i · j~r · s~z, 2 글자 단계에서 a 가 aa-ag · ah-an · ao-au · av-az 로 넷, 질의 수 분포에 맞춘 샤드 지도 예시 s 한 칸과 u~z 한 칸) · PDF 216~217쪽.
#   막대 길이는 글자 수다: a~m 13 · n~z 13 · a~i 9 · j~r 9 · s~z 8 · aa~ag 7 · ah~an 7 · ao~au 7 · av~az 5. 마지막 행의 s 와 u~z 는 책의 예시 한 쌍이고 t 의 배정은 예시가 정하지 않는다.
# Layout conventions: 축 x(i) = 184 + 30i (i=0~25), 행 stride 64(y=148·212·276·340), 막대 높이 32. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, WARN, MUTED, INK, RULE, KR, MONO

X0, U = 184, 30
W, H = 1000, 504
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §8",
      "첫 글자로 나누면 서버 26 대까지 가고 쏠리면 지도로 다시 나눈다",
      "알파벳 26 글자를 구간으로 묶어 샤드에 배정하고, 질의 수가 쏠린 글자는 샤드 하나를 따로 둔다.",
      "막대 길이 = 한 샤드가 맡는 글자 수")

LET = "abcdefghijklmnopqrstuvwxyz"


def x(i):
    return X0 + i * U


for i, ch in enumerate(LET):
    d.t(x(i) + U / 2, 108, ch, 12, MUTED, MONO)
d.line(X0, 120, x(26), 120, RULE, 1.0)

ROWS = (
    ("서버 2 대", INFO, (("a–m", 0, 13), ("n–z", 13, 26))),
    ("서버 3 대", INFO, (("a–i", 0, 9), ("j–r", 9, 18), ("s–z", 18, 26))),
    ("a 로 시작 · 둘째 글자", WARN, (("aa–ag", 0, 7), ("ah–an", 7, 14), ("ao–au", 14, 21), ("av–az", 21, 26))),
    ("샤드 지도 예", ACC, (("s", 18, 19), ("u–z", 20, 26))),
)
for r, (lab, c, bars) in enumerate(ROWS):
    y = 148 + r * 64
    d.t(24, y + 21, lab, 13, INK, KR, "start", 600)
    for name, a, b in bars:
        d.tone(x(a), y, (b - a) * U, 32, c, 4, "14", 1.4 if c == ACC else 1.0)
        d.t(x(a) + (b - a) * U / 2, y + 21, name, 12, INK, MONO, "middle", 600)

d.legend(H - 56, [("첫 글자 단계", INFO), ("둘째 글자 단계", WARN), ("질의 수에 맞춘 배분", ACC)])
d.save("13-01.shard-ranges.svg")
