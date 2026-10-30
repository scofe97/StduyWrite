# 04-04 §2 — 인덱스 리프에 실제 행 전체를 저장하는 clustered, 힙 파일 참조만 두는 heap 방식, 일부 컬럼을 포함하는 covering 인덱스의 구조 비교.
# 사실 출처: 04-04 본문 §2(L49~L59), DDIA 2판 Ch.4 "Storing Values Within the Index"(원서 PDF 20쪽). 예시 값(id 42·Alice·Seoul·Page 5)은 본문·원서에 없어 2026-10-30 검증에서 걷어냄
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 96
PH = 308
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-04 · INDEX VALUE STORAGE", "인덱스에 값을 두는 세 가지 방식",
      "실제 행 전체를 인덱스 리프에 저장하는 clustered, 힙 파일의 위치 참조만 두는 heap 방식, 일부 컬럼을 포함하는 covering 인덱스의 저장 구조 비교.",
      "clustered(행 직접 저장) · heap file(위치 참조) · covering(일부 컬럼 포함)")

CW = 264
GAP = 16
X0 = 24

# 1. clustered index (InnoDB)
x1 = X0
d.box(x1, PY, CW, PH, PAPER2, OK, 1.2)
d.chip(x1 + CW / 2, PY + 22, "1. clustered index", OK, 12)
d.t(x1 + CW / 2, PY + 46, "MySQL InnoDB 테이블 기본키", 12, SOFT, KR, "middle")
d.line(x1 + 14, PY + 58, x1 + CW - 14, PY + 58, RULE, 0.8)

# 리프 노드
d.box(x1 + 14, PY + 70, CW - 28, 86, PAPER, OK, 1.0)
d.t(x1 + CW / 2, PY + 90, "인덱스 리프 노드 (B-tree)", 12, OK, KR, "middle", 600)
d.t(x1 + 26, PY + 112, "Key:", 12, MUTED, KR, "start")
d.t(x1 + 68, PY + 112, "기본키", 12, INK, KR, "start", 600)
d.t(x1 + 26, PY + 134, "Data:", 12, MUTED, KR, "start")
d.t(x1 + 68, PY + 134, "행 전체 (모든 컬럼)", 12, OK, KR, "start", 600)

d.arrow([(x1 + 32, PY + 162), (x1 + 32, PY + 188)], OK, "ok", 1.4)
d.t(x1 + 46, PY + 179, "행·문서·정점을 직접 저장", 12, OK, KR, "start")

# 설명 상자
d.box(x1 + 14, PY + 196, CW - 28, 96, PAPER, RULE, 0.8)
d.t(x1 + CW / 2, PY + 218, "실제 행 전체를 인덱스에 저장", 12, INK, KR, "middle", 600)
d.t(x1 + CW / 2, PY + 238, "heap 조회 없이 값 읽음", 12, OK, KR, "middle")
d.t(x1 + CW / 2, PY + 258, "InnoDB 보조 인덱스는 기본키 참조", 12, MUTED, KR, "middle")
d.t(x1 + CW / 2, PY + 276, "SQL Server 는 테이블당 하나 지정", 12, MUTED, KR, "middle")


# 2. nonclustered / heap file (PostgreSQL)
x2 = X0 + CW + GAP
d.box(x2, PY, CW, PH, PAPER2, INFO, 1.2)
d.chip(x2 + CW / 2, PY + 22, "2. heap file 참조", INFO, 12)
d.t(x2 + CW / 2, PY + 46, "Postgres 가 쓰는 방식", 12, SOFT, KR, "middle")
d.line(x2 + 14, PY + 58, x2 + CW - 14, PY + 58, RULE, 0.8)

