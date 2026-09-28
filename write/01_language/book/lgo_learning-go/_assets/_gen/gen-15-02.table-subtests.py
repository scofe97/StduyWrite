# 15-02.table-subtests — 사례 슬라이스의 원소 하나가 하위 테스트 하나가 되고, -run 은 부모/사례 이름으로 하나만 고른다
# 본문 요구(15-02 §1 「하위 테스트는 이름으로 보고되고 이름으로 골라 돌립니다」): TestDoMathTable 아래 addition · subtraction ·
#           multiplication · division · bad_division 다섯 하위 테스트. -run 'TestDoMathTable/bad_division' 은 그 하나만 돈다.
#           multiplication(2, 2) 는 더하기 버그가 있어도 4 라 통과한다.
# 타입 스펙: type-tree — root 1 · 자식 5(leaf). 노드 176×52, 가로 stride 192, 단 간격 116. 연결선은 꺾은선(수직 → 가로 버스 → 수직).
#           focal 은 -run 이 고른 leaf 하나(coral). multiplication 은 warn 테두리로 "통과했지만 버그를 가림".
# 사실 출처: Learning Go 2판 15장 「Running Table Tests」, go1.27.1 실행(2026-09-28) — -v 출력 다섯 PASS, -run 결과 bad_division 하나.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 984, 460
NW, NH, STRIDE = 176, 52, 192
X0 = (W - (5 * STRIDE - 16)) // 2
ROOT_Y, BUS_Y, L1_Y = 116, 196, 232


def cx(j):
    return X0 + j * STRIDE + NW // 2


d = D(W, H, "TREE · 15-02 §1",
      "사례 한 줄이 하위 테스트 하나가 되고 이름으로 골라 돌립니다",
      "TestDoMathTable 의 사례 슬라이스 다섯 원소가 t.Run 으로 하위 테스트 다섯이 된다. 결과는 TestDoMathTable/사례이름 으로 따로 보고되고, "
      "-run 'TestDoMathTable/bad_division' 은 그 하위 테스트 하나만 돌린다. multiplication 사례는 2 와 2 라 더하기로 잘못 짠 곱셈도 4 를 내어 통과한다.",
      lead="사례 이름이 하위 테스트 이름이 됩니다. -run 은 / 로 나뉜 이름의 부분마다 맞춥니다.")

rx = W // 2
d.line(rx, ROOT_Y + 44, rx, BUS_Y, SOFT, 1.0)
d.line(cx(0), BUS_Y, cx(4), BUS_Y, SOFT, 1.0)
for j in range(5):
    d.line(cx(j), BUS_Y, cx(j), L1_Y, SOFT, 1.0)

d.box(rx - 140, ROOT_Y, 280, 44)
d.t(rx, ROOT_Y + 27, "TestDoMathTable", 14, INK, MONO, "middle", 600)

cases = [("addition", "2 + 2 = 4", None), ("subtraction", "2 - 2 = 0", None), ("multiplication", "2 * 2 → 4 · 버그 가림", WARN),
         ("division", "2 / 2 = 1", None), ("bad_division", "-run 이 고름", ACC)]
for j, (name, sub, c) in enumerate(cases):
    x = cx(j) - NW // 2
    if c:
        d.tone(x, L1_Y, NW, NH, c, 6, "14" if c == ACC else "10", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, L1_Y, NW, NH)
    d.t(cx(j), L1_Y + 22, name, 13, c or INK, MONO, "middle", 600)
    d.t(cx(j), L1_Y + 42, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

cmd = "go test -v -run 'TestDoMathTable/bad_division'"
d.t(cx(4) + NW // 2, L1_Y + NH + 44, cmd, 12, ACC, MONO, "end", 600)
d.t(cx(4) + NW // 2, L1_Y + NH + 66, "→ TestDoMathTable/bad_division 하나만 PASS", 11, MUTED, KR, "end")

d.legend(400, [("-run 이 고른 하위 테스트", ACC), ("통과했지만 버그를 가린 사례", WARN)])
d.save("15-02.table-subtests.svg")
print("ok 15-02 subtests")
