# 02-01.conntrack-states — conntrack flow 의 주 경로와 두 단계
# 본문 요구: "[UNREPLIED] 와 [ASSURED] 는 한 번의 전이가 아니라 두 단계다.
#            [UNREPLIED] 는 반대 방향 패킷이 관측되면 떨어지고, [ASSURED] 는 그보다 뒤에 붙는다.
#            테이블이 꽉 찼을 때 커널은 [ASSURED] 가 없는 항목을 먼저 버린다."
#            본문이 '주 경로'·'다음 단계'·'그보다 뒤'로 순서를 말하는데 도식은 순서 없는 표였다.
#            (2026-08-28 이전 이 자리의 SVG 는 생성기가 없어 타입 선택을 통째로 건너뛴 손 SVG 였다.)
# 타입 스펙: type-state.md — 상태는 rx=8 둥근 사각, 시작은 채운 점, 끝은 고리 점,
#           전이 라벨은 event / action, 자기 루프는 상태 위로. 곁가지는 상태마다 그리지 않고
#           주석 한 줄로 모은다(스펙의 "'From any state' 는 단일 주석" 규칙).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, PAPER, PAPER2, KR, MONO

W, H = 1000, 608
d = D(W, H, "CONNTRACK · MAIN PATH",
      "conntrack 엔트리가 밟는 주 경로 — 플래그 둘은 한 전이가 아니라 두 단계다",
      "conntrack flow 의 주 경로는 NEW 에서 ESTABLISHED 로 간다. [UNREPLIED] 는 반대 방향 패킷이 "
      "관측될 때 떨어지고, [ASSURED] 는 양방향으로 데이터가 실제로 오간 뒤에 붙는다. "
      "테이블이 꽉 차면 커널은 [ASSURED] 가 없는 항목부터 버린다.",
      lead="[UNREPLIED] 가 떨어지는 시점과 [ASSURED] 가 붙는 시점은 다르다")

CY = 296
DOT_X, END_X = 64, 888
NEW_CX, NEW_W = 256, 192
EST_CX, EST_W = 648, 216
BH = 112

def state(cx, w, name, desc, ttl, flag, c):
    x, y = cx - w // 2, CY - BH // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="8" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    d.t(cx, CY - 36, ddx.fit(name, 12, w - 24, name), 12, c, MONO, "middle", 600)
    d.t(cx, CY - 12, ddx.fit(desc, 12, w - 24, desc), 12, INK, KR)
    d.t(cx, CY + 14, ddx.fit(ttl, 12, w - 24, ttl), 12, MUTED, MONO)
    d.t(cx, CY + 38, ddx.fit(flag, 11, w - 24, flag), 11, SOFT, MONO)

def trans(x0, x1, main, sub, c=MUTED, mk="ar"):
    d.path(f"M {x0} {CY} L {x1-8} {CY}", c, 1.5, m=mk)
    mx = (x0 + x1) // 2
    d.t(mx, CY - 34, main, 12, c, KR)
    d.t(mx, CY - 14, sub, 11, SOFT, MONO)

# 시작 — 채운 점
d.o.append(f'<circle cx="{DOT_X}" cy="{CY}" r="6" fill="{INK}"/>')
trans(DOT_X + 8, NEW_CX - NEW_W // 2, "첫 패킷", "TCP SYN")
state(NEW_CX, NEW_W, "NEW", "응답이 아직 없다", "120초", "[UNREPLIED]", WARN)
trans(NEW_CX + NEW_W // 2, EST_CX - EST_W // 2, "반대 방향 패킷 관측", "[UNREPLIED] 해제")
state(EST_CX, EST_W, "ESTABLISHED", "양방향으로 패킷 관측", "432000초 · 닷새", "[ASSURED]", OK)
trans(EST_CX + EST_W // 2, END_X - 12, "수명 만료", "테이블에서 삭제")

# 끝 — 고리 점
d.o.append(f'<circle cx="{END_X}" cy="{CY}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{END_X}" cy="{CY}" r="5" fill="{MUTED}"/>')

# 자기 루프 — 두 번째 단계. focal 은 이 한 곳이다.
LX, RX, TOP = EST_CX - 48, EST_CX + 48, 196
d.path(f"M {LX} {CY-BH//2} C {LX} {TOP}, {RX} {TOP}, {RX} {CY-BH//2-8}", ACC, 1.6, m="acc")
d.t(EST_CX, TOP - 26, "양방향으로 데이터가 오간 뒤", 12, ACC, KR)
d.t(EST_CX, TOP - 8, "[ASSURED] 부착", 11, ACC, MONO)

# 곁가지 — 상태마다 그리지 않고 한 줄로 모은다
ddx.band(d, 416, 496, "곁가지 — 주 경로의 다음 단계가 아니다")
for x, name, desc in ((120, "RELATED", "부모 연결에 종속"),
                      (420, "INVALID", "즉시 폐기"),
                      (700, "UNTRACKED", "raw 에서 NOTRACK")):
    d.t(x, 466, name, 12, MUTED, MONO, "start", 600)
    d.t(x, 484, desc, 12, SOFT, KR, "start")

d.t(36, 536, "두 단계를 가르는 이유가 여기 있다 — 테이블이 꽉 차면 커널은 [ASSURED] 가 붙지 않은 항목부터 버린다. "
             "conntrack 의 상태는 TCP 의 상태와 별개다.", 12, MUTED, KR, "start")
d.legend(552, [("응답 대기", WARN), ("수립됨", OK), ("두 번째 단계", ACC)])
d.save("02-01.conntrack-states.svg")
print("ok conntrack-states")
