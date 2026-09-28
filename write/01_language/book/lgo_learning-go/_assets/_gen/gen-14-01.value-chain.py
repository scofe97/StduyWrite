# 14-01.value-chain — WithValue 는 부모를 감싼 자식을 만들고, Value 는 자식에서 부모 쪽으로 거슬러 찾는다
# 본문 요구(14-01 §2 「WithValue 는 부모를 감싼 자식을 만들고 Value 는 거슬러 찾습니다」): WithValue 가 돌려주는 context 는
#           키·값 쌍을 담고 부모를 감싼 자식이다. Value 는 그 context 와 부모들에서 키를 찾고 없으면 nil 이다. 원문은 이 탐색이 선형이라고 짚는다.
#           context 는 정보를 아래 계층으로만 넘기고 위로 꺼내 올리지 않는다.
# 타입 스펙: type-nested — 바깥에서 안쪽으로 guid 자식 ⊃ user 자식 ⊃ Background. 한 겹당 안쪽 여백 28. 오른쪽 열에 Value 조회 두 줄을
#           겹 순서대로 칩으로 적는다. focal 은 user 겹에서 찾아내는 칩 하나. 키 이름 guidKey·userKey 와 값은 설명을 위한 예다.
# 사실 출처: Learning Go 2판 14장 「Values」, go doc context.WithValue.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 480
X0, Y0, BW, BH, PAD = 36, 132, 520, 280, 28


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NESTED · 14-01 §2",
      "WithValue 는 감싸고 Value 는 거슬러 찾습니다",
      "Background 를 사용자 값을 담은 자식이 감싸고, 그것을 다시 GUID 값을 담은 자식이 감싼 context 사슬이다. "
      "바깥 context 에서 Value(userKey) 를 부르면 가장 바깥 겹부터 키를 비교하며 안쪽으로 들어가 user 겹에서 jon 을 찾는다. "
      "어느 겹에도 없는 키는 Background 까지 내려가 nil 을 돌려준다. 이 탐색은 선형이라 값을 수십 개 담으면 느려진다.",
      lead="guidKey · userKey 와 값은 설명을 위한 예입니다. 값은 안쪽으로만 흘러 들어갑니다.")

layers = [("ctx = contextWithGUID(ctx, …)", "guidKey · \"abc-123\"", None),
          ("ctx = ContextWithUser(ctx, \"jon\")", "userKey · \"jon\"", INFO),
          ("context.Background()", "값 없음 · 사슬의 끝", None)]
for k, (title, kv, c) in enumerate(layers):
    x, y = X0 + k * PAD, Y0 + k * (PAD + 44)
    w, h = BW - 2 * k * PAD, BH - k * (2 * PAD + 44)
    if c:
        d.tone(x, y, w, h, c, 8, "0d", 1.1)
    else:
        d.box(x, y, w, h, r=8)
    d.t(x + 16, y + 24, title, 12, c or INK, MONO, "start", 600)
    d.t(x + 16, y + 42, kv, 11, MUTED, kr(kv), "start")

RX = 600
d.t(RX, Y0 + 12, "ctx.Value(userKey)", 13, INK, MONO, "start", 600)
steps = [("guid 겹 · 키가 다름", SOFT, False), ("user 겹 · \"jon\" 반환", ACC, True)]
for i, (txt, c, focal) in enumerate(steps):
    y = Y0 + 32 + i * 44
    d.tone(RX, y, 340, 32, c, 4, "22" if focal else "10", 1.4 if focal else 1.0)
    d.t(RX + 16, y + 21, txt, 12, c if focal else MUTED, KR, "start", 600)

d.t(RX, Y0 + 152, "ctx.Value(otherKey)", 13, INK, MONO, "start", 600)
steps = [("guid 겹 · user 겹 · 없음", SOFT), ("Background 까지 가서 nil", BAD)]
for i, (txt, c) in enumerate(steps):
    y = Y0 + 172 + i * 44
    d.tone(RX, y, 340, 32, c, 4, "10", 1.0)
    d.t(RX + 16, y + 21, txt, 12, c if c == BAD else MUTED, KR, "start", 600)

d.legend(424, [("값을 담은 겹", INFO), ("찾아낸 곳", ACC), ("없으면 nil", BAD)])
d.save("14-01.value-chain.svg")
print("ok 14-01 value-chain")
