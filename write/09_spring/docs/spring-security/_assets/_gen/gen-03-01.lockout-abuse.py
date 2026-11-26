# 사실 출처: 실패 5회 계정 잠금 정책과 서비스 거부 역이용 흐름 예시
# 타입 스펙: type-sequence
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 690
seq = Seq(
    W, H,
    "SEQUENCE · ACCOUNT LOCKOUT ABUSE",
    "동료 이메일로 다섯 번 틀려 계정을 잠그는 과정",
    "타인 계정으로 연속 5회 로그인 실패 시 계정이 잠겨 정당한 사용자도 차단되는 서비스 거부 흐름",
    "실패 5회 잠금(예), 사용자 테이블 상태 전이"
)

seq.lanes([
    ("사용자 A", "공격자 (이후 B 본인)"),
    ("로그인 API", "POST /api/public/auth/login"),
    ("B 계정", "사용자 테이블"),
], y0=104, lane_w=200)
seq.rails(562)

# 1회 실패
seq.msg("사용자 A", "로그인 API", "1회: b@example.com · 틀린 비밀번호", 176, INFO)
seq.msg("로그인 API", "B 계정", "실패 기록", 202, WARN)
seq.state("B 계정", "fail_count: 1", 226, WARN)

# 2~4회 반복 실패
seq.msg("사용자 A", "로그인 API", "2~4회: 동일 요청 반복", 262, INFO, dash="3 3")
seq.msg("로그인 API", "B 계정", "실패 누적", 288, WARN, dash="3 3")
seq.state("B 계정", "fail_count: 2 → 4", 312, WARN)

# 5회째 임계치 도달 및 잠금
seq.msg("사용자 A", "로그인 API", "5회: 틀린 비밀번호", 348, ACC)
seq.msg("로그인 API", "B 계정", "임계치 도달", 374, ACC)
seq.state("B 계정", "fail_count: 5", 398, ACC)
seq.state("B 계정", "ACTIVE → LOCKED", 426, BAD)
seq.msg("로그인 API", "사용자 A", "401 · 계정 유무와 같은 응답", 454, INFO, dash="3 3")

# 구분선 (B 본인 시도)
seq.line(40, 480, 920, 480, RULE, 1.0, dash="4 3")
seq.t(44, 498, "이후 B 본인 정상 로그인 시도", 11, SOFT, KR, "start")

# B 본인 올바른 비밀번호 시도 -> 423
seq.msg("사용자 A", "로그인 API", "B 본인: 올바른 비밀번호", 520, INFO)
seq.msg("로그인 API", "사용자 A", "423 Locked 거부", 548, BAD, dash="3 3", sub="B 본인도 못 들어감")

# 하단 칩 2개 (정책 차이 비교)
seq.chip(260, 598, "관리자만 해제 → 전 사용자 잠금 가능", BAD, 11)
seq.chip(700, 598, "시간 경과 해제 → 피해가 그 시간으로 줄어듦", OK, 11)

# 범례
seq.legend(H - 44, [
    ("임계치 도달", ACC),
    ("완화책", OK),
    ("계정 잠금·차단", BAD),
    ("실패 누적", WARN),
    ("로그인 요청", INFO),
])

out_path = Path(__file__).parent.parent / "03-01.lockout-abuse.svg"
seq.save(str(out_path))
print(f"생성 완료: {out_path}")
