# 13-01 §2 — 단일 데이터베이스(SoR)가 쓰기 순서를 결정하고 CDC 이벤트 로그를 통해 파생 시스템들로 일관되게 전파되는 데이터플로우.
# 사실 출처: 13-01 §1(L31)·§2(L34~L45), DDIA 2판 Ch.13 Reasoning about dataflows(장 PDF p.3) — system-of-record database, CDC applied in the same order, funnel all user input through a single system, state machine replication; 파생 목록(data warehouses·caches or denormalized versions)은 같은 쪽 앞 문단.
# 2026-10-31 검증(cc-ddia-dverify13): 근거 없는 라벨(사용자 입력 정류·커밋 순서 불변 보존·대규모 집계 및 OLAP·인메모리 저지연 읽기 등)을 본문·원서 낱말로 바꿨다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
Y0 = 104
CARD_H = 300
LEG = Y0 + CARD_H + 28
H = LEG + 52

d = D(W, H, "13-01 · §2 REASONING ABOUT DATAFLOWS", "CDC 기반 단일 진실 공급원과 파생 데이터플로우",
      "단일 데이터베이스가 쓰기 전순서를 결정하고 CDC 이벤트 로그를 통해 검색 인덱스·DW·캐시로 일관되게 전파된다.",
      "단일 진실 공급원(SoR) · 쓰기 전순서 결정 · CDC 변경 스트림 · 결정론적 멱등 갱신")

# Stage coordinates
S1_X, S1_W = 24, 154
S2_X, S2_W = 200, 186
S3_X, S3_W = 406, 196
S4_X, S4_W = 622, 234

# Stage 1: 클라이언트 쓰기 (요청 유입)
d.box(S1_X, Y0, S1_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S1_X + 26, Y0 + 20, "요청", WARN, 11, pad=4)
d.t(S1_X + 88, Y0 + 24, "클라이언트", 12, INK, KR, "middle", 600)
d.line(S1_X + 10, Y0 + 38, S1_X + S1_W - 10, Y0 + 38, RULE, 0.6)
d.t(S1_X + S1_W / 2, Y0 + 54, "단일 유입 경로", 11, SOFT, KR, "middle")

d.box(S1_X + 10, Y0 + 76, S1_W - 20, 90, PAPER, RULE, 0.8)
d.t(S1_X + S1_W / 2, Y0 + 104, "두 곳 직접 쓰기 (피함)", 12, INK, KR, "middle", 600)
d.t(S1_X + S1_W / 2, Y0 + 128, "Figure 12-4 문제", 11, WARN, KR, "middle")
d.t(S1_X + S1_W / 2, Y0 + 148, "두 시스템 영구 불일치", 11, MUTED, KR, "middle")

d.box(S1_X + 10, Y0 + 180, S1_W - 20, 96, PAPER, RULE, 0.8)
d.t(S1_X + S1_W / 2, Y0 + 208, "모든 사용자 입력", 12, INK, KR, "middle", 600)
d.t(S1_X + S1_W / 2, Y0 + 232, "한 시스템으로 모음", 11, MUTED, KR, "middle")
d.t(S1_X + S1_W / 2, Y0 + 254, "쓰기 순서 한 곳에서 결정", 11, MUTED, KR, "middle")

# Stage 1 -> Stage 2 Arrow
d.arrow([(S1_X + S1_W, Y0 + 121), (S2_X - 2, Y0 + 121)], WARN, "warn", 1.3)
d.t(S1_X + S1_W + (S2_X - S1_X - S1_W) / 2, Y0 + 112, "쓰기", 11, WARN, KR, "middle", 600)

# Stage 2: 원본 데이터베이스 (System of Record)
d.box(S2_X, Y0, S2_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S2_X + 26, Y0 + 20, "SoR", INFO, 11, pad=4)
d.t(S2_X + 102, Y0 + 24, "원본 데이터베이스", 12, INK, KR, "middle", 600)
d.line(S2_X + 10, Y0 + 38, S2_X + S2_W - 10, Y0 + 38, RULE, 0.6)
d.t(S2_X + S2_W / 2, Y0 + 54, "쓰기 전순서 결정 주체", 11, INFO, KR, "middle", 600)

d.box(S2_X + 10, Y0 + 76, S2_W - 20, 90, PAPER, RULE, 0.8)
d.t(S2_X + S2_W / 2, Y0 + 104, "모든 쓰기 순서 결정", 12, INK, KR, "middle", 600)
d.t(S2_X + S2_W / 2, Y0 + 128, "OLTP 트랜잭션 커밋", 11, MUTED, KR, "middle")
d.t(S2_X + S2_W / 2, Y0 + 148, "PostgreSQL 등 저장소", 11, MUTED, KR, "middle")

