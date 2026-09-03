# 08-01 §3 헤더를 전파할 때와 하지 않을 때.
# 본문: "프록시는 들어온 요청과 나가는 호출 사이의 인과를 모릅니다." 저자 8.2.1 의 "Istio cannot know which
#       outgoing calls were a result of which incoming requests" 를 요청 하나의 시간축으로 옮긴 것.
# 마지막 두 메시지가 갈림길이다. 앱이 헤더를 실으면 catalog 스팬이 같은 트레이스에 붙고, 안 실으면 새 트레이스가 선다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 헤드라인 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, BAD, INK, KR, MONO

W, H = 1000, 620
d = Seq(W, H, "ISTIO IN ACTION · 08-01 §3",
        "프록시는 스팬을 만들고 트레이스는 앱이 잇는다",
        "요청 하나가 인그레스 게이트웨이와 webapp 을 지나 catalog 로 간다. 프록시는 홉마다 스팬을 만들지만, "
        "webapp 이 들어온 헤더를 나가는 호출에 싣지 않으면 마지막 홉이 다른 트레이스로 갈라진다.",
        "프록시는 어느 아웃바운드가 어느 인바운드 때문인지 알 수 없습니다")

d.lanes([("클라이언트", "curl"),
         ("인그레스 게이트웨이", "istio-proxy"),
         ("webapp", "app + istio-proxy"),
         ("catalog", "app + istio-proxy")], y0=104, lane_w=248)
d.rails(524)

d.msg("클라이언트", "인그레스 게이트웨이", "GET /api/catalog", 196, MUTED, "ar", sub="추적 헤더 없이 들어온다")
d.selfmsg("인그레스 게이트웨이", "트레이스 시작", 252, MUTED, sub="x-b3-traceid 를 만들어 붙인다")
d.msg("인그레스 게이트웨이", "webapp", "x-b3-traceid · spanid", 316, MUTED, "ar", sub="사이드카가 스팬 하나를 보낸다")
d.selfmsg("webapp", "헤더를 복사한다", 372, ACC, sub="프록시가 못 하는 일 — 앱의 몫")
d.msg("webapp", "catalog", "같은 traceid · 새 spanid", 436, ACC, "acc", sub="한 트레이스로 이어진다")
d.msg("webapp", "catalog", "헤더 없음", 496, BAD, "bad", sub="복사하지 않으면 새 트레이스가 선다")

# 마지막 둘은 동시에 일어나지 않는다 — 택일임을 왼쪽 대괄호로 표시
d.line(564, 418, 564, 512, MUTED, 1.0)
d.line(564, 418, 576, 418, MUTED, 1.0)
d.line(564, 512, 576, 512, MUTED, 1.0)
d.t(560, 462, "택일", 11, SOFT, KR, "end", 600)

d.t(20, 552, "저자는 이 말을 8.2.1 본문과 8.2.4 별도 상자에서 두 번 반복한다", 11, SOFT, KR, "start")
d.legend(576, [("앱이 해야 하는 몫", ACC), ("전파하지 않았을 때", BAD)])
d.save("08-01.span-stitching.svg")
