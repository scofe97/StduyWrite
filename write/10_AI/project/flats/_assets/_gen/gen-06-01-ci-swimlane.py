# 사실 출처: .github/workflows/ci.yml:16-163 · scripts/ci-test.sh:6-73
# 타입 스펙: type-swimlane
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 520
d = D(
    W, H,
    "CI PIPELINE · ci.yml",
    "Flats CI 병렬 검증 레인",
    "CI 워크플로의 작업별 실행 명령과 병렬 샤드 검증 구조",
    lead="7개 샤드 분할과 정적 분석·경합 검출·스모크를 병렬 검증합니다"
)

LANES = [
    ("npm 테스트", "docs-web"),
    ("Go 샤드 테스트", "test (matrix)"),
    ("정적·문서 검사", "test (other)"),
    ("경합 검출", "race"),
    ("린트·게이트 헬퍼", "install-script"),
    ("릴리스·스모크", "install-script"),
]

LX = 150
LW = 826
LANE_H = 58
Y0 = 100

def lane_top(k): return Y0 + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for k, (name, job) in enumerate(LANES):
    yt = lane_top(k)
    ym = lane_mid(k)
    d.line(LX, yt, LX + LW, yt, RULE, 0.8)
    d.t(14, ym - 4, name, 11, INK, KR, "start", 600)
    d.t(14, ym + 11, job, 9.5, MUTED, MONO, "start")

d.line(LX, lane_top(len(LANES)), LX + LW, lane_top(len(LANES)), RULE, 0.8)
d.line(LX, Y0, LX, lane_top(len(LANES)), RULE, 0.8)

