# 사실 출처: Spring Security 7.1.1 SessionManagementConfigurer·SessionManagementFilter·CsrfConfigurer
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 736
d = D(
    W, H,
    "FLOWCHART · PAIRED TRACES · SHORTCUT VS DIRECT",
    "같은 공개 API 요청이 단축키와 직접 조립에서 갈리는 지점",
    "세션 밖에서 인증이 생긴 요청이 단축키 구성에서는 SessionManagementFilter 를 지나 세션과 토큰이 바뀌고 직접 조립에서는 그대로 지난다",
    "Spring Security 7.1.1 SessionManagementConfigurer·SessionManagementFilter 기준"
)

LX, RX = 230, 650
COL_W = 300


def step(cx, cy, title, sub, c=RULE, sw=1.1):
    d.box(cx - COL_W / 2, cy - 26, COL_W, 52, PAPER2, c, sw)
    d.t(cx, cy - 4, title, 12, INK, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def focal(cx, cy, title, sub):
    d.tone(cx - COL_W / 2, cy - 26, COL_W, 52, ACC, op="12", sw=1.4)
    d.t(cx, cy - 4, title, 12, INK, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def result(cx, cy, code, sub, c):
    d.tone(cx - COL_W / 2, cy - 26, COL_W, 52, c)
    d.t(cx, cy - 4, code, 12, c, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def ghost(cx, cy, title, sub):
    d.o.append(f'<rect x="{cx-COL_W/2}" y="{cy-26}" width="{COL_W}" height="52" rx="6" fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    d.t(cx, cy - 4, title, 12, MUTED, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, SOFT, KR)


# 공통 요청
d.box(260, 100, 360, 56, PAPER2, RULE, 1.0)
d.t(440, 123, "POST /api/public/auth/initial-password", 12, INK, MONO, "middle", 600)
d.t(440, 142, "세션 없음 · 세션 밖 인증 주입", 12, MUTED, KR)
for cx in (LX, RX):
    d.arrow([(440, 156), (440, 176), (cx, 176), (cx, 198)], MUTED, "ar", 1.4)

for cx, ttl, flow in ((LX, "단축키 구성", "sessionManagement().maximumSessions()"),
                      (RX, "직접 조립", "addFilterAfter(ConcurrentSessionFilter)")):
    d.box(cx - 170, 198, 340, 48, PAPER2, RULE, 1.0)
    d.t(cx, 218, ttl, 13, INK, KR, "middle", 600)
    d.t(cx, 236, flow, 11, MUTED, MONO)
d.line(440, 184, 440, 640, RULE, 0.8, dash="4 4")

R1, R2, R3, R4 = 296, 392, 488, 584

# 왼쪽: 단축키
d.arrow([(LX, 246), (LX, R1 - 28)], MUTED, "ar", 1.4)
step(LX, R1, "ConcurrentSessionFilter", "세션 없음 · 그대로 통과")
d.arrow([(LX, R1 + 26), (LX, R2 - 28)], MUTED, "ar", 1.4)
focal(LX, R2, "SessionManagementFilter", "함께 붙음 · 세션 밖 인증 감지")
d.arrow([(LX, R2 + 26), (LX, R3 - 28)], WARN, "warn", 1.4)
step(LX, R3, "onAuthentication", "XSRF-TOKEN 교체 · 세션 저장", WARN)
d.arrow([(LX, R3 + 26), (LX, R4 - 28)], BAD, "bad", 1.4)
result(LX, R4, "JSESSIONID 발급", "공개 API 응답에 세션 쿠키", BAD)

# 오른쪽: 직접 조립
d.arrow([(RX, 246), (RX, R1 - 28)], MUTED, "ar", 1.4)
step(RX, R1, "ConcurrentSessionFilter", "세션 없음 · 그대로 통과")
d.arrow([(RX, R1 + 26), (RX, R2 - 28)], SOFT, "soft", 1.2, dash="4 4")
ghost(RX, R2, "SessionManagementFilter", "체인에 없음")
d.arrow([(RX, R2 + 26), (RX, R3 - 28)], SOFT, "soft", 1.2, dash="4 4")
step(RX, R3, "AuthorizationFilter", "공개 API 허용")
d.arrow([(RX, R3 + 26), (RX, R4 - 28)], OK, "ok", 1.4)
result(RX, R4, "쿠키 변화 없음", "세션 · XSRF-TOKEN 그대로", OK)

d.legend(H - 56, [
    ("갈린 지점 (핵심)", ACC),
    ("비용 · 변경", WARN),
    ("부작용", BAD),
    ("정상 통과", OK),
    ("체인에 없음", SOFT),
])

out_path = Path(__file__).parent.parent / "02-02.shortcut-trap.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
