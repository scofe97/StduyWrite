# 사실 출처: internal/core/document.go:207, docs/content-types.md 「Edit live text」, docs/internal/docs-app.md
# 타입 스펙: type-data-flow
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "DOCUMENTS · LIVE EDIT & REVISION FLOW",
    "에이전트 저장과 브라우저 편집이 실시간 합쳐지는 데이터 흐름",
    "save_document 와 사람 브라우저 편집이 문서 워커에서 병합되어 새 리비전으로 영속화되는 파이프라인",
    "승인 없이 live 에 즉시 서빙되며 덮어쓴 편집분은 직전 닫힌 person 리비전에 보존"
)

# 4개 단계 열 (Column X 좌표)
COL_W = 190
C1_X = 24
C2_X = 264
C3_X = 504
C4_X = 744

headers = [
    (C1_X, "1. 동시 편집 요청", "에이전트 및 브라우저"),
    (C2_X, "2. 문서 워커 병합", "runtime/docs/…/server.js"),
    (C3_X, "3. 리비전 스토어 기록", "outbox → importDocsLocked"),
    (C4_X, "4. 라이브 즉시 반영", "포트 :7879 즉시 서빙")
]

for x, title, sub in headers:
    d.t(x + COL_W / 2, 114, title, 12, INK, KR, "middle", 600)
    d.t(x + COL_W / 2, 132, sub, 10, MUTED, MONO, "middle")

# 1열: 요청원 2개 (에이전트 vs 사람)
# 상단: 에이전트 save_document
d.box(C1_X, 160, COL_W, 90, fill=PAPER2, stroke=INFO, sw=1.2)
d.t(C1_X + 16, 184, "에이전트 도구 호출", 11, INFO, KR, "start", 600)
d.t(C1_X + 16, 204, "save_document", 12, INK, MONO, "start", 600)
d.t(C1_X + 16, 222, "Markdown 파일 저장", 10, MUTED, KR, "start")
d.t(C1_X + 16, 238, "path · markdown 전달", 9, SOFT, MONO, "start")

# 하단: 사람 브라우저 편집
d.box(C1_X, 290, COL_W, 90, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(C1_X + 16, 314, "사람 브라우저 편집", 11, ACC, KR, "start", 600)
d.t(C1_X + 16, 334, "Private 웹 편집기", 12, INK, KR, "start", 600)
d.t(C1_X + 16, 352, "실시간 키 입력 스트림", 10, MUTED, KR, "start")
d.t(C1_X + 16, 368, "30초 유휴/5분 그룹화", 9, SOFT, KR, "start")

# 화살표 1 -> 2
d.arrow([(C1_X + COL_W, 205), (C2_X, 205)], c=INFO, m="info")
d.arrow([(C1_X + COL_W, 335), (C2_X, 335)], c=ACC, m="acc")

# 2열: 워커 내부 처리 (병합 및 보존)
d.box(C2_X, 160, COL_W, 220, fill=PAPER2, stroke=RULE, sw=1.2)
d.t(C2_X + COL_W / 2, 186, "워커 런타임 처리", 12, INK, KR, "middle", 600)
d.line(C2_X + 12, 198, C2_X + COL_W - 12, 198, RULE, 0.8)

# 워커 내부 상자 1: 라인 단위 병합
d.box(C2_X + 10, 210, COL_W - 20, 64, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(C2_X + 18, 230, "라인 단위 자동 병합", 11, OK, KR, "start", 600)
d.t(C2_X + 18, 248, "비충돌 행: 양쪽 보존", 10, MUTED, KR, "start")
d.t(C2_X + 18, 262, "충돌 행: 새 저장 우선", 10, MUTED, KR, "start")

# 워커 내부 상자 2: 덮어쓴 글 보존 위치
d.box(C2_X + 10, 286, COL_W - 20, 80, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(C2_X + 18, 306, "덮어쓴 글 보존 위치", 11, WARN, KR, "start", 600)
d.t(C2_X + 18, 324, "직전 닫힌 person 리비전", 10, INK, KR, "start")
d.t(C2_X + 18, 340, "저장 직전 미완료 그룹 강제 확정", 9, MUTED, KR, "start")
d.t(C2_X + 18, 354, "핀 안 하면 쿼터 내 보존", 9, OK, KR, "start")

# 화살표 2 -> 3
d.arrow([(C2_X + COL_W, 242), (C3_X, 242)], c=RULE, m="ar")

# 3열: 리비전 스토어 (SQLite + Blobs)
d.box(C3_X, 160, COL_W, 220, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(C3_X + COL_W / 2, 186, "리비전 스토어 영속화", 12, ACC, KR, "middle", 600)
d.line(C3_X + 12, 198, C3_X + COL_W - 12, 198, RULE, 0.8)

# 3열 내부: 새 리비전 생성
d.box(C3_X + 10, 210, COL_W - 20, 72, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(C3_X + 18, 230, "새 리비전 N+1 커밋", 11, INFO, KR, "start", 600)
d.t(C3_X + 18, 248, "table: revisions", 10, INK, MONO, "start")
d.t(C3_X + 18, 264, "kind: agent / person", 10, MUTED, MONO, "start")

# 3열 내부: 불변 Blob 저장
d.box(C3_X + 10, 294, COL_W - 20, 72, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.t(C3_X + 18, 314, "불변 블롭 (SHA-256)", 11, INK, KR, "start", 600)
d.t(C3_X + 18, 332, "revisions/blobs/<hh>/…", 10, MUTED, MONO, "start")
d.t(C3_X + 18, 350, "모드 0444 읽기 전용", 9, SOFT, KR, "start")

# 화살표 3 -> 4
d.arrow([(C3_X + COL_W, 246), (C4_X, 246)], c=OK, m="ok")

# 4열: 라이브 즉시 반영 (No approval, No draft)
d.box(C4_X, 180, COL_W, 180, fill=PAPER2, stroke=OK, sw=1.4)
d.t(C4_X + COL_W / 2, 210, "라이브 즉시 서빙", 12, OK, KR, "middle", 600)
d.line(C4_X + 12, 222, C4_X + COL_W - 12, 222, RULE, 0.8)

d.box(C4_X + 10, 234, COL_W - 20, 48, fill=PAPER, stroke=OK, sw=0.8, r=4)
d.t(C4_X + COL_W / 2, 252, "HTTP 200 OK", 11, OK, MONO, "middle", 600)
d.t(C4_X + COL_W / 2, 268, "포트 127.0.0.1:7879", 10, MUTED, MONO, "middle")

d.t(C4_X + COL_W / 2, 302, "Draft / Version 없음", 10, INK, KR, "middle")
d.t(C4_X + COL_W / 2, 320, "배포 승인 절차 없음", 10, INK, KR, "middle")
d.t(C4_X + COL_W / 2, 338, "Public 시 즉시 노출", 9, WARN, KR, "middle")

# 하단 범례
d.legend(456, [
    ("에이전트 입력", INFO),
    ("사람 편집 입력", ACC),
    ("충돌 보존 리비전", WARN),
    ("라이브 즉시 반영", OK)
])

out_path = _HERE.parent / "01-04-doc-save-flow.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
