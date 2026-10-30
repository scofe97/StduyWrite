# 04-02 §2 — LSM 저장 엔진의 쓰기(memtable·WAL·flush), 읽기(최신 순회), 병합(mergesort·tombstone) 데이터 흐름.
# 사실 출처: 04-02 본문 §2(L43~L52) — 1~4단계 LSM 생명주기, WAL 동시 기록, mergesort 세그먼트 병합, tombstone 삭제 마커.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 100
PH = 388
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-02 · §2 LSM FLOW", "LSM 저장 엔진의 쓰기·읽기·병합 데이터 흐름",
      "쓰기는 WAL과 memtable에 동시 기록 후 flush되고, 읽기는 memtable부터 최신 세그먼트 순으로 찾으며, 백그라운드 mergesort로 병합한다.",
      "쓰기 및 flush 경로(좌측) · 읽기 탐색 및 백그라운드 mergesort 병합(우측)")

PW = 400
X_LEFT = 28
X_RIGHT = 452

# 좌측 패널: 쓰기 및 flush 경로
d.box(X_LEFT, PY, PW, PH, PAPER2, INFO, 1.2)
d.t(X_LEFT + 20, PY + 26, "쓰기 및 flush", 14, INFO, KR, "start", 600)
d.t(X_LEFT + 130, PY + 26, "메모리 적재부터 디스크 생성까지", 12, MUTED, KR, "start")

# 1. 클라이언트 쓰기 요청
d.box(X_LEFT + 16, PY + 44, PW - 32, 42, PAPER, RULE, 0.9)
d.t(X_LEFT + 28, PY + 70, "쓰기: set(handbag, v2) · del(handful)", 12, INK, MONO, "start", 600)

# 두 갈래 분기 화살표
d.arrow([(X_LEFT + PW / 2, PY + 86), (X_LEFT + PW / 2, PY + 104)], MUTED, "ar", 1.2)
d.line(X_LEFT + 104, PY + 104, X_LEFT + PW - 104, PY + 104, RULE, 1.0)
d.arrow([(X_LEFT + 104, PY + 104), (X_LEFT + 104, PY + 120)], MUTED, "ar", 1.2)
d.arrow([(X_LEFT + PW - 104, PY + 104), (X_LEFT + PW - 104, PY + 120)], MUTED, "ar", 1.2)

# WAL (좌측 하위) & memtable (우측 하위)
d.box(X_LEFT + 16, PY + 122, 174, 68, PAPER, RULE, 0.9)
d.t(X_LEFT + 103, PY + 144, "WAL 로그", 13, INK, KR, "middle", 600)
d.t(X_LEFT + 103, PY + 164, "디스크 순차 append", 12, MUTED, KR, "middle")
d.t(X_LEFT + 103, PY + 180, "크래시 복원 전용", 11, SOFT, KR, "middle")

d.box(X_LEFT + 210, PY + 122, 174, 68, PAPER, ACC, 1.4)
d.t(X_LEFT + 297, PY + 144, "memtable", 13, INK, MONO, "middle", 600)
d.t(X_LEFT + 297, PY + 164, "인메모리 정렬 트리", 12, ACC, KR, "middle")
d.t(X_LEFT + 297, PY + 180, "handbag:v2 · handful:tomb", 10, MUTED, MONO, "middle")

# memtable -> Flush 화살표
d.arrow([(X_LEFT + 297, PY + 190), (X_LEFT + 297, PY + 234)], ACC, "acc", 1.4)
d.t(X_LEFT + 200, PY + 214, "수 MB 임계 초과 시 flush", 11, ACC, KR, "middle")

# SSTable 세그먼트 생성
d.box(X_LEFT + 16, PY + 236, PW - 32, 58, PAPER, ACC, 1.2)
d.t(X_LEFT + 28, PY + 260, "신규 디스크 SSTable 세그먼트 생성", 13, INK, KR, "start", 600)
d.t(X_LEFT + 28, PY + 280, "키 정렬 불변 파일 · sparse 인덱스 포함", 12, MUTED, KR, "start")

