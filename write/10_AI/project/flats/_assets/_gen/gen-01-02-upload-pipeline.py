# 타입 스펙: type-process
# 사실 출처: internal/cli/pack.go:45-126, internal/api/api.go:118,414-440, internal/bundle/bundle.go:46-540,671, docs/design.md 「Manifest」
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "PROCESS · UPLOAD PIPELINE",
    "클라이언트 패키징부터 초안 리비전 확정까지의 검증 파이프라인",
    "클라이언트와 서버가 중복 검증을 수행해 심볼릭 링크·압축 폭탄·루트 탈출을 단계별로 차단합니다",
    "CLI packDir ── HTTP POST ──> bundle.FromArchive ──> ParseManifest ──> os.Root 쓰기 ──> Draft 확정"
)

# 4개 처리 구역 (Process Stages)
COL_W = 184
GAP = 56
C1_X = 28
C2_X = C1_X + COL_W + GAP  # 268
C3_X = C2_X + COL_W + GAP  # 508
C4_X = C3_X + COL_W + GAP  # 748

stages = [
    (C1_X, "1. 클라이언트 패키징", "pack.go · packDir"),
    (C2_X, "2. 전송 및 압축 해제", "bundle.go · FromArchive"),
    (C3_X, "3. 규약 및 매니페스트 검증", "ParseManifest · checkHealth"),
    (C4_X, "4. 격리 쓰기 및 확정", "writeBundleFiles · Draft")
]

