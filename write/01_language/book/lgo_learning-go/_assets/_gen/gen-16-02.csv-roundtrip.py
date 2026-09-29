# 16-02.csv-roundtrip — CSV 텍스트가 csv.ReadAll·Unmarshal 로 []MyData 가 되고, Marshal·csv.Writer 로 다시 텍스트가 되는 두 방향
# 본문 요구(16-02 §1 「Marshal 은 태그로 머리글을…」「Unmarshal 은 slice 의 포인터를 받아…」): 윗줄 CSV → [][]string → Unmarshal(머리글로
#           namePos, 행마다 New·unmarshalOne·Append) → []MyData. 아랫줄 []MyData → Marshal(marshalHeader 태그, marshalOne Kind) → [][]string → CSV.
# 타입 스펙: type-flowchart — 윗줄 왼→오른, 아랫줄 오른→왼, 오른쪽 끝에서 위→아래로 잇는 직교 선. 노드 200×60, stride 236.
#           focal 은 []MyData 노드 하나(리플렉션이 채우는 구조체 slice).
# 사실 출처: Learning Go 2판 16장 「Use Reflection to Write a Data Marshaler」, go1.27.1 실행(2026-09-29) — sample_code/csv 출력.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 460
NW, NH, ST = 200, 60, 236
X = [28 + i * ST for i in range(4)]
Y1, Y2 = 140, 300


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, title, sub, c=None):
    if c:
        d.tone(x, y, NW, NH, c, 6, "18" if c == ACC else "12", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 26, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 46, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "FLOWCHART · 16-02 §1",
      "태그가 열 이름을, Kind 가 칸 변환을 정합니다",
      "윗줄은 읽는 방향이다. csv.ReadAll 이 CSV 텍스트를 [][]string 으로 읽고, Unmarshal 이 머리글로 열 위치를 잡은 뒤 행마다 reflect.New 로 구조체를 만들어 "
      "unmarshalOne 으로 채우고 Append 로 붙여 []MyData 를 만든다. 아랫줄은 쓰는 방향이다. Marshal 이 csv 태그로 머리글을, 필드 Kind 로 각 칸을 만들어 "
      "[][]string 을 돌려주고 csv.Writer 가 다시 CSV 텍스트로 쓴다.",
      lead="윗줄은 텍스트를 구조체로, 아랫줄은 구조체를 텍스트로 바꿉니다.")

node(X[0], Y1, "CSV 텍스트", "name,age,has_pet")
node(X[1], Y1, "[][]string", "csv.ReadAll · 첫 행은 머리글", INFO)
node(X[2], Y1, "Unmarshal(&entries)", "New · unmarshalOne · Append", INFO)
node(X[3], Y1, "[]MyData", "태그로 필드를 채움", ACC)
for i in range(3):
    x1, x2 = X[i] + NW, X[i + 1]
    d.arrow([(x1 + 2, Y1 + NH / 2), (x2 - 4, Y1 + NH / 2)], SOFT, "soft", 1.3)

cx = X[3] + NW / 2
d.arrow([(cx, Y1 + NH + 2), (cx, Y2 - 4)], SOFT, "soft", 1.3)
d.t(cx + 10, (Y1 + NH + Y2) / 2 + 4, "entries", 11, MUTED, MONO, "start", 600)

node(X[3], Y2, "Marshal", "marshalHeader · marshalOne", INFO)
node(X[2], Y2, "[][]string", "태그 → 머리글, Kind → 칸", INFO)
node(X[1], Y2, "csv.Writer", "WriteAll", None)
node(X[0], Y2, "CSV 텍스트", "\"\"The Hammer\"\" 도 감쌈", OK)
for i in (3, 2, 1):
    d.arrow([(X[i] - 2, Y2 + NH / 2), (X[i - 1] + NW + 4, Y2 + NH / 2)], SOFT, "soft", 1.3)

d.legend(404, [("리플렉션이 채우는 구조체", ACC), ("중간 표현·변환", INFO), ("다시 쓴 텍스트", OK)])
d.save("16-02.csv-roundtrip.svg")
print("ok 16-02 csv-roundtrip")
