# 10-02.import-cycle — 서로 import 하는 두 패키지는 컴파일 오류이고, 합치거나 원인 항목을 옮겨 푼다
# 본문 요구(10-02 §4 「순환 의존은 허용되지 않습니다」): pet 이 person 을, person 이 pet 을 import 하면 import cycle not allowed 로
#           빌드가 실패한다. 두 패키지를 하나로 합치거나, 나눠 둘 이유가 있으면 순환을 일으키는 항목만 한쪽이나 새 패키지로 옮긴다.
# 타입 스펙: type-architecture — 판 셋을 좌우로(순환 · 해결 1 합치기 · 해결 2 옮기기). 판 폭 296, 간격 16. 판 안은 노드와 직교 화살표.
#           focal 은 순환 판의 오류 칩 하나. 해결 2 의 새 패키지 이름 shared 는 설명을 위한 예다.
# 사실 출처: Learning Go 2판 10장 「Avoiding Circular Dependencies」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 452
PW, PG, PX0, PY, PH = 296, 16, 36, 132, 256


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def panel(k, title, c=None):
    x = PX0 + k * (PW + PG)
    d.box(x, PY, PW, PH, r=8)
    d.t(x + 16, PY + 24, title, 13, c or INK, KR, "start", 600)
    return x


def node(x, y, w, name, c=None):
    if c:
        d.tone(x, y, w, 40, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, 40, r=6)
    d.t(x + w // 2, y + 25, name, 13, c or INK, MONO, "middle", 600)


d = D(W, H, "ARCHITECTURE · 10-02 §4",
      "서로 import 하면 빌드되지 않습니다",
      "왼쪽 판은 pet 이 person 을, person 이 pet 을 import 한 순환으로 import cycle not allowed 로 실패한다. "
      "가운데 판은 두 패키지를 하나로 합친 해결이고, 오른쪽 판은 순환을 일으키는 항목만 새 패키지로 옮겨 두 패키지가 그쪽만 import 하게 한 해결이다.",
      lead="화살표는 import 방향입니다. 오른쪽 판의 shared 는 설명을 위한 예입니다.")

# 순환
x = panel(0, "순환 · 컴파일 오류", BAD)
node(x + 24, PY + 56, 104, "pet", None)
node(x + PW - 128, PY + 56, 104, "person", None)
d.arrow([(x + 128, PY + 70), (x + PW - 132, PY + 70)], BAD, "bad", 1.3)
d.arrow([(x + PW - 128, PY + 86), (x + 132, PY + 86)], BAD, "bad", 1.3)
d.tone(x + 24, PY + 132, PW - 48, 36, ACC, 4, "22", 1.4)
d.t(x + PW // 2, PY + 155, "import cycle not allowed", 12, ACC, MONO, "middle", 600)
d.t(x + PW // 2, PY + 200, "직접이든 간접이든 되돌아오면 금지", 12, MUTED, KR, "middle")

# 해결 1
x = panel(1, "해결 1 · 하나로 합치기", OK)
node(x + 48, PY + 72, PW - 96, "pet + person", OK)
d.t(x + PW // 2, PY + 150, "너무 잘게 쪼갠 경우", 12, MUTED, KR, "middle")
d.t(x + PW // 2, PY + 172, "서로 기대면 한 패키지일 가능성이 큼", 12, MUTED, KR, "middle")

# 해결 2
x = panel(2, "해결 2 · 원인 항목 옮기기", OK)
node(x + 24, PY + 56, 104, "pet", None)
node(x + PW - 128, PY + 56, 104, "person", None)
node(x + PW // 2 - 64, PY + 160, 128, "shared", OK)
d.arrow([(x + 76, PY + 96), (x + 76, PY + 180), (x + PW // 2 - 68, PY + 180)], SOFT, "soft", 1.2)
d.arrow([(x + PW - 76, PY + 96), (x + PW - 76, PY + 180), (x + PW // 2 + 68, PY + 180)], SOFT, "soft", 1.2)
d.t(x + PW // 2, PY + 228, "두 패키지가 한쪽만 import", 12, MUTED, KR, "middle")

d.legend(396, [("순환 import", BAD), ("빌드 실패", ACC), ("해결", OK)])
d.save("10-02.import-cycle.svg")
print("ok 10-02 import-cycle")
