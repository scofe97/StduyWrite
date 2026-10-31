# 09-04 §3 — 분산 시스템 검증 3대 접근법(모델 체커·결함 주입·결정론적 시뮬레이션 DST) 비교 행렬.
# 사실 출처: 09-04 본문 §1(L24~L30), §2(L36~L40), §3(L46~L56), 면접 질문 2(L114~L116), 원서 Ch.9 "Formal Methods and Randomized Testing".
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 512
H = LEG + 56

d = D(W, H, "09-04 §3 · VERIFICATION APPROACHES", "분산 시스템 검증 3대 접근법 비교",
      "형식 명세를 검증하는 모델 체커, 실제 환경에 장애를 주입하는 결함 주입, 실행 순서를 가상 제어하는 결정론적 시뮬레이션(DST)을 비교한다.",
      "모델 체커(명세 탐색) · 결함 주입(실제 환경 장애) · 결정론적 시뮬레이션(완전 제어 재현)")

CW = 260
GAP = 14
X0 = 31

columns = [
    ("모델 체커 (Model Checking)", "알고리즘 명세 검증 · §1", INFO, False, [
        ("검증 대상과 환경", "수학적 알고리즘 명세 기술", "TLA+ · Gallina · FizzBee"),
        ("핵심 강점과 한계", "전체 상태 공간 체계적 탐색", "실제 코드 미검사 · 명세 괴리"),
        ("재현성 · 탐색 범위", "상태 수 상한 설정 탐색", "무한 상태 공간 · 단순화된 모델"),
        ("대표 도구 및 적용 사례", "CockroachDB · Kafka 버그 발견", "Viewstamped Replication 분석"),
    ]),
    ("결함 주입 (Fault Injection)", "실제 환경 장애 주입 · §2", WARN, False, [
        ("검증 대상과 환경", "실행 중인 실제 코드", "프로덕션 · 스테이징 환경"),
        ("핵심 강점과 한계", "실제 환경 장애 반응 관찰", "모델 · 구현 괴리 없음"),
        ("재현성 · 탐색 범위", "낮은 재현성 (비결정론 거동)", "실제 네트워크 타이밍 의존"),
        ("대표 도구 및 적용 사례", "Chaos Monkey (카오스)", "Jepsen (Redis · etcd 검증)"),
    ]),
    ("결정론적 시뮬레이션 (DST)", "가상 환경 완전 제어 · §3", ACC, True, [
        ("검증 대상과 환경", "실제 코드 (수정 최소화)", "네트워크 · I/O · 시계 모의 교체"),
        ("핵심 강점과 한계", "같은 실행 시퀀스 재현", "앱 · 런타임 · 머신 3수준 제어"),
        ("재현성 · 탐색 범위", "벽시계보다 빠른 시뮬레이션", "실제 타임아웃 대기 없음"),
        ("대표 도구 및 적용 사례", "Flow · TigerBeetle", "MadSim · Antithesis"),
    ]),
]

for col_idx, (col_title, col_sub, col_c, is_focal, rows) in enumerate(columns):
    x = X0 + col_idx * (CW + GAP)

    # 컬럼 헤더
    if is_focal:
        d.tone(x, 96, CW, 50, col_c, 6, "18", 1.4)
    else:
        d.tone(x, 96, CW, 50, col_c, 6, "12", 1.0)
    d.t(x + CW / 2, 118, col_title, 13, col_c if is_focal else INK, KR, "middle", 600)
    d.t(x + CW / 2, 136, col_sub, 12, MUTED, KR, "middle")

    # 4개 행 카드
    for row_idx, (r_title, r_line1, r_line2) in enumerate(rows):
        y = 156 + row_idx * 88
        if is_focal:
            d.box(x, y, CW, 80, PAPER2, col_c, 1.0)
        else:
            d.box(x, y, CW, 80, PAPER2, RULE, 1.0)

        # 서브카드 헤더
        d.t(x + CW / 2, y + 20, r_title, 12, INK, KR, "middle", 600)
        d.line(x + 12, y + 28, x + CW - 12, y + 28, RULE, 0.6)

        # 항목 1, 2
        d.box(x + 8, y + 34, CW - 16, 20, PAPER, RULE, 0.5, r=3)
        d.t(x + CW / 2, y + 48, r_line1, 11, col_c, KR, "middle")

        d.box(x + 8, y + 56, CW - 16, 20, PAPER, RULE, 0.5, r=3)
        d.t(x + CW / 2, y + 70, r_line2, 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("알고리즘 명세 검증", INFO),
    ("실제 환경 장애 주입", WARN),
    ("가상 제어 시뮬레이션 (focal)", ACC),
])

d.save("09-04.distributed-system-verification.svg")
