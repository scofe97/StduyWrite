# 사실 출처: Spring Security 7.1.1 LogoutFilter L99-L111·CookieClearingLogoutHandler L78 · 예제 앱 로그아웃 응답 관찰
# 타입 스펙: type-process
# 고른 이유: 필터가 단계마다 응답에 무엇을 쌓고 어디서 끝내는지가 논지라, 왼쪽 단계 열과 오른쪽 응답 누적 열을 같은 행으로 잇는 파이프라인을 쓴다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 660
d = D(
    W, H,
    "PROCESS · LOGOUTFILTER ENDS THE REQUEST",
    "LogoutFilter 가 단계마다 응답에 쌓고 직접 끝내는 과정",
    "왼쪽은 필터가 하는 일, 오른쪽은 그 시점까지 응답에 실린 것",
    "컨트롤러와 뒤 필터는 이 요청을 보지 못함"
)

LX, LW = 24, 380
RX, RW = 472, 384
Y0, BH, STRIDE = 128, 68, 96

steps = [
    ("POST /api/my/logout", "쿠키 JSESSIONID · 헤더 X-XSRF-TOKEN", INFO, ["(비어 있음)"]),
    ("LogoutFilter", "로그아웃 URL 과 일치", INFO, ["(비어 있음)"]),
    ("LogoutHandler 묶음", "로그 · 쿠키 삭제 · 토큰 정리 · 세션 무효화", INFO,
     ["Set-Cookie: JSESSIONID=; Expires=1970…", "Set-Cookie: XSRF-TOKEN=; Expires=1970…"]),
    ("성공 핸들러", "상태 204 고정", OK,
     ["Set-Cookie: JSESSIONID=; Expires=1970…", "Set-Cookie: XSRF-TOKEN=; Expires=1970…", "204 No Content"]),
    ("return", "chain.doFilter 를 부르지 않음", ACC, ["응답 완료", "컨트롤러 · 뒤 필터 미도달"]),
]


def yy(i):
    return Y0 + i * STRIDE


d.t(LX + LW / 2, Y0 - 18, "필터가 하는 일", 12, SOFT, KR, "middle", 600)
d.t(RX + RW / 2, Y0 - 18, "그때까지 응답에 실린 것", 12, SOFT, KR, "middle", 600)

# 연결선 먼저
for i in range(len(steps) - 1):
    d.arrow([(LX + LW / 2, yy(i) + BH), (LX + LW / 2, yy(i + 1) - 2)], MUTED, "ar", 1.4)
for i, (_, _, c, _) in enumerate(steps):
    col = {INFO: "ar", OK: "ok", ACC: "acc"}[c]
    d.arrow([(LX + LW + 2, yy(i) + BH / 2), (RX - 2, yy(i) + BH / 2)], c if c != INFO else MUTED, col, 1.2, dash="4 4")

for i, (ttl, sub, c, resp) in enumerate(steps):
    y = yy(i)
    if c == ACC:
        d.tone(LX, y, LW, BH, ACC, op="12", sw=1.4)
    else:
        d.box(LX, y, LW, BH, PAPER2, c, 1.1)
    d.t(LX + LW / 2, y + 28, ttl, 12, INK, MONO, "middle", 600)
    d.t(LX + LW / 2, y + 50, sub, 12, MUTED, KR)
    d.box(RX, y, RW, BH, PAPER2, RULE, 1.0)
    n = len(resp)
    top = y + BH / 2 - (n - 1) * 9 + 4
    for k, line in enumerate(resp):
        col = OK if line.startswith("204") else (MUTED if line.startswith("(") else INK)
        d.t(RX + RW / 2, top + k * 18, line, 11 if line.startswith("Set-Cookie") else 12, col, MONO if not any("가" <= ch <= "힣" for ch in line) else KR)

d.legend(H - 56, [
    ("체인을 넘기지 않고 끝냄 (핵심)", ACC),
    ("성공 응답", OK),
    ("필터 단계", INFO),
])

out_path = Path(__file__).parent.parent / "01-02.logout-trace.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