for x, title, sub in stages:
    d.box(x, 104, COL_W, 44, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(x + COL_W / 2, 124, title, 12, INK, KR, "middle", 600)
    d.t(x + COL_W / 2, 139, sub, 10, MUTED, MONO, "middle")

# 1열: 클라이언트 패키징
d.box(C1_X, 164, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C1_X + 14, 186, "디렉터리 순회 및 필터", 12, INK, KR, "start", 600)
d.t(C1_X + 14, 206, "os.OpenRoot · fs.WalkDir", 10, INFO, MONO, "start")
d.t(C1_X + 14, 222, "skip: .git · node_modules", 10, MUTED, MONO, "start")

d.arrow([(C1_X + COL_W / 2, 236), (C1_X + COL_W / 2, 248)], c=MUTED, m="ar", sw=1.2)

d.tone(C1_X, 248, COL_W, 72, BAD, 6, "14", 1.1)
d.t(C1_X + 14, 270, "위험 파일 즉시 거부", 12, BAD, KR, "start", 600)
d.t(C1_X + 14, 290, "ModeSymlink 링크 차단", 10, INK, MONO, "start")
d.t(C1_X + 14, 306, "소켓·디바이스 특수 파일 거부", 9, MUTED, KR, "start")

d.arrow([(C1_X + COL_W / 2, 320), (C1_X + COL_W / 2, 332)], c=MUTED, m="ar", sw=1.2)

d.box(C1_X, 332, COL_W, 72, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(C1_X + 14, 354, "인메모리 tar.gz 압축", 12, INFO, KR, "start", 600)
d.t(C1_X + 14, 374, "FormatPAX 정규 스트림", 10, MUTED, MONO, "start")
d.t(C1_X + 14, 390, "POST /api/flats/{slug}/draft", 8.5, INFO, MONO, "start")

# 1열 -> 2열 직각 화살표 및 전송 칩 (GAP = 56px, mid = 240)
mid1 = C1_X + COL_W + GAP / 2
d.arrow([(C1_X + COL_W, 368), (mid1, 368), (mid1, 200), (C2_X, 200)], c=INFO, m="info", sw=1.4)
d.chip(mid1, 284, "tar.gz", c=INFO, size=10)

# 2열: 서버 아카이브 해제 & 제한
d.box(C2_X, 164, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C2_X + 14, 186, "용량 상한 검사", 12, INK, KR, "start", 600)
d.t(C2_X + 14, 206, "upload_max_bytes: 20 MiB", 9.5, INFO, MONO, "start")
d.t(C2_X + 14, 222, "MaxFiles: 최대 20 000 개", 10, MUTED, MONO, "start")

d.arrow([(C2_X + COL_W / 2, 236), (C2_X + COL_W / 2, 248)], c=MUTED, m="ar", sw=1.2)

d.tone(C2_X, 248, COL_W, 72, WARN, 6, "14", 1.1)
d.t(C2_X + 14, 270, "압축 폭탄 방어", 12, WARN, KR, "start", 600)
d.t(C2_X + 14, 290, "maxTarEntries: 60 000", 10, INK, MONO, "start")
d.t(C2_X + 14, 306, "해제 예산: 용량 + 235 MiB", 10, MUTED, KR, "start")

d.arrow([(C2_X + COL_W / 2, 320), (C2_X + COL_W / 2, 332)], c=MUTED, m="ar", sw=1.2)

d.box(C2_X, 332, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C2_X + 14, 354, "경로 정규화 및 스트리핑", 12, INK, KR, "start", 600)
d.t(C2_X + 14, 374, "cleanPath: 루트 탈출 거부", 10, MUTED, MONO, "start")
d.t(C2_X + 14, 390, "stripCommonRoot: dist/ 제거", 9.5, INFO, MONO, "start")

# 2열 -> 3열 직각 화살표 및 파일 목록 칩 (GAP = 56px, mid = 480)
mid2 = C2_X + COL_W + GAP / 2
d.arrow([(C2_X + COL_W, 368), (mid2, 368), (mid2, 200), (C3_X, 200)], c=MUTED, m="ar", sw=1.4)
d.chip(mid2, 284, "files", c=MUTED, size=10)

# 3열: 규약 및 매니페스트 검증
d.box(C3_X, 164, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C3_X + 14, 186, "매니페스트 디코딩", 12, INK, KR, "start", 600)
d.t(C3_X + 14, 206, "flats.json 필드 파싱", 10, INFO, MONO, "start")
d.t(C3_X + 14, 222, "미등록 필드 에러 거부", 10, MUTED, KR, "start")

d.arrow([(C3_X + COL_W / 2, 236), (C3_X + COL_W / 2, 248)], c=MUTED, m="ar", sw=1.2)

d.box(C3_X, 248, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C3_X + 14, 270, "유형 및 기본값 결정", 12, INK, KR, "start", 600)
d.t(C3_X + 14, 290, "type: flat · docs · page", 10, INK, MONO, "start")
d.t(C3_X + 14, 306, "kind: static 기본값 적용", 9.5, MUTED, KR, "start")

d.arrow([(C3_X + COL_W / 2, 320), (C3_X + COL_W / 2, 332)], c=MUTED, m="ar", sw=1.2)

d.box(C3_X, 332, COL_W, 72, fill=PAPER2, stroke=INFO, sw=0.9)
d.t(C3_X + 14, 354, "진입점 및 헬스 검증", 12, INFO, KR, "start", 600)
d.t(C3_X + 14, 374, "entry · index.html 존재 확인", 9.5, MUTED, KR, "start")
d.t(C3_X + 14, 390, "checkHealth: / 절대경로 검사", 9.5, INFO, MONO, "start")

# 3열 -> 4열 직각 화살표 및 검증 통과 칩 (GAP = 56px, mid = 720)
mid3 = C3_X + COL_W + GAP / 2
d.arrow([(C3_X + COL_W, 368), (mid3, 368), (mid3, 200), (C4_X, 200)], c=OK, m="ok", sw=1.4)
d.chip(mid3, 284, "valid", c=OK, size=10)

# 4열: 디스크 쓰기 및 초안 확정
d.tone(C4_X, 164, COL_W, 72, OK, 6, "14", 1.1)
d.t(C4_X + 14, 186, "Go 1.24 os.Root 격리", 12, OK, KR, "start", 600)
d.t(C4_X + 14, 206, "임시 스테이징 디렉터리", 10, INK, MONO, "start")
d.t(C4_X + 14, 222, "심볼릭 레이스 탈출 차단", 10, MUTED, KR, "start")

d.arrow([(C4_X + COL_W / 2, 236), (C4_X + COL_W / 2, 248)], c=MUTED, m="ar", sw=1.2)

d.box(C4_X, 248, COL_W, 72, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C4_X + 14, 270, "원자적 디렉터리 교체", 12, INK, KR, "start", 600)
d.t(C4_X + 14, 290, "os.Rename(tmp, dst)", 10, INFO, MONO, "start")
d.t(C4_X + 14, 306, "bundle.Hash 지문 산출", 10, MUTED, MONO, "start")

d.arrow([(C4_X + COL_W / 2, 320), (C4_X + COL_W / 2, 332)], c=MUTED, m="ar", sw=1.2)

d.tone(C4_X, 332, COL_W, 72, ACC, 6, "14", 1.2)
d.t(C4_X + 14, 354, "초안 확정 (Draft revision)", 12, ACC, KR, "start", 600)
d.t(C4_X + 14, 374, "flats.db 메타데이터 저장", 10, INK, MONO, "start")
d.t(C4_X + 14, 390, "HTTP 201 Created 반환", 10, MUTED, MONO, "start")

# 바닥 검증 에러 힌트 박스
d.box(28, 424, C4_X + COL_W - 28, 52, fill=PAPER2, stroke=OK, sw=1.0)
d.t(44, 446, "모든 검증 오류에 fix 힌트 제공 (ValidationError)", 11, OK, KR, "start", 600)
d.t(44, 464, "예: path escapes the bundle root or is absolute (fix: use relative paths inside the build directory)", 9.5, MUTED, MONO, "start")

out_path = Path(__file__).parent.parent / "01-02-upload-pipeline.svg"
d.save(str(out_path))
print(f"Generated: {out_path}")
