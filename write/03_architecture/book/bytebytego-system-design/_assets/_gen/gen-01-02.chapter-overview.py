# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 1996~2051행(UserID mod 2, 1·3 / 2·4 두 샤드), 2549~2650행(주문 읽기·쓰기 경로와 복제 지연), twitter-archive/snowflake snowflake-2010 README(time 41 · machine 10 · sequence 12 비트), MySQL Router 8.4 문서(wait_for_my_writes_timeout 기본 1초, read_write 로 폴백). WHERE 열·분포·유일 키 기준은 본문 §2(PostgreSQL 5.12.6, MySQL 26.1).
# Layout conventions: 카드 폭 164·높이 212, 가로 stride 180(x=40+180k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 01-02",
      "데이터를 나누고 복제하고 ID 를 붙이는 다섯 절",
      "열·행으로 나눈 조각이 샤드가 되고, 복제본이 읽기를 받으며, 나뉜 곳마다 ID 가 겹치지 않아야 합니다",
      "절마다 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 164, 212, 180, 40, 112
cards = [
    ("§1", "열로 · 행으로 자르기", "UserID mod 2", "1 · 3  |  2 · 4", "행 4개가 샤드 둘로", INFO),
    ("§2", "샤딩 키 고르기", "WHERE UserID = ?", "질의 · 분포 · 유일 키", "키가 질의 범위를 정함", INFO),
    ("§3", "읽기 복제본과 지연", "SELECT id=1001", "0 rows → 1 row", "주 DB 쓰기 직후 읽기", ACC),
    ("§4", "라우팅과 완화책", "wait_for_my_writes", "timeout 1 → 주 DB", "미들웨어가 폴백", INFO),
    ("§5", "전역 유일 ID", "41 · 10 · 12 비트", "시각 · 서버 · 일련번호", "여섯 방식을 비교", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("01-02.chapter-overview.svg")
