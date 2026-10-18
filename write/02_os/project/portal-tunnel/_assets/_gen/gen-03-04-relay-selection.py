# 타입 스펙: type-data-flow
# 사실 출처: registry.json:1-12, portal/discovery/relay_descriptor.go:22,62,164,
#   portal/api_server.go:222, portal/discovery/relayset.go:162,255,270-284,
#   portal/discovery/mols.go:1-25,239,352,387, portal/discovery/controller.go:21,73,174,186.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 500
d = D(
    W, H,
    "PORTAL-TUNNEL · RELAY DISCOVERY & MOLS SELECTION",
    "다중 릴레이 탐색과 격자 순위화 파이프라인",
    "레지스트리와 가십으로 수집한 디스크립터의 서명을 검증하고, 탈취 방어 후 MOLS 격자로 기본 3개의 활성 릴레이를 선출합니다.",
    "후보 수집 · 서명 검증 · 탈취 방어 · MOLS 순위 · 활성 선출 · 장애 교체의 6단계 흐름"
)

# 6개 파이프라인 단계 열 정의
COLS = [
    ("1. 후보 수집", 24, 140, INFO),
    ("2. 서명 검증", 180, 140, INFO),
    ("3. 풀 관리·방어", 336, 140, WARN),
    ("4. MOLS 순위화", 492, 140, ACC),
    ("5. 활성 풀 선출", 648, 140, OK),
    ("6. 장애 피드백", 804, 132, BAD)
]

for title, x, w, color in COLS:
    d.box(x, 104, w, 28, PAPER2, RULE, 1.0)
    d.t(x + w // 2, 122, title, 11, INK, KR, "middle", 600)

Y_BOX = 144
H_BOX = 250

# 단계 1: 후보 수집
x, w = 24, 140
d.box(x, Y_BOX, w, H_BOX, PAPER2, RULE, 1.0)
d.chip(x + w // 2, Y_BOX + 24, "수집 경로", INFO, 10)
d.t(x + w // 2, Y_BOX + 62, "registry.json", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 84, "저장소 목록", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "bootstrap URLs", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 146, "시드 주소", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "/discovery/announce", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 208, "gossip 전파", 10, MUTED, KR, "middle")

# 단계 2: 서명 검증
x, w = 180, 140
d.box(x, Y_BOX, w, H_BOX, PAPER2, RULE, 1.0)
d.chip(x + w // 2, Y_BOX + 24, "암호학적 검증", INFO, 10)
d.t(x + w // 2, Y_BOX + 62, "NormalizeRelayDescriptor", 9, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 84, "포맷·길이 검사", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "VerifyRelayDescriptor", 11, OK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 146, "secp256k1 복원", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "Address 일치 확인", 11, INK, KR, "middle")
d.t(x + w // 2, Y_BOX + 208, "서명자 공개키 대조", 10, MUTED, KR, "middle")

# 단계 3: 풀 관리·방어
x, w = 336, 140
d.box(x, Y_BOX, w, H_BOX, PAPER2, WARN, 1.1)
d.chip(x + w // 2, Y_BOX + 24, "RelaySet 격리", WARN, 10)
d.t(x + w // 2, Y_BOX + 62, "IssuedAt 롤백 거절", 11, INK, KR, "middle")
d.t(x + w // 2, Y_BOX + 84, "구버전 재생 차단", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "crossIdentity 차단", 11, BAD, MONO, "middle")
d.t(x + w // 2, Y_BOX + 146, "URL 가로채기 방어", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "allowCrossIdentity", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 208, "직접 검증 시만 허용", 10, MUTED, KR, "middle")

# 단계 4: MOLS 순위화
x, w = 492, 140
d.box(x, Y_BOX, w, H_BOX, PAPER2, ACC, 1.2)
d.chip(x + w // 2, Y_BOX + 24, "격자 순위화", ACC, 10)
d.t(x + w // 2, Y_BOX + 62, "NxN 직교 라틴 방진", 11, INK, KR, "middle")
d.t(x + w // 2, Y_BOX + 84, "서로 소 승수 쌍", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "HMAC-SHA256 키 해시", 11, ACC, KR, "middle")
d.t(x + w // 2, Y_BOX + 146, "비예측적 순위 생성", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "군집 쏠림 방지", 11, INK, KR, "middle")
d.t(x + w // 2, Y_BOX + 208, "P2C 꼬리 지연 스왑", 10, MUTED, KR, "middle")

# 단계 5: 활성 풀 선출
x, w = 648, 140
d.box(x, Y_BOX, w, H_BOX, PAPER2, OK, 1.1)
d.chip(x + w // 2, Y_BOX + 24, "선출 및 유지", OK, 10)
d.t(x + w // 2, Y_BOX + 62, "SelectPriority", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 84, "명시적 릴레이 우선", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "activeStickiness", 11, OK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 146, "건강한 활성 연결 유지", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "최대 활성 릴레이 N", 11, INK, KR, "middle")
d.t(x + w // 2, Y_BOX + 208, "--max-active-relays 3", 10, MUTED, MONO, "middle")

# 단계 6: 장애 피드백
x, w = 804, 132
d.box(x, Y_BOX, w, H_BOX, PAPER2, BAD, 1.1)
d.chip(x + w // 2, Y_BOX + 24, "장애 분류", BAD, 10)
d.t(x + w // 2, Y_BOX + 62, "controller.Report", 11, INK, MONO, "middle")
d.t(x + w // 2, Y_BOX + 84, "FailureKind 전달", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 124, "FailureMITM", 11, BAD, MONO, "middle")
d.t(x + w // 2, Y_BOX + 146, "풀 영구 ban", 10, MUTED, KR, "middle")
d.t(x + w // 2, Y_BOX + 186, "FailureRuntime", 11, WARN, MONO, "middle")
d.t(x + w // 2, Y_BOX + 208, "지연 억제 및 교체", 10, MUTED, KR, "middle")

# 단계 간 순방향 화살표 (y = 268)
for i in range(5):
    x1 = COLS[i][1] + COLS[i][2]
    x2 = COLS[i+1][1]
    d.arrow([(x1 + 2, 268), (x2 - 4, 268)], MUTED, "ar", 1.2)

# 하단 역방향 실패 피드백 루프 (Stage 6 -> Stage 3/4)
Y_LOOP = 428
d.arrow([(870, Y_BOX + H_BOX), (870, Y_LOOP), (406, Y_LOOP), (406, Y_BOX + H_BOX)], BAD, "bad", 1.2, dash="4 4")
d.chip(638, Y_LOOP, "장애 보고 및 차순위 교체 루프", BAD, 10)

# 범례
d.legend(464, [
    ("수집·검증", INFO),
    ("풀 보안 격리", WARN),
    ("MOLS 격자 평가", ACC),
    ("활성 연결 유지", OK),
    ("장애 감지·차단", BAD)
])

out_path = _HERE.parent / "03-04-relay-selection.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
