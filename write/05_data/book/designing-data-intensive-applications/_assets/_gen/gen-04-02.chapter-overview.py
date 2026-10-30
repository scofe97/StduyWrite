# 04-02 개요 — 쓰기·읽기·병합 세 경로와 네 절의 LSM 저장 엔진 전체 지도.
# 사실 출처: 04-02 서두(L17~L25), §1(L29~L34), §2(L40~L52), §3(L56~L63), §4(L67~L77).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

W = 880
PY = 100
PH = 372
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-02 · CHAPTER OVERVIEW", "LSM 저장 엔진의 세 경로 전체 지도",
      "쓰기·읽기·병합 세 경로가 memtable, 불변 SSTable, Bloom 필터, compaction을 거치는 구조를 조망한다.",
      "쓰기 경로(§2) · 읽기 세그먼트 탐색(§1, §3) · 백그라운드 병합(§4)")

# 3개 컬럼: 쓰기 경로, 읽기 경로, 병합 경로
CW = 264
GAP = 16
X0 = 28

cols = [
    ("쓰기 경로", "§2 쓰기 경로", INFO, [
        ("클라이언트 쓰기", "set(key, val) 요청", MONO),
        ("WAL 로그 즉시 기록", "디스크 순차 추가 · 크래시 복원용", KR),
        ("memtable 정렬맵 삽입", "인메모리 트리 구조에 키 정렬 저장", KR),
        ("임계 초과 시 flush", "수 MB 도달 시 SSTable 생성(§1)", KR),
    ]),
    ("읽기 경로", "§2 읽기 · §3 Bloom", ACC, [
        ("클라이언트 읽기", "get(key) 요청", MONO),
        ("memtable 1차 검색", "인메모리 최신 값 즉시 반환", KR),
        ("Bloom 필터 비트 확인", "부재 키 SSTable 즉시 건너뜀", KR),
        ("sparse 인덱스 블록 탐색", "첫 키 범위 확인 후 블록 스캔(§1)", KR),
    ]),
    ("병합·압축 경로", "§4 compaction", WARN, [
        ("백그라운드 병합 시작", "세그먼트 누적 시 백그라운드 구동", KR),
        ("mergesort 순차 병합", "입력 파일 나란히 읽어 최신값 유지", KR),
        ("tombstone 정리", "삭제 마커 및 이전 값 폐기", KR),
        ("compaction 전략 적용", "size-tiered vs leveled 층 관리", KR),
    ]),
]

FOCAL_IDX = 1  # 읽기 경로(SSTable + Bloom + sparse)가 네 절의 교차점

for i, (title, sec_tag, tag_c, steps) in enumerate(cols):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL_IDX)
    
    # 외곽 박스
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)
    
    # 헤더: 칩과 제목
    d.chip(x + CW / 2, PY + 24, sec_tag, tag_c, 12)
    d.t(x + CW / 2, PY + 52, title, 15, INK, KR, "middle", 600)
    d.line(x + 16, PY + 68, x + CW - 16, PY + 68, RULE, 0.8)
    
    # 4단계 카드
    step_y0 = PY + 80
    step_h = 56
    step_gap = 14
    for j, (st_title, st_sub, st_fam) in enumerate(steps):
        sy = step_y0 + j * (step_h + step_gap)
        d.box(x + 14, sy, CW - 28, step_h, PAPER, RULE, 0.8)
        d.t(x + CW / 2, sy + 22, st_title, 13, INK, st_fam, "middle", 600)
        d.t(x + CW / 2, sy + 42, st_sub, 12, MUTED, KR, "middle")
        
        # 단계 사이 화살표
        if j < len(steps) - 1:
            arrow_y = sy + step_h
            d.arrow([(x + CW / 2, arrow_y), (x + CW / 2, arrow_y + step_gap - 2)], MUTED, "ar", 1.0)

d.legend(LEG, [
    ("쓰기 파이프라인", INFO),
    ("읽기·탐색 파이프라인", ACC),
    ("백그라운드 병합", WARN),
])

d.save("04-02.chapter-overview.svg")
