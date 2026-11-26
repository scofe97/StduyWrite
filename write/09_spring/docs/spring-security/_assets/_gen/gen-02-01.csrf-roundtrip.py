# 사실 출처: Spring Security 7.1.1 CsrfConfigurer.spa() 바이트코드·CsrfFilter, axios xsrfCookieName·xsrfHeaderName
# 타입 스펙: type-sequence
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

seq = Seq(
    960, 640,
    "SEQUENCE · CSRF COOKIE TO HEADER",
    "CSRF 토큰이 쿠키에서 헤더로 돌아오는 길",
    "서버가 XSRF-TOKEN 쿠키를 내려 주고, axios가 그 값을 X-XSRF-TOKEN 헤더로 실어 보내면 서버가 둘을 비교하는 순서",
    "같은 도메인 SPA · 세션 쿠키 인증"
)

seq.lanes([
    ("브라우저", "React · axios"),
    ("보안 필터", "CsrfFilter 외"),
    ("컨트롤러", "BE"),
], y0=104, lane_w=190)
seq.rails(566)

seq.msg("브라우저", "보안 필터", "GET /api/...", 178, INK)
seq.selfmsg("보안 필터", "토큰 생성", 214, INFO, sub="CsrfCookieFilter")
seq.msg("보안 필터", "브라우저", "Set-Cookie: XSRF-TOKEN", 258, INFO, dash="3 3")
seq.selfmsg("브라우저", "쿠키 값 읽기", 298, INFO, sub="xsrfCookieName")

seq.msg("브라우저", "보안 필터", "POST + X-XSRF-TOKEN", 350, INK)
seq.selfmsg("보안 필터", "쿠키 값 = 헤더 값?", 388, WARN)
seq.msg("보안 필터", "컨트롤러", "일치: 통과", 428, OK)
seq.msg("보안 필터", "브라우저", "불일치: 403", 462, BAD, dash="3 3")

seq.line(40, 488, 920, 488, RULE, 1.0, dash="4 3")
seq.t(44, 506, "로그인 성공 뒤", 11, SOFT, KR, "start")

seq.selfmsg("보안 필터", "토큰 재발급", 530, ACC, sub="로그인 전 토큰 폐기")
seq.msg("보안 필터", "브라우저", "새 XSRF-TOKEN", 556, ACC, dash="3 3")

seq.legend(590, [
    ("쿠키 발급", INFO),
    ("비교", WARN),
    ("통과", OK),
    ("거부", BAD),
    ("재발급", ACC),
])

out_path = Path(__file__).parent.parent / "02-01.csrf-roundtrip.svg"
seq.save(str(out_path))
print(f"생성 완료: {out_path}")
