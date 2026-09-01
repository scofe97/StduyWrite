# 04-02 §5 — 셸이 리모트를 런타임에 등록하고 조각을 불러오는 흐름.
# 함수 이름(getInstance · registerRemotes · loadRemote)과 디스커버리 JSON 은 원문 코드 그대로다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1200, 640
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 04-02 §5",
        "리모트는 런타임에 등록된다",
        "번들러 설정에 리모트를 적지 않았기 때문에 셸이 뜰 때 등록해야 한다. 그 대가로 환경마다 다른 엔드포인트를 같은 산출물로 부를 수 있다.",
        "왼쪽 레인이 셸의 초기화 코드이고 오른쪽 둘이 네트워크 너머에 있는 것입니다")

d.lanes([("애플리케이션 셸", "initializeMFEs"),
         ("디스커버리", "MFEDiscovery.json"),
         ("리모트", "micro-frontend bundle")], y0=104, lane_w=300)
d.rails(548)
d.selfmsg("애플리케이션 셸", "getInstance()", 208, MUTED, sub="번들러가 만든 인스턴스를 집는다")
d.msg("애플리케이션 셸", "디스커버리", "fetch()", 272, MUTED, sub="라우트 설정을 가져온다")
d.msg("디스커버리", "애플리케이션 셸", "microFrontends", 328, MUTED,
      sub="name · alias · exposed · route · url")
d.selfmsg("애플리케이션 셸", "registerRemotes()", 392, ACC, sub="여기서 비로소 리모트가 알려진다")
d.selfmsg("애플리케이션 셸", "setRoutes()", 452, MUTED, sub="1 단계 경로마다 Route 를 만든다")
d.msg("애플리케이션 셸", "리모트", "loadRemote(request)", 512, ACC,
      sub="사용자가 그 경로로 가면 그때 내려받는다")
d.state("리모트", "Suspense 안에서 렌더", 552, OK)
d.legend(576, [("리모트를 알게 되는 두 지점", ACC), ("네트워크를 건너는 요청", MUTED)])
d.save("04-02.dynamic-remotes.svg")
print("h 필요:", 576 + 40, " 실제:", H)
