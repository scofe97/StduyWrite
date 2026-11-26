# 사실 출처: 별도 JVM 관찰(clearContext·setAuthentication(null)·invalidate) · Spring Security 7.1.1 SecurityContextLogoutHandler L74·L81·L83
# 타입 스펙: type-state
# 고른 이유: 같은 SecurityContext 객체 하나가 지우는 동작마다 도달 가능 여부와 값이 바뀌므로 객체 하나의 상태 전이로 그린다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 520
d = D(
    W, H,
    "STATE · ONE SECURITYCONTEXT, FOUR ERASES",
    "같은 SecurityContext 객체가 지우는 동작마다 달라지는 모습",
    "clearContext 는 스레드 쪽 참조만 끊고, setAuthentication(null) 은 객체 안의 인증을 비우며, invalidate 는 세션을 지운다",
    "스레드 로컬과 세션 속성이 같은 객체를 가리킴"
)

PW, GAPX, X0 = 200, 20, 10
PY = 104


def px(i):
    return X0 + i * (PW + GAPX)


def box(x, y, w, h, c, dashed=False, tone=False, op="14"):
    if dashed:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{c}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    elif tone:
        d.tone(x, y, w, h, c, op=op, sw=1.4 if c == ACC else 1.2)
    else:
        d.box(x, y, w, h, PAPER2, c, 1.1)


panels = [
    # 제목, 스레드(상태, 색, 점선), 컨텍스트(sub, 색), 속성(상태, 점선), 화살표
    ("1. 로그인 직후", ("참조 있음", OK, False), ("auth = LoginUser", OK), ("SPRING_SECURITY_CONTEXT", False), True, True),
    ("2. clearContext()", ("비어 있음", SOFT, True), ("auth = LoginUser", ACC), ("SPRING_SECURITY_CONTEXT", False), False, True),
    ("3. setAuthentication(null)", ("비어 있음", SOFT, True), ("auth = null", BAD), ("SPRING_SECURITY_CONTEXT", False), False, True),
    ("4. invalidate()", ("비어 있음", SOFT, True), ("참조 없음", SOFT), ("세션 삭제", True), False, False),
]

TY, TH = 156, 48       # 스레드 노드
CY, CH = 262, 64       # 컨텍스트 노드
AY, AH = 380, 48       # 속성 노드

# 연결선 먼저
for i, (_, th, cx, at, a_thread, a_attr) in enumerate(panels):
    x = px(i) + 16
    mid = px(i) + PW / 2
    if a_thread:
        d.arrow([(mid, TY + TH), (mid, CY - 2)], OK, "ok", 1.5)
    else:
        d.line(mid, TY + TH, mid, CY - 6, SOFT, 1.0, "3 5")
        d.t(mid + 10, (TY + TH + CY) / 2 + 4, "끊김", 12, SOFT, KR, "start")
    if a_attr:
        d.arrow([(mid, AY - 2), (mid, CY + CH + 2)], OK, "ok", 1.5)
    else:
        d.line(mid, AY + AH, mid, AY + AH, SOFT, 1.0)

for i, (ttl, th, cx, at, a_thread, a_attr) in enumerate(panels):
    x = px(i) + 16
    w = PW - 32
    mid = px(i) + PW / 2
    d.t(mid, PY + 18, ttl, 12, INK, MONO if "(" in ttl else KR, "middle", 600)
    d.line(px(i) + 8, PY + 32, px(i) + PW - 8, PY + 32, RULE, 0.8)
    # 스레드
    box(x, TY, w, TH, th[1], dashed=th[2])
    d.t(mid, TY + 20, "스레드 로컬", 12, INK if not th[2] else MUTED, KR, "middle", 600)
    d.t(mid, TY + 38, th[0], 12, MUTED, KR)
    # 컨텍스트
    if cx[1] == SOFT:
        box(x, CY, w, CH, SOFT, dashed=True)
    else:
        box(x, CY, w, CH, cx[1], tone=True, op="12" if cx[1] == ACC else "14")
    d.t(mid, CY + 26, "SecurityContext", 12, INK if cx[1] != SOFT else MUTED, MONO, "middle", 600)
    d.t(mid, CY + 46, cx[0], 12, MUTED, KR if any("가" <= ch <= "힣" for ch in cx[0]) else MONO)
    # 속성
    if at[1]:
        box(x, AY, w, AH, BAD, dashed=True)
        d.t(mid, AY + 20, "세션 attributes", 12, MUTED, KR, "middle", 600)
        d.t(mid, AY + 38, at[0], 12, BAD, KR)
    else:
        box(x, AY, w, AH, INFO)
        d.t(mid, AY + 20, "세션 attributes", 12, INK, KR, "middle", 600)
        d.t(mid, AY + 38, at[0], 11, MUTED, MONO)

d.legend(H - 56, [
    ("clearContext 뒤 인증 남음 (핵심)", ACC),
    ("정상", OK),
    ("인증 비움", BAD),
    ("세션 속성", INFO),
    ("끊김 · 없음", SOFT),
])

out_path = Path(__file__).parent.parent / "01-02.context-states.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
