# 02-01 §1 — 같은 5계층 위에 올라가는 두 배치를 나란히 놓는다.
# 본문이 각 배치의 성질을 세 가지로 못 박아 두었다: 클라이언트-서버는 항상 켜진 서버·고정 주소·
# 클라이언트끼리 직접 통신 없음, P2P 는 간헐적으로 연결되는 호스트 쌍의 직접 통신·자기 확장성.
# 그림은 그 문장을 배치로 옮긴 것이고, 없는 성질을 더하지 않았다.
# 타입 스펙: type-architecture — 구성 요소와 연결. zone 으로 두 배치를 묶고 한쪽 성질에만 강조를 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 568
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §1",
      "같은 5계층 위에 두 배치가 올라갑니다",
      "클라이언트-서버는 항상 켜진 서버로 모이고, P2P 는 피어끼리 직접 주고받는다.",
      "사용자가 늘 때 무엇이 함께 느는지가 두 배치를 가릅니다")

# ── 왼쪽 zone: 클라이언트-서버
d.box(24, 104, 468, 300, "none", RULE, 1.0)
d.t(44, 130, "클라이언트-서버", 14, INK, KR, "start", 600)

d.tone(168, 150, 180, 52, OK, 6, "14", 1.2)
d.t(258, 172, "서버", 12, OK, KR, "middle", 600)
d.t(258, 190, "항상 켜짐 · 주소 고정", 11, MUTED, KR)

d.line(96, 232, 420, 232, RULE, 1.0)
d.path("M 258 230 L 258 208", MUTED, 1.3, m="ar")
CX = [96, 204, 312, 420]
for cx in CX:
    d.box(cx - 46, 268, 92, 48, PAPER2, RULE, 0.9)
    d.t(cx, 297, "클라이언트", 11, INK, KR)
    d.path(f"M {cx} 266 L {cx} 238", MUTED, 1.2, m="ar")

d.line(96, 340, 420, 340, BAD, 1.0, "5 5")
d.chip(258, 340, "서로 말을 걸지 않습니다", BAD)

d.tone(44, 356, 428, 36, WARN, 6, "10", 1.0)
d.t(60, 379, "규모가 커지면 데이터센터 — 전기·관리와 대역폭 비용이 계속 나갑니다", 11, WARN, KR, "start")

# ── 오른쪽 zone: P2P
d.box(508, 104, 468, 300, "none", RULE, 1.0)
d.t(528, 130, "P2P", 14, INK, KR, "start", 600)

PX, PY_ = [607, 877], [160, 268]
for px in PX:
    for py in PY_:
        d.box(px - 75, py, 150, 52, PAPER2, RULE, 0.9)
        d.t(px, py + 24, "피어", 11, INFO, KR, "middle", 600)
        d.t(px, py + 42, "간헐적으로 연결", 11, MUTED, KR)
d.path("M 686 186 L 796 186", INFO, 1.3, m="info")
d.path("M 877 216 L 877 262", INFO, 1.3, m="info")
d.path("M 798 294 L 688 294", INFO, 1.3, m="info")
d.path("M 607 264 L 607 218", INFO, 1.3, m="info")
d.t(742, 342, "피어끼리 직접 주고받습니다", 11, MUTED, KR)

d.tone(528, 356, 428, 36, ACC, 6, "12", 1.4)
d.t(544, 379, "자기 확장성 — 사용자가 늘면 부하와 용량이 같이 늡니다", 11, ACC, KR, "start")

# ── 결론
d.line(24, 432, 976, 432, RULE, 0.8)
d.t(24, 456, "자기 확장성과 비용 이점을 다 적어 놓고도 결론은 클라이언트-서버입니다.", 12, INK, KR, "start")
d.t(24, 478, "P2P 는 고도로 분산된 구조 때문에 보안·성능·신뢰성의 도전에 부딪힙니다.", 11, MUTED, KR, "start")

d.legend(H - 52, [("자기 확장성", ACC), ("항상 켜진 서버", OK), ("피어", INFO),
                  ("일어나지 않는 통신", BAD), ("치르는 비용", WARN)])
d.save("02-01.two-architectures.svg")
print("ok two-architectures")
