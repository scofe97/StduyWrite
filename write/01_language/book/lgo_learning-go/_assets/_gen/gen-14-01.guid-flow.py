# 14-01.guid-flow — 추적 GUID 가 app1 의 업무 로직을 모른 채 지나 app2 까지 같은 값으로 전해지는 경로
# 본문 요구(14-01 §2 「추적 GUID 는 context 에 남겨 둡니다」): tracker.Middleware 가 X-GUID 헤더에서 GUID 를 꺼내거나 새로 만들어 context 에
#           담는다. LogicImpl 은 Logger 인터페이스와 RequestDecorator 함수 타입만 알고, main 이 tracker.Logger 와 tracker.Request 를 연결한다.
#           tracker.Request 가 나가는 요청에 X-GUID 를 붙이고, app2 의 미들웨어가 다시 꺼내 로그에 찍는다.
# 타입 스펙: type-architecture — 왼→오른 존 둘(app1 :3000 · app2 :4000), 존 안의 노드는 위→아래 호출 순서. 직교 화살표만.
#           focal 은 업무 로직 노드 하나(GUID 를 모름). 아래 줄에 두 서비스의 로그 칩.
# 사실 출처: Learning Go 2판 14장 「Values」 GUID tracker, go1.25.1 로컬 실행(2026-09-28) —
#           app1 GUID: note-guid-123 - starting Process with hi · app2 GUID: note-guid-123 - starting QueryHandler with query: hi.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, WARN, PAPER2, KR, MONO

W, H = 984, 588
NW, NH = 264, 52
Z1X, Z2X, ZY, ZW, ZH = 196, 612, 132, 312, 332


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, title, sub, c=None, w=NW):
    if c:
        d.tone(x, y, w, NH, c, 6, "14" if c != ACC else "18", 1.1 if c != ACC else 1.4)
    else:
        d.box(x, y, w, NH)
    d.t(x + w // 2, y + 22, title, 12, c or INK, kr(title), "middle", 600)
    d.t(x + w // 2, y + 40, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "ARCHITECTURE · 14-01 §2",
      "추적 GUID 는 업무 로직을 모른 채 서비스를 건넙니다",
      "클라이언트가 X-GUID 헤더를 붙여 app1 을 부른다. app1 의 tracker.Middleware 가 GUID 를 context 에 담고, 업무 로직 LogicImpl 은 context 만 넘길 뿐 GUID 를 모른다. "
      "주입된 Logger 가 로그 앞에 GUID 를 붙이고, 주입된 Request 데코레이터가 app2 로 나가는 요청에 X-GUID 를 다시 붙인다. app2 의 미들웨어가 그것을 꺼내 같은 GUID 로 로그를 남긴다.",
      lead="헤더가 없으면 app1 의 미들웨어가 새 UUID 를 만들고, app2 에도 같은 UUID 가 찍힙니다.")

for zx, name in ((Z1X, "app1 · :3000"), (Z2X, "app2 · :4000")):
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="10" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 5"/>')
    d.t(zx + 16, ZY + 22, name, 12, MUTED, MONO, "start", 600)

node(36, ZY + 48, "클라이언트", "X-GUID 헤더", None, 136)
ax = Z1X + (ZW - NW) // 2
node(ax, ZY + 48, "tracker.Middleware", "context 에 GUID 담기", INFO)
node(ax, ZY + 140, "LogicImpl.Process", "GUID 를 모름 · ctx 만 넘김", ACC)
node(ax, ZY + 232, "tracker.Request", "나가는 요청에 X-GUID", INFO)
bx = Z2X + (ZW - NW) // 2
node(bx, ZY + 232, "tracker.Middleware", "헤더에서 GUID 꺼냄", INFO)
node(bx, ZY + 140, "QueryHandler", "Logger 로 로그", None)

d.arrow([(36 + 136 + 2, ZY + 74), (ax - 4, ZY + 74)], SOFT, "soft", 1.3)
cx = ax + NW // 2
d.arrow([(cx, ZY + 100 + 2), (cx, ZY + 140 - 4)], SOFT, "soft", 1.3)
d.t(cx + 10, ZY + 124, "ctx", 11, MUTED, MONO, "start", 600)
d.arrow([(cx, ZY + 192 + 2), (cx, ZY + 232 - 4)], SOFT, "soft", 1.3)
d.t(cx + 10, ZY + 216, "RequestDecorator", 11, MUTED, MONO, "start", 600)
d.arrow([(ax + NW + 2, ZY + 258), (bx - 4, ZY + 258)], OK, "ok", 1.3)
d.t((ax + NW + bx) // 2, ZY + 250, "X-GUID", 11, OK, MONO, "middle", 600)
bcx = bx + NW // 2
d.arrow([(bcx, ZY + 232 - 2), (bcx, ZY + 192 + 4)], SOFT, "soft", 1.3)

LY = ZY + ZH + 24
d.tone(Z1X, LY, ZW, 32, OK, 4, "10", 1.0)
d.t(Z1X + 12, LY + 21, "GUID: note-guid-123 - starting Process…", 11, OK, MONO, "start", 600)
d.tone(Z2X, LY, ZW, 32, OK, 4, "10", 1.0)
d.t(Z2X + 12, LY + 21, "GUID: note-guid-123 - starting QueryHandler…", 11, OK, MONO, "start", 600)

d.legend(532, [("GUID 를 다루는 tracker", INFO), ("GUID 를 모르는 업무 로직", ACC), ("같은 GUID", OK)])
d.save("14-01.guid-flow.svg")
print("ok 14-01 guid-flow")
