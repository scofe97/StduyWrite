# 07-02 개요 — 해시 샤딩의 균등 분산과 세 가지 재배치 전략(고정 샤드·해시 범위·일관 해싱), 핫 키 완화 전체 지도.
# 사실 출처: 07-02 서두(L14~L16), §1(L23~L28), §2(L35~L40), §3(L47~L52), §4(L61~L70), §5(L75~L86), §6(L89~L94)
# 원서: DDIA 2판 7장 p.10~17 (Sharding by Hash of Key ~ Skewed Workloads). 2026-10-31 검증: §5 색이 §1 범례 색과 겹쳐 대안 셋을 한 색으로 묶음,
#   '100개 샤드 병렬 조회'(원서·본문은 100개 키) · '토큰 범위'(본문 용어 아님) · '75%'(본문은 '대부분') 수정
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 280
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "07-02 · CHAPTER OVERVIEW", "해시 샤딩과 일관 해싱 전체 지도",
      "해시 균등 분산(§1), mod N 문제와 세 대안(§2~§5), 핫 키 우회(§6)를 절 순서로 놓은 지도.",
      "해시 함수 균등 분산 · mod N 문제와 세 대안(고정 샤드·해시 범위·일관 해싱) · 핫 키 분할")

# 상단 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "목표: 키 범위 샤딩의 핫스팟을 완화하고 노드 추가·제거 시 재배치 비용을 최소화", 12, INK, KR, "middle", 600)

# Card 0: §1
X0 = 28; CW0 = 250
d.box(X0, PY, CW0, PH, PAPER2, RULE, 0.9)
d.chip(X0 + 32, PY + 22, "§1", INFO, 11)
d.t(X0 + CW0 / 2 + 16, PY + 26, "해시 함수로 균등 분산", 13, INK, KR, "middle", 600)
d.t(X0 + CW0 / 2, PY + 46, "파티션 키의 해시 공간 사상", 12, SOFT, KR, "middle")
d.line(X0 + 12, PY + 56, X0 + CW0 - 12, PY + 56, RULE, 0.8)

c0_items = [
    ("32비트 균등 분포", "0 ~ 2³²−1 공간으로 사상", INFO),
    ("샤딩용 해시 함수", "MD5 · Murmur3", MUTED),
    ("프로세스마다 같은 값", "Java hashCode() 부적합", MUTED),
]
for j, (top_t, bot_t, col) in enumerate(c0_items):
    iy = PY + 68 + j * 66
    if col == INFO:
        d.tone(X0 + 12, iy, CW0 - 24, 54, INFO, 6, "18", 1.1)
        d.t(X0 + CW0 / 2, iy + 22, top_t, 12, INK, KR, "middle", 600)
        d.t(X0 + CW0 / 2, iy + 40, bot_t, 12, INFO, KR, "middle")
    else:
        d.box(X0 + 12, iy, CW0 - 24, 54, PAPER, RULE, 0.8)
        d.t(X0 + CW0 / 2, iy + 22, top_t, 12, INK, KR, "middle", 600)
        d.t(X0 + CW0 / 2, iy + 40, bot_t, 12, MUTED, KR, "middle")

# Card 1: §2~§5 (FOCAL)
X1 = 298; CW1 = 284
d.box(X1, PY, CW1, PH, PAPER2, ACC, 1.4)
d.chip(X1 + 42, PY + 22, "§2~§5", ACC, 11)
d.t(X1 + CW1 / 2 + 20, PY + 26, "mod N 문제와 세 대안", 13, INK, KR, "middle", 600)
d.t(X1 + CW1 / 2, PY + 46, "노드 추가·제거 때 키 이동량", 12, SOFT, KR, "middle")
d.line(X1 + 12, PY + 56, X1 + CW1 - 12, PY + 56, RULE, 0.8)

c1_items = [
    ("§2 mod N 방식의 문제", "노드 수 변경 시 대부분 키 이동", MUTED),
    ("§3 고정 샤드 수 (Citus)", "샤드 단위 이전 · 키 매핑 불변", ACC),
    ("§4 해시 범위 (DynamoDB)", "연속 해시 범위 · 범위 분할", ACC),
    ("§5 일관 해싱 (Cassandra)", "샤드 수 변경 시 최소 키 이동", ACC),
]
for j, (top_t, bot_t, col) in enumerate(c1_items):
    iy = PY + 66 + j * 50
    if col == ACC:
        d.tone(X1 + 12, iy, CW1 - 24, 42, ACC, 6, "22", 1.3)
        d.t(X1 + CW1 / 2, iy + 18, top_t, 12, INK, KR, "middle", 600)
        d.t(X1 + CW1 / 2, iy + 33, bot_t, 12, ACC, KR, "middle")
    else:
        d.box(X1 + 12, iy, CW1 - 24, 42, PAPER, RULE, 0.8)
        d.t(X1 + CW1 / 2, iy + 18, top_t, 12, INK, KR, "middle", 600)
        d.t(X1 + CW1 / 2, iy + 33, bot_t, 12, MUTED, KR, "middle")

# Card 2: §6
X2 = 602; CW2 = 250
d.box(X2, PY, CW2, PH, PAPER2, RULE, 0.9)
d.chip(X2 + 32, PY + 22, "§6", WARN, 11)
d.t(X2 + CW2 / 2 + 16, PY + 26, "핫 키 애플리케이션 우회", 13, INK, KR, "middle", 600)
d.t(X2 + CW2 / 2, PY + 46, "특정 키 집중 부하 분산", 12, SOFT, KR, "middle")
d.line(X2 + 12, PY + 56, X2 + CW2 - 12, PY + 56, RULE, 0.8)

c2_items = [
    ("특정 키 집중 한계", "해시 균등성으로 미해결", MUTED),
    ("2자리 난수 붙이기", "100개 키로 쓰기 분산", WARN),
    ("읽기 때 합산", "100개 키 모두 조회", MUTED),
]
for j, (top_t, bot_t, col) in enumerate(c2_items):
    iy = PY + 68 + j * 66
    if col == WARN:
        d.tone(X2 + 12, iy, CW2 - 24, 54, WARN, 6, "18", 1.1)
        d.t(X2 + CW2 / 2, iy + 22, top_t, 12, INK, KR, "middle", 600)
        d.t(X2 + CW2 / 2, iy + 40, bot_t, 12, WARN, KR, "middle")
    else:
        d.box(X2 + 12, iy, CW2 - 24, 54, PAPER, RULE, 0.8)
        d.t(X2 + CW2 / 2, iy + 22, top_t, 12, INK, KR, "middle", 600)
        d.t(X2 + CW2 / 2, iy + 40, bot_t, 12, MUTED, KR, "middle")

# 연결 화살표
d.arrow([(X0 + CW0, PY + PH / 2), (X1, PY + PH / 2)], SOFT, "soft", 1.4)
d.arrow([(X1 + CW1, PY + PH / 2), (X2, PY + PH / 2)], SOFT, "soft", 1.4)

d.legend(LEG, [("재배치 대안", ACC), ("해시 분산 (§1)", INFO), ("핫 키 우회 (§6)", WARN)])
d.save("07-02.chapter-overview.svg")
