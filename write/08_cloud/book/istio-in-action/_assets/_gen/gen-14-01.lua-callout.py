# 14-01 §6 Lua 스크립트가 요청 경로에서 밖을 부른다 — 원문 14.4.
# 본문(원문 14.4): 들어오는 모든 요청을 A/B 테스트 그룹의 일부로 다루려는데 어느 그룹인지는 런타임에
#       요청의 특성으로만 정할 수 있다. 그래서 A/B 테스트 엔진을 불러 그룹을 받고, 그 응답을 헤더로
#       요청에 붙인다. 업스트림의 어떤 서비스든 그 헤더로 A/B 라우팅을 판단할 수 있다.
#       Lua 안에서 다른 서비스를 부르려면 Envoy 가 제공하는 함수를 써야 한다 — 범용 Lua 라이브러리로
#       RPC 를 걸면 안 되고, Envoy 가 자기 논블로킹 스레딩 아키텍처로 그 호출을 올바로 관리해야 하기
#       때문이다. 그 함수가 httpCall() 이고 마지막 인자가 타임아웃 5000 이다.
#       확인 결과의 응답 헤더는 X-Test-Cohort: dark-launch-7 이다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 한 곳.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, KR, MONO

W, H = 1000, 700
d = Seq(W, H, "ISTIO IN ACTION · 14-01 §6",
        "스크립트가 요청을 멈춰 세우고 밖에 묻는다",
        "요청이 업스트림으로 가기 전에 Lua 필터가 A/B 엔진을 부르고 그 답을 헤더로 붙인다. 색이 붙은 "
        "화살표가 그 콜아웃이고, 그것을 Envoy 가 준 함수로만 걸어야 하는 이유가 이 절의 논점이다.",
        "범용 Lua 라이브러리로 RPC 를 걸면 Envoy 의 스레딩이 그 호출을 관리하지 못합니다")

d.lanes([("클라이언트", "sleep 파드"),
         ("Lua 필터", "envoy_on_request"),
         ("A/B 엔진", "bucket-tester"),
         ("업스트림", "httpbin")], y0=104, lane_w=216)
d.rails(560)

d.msg("클라이언트", "Lua 필터", "요청이 들어온다", 196, MUTED, "ar", sub="라우터 필터 앞에서 붙들린다")
d.msg("Lua 필터", "A/B 엔진", "httpCall(\"bucket_tester\")", 260, ACC, "acc", sub="타임아웃 5000")
d.msg("A/B 엔진", "Lua 필터", "그룹 문자열", 324, INFO, "info", sub="dark-launch-7")
d.selfmsg("Lua 필터", "headers():add", 388, MUTED, sub="x-test-cohort 를 붙인다")
d.msg("Lua 필터", "업스트림", "요청을 넘긴다", 452, MUTED, "ar", sub="헤더가 실려서 간다")
d.msg("업스트림", "클라이언트", "응답", 516, OK, "ok", sub="X-Test-Cohort: dark-launch-7")

d.t(24, 596, "본문을 들여다보면 스트림 취급이 달라진다 — 통째로 메모리에 버퍼링하게 만들 수 있고 성능에 영향이 간다", 11, SOFT, KR, "start")
d.t(24, 620, "구현할 함수는 둘이다 — 요청 쪽은 envoy_on_request, 응답 쪽은 envoy_on_response. Envoy 의 Lua VM 은 LuaJIT 이다", 11, MUTED, KR, "start")
d.legend(640, [("Envoy 가 준 함수로만 걸어야 하는 호출", ACC), ("콜아웃이 돌려주는 값", INFO), ("업스트림이 돌려주는 응답", OK)])
d.save("14-01.lua-callout.svg")
