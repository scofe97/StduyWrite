# 04-01.block-shadow — 블록은 겹겹이 들어 있고, 안쪽에서 같은 이름을 선언하면 바깥 것을 가린다
# 본문 요구(04-01 §1 「블록」·§2 「섀도잉」): universe 블록이 모든 블록을 담고, 그 안에 패키지·파일·함수·if 블록이
#           차례로 들어간다. 예제 4-1 의 if 블록 안 x := 5 가 함수 블록의 x 를 가리고, 예제 4-3 의 fmt := "oops" 가
#           파일 블록의 fmt 를, 예제 4-4 의 true := 10 이 universe 블록의 true 를 가린다 — 포함 관계가 논지다.
# 타입 스펙: type-nested — 바깥에서 안쪽으로 겹친 둥근 사각형, 한 겹당 안쪽 여백 24. 블록 이름은 좌상단 라벨,
#           그 블록에 선언된 식별자는 오른쪽 칩. focal 은 가리는 선언이 있는 if 블록 하나.
#           stride: 겹 여백 24(좌우)·44(위), 칩 높이 20. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 4장 「Blocks」「Shadowing Variables」「The Universe Block」, go1.25.1 실행(2026-09-27) —
#           예제 4-1 출력 10 5 10, 예제 4-4 출력 true 10, 예제 4-3 은 fmt.Println undefined.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 560
X0, Y0, W0, H0 = 24, 104, 936, 384
PADX, PADY = 24, 56
layers = [
    ("universe 블록", "true · false · int · string · nil · make"),
    ("패키지 블록", "함수 밖에 선언한 변수 · 상수 · 타입 · 함수"),
    ("파일 블록", "import 한 패키지 이름 fmt"),
    ("함수 블록 · main", "x := 10  · 매개변수도 여기"),
    ("if 블록", "x := 5  → 바깥 x 를 가림"),
]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NESTED · 04-01 §1",
      "블록은 겹겹이 들어 있다",
      "universe 블록이 패키지 블록을, 패키지 블록이 파일 블록을, 파일 블록이 함수 블록을, 함수 블록이 if 블록을 담는 겹 구조. "
      "안쪽 블록은 바깥 블록의 식별자를 쓸 수 있고, 같은 이름을 새로 선언하면 그 블록이 끝날 때까지 바깥 것을 가린다. "
      "if 블록의 x := 5 가 함수 블록의 x 를 가리는 것이 예제 4-1 이다.",
      lead="바깥 상자일수록 넓은 블록입니다. 오른쪽 글은 그 블록에 선언된 이름입니다.")

for k, (name, decl) in enumerate(layers):
    x, y = X0 + k * PADX, Y0 + k * PADY
    w, h = W0 - 2 * k * PADX, H0 - k * PADY - (0 if k == 0 else k * 8)
    focal = k == 4
    stroke = ACC if focal else "rgba(191,192,192,0.30)"
    fill = (ACC + "14") if focal else ("#161B22" if k % 2 else "#0D1117")
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{1.4 if focal else 0.9}"/>')
    d.t(x + 16, y + 26, name, 14, ACC if focal else INK, kr(name), "start", 600)
    d.t(x + w - 16, y + 26, decl, 13, ACC if focal else MUTED, kr(decl), "end")

# 가림 표시 — if 블록의 x 에서 함수 블록의 x 로
fx = X0 + 3 * PADX + (W0 - 6 * PADX) - 16
d.t(X0 + 4 * PADX + 16, Y0 + 4 * PADY + 60, "fmt.Println(x) → 5", 13, INK, MONO, "start")
d.t(X0 + 4 * PADX + 16, Y0 + 4 * PADY + 84, "블록이 끝나면 다시 10", 12, MUTED, KR, "start")

d.legend(504, [("가리는 선언이 있는 블록", ACC), ("바깥 블록", SOFT)])
d.save("04-01.block-shadow.svg")
print("ok 04-01 block-shadow")
