# 08-04 §6 — 8장 트랜잭션 격리 수준·직렬화 구현·분산 원자성 종합 비교 행렬.
# 검증(10-31 cc-ddia-dverify08): 본문·원서 8장에 없는 Raft/Paxos·"락 프리"·"상호 블록 차단"(뜻 반대로 읽힘)·평가어를 본문 말로 · 본문에 없는 번역어 "커밋 후 읽기"를 본문 표기 Read Committed 로
# 사실 출처: 08-04 §6(L97~L115), 원서 Ch.8 Summary(PDF p.63~65)
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 510
H = LEG + 56

d = D(W, H, "08-04 §6 · CHAPTER 8 SUMMARY MATRIX", "8장 트랜잭션 격리 수준·직렬화·분산 원자성 종합 비교",
      "격리 수준별 방지 이상 현상, 직렬화 구현 3대 방식의 트레이드오프, 분산 원자 커밋과 회피 대안을 비교한다.",
      "트랜잭션 격리 수준의 이상 현상 방어 사다리 · 직렬화 격리 구현 3대 방식 · 분산 원자성 접근법 종합")

CW = 260
GAP = 14
X0 = 31

columns = [
    ("격리 수준 사다리", "이상 현상 방지 보장", INFO, [
        ("Read Committed", "더티 읽기 · 더티 쓰기 방지", "행 잠금 및 커밋 시점 뷰 제공"),
        ("스냅샷 격리 (Snapshot Isolation)", "읽기 스큐 방지 (MVCC 다중 버전)", "읽기·쓰기가 서로 막지 않음"),
        ("직렬화 격리 (Serializable)", "갱신 손실 · 쓰기 스큐 · 팬텀 방지", "모든 경쟁 조건 방지"),
    ]),
    ("직렬화 3대 구현", "동시성 제어 트레이드오프", ACC, [
        ("단일 스레드 직렬 실행", "단일 CPU 코어 순차 처리", "인메모리 데이터 · 저장 프로시저"),
        ("2단계 잠금 (2PL)", "읽기 공유 · 쓰기 배타 잠금", "비관적 대기 · 경합 및 교착 빈발"),
        ("직렬화 가능 스냅샷 (SSI)", "낙관적 접근 · 잠금 없는 읽기", "커밋 시 직렬화 충돌 감지 및 중단"),
    ]),
    ("분산 원자성 대안", "다중 노드 일관성 달성", OK, [
        ("2PC 프로토콜", "준비 질의와 커밋 포인트 2단계 약속", "코디네이터 장애 시 의심 상태 블록"),
        ("XA 이기종 분산 표준", "앱 내장 코디네이터 · 로컬 로그", "최소 공통 분모 한계 · 휴리스틱 위험"),
        ("NewSQL 합의 & 멱등성", "합의 알고리즘으로 코디네이터 복제", "고유 메시지 ID 기록 멱등 처리"),
    ]),
]

for col_idx, (col_title, col_sub, col_c, cards) in enumerate(columns):
    x = X0 + col_idx * (CW + GAP)

    # 컬럼 헤더
    d.tone(x, 100, CW, 50, col_c, 6, "16", 1.4)
    d.t(x + CW / 2, 122, col_title, 13, col_c, KR, "middle", 600)
    d.t(x + CW / 2, 140, col_sub, 12, INK, KR, "middle")

    # 카드 3개
    for row_idx, (c_title, c_line1, c_line2) in enumerate(cards):
        y = 160 + row_idx * 110
        d.box(x, y, CW, 100, PAPER2, RULE, 1.0)

        # 서브카드 헤더
        d.t(x + CW / 2, y + 25, c_title, 12, INK, KR, "middle", 600)
        d.line(x + 12, y + 36, x + CW - 12, y + 36, RULE, 0.7)

        # 항목 라인
        d.box(x + 8, y + 44, CW - 16, 22, PAPER, RULE, 0.5, r=3)
        d.t(x + CW / 2, y + 59, c_line1, 11, col_c, KR, "middle")

        d.box(x + 8, y + 70, CW - 16, 22, PAPER, RULE, 0.5, r=3)
        d.t(x + CW / 2, y + 85, c_line2, 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("격리 수준 보장", INFO),
    ("직렬화 트레이드오프", ACC),
    ("분산 원자성 대안", OK)
])

d.save("08-04.chapter-summary.svg")
