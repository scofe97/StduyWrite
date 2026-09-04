# 07-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 744
d = D(W, H, "LEARNING COREDNS · 07-01",
      "질문과 답이 어긋나면 클라이언트가 버린다",
      "이 노트가 나눈 절 여덟을 읽는 순서로 이은 지도(원서의 상위 절은 다섯). 1~5절이 요청과 응답을 고치는 이야기이고, "
      "6~7절이 서명, 8절이 둘을 합친 서비스다.",
      "3절과 4절이 이 장의 논지가 드러나는 자리입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "존 파일 없이 답을 짓는다", "답의 첫 칸이 질문 이름 그대로다"),
    ("§2", "인증서 하나로 안팎을 쓰려면", "외부 이름을 부르면 나갔다 온다"),
    ("§3", "정규식은 질문을 안 돌려준다", "answer name 을 빠뜨리면 버려진다"),
    ("§4", "class 에는 되돌릴 길이 없다", "일곱 해가 지나도 그대로다"),
    ("§5", "요청에 싣고 상류에서 푼다", "rewrite edns0 와 metadata"),
    ("§6", "키를 둘로 나누는 이유", "부모 존이 아는 키는 하나뿐"),
    ("§7", "합성 레코드에는 파일이 없다", "그래서 요청 때 서명한다"),
    ("§8", "사례 — 신원을 실어 보낸다", "앞 절들을 그대로 이어 붙였다"),
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
    focal = (i in (2, 3))
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 632, "요청을 고치면 응답도 같이 고쳐야 한다 — 대응을 검사하는 쪽은 서버가 아니라 클라이언트다", 13, MUTED, KR, "start")
d.t(20, 656, "이름은 되돌릴 수 있고 클래스는 되돌릴 수 없다", 13, MUTED, KR, "start")

d.legend(684, [("대응이 깨지는 자리", ACC)])
d.save("07-01.chapter-overview.svg")
