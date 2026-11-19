# 06-03 §4 putenv() 와 setenv() — 환경 목록의 원소가 가리키는 곳과, 호출한 함수가 반환한 뒤에 그 문자열이 어떻게 되는가.
# 본문 근거: 이 노트 「4. C 프로그램의 환경 조작 인터페이스」의 「putenv() 와 setenv() 의 메모리 차이」.
# 값 근거: 개념 도식이라 값은 없다. putenv() 는 문자열을 복사하지 않고 그 포인터가 환경의 일부가 된다(TLPI 6.7, putenv(3) 「The string pointed to by string becomes part of the environment」),
#          setenv() 는 name 과 value 를 복사한다(setenv(3) 「This function makes copies of the strings」).
# 타입 스펙: type-process — 행마다 같은 노드 열(호출 · 원소가 가리키는 곳 · 반환한 뒤)이 같은 자리에 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, WARN, INFO, KR, MONO

NX, STRIDE, NW, NH = [40, 340, 640], 300, 200, 72
W, H = 880, 480
d = D(W, H, "TLPI · 06-03 §4",
      "putenv() 는 포인터를 등록하고 setenv() 는 문자열을 복사한다",
      "putenv() 에 지역 배열을 넘기면 environ 의 원소가 스택 프레임을 가리키므로 함수가 반환한 뒤 값이 깨진다. 정적 문자열이나 malloc() 한 문자열은 유지되고, setenv() 는 복사본을 쓰므로 인자의 수명과 무관하다.",
      lead="행마다 왼쪽에서 오른쪽으로 호출 · environ 원소가 가리키는 곳 · 호출한 함수가 반환한 뒤를 따라갑니다.")

for j, head in enumerate(("호출", "environ 원소가 가리키는 곳", "함수가 반환한 뒤")):
    d.t(NX[j] + NW / 2, 108, head, 13, MUTED, KR, "middle", 600)

ROWS = [
    # (호출, 호출 sub, 가리키는 곳, sub, 반환 뒤, sub, 색)
    ("putenv(buf)", "buf 는 지역 배열", "스택 프레임의 buf", "복사 없이 포인터만 등록", "스택이 재사용됨", "환경 값이 깨짐", WARN),
    ("putenv(str)", "str 은 정적·malloc 문자열", "그 문자열 자체", "복사 없이 포인터만 등록", "그대로 유지됨", "문자열을 고치면 환경도 바뀜", INFO),
    ("setenv(name, value, 1)", "인자는 지역 변수여도 됨", "힙의 복사본", "새 버퍼에 name=value 복사", "그대로 유지됨", "인자의 수명과 무관", OK),
]
RY, RS = 124, 100
for i, (c1, s1, c2, s2, c3, s3, col) in enumerate(ROWS):
    y = RY + i * RS
    for j, (title, sub) in enumerate(((c1, s1), (c2, s2), (c3, s3))):
        x = NX[j]
        if j == 2:
            d.tone(x, y, NW, NH, col, 6, "14", 1.1)
        else:
            d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
        d.t(x + NW / 2, y + 30, title, 13, col if j == 2 else INK, MONO if title.isascii() else KR, "middle", 600)
        d.t(x + NW / 2, y + 54, sub, 12, MUTED, MONO if sub.isascii() else KR, "middle")
    for j, lab in ((0, "등록하면"), (1, "반환하면")):
        ya = y + NH / 2
        x1, x2 = NX[j] + NW, NX[j + 1]
        d.arrow([(x1 + 2, ya), (x2 - 4, ya)], SOFT, "soft", 1.3)
        d.t((x1 + x2) / 2, ya - 8, lab, 12, MUTED, KR, "middle", 600)

d.legend(H - 56, [("위험", WARN), ("주의", INFO), ("안전", OK)])
d.save("06-03.putenv-vs-setenv.svg")
print("ok 06-03 putenv-vs-setenv")