# 새 memtable 교체
d.box(X_LEFT + 16, PY + 306, PW - 32, 66, PAPER, RULE, 0.8)
d.t(X_LEFT + 28, PY + 328, "새 memtable 교체", 12, OK, KR, "start", 600)
d.t(X_LEFT + 28, PY + 348, "flush 진행 중에도 새 쓰기 지속 수신", 12, MUTED, KR, "start")
d.t(X_LEFT + 28, PY + 363, "이전 WAL 로그 안전하게 절삭 폐기", 11, SOFT, KR, "start")


# 우측 패널: 읽기 탐색 및 백그라운드 mergesort 병합
d.box(X_RIGHT, PY, PW, PH, PAPER2, RULE, 1.0)
d.t(X_RIGHT + 20, PY + 26, "읽기 및 병합 흐름", 14, WARN, KR, "start", 600)
d.t(X_RIGHT + 150, PY + 26, "최신순 탐색과 백그라운드 compaction", 12, MUTED, KR, "start")

# 읽기 탐색 경로 (상부)
d.box(X_RIGHT + 16, PY + 44, PW - 32, 134, PAPER, RULE, 0.9)
d.t(X_RIGHT + 28, PY + 66, "읽기 요청: get(handbag)", 12, INK, MONO, "start", 600)

# 읽기 순회 단계들
d.box(X_RIGHT + 28, PY + 76, PW - 56, 26, PAPER2, ACC, 1.0)
d.t(X_RIGHT + 40, PY + 94, "1. memtable 확인", 12, ACC, KR, "start", 600)
d.t(X_RIGHT + PW - 40, PY + 94, "적중 시 즉시 반환", 11, OK, KR, "end")

d.box(X_RIGHT + 28, PY + 108, PW - 56, 26, PAPER2, RULE, 0.8)
d.t(X_RIGHT + 40, PY + 126, "2. Segment 3 (가장 최근)", 12, INK, KR, "start")
d.t(X_RIGHT + PW - 40, PY + 126, "Bloom 필터 거쳐 탐색", 11, MUTED, KR, "end")

d.box(X_RIGHT + 28, PY + 140, PW - 56, 26, PAPER2, RULE, 0.8)
d.t(X_RIGHT + 40, PY + 158, "3. Segment 2 → Segment 1", 12, MUTED, KR, "start")
d.t(X_RIGHT + PW - 40, PY + 158, "오래된 세그먼트 순 탐색", 11, SOFT, KR, "end")

# 병합·압축 (하부)
d.box(X_RIGHT + 16, PY + 190, PW - 32, 182, PAPER, WARN, 1.2)
d.t(X_RIGHT + 28, PY + 214, "백그라운드 mergesort 병합 (compaction)", 13, INK, KR, "start", 600)

# 입력 세그먼트들
d.box(X_RIGHT + 20, PY + 228, 172, 44, PAPER2, RULE, 0.8)
d.t(X_RIGHT + 30, PY + 246, "Segment 1 (구)", 12, MUTED, KR, "start", 600)
d.t(X_RIGHT + 30, PY + 262, "handbag:v1 · handful:v1", 10, SOFT, MONO, "start")

d.box(X_RIGHT + 208, PY + 228, 172, 44, PAPER2, RULE, 0.8)
d.t(X_RIGHT + 218, PY + 246, "Segment 2 (신)", 12, MUTED, KR, "start", 600)
d.t(X_RIGHT + 218, PY + 262, "handbag:v2 · handful:tomb", 10, ACC, MONO, "start")

# 병합 화살표
d.arrow([(X_RIGHT + PW / 2, PY + 272), (X_RIGHT + PW / 2, PY + 300)], WARN, "warn", 1.2)
d.t(X_RIGHT + PW / 2 + 10, PY + 290, "mergesort 키 비교", 11, WARN, KR, "start")

# 병합 결과 세그먼트
d.box(X_RIGHT + 24, PY + 304, PW - 48, 56, PAPER2, OK, 1.2)
d.t(X_RIGHT + 36, PY + 326, "병합 세그먼트 (New Segment)", 12, OK, KR, "start", 600)
d.t(X_RIGHT + 36, PY + 348, "handbag:v2 (최신값 유지) · handful (삭제 폐기)", 11, INK, KR, "start")

d.legend(LEG, [
    ("쓰기 경로", INFO),
    ("memtable·최신 세그먼트", ACC),
    ("mergesort 병합", WARN),
    ("병합 완료", OK),
])

d.save("04-02.lsm-flow.svg")
