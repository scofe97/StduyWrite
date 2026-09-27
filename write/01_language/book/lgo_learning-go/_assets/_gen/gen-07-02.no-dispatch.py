# 07-02.no-dispatch — 임베딩된 필드의 메서드는 바깥 struct 의 같은 이름 메서드를 부르지 않는다
# 본문 요구(07-02 §3 「임베딩은 상속이 아닙니다」): o.Double() 은 승격된 Inner.Double 이고, 그 안의 i.IntPrinter 는
#           Outer 에 IntPrinter 가 있어도 Inner 의 것을 불러 "Inner: 20" 이 찍힌다. 참여자 셋 사이의 시간순 호출이다.
# 타입 스펙: type-sequence — 레인 3개(main · Outer · Inner), 시간은 위→아래, 메시지는 수평 화살표.
#           05-01.named-return 과 같은 방식으로 13px·한글 분기 라벨을 직접 그린다. stride: 메시지 행 간격 64.
#           불리지 않는 Outer.IntPrinter 는 화살표가 아니라 Outer 레인 위 칩으로 둔다(없는 호출을 선으로 그리지 않는다).
#           focal 은 Inner 가 자기 IntPrinter 를 부르는 자기 호출 하나.
# 사실 출처: Learning Go 2판 7장 「Embedding Is Not Inheritance」 예제, go1.25.1 실행(2026-09-27) — Inner: 20.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 520
LANE_W = 232
LX = {"main": 152, "outer": 492, "inner": 832}
Y0, STRIDE = 104, 64


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 07-02 §3",
      "임베딩에는 동적 디스패치가 없다",
      "o.Double() 한 번의 호출을 시간순으로 그린 시퀀스. Double 은 임베딩된 Inner 에서 승격된 메서드라 실제로는 o.Inner.Double() 이 불린다. "
      "Inner.Double 안의 i.IntPrinter 는 Inner 의 메서드이므로, Outer 에 같은 이름의 IntPrinter 가 있어도 불리지 않고 Inner: 20 이 돌아온다.",
      lead="위에서 아래로 시간이 흐릅니다. 원문 밖 비교로, Java 의 오버라이딩이라면 Outer 의 IntPrinter 가 불렸을 자리입니다.")

names = [("main", "호출한 쪽", "o := Outer{...}"), ("outer", "Outer", "IntPrinter 를 가짐"), ("inner", "Inner (임베딩된 필드)", "Double · IntPrinter")]
for key, title, sub in names:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, KR, "middle", 600)
    d.t(x, Y0 + 38, sub, 12, MUTED, kr(sub), "middle")
    d.line(x, Y0 + 56, x, 440, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft", sub=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 13, c if c != MUTED else INK, kr(label), "middle", 600)
    if sub:
        d.t((x1 + x2) / 2, y + 20, sub, 12, MUTED, kr(sub), "middle")


y = Y0 + 96
msg("main", "outer", "o.Double()", y, sub="Outer 에는 Double 이 없음")
y += STRIDE
msg("outer", "inner", "o.Inner.Double()", y, sub="승격된 메서드")
y += STRIDE
x = LX["inner"]
d.path(f"M {x + 10} {y - 12} L {x + 64} {y - 12} L {x + 64} {y + 12} L {x + 14} {y + 12}", ACC, 1.6, m="acc")
d.t(x - 12, y - 18, "i.IntPrinter(20)", 13, ACC, MONO, "end", 600)
d.t(x - 12, y + 2, "Inner 의 것", 12, ACC, KR, "end")
# 불리지 않는 Outer.IntPrinter — 칩
cx = LX["outer"]
d.o.append(f'<rect x="{cx - 104}" y="{y - 14}" width="208" height="28" rx="4" fill="#0D1117"/>')
d.tone(cx - 104, y - 14, 208, 28, BAD, 4, "14", 1.0)
d.t(cx, y + 5, "Outer.IntPrinter · 불리지 않음", 12, BAD, KR, "middle", 600)
y += STRIDE + 16
msg("inner", "main", "\"Inner: 20\"", y, OK, "ok")

d.legend(456, [("Inner 가 자기 메서드를 부름", ACC), ("불리지 않는 메서드", BAD), ("돌아온 값", OK)])
d.save("07-02.no-dispatch.svg")
print("ok 07-02 no-dispatch")
