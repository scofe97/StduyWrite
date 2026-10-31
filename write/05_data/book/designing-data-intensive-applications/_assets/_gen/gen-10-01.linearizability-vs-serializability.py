# 10-01 §3 — 선형성(최신성 보장)과 직렬화 가능성(트랜잭션 격리)의 2차원 비교 매트릭스.
# 사실 출처: 10-01 §3(L54~L72), DDIA 2판 Ch.10 Linearizability vs Serializability(PDF p.9~10)
# 타입 스펙: type-quadrant
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 506
H = LEG + 52

d = D(W, H, "10-01 · §3 SERIALIZABILITY VS LINEARIZABILITY", "선형성과 직렬화 가능성 2차원 비교 매트릭스",
      "단일 객체 최신성을 보장하는 선형성과 다중 객체 트랜잭션 격리를 보장하는 직렬화 가능성의 4분면 체계.",
      "단일 객체 vs 다중 객체 · 실제 시간 순서 vs 임의 직렬 순서 · 엄격한 직렬화 · 시스템별 조합")

# 축 안내 라벨
d.t(W / 2, 94, "▲ 직렬화 가능성 보장 (다중 객체 트랜잭션 격리)", 11, INFO, KR, "middle", 600)
d.t(W / 2, 420, "▼ 직렬화 가능성 미보장", 11, SOFT, KR, "middle")
d.t(844, 254, "선형성 보장 ▶", 11, OK, KR, "end", 600)
d.t(36, 254, "◀ 선형성 미보장", 11, SOFT, KR, "start")

# 중앙 십자 분할선 (라벨 닿지 않게 여유 간격)
d.line(W / 2, 104, W / 2, 404, RULE, 1.2)
d.line(144, 254, W - 144, 254, RULE, 1.2)

# 1. Top-Right (Q1): 엄격한 직렬화 (Strict Serializability)
d.tone(454, 106, 390, 126, OK, 6, "18", 1.2)
d.t(470, 128, "엄격한 직렬화 (Strict Serializability)", 13, OK, KR, "start", 600)
d.t(470, 146, "선형성 + 직렬성 동시 보장 (strong-1SR)", 11, MUTED, KR, "start")
d.t(470, 170, "• 실제 시간 순서와 직렬 순서 일치", 11, INK, KR, "start")
d.t(470, 190, "• 최신성 보장 및 쓰기 스큐 방지", 11, INK, KR, "start")
d.t(470, 212, "• 대표: Spanner · FoundationDB", 11, OK, KR, "start", 600)

# 2. Top-Left (Q2): 직렬화 가능성만 (Serializability Only)
d.tone(36, 106, 390, 126, INFO, 6, "14", 1.0)
d.t(52, 128, "직렬화 가능성만 제공 (Serializability Only)", 13, INFO, KR, "start", 600)
d.t(52, 146, "다중 객체 트랜잭션 격리 보장", 11, MUTED, KR, "start")
d.t(52, 170, "• 임의 직렬 순서 실행 보장", 11, INK, KR, "start")
d.t(52, 190, "• 과거 스냅샷 읽기 허용", 11, INK, KR, "start")
d.t(52, 212, "• 대표: CockroachDB 기본 설정", 11, INFO, KR, "start", 600)

# 3. Bottom-Right (Q3): 선형성만 (Linearizability Only)
d.tone(454, 274, 390, 126, WARN, 6, "14", 1.0)
d.t(470, 296, "선형성만 제공 (Linearizability Only)", 13, WARN, KR, "start", 600)
d.t(470, 314, "단일 객체 최신성 보장 (recency guarantee)", 11, MUTED, KR, "start")
d.t(470, 338, "• 단일 키 읽기·쓰기·CAS 최신성", 11, INK, KR, "start")
d.t(470, 358, "• 트랜잭션 격리 없음", 11, INK, KR, "start")
d.t(470, 380, "• 실제 시간 순서 준수", 11, WARN, KR, "start", 600)

# 4. Bottom-Left (Q4): 둘 다 없음 (Eventual Consistency)
d.tone(36, 274, 390, 126, BAD, 6, "14", 1.0)
d.t(52, 296, "둘 다 없음 (최종 일관성 / 약한 격리)", 13, BAD, KR, "start", 600)
d.t(52, 314, "성능을 위해 둘 다 포기", 11, MUTED, KR, "start")
d.t(52, 338, "• 트랜잭션 및 최신성 미보장", 11, INK, KR, "start")
d.t(52, 358, "• 동시 쓰기 충돌 · 지연 노출", 11, INK, KR, "start")
d.t(52, 380, "• 최종 일관성만 제공", 11, BAD, KR, "start", 600)

# 하단 요약 패널
d.tone(28, 432, W - 56, 48, INFO, 6, "14", 1.0)
d.t(W / 2, 452, "선형성은 단일 객체 최신성 보장, 직렬화는 다중 객체 트랜잭션 격리", 12, INK, KR, "middle", 600)
d.t(W / 2, 470, "두 차원 동시 만족 = 엄격한 직렬화 (가장 강한 보장)", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("엄격한 직렬화 (focal)", OK),
    ("직렬성만", INFO),
    ("선형성만", WARN),
    ("최종 일관성", BAD),
])

d.save("10-01.linearizability-vs-serializability.svg")
