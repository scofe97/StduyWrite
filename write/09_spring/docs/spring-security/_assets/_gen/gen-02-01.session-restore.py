# 사실 출처: Spring Security 7.1.1 SecurityContextHolderFilter·HttpSessionSecurityContextRepository
# 타입 스펙: type-sequence
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

seq = Seq(
    960, 600,
    "SEQUENCE · SESSION RESTORE",
    "로그인 뒤 요청이 인증을 되찾는 과정",
    "로그인 컨트롤러가 인증 정보를 세션에 저장하고, 다음 요청에서 보안 필터가 세션 쿠키로 그 인증 정보를 다시 꺼내는 순서",
    "예제 앱 기준"
)

seq.lanes([
    ("브라우저", "React"),
    ("보안 필터", "SecurityContextHolderFilter"),
    ("세션", "HttpSession"),
    ("컨트롤러", "BE"),
], y0=104, lane_w=200)
seq.rails(526)

seq.msg("브라우저", "컨트롤러", "POST /api/public/auth/login", 176, INK)
seq.selfmsg("컨트롤러", "", 212, WARN)
seq.t(seq.LX["컨트롤러"] - 14, 216, "비밀번호 비교", 11, WARN, MONO, "end")
seq.msg("컨트롤러", "세션", "saveContext", 250, ACC)
seq.msg("컨트롤러", "브라우저", "Set-Cookie: 세션 ID", 284, INFO, dash="3 3")

seq.line(40, 308, 920, 308, RULE, 1.0, dash="4 3")
seq.t(44, 326, "다음 요청부터", 11, SOFT, KR, "start")

seq.msg("브라우저", "보안 필터", "GET /api/my/account", 360, INK)
seq.msg("보안 필터", "세션", "세션 ID로 조회", 394, INFO)
seq.msg("세션", "보안 필터", "SecurityContext", 428, INFO, dash="3 3")
seq.selfmsg("보안 필터", "인증 정보 복원", 464, OK)
seq.msg("보안 필터", "컨트롤러", "", 506, OK)
seq.t((seq.LX["세션"] + seq.LX["컨트롤러"]) / 2, 497, "인가 통과", 11, OK, MONO, "middle", 600)

seq.legend(548, [
    ("세션에 저장", ACC),
    ("조회", INFO),
    ("복원·통과", OK),
    ("비교", WARN),
])

out_path = Path(__file__).parent.parent / "02-01.session-restore.svg"
seq.save(str(out_path))
print(f"생성 완료: {out_path}")
