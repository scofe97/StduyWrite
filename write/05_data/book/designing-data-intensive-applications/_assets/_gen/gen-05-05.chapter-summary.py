# 05-05 §4 — 5장 인코딩 형식과 데이터플로우 모드 종합 비교 행렬.
# 사실 출처: 05-05 본문 §4(L85~L93) · 05-04 §1(L33~L41)·§2(L54)·§3(L59~L67, L75) · 05-05 §2(L61)·§3(L74), 원서 Summary(PDF p.32) — 언어 특정·텍스트·스키마 이진 인코딩, DB·RPC/REST·이벤트 기반 3대 데이터플로우, backward/forward 호환성, 롤링 업그레이드.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 452
H = LEG + 56

d = D(W, H, "05-05 §4 · CHAPTER SUMMARY MATRIX", "5장 인코딩과 데이터플로우 종합 비교",
      "데이터베이스, RPC/REST, 이벤트 기반 아키텍처의 인코딩 주체, 주요 형식, 호환성 요구조건, 통신 결합도를 한눈에 비교한다.",
      "프로세스 간 데이터 이동 모드별 인코딩 책임과 롤링 업그레이드 호환성")

# 컬럼 기하 (W_AXIS=150, W_COL=220, GAP=10)
X_AXIS = 20
W_AXIS = 150
X_COLS = [180, 410, 640]
W_COL = 220

# 헤더 행 (y=96, h=48)
d.box(X_AXIS, 96, W_AXIS, 48, PAPER2, RULE, 1.0, r=4)
d.t(X_AXIS + W_AXIS / 2, 118, "데이터플로우", 13, INK, KR, "middle", 600)
d.t(X_AXIS + W_AXIS / 2, 134, "5장 종합 비교 축", 11, MUTED, KR, "middle")

headers = [
    ("데이터베이스 (DB)", "05-04 §1", MUTED, False),
    ("RPC · REST API", "05-04 §2 · §3", MUTED, False),
    ("이벤트 기반 (브로커·액터)", "05-05 §2 · §3", ACC, True),
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

# 데이터 행 4개 (stride = 72)
rows = [
    ("인코딩 주체", "책임 위치", [
        ("쓰는 프로세스 인코딩", "읽는 프로세스 디코딩"),
        ("클라이언트 요청 인코딩", "서버 응답 디코딩"),
        ("송신자 비동기 인코딩", "수신자 독립 디코딩"),
    ]),
    ("대표 인코딩", "주요 포맷", [
        ("원래 인코딩으로 남음", "다시 쓰기는 지연 처리"),
        ("JSON (OpenAPI)", "Protocol Buffers (gRPC)"),
        ("Protobuf · Avro · JSON", "스키마 레지스트리로 호환 검사"),
    ]),
    ("호환성 요구", "데이터 수명", [
        ("backward + forward", "data outlives code"),
        ("요청 backward · 응답 forward", "서버를 먼저 업데이트할 때"),
        ("미지 필드 보존 주의", "actor 도 forward · backward"),
    ]),
    ("통신 결합도", "송수신 관계", [
        ("저장소를 거쳐 전달", "미래의 나에게 보내는 메시지"),
        ("응답을 기다림", "예측 불가 · 타임아웃 · 가변 지연"),
        ("비동기 · 논리적 분리", "버퍼 · 자동 재전달"),
    ]),
]

for r_idx, (axis_title, axis_sub, col_data) in enumerate(rows):
    y = 152 + r_idx * 72
    # 축 라벨 셀
    d.box(X_AXIS, y, W_AXIS, 64, PAPER2, RULE, 1.0, r=4)
    d.t(X_AXIS + W_AXIS / 2, y + 28, axis_title, 13, INK, KR, "middle", 600)
    d.t(X_AXIS + W_AXIS / 2, y + 46, axis_sub, 12, MUTED, KR, "middle")

    # 3개 컬럼 셀
    for c_idx, (line1, line2) in enumerate(col_data):
        x = X_COLS[c_idx]
        is_focal = (c_idx == 2)
        if is_focal:
            d.tone(x, y, W_COL, 64, ACC, 4, "0a", 1.2)
            d.t(x + W_COL / 2, y + 26, line1, 12, ACC, KR, "middle", 600)
            d.t(x + W_COL / 2, y + 46, line2, 12, INK, KR, "middle")
        else:
            d.box(x, y, W_COL, 64, PAPER, RULE, 0.8, r=4)
            d.t(x + W_COL / 2, y + 26, line1, 12, INK, KR, "middle")
            d.t(x + W_COL / 2, y + 46, line2, 12, MUTED, KR, "middle")

d.legend(LEG, [
    ("DB · RPC/REST (05-04 에서 다룸)", MUTED),
    ("비동기 메시지 분리 (이벤트 기반, 이 노트)", ACC)
])
d.save("05-05.chapter-summary.svg")
