# 13-03 §2 — 뜻대로 안 되는 양상이 셋이고 각각 다르다
# 본문이 "값이 틀린 것을 찾는 눈과 값이 없는 것을 찾는 눈은 다르다"로 진단법을 갈라 둔다.
# status 열이 셋을 가르는 축이라 그 열을 판정 축으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, KR
import ddx

d = D(1240, 604, "KUBERNETES IN ACTION · 13-03",
      "에러가 안 나는 실패가 가장 어렵다",
      "apply 를 받는 것은 API 서버이고 status 를 채우는 것은 컨트롤러다. 둘이 별개라, "
      "컨트롤러가 그 리소스 종류를 아예 안 보면 채울 사람이 없어 status 가 빈다.",
      "Istio 에 UDPRoute 를 apply 했을 때 무슨 일이 나는가")

ddx.matrix(
    d, x0=24, hdr_y=140, row_h=86, gap=12, focal_col=2,
    cols=[(300, "상황"), (170, "apply"), (330, "status"), (380, "어떻게 찾나")],
    rows=[
        ([("스키마 오류", "없는 필드를 적었다"), ("실패",),
          ("해당 없음", "만들어지지도 않는다"),
          ("바로 안다", "명령이 에러를 낸다")], BAD),
        ([("참조 거부", "ReferenceGrant 가 없다"), ("성공",),
          ("ResolvedRefs: False", "RefNotPermitted"),
          ("이유가 적힌다", "reason 을 읽으면 된다")], WARN),
        ([("구현 미지원", "Istio 는 UDPRoute 를 안 본다"), ("성공",),
          ("비어 있다", "아무 일도 안 일어난다"),
          ("빈지·0 인지 보라", "값이 없는 것을 찾는 눈")], ACC),
    ])

d.t(24, 484, "같은 결의 사례가 셋이다 — 13-01 의 attachedRoutes: 0, 12-02 의 기본 IngressClass 부재, 그리고 여기 status 빔. "
             "전부 아무도 처리하지 않아 조용히 아무 일도 안 일어나는 경우다.", 11, MUTED, KR, "start")
d.t(24, 506, "support level 은 명세에 적힌 규범이고, 지금 이 컨트롤러가 실제로 지원하는가는 status 로 확인한다 — 규범과 실측은 다른 자료다.",
     11, MUTED, KR, "start")
d.legend(532, [("바로 걸린다", BAD), ("이유가 남는다", WARN), ("아무 말이 없다", ACC)])
d.save("13-03-three-failure-modes.svg")
print("ok")
