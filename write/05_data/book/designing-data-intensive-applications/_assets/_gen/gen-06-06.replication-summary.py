# 06-06 §4 — 6장 단일 리더·다중 리더·리더리스 세 복제 방식의 종합 비교 행렬.
# 사실 출처: 06-06 본문 §4(L70~L80), DDIA 2판 Ch 6 Summary (PDF p.56) — 쓰기·읽기 경로, 동시성·충돌, 장애 대응(failover), 일관성 수준 비교.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 528
H = LEG + 56

d = D(W, H, "06-06 §4 · REPLICATION SUMMARY MATRIX", "6장 단일 리더·다중 리더·리더리스 종합 비교",
      "복제 방식별 쓰기·읽기 경로, 충돌 처리, 장애 대응, 일관성 보장의 핵심 절충을 한눈에 비교한다.",
      "복제 아키텍처별 요청 경로와 충돌 해소 및 장애 복구 절충")

# 컬럼 기하 (W_AXIS=150, W_COL=220, GAP=10)
X_AXIS = 20
W_AXIS = 150
X_COLS = [180, 410, 640]
W_COL = 220

# 헤더 행 (y=96, h=48)
d.box(X_AXIS, 96, W_AXIS, 48, PAPER2, RULE, 1.0, r=4)
d.t(X_AXIS + W_AXIS / 2, 118, "복제 아키텍처", 13, INK, KR, "middle", 600)
d.t(X_AXIS + W_AXIS / 2, 134, "6장 종합 비교 축", 11, MUTED, KR, "middle")

headers = [
    ("단일 리더 복제", "06-01 ~ 06-03", INFO, False),
    ("다중 리더 복제", "06-04 ~ 06-05", MUTED, False),
    ("리더리스 복제", "06-06", ACC, True),
]

for i, (title, sub, col, is_focal) in enumerate(headers):
    x = X_COLS[i]
    if is_focal:
        d.tone(x, 96, W_COL, 48, ACC, 4, "14", 1.4)
        d.t(x + W_COL / 2, 118, title, 13, ACC, KR, "middle", 600)
        d.t(x + W_COL / 2, 134, sub, 11, ACC, MONO, "middle")
    else:
        d.box(x, 96, W_COL, 48, PAPER2, RULE, 1.0, r=4)
        d.t(x + W_COL / 2, 118, title, 13, INK, KR, "middle", 600)
        d.t(x + W_COL / 2, 134, sub, 11, MUTED, MONO, "middle")

# 데이터 행 5개 (stride = 72)
rows = [
    ("쓰기 경로", "처리 노드", [
        ("지정된 리더 1대", "팔로워로 변경 스트림 전달"),
        ("각 리전별 로컬 리더", "리더 간 비동기 복제 전달"),
        ("임의 레플리카 병렬", "w개 노드 확인으로 성공 판정"),
    ]),
    ("읽기 경로", "질의 노드", [
        ("모든 레플리카 가능", "팔로워 읽기 시 복제 지연 가능"),
        ("로컬 리더·팔로워", "타 리전 쓰기 반영 지연 가능"),
        ("r개 병렬 쿼럼 질의", "stale 감지 시 read repair 보정"),
    ]),
    ("동시성·충돌", "쓰기 충돌", [
        ("한 리더가 모든 쓰기 처리", "쓰기 충돌 없음"),
        ("다중 쓰기 충돌 발생", "LWW · 수동 병합 · CRDT 해소"),
        ("동시 쓰기 siblings 보존", "happens-before · version vector"),
    ]),
    ("장애 대응", "Failover", [
        ("리더 장애 시 failover", "스플릿 브레인 방지 필요"),
        ("리더 단위 독립 처리", "네트워크 단절 중 로컬 수용"),
        ("failover 절차 없음", "read repair · hinted handoff"),
    ]),
    ("일관성 수준", "보장 모델", [
        ("강한 일관성 제공 가능", "이해하기 쉬워 인기"),
        ("약한 일관성", "충돌 해소 필요"),
        ("약한 일관성", "w+r>n 손잡이로 stale 제어"),
    ]),
]

for r_idx, (axis_title, axis_sub, col_data) in enumerate(rows):
    y = 152 + r_idx * 72
    # 축 라벨 셀
    d.box(X_AXIS, y, W_AXIS, 64, PAPER2, RULE, 1.0, r=4)
    d.t(X_AXIS + W_AXIS / 2, y + 28, axis_title, 13, INK, KR, "middle", 600)
    d.t(X_AXIS + W_AXIS / 2, y + 46, axis_sub, 11, MUTED, KR, "middle")

    # 3개 컬럼 셀
    for c_idx, (line1, line2) in enumerate(col_data):
        x = X_COLS[c_idx]
        is_focal = (c_idx == 2)
        if is_focal:
            d.tone(x, y, W_COL, 64, ACC, 4, "0a", 1.2)
            d.t(x + W_COL / 2, y + 26, line1, 12, ACC, KR, "middle", 600)
            d.t(x + W_COL / 2, y + 46, line2, 11, INK, KR, "middle")
        else:
            d.box(x, y, W_COL, 64, PAPER, RULE, 0.8, r=4)
            d.t(x + W_COL / 2, y + 26, line1, 12, INK, KR, "middle")
            d.t(x + W_COL / 2, y + 46, line2, 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("단일 리더·다중 리더", MUTED),
    ("리더리스 (focal)", ACC)
])
d.save("06-06.replication-summary.svg")
