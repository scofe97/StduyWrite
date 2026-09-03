# 07-01 §8 attribute-gen 이 만든 속성을 stats 가 받아 쓰는 순서.
# 본문: "이 플러그인은 stats 앞에 겹쳐 섭니다. 순서가 중요합니다. 앞에 서야 자기가 만든 속성을 뒤의 stats 가
#       쓸 수 있습니다." 원문 7.4.3 의 getitems 예를 그대로 옮겼다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 5(최대 12), coral 은 헤드라인 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 524
d = Seq(W, H, "ISTIO IN ACTION · 07-01 §8",
        "attribute-gen 이 앞에 서야 stats 가 쓴다",
        "요청 하나가 두 Wasm 확장을 차례로 지난다. 앞의 것이 기존 속성 둘을 조합해 새 속성을 만들고, "
        "뒤의 것이 그 속성을 차원 값으로 읽는다. 색이 붙은 메시지가 순서가 중요한 이유다.",
        "속성을 만드는 쪽이 소비하는 쪽보다 먼저 서야 합니다")

d.lanes([("요청", "GET /items"),
         ("attribute-gen", "wasm ext"),
         ("stats", "istio.stats"),
         ("프록시 통계", ":15090")], y0=104, lane_w=240)
d.rails(440)

d.msg("요청", "attribute-gen", "request.url_path", 196, MUTED, "ar", sub="request.method 도 함께 읽는다")
d.selfmsg("attribute-gen", "condition 대조", 252, MUTED, sub="url_path == '/items' && method == 'GET'")
d.msg("attribute-gen", "stats", "istio_operationId = getitems", 316, ACC, "acc", sub="새 속성이 만들어진 자리")
d.selfmsg("stats", "차원에 대입", 368, MUTED, sub="upstream_operation")
d.msg("stats", "프록시 통계", "requests_total +1", 424, MUTED, "ar")

d.t(20, 468, "attribute-gen 이 stats 뒤에 서면 istio_operationId 는 아직 없는 속성이 된다", 11, SOFT, KR, "start")
d.legend(480, [("순서가 중요한 이유", ACC)])
d.save("07-01.plugin-order.svg")