d.box(S2_X + 10, Y0 + 180, S2_W - 20, 96, PAPER, RULE, 0.8)
d.t(S2_X + S2_W / 2, Y0 + 208, "유일한 입력 지점", 12, INK, KR, "middle", 600)
d.t(S2_X + S2_W / 2, Y0 + 232, "DB 쓰기 = 새 입력", 11, INFO, KR, "middle")
d.t(S2_X + S2_W / 2, Y0 + 254, "변경 캡처 대상", 11, MUTED, KR, "middle")

# Stage 2 -> Stage 3 Arrow
d.arrow([(S2_X + S2_W, Y0 + 228), (S3_X - 2, Y0 + 228)], ACC, "acc", 1.3)
d.t(S2_X + S2_W + (S3_X - S2_X - S2_W) / 2, Y0 + 219, "CDC", 11, ACC, MONO, "middle", 600)

# Stage 3: CDC & 이벤트 로그
S3_X, S3_W = 406, 196
d.tone(S3_X, Y0, S3_W, CARD_H, ACC, 6, "14", 1.4)
d.chip(S3_X + 32, Y0 + 20, "스트림", ACC, 11, pad=4)
d.t(S3_X + 114, Y0 + 24, "CDC & 이벤트 로그", 12, ACC, KR, "middle", 600)
d.line(S3_X + 10, Y0 + 38, S3_X + S3_W - 10, Y0 + 38, RULE, 0.6)
d.t(S3_X + S3_W / 2, Y0 + 54, "순서 보존 변경 스트림", 11, INK, KR, "middle")

d.box(S3_X + 10, Y0 + 76, S3_W - 20, 90, PAPER, ACC, 0.9)
d.t(S3_X + S3_W / 2, Y0 + 104, "변경 캡처", 12, INK, KR, "middle", 600)
d.t(S3_X + S3_W / 2, Y0 + 128, "SoR 변경을 같은 순서로", 11, ACC, KR, "middle")
d.t(S3_X + S3_W / 2, Y0 + 148, "검색 인덱스에 적용", 11, MUTED, KR, "middle")

d.box(S3_X + 10, Y0 + 180, S3_W - 20, 96, PAPER, RULE, 0.8)
d.t(S3_X + S3_W / 2, Y0 + 208, "CDC 또는 이벤트 소싱 로그", 12, INK, KR, "middle", 600)
d.t(S3_X + S3_W / 2, Y0 + 232, "상태 기계 복제 응용", 11, INK, KR, "middle")
d.t(S3_X + S3_W / 2, Y0 + 254, "전순서를 한 곳에서", 11, OK, KR, "middle")

# Stage 4: 파생 시스템 (Derivations)
S4_X, S4_W = 622, 234
d.box(S4_X, Y0, S4_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S4_X + 26, Y0 + 20, "파생", OK, 11, pad=4)
d.t(S4_X + 114, Y0 + 24, "파생 시스템 목록", 12, INK, KR, "middle", 600)
d.line(S4_X + 10, Y0 + 38, S4_X + S4_W - 10, Y0 + 38, RULE, 0.6)
d.t(S4_X + S4_W / 2, Y0 + 54, "동일 순서 비동기 반영", 11, OK, KR, "middle")

# 3 Consumer Boxes
consumers = [
    ("검색 인덱스", "Elasticsearch 전문 검색", 102),
    ("분석 웨어하우스", "분석 시스템 사본", 166),
    ("캐시", "비정규화 사본", 230),
]

for title, sub, cy in consumers:
    d.box(S4_X + 10, Y0 + cy - 26, S4_W - 20, 52, PAPER, OK, 0.8)
    d.t(S4_X + 22, Y0 + cy - 6, title, 12, INK, KR, "start", 600)
    d.t(S4_X + 22, Y0 + cy + 12, sub, 11, MUTED, KR, "start")

# Fan-out arrows from Stage 3 to Stage 4 (Manhattan routing)
out_x = S3_X + S3_W
in_x = S4_X
for _, _, cy in consumers:
    target_y = Y0 + cy
    d.arrow([(out_x, Y0 + 208), (out_x + 10, Y0 + 208), (out_x + 10, target_y), (in_x - 2, target_y)], OK, "ok", 1.2)

d.t(S4_X + S4_W / 2, Y0 + 282, "결정론적 재처리 + 멱등 갱신", 11, OK, KR, "middle", 600)

d.legend(LEG, [
    ("복제 스트림 (focal)", ACC),
    ("단일 순서 결정 (SoR)", INFO),
    ("파생 시스템 갱신", OK),
    ("클라이언트 유입", WARN),
])

d.save("13-01.derived-dataflow.svg")
