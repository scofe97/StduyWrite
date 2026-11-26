# 사실 출처: 예제 앱 관찰 기록 + Spring Security 7.1.1 FilterChainProxy·Tomcat 11.0.24
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 1000
LANE_W = 164
NAMES = [
    ("브라우저", "cookie jar"),
    ("Tomcat", "11.0.24"),
    ("Security 필터 체인", "FilterChainProxy"),
    ("DispatcherServlet", "Spring MVC"),
    ("컨트롤러", "MyAccountController"),
]
LANES_Y = 96
STRIDE = 48

# 레인 중심 x: 가장자리 24px 여백 안에서 균등 배치
span = (W - 48 - 24) - LANE_W
CX = [24 + LANE_W / 2 + span * i / (len(NAMES) - 1) for i in range(len(NAMES))]
B, T, C, DS, K = CX

# 세로 배치: 틀 상단 → 가드 → 메시지(STRIDE) → 구분선 → 가드 → 메시지 → 틀 하단
FRAME_Y = 164
G1 = FRAME_Y + 36
Y = [G1 + 40 + STRIDE * i for i in range(8)]          # 쿠키 있음 메시지 8개
DIV = Y[-1] + 36
G2 = DIV + 28
Z = [G2 + 40 + STRIDE * i for i in range(3)]          # 쿠키 없음 메시지 3개
FRAME_B = Z[-1] + 40
H = FRAME_B + 36 + 44

d = D(
    W, H,
    "SEQUENCE · REQUEST JOURNEY",
    "요청 하나가 Tomcat에서 컨트롤러까지 가는 길",
    "GET /api/my/account 한 번이 쿠키 있을 때 200, 없을 때 401로 끝나는 두 갈래",
    "세션 쿠키가 있는 요청과 없는 요청이 Security 필터 체인에서 갈리는 순서를 예제 앱에서 관찰한 값으로 그린다",
)

# 1. 레인 머리 (focal: Security 필터 체인 한 곳)
for i, (nm, sub) in enumerate(NAMES):
    x = CX[i]
    focal = i == 2
    if focal:
        d.o.append(f'<rect x="{x - LANE_W/2}" y="{LANES_Y}" width="{LANE_W}" height="44" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x - LANE_W / 2, LANES_Y, LANE_W, 44, PAPER2, RULE, 1.0)
    d.t(x, LANES_Y + 19, nm, 13, INK, KR, "middle", 600)
    d.t(x, LANES_Y + 36, sub, 11, MUTED, MONO)

# 2. 생명선
bottom = FRAME_B + 24
for x in CX:
    d.line(x, LANES_Y + 50, x, bottom, RULE, 1.0, "3 6")

# 3. alt 틀 (두 영역)
FX0, FX1 = B - 60, K + 60
d.o.append(f'<rect x="{FX0}" y="{FRAME_Y}" width="{FX1 - FX0}" height="{FRAME_B - FRAME_Y}" rx="4" fill="rgba(245,245,243,0.03)" stroke="{RULE}" stroke-width="1"/>')
d.o.append(f'<rect x="{FX0}" y="{FRAME_Y}" width="44" height="18" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
d.t(FX0 + 22, FRAME_Y + 13, "ALT", 10, MUTED, MONO, "middle", 600)
d.t(FX0 + 12, G1, "[세션 쿠키 있음]", 13, MUTED, KR, "start")
d.line(FX0 + 8, DIV, FX1 - 8, DIV, RULE, 1.0, "4 3")
d.t(FX0 + 12, G2, "[쿠키 없음]", 13, MUTED, KR, "start")


# 4. 활성 막대 (Tomcat 작업 스레드가 쥐고 있는 구간, 필터 체인이 쥐고 있는 구간)
def bar(x, y0, y1):
    d.o.append(f'<rect x="{x - 4}" y="{y0}" width="8" height="{y1 - y0}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="0.8"/>')


bar(T, Y[0] - 8, Y[7] + 8)
bar(C, Y[2] - 8, Y[5] + 8)
bar(T, Z[0] - 8, Z[2] + 8)
bar(C, Z[1] - 8, Z[2] + 8)


# 5. 메시지
def call(a, b, label, y, sub=None, c=MUTED, mk="ar"):
    x1, x2 = CX[a], CX[b]
    s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 6 * s} {y} L {x2 - 8 * s} {y}", c, 1.5, m=mk)
    d.t((x1 + x2) / 2, y - 9, label, 12, INK if c == MUTED else c, MONO, "middle", 600)
    if sub:
        kr = any("가" <= ch <= "힣" for ch in sub)
        d.t((x1 + x2) / 2, y + 17, sub, 13 if kr else 12, MUTED, KR if kr else MONO)


def ret(a, b, y, label, sub, c, mk, near_start=False):
    x1, x2 = CX[a], CX[b]
    s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 6 * s} {y} L {x2 - 8 * s} {y}", c, 1.5, m=mk, dash="6 4")
    tx = x2 + 14 if near_start else (x1 + x2) / 2
    anchor = "start" if near_start else "middle"
    d.t(tx, y - 9, label, 12, c, MONO, anchor, 600)
    d.t(tx, y + 17, sub, 13, MUTED, KR, anchor)


# 쿠키 있음
call(0, 1, "GET /api/my/account", Y[0], "JSESSIONID=CE94…")
# 자기 메시지: Tomcat 이 작업 스레드를 배정한다
d.path(f"M {T + 10} {Y[1] - 8} L {T + 58} {Y[1] - 8} L {T + 58} {Y[1] + 10} L {T + 13} {Y[1] + 10}", MUTED, 1.4, m="ar")
d.t(T + 68, Y[1] - 4, "exec-5 배정", 13, INK, KR, "start", 600)
d.t(T + 68, Y[1] + 14, "풀에서 꺼냄", 13, MUTED, KR, "start")
call(1, 2, "doFilter", Y[2], "DelegatingFilterProxy")
call(2, 1, "getSession()", Y[3], "CE94… → HttpSession")
ret(1, 2, Y[4], "SecurityContext", "SPRING_SECURITY_CONTEXT", MUTED, "ar")
call(2, 3, "doFilter", Y[5], "필터 12개 통과")
call(3, 4, "account()", Y[6], "@AuthenticationPrincipal")
ret(4, 0, Y[7], "200", "같은 길로 되돌아감", OK, "ok", near_start=True)

# 쿠키 없음
call(0, 1, "GET /api/my/account", Z[0], "쿠키 없음")
call(1, 2, "doFilter", Z[1], "스레드 exec-1")
ret(2, 0, Z[2], "401", "컨트롤러엔 닿지 않음", BAD, "bad", near_start=True)

d.legend(H - 44, [
    ("핵심 구간", ACC),
    ("200 응답", OK),
    ("401 거부", BAD),
])

out = Path(__file__).parent.parent / "01-01.request-journey.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
