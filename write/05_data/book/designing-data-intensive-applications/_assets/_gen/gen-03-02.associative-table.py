# 타입 스펙: type-er — 다대다 관계를 연관 테이블(positions)과 양방향 보조 인덱스로 표현하는 ER 개념도.
# 사실 출처: user_id 251·first_name·region_id "us:91"·org_id 513·job_title 은 원서 Example 3-1·3-2, 조직의 name·logo URL 은 원서 §Normalization(값은 원서에 없어 이름만 둔다).
# 노트 L90~L116(§3 다대일·다대다 관계: 이력서 positions 1:N, region_id 다대일, 조직 엔티티 다대다, 연관 테이블, user ID와 org ID 연결, 양방향 쿼리를 위한 user_id·org_id 양쪽 보조 인덱스)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W = 880
EY, EH = 108, 172
EW = 224
X_USR = 24
X_POS = 328
X_ORG = 632
QY = EY + EH + 20
QH = 96
LEG = QY + QH + 28
H = LEG + 56

d = D(W, H, "03-02 · §3 ASSOCIATIVE TABLE", "다대다 관계의 연관 테이블과 양방향 인덱스",
      "다대다 관계는 자족적 문서에 들어가지 않아 연관 테이블(positions)로 관계를 한 곳에만 저장하고, user_id와 org_id 양쪽 보조 인덱스로 양방향 쿼리를 지원한다.",
      "가운데 연관 테이블이 관계를 한 곳에만 모으고, 양쪽 보조 인덱스가 양방향 탐색을 지원합니다.")

# 1. users 엔티티
d.box(X_USR, EY, EW, EH, PAPER2, RULE, 1.0)
d.box(X_USR, EY, EW, 36, PAPER, RULE, 0.8)
d.t(X_USR + 14, EY + 23, "users", 13, INFO, MONO, "start", 600)
d.t(X_USR + EW - 14, EY + 23, "사용자 엔티티", 11, MUTED, KR, "end")
d.line(X_USR, EY + 36, X_USR + EW, EY + 36, RULE, 0.8)

fields_usr = [
    ("# user_id: 251", "PK", OK),
    ("first_name: \"Barack\"", "속성", MUTED),
    ("→ region_id: \"us:91\"", "FK", INFO),
]
for i, (f, tag, tc) in enumerate(fields_usr):
    fy = EY + 48 + i * 28
    d.t(X_USR + 14, fy + 16, f, 11, INK, MONO, "start")
    d.chip(X_USR + EW - 32, fy + 12, tag, tc, 11, pad=4)

# 2. positions 연관 엔티티 (focal ACC)
d.tone(X_POS, EY, EW, EH, ACC, 6, "18", 1.4)
d.box(X_POS, EY, EW, 36, PAPER, ACC, 1.0)
d.t(X_POS + 14, EY + 23, "positions", 13, ACC, MONO, "start", 600)
d.t(X_POS + EW - 14, EY + 23, "연관 엔티티", 11, ACC, KR, "end", 600)
d.line(X_POS, EY + 36, X_POS + EW, EY + 36, ACC, 0.8)

fields_pos = [
    ("# position_id", "PK", OK),
    ("→ user_id: 251", "FK · 인덱스", ACC),
    ("→ org_id: 513", "FK · 인덱스", ACC),
    ("job_title: \"President\"", "속성", MUTED),
]
for i, (f, tag, tc) in enumerate(fields_pos):
    fy = EY + 48 + i * 28
    d.t(X_POS + 14, fy + 16, f, 11, INK, MONO, "start")
    cx = X_POS + EW - 52 if "인덱스" in tag else X_POS + EW - 32
    d.chip(cx, fy + 12, tag, tc, 11, pad=4)

# 3. organizations 엔티티
d.box(X_ORG, EY, EW, EH, PAPER2, RULE, 1.0)
d.box(X_ORG, EY, EW, 36, PAPER, RULE, 0.8)
d.t(X_ORG + 14, EY + 23, "organizations", 13, INFO, MONO, "start", 600)
d.t(X_ORG + EW - 14, EY + 23, "조직 엔티티", 11, MUTED, KR, "end")
d.line(X_ORG, EY + 36, X_ORG + EW, EY + 36, RULE, 0.8)

fields_org = [
    ("# org_id: 513", "PK", OK),
    ("name", "속성", MUTED),
    ("logo_url", "속성", MUTED),
]
for i, (f, tag, tc) in enumerate(fields_org):
    fy = EY + 48 + i * 28
    d.t(X_ORG + 14, fy + 16, f, 11, INK, MONO, "start")
    d.chip(X_ORG + EW - 32, fy + 12, tag, tc, 11, pad=4)

# 관계선 및 다중도 (users ──── positions ──── organizations)
MID_REL_Y = EY + 104
# users -> positions
d.line(X_USR + EW, MID_REL_Y, X_POS, MID_REL_Y, RULE, 1.2)
d.t(X_USR + EW + 14, MID_REL_Y - 8, "1", 12, INK, MONO, "middle", 600)
d.t(X_POS - 14, MID_REL_Y - 8, "N", 12, ACC, MONO, "middle", 600)
d.t((X_USR + EW + X_POS) / 2, MID_REL_Y + 16, "1 : N 직위", 11, MUTED, KR, "middle")

# positions -> orgs
d.line(X_POS + EW, MID_REL_Y, X_ORG, MID_REL_Y, RULE, 1.2)
d.t(X_POS + EW + 14, MID_REL_Y - 8, "N", 12, ACC, MONO, "middle", 600)
d.t(X_ORG - 14, MID_REL_Y - 8, "1", 12, INK, MONO, "middle", 600)
d.t((X_POS + EW + X_ORG) / 2, MID_REL_Y + 16, "N : 1 소속", 11, MUTED, KR, "middle")

# 하단 양방향 보조 인덱스 쿼리 경로 존
d.box(X_USR, QY, W - X_USR * 2, QH, PAPER2, RULE, 0.8)
d.t(X_USR + 16, QY + 22, "양방향 쿼리 지원 (관계는 1곳만 저장하고 보조 인덱스로 양방향 탐색)", 12, INK, KR, "start", 600)

# 1행: 사용자 -> 조직 탐색
d.arrow([(X_USR + 20, QY + 46), (X_USR + 56, QY + 46)], ACC, "acc", 1.2)
d.t(X_USR + 68, QY + 50, "사용자별 조직: user_id 인덱스 → positions ⋈ orgs", 11, INK, KR, "start")

# 2행: 조직 -> 직원 탐색
d.arrow([(X_USR + 20, QY + 74), (X_USR + 56, QY + 74)], INFO, "info", 1.2)
d.t(X_USR + 68, QY + 78, "조직별 직원: org_id 인덱스 → positions ⋈ users", 11, INK, KR, "start")

d.legend(LEG, [
    ("연관 테이블 · FK 인덱스 (focal)", ACC),
    ("엔티티 테이블 · FK", INFO),
    ("PK", OK),
    ("속성", MUTED)
])

d.save("03-02.associative-table.svg")
