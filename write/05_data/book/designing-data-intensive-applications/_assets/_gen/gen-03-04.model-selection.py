# 03-04 §1 — 애플리케이션 데이터 구조와 접근 패턴에 따른 문서 모델 vs 관계형 모델 선택 결정 트리.
# 사실 출처: 03-04 본문 §1(L32~L42) — 1:N 트리와 일괄 로드, 중첩 항목 직접 참조와 ID, 드래그&드롭 재정렬과 JSON 배열.
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W, H = 880, 540
LEG = 472

d = D(W, H, "03-04 · MODEL SELECTION", "문서 모델과 관계형 모델 선택 결정 트리",
      "데이터가 1:N 트리인지, 중첩 항목 ID 참조가 필요한지, 항목 순서 재정렬이 있는지에 따라 모델을 결정한다.",
      "데이터 접근 패턴 → 조건 분기 → 권장 데이터 모델")

CX = 300
RX = 660
BW = 260
BH = 50
DW = 270
DH = 56

def oval(x, y, w, h, txt, sub=None):
    d.box(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.1, r=h / 2)
    d.t(x + w / 2, y + (18 if sub else h / 2 + 5), txt, 12, INK, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 33, sub, 11, MUTED, KR, "middle")

def dia(cx, cy, w, h, txt, sub=None):
    d.o.append(f'<path d="M {cx} {cy - h / 2} L {cx + w / 2} {cy} '
               f'L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(cx, cy + (2 if sub else 5), txt, 12, INK, KR, "middle", 600)
    if sub:
        d.t(cx, cy + 18, sub, 10, MUTED, KR, "middle")

def step(x, y, w, h, txt, sub=None, c=RULE, sw=1.0, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="16", sw=1.4)
    else:
        d.box(x, y, w, h, fill=PAPER2, stroke=c, sw=sw, r=6)
    tc = ACC if focal else INK
    sc = ACC if focal else MUTED
    d.t(x + w / 2, y + (20 if sub else h / 2 + 5), txt, 12, tc, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 36, sub, 11, sc, KR, "middle")

# 1. 시작 노드
oval(CX - 110, 88, 220, 36, "데이터 접근 패턴 평가", "신규 애플리케이션 데이터 구조")
d.arrow([(CX, 124), (CX, 152)], MUTED, "ar")

# 2. 결정 1: 1:N 트리 구조 & 일괄 로드
dia(CX, 180, DW, DH, "1:N 트리 구조 · 일괄 로드 ?")

# No -> 오른쪽: 관계형 모델 권장 (다대다 · 조인 필요)
d.arrow([(CX + DW / 2, 180), (RX - BW / 2, 180)], MUTED, "ar")
d.t((CX + DW / 2 + RX - BW / 2) / 2, 170, "아니오", 11, MUTED, KR, "middle")
step(RX - BW / 2, 155, BW, BH, "관계형 모델 권장", "조인 · 다대일 · 다대다 지원", c=INFO)

# Yes -> 아래
d.arrow([(CX, 208), (CX, 242)], MUTED, "ar")
d.t(CX + 14, 228, "예", 11, MUTED, KR, "start")

# 3. 결정 2: 중첩 항목 ID 직접 참조 필요
dia(CX, 270, DW, DH, "중첩 항목 ID 직접 참조 필요 ?")

# Yes -> 오른쪽: 관계형 모델 권장 (ID 직접 참조)
d.arrow([(CX + DW / 2, 270), (RX - BW / 2, 270)], MUTED, "ar")
d.t((CX + DW / 2 + RX - BW / 2) / 2, 260, "예", 11, MUTED, KR, "middle")
step(RX - BW / 2, 245, BW, BH, "관계형 모델 권장", "ID 직접 참조 · 중첩 경로 탐색 불필요", c=INFO)

# No -> 아래
d.arrow([(CX, 298), (CX, 332)], MUTED, "ar")
d.t(CX + 14, 318, "아니오", 11, MUTED, KR, "start")

# 4. 결정 3: 드래그&드롭 항목 순서 재정렬
dia(CX, 360, DW, DH, "드래그&드롭 순서 재정렬 ?")

# Yes -> 오른쪽: 문서 모델 권장 (focal)
d.arrow([(CX + DW / 2, 360), (RX - BW / 2, 360)], ACC, "acc", sw=1.4)
d.t((CX + DW / 2 + RX - BW / 2) / 2, 350, "예", 11, ACC, KR, "middle", 600)
step(RX - BW / 2, 335, BW, BH, "문서 모델 권장 (배열 순서)", "JSON 배열 순서 보존 · 재번호 트릭 불필요", focal=True)

# No -> 아래: 기본 문서 모델 권장
d.arrow([(CX, 388), (CX, 414)], MUTED, "ar")
d.t(CX + 14, 401, "아니오", 11, MUTED, KR, "start")
step(CX - BW / 2, 414, BW, BH, "문서 모델 권장 (트리 로드)", "단일 문서 로드 · 테이블 분쇄 회피", c=OK)

d.legend(LEG, [("문서 모델 (순서 보존)", ACC), ("문서 모델 (트리 로드)", OK), ("관계형 (조인·참조)", INFO), ("분기", MUTED)])
d.save("03-04.model-selection.svg")
