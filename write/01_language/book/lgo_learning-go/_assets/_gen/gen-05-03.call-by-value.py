# 05-03.call-by-value — 함수 안에서 바꾼 것 가운데 호출자에게 보이는 것과 보이지 않는 것
# 본문 요구(05-03 §3 「Go 는 값에 의한 호출」): modifyFails 는 int·string·struct 를 바꿔도 호출자에게 안 보이고,
#           modMap 의 변경은 보이며, modSlice 는 원소 변경만 보이고 append 는 안 보인다. "어느 조합이 되는가" 형태다.
# 타입 스펙: type-dp-security-matrix — 행 = 인자 종류와 함수 안의 동작 6개, 열 = 호출자 쪽 결과 1개와 원문 예제 이름 1개.
#           03-03.struct-compat 과 같은 조정 공식(comp_col 264 · row_h 44 · row_stride 52 · header_y 112)을 쓰고,
#           열이 둘이라 role_col_w 를 188 → 280 으로 넓혔다. focal 은 결과가 둘로 갈리는 slice append 행 하나.
# 사실 출처: Learning Go 2판 5장 「Go Is Call by Value」, go1.25.1 실행(2026-09-27) — 2 Hello {0 }, map[2:hello 3:goodbye], [2 4 6].
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, PAPER2, KR, MONO

LEFT, RIGHT = 12, 48
COMP_W, GAP_CR = 264, 12
ROLE_W, ROLE_GAP = 280, 16
HEADER_Y, HEADER_H = 112, 52
ROW_H, STRIDE = 44, 52
roles = ["호출자에게 보이나", "원문 예제"]
rows = [("int", "i = i * 2", False, "modifyFails"),
        ("string", "s = \"Goodbye\"", False, "modifyFails"),
        ("struct", "p.name = \"Bob\"", False, "modifyFails"),
        ("map", "m[2] = … · delete(m, 1)", True, "modMap"),
        ("slice 원소", "s[k] = v * 2", True, "modSlice"),
        ("slice 길이", "s = append(s, 10)", False, "modSlice")]
W = LEFT + COMP_W + GAP_CR + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT   # 912
row_y = lambda k: HEADER_Y + HEADER_H + 24 + k * STRIDE
role_x = lambda j: LEFT + COMP_W + GAP_CR + j * (ROLE_W + ROLE_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 20 + 48


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "MATRIX · 05-03 §3",
      "함수 안의 변경이 호출자에게 보이는가",
      "Go 는 인자를 늘 복사해 넘긴다. int·string·struct 는 복사본을 바꾸므로 호출자에게 안 보이고, map 은 바꾼 내용이 보인다. "
      "slice 는 원소를 바꾼 것은 보이지만 append 로 늘린 길이는 안 보인다. map 과 slice 가 다르게 구는 이유는 6장의 포인터에서 풀린다.",
      lead="행은 인자 종류와 함수 안에서 한 일, 열은 호출자 쪽 결과입니다.")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H)
d.t(LEFT + COMP_W // 2, HEADER_Y + 22, "인자 · 함수 안에서 한 일", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W // 2, HEADER_Y + 40, "값에 의한 호출", 12, MUTED, KR, "middle")
for j, r in enumerate(roles):
    d.o.append(f'<rect x="{role_x(j)}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(role_x(j) + ROLE_W // 2, HEADER_Y + 32, r, 14, "#0D1117", kr(r), "middle", 600)

for k, (kind, act, seen, ex) in enumerate(rows):
    y = row_y(k)
    focal = k == 5
    if focal:
        d.tone(LEFT, y, COMP_W, ROW_H, ACC, 4, "14", 1.4)
    else:
        d.box(LEFT, y, COMP_W, ROW_H, r=4)
    d.t(LEFT + 16, y + 20, kind, 14, ACC if focal else INK, kr(kind), "start", 600)
    d.t(LEFT + 16, y + 37, act, 12, MUTED, MONO, "start")
    c = OK if seen else BAD
    d.tone(role_x(0), y, ROLE_W, ROW_H, c, 4, "18", 1.0)
    d.t(role_x(0) + ROLE_W // 2, y + 28, "보임" if seen else "안 보임", 14, c, KR, "middle", 600)
    d.box(role_x(1), y, ROLE_W, ROW_H, r=4)
    d.t(role_x(1) + ROLE_W // 2, y + 28, ex, 13, MUTED, MONO, "middle")

d.legend(bottom + 20, [("호출자에게 보임", OK), ("호출자에게 안 보임", BAD), ("한 타입 안에서 갈리는 행", ACC)])
d.save("05-03.call-by-value.svg")
print("ok 05-03 call-by-value", W, H)
