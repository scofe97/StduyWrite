# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: PostgreSQL 18 문서 13.2 표 13.1(격리 수준 × 현상), MySQL 9.7 문서 17.7.2.1(InnoDB 기본 REPEATABLE READ)·17.3(DB_TRX_ID 200·201 은 예시 값), 추출본 v1.txt 1623~1670행(version 낙관적 잠금 · 객실 예약), 1673~1681행(세 노드 저장 확인 옵션 3종), 577~640행(데이터베이스 범주 12종).
# Layout conventions: 카드 폭 164·높이 212, 가로 stride 180(x=40+180k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 01-01",
      "동시 쓰기의 이상을 막는 세 도구와 데이터 모양",
      "격리 수준·MVCC·낙관적 잠금이 이상 현상을 막고, 복제 확인 수가 지연과 일관성을 맞바꾸며, 데이터 모양이 범주를 고른다.",
      "다섯 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 164, 212, 180, 40, 112
cards = [
    ("§1", "격리 수준과 이상 현상", "READ COMMITTED", "반복 불가 읽기 가능", "다음 수준에서 차단", ACC),
    ("§2", "MVCC 와 잠금", "200 · trx 201", "100 · trx 200", "트랜잭션 B 는 100 을 읽음", INFO),
    ("§3", "버전 번호 비교", "WHERE version=1", "1 row → 0 rows", "두 번째 사용자는 다시 읽음", INFO),
    ("§4", "복제 확인 수", "1/3 · 2/3 · 3/3", "지연 낮음 → 높음", "일관성 약함 → 강함", INFO),
    ("§5", "데이터 모양과 범주", "중첩 JSON", "→ 문서 데이터베이스", "범주 12종", INFO),
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
    d.t(cx, Y0 + 132, v2, 12, c if v2.startswith("1 row") else INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("01-01.chapter-overview.svg")
