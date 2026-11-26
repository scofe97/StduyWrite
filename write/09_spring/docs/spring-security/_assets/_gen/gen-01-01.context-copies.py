# 사실 출처: 예제 앱 관찰 기록 + spring-security 7.1.1 SecurityContextHolderFilter·SecurityContextLogoutHandler
# 타입 스펙: type-process
# 고른 이유: 같은 SecurityContext 가 단계마다 두 주체(세션 속성·스레드 로컬)에서 어떻게 달라지는지를 칸 단위로 보이려면 주체×단계 격자인 process 가 맞다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LABEL_W, SLOT_W, NODE_W, NODE_H, LANE_H, RIGHT = 168, 192, 176, 56, 96, 28
STEPS = ["1 · Security 체인 앞", "2 · 컨트롤러 직전", "3 · 체인을 벗어남", "4 · 로그아웃 핸들러 뒤"]
LANES = [("세션 속성", "Tomcat 의 HttpSession", INFO), ("스레드 로컬", "Tomcat 스레드 위", OK)]
W = LABEL_W + 4 * SLOT_W + RIGHT
HEADER_Y = 100
LANE0 = HEADER_Y + 40
H = LANE0 + 2 * LANE_H + 20 + 44 + 24

d = D(
    W, H,
    "PROCESS · ONE SECURITYCONTEXT, TWO PLACES",
    "같은 SecurityContext가 단계마다 놓이는 자리",
    "세션 속성은 로그아웃 전까지 그대로이고 스레드 로컬은 요청 안에서만 채워진다",
    "Security 체인 앞, 컨트롤러 직전, 체인 뒤, 로그아웃 뒤 네 시점에 세션 속성과 스레드 로컬이 SecurityContext 를 쥐고 있는지 그린다",
)


def cx(j):
    return LABEL_W + 8 + j * SLOT_W + NODE_W / 2


def cy(k):
    return LANE0 + k * LANE_H + LANE_H / 2


# 단계 머리
for j, s in enumerate(STEPS):
    d.t(cx(j), HEADER_Y + 22, s, 13, INK, KR, "middle", 600)
d.line(24, HEADER_Y + 36, W - 24, HEADER_Y + 36, RULE, 1.0)

# 레인 배경과 이름
for k, (nm, sub, c) in enumerate(LANES):
    y = LANE0 + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 24}" height="{LANE_H}" fill="rgba(245,245,243,0.02)"/>')
    d.line(24, y, W - 24, y, RULE, 0.8)
    d.t(24, y + LANE_H / 2 - 2, nm, 13, INK, KR, "start", 600)
    d.t(24, y + LANE_H / 2 + 16, sub, 13, MUTED, KR, "start")
d.line(24, LANE0 + 2 * LANE_H, W - 24, LANE0 + 2 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE0, LABEL_W, LANE0 + 2 * LANE_H, RULE, 1.0)

# 칸: (레인, 단계) -> (제목, 부제, 색, focal)
NODES = {
    (0, 0): ("SecurityContext", "쿠키로 찾은 세션", INFO, False),
    (0, 1): ("같은 객체", "== 비교 true", INFO, False),
    (0, 2): ("그대로", "세션은 유지", INFO, False),
    (0, 3): ("삭제", "session.invalidate()", BAD, False),
    (1, 0): ("비어 있음", "요청 시작", MUTED, False),
    (1, 1): ("SecurityContext", "세션에서 꺼내 놓음", OK, True),
    (1, 2): ("비어 있음", "finally 에서 clearContext", MUTED, False),
    (1, 3): ("비어 있음", "clearContext", MUTED, False),
}
for (k, j), (t, sub, c, focal) in NODES.items():
    x, y = cx(j) - NODE_W / 2, cy(k) - NODE_H / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.tone(x, y, NODE_W, NODE_H, c, 6, "14" if c != MUTED else "0a", 1.1)
    mono = not any("가" <= ch <= "힣" for ch in t)
    d.t(cx(j), cy(k) - 3, t, 13 if not mono else 12, ACC if focal else INK, MONO if mono else KR, "middle", 600)
    sm = not any("가" <= ch <= "힣" for ch in sub)
    d.t(cx(j), cy(k) + 16, sub, 12 if sm else 13, MUTED, MONO if sm else KR)

# 같은 레인 안 화살표
for k in range(2):
    for j in range(3):
        x1, x2 = cx(j) + NODE_W / 2 + 4, cx(j + 1) - NODE_W / 2 - 4
        d.arrow([(x1, cy(k)), (x2, cy(k))], MUTED, "ar", 1.4)
# 세션에서 스레드로 같은 객체를 가리킴
d.arrow([(cx(1), cy(0) + NODE_H / 2 + 2), (cx(1), cy(1) - NODE_H / 2 - 4)], ACC, "acc", 1.6)
d.t(cx(1) + 10, (cy(0) + cy(1)) / 2 + 4, "참조", 13, ACC, KR, "start", 600)

d.legend(H - 44, [
    ("Tomcat 세션 안", INFO),
    ("스레드 로컬", OK),
    ("삭제", BAD),
    ("이 절의 요점", ACC),
])

out = Path(__file__).parent.parent / "01-01.context-copies.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