# 레인 0: npm
y0 = lane_mid(0) - 18
d.box(166, y0, 160, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(246, y0 + 15, "npm ci", 10.5, INK, MONO, "middle", 600)
d.t(246, y0 + 28, "웹 의존성 설치", 9, MUTED, KR, "middle")

d.arrow([(326, lane_mid(0)), (356, lane_mid(0))], c=MUTED, m="ar")

d.box(360, y0, 170, 36, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(445, y0 + 15, "npm test", 10.5, INFO, MONO, "middle", 600)
d.t(445, y0 + 28, "문서 앱 테스트", 9, MUTED, KR, "middle")

# 레인 1: Go 샤드 테스트
y1 = lane_mid(1) - 18
d.box(166, y1, 160, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(246, y1 + 15, "setup-go", 10.5, INK, MONO, "middle", 600)
d.t(246, y1 + 28, "캐시 복원", 9, MUTED, KR, "middle")

d.arrow([(326, lane_mid(1)), (356, lane_mid(1))], c=MUTED, m="ar")

d.box(360, y1, 260, 36, fill=PAPER2, stroke=OK, sw=1.1, r=4)
d.t(490, y1 + 15, "ci-test.sh <shard>", 10.5, OK, MONO, "middle", 600)
d.t(490, y1 + 28, "7개 샤드 병렬 실행", 9, MUTED, KR, "middle")

d.arrow([(620, lane_mid(1)), (650, lane_mid(1))], c=MUTED, m="ar")

d.box(654, y1, 220, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(764, y1 + 15, "전체 go test 포괄", 10.5, INK, KR, "middle", 600)
d.t(764, y1 + 28, "-run / -skip 상호 배타", 9, MUTED, MONO, "middle")

# 레인 2: 정적·문서 검사 (other 샤드)
y2 = lane_mid(2) - 18
d.box(166, y2, 160, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(246, y2 + 15, "go vet ./...", 10.5, INK, MONO, "middle", 600)
d.t(246, y2 + 28, "정적 코드 분석", 9, MUTED, KR, "middle")

d.arrow([(326, lane_mid(2)), (356, lane_mid(2))], c=MUTED, m="ar")

d.box(360, y2, 170, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(445, y2 + 15, "make docs-check", 10.5, INK, MONO, "middle", 600)
d.t(445, y2 + 28, "문서 링크 검증", 9, MUTED, KR, "middle")

d.arrow([(530, lane_mid(2)), (560, lane_mid(2))], c=MUTED, m="ar")

d.box(564, y2, 190, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(659, y2 + 15, "go mod tidy", 10.5, INK, MONO, "middle", 600)
d.t(659, y2 + 28, "모듈 파일 차분 확인", 9, MUTED, KR, "middle")

# 레인 3: 경합 검출 (race)
y3 = lane_mid(3) - 18
d.box(166, y3, 240, 36, fill=PAPER2, stroke=ACC, sw=1.1, r=4)
d.t(286, y3 + 15, "go test -race 선별 패키지", 10.5, ACC, KR, "middle", 600)
d.t(286, y3 + 28, "core·api·app·mcpx·store 등", 9, MUTED, MONO, "middle")

d.arrow([(406, lane_mid(3)), (436, lane_mid(3))], c=MUTED, m="ar")

d.box(440, y3, 220, 36, fill=PAPER2, stroke=ACC, sw=1.1, r=4)
d.t(550, y3 + 15, "FILES 동시성 경합", 10.5, ACC, KR, "middle", 600)
d.t(550, y3 + 28, "TestConcurrentFiles", 9, MUTED, MONO, "middle")

d.arrow([(660, lane_mid(3)), (690, lane_mid(3))], c=MUTED, m="ar")

d.box(694, y3, 220, 36, fill=PAPER2, stroke=ACC, sw=1.1, r=4)
d.t(804, y3 + 15, "WebSocket 자원 한도", 10.5, ACC, KR, "middle", 600)
d.t(804, y3 + 28, "TestWebSocket* 경합 검출", 9, MUTED, MONO, "middle")

# 레인 4: 린트·게이트 헬퍼 (install-script Linux)
y4 = lane_mid(4) - 18
d.box(166, y4, 190, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(261, y4 + 15, "shellcheck (sh / bash)", 10, INK, MONO, "middle", 600)
d.t(261, y4 + 28, "스크립트 정적 린트", 9, MUTED, KR, "middle")

d.arrow([(356, lane_mid(4)), (386, lane_mid(4))], c=MUTED, m="ar")

d.box(390, y4, 210, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(495, y4 + 15, "bash -n 게이트 구문", 10, INK, KR, "middle", 600)
d.t(495, y4 + 28, "구문 오류 사전 차단", 9, MUTED, KR, "middle")

d.arrow([(600, lane_mid(4)), (630, lane_mid(4))], c=MUTED, m="ar")

d.box(634, y4, 240, 36, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(754, y4 + 15, "test_approval_gate.py", 10, INFO, MONO, "middle", 600)
d.t(754, y4 + 28, "가짜 클라이언트 승인 계약", 9, MUTED, KR, "middle")

# 레인 5: 릴리스·스모크 (install-script macOS/Linux)
y5 = lane_mid(5) - 18
d.box(166, y5, 230, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(281, y5 + 15, "build-release.sh", 10, INK, MONO, "middle", 600)
d.t(281, y5 + 28, "플랫폼별 릴리스 아카이브", 9, MUTED, KR, "middle")

d.arrow([(396, lane_mid(5)), (426, lane_mid(5))], c=MUTED, m="ar")

d.box(430, y5, 260, 36, fill=PAPER2, stroke=OK, sw=1.2, r=4)
d.t(560, y5 + 15, "install-smoke.sh", 10.5, OK, MONO, "middle", 600)
d.t(560, y5 + 28, "설치·재실행·복구·삭제 검증", 9, MUTED, KR, "middle")

d.arrow([(690, lane_mid(5)), (720, lane_mid(5))], c=MUTED, m="ar")

d.box(724, y5, 220, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=4)
d.t(834, y5 + 15, "launchd / systemd 검증", 10.5, INK, KR, "middle", 600)
d.t(834, y5 + 28, "실제 서비스 라이프사이클", 9, MUTED, KR, "middle")

d.legend(H - 46, [
    ("샤드 분할 테스트", OK),
    ("동시성 경합 검출", ACC),
    ("정적 검증 및 린트", INFO),
    ("실제 릴리스 스모크", MUTED),
])

out_path = _HERE.parent / "06-01-ci-swimlane.svg"
d.save(str(out_path))
print(f"saved {out_path}")
