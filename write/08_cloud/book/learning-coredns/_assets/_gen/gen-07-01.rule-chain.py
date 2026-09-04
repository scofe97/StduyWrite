# 07-01 §4 — continue 와 stop 이 만드는 규칙 처리. 기본값이 stop 이라는 것이 이 절의 요점이다.
# 원문 근거: "By default, the first matching rule will be applied and rule processing will stop.
#            To enable multiple rules to affect the same query, you can specify the continue
#            option." / "when multiple rewrite rules are specified within a server block, they
#            are processed in order. It also does not matter whether other plug-in directives
#            appear between the rewrite rules."
# 타입 스펙: type-state — 상태는 "지금 어느 규칙을 보고 있는가"이고, 전이 라벨이
#           event [guard] / action 꼴이다. 기본값(stop)이 초점이라 그 전이만 주황으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING COREDNS · 07-01 §4",
      "continue 와 stop 이 만드는 규칙 처리",
      "rewrite 규칙 여럿이 한 서버 블록에 있을 때의 상태 전이. 기본은 첫 매치에서 멈추는 것이라, "
      "두 규칙을 이어 붙이려면 앞 규칙에 continue 를 명시해야 한다.",
      "주황이 명시하지 않았을 때 밟는 기본 전이입니다")

SX, SW = 240, 280
CX = SX + SW / 2

# 시작 점
d.tone(CX - 6, 96, 12, 12, INK, 6, "FF", 1.0)
d.arrow([(CX, 110), (CX, 128)], MUTED, "ar", 1.4)

# 상태 셋
d.box(SX, 130, SW, 76, PAPER2, RULE, 1.0, 8)
d.t(CX, 160, "규칙 1 평가", 15, INK, KR, "middle", 600)
d.t(CX, 182, "rewrite continue class CH IN", 10, MUTED, MONO)

d.box(SX, 280, SW, 76, PAPER2, RULE, 1.0, 8)
d.t(CX, 310, "규칙 2 평가", 15, INK, KR, "middle", 600)
d.t(CX, 332, "rewrite stop name bind.version …", 10, MUTED, MONO)

d.box(SX, 430, SW, 76, PAPER2, RULE, 1.0, 8)
d.t(CX, 460, "플러그인 체인 계속", 15, INK, KR, "middle", 600)
d.t(CX, 482, "kubernetes · forward · cache", 10, MUTED, MONO)

# 척추 전이 — 라벨은 왼쪽
d.arrow([(CX, 206), (CX, 278)], MUTED, "ar", 1.4)
d.t(SX - 16, 236, "매치 [continue] / 재작성", 11, MUTED, MONO, "end")
d.t(SX - 16, 254, "매치 없음 / 그대로", 11, MUTED, MONO, "end")

d.arrow([(CX, 356), (CX, 428)], MUTED, "ar", 1.4)
d.t(SX - 16, 386, "매치 [stop] / 재작성", 11, MUTED, MONO, "end")
d.t(SX - 16, 404, "매치 없음 / 그대로", 11, MUTED, MONO, "end")

# 우회 전이 — 기본값. 규칙 1 이 매치했는데 continue 가 없으면 여기로 온다.
d.path(f"M {SX + SW} 168 L 700 168 L 700 468 L {SX + SW + 2} 468", ACC, 1.6, m="acc")
d.t(712, 292, "매치했는데", 11, ACC, KR, "start")
d.t(712, 310, "continue 가 없으면 /", 11, ACC, MONO, "start")
d.t(712, 328, "재작성 후 규칙 처리 종료", 11, ACC, KR, "start")
d.t(712, 352, "옵션을 안 적으면 이쪽이", 11, MUTED, KR, "start")
d.t(712, 370, "기본이다 — 원서 예제는", 11, MUTED, KR, "start")
d.t(712, 388, "continue 를 적어 피한다", 11, MUTED, KR, "start")

# 끝 점
d.arrow([(CX, 506), (CX, 528)], MUTED, "ar", 1.4)
d.tone(CX - 9, 536, 18, 18, INK, 9, "00", 1.2)
d.tone(CX - 5, 540, 10, 10, INK, 5, "FF", 1.0)

# 곁주석
d.box(20, 130, 190, 76, PAPER, RULE, 0.8)
d.t(32, 154, "규칙 사이에", 11, INK, KR, "start", 600)
d.t(32, 174, "다른 플러그인 지시자가", 11, MUTED, KR, "start")
d.t(32, 192, "있어도 순서대로 처리된다", 11, MUTED, KR, "start")

d.legend(576, [("명시하지 않았을 때의 기본 전이", ACC)])
d.save("07-01.rule-chain.svg")
