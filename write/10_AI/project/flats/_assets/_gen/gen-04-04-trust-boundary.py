# 사실 출처: docs/design.md 「Approvals」 Enforced·Not enforced · docs/surfaces.md 「Request guards」 · internal/api/guard.go:15-41,122-171
# 타입 스펙: type-nested
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 10

class DNested(D):
    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 60
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 22, y + 22, lab, 11, MUTED, KR, "start")
            x += 32 + int(_w(lab, 11))

W, H = 1000, 560
d = DNested(
    W, H,
    "TRUST BOUNDARY · SECURITY MODEL",
    "flats 신뢰 경계와 권한 격리 구조",
    "운영자 OS 권한 범위와 외부 에이전트·웹페이지 간 방어 경계 및 잔여 한계",
    lead="계정 없는 아키텍처의 요청 출처와 헤더 기반 방어선입니다"
)

# 좌측 대형 컨테이너: 운영자 OS 권한 범위 (Host Scope)
d.box(40, 100, 480, 370, fill=PAPER2, stroke=WARN, sw=1.4, r=10)
d.t(60, 126, "운영자 OS 권한 범위 (Host Scope)", 13, WARN, KR, "start", 600)
d.t(60, 146, "데이터 폴더 접근 · secret.key 열람 · 임의 HTTP 전송 가능", 10, SOFT, KR, "start")

# 호스트 프로세스 설명 박스
d.box(60, 165, 440, 75, fill=PAPER, stroke=RULE, sw=1.0, r=6)
d.t(80, 190, "로컬 프로세스 (Not Enforced)", 11, BAD, KR, "start", 600)
d.t(80, 210, "콘솔 헤더 흉내 가능 · flats.db 직접 열람", 10, MUTED, KR, "start")
d.t(80, 226, "별도 계정/MFA 없음 → 사람 승인 입증 불가", 10, SOFT, KR, "start")

# 내포된 안쪽 상자: 브라우저 콘솔 페이지 (Enforced)
d.box(60, 260, 440, 185, fill=PAPER, stroke=OK, sw=1.4, r=8)
d.t(80, 288, "브라우저 콘솔 페이지 (Web Console Scope)", 12, OK, KR, "start", 600)
d.t(80, 310, "동일 출처 제약 (Same-Origin) 강제", 10, INK, KR, "start")

# 콘솔 세부 조건 칩
d.box(80, 330, 400, 95, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(96, 352, "경로: /console/api/approvals/{id}/approve", 10, INFO, MONO, "start")
d.t(96, 372, "헤더: X-Flats-Console: 1", 10, OK, MONO, "start")
d.t(96, 392, "메타: Sec-Fetch-Site: same-origin", 10, OK, MONO, "start")
d.t(96, 412, "감사: decided_by (WhoIs 로그인 / 콘솔)", 10, SOFT, KR, "start")


# 우측 영역: 경계 밖 신뢰 주체들 (External / Outside Scope)

# 1. 다른 사이트 웹페이지 (완전 차단)
d.box(560, 100, 400, 105, fill=PAPER2, stroke=BAD, sw=1.2, r=8)
d.t(580, 126, "다른 사이트 웹페이지 (외부 출처)", 12, BAD, KR, "start", 600)
d.t(580, 148, "HostGuard: DNS Rebinding 차단", 10, INK, KR, "start")
d.t(580, 168, "CSRF 가드: 교차 출처 거절", 10, MUTED, KR, "start")
d.t(580, 188, "403 Forbidden · 콘솔 접근 불가", 10, BAD, KR, "start")

# 2. 에이전트 (MCP · CLI · /api) - 요청만 허용
d.box(560, 225, 400, 115, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(580, 251, "에이전트 (MCP · CLI · /api)", 12, INFO, KR, "start", 600)
d.t(580, 273, "승인/거절 엔드포인트 미노출", 10, INK, KR, "start")
d.t(580, 293, "consoleRequest: X-Flats-Client 거절", 10, MUTED, KR, "start")
d.t(580, 313, "요청(pending)만 생성 · 결정 권한 없음", 10, INFO, KR, "start")

# 3. 권장 완화책: 격리된 에이전트
d.box(560, 360, 400, 110, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(580, 386, "권장 완화책: 격리된 에이전트", 12, OK, KR, "start", 600)
d.t(580, 408, "다른 OS 계정 또는 다른 기계 배치", 10, INK, KR, "start")
d.t(580, 428, "Tailnet ACL: MCP·/api 만 허용", 10, MUTED, KR, "start")
d.t(580, 448, "데이터 폴더 접근 및 콘솔 흉내 차단", 10, OK, KR, "start")


# 범례
d.legend(490, [
    ("운영자 OS 권한 (미격리 범위)", WARN),
    ("강제된 보호 경계 (Enforced)", OK),
    ("외부 위협 차단 (Blocked)", BAD),
    ("제한된 에이전트 표면 (Request Only)", INFO)
])

d.save(str(_HERE.parent / "04-04-trust-boundary.svg"))
print("ok 04-04-trust-boundary.svg")
