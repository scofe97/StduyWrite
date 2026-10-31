# 10-04 §1 — 단일 값 합의와 선형화 CAS·공유 로그·원자 커밋 간 상호 변환 동치 관계 및 FLP 불가능성 한계.
# 사실 출처: 10-04 §1(L23~L38), 원서 Ch.10 "THE IMPOSSIBILITY OF CONSENSUS" ~ "Atomic commitment as consensus"(PDF p.34~41)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 435
H = LEG + 56

d = D(W, H, "10-04 · §1 EQUIVALENT PROBLEMS TO CONSENSUS", "합의 문제와 동치인 핵심 분산 연산들",
      "단일 값 합의와 선형화 CAS, 공유 로그, 2노드 fetch-and-add, 원자 커밋은 상호 변환 가능한 동치 관계다.",
      "단일 값 합의 4대 속성 · 상호 변환 가능한 동치 문제군 · 원자 커밋 규칙 차이 · FLP 불가능성과 타임아웃")

# 중앙 허브: 단일 값 합의 (Consensus)
CX, CY, CW, CH = 296, 105, 288, 222
d.tone(CX, CY, CW, CH, ACC, 6, "14", 1.4)
d.t(440, 128, "단일 값 합의 (Consensus)", 14, ACC, KR, "middle", 600)
d.t(440, 146, "하나 이상의 제안 값 중 정확히 하나를 결정", 11, MUTED, KR, "middle")

