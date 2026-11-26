# 사실 출처: Spring Security 7.1.1 CsrfFilter·AuthorizationFilter·HttpStatusEntryPoint 및 개발 환경 전용 임시 인증 필터 예시
# 타입 스펙: type-flowchart
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 760
d = D(
    W, H,
    "FLOWCHART · SECURITY FILTER CHAIN",
    "요청 하나가 보안 필터를 지나는 길",
    "요청이 CSRF 검사, CSRF 쿠키 발급, 개발 환경 임시 인증 주입, URL 인가 규칙을 거쳐 컨트롤러·401·403 중 하나로 가는 흐름",
    "예제 앱 기준 · 개발 환경 전용 임시 인증 필터 예시 포함"
)

CX = 380          # 본선 열
RX = 700          # 오른쪽 분기 열
LX = 110          # 왼쪽 분기 열
BW, BH = 260, 50  # 단계 상자
DW, DH = 84, 34   # 마름모 반폭·반높이
ROWS = [118, 196, 282, 368, 454, 532, 612, 700]


def oval(cx, cy, w, label, c):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-18}" width="{w}" height="36" rx="18" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 12, INK, KR, "middle", 600)


def step(cx, cy, title, sub, c=RULE, w=BW):
    d.box(cx - w / 2, cy - BH / 2, w, BH, PAPER2, c, 1.1)
    fam = KR if any("가" <= ch <= "힣" for ch in str(title)) else MONO
    d.t(cx, cy - 4, title, 12, INK, fam, "middle", 600)
    d.t(cx, cy + 14, sub, 11, MUTED, KR)


def diamond(cx, cy, label, c=MUTED):
    pts = f"{cx},{cy-DH} {cx+DW},{cy} {cx},{cy+DH} {cx-DW},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 12, INK, KR, "middle", 600)


def result(cx, cy, title, sub, c, w=200):
    d.tone(cx - w / 2, cy - BH / 2, w, BH, c)
    d.t(cx, cy - 4, title, 12, c, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 11, MUTED, KR)


def down(y1, y2, c=MUTED, label=None):
    d.arrow([(CX, y1), (CX, y2 - 2)], c, "ar", 1.3)
    if label:
        d.t(CX + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, KR, "start")


# 0 요청
oval(CX, ROWS[0], 150, "요청 도착", INFO)
down(ROWS[0] + 18, ROWS[1] - BH / 2)

# 1 CsrfFilter
step(CX, ROWS[1], "CsrfFilter", "GET·HEAD는 검사 생략")
down(ROWS[1] + BH / 2, ROWS[2] - DH)

# 2 토큰 비교
diamond(CX, ROWS[2], "토큰 일치?", WARN)
d.arrow([(CX + DW, ROWS[2]), (RX - 100 - 2, ROWS[2])], BAD, "bad", 1.3)
d.t((CX + DW + RX - 100) / 2, ROWS[2] - 8, "아니오", 11, BAD, KR)
result(RX, ROWS[2], "403", "CSRF 거부", BAD)
down(ROWS[2] + DH, ROWS[3] - BH / 2, MUTED, "예")

# 3 CsrfCookieFilter
step(CX, ROWS[3], "CsrfCookieFilter", "XSRF-TOKEN 쿠키 발급", INFO)
down(ROWS[3] + BH / 2, ROWS[4] - DH)

# 4 임시 필터 활성?  (개발 초기 예시 분기 → 코랄)
diamond(CX, ROWS[4], "임시 필터 활성?", ACC)
d.arrow([(CX + DW, ROWS[4]), (RX - 130 - 2, ROWS[4])], ACC, "acc", 1.3)
d.t((CX + DW + RX - 130) / 2, ROWS[4] - 8, "예", 11, ACC, KR)
step(RX, ROWS[4], "개발 환경 전용 임시 인증 필터", "고정 관리자 권한 주입", ACC, w=260)
# 오른쪽 분기 → 합류점
d.path(f"M {RX} {ROWS[4]+BH/2} L {RX} {ROWS[5]} L {CX+6} {ROWS[5]}", ACC, 1.3, m="acc")
down(ROWS[4] + DH, ROWS[5] - 4, MUTED, "아니오")
d.o.append(f'<circle cx="{CX}" cy="{ROWS[5]}" r="4" fill="{INK}"/>')
d.arrow([(CX, ROWS[5] + 4), (CX, ROWS[6] - DH - 2)], MUTED, "ar", 1.3)

# 6 인가 규칙
diamond(CX, ROWS[6], "URL 규칙", INFO)
d.arrow([(CX + DW, ROWS[6]), (RX - 100 - 2, ROWS[6])], BAD, "bad", 1.3)
d.t((CX + DW + RX - 100) / 2, ROWS[6] - 8, "인증 없음", 11, BAD, KR)
result(RX, ROWS[6], "401", "HttpStatusEntryPoint", BAD)
d.arrow([(CX - DW, ROWS[6]), (LX + 90 + 2, ROWS[6])], WARN, "warn", 1.3)
d.t((CX - DW + LX + 90) / 2, ROWS[6] - 8, "역할 부족", 11, WARN, KR)
result(LX, ROWS[6], "403", "관리자 API", WARN, w=180)
down(ROWS[6] + DH, ROWS[7] - 18, OK, "통과")

# 7 컨트롤러
oval(CX, ROWS[7], 150, "컨트롤러", OK)

d.legend(H - 40, [
    ("임시 인증 분기", ACC),
    ("통과", OK),
    ("거부", BAD),
    ("권한 부족", WARN),
])

out_path = Path(__file__).parent.parent / "02-01.filter-chain.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
