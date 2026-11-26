# 사실 출처: 예제 앱 관찰 기록 + Tomcat 11.0.24·Spring Security 7.1.1
# 타입 스펙: type-nested
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 844
d = D(
    W, H,
    "NESTED · WHO HOLDS WHAT",
    "한 JVM 안에서 Tomcat과 Spring이 각자 쥔 것",
    "연결·스레드·세션은 Tomcat 칸에, 빈·필터 체인은 Spring 칸에 있고 SecurityContext 만 양쪽에 걸친다",
    "Tomcat 11.0.24와 Spring ApplicationContext 가 한 프로세스 안에서 나누어 쥔 것을 포함 관계로 그린다",
)


def kr(txt):
    return any("가" <= c <= "힣" for c in str(txt))


def fs(txt):
    """한글이 든 글은 13px, 식별자는 12px."""
    return 13 if kr(txt) else 12


def tw(txt, size=None):
    """글자 폭 추정: 한글 전각 1em, 라틴 0.62em."""
    size = size or fs(txt)
    return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(txt))


def ring(x, y, w, h, label, c, fill=None, sw=1.2, mono=False):
    """포함 상자. 이름표는 상자 안쪽 위에 둔다(테두리에 걸치지 않는다)."""
    f = fill if fill is not None else f"{c}0d"
    size = fs(label)
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f}" stroke="{c}" stroke-width="{sw}"/>')
    d.t(x + 16, y + 20, label, size, ACC if c == ACC else INK, MONO if (mono or not kr(label)) else KR, "start", 600)


def chip(x, y, txt, c=MUTED, w=None):
    """칸 안의 작은 항목 하나."""
    size = fs(txt)
    ww = w if w else tw(txt, size) + 16
    d.o.append(f'<rect x="{x}" y="{y}" width="{ww}" height="24" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
    d.t(x + ww / 2, y + 16, txt, size, INK, KR if kr(txt) else MONO)
    return ww


def line(x, y, txt, fill=INK, size=None):
    size = size or fs(txt)
    d.t(x, y, txt, size, fill, KR if kr(txt) else MONO, "start")


# 바깥: JVM 프로세스
ring(24, 104, 952, 676, "JVM 프로세스 · 포트 8080", RULE, fill="rgba(245,245,243,0.015)")

# ── Tomcat (왼쪽)
ring(48, 144, 528, 612, "Tomcat 11.0.24 (내장)", INFO, sw=1.3)

# 연결: Connector
CX0, CY0 = 72, 184
ring(CX0, CY0, 480, 96, "Connector · Http11NioProtocol", INFO, fill=f"{INFO}14")
x = CX0 + 16
for t in ("Acceptor", "Poller"):
    x += chip(x, CY0 + 32, t) + 8
x = CX0 + 16
for t in ("연결 최대 8192", "대기열 100"):
    x += chip(x, CY0 + 62, t) + 8

# 스레드 풀 ⊃ exec-5 ⊃ ThreadLocal
PX, PY = 72, 304
ring(PX, PY, 480, 156, "스레드 풀 · 최대 200, 상시 10", INFO, fill=f"{INFO}14")
EX, EY = 96, 336
ring(EX, EY, 280, 100, "exec-5 · 이 요청을 맡은 스레드", INFO, fill=f"{INFO}1c")
LX, LY, LW, LH = 112, 366, 248, 56
ring(LX, LY, LW, LH, "ThreadLocal", ACC, fill=f"{ACC}12", sw=1.5, mono=True)
line(LX + 16, LY + 44, "SecurityContext")
# 같은 풀의 다른 스레드
x = 400
for t in ("exec-1", "…"):
    x += chip(x, 340, t, w=None if t != "…" else 28) + 8

# Context ⊃ 필터 줄, 세션 저장소 ⊃ HttpSession
ring(72, 488, 480, 240, "Context · ServletContext", INFO, fill=f"{INFO}14")
FX, FY = 96, 520
ring(FX, FY, 432, 68, "서블릿 필터 줄", INFO, fill=f"{INFO}1c")
fx = FX + 16
fx += chip(fx, FY + 32, "requestIdFilter") + 8
fx += chip(fx, FY + 32, "…", w=28) + 8
FILTER_CHIP_X = fx
FILTER_CHIP_W = chip(fx, FY + 32, "springSecurityFilterChain", INFO)
ring(96, 604, 432, 108, "세션 저장소 · StandardManager", INFO, fill=f"{INFO}1c")
HX, HY = 112, 634
ring(HX, HY, 400, 66, "HttpSession · CE94…", INFO, fill=f"{INFO}26")
chip(HX + 16, HY + 30, "SPRING_SECURITY_CONTEXT", OK, w=240)

# ── Spring (오른쪽)
ring(640, 144, 312, 612, "Spring ApplicationContext", OK, sw=1.3)

# 빈 모음: Connector 줄에 맞춤
ring(664, 184, 264, 96, "SecurityConfig 가 만든 빈", OK, fill=f"{OK}14")
for i, t in enumerate(("sessionRegistry", "securityContextRepository", "csrfTokenRepository")):
    line(680, 224 + i * 20, t)

# SecurityContextHolder: ThreadLocal 줄에 맞춤
ring(664, 346, 264, 88, "SecurityContextHolder", OK, fill=f"{OK}14")
line(680, 346 + 52, "정적 클래스, 값은 스레드 쪽에")

# FilterChainProxy ⊃ SecurityFilterChain: 필터 줄에 맞춤
ring(664, 520, 264, 136, "FilterChainProxy", OK, fill=f"{OK}14")
QX, QY = 680, 550
ring(QX, QY, 232, 94, "필터 체인 12개", OK, fill=f"{OK}1c")
x = QX + 12
x += chip(x, QY + 30, "CsrfFilter") + 6
chip(x, QY + 30, "LogoutFilter")
chip(QX + 12, QY + 58, "ConcurrentSessionFilter")

# DispatcherServlet ⊃ 컨트롤러
ring(664, 672, 264, 70, "DispatcherServlet", OK, fill=f"{OK}14")
chip(680, 706, "MyAccountController")

# ── 경계를 넘는 화살표 두 개 (가로)
# 1. Spring 의 SecurityContextHolder 가 Tomcat 스레드의 ThreadLocal 에 넣고 뺀다
ay1 = LY + LH / 2
d.arrow([(664 - 2, ay1), (LX + LW + 4, ay1)], ACC, "acc", 1.5)
d.t(480, ay1 - 8, "set · clear", 12, ACC, MONO, "middle", 600)
# 2. Tomcat 의 필터 줄이 이름으로 Spring 빈을 찾는다
ay2 = FY + 44
d.arrow([(FILTER_CHIP_X + FILTER_CHIP_W + 4, ay2), (664 - 2, ay2)], MUTED, "ar", 1.5)
d.t(608, ay2 - 8, "getBean", 12, MUTED, MONO, "middle", 600)

d.legend(H - 44, [
    ("Tomcat 이 쥠", INFO),
    ("Spring 이 쥠", OK),
    ("Spring 이 스레드에 놓는 칸", ACC),
])

out = Path(__file__).parent.parent / "01-01.who-holds-what.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
