# 04-05 §3 — 행 전체 다중 키 정렬 순서에 따른 컬럼 압축과 로그 구조 대량 쓰기.
# 사실 출처: 본문 §3(L56~L65), DDIA Ch.4 Sort order in column storage & Writing to column-oriented storage
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 104, 276
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-05 · SORT ORDER", "행 전체 다중 키 정렬과 일괄 쓰기 구조",
      "행 전체 단위로 정렬해 첫 정렬 키의 긴 반복으로 압축 효과를 극대화하고, 쓰기는 인메모리 버퍼 축적 후 디스크 컬럼 파일로 일괄 병합한다.",
      "1차 정렬 키 RLE 압축 · 2차 정렬 순서 보장 · 인메모리 버퍼 일괄 병합")

LW = 412
RW = 412
LX0 = 20
RX0 = 448

# 좌측 패널: 다중 키 정렬 순서와 압축 효과
d.box(LX0, PY, LW, PH, PAPER2, ACC, 1.2)
d.chip(LX0 + 36, PY + 22, "정렬", ACC, 11)
d.t(LX0 + 180, PY + 26, "다중 정렬 키와 압축 효과", 13, INK, KR, "middle", 600)
d.t(LX0 + LW / 2, PY + 46, "행 전체 단위 정렬 · 컬럼별 독립 정렬 금지", 12, SOFT, KR, "middle")
d.line(LX0 + 12, PY + 56, LX0 + LW - 12, PY + 56, RULE, 0.8)

# 정렬 키 컬럼 3개
keys_info = [
    ("1차 정렬: date_key", "[ 260101, 260101, 260101, 260102, ... ]", OK, "긴 연속 반복 · 압축 가장 잘 됨"),
    ("2차 정렬: product_sk", "[     29,     30,     69,     31, ... ]", INFO, "같은 날짜 안의 순서 결정"),
    ("하위 컬럼: store_sk", "[      3,      5,      3,      4, ... ]", SOFT, "k번째 항목 일치 유지 · 행 재조립"),
]

for idx, (k_title, k_sample, k_color, k_desc) in enumerate(keys_info):
    ky = PY + 66 + idx * 42
    d.box(LX0 + 12, ky, LW - 24, 36, PAPER, RULE, 0.8)
    d.t(LX0 + 20, ky + 16, k_title, 11.5, k_color, MONO if "key" in k_title else KR, "start", 600)
    d.t(LX0 + LW - 20, ky + 16, k_desc, 11, k_color, KR, "end")
    d.t(LX0 + 20, ky + 30, k_sample, 11, MUTED, MONO, "start")

# 정렬 효과 요약
d.tone(LX0 + 12, PY + 200, LW - 24, 64, ACC, 6, "18", 1.2)
d.t(LX0 + LW / 2, PY + 220, "첫 정렬 키는 수십억 행도 수 KB로 RLE 압축", 12, INK, KR, "middle", 600)
d.t(LX0 + LW / 2, PY + 238, "날짜 범위 쿼리 시 대상 구간 블록만 스캔", 11.5, ACC, KR, "middle")
d.t(LX0 + LW / 2, PY + 253, "컬럼 간 같은 행 순서 유지로 k번째 항목 결합 보장", 11, OK, KR, "middle")

# 우측 패널: 로그 구조 일괄 쓰기
d.box(RX0, PY, RW, PH, PAPER2, RULE, 0.9)
d.chip(RX0 + 36, PY + 22, "쓰기", WARN, 11)
d.t(RX0 + 180, PY + 26, "로그 구조 일괄 적재 (ETL)", 13, INK, KR, "middle", 600)
d.t(RX0 + RW / 2, PY + 46, "압축 컬럼 재작성 비용 분산 파이프라인", 12, SOFT, KR, "middle")
d.line(RX0 + 12, PY + 56, RX0 + RW - 12, PY + 56, RULE, 0.8)

# 쓰기 흐름 3단계
# 1) 쓰기 유입
d.box(RX0 + 12, PY + 66, RW - 24, 34, PAPER, RULE, 0.8)
d.t(RX0 + 24, PY + 87, "신규 쓰기 유입", 11.5, INK, KR, "start", 600)
d.t(RX0 + RW - 24, PY + 87, "행 단위 삽입 요청", 11, SOFT, KR, "end")

# 화살표
d.arrow([(RX0 + RW / 2, PY + 102), (RX0 + RW / 2, PY + 110)], SOFT, "soft", 1.1)

# 2) 인메모리 버퍼
d.tone(RX0 + 12, PY + 112, RW - 24, 38, WARN, 4, "16", 1.0)
d.t(RX0 + 24, PY + 130, "인메모리 정렬 행 저장소", 11.5, WARN, KR, "start", 600)
d.t(RX0 + RW - 24, PY + 130, "정렬 순서 유지하며 버퍼링", 11, WARN, KR, "end")
d.t(RX0 + 24, PY + 144, "일정량 누적 시까지 메모리 보관", 11, MUTED, KR, "start")

# 화살표
d.arrow([(RX0 + RW / 2, PY + 152), (RX0 + RW / 2, PY + 160)], SOFT, "soft", 1.1)

# 3) 디스크 일괄 병합
d.box(RX0 + 12, PY + 162, RW - 24, 38, PAPER, RULE, 0.9)  # 범례 초록(1차 키 RLE)과 겹치지 않게 중립색
d.t(RX0 + 24, PY + 180, "디스크 컬럼 파일 일괄 병합", 11.5, INK, KR, "start", 600)
d.t(RX0 + RW - 24, PY + 180, "신규 불변 파일 일괄 작성", 11, SOFT, KR, "end")
d.t(RX0 + 24, PY + 194, "오브젝트 스토리지 적합 구조", 11, MUTED, KR, "start")

# 쓰기 계층 요약
d.box(RX0 + 12, PY + 208, RW - 24, 56, PAPER, RULE, 0.8)
d.t(RX0 + RW / 2, PY + 228, "쿼리는 메모리 쓰기와 디스크 컬럼 파일을 결합", 11.5, INK, KR, "middle", 600)
d.t(RX0 + RW / 2, PY + 246, "실행 엔진이 계층 분리를 사용자에게 은닉", 11, SOFT, KR, "middle")

d.legend(LEG, [("1차 키 RLE 압축", OK), ("2차 정렬 키", INFO), ("인메모리 정렬 버퍼", WARN), ("행 재조립 순서 보장", ACC)])
d.save("04-05.sort-order.svg")