# 리프 노드
d.box(x2 + 14, PY + 70, CW - 28, 70, PAPER, INFO, 1.0)
d.t(x2 + CW / 2, PY + 88, "인덱스 리프 노드 (참조 저장)", 12, INFO, KR, "middle", 600)
d.t(x2 + 26, PY + 108, "Key:", 12, MUTED, KR, "start")
d.t(x2 + 68, PY + 108, "인덱싱된 키", 12, INK, KR, "start", 600)
d.t(x2 + 26, PY + 126, "Ref:", 12, MUTED, KR, "start")
d.t(x2 + 68, PY + 126, "디스크 위치", 12, INFO, KR, "start", 600)

d.arrow([(x2 + 32, PY + 146), (x2 + 32, PY + 168)], INFO, "info", 1.4)
d.t(x2 + 46, PY + 161, "디스크 위치를 직접 참조", 12, INFO, KR, "start")

# 힙 파일 상자
d.box(x2 + 14, PY + 174, CW - 28, 54, PAPER, RULE, 0.9)
d.t(x2 + CW / 2, PY + 192, "heap file (순서 없는 행 저장)", 12, MUTED, KR, "middle")
d.t(x2 + CW / 2, PY + 212, "append-only · 삭제 자리 재사용", 12, INK, KR, "middle")

# 갱신 특징
d.box(x2 + 14, PY + 236, CW - 28, 56, PAPER, RULE, 0.8)
d.t(x2 + CW / 2, PY + 256, "제자리 덮어쓰기 (크기 유지 시)", 12, OK, KR, "middle")
d.t(x2 + CW / 2, PY + 276, "위치 이동 시 forwarding pointer", 12, WARN, KR, "middle")


# 3. covering index (Index with Included Columns)
x3 = X0 + 2 * (CW + GAP)
d.box(x3, PY, CW, PH, PAPER2, ACC, 1.2)
d.chip(x3 + CW / 2, PY + 22, "3. covering index", ACC, 12)
d.t(x3 + CW / 2, PY + 46, "일부 컬럼을 인덱스에 포함", 12, SOFT, KR, "middle")
d.line(x3 + 14, PY + 58, x3 + CW - 14, PY + 58, RULE, 0.8)

# 리프 노드
d.box(x3 + 14, PY + 70, CW - 28, 86, PAPER, ACC, 1.0)
d.t(x3 + CW / 2, PY + 90, "인덱스 리프 (included columns)", 12, ACC, KR, "middle", 600)
d.t(x3 + 26, PY + 110, "Key:", 12, MUTED, KR, "start")
d.t(x3 + 68, PY + 110, "인덱싱 컬럼", 12, INK, KR, "start", 600)
d.t(x3 + 26, PY + 128, "Include:", 12, MUTED, KR, "start")
d.t(x3 + 86, PY + 128, "포함한 일부 컬럼", 12, ACC, KR, "start", 600)
d.t(x3 + 26, PY + 146, "Ref:", 12, MUTED, KR, "start")
d.t(x3 + 68, PY + 146, "기본키 또는 heap 위치", 12, SOFT, KR, "start")

d.arrow([(x3 + 32, PY + 162), (x3 + 32, PY + 188)], ACC, "acc", 1.4)
d.t(x3 + 46, PY + 179, "인덱스가 쿼리를 cover", 12, ACC, KR, "start")

# 설명 상자
d.box(x3 + 14, PY + 196, CW - 28, 96, PAPER, RULE, 0.8)
d.t(x3 + CW / 2, PY + 218, "일부 쿼리는 인덱스만으로 답함", 12, INK, KR, "middle", 600)
d.t(x3 + CW / 2, PY + 238, "기본키 해소나 heap 조회 건너뜀", 12, OK, KR, "middle")
d.t(x3 + CW / 2, PY + 258, "일부 쿼리 빨라짐", 12, ACC, KR, "middle")
d.t(x3 + CW / 2, PY + 276, "데이터 중복 · 디스크 더 씀 · 쓰기 느림", 12, WARN, KR, "middle")

d.legend(LEG, [("clustered", OK), ("heap file 참조", INFO), ("covering index", ACC), ("트레이드오프", WARN)])
d.save("04-04.index-value-storage.svg")
