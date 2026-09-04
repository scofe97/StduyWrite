# 06-02 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "LEARNING COREDNS · 06-02",
      "기본 Corefile 의 줄마다 이유가 있다",
      "6장 중반부의 절 여섯을 읽는 순서로 이은 지도. 1~3절이 플러그인의 동작이고, "
      "4~6절이 그 동작 위에 얹힌 설정이다.",
      "1절의 사실 하나가 2절과 4절을 함께 설명합니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "되쓰지 않는 컨트롤러", "watch 로 받고 질의 때 만든다"),
    ("§2", "두 캐시는 다른 것이다", "이미 메모리에 있는 것을 또 담는다"),
    ("§3", "Endpoints 감시가 비싼 이유", "하나 바뀌면 객체가 통째로 온다"),
    ("§4", "기본 Corefile 열두 줄", "줄마다 왜 있는지가 다르다"),
    ("§5", "스텁 도메인은 블록이 된다", "최장 일치 규칙 하나로 끝난다"),
    ("§6", "페더레이션은 남은 유산이다", "지금은 옵션 자체가 없다"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(len(cards) - 1):
    x1, y1 = pos(i)
    x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 0)
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 504, "\"레코드를 쌓아 두지 않는다\" 는 1절의 사실이 2절의 캐시 무용론과 4절의 cache 30 비판을 함께 만든다", 13, MUTED, KR, "start")
d.t(20, 528, "5절과 6절은 기본 Corefile 밖으로 밀려 있던 변수 둘을 마저 본다", 13, MUTED, KR, "start")

d.legend(556, [("나머지를 설명하는 절", ACC)])
d.save("06-02.chapter-overview.svg")
