# 03-03.struct-compat — firstPerson 과 다른 struct 사이에 무엇이 되고 무엇이 안 되는가
# 본문 요구(03-03 §3 「struct 비교와 변환」): 원문은 firstPerson 을 기준으로 secondPerson(같은 필드)·thirdPerson(순서 다름)·
#           fourthPerson(이름 다름)·fifthPerson(필드 추가)·익명 struct 를 차례로 들며 변환·비교·대입 가능 여부를 가른다.
#           "어느 조합이 되고 안 되는가" 형태다.
# 타입 스펙: type-dp-security-matrix — 행 = 비교 대상 struct 5개, 열 = 연산 3개(변환 · == 비교 · 대입).
#           §2 공식의 구조(comp_col · role_col · header · row_stride)를 따르되 한글 13px 하한 때문에
#           comp_col_w 208 → 264, role_col_w 148 → 188, row_h 36 → 44, row_stride 40 → 52, header_y 72 → 112 로 키웠다.
#           focal 은 규칙이 뒤집히는 익명 struct 행 하나.
# 사실 출처: Learning Go 2판 3장 「Comparing and Converting Structs」, go1.25.1 빌드(2026-09-27) —
#           secondPerson 은 변환만 되고 == 는 mismatched types, 대입은 cannot use. third·fourth·fifth 는 cannot convert.
#           익명 struct 는 g = f 와 f == g 모두 컴파일.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, PAPER2, KR, MONO

LEFT, RIGHT = 12, 48
COMP_W, GAP_CR = 264, 12
ROLE_W, ROLE_GAP = 188, 16
HEADER_Y, HEADER_H = 112, 52
ROW_H, STRIDE = 44, 52
roles = ["타입 변환", "== 비교", "대입"]
rows = [("secondPerson", "필드 이름·순서·타입 같음"),
        ("thirdPerson", "필드 순서 다름"),
        ("fourthPerson", "필드 이름 다름"),
        ("fifthPerson", "필드 하나 더 있음"),
        ("익명 struct", "필드 이름·순서·타입 같음")]
cells = [(True, False, False), (False, False, False), (False, False, False),
         (False, False, False), (True, True, True)]
W = LEFT + COMP_W + GAP_CR + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT   # 932
row_y = lambda k: HEADER_Y + HEADER_H + 24 + k * STRIDE                                   # 188 ...
role_x = lambda j: LEFT + COMP_W + GAP_CR + j * (ROLE_W + ROLE_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 20 + 48


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "MATRIX · 03-03 §3",
      "firstPerson 과 무엇이 되는가",
      "firstPerson{name string; age int} 을 기준으로 다섯 struct 와의 타입 변환·== 비교·대입 가능 여부를 가른 행렬. "
      "필드 이름·순서·타입이 모두 같은 secondPerson 은 변환만 되고, 순서·이름·개수가 다른 셋은 아무것도 안 된다. "
      "필드가 같은 익명 struct 는 변환 없이 비교와 대입까지 된다.",
      lead="행은 firstPerson 과 견줄 struct, 열은 연산입니다.")

# 헤더
d.box(LEFT, HEADER_Y, COMP_W, HEADER_H)
d.t(LEFT + COMP_W // 2, HEADER_Y + 22, "firstPerson 과 견줄 대상", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W // 2, HEADER_Y + 40, "name string · age int", 12, MUTED, MONO, "middle")
for j, r in enumerate(roles):
    d.o.append(f'<rect x="{role_x(j)}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(role_x(j) + ROLE_W // 2, HEADER_Y + 32, r, 14, "#0D1117", kr(r), "middle", 600)

for k, (name, sub) in enumerate(rows):
    y = row_y(k)
    focal = k == 4
    if focal:
        d.tone(LEFT, y, COMP_W, ROW_H, ACC, 4, "14", 1.4)
    else:
        d.box(LEFT, y, COMP_W, ROW_H, r=4)
    d.t(LEFT + 16, y + 20, name, 14, ACC if focal else INK, kr(name), "start", 600)
    d.t(LEFT + 16, y + 37, sub, 12, MUTED, KR, "start")
    for j in range(3):
        ok = cells[k][j]
        c = OK if ok else BAD
        d.tone(role_x(j), y, ROLE_W, ROW_H, c, 4, "18", 1.0)
        d.t(role_x(j) + ROLE_W // 2, y + 28, "됨" if ok else "안 됨", 14, c, KR, "middle", 600)

d.legend(bottom + 20, [("컴파일됨", OK), ("컴파일 에러", BAD), ("규칙이 풀리는 행", ACC)])
d.save("03-03.struct-compat.svg")
print("ok 03-03 struct-compat", W, H)
