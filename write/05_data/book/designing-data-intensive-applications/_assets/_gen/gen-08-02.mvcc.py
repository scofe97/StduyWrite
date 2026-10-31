# 08-02 §3 — PostgreSQL 방식의 MVCC 다중 버전 행 구조(inserted_by, deleted_by)와 트랜잭션 txid 기반 스냅샷 가시성 판정.
# 사실 출처: 08-02 본문 §3(L50~L60), 원서 Ch.8 p.21 Figure 8-7 ("Implementing snapshot isolation using multiversion concurrency control")
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
H = 556
LEG = H - 56

d = D(W, H, "08-02 · §3 MVCC ROW VERSIONS", "MVCC 다중 버전 행 구조와 스냅샷 가시성",
      "각 행의 inserted_by와 deleted_by 필드를 대조해 시작 시점 스냅샷을 선별한다.",
      "txid 태깅 · inserted_by · deleted_by · 가시성 판정")

# 상단 트랜잭션 컨텍스트 (읽기 txid=12 vs 쓰기 txid=13)
TW = 404
d.box(24, PY, TW, 44, PAPER2, INFO, 1.2)
d.chip(72, PY + 22, "txid = 12", INFO, 11)
d.t(136, PY + 26, "읽기 트랜잭션 (시작 시점 t12 스냅샷 기준)", 12, INK, KR, "start", 600)

d.box(452, PY, TW, 44, PAPER2, ACC, 1.2)
d.chip(500, PY + 22, "txid = 13", ACC, 11)
d.t(564, PY + 26, "이체 쓰기 트랜잭션 (계좌 2 → 계좌 1 100달러)", 12, INK, KR, "start", 600)

# 중앙 accounts 테이블 컨테이너
TY = 160
TH = 260
d.box(24, TY, W - 48, TH, PAPER, RULE, 1.0)
d.tone(36, TY + 12, W - 72, 28, SOFT, 4, "12", 0.8)
d.t(48, TY + 30, "ACCOUNTS 테이블 다중 버전", 11, INK, MONO, "start", 600)
d.t(240, TY + 30, "UPDATE = 구 행 deleted_by 기록 + 신규 행 INSERT", 11, SOFT, KR, "start")

# 계좌 1 블록 (id = 1)
AY1 = TY + 48
d.box(36, AY1, 96, 92, PAPER2, RULE, 0.9)
d.t(84, AY1 + 40, "계좌 1", 12, INK, KR, "middle", 600)
d.t(84, AY1 + 58, "id = 1", 11, MUTED, MONO, "middle")

# 계좌 1: v1 (500달러, 가시)
d.tone(140, AY1, W - 188, 42, OK, 4, "14", 1.1)
d.t(152, AY1 + 18, "inserted_by = 3 · deleted_by = 13 · balance = 500", 11, INK, MONO, "start")
d.t(152, AY1 + 33, "가시: 생성(3 < 12) 완료 · 삭제(13 > 12) 미반영", 11, OK, KR, "start", 600)
d.t(W - 68, AY1 + 25, "가시 (500)", 11, OK, KR, "end", 600)

# 계좌 1: v2 (600달러, 비가시)
d.box(140, AY1 + 50, W - 188, 42, PAPER, RULE, 0.8)
d.t(152, AY1 + 68, "inserted_by = 13 · deleted_by = null · balance = 600", 11, MUTED, MONO, "start")
d.t(152, AY1 + 83, "비가시: 생성(13 > 12) t12 시점 이후 쓰기", 11, SOFT, KR, "start")
d.t(W - 68, AY1 + 75, "비가시", 11, MUTED, KR, "end")

# 계좌 2 블록 (id = 2)
AY2 = TY + 152
d.box(36, AY2, 96, 92, PAPER2, RULE, 0.9)
d.t(84, AY2 + 40, "계좌 2", 12, INK, KR, "middle", 600)
d.t(84, AY2 + 58, "id = 2", 11, MUTED, MONO, "middle")

# 계좌 2: v1 (500달러, 가시)
d.tone(140, AY2, W - 188, 42, OK, 4, "14", 1.1)
d.t(152, AY2 + 18, "inserted_by = 5 · deleted_by = 13 · balance = 500", 11, INK, MONO, "start")
d.t(152, AY2 + 33, "가시: 생성(5 < 12) 완료 · 삭제(13 > 12) 미반영", 11, OK, KR, "start", 600)
d.t(W - 68, AY2 + 25, "가시 (500)", 11, OK, KR, "end", 600)

# 계좌 2: v2 (400달러, 비가시)
d.box(140, AY2 + 50, W - 188, 42, PAPER, RULE, 0.8)
d.t(152, AY2 + 68, "inserted_by = 13 · deleted_by = null · balance = 400", 11, MUTED, MONO, "start")
d.t(152, AY2 + 83, "비가시: 생성(13 > 12) t12 시점 이후 쓰기", 11, SOFT, KR, "start")
d.t(W - 68, AY2 + 75, "비가시", 11, MUTED, KR, "end")

# 하단 일관성 확인 배너
BY = TY + TH + 12
d.tone(24, BY, W - 48, 36, OK, 4, "16", 1.2)
d.t(W / 2, BY + 23, "txid = 12 읽기 결과: 계좌 1 $500 + 계좌 2 $500 = 총액 $1,000 일관 스냅샷 유지", 12, INK, KR, "middle", 600)

d.legend(LEG, [("가시 버전 (focal)", OK), ("비가시 미래 버전", MUTED), ("쓰기 트랜잭션", ACC), ("읽기 트랜잭션", INFO)])
d.save("08-02.mvcc.svg")