# 안전성 박스
d.box(CX + 10, 160, CW - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(440, 178, "안전성 속성 (Safety)", 11, INK, KR, "middle", 600)
d.t(440, 196, "균일 합의: 모든 노드가 동일 값 결정", 11, MUTED, KR, "middle")
d.t(440, 214, "무결성·유효성: 번복 불가 및 제안 값 한정", 11, MUTED, KR, "middle")

# 활동성 박스
d.box(CX + 10, 240, CW - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(440, 260, "활동성 속성 (Liveness)", 11, INK, KR, "middle", 600)
d.t(440, 280, "종료: 무장애 노드는 반드시 결정", 11, MUTED, KR, "middle")
d.t(440, 298, "과반수 쿼럼 동작 시 종료 보장", 11, MUTED, KR, "middle")

# 1. 좌상단: 선형화 Compare-and-Set
X1, Y1, W1, H1 = 24, 105, 216, 104
d.box(X1, Y1, W1, H1, PAPER2, RULE, 1.0)
d.chip(X1 + 24, Y1 + 20, "CAS", INFO, 11, pad=4)
d.t(X1 + 120, Y1 + 24, "선형화 CAS 연산", 12, INK, KR, "middle", 600)
d.line(X1 + 10, Y1 + 38, X1 + W1 - 10, Y1 + 38, RULE, 0.6)
d.t(X1 + W1 / 2, Y1 + 56, "null 에서 새 값으로 CAS 성공", 11, MUTED, KR, "middle")
d.t(X1 + W1 / 2, Y1 + 74, "동시 시도 중 단 하나만 성공", 11, MUTED, KR, "middle")
d.t(X1 + W1 / 2, Y1 + 92, "합의 ↔ 선형화 CAS 상호 변환", 11, INFO, KR, "middle")

# 2. 좌하단: 선형화 Fetch-and-Add
X2, Y2, W2, H2 = 24, 223, 216, 104
d.box(X2, Y2, W2, H2, PAPER2, RULE, 1.0)
d.chip(X2 + 24, Y2 + 20, "F&A", INFO, 11, pad=4)
d.t(X2 + 120, Y2 + 24, "선형화 Fetch-and-Add", 12, INK, KR, "middle", 600)
d.line(X2 + 10, Y2 + 38, X2 + W2 - 10, Y2 + 38, RULE, 0.6)
d.t(X2 + W2 / 2, Y2 + 56, "원자 카운터 읽기 및 증분", 11, MUTED, KR, "middle")
d.t(X2 + W2 / 2, Y2 + 74, "2노드 시스템 한정 합의와 동치", 11, MUTED, KR, "middle")
d.t(X2 + W2 / 2, Y2 + 92, "다중 노드 시 일반 합의 불가", 11, INFO, KR, "middle")

# 3. 우상단: 공유 로그 (Total Order Broadcast)
X3, Y3, W3, H3 = 640, 105, 216, 104
d.box(X3, Y3, W3, H3, PAPER2, RULE, 1.0)
d.chip(X3 + 24, Y3 + 20, "TOB", OK, 11, pad=4)
d.t(X3 + 120, Y3 + 24, "공유 로그 (전체 순서)", 12, INK, KR, "middle", 600)
d.line(X3 + 10, Y3 + 38, X3 + W3 - 10, Y3 + 38, RULE, 0.6)
d.t(X3 + W3 / 2, Y3 + 56, "신뢰 전달 + 전체 순서 보장", 11, MUTED, KR, "middle")
d.t(X3 + W3 / 2, Y3 + 74, "첫 번째 추가 항목 = 합의 결정", 11, MUTED, KR, "middle")
d.t(X3 + W3 / 2, Y3 + 92, "연속 합의 인스턴스로 구축", 11, OK, KR, "middle")

# 4. 우하단: 원자 커밋 (Atomic Commitment / 2PC)
X4, Y4, W4, H4 = 640, 223, 216, 104
d.box(X4, Y4, W4, H4, PAPER2, RULE, 1.0)
d.chip(X4 + 24, Y4 + 20, "2PC", WARN, 11, pad=4)
d.t(X4 + 120, Y4 + 24, "원자 커밋 (2PC)", 12, INK, KR, "middle", 600)
d.line(X4 + 10, Y4 + 38, X4 + W4 - 10, Y4 + 38, RULE, 0.6)
d.t(X4 + W4 / 2, Y3 + 56 + 118, "전원 커밋 또는 전체 중단", 11, MUTED, KR, "middle")
d.t(X4 + W4 / 2, Y3 + 74 + 118, "차이점: 1개라도 거부 시 중단", 11, WARN, KR, "middle")
d.t(X4 + W4 / 2, Y3 + 92 + 118, "투표 뒤 commit·abort 를 합의로 결정", 11, MUTED, KR, "middle")

# 화살표 배선
# 좌상단 <-> 중앙 (간격 X: 240 to 296, gap=56, center=268)
d.path("M 242 148 L 294 148", INFO, 1.2, m="info")
d.path("M 294 162 L 242 162", MUTED, 1.2, m="ar")
d.t(268, 140, "상호 변환", 11, MUTED, KR, "middle")

# 좌하단 <-> 중앙 (간격 X: 240 to 296, gap=56, center=268)
d.path("M 242 266 L 294 266", INFO, 1.2, m="info")
d.path("M 294 280 L 242 280", MUTED, 1.2, m="ar")
d.t(268, 258, "2노드 동치", 11, MUTED, KR, "middle")

# 중앙 <-> 우상단 (간격 X: 584 to 640, gap=56, center=612)
d.path("M 586 148 L 638 148", OK, 1.2, m="ok")
d.path("M 638 162 L 586 162", MUTED, 1.2, m="ar")
d.t(612, 140, "상호 변환", 11, MUTED, KR, "middle")

# 중앙 <-> 우하단 (간격 X: 584 to 640, gap=56, center=612)
d.path("M 586 266 L 638 266", WARN, 1.2, m="warn")
d.path("M 638 280 L 586 280", MUTED, 1.2, m="ar")
d.t(612, 258, "투표 변환", 11, MUTED, KR, "middle")

# 하단: FLP 불가능성 정리와 실용적 해법
d.box(24, 345, 832, 72, PAPER2, RULE, 1.0)
d.t(440, 366, "FLP 불가능성 정리 (1985) 와 실용적 해결", 12, INK, KR, "middle", 600)
d.t(440, 386, "결정론적 비동기 모델에서는 노드 1개 크래시 가능성만 있어도 종료를 항상 보장할 수 없음", 11, MUTED, KR, "middle")
d.t(440, 404, "실용 시스템(Raft·Paxos): 타임아웃을 도입해 리더 장애를 감지하고 현실적 활동성 확보", 11, INK, KR, "middle")

# 범례
d.legend(LEG, [
    ("단일 값 합의 (focal)", ACC),
    ("선형화 연산 동치", INFO),
    ("공유 로그 동치", OK),
    ("원자 커밋 (abort 차이)", WARN)
])

d.save("10-04.consensus-equivalences.svg")
