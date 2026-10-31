# 10-01 §5 — 복제 방법별 선형성(최신성 보장) 달성 가능 여부와 핵심 제약 비교.
# 사실 출처: 10-01 §5(L86~L96), DDIA 2판 Ch.10 Implementing Linearizable Systems(PDF p.11~14)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 250
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "10-01 · §5 REPLICATION & LINEARIZABILITY", "복제 방법별 선형화 가능성 비교",
      "합의 알고리즘, 단일 리더, 다중 리더, 리더리스 복제의 선형성 보장 여부와 제약.",
      "쿼럼 합의 보장 · 단일 리더 한계 · 다중 리더 충돌 · 리더리스 쿼럼 역전")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "복제 방법별 선형화 비교: 알고리즘별 선형성 보장 여부와 핵심 위험", 12, INK, KR, "middle", 600)

CW = 196
GAP = 14
X0 = 28

cards = [
    ("합의 알고리즘", "Raft · Zab (etcd, ZK)", "선형화 가능", OK,
     [("과반수 투표 커밋", "쿼럼 합의 기반 쓰기 처리"),
      ("스플릿 브레인 방지", "좀비 리더 차단"),
      ("리더 lease 검증", "읽기 시 stale read 방지")]),
    ("단일 리더 복제", "리더에서만 처리", "잠재적 가능", WARN,
     [("리더 읽기·쓰기", "리더에서만 처리 시 선형화"),
      ("비동기 유실 위험", "페일오버 시 커밋 쓰기 유실"),
      ("좀비 리더 위험", "분단 시 구 값 응답 가능")]),
    ("다중 리더 복제", "여러 노드 동시 쓰기", "선형화 불가", BAD,
     [("독립 노드 쓰기", "같은 객체 충돌 쓰기"),
      ("단일 포인트 부재", "선형화 기준점 성립 불가"),
      ("충돌 해소 한계", "LWW 적용 시 이미 포기")]),
    ("리더리스 복제", "Dynamo 스타일", "불가 가능성 높음", BAD,
     [("쿼럼 읽기·쓰기", "w + r > n 조건 사용"),
      ("클럭 스큐 위험", "최근 쓰기가 낮은 타임스탬프"),
      ("동시 읽기 역전", "진행 중 쓰기 구·신값 혼재")]),
]

for idx, (title, sub, status, status_c, items) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 상태 칩 + 제목 + 부제목
    d.chip(x + CW / 2, y + 20, status, status_c, 11)
    d.t(x + CW / 2, y + 44, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, y + 62, sub, 11, SOFT, KR, "middle")

    d.line(x + 12, y + 74, x + CW - 12, y + 74, RULE, 0.8)

    # 3개 항목 박스
    iy0 = y + 96
    for i_idx, (head, desc) in enumerate(items):
        iy = iy0 + i_idx * 48
        d.box(x + 10, iy - 14, CW - 20, 42, PAPER, RULE, 0.6)
        d.t(x + CW / 2, iy + 2, head, 12, INK, KR, "middle", 600)
        d.t(x + CW / 2, iy + 18, desc, 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("선형화 가능", OK),
    ("잠재적 가능 (조건부)", WARN),
    ("선형화 불가·위험", BAD),
    ("구조·원리", INFO),
])

d.save("10-01.replication-linearizability.svg")
