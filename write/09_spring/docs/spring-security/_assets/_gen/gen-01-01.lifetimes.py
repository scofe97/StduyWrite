# 사실 출처: 예제 앱 관찰 기록
# 타입 스펙: type-gantt
# 고른 이유: 연결·스레드·세션이 "얼마나 오래 사는가"가 논지이므로 막대 길이가 곧 수명인 간트가 맞다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 544
LABEL_X, TL_X0, TL_X1 = 24, 252, 976
SLOT = (TL_X1 - TL_X0) / 4
AXIS_Y = 112

d = D(
    W, H,
    "GANTT · LIFETIMES ACROSS 4 REQUESTS",
    "요청 네 번 동안 무엇이 얼마나 사는가",
    "연결과 작업 스레드는 요청마다 바뀌고 쿠키와 세션은 로그인부터 로그아웃까지 이어진다",
    "예제 앱에 curl 로 보낸 401, 예제 앱 로그인(204), 200, 로그아웃 204 네 요청에서 연결·스레드·쿠키·세션이 존재한 구간을 그린다",
)

REQS = [("요청 1", "GET · 401"), ("요청 2", "예제 앱 로그인(204)"), ("요청 3", "GET · 200"), ("요청 4", "로그아웃 · 204")]


def sx(i, frac=0.0):
    return TL_X0 + (i + frac) * SLOT


# 시간축 머리
for i, (a, b) in enumerate(REQS):
    cx = sx(i, 0.5)
    d.t(cx, AXIS_Y, a, 13, INK, KR, "middle", 600)
    d.t(cx, AXIS_Y + 18, b, 13, MUTED, KR)
d.line(LABEL_X, AXIS_Y + 30, TL_X1, AXIS_Y + 30, RULE, 1.0)
for i in range(5):
    d.line(sx(i), AXIS_Y + 30, sx(i), 480, RULE, 0.8, "3 6")

ROW = 48


def zone(y, h, label):
    d.o.append(f'<rect x="{LABEL_X - 8}" y="{y}" width="{TL_X1 - LABEL_X + 16}" height="{h}" rx="6" fill="rgba(245,245,243,0.02)" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(LABEL_X + 4, y + 18, label, 13, SOFT, KR, "start", 600)


def bar(y, x0, x1, text, c=MUTED, focal=False):
    stroke = ACC if focal else c
    fill = f"{ACC}22" if focal else f"{c}22"
    d.o.append(f'<rect x="{x0}" y="{y + 12}" width="{x1 - x0}" height="24" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{1.5 if focal else 1.0}"/>')
    if text:
        kr = any("가" <= c <= "힣" for c in text)
        d.t((x0 + x1) / 2, y + 29, text, 13 if kr else 12, ACC if focal else INK, KR if kr else MONO, "middle", 600)


def label(y, a, b=None):
    d.t(LABEL_X + 4, y + 26 if not b else y + 22, a, 13, INK, KR if any("가" <= c <= "힣" for c in a) else MONO, "start", 600)
    if b:
        kr = any("가" <= c <= "힣" for c in b)
        d.t(LABEL_X + 4, y + 40, b, 13 if kr else 12, MUTED, KR if kr else MONO, "start")


# 구역 1: 요청 하나 안에서만 사는 것
Z1 = 164
zone(Z1, 118, "요청 하나 안에서만")
r1 = Z1 + 26
label(r1, "TCP 연결", "curl 은 매번 새로")
for i in range(4):
    bar(r1, sx(i, 0.12), sx(i, 0.88), f"연결 {i + 1}", INFO)
r2 = r1 + ROW
label(r2, "작업 스레드")
for i, t in enumerate(("exec-1", "exec-2", "exec-5", "exec-7")):
    bar(r2, sx(i, 0.12), sx(i, 0.88), t, INFO)

# 구역 2: 요청을 넘어 사는 것
Z2 = Z1 + 118 + 16
zone(Z2, 170, "요청을 넘어서")
r3 = Z2 + 26
label(r3, "브라우저 쿠키", "JSESSIONID")
bar(r3, sx(1, 0.86), sx(3, 0.86), "CE94…", MUTED)
r4 = r3 + ROW
label(r4, "Tomcat 세션 표", "CE94…")
bar(r4, sx(1, 0.4), sx(3, 0.4), "HttpSession", INFO, focal=True)
r5 = r4 + ROW
label(r5, "세션 속성", "SPRING_SECURITY_CONTEXT")
bar(r5, sx(1, 0.55), sx(3, 0.4), "SecurityContext", OK)

d.legend(H - 44, [
    ("Tomcat 이 쥠", INFO),
    ("Spring 의 객체", OK),
    ("브라우저 쿠키", MUTED),
    ("이 절의 요점", ACC),
])

out = Path(__file__).parent.parent / "01-01.lifetimes.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
