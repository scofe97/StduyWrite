# 15-04.stub-shapes — Logic 의 Entities 자리에 끼우는 두 스텁. 임베딩 스텁은 쓰는 메서드만 구현하고 나머지는 nil 패닉, 함수 필드 스텁은 사례마다 답을 끼운다
# 본문 요구(15-04 §1 「큰 인터페이스는 임베딩해서 쓰는 메서드만 구현합니다」「함수 필드 스텁은 사례마다 동작을 바꿉니다」):
#           GetPetNamesStub 은 Entities 를 임베딩해 GetPets 만 구현하고, 나머지 넷을 부르면 nil 역참조 패닉이다. EntitiesStub 은 메서드마다
#           함수 필드를 두고, 사례마다 새 스텁에 그 사례의 getPets 를 넣는다.
# 타입 스펙: type-architecture — 위 가운데 Logic 노드 하나, 아래 왼·오른 존 둘(각 440 폭). 존 안은 위→아래 노드. 직교 화살표만.
#           focal 은 함수 필드 스텁의 "사례마다 새 스텁" 노드 하나.
# 사실 출처: Learning Go 2판 15장 「Using Stubs in Go」, go1.27.1 실행(2026-09-28) — GetUser 호출 시 invalid memory address or nil pointer dereference.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 580
ZL, ZR, ZY, ZW, ZH = 36, 508, 232, 440, 272
NW, NH = 392, 52


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, title, sub, c=None, w=NW):
    if c:
        d.tone(x, y, w, NH, c, 6, "18" if c == ACC else "12", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 22, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + 41, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "ARCHITECTURE · 15-04 §1",
      "임베딩 스텁은 한 구현을 나눠 쓰고 함수 필드 스텁은 사례마다 답을 끼웁니다",
      "Logic 은 Entities 인터페이스를 필드로 받는다. 왼쪽 GetPetNamesStub 은 Entities 를 임베딩해 GetPets 만 구현하고, 구현하지 않은 GetUser 같은 메서드를 부르면 "
      "임베딩된 nil 인터페이스 때문에 패닉이 난다. 오른쪽 EntitiesStub 은 메서드마다 같은 시그니처의 함수 필드를 두고 메서드가 그 필드를 부른다. "
      "테이블 테스트는 사례마다 새 EntitiesStub 을 만들어 그 사례의 getPets 를 넣는다.",
      lead="왼쪽은 한 구현에 모든 사례의 답을 넣고, 오른쪽은 사례가 스텁의 답을 정합니다.")

node(296, 104, "Logic", "Entities Entities 필드", None, 392)
lx, rx = ZL + ZW / 2, ZR + ZW / 2
d.line(492, 156, 492, 188, SOFT, 1.3)
d.line(lx, 188, rx, 188, SOFT, 1.3)
d.arrow([(lx, 188), (lx, ZY - 4)], SOFT, "soft", 1.3)
d.arrow([(rx, 188), (rx, ZY - 4)], SOFT, "soft", 1.3)
d.t(504, 180, "인터페이스 자리에 끼움", 11, MUTED, KR, "start", 600)

for zx, name in ((ZL, "임베딩 스텁 · GetPetNamesStub"), (ZR, "함수 필드 스텁 · EntitiesStub")):
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="10" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 5"/>')
    d.t(zx + 16, ZY + 22, name, 12, MUTED, KR, "start", 600)

nx = ZL + (ZW - NW) / 2
node(nx, ZY + 40, "struct { Entities }", "임베딩한 인터페이스 값은 nil", INFO)
node(nx, ZY + 124, "GetPets", "직접 구현 · switch userID", OK)
node(nx, ZY + 196, "GetUser · GetChildren …", "구현 안 함 → nil 역참조 패닉", BAD)
d.arrow([(ZL + ZW / 2, ZY + 92 + 2), (ZL + ZW / 2, ZY + 124 - 4)], SOFT, "soft", 1.2)
d.t(ZL + ZW / 2 + 10, ZY + 114, "쓰는 메서드만", 11, MUTED, KR, "start", 600)

mx = ZR + (ZW - NW) / 2
node(mx, ZY + 40, "사례의 getPets 필드", "func(userID string) ([]Pet, error)", INFO)
node(mx, ZY + 124, "EntitiesStub{getPets: d.getPets}", "사례마다 새 스텁", ACC)
node(mx, ZY + 196, "GetPets(userID)", "return es.getPets(userID)", OK)
d.arrow([(ZR + ZW / 2, ZY + 92 + 2), (ZR + ZW / 2, ZY + 124 - 4)], SOFT, "soft", 1.2)
d.arrow([(ZR + ZW / 2, ZY + 176 + 2), (ZR + ZW / 2, ZY + 196 - 4)], SOFT, "soft", 1.2)

d.legend(528, [("스텁 구조", INFO), ("쓰는 메서드", OK), ("부르면 패닉", BAD), ("사례가 정하는 답", ACC)])
d.save("15-04.stub-shapes.svg")
print("ok 15-04 stub-shapes")
