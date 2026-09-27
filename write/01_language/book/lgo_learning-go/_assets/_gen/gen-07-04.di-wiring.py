# 07-04.di-wiring — 구성 요소는 서로의 인터페이스만 알고, 구체 타입을 연결하는 곳은 main 하나다
# 본문 요구(07-04 §4 「암묵적 인터페이스로 의존성을 주입합니다」): LoggerAdapter·SimpleDataStore 가 SimpleLogic 이 정의한
#           Logger·DataStore 를, SimpleLogic 이 Controller 가 정의한 Logic 을 선언 없이 만족한다. Controller.SayHello 는
#           메서드 값으로 http.HandleFunc 에 넘어가 HandlerFunc 가 된다. 이 연결을 모두 main 이 한다 — 누가 누구에 기대는가가 논지.
# 타입 스펙: type-architecture — 존(main 이 연결하는 범위) 안의 노드 그래프. 노드 = 구체 타입, 간선 = "이 인터페이스로 넘긴다",
#           간선 라벨 = 받는 쪽이 정의한 인터페이스 이름. 흐름은 왼→오른, 직교 화살표만. stride: 열 x 40·280·520·760, 노드 폭 160(열 사이 80 은 간선 라벨 자리).
#           focal 은 main 존 라벨 하나(구체 타입을 아는 유일한 곳).
# 사실 출처: Learning Go 2판 7장 「Implicit Interfaces Make Dependency Injection Easier」, go1.25.1 httptest 실행(2026-09-27) —
#           200 Hello, Fred · 400 unknown user.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 984, 500
COLS = [40, 280, 520, 760]
NW = 160
TOP_Y, TOP_H = 196, 64       # 왼쪽 위 노드
BOT_Y = 324                  # 왼쪽 아래 노드
MID_Y, MID_H = 196, 192      # 가운데 세로로 긴 노드 (SimpleLogic · Controller · http)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, h, title, lines, c=None):
    if c:
        d.tone(x, y, NW, h, c, 6, "10", 1.0)
    else:
        d.box(x, y, NW, h)
    d.t(x + NW // 2, y + 26, title, 14, INK, kr(title), "middle", 600)
    for i, ln in enumerate(lines):
        d.t(x + NW // 2, y + 50 + i * 20, ln, 12, MUTED, kr(ln), "middle")


d = D(W, H, "ARCHITECTURE · 07-04 §4",
      "구체 타입을 아는 곳은 main 뿐이다",
      "의존성 주입 웹 앱의 연결도. LoggerAdapter(LogOutput) 와 SimpleDataStore 는 SimpleLogic 이 필드 타입으로 쓰는 Logger·DataStore 인터페이스를, "
      "SimpleLogic 은 컨트롤러를 위해 정의한 Logic 인터페이스를 선언 없이 만족한다. Controller.SayHello 는 메서드 값으로 http.HandleFunc 에 넘어가 "
      "http.HandlerFunc 가 된다. 이 모든 연결은 main 이 하며, 다른 구성 요소는 인터페이스만 안다.",
      lead="화살표 라벨은 받는 쪽 필드의 인터페이스 타입, 마지막은 메서드 값입니다. 점선 안이 main 입니다.")

# main 존
d.o.append(f'<rect x="24" y="148" width="{W - 72}" height="272" rx="10" fill="none" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="6 5"/>')
d.t(40, 140, "main · 구체 타입을 아는 유일한 곳", 13, ACC, KR, "start", 600)

node(COLS[0], TOP_Y, TOP_H, "LoggerAdapter", ["(LogOutput)"])
node(COLS[0], BOT_Y, TOP_H, "SimpleDataStore", ["NewSimpleDataStore()"])
node(COLS[1], MID_Y, MID_H, "SimpleLogic", ["l  Logger", "ds DataStore", "", "SayHello", "SayGoodbye"])
node(COLS[2], MID_Y, MID_H, "Controller", ["l     Logger", "logic Logic", "", "SayHello(w, r)"])
node(COLS[3], MID_Y, MID_H, "http.HandleFunc", ["\"/hello\"", "", "→ HandlerFunc", "→ http.Handler"])

# 간선 — 왼쪽 두 노드 → SimpleLogic
ly1 = TOP_Y + TOP_H // 2
ly2 = BOT_Y + TOP_H // 2
d.arrow([(COLS[0] + NW, ly1), (COLS[1] - 2, ly1)], SOFT, "soft", 1.4)
d.t((COLS[0] + NW + COLS[1]) // 2, ly1 - 8, "Logger", 12, INFO, MONO, "middle", 600)
d.arrow([(COLS[0] + NW, ly2), (COLS[1] - 2, ly2)], SOFT, "soft", 1.4)
d.t((COLS[0] + NW + COLS[1]) // 2, ly2 - 8, "DataStore", 12, INFO, MONO, "middle", 600)
# SimpleLogic → Controller
my = MID_Y + 140
d.arrow([(COLS[1] + NW, my), (COLS[2] - 2, my)], SOFT, "soft", 1.4)
d.t((COLS[1] + NW + COLS[2]) // 2, my - 8, "Logic", 12, INFO, MONO, "middle", 600)
# LoggerAdapter → Controller (위로 돌아감)
ux = COLS[0] + NW // 2
d.arrow([(ux, TOP_Y), (ux, 172), (COLS[2] + NW // 2, 172), (COLS[2] + NW // 2, MID_Y - 2)], SOFT, "soft", 1.4)
d.t((COLS[1] + COLS[2]) // 2 + NW // 2, 166, "Logger", 12, INFO, MONO, "middle", 600)
# Controller → http
hy = MID_Y + 140
d.arrow([(COLS[2] + NW, hy), (COLS[3] - 2, hy)], SOFT, "soft", 1.4)
d.t((COLS[2] + NW + COLS[3]) // 2, hy - 8, "c.SayHello", 12, INFO, MONO, "middle", 600)

d.legend(444, [("받는 쪽 필드의 인터페이스 · 메서드 값", INFO), ("main 의 범위", ACC)])
d.save("07-04.di-wiring.svg")
print("ok 07-04 di-wiring")
