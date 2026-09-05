# 09-02 §2 — 네 함수가 각각 몇 번 불리는가. 호출 횟수가 곧 무엇을 어디 둘지를 정한다.
# 원문 근거: "You need to implement only four functions: init, setup, Name, and ServeDNS."
#            / init: "performs one-time initialization of the plug-in. This is a standard Go
#            package initialization function" / setup: "It will be called exactly once for each
#            server block in which it appears." / "ServeDNS is the heart of any backend or
#            mutator plug-in, performing the actual query and response manipulation."
# 타입 스펙: type-layers — 위에서 아래로 갈수록 호출 빈도가 커지는 층이고, 층마다 같은 슬롯
#           (이름 · 하는 일 · 몇 번)이 반복된다. 요청마다 불리는 층 하나가 초점이다.
#           단 Name 의 호출 빈도는 원서가 말하지 않으므로 층에 끼워 넣되 빈도를 적지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 556
d = D(W, H, "LEARNING COREDNS · 09-02 §2",
      "네 함수가 불리는 시점",
      "위로 갈수록 드물게 불리고 아래로 갈수록 잦게 불린다. 원격 연결을 여는 코드를 "
      "아래층에 두면 요청마다 연결이 열린다.",
      "주황이 요청마다 불리는 층입니다")

SX, SW, RH = 190, 660, 68
ROWS = [
    ("F1", "init", "지시자를 등록한다", "프로세스당 한 번", False),
    ("F2", "setup", "Corefile 을 파싱하고 훅을 건다", "서버 블록당 한 번", False),
    ("F3", "Name", "이름 문자열을 돌려준다", "원서가 빈도를 말하지 않는다", False),
    ("F4", "ServeDNS", "질의와 응답을 다룬다", "요청마다", True),
]

for i, (tag, name, mid, right, focal) in enumerate(ROWS):
    y = 130 + i * RH
    if focal:
        d.tone(SX, y, SW, RH, ACC, 0, "12", 1.4)
    else:
        d.box(SX, y, SW, RH, PAPER2 if i % 2 else PAPER, RULE, 1.0, 0)
    d.t(SX + 18, y + 26, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(SX + 18, y + 48, name, 15, ACC if focal else INK, MONO, "start", 600)
    d.t(SX + 168, y + 42, mid, 12, MUTED, KR, "start")
    d.t(SX + SW - 18, y + 42, right, 11, ACC if focal else MUTED, KR, "end")

d.t(58, 152, "CALLS", 9, SOFT, MONO, "start")
d.t(58, 174, "잦아진다", 11, MUTED, KR, "start")
d.arrow([(44, 192), (44, 386)], MUTED, "ar", 1.4)
d.t(58, 300, "그래서 비싼 일은", 11, SOFT, KR, "start")
d.t(58, 318, "위쪽 층에", 11, SOFT, KR, "start")
d.t(58, 336, "예약해 둔다", 11, SOFT, KR, "start")

d.box(20, 426, 840, 62, PAPER, RULE, 0.8)
d.t(36, 450, "Name 과 ServeDNS 가 Handler 인터페이스를 이룬다", 12, INK, KR, "start", 600)
d.t(36, 472, "설정만 바꾸는 플러그인이라면 ServeDNS 는 한 줄이어도 된다고 저자들이 적는다",
     11, MUTED, KR, "start")

d.legend(508, [("요청마다 불리는 층", ACC)])
d.save("09-02.four-functions.svg")
