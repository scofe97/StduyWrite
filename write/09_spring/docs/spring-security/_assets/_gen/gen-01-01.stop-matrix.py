# 사실 출처: 예제 앱 관찰 기록 + FilterChainProxy 기동 로그
# 타입 스펙: type-dp-security-matrix
# 고른 이유: "어느 요청이 어느 필터까지 가고 어디서 멈추는가"는 조합이 되고 안 되는 격자이므로 행렬 문법이 맞다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

FILTERS = [
    "DisableEncodeUrlFilter", "WebAsyncManagerIntegrationFilter", "SecurityContextHolderFilter",
    "HeaderWriterFilter", "CsrfFilter", "CsrfCookieFilter", "LogoutFilter", "ConcurrentSessionFilter",
    "SecurityContextHolderAwareRequestFilter", "AnonymousAuthenticationFilter",
    "ExceptionTranslationFilter", "AuthorizationFilter",
]
ROLES = [  # (1줄, 2줄)
    ("POST logout", "CSRF 헤더 있음"),
    ("POST logout", "CSRF 헤더 없음"),
    ("GET account", "쿠키 없음"),
    ("GET account", "쿠키 있음"),
]
# 행 0..11 = 필터, 행 12 = 컨트롤러. 값: (표시, 수준)
PASS, NONE = ("통과", "ok"), ("—", "none")
cells = {}
for c in range(4):
    for r in range(13):
        cells[(r, c)] = NONE
for r in range(0, 6):
    cells[(r, 0)] = PASS
cells[(6, 0)] = ("멈춤 · 204", "focal")
for r in range(0, 4):
    cells[(r, 1)] = PASS
cells[(4, 1)] = ("멈춤 · 403", "bad")
for r in range(0, 10):
    cells[(r, 2)] = PASS
cells[(10, 2)] = ("401 작성", "bad")
cells[(11, 2)] = ("거부", "warn")
for r in range(0, 12):
    cells[(r, 3)] = PASS
cells[(12, 3)] = ("200 도착", "ok")

COMP_W, ROLE_W, ROLE_GAP, GAP, LPAD = 330, 128, 16, 12, 12
HEADER_Y, HEADER_H = 96, 52
ROW0, STRIDE, ROW_H = HEADER_Y + HEADER_H + 16, 40, 36
W = LPAD + COMP_W + GAP + 4 * ROLE_W + 3 * ROLE_GAP + 48
rows_bottom = ROW0 + 12 * STRIDE + ROW_H
H = rows_bottom + 20 + 44 + 24

d = D(
    W, H,
    "MATRIX · WHERE REQUESTS STOP",
    "네 요청이 열두 필터 중 어디까지 가나",
    "필터 번호 순서대로 내려가며 통과한 칸과 멈춘 칸, 컨트롤러에 닿은 요청은 마지막 하나",
    "예제 앱 관찰값에서 요청 캐시를 끈 구성(12 개, 기동 로그로 확인)",
)


def rx(j):
    return LPAD + COMP_W + GAP + j * (ROLE_W + ROLE_GAP)


# 머리 행
d.box(LPAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LPAD + COMP_W / 2, HEADER_Y + 22, "Security 필터", 13, INK, KR, "middle", 600)
d.t(LPAD + COMP_W / 2, HEADER_Y + 40, "위에서 아래로 실행", 13, MUTED, KR)
for j, (a, b) in enumerate(ROLES):
    d.o.append(f'<rect x="{rx(j)}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(rx(j) + ROLE_W / 2, HEADER_Y + 22, a, 12, PAPER, MONO, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HEADER_Y + 40, b, 13, PAPER, KR, "middle", 400)

STYLE = {
    "ok": (OK, f"{OK}14", INK),
    "bad": (BAD, f"{BAD}22", INK),
    "warn": (WARN, f"{WARN}22", INK),
    "none": (RULE, PAPER, MUTED),
    "focal": (ACC, f"{ACC}22", ACC),
}

for r in range(13):
    y = ROW0 + r * STRIDE
    name = FILTERS[r] if r < 12 else "컨트롤러"
    d.box(LPAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LPAD + 12, y + 23, str(r + 1) if r < 12 else "", 12, SOFT, MONO, "start")
    d.t(LPAD + 40, y + 23, name, 12 if r < 12 else 13, INK, MONO if r < 12 else KR, "start")
    for c in range(4):
        text, lv = cells[(r, c)]
        stroke, fill, tc = STYLE[lv]
        sw = 1.5 if lv == "focal" else 0.9
        d.o.append(f'<rect x="{rx(c)}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        kr = any("가" <= ch <= "힣" for ch in text)
        d.t(rx(c) + ROLE_W / 2, y + 23, text, 13 if kr else 12, tc, KR if kr else MONO, "middle", 600 if lv != "none" else 400)

d.legend(H - 44, [
    ("통과", OK),
    ("멈춤 · 응답 작성", BAD),
    ("거부 예외", WARN),
    ("이 절의 요점", ACC),
])

out = Path(__file__).parent.parent / "01-01.stop-matrix.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
