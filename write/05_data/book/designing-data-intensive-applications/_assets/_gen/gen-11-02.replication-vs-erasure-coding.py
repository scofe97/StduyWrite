# 11-02 §2 — 단순 복제와 이레이저 코딩의 특성 및 트레이드오프 비교
# 사실 출처: 11-02 본문 §2(L48~L54) — 복제 인수 3, k=6·m=3 → 9개 샤드 1.5배(9/6), XOR·갈루아 체 연산, 읽기 로컬리티, RAID-5·6.
# 원서 Ch.11 p.10 은 Reed–Solomon·"6장의 복제"·RAID 유사성만 말하고 수치(3, k=6, m=3)는 주지 않는다. 그래서 배너는 "본문 예"로 단다.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 900
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 372
LEG = PY + PH + 26
H = LEG + 52

d = D(W, H, "11-02 · §2 REPLICATION VS ERASURE CODING", "복제와 이레이저 코딩 트레이드오프 비교",
      "단순 복제의 읽기 로컬리티와 이레이저 코딩의 저장 효율 대조",
      "저장 오버헤드 배수 · 복구 메커니즘 · 읽기 로컬리티 · CPU 계산 비용 · 유사 기법")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "본문 예: 복제 인수 3(3.0배 공간) 대 Reed-Solomon(k=6, m=3, 1.5배 공간 및 계산 복구)", 12, INK, KR, "middle", 600)

CW = 414
GAP = 24
X0 = 24

cols = [
    ("단순 복제 (Replication)", "3배 복사본 · 읽기 로컬리티 확보", INFO, [
        ("저장 배수", "원본 데이터의 3.0배 용량", "복제 인수 3 기준 디스크 300% 점유"),
        ("복구 방식", "바이트 단위 단순 복사", "잃어버린 블록의 다른 복사본 복사"),
        ("로컬리티", "읽기 로컬리티(read locality) 확보", "연산 태스크를 데이터 노드에 우선 배치"),
        ("계산 비용", "복구 시 연산 오버헤드 없음", "갈루아 체 연산 불필요"),
        ("유사 기법", "같은 데이터를 여러 머신에 복사", "6장 복제와 같은 방식"),
    ]),
    ("이레이저 코딩 (Erasure Coding)", "1.5배 용량 · 계산 기반 샤드 복구", ACC, [
        ("저장 배수", "원본 데이터의 1.5배 용량", "Reed-Solomon (k=6 데이터 + m=3 패리티)"),
        ("복구 방식", "XOR·갈루아 체 수학적 재구성", "어느 3개(m) 샤드가 사라져도 복구"),
        ("로컬리티", "읽기 로컬리티 활용 불가", "데이터 재구성을 위해 다수 노드 샤드 수집"),
        ("계산 비용", "복구 시 CPU 연산 오버헤드 발생", "남은 샤드로 원본 재구성"),
        ("유사 기법", "RAID-5 · RAID-6 와 같은 원리", "샤드를 여러 머신 디스크에 분산"),
    ]),
]

for i, (title, subtitle, col_c, rows) in enumerate(cols):
    x = X0 + i * (CW + GAP)

    # 열 외곽 상자
    is_focal_col = (i == 1)
    if is_focal_col:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.3)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 열 헤더
    d.chip(x + 48, PY + 24, "단순 복제" if i == 0 else "이레이저", col_c, 12)
    d.t(x + CW / 2 + 20, PY + 27, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 47, subtitle, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 5개 행 비교 항목
    for j, (dim, top_txt, bot_txt) in enumerate(rows):
        iy = PY + 68 + j * 58
        is_focal_cell = (i == 1 and j == 0)  # 1.5배 용량 절감
        is_locality_focal = (i == 0 and j == 2)  # 로컬리티 최적화

        if is_focal_cell:
            d.tone(x + 10, iy, CW - 20, 50, ACC, 5, "22", 1.3)
            d.chip(x + 48, iy + 25, dim, ACC, 12)
            d.t(x + 88, iy + 20, top_txt, 12, ACC, KR, "start", 600)
            d.t(x + 88, iy + 38, bot_txt, 12, INK, KR, "start")
        elif is_locality_focal:
            d.tone(x + 10, iy, CW - 20, 50, OK, 5, "18", 1.2)
            d.chip(x + 48, iy + 25, dim, OK, 12)
            d.t(x + 88, iy + 20, top_txt, 12, OK, KR, "start", 600)
            d.t(x + 88, iy + 38, bot_txt, 12, INK, KR, "start")
        else:
            d.box(x + 10, iy, CW - 20, 50, PAPER, RULE, 0.8)
            d.chip(x + 48, iy + 25, dim, col_c if j == 0 else SOFT, 12)
            d.t(x + 88, iy + 20, top_txt, 12, INK, KR, "start", 600)
            d.t(x + 88, iy + 38, bot_txt, 12, MUTED, KR, "start")

d.legend(LEG, [
    ("이레이저 코딩 (focal)", ACC),
    ("단순 복제 특성", INFO),
    ("로컬리티 이점", OK),
])

d.save("11-02.replication-vs-erasure-coding.svg")
