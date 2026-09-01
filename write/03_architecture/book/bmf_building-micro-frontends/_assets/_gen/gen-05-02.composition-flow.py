# 05-02 §3 — UI 컴포저가 한 요청을 처리하는 순서. 저자의 transformTemplate 코드가 하는 일을 시간축에 편다.
# 함수 이름과 단계는 원문 코드 그대로다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1240, 700
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 05-02 §3",
        "한 요청이 조립되는 순서",
        "컴포저는 템플릿에서 조각 자리를 읽고 어디서 가져올지 물은 뒤 병렬로 받아 끼운다. 이 과정에 비즈니스 판단이 한 줄도 없다.",
        "왼쪽 레인이 컴포저이고 오른쪽 둘이 네트워크 너머에 있는 것입니다")

d.lanes([("UI 컴포저", "orchestrator"),
         ("디스커버리", "key-value registry"),
         ("조각 서비스", "upstream")], y0=104, lane_w=300)
d.rails(576)
d.selfmsg("UI 컴포저", "parse(template)", 208, MUTED, sub="정적 템플릿을 읽는다")
d.selfmsg("UI 컴포저", "getMfeElements()", 268, MUTED, sub="micro-frontend 요소를 모은다")
d.msg("UI 컴포저", "디스커버리", "getServices(mfeList)", 336, MUTED,
      sub="논리 이름을 실제 위치로 바꾼다")
d.msg("디스커버리", "UI 컴포저", "endpoints", 392, MUTED, sub="팀이 독립 배포해도 여기만 바뀐다")
d.msg("UI 컴포저", "조각 서비스", "Promise.allSettled", 452, ACC, "acc",
      sub="모든 조각에 한꺼번에 요청한다")
d.msg("조각 서비스", "UI 컴포저", "HTML fragment", 508, MUTED, sub="각자 자기 데이터로 그려 돌려준다")
d.selfmsg("UI 컴포저", "replaceWith(html)", 560, ACC, sub="플레이스홀더를 바꿔 끼운다")
d.state("UI 컴포저", "스트리밍 시작", 612, OK)
d.legend(636, [("이 방식의 성능을 정하는 두 지점", ACC), ("그 밖의 단계", MUTED)])
d.save("05-02.composition-flow.svg")
print("h 필요:", 636 + 40, " 실제:", H)
