# 타입 스펙: type-data-flow — 지역 이름 변경 시 비정규화의 다수 행 갱신 경로와 정규화의 단일 행 갱신 경로를 비교하는 데이터 흐름도.
# 사실 출처: region_id 값 "us:91" 은 원서 Example 3-1. 새 이름은 값을 지어내지 않고 "새 이름" 으로 둔다.
# 노트 L33~L57(§1 정규화와 ID 참조: 평문 "Washington, DC" vs region_id, 이름이 바뀔 때 한 곳만 수정 vs 복제 사본 갱신 불일치 위험, SELECT users.*, regions.region_name FROM users JOIN regions ON users.region_id = regions.id)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, PAPER, PAPER2, KR, MONO

W = 880
PY, PH = 104, 308
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "03-02 · §1 ID REFERENCE", "이름 변경 시 ID 참조와 복제 저장의 갱신 경로",
      "지역 이름이 바뀔 때 비정규화는 모든 사용자 행의 텍스트를 갱신해야 하고 불일치 위험이 따르지만, 정규화는 지역 엔티티 한 곳만 갱신하고 불변 ID 참조는 그대로 유지된다.",
      "왼쪽은 사본 다수 갱신과 불일치 위험, 오른쪽은 단 1곳 갱신과 불변 ID를 통한 일관성 보장입니다.")

# 좌우 패널 분할 (각 폭 416)
d.box(16, PY, 416, PH, PAPER, WARN, 1.2)
d.box(448, PY, 416, PH, PAPER, ACC, 1.4)

d.t(32, PY + 28, "비정규화 — 텍스트 복제 저장", 14, INK, KR, "start", 600)
d.t(32, PY + 46, "각 사용자 행마다 지역명 문자열 직접 저장", 11, MUTED, KR, "start")

d.t(464, PY + 28, "정규화 — ID 참조와 단일 저장", 14, INK, KR, "start", 600)
d.t(464, PY + 46, "사람에게 의미 있는 정보는 한 곳만 저장", 11, MUTED, KR, "start")

# === 좌측: 비정규화 흐름 ===
# 상단 변경 요청
d.box(32, PY + 64, 384, 36, PAPER2, WARN, 1.0)
d.t(48, PY + 86, "지역 이름 변경 → 새 이름", 12, WARN, KR, "start", 600)

# 갱신 화살표 분기
d.arrow([(224, PY + 100), (224, PY + 120)], WARN, "warn", 1.4)
d.line(96, PY + 120, 352, PY + 120, WARN, 1.2)
d.arrow([(96, PY + 120), (96, PY + 138)], WARN, "warn", 1.2)
d.arrow([(224, PY + 120), (224, PY + 138)], WARN, "warn", 1.2)
d.arrow([(352, PY + 120), (352, PY + 138)], WARN, "warn", 1.2)

# 사용자 행 3개
users_denorm = [
    ("users · 251", "region: \"새 이름\"", "갱신함", WARN),
    ("users · 다른 행", "region: \"새 이름\"", "갱신함", WARN),
    ("users · 다른 행", "region: \"Washington, DC\"", "누락 · 불일치", BAD),
]

for i, (title, val, status, col) in enumerate(users_denorm):
    uy = PY + 144 + i * 44
    d.box(32, uy, 384, 36, PAPER2, RULE, 0.9)
    d.t(44, uy + 17, title, 11, INK, KR, "start", 600)
    d.t(44, uy + 30, val, 11, MUTED, KR, "start")
    # 우측 칩: 상자 내부 (32 + 384 = 416, 칩 너비 고려 cx=356)
    d.chip(356, uy + 18, status, col, 11, pad=5)

# 하단 결과 요약
d.box(32, PY + 280, 384, 20, PAPER2, WARN, 0.8)
d.t(224, PY + 294, "모든 사본 갱신 필요 · 쓰기 비용 증가 · 불일치 위험", 11, WARN, KR, "middle", 600)

# === 우측: 정규화 흐름 ===
# 상단 변경 요청
d.box(464, PY + 64, 384, 36, PAPER2, ACC, 1.0)
d.t(480, PY + 86, "지역 이름 변경 → 새 이름", 12, ACC, KR, "start", 600)

# 단 1곳 갱신 화살표
d.arrow([(656, PY + 100), (656, PY + 120)], OK, "ok", 1.4)

# regions 테이블 단 1행
d.box(464, PY + 120, 384, 40, PAPER2, OK, 1.2)
d.t(476, PY + 138, "regions · id \"us:91\"", 11, INK, KR, "start", 600)
d.t(476, PY + 152, "region_name: \"새 이름\"", 11, OK, KR, "start")
d.chip(776, PY + 140, "단 1곳만 갱신", OK, 11, pad=5)

# 아래 users 행들과의 조인 참조 관계 안내
d.t(656, PY + 174, "조인으로 최신 이름 조회 (JOIN regions)", 11, MUTED, KR, "middle")

users_norm = [
    ("users · 251", "region_id: \"us:91\"", "ID 불변", OK),
    ("users · 다른 행", "region_id: \"us:91\"", "ID 불변", OK),
    ("users · 다른 행", "region_id: \"us:91\"", "ID 불변", OK),
]

for i, (title, val, status, col) in enumerate(users_norm):
    uy = PY + 186 + i * 29
    d.box(464, uy, 384, 25, PAPER2, RULE, 0.8)
    d.t(476, uy + 17, title, 11, INK, KR, "start")
    d.t(620, uy + 17, val, 11, MUTED, KR, "start")
    d.chip(788, uy + 12, status, col, 11, pad=5)

# 하단 결과 요약
d.box(464, PY + 280, 384, 20, PAPER2, OK, 0.8)
d.t(656, PY + 294, "단 1곳만 갱신 · 불변 ID 참조 유지로 일관성 보장", 11, OK, KR, "middle", 600)

d.legend(LEG, [
    ("핵심 — 정규화 ID 참조", ACC),
    ("단 1곳 갱신 · 일관성", OK),
    ("복제 사본 · 갱신 비용", WARN),
    ("불일치 결함", BAD)
])

d.save("03-02.id-reference.svg")
