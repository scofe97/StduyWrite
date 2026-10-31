# 07-04 §4 — 7장 종합: 두 샤딩 축(키 범위·해시)을 같은 네 속성으로 견주고, 세 운영 과제와 8장 연결을 아래 띠로 둔다.
# 사실 출처: 07-04 본문 §4 — 두 샤딩 축 L76~L78, 세 운영 과제 L82~L86, 8장 연결 L88.
#   격자는 두 축에만 쓴다(같은 속성을 두 경우에 견주는 것이 L76~L78 의 논지). 세 과제는 속성이 서로 달라 격자에 넣지 않는다.
# 타입 스펙: type-dp-security-matrix (이 저장소에서 비교 격자로 쓰는 타입)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

W = 880
# 세로 배치: 격자 머리 96~136, 행 4개(행 간격 46) 144~322, 과제 띠 350~426, 8장 띠 444~480, 범례 512
LEG = 512
H = LEG + 56

d = D(W, H, "07-04 §4 · CHAPTER 7 SUMMARY", "7장 종합 — 두 샤딩 축과 세 과제",
      "두 샤딩 축(키 범위·해시)을 같은 속성으로 견주고, 세 운영 과제(라우팅·리밸런싱·보조 인덱스)와 8장 연결을 보인다.",
      "키 범위 vs 해시 · 라우팅 · 리밸런싱 · 보조 인덱스 · 8장")

# ── 위: 두 샤딩 축 격자 (속성 열 + 두 축 열)
X_AXIS, W_AXIS = 24, 160
X_COLS = [196, 530]
W_COL = 322
HY, HH = 96, 40

d.box(X_AXIS, HY, W_AXIS, HH, PAPER2, RULE, 1.0, r=4)
d.t(X_AXIS + W_AXIS / 2, HY + 25, "두 샤딩 축", 13, INK, KR, "middle", 600)
for x, title in zip(X_COLS, ["키 범위 샤딩", "해시 샤딩"]):
    d.tone(x, HY, W_COL, HH, INFO, 4, "18", 1.2)
    d.t(x + W_COL / 2, HY + 25, title, 13, INK, KR, "middle", 600)

rows = [
    ("키 배치", ["정렬 유지", "균등 분산"]),
    ("범위 쿼리", ["범위 쿼리에 강함", "불가 · 복합 키 두 번째 열부터 가능"]),
    ("핫스팟", ["인접 키 쓰기 집중 시 발생", "균등 분산으로 줄어듦"]),
    ("조치", ["핫스팟 해소: 복합 키 순서 조정 · 샤드 분할", "리밸런싱: 고정 샤드 수 · 해시 범위 · 일관 해싱"]),
]
RY0, RH, RS = HY + HH + 8, 40, 46
for i, (attr, cells) in enumerate(rows):
    y = RY0 + i * RS
    d.box(X_AXIS, y, W_AXIS, RH, PAPER2, RULE, 1.0, r=4)
    d.t(X_AXIS + W_AXIS / 2, y + 25, attr, 12, MUTED, KR, "middle", 600)
    for x, c in zip(X_COLS, cells):
        d.box(x, y, W_COL, RH, PAPER, RULE, 0.8, r=4)
        d.t(x + W_COL / 2, y + 25, c, 12, INK, KR, "middle")

# ── 아래: 세 운영 과제 띠
BY = RY0 + 3 * RS + RH + 28
d.t(X_AXIS, BY - 10, "세 운영 과제", 12, WARN, KR, "start", 600)
CW, CG = 264, 18
CH = 76
tasks = [
    ("라우팅", "클라이언트 · 라우팅 티어 · 임의 노드", "ZooKeeper · etcd · 내장 Raft 매핑"),
    ("리밸런싱", "자동: 연쇄 과부하 위험", "수동: 예측 가능하지만 느림"),
    ("보조 인덱스", "로컬: 쓰기 단순 · 읽기 fan-out", "글로벌: 읽기 효율 · 쓰기 복잡"),
]
for i, (title, l1, l2) in enumerate(tasks):
    x = X_AXIS + i * (CW + CG)
    d.box(x, BY, CW, CH, PAPER2, WARN, 1.1, r=4)
    d.t(x + CW / 2, BY + 22, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, BY + 44, l1, 11, SOFT, KR, "middle")
    d.t(x + CW / 2, BY + 64, l2, 11, SOFT, KR, "middle")

# ── 8장 연결
EY = BY + CH + 18
EW = 3 * CW + 2 * CG
d.tone(X_AXIS, EY, EW, 36, ACC, 4, "18", 1.2)
d.t(X_AXIS + EW / 2, EY + 23, "8장 · 여러 샤드 동시 변경 → 분산 트랜잭션", 12, ACC, KR, "middle", 600)

assert EY + 36 + 32 == LEG, EY
d.legend(LEG, [("두 샤딩 축", INFO), ("세 운영 과제", WARN), ("8장 연결", ACC)])
d.save("07-04.chapter-summary.svg")
