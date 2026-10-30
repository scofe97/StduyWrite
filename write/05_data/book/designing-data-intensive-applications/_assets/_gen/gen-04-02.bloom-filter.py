# 04-02 §3 — Bloom 필터의 해시 비트 확인과 키 부재 확정 / 디스크 확인 결정 트리.
# 사실 출처: 04-02 본문 §3(L59~L63) — handbag (2,9,4) 비트 설정 예시, 0 비트 시 확실한 부재, 모두 1일 때 거짓양성과 디스크 블록 검사.
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 96
PH = 396
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-02 · §3 BLOOM FILTER", "Bloom 필터 키 확인 결정 흐름",
      "해시 함수로 비트 배열을 확인하여 0 비트 발견 시 키 부재를 즉시 확정하고 불필요한 디스크 I/O를 건너뛴다.",
      "해시 계산(2·9·4번 비트) → 0 비트 여부 분기 → 부재 확정 또는 디스크 블록 검사")

# 상단: 비트 배열 실제 상태 예시 바
d.box(28, PY, 824, 64, PAPER2, RULE, 1.0)
d.chip(96, PY + 20, "Bloom 비트 배열", INFO, 12)
d.t(176, PY + 20, "키당 10비트 할당 · handbag 해시 인덱스: 2, 4, 9 비트 설정", 12, MUTED, KR, "start")

# 10개 비트 셀 (인덱스 상단, 비트값 내부)
BX0 = 176
BW = 60
for idx in range(10):
    bx = BX0 + idx * BW
    is_hit = idx in (2, 4, 9)
    val = "1" if is_hit else "0"
    bc = ACC if is_hit else RULE
    bg = PAPER if not is_hit else PAPER2
    
    # 인덱스 라벨
    d.t(bx + 26, PY + 38, f"bit {idx}", 10, ACC if is_hit else MUTED, MONO, "middle")
    # 비트 상자
    d.box(bx, PY + 42, 52, 20, bg, bc, 1.2 if is_hit else 0.8, r=3)
    d.t(bx + 26, PY + 56, val, 12, ACC if is_hit else MUTED, MONO, "middle", 600)


# 플로우차트 메인 분기 (Y=176 ~ Y=476)
# 1. 시작 노드: 키 검색
d.box(320, 176, 240, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=18)
d.t(440, 199, "키 검색: get(target_key)", 12, INK, MONO, "middle", 600)

d.arrow([(440, 212), (440, 244)], MUTED, "ar", 1.2)

# 2. 단계: 독립 해시 함수 3개 계산
d.box(300, 244, 280, 44, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(440, 262, "해시 함수 k=3 개 계산", 12, INK, KR, "middle", 600)
d.t(440, 278, "해시 인덱스: (h1, h2, h3) 산출", 11, MUTED, MONO, "middle")

d.arrow([(440, 288), (440, 318)], MUTED, "ar", 1.2)

# 3. 핵심 결정 다이아몬드 (focal: ACC)
CX, CY, DW, DH = 440, 348, 260, 60
d.o.append(f'<path d="M {CX} {CY - DH / 2} L {CX + DW / 2} {CY} '
           f'L {CX} {CY + DH / 2} L {CX - DW / 2} {CY} Z" '
           f'fill="{PAPER2}" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, CY - 4, "비트 중 하나라도 0인가?", 13, ACC, KR, "middle", 600)
d.t(CX, CY + 14, "최소 1개 비트가 0인 상태", 11, MUTED, KR, "middle")

# 분기 1: Yes (좌측) -> 키 부재 확정
d.arrow([(CX - DW / 2, CY), (212, CY)], OK, "ok", 1.4)
d.t(260, CY - 10, "예 (비트 0)", 11, OK, KR, "middle")

d.box(36, CY - 28, 176, 56, PAPER, OK, 1.2, r=6)
d.t(124, CY - 6, "키 부재 확정", 12, OK, KR, "middle", 600)
d.t(124, CY + 14, "해당 SSTable에 확실히 없음", 11, MUTED, KR, "middle")

d.arrow([(124, CY + 28), (124, 420)], OK, "ok", 1.2)

d.box(36, 420, 176, 52, PAPER2, OK, 1.4, r=6)
d.t(124, 440, "SSTable 파일 건너뜀", 13, OK, KR, "middle", 600)
d.t(124, 458, "그 SSTable 읽기 생략", 11, MUTED, KR, "middle")


# 분기 2: No (우측) -> 모든 비트 1인 경우
d.arrow([(CX + DW / 2, CY), (668, CY)], WARN, "warn", 1.4)
d.t(620, CY - 10, "아니오 (모두 1)", 11, WARN, KR, "middle")

d.box(668, CY - 28, 176, 56, PAPER, WARN, 1.2, r=6)
d.t(756, CY - 6, "키 존재 가능성 높음", 12, WARN, KR, "middle", 600)
d.t(756, CY + 14, "sparse 인덱스 디스크 검사", 11, MUTED, KR, "middle")

d.arrow([(756, CY + 28), (756, 404)], WARN, "warn", 1.2)

# 디스크 확인 후 분기 박스
d.box(656, 404, 200, 68, PAPER2, RULE, 1.0, r=6)
d.t(756, 422, "디스크 블록 검증 결과", 12, INK, KR, "middle", 600)
d.t(672, 442, "실제 키 존재 → 값 반환", 11, OK, KR, "start")
d.t(672, 460, "거짓양성(1%) → 다음 탐색", 11, WARN, KR, "start")

d.legend(LEG, [
    ("해시 및 비트 확인", INFO),
    ("부재 확정 · I/O 생략", OK),
    ("거짓양성 가능 · 디스크 확인", WARN),
    ("분기 판단 (focal)", ACC),
])

d.save("04-02.bloom-filter.svg")
