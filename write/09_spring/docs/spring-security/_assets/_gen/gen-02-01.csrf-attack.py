# 사실 출처: Spring Security 7.1.1 CsrfConfigurer.spa()·CsrfFilter, Spring Boot same-site: lax, 01-02 세션 저장소 구조
# 타입 스펙: type-sequence
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 988
seq = Seq(
    W, H,
    "SEQUENCE · CSRF ATTACK & DEFENSE",
    "CSRF 공격 흐름과 이중 제출 쿠키 방어",
    "로그인된 브라우저의 세션 쿠키 자동 전송 악용과 두 겹 방어(SameSite=Lax · X-XSRF-TOKEN 검증)",
    "세션 쿠키 자동 전송 악용 vs 두 겹 방어(SameSite=Lax 쿠키 제외 · X-XSRF-TOKEN 대조 차단)"
)

seq.lanes([
    ("사용자 브라우저", "Chrome · 세션 보관"),
    ("악성 사이트", "evil.com · 위조 유도"),
    ("대상 웹 앱", "앱 서버 · Spring"),
], y0=104, lane_w=200)
seq.rails(910)

def msg_across(a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    """레인 건너는 메시지: 한국어는 KR 폰트, 실제 경로는 MONO 로 렌더."""
    x1, x2 = seq.LX[a], seq.LX[b]
    d = 1 if x2 > x1 else -1
    seq.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    is_label_kr = any('가' <= ch <= '힣' for ch in str(label))
    seq.t(mx, y - 9, label, 11, c, KR if is_label_kr else MONO, "middle", 600)
    if sub:
        is_sub_kr = any('가' <= ch <= '힣' for ch in str(sub))
        seq.t(mx, y + 15, sub, 11, MUTED, KR if is_sub_kr else MONO, "middle")

def selfmsg_left(a, label, y, c=MUTED, sub=None):
    """우측 끝 레인의 자체 메시지: 캔버스 우측 이탈을 방지하고 좌측 빈 공간으로 루프."""
    x = seq.LX[a]
    seq.path(f"M {x - 10} {y - 10} L {x - 48} {y - 10} L {x - 48} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
    seq.t(x - 56, y - 4, label, 11, c, KR, "end", 600)
    if sub:
        seq.t(x - 56, y + 13, sub, 11, MUTED, KR, "end")

def branch_label(cx, y, text, c):
    """갈래 라벨: 악성 사이트 생명선 관통 방지를 위해 배경을 깔고 텍스트 렌더."""
    w = sum(11 if '가' <= ch <= '힣' else 7 for ch in text) + 16
    seq.o.append(f'<rect x="{cx - w/2}" y="{y - 12}" width="{w}" height="18" rx="3" fill="{PAPER}"/>')
    seq.t(cx, y, text, 11, c, KR, "middle", 600)

# 단계 제목 시작 x: 브라우저 생명선(x=124)과 겹치지 않도록 오른쪽(x=144)에 배치
TITLE_X = seq.LX["사용자 브라우저"] + 20

# ① 대상 웹 앱 정상 로그인
seq.t(TITLE_X, 168, "① 정상 로그인 (세션 쿠키 발급)", 11, SOFT, KR, "start")
msg_across("사용자 브라우저", "대상 웹 앱", "POST /api/public/auth/login", 196, INK, sub="이메일 · 비밀번호")
msg_across("대상 웹 앱", "사용자 브라우저", "Set-Cookie: JSESSIONID (HttpOnly)", 234, INFO, dash="3 3", sub="세션 생성 · 쿠키 저장 (SameSite=Lax)")
seq.chip(seq.LX["사용자 브라우저"], 268, "쿠키: JSESSIONID", INFO, 11)

# ② 악성 사이트 방문 및 ③ 위조 유도
seq.line(40, 298, 920, 298, RULE, 1.0, dash="4 3")
seq.t(TITLE_X, 316, "② 악성 사이트 방문 및 ③ 위조 유도", 11, SOFT, KR, "start")
seq.msg("사용자 브라우저", "악성 사이트", "GET evil.com", 344, INK)
seq.msg("악성 사이트", "사용자 브라우저", "악성 페이지 응답 (자동 submit 폼)", 380, WARN, dash="3 3", sub="대상 앱으로 POST 를 보내는 스크립트 포함")
seq.selfmsg("사용자 브라우저", "악성 스크립트 실행", 418, WARN, sub="POST /api/admin/items 자동 제출")

# ④ 위조 요청 전송
seq.line(40, 452, 920, 452, RULE, 1.0, dash="4 3")
seq.t(TITLE_X, 470, "④ 위조 요청 전송 (쿠키 자동 첨부 여부 갈림)", 11, SOFT, KR, "start")
msg_across("사용자 브라우저", "대상 웹 앱", "POST /api/admin/items", 502, ACC, sub="SameSite=Lax 시 쿠키 제외 · 구형은 자동 첨부 (토큰 없음)")

# ⑤ 처리 결과 갈래
seq.line(40, 540, 920, 540, RULE, 1.0, dash="4 3")
seq.t(TITLE_X, 558, "⑤ 처리 결과 세 갈래 (방어 없음 · SameSite 차단 · 토큰 차단)", 11, SOFT, KR, "start")

# 갈래 A · 방어 없음
branch_label(seq.LX["악성 사이트"], 584, "갈래 A · 방어 없음 (토큰 검사 부재)", BAD)
selfmsg_left("대상 웹 앱", "쿠키만 검증", 610, BAD, sub="세션 일치로 정상 처리")
msg_across("대상 웹 앱", "사용자 브라우저", "200 OK (공격 성공 · 상태 변경)", 648, BAD, dash="3 3")

# 갈래 분리선 1
seq.line(seq.LX["악성 사이트"] - 80, 678, 920, 678, RULE, 0.8, dash="2 2")

# 갈래 B · SameSite 만 있을 때 (1겹)
branch_label(seq.LX["악성 사이트"], 702, "갈래 B · SameSite 만 있을 때 (1겹)", OK)
selfmsg_left("대상 웹 앱", "세션 쿠키 없음", 728, OK, sub="교차 사이트 POST 쿠키 미전송")
msg_across("대상 웹 앱", "사용자 브라우저", "401 Unauthorized (미인증 차단)", 766, OK, dash="3 3")

# 갈래 분리선 2
seq.line(seq.LX["악성 사이트"] - 80, 796, 920, 796, RULE, 0.8, dash="2 2")

# 갈래 C · 2겹 방어 (CsrfFilter 검증)
branch_label(seq.LX["악성 사이트"], 820, "갈래 C · 2겹 방어 (CsrfFilter 검증)", OK)
selfmsg_left("대상 웹 앱", "X-XSRF-TOKEN 검증", 846, OK, sub="헤더 누락 또는 쿠키와 불일치")
msg_across("대상 웹 앱", "사용자 브라우저", "403 Forbidden (차단 · 방어 성공)", 884, OK, dash="3 3")

# 범례
seq.legend(H - 44, [
    ("정상 인증", INFO),
    ("위조 유도", WARN),
    ("핵심 취약점(자동 전송)", ACC),
    ("공격 성공(방어 없음)", BAD),
    ("방어 성공(쿠키+헤더 토큰)", OK),
])

out_path = Path(__file__).parent.parent / "02-01.csrf-attack.svg"
seq.save(str(out_path))
print(f"생성 완료: {out_path}")

