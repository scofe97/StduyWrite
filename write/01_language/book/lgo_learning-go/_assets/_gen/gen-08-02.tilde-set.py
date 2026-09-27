# 08-02.tilde-set — 타입 항 int 는 int 하나만, ~int 는 바탕 타입이 int 인 모든 타입을 받는다
# 본문 요구(08-02 §1 「타입 항은 정확히 맞아야 하고 ~ 가 바탕 타입까지 넓힙니다」): MyInt 는 int 항을 만족하지 못해
#           "possibly missing ~ for int" 오류가 나고, ~int 로 바꾸면 만족한다. 두 타입 집합의 포함 관계가 논지다.
# 타입 스펙: type-nested — 바깥 상자 = ~int 가 받는 타입 집합, 안쪽 상자 = int 가 받는 집합. 바깥 밖에 받지 않는 타입을 둔다.
#           stride: 바깥 상자 여백 32, 칩 높이 36·간격 16. focal 은 ~int 에만 드는 MyInt 칩 하나. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 8장 「Use Type Terms to Specify Operators」, go1.25.1 빌드(2026-09-27) —
#           MyInt does not satisfy Integer (possibly missing ~ for int in Integer), ~ 판에서 0 10 <nil>.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 440
OX, OY, OW, OH = 36, 132, 616, 240
IX, IY, IW, IH = 68, 196, 232, 144


def chip(x, y, w, txt, c, sub=None, focal=False):
    d.tone(x, y, w, 40, c, 6, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x + w // 2, y + 25, txt, 14, c, MONO, "middle", 600)
    if sub:
        d.t(x + w // 2, y + 58, sub, 11, MUTED, KR, "middle")


d = D(W, H, "NESTED · 08-02 §1",
      "타입 항 int 와 ~int 가 받는 타입",
      "타입 항 int 가 받는 집합은 int 하나뿐이다. ~int 는 바탕 타입이 int 인 모든 타입을 받으므로 int 와 함께 type MyInt int 같은 사용자 정의 타입이 들어간다. "
      "그래서 MyInt 는 int 항의 제약을 만족하지 못하고 ~int 항의 제약은 만족한다. 바탕 타입이 다른 int64 나 string 은 어느 쪽에도 들지 않는다.",
      lead="바깥 상자가 ~int, 안쪽 상자가 int 의 타입 집합입니다. Age 는 노트가 더한 예입니다.")

d.tone(OX, OY, OW, OH, INFO, 10, "0A", 1.2)
d.t(OX + 20, OY + 28, "~int · 바탕 타입이 int 인 모든 타입", 13, INFO, KR, "start", 600)
d.tone(IX, IY, IW, IH, OK, 8, "0A", 1.2)
d.t(IX + 20, IY + 28, "int · 정확히 int 만", 13, OK, KR, "start", 600)
chip(IX + 40, IY + 56, 152, "int", OK)
chip(348, IY + 16, 136, "MyInt", ACC, "type MyInt int", focal=True)
chip(500, IY + 16, 136, "Age", INFO, "type Age int")
d.t(IX + IW // 2, IY + IH - 16, "~ 없는 제약도 만족", 11, MUTED, KR, "middle")
d.t(492, OY + OH - 20, "~ 가 없으면 MyInt 는 탈락", 12, ACC, KR, "middle", 600)

# 바깥 — 받지 않는 타입
d.t(816, OY + 28, "어느 쪽에도 들지 않음", 13, MUTED, KR, "middle", 600)
chip(748, OY + 56, 136, "int64", BAD)
chip(748, OY + 124, 136, "string", BAD)
d.t(816, OY + 196, "바탕 타입이 다름", 11, MUTED, KR, "middle")

d.legend(392, [("int 항", OK), ("~int 항", INFO), ("~ 로만 들어오는 타입", ACC), ("제외", BAD)])
d.save("08-02.tilde-set.svg")
print("ok 08-02 tilde-set")
