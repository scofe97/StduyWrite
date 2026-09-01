# 05-04 §2 — 사용자가 /catalog/shirts 를 요청했을 때 벌어지는 일 (원문 Figure 5-3).
# 저자가 Mermaid 로 그린 시퀀스를 그대로 옮긴다. 브라우저는 핸드오프를 알지 못한다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1180, 580
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 05-04 §2",
        "브라우저는 핸드오프를 모른다",
        "홈 존이 경로를 보고 카탈로그 존에 프록시한 뒤 돌아온 HTML 을 그대로 전달한다. 사용자는 같은 도메인에 머문다.",
        "가운데 레인이 진입점이자 프록시인 홈 존입니다")

d.lanes([("브라우저", "user agent"),
         ("홈 존", "Next.js server"),
         ("카탈로그 존", "Next.js server")], y0=104, lane_w=290)
d.rails(432)
d.msg("브라우저", "홈 존", "GET /catalog/shirts", 210, MUTED, sub="사용자는 한 도메인만 안다")
d.selfmsg("홈 존", "match /catalog/:path*", 272, ACC, sub="rewrites 규칙에 걸린다")
d.msg("홈 존", "카탈로그 존", "proxy request", 336, ACC, "acc",
      sub="다른 서버여도 CORS 가 생기지 않는다")
d.msg("카탈로그 존", "홈 존", "rendered HTML", 392, MUTED, sub="자기 라우팅으로 그려 돌려준다")
d.msg("홈 존", "브라우저", "HTML", 448, MUTED, sub="그대로 전달한다")
d.state("브라우저", "같은 도메인 유지", 488, OK)
d.legend(508, [("서버 수준에서 갈리는 자리", ACC), ("그 밖의 왕복", MUTED)])
d.save("05-04.rewrite-proxy.svg")
print("h 필요:", 508 + 40, " 실제:", H)
