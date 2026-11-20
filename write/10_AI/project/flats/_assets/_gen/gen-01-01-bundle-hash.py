# 타입 스펙: type-data-flow
# 사실 출처: internal/bundle/bundle.go:695-701, docs/design.md 「Model and flows」
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "BUNDLE · CONTENT-ADDRESSABLE DIGEST FLOW",
    "파일 묶음에서 버전 해시를 만드는 결정적 파이프라인",
    "개별 파일 해시 계산, 경로 정렬, NUL 구분 결합을 거쳐 단일 버전 해시를 도출하는 데이터 흐름",
    "경로 정렬과 NUL 바이트 구분자로 경계 모호성을 제거하고 동일 내용에 동일 해시를 보장"
)

# 4개 단계 열 (Column X 좌표)
COL_W = 190
C1_X = 24
C2_X = 264
C3_X = 504
C4_X = 744

# 열 헤더
headers = [
    (C1_X, "1. 원본 파일 집합", "임의 순서의 파일 입력"),
    (C2_X, "2. 개별 SHA-256", "sha256.Sum256(data)"),
    (C3_X, "3. 경로 정렬·포맷 결합", "path\\0hex\\n 스트림"),
    (C4_X, "4. 최종 버전 해시", "전체 스트림 SHA-256")
]

for x, title, sub in headers:
    d.t(x + COL_W / 2, 114, title, 12, INK, KR, "middle", 600)
    d.t(x + COL_W / 2, 132, sub, 10, MUTED, MONO, "middle")

# 3개 파일 정보
files = [
    ("flats.json", "18 B", "708d5f3a", 160),
    ("index.html", "30 B", "73899980", 244),
    ("server.js", "52 B", "73fd85bf", 328)
]

for name, size, hval, y in files:
    # 1열: 원본 파일 상자
    d.box(C1_X, y, COL_W, 56, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(C1_X + 16, y + 24, name, 12, INK, MONO, "start", 600)
    d.t(C1_X + 16, y + 42, f"크기: {size}", 10, MUTED, KR, "start")

    # 화살표 1 -> 2
    d.arrow([(C1_X + COL_W, y + 28), (C2_X, y + 28)], c=INFO, m="info")

    # 2열: 개별 SHA-256 해시
    d.box(C2_X, y, COL_W, 56, fill=PAPER2, stroke=INFO, sw=1.0)
    d.t(C2_X + 16, y + 24, f"{hval}…", 11, INFO, MONO, "start", 600)
    d.t(C2_X + 16, y + 42, "32바이트 (16진수 64자)", 10, MUTED, KR, "start")

    # 화살표 2 -> 3
    d.arrow([(C2_X + COL_W, y + 28), (C3_X, y + 28)], c=RULE, m="ar")

# 3열: 정렬 및 포맷팅 결합 상자 (하나의 스트림 블록)
d.box(C3_X, 160, COL_W, 224, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(C3_X + COL_W / 2, 186, "경로 오름차순 정렬", 11, ACC, KR, "middle", 600)
d.line(C3_X + 12, 198, C3_X + COL_W - 12, 198, RULE, 0.8)

# 스트림 줄 3개
stream_lines = [
    ("flats.json", "708d5f3a", 226),
    ("index.html", "73899980", 276),
    ("server.js", "73fd85bf", 326)
]
for p, hv, ly in stream_lines:
    d.box(C3_X + 10, ly - 14, COL_W - 20, 36, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.t(C3_X + 18, ly + 2, f"{p}", 10, INK, MONO, "start", 600)
    d.t(C3_X + 18, ly + 16, f"\\0 {hv}… \\n", 9, MUTED, MONO, "start")

d.t(C3_X + COL_W / 2, 368, "총 227바이트 바이트열", 10, MUTED, KR, "middle")

# 화살표 3 -> 4
d.arrow([(C3_X + COL_W, 272), (C4_X, 272)], c=ACC, m="acc")

# 4열: 최종 버전 해시
d.box(C4_X, 216, COL_W, 112, fill=PAPER2, stroke=OK, sw=1.4)
d.t(C4_X + COL_W / 2, 246, "버전 해시 (vN)", 12, OK, KR, "middle", 600)
d.box(C4_X + 14, 258, COL_W - 28, 30, fill=PAPER, stroke=OK, sw=0.8, r=4)
d.t(C4_X + COL_W / 2, 278, "45545980…", 12, OK, MONO, "middle", 600)
d.t(C4_X + COL_W / 2, 310, "불변 버전 식별자", 10, MUTED, KR, "middle")

# 범례
d.legend(456, [
    ("원본 입력 파일", RULE),
    ("개별 바이트 SHA-256", INFO),
    ("정렬 스트림 (NUL 구분)", ACC),
    ("최종 버전 다이제스트", OK)
])

out_path = _HERE.parent / "01-01-bundle-hash.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
