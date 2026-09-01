# 03-09 §4 — ESI 가 엣지에서 페이지를 조립하던 방식. 저자가 적은 동작만 옮긴다.
# 저자의 뉴스 사이트 예(레이아웃 24시간 · 헤드라인 15분)를 캐시 수명 값으로 쓴다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1160, 604
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 03-09 §4",
        "ESI 는 엣지에서 태그를 읽어 페이지를 조립했다",
        "정적인 부분과 동적인 부분을 갈라 캐시 전략을 다르게 가져가는 것이 이 방식의 원리다.",
        "가운데 레인의 엣지 서버가 태그를 해석해 조각을 채워 넣습니다")

d.lanes([("브라우저", "user"),
         ("엣지 서버", "ESI processor"),
         ("오리진", "application")], y0=104, lane_w=280)
d.rails(512)
d.msg("브라우저", "엣지 서버", "GET /product", 210, MUTED, sub="사용자가 페이지를 요청한다")
d.selfmsg("엣지 서버", "parse ESI tags", 276, ACC, sub="어떤 조각을 어떻게 채울지가 태그에 적혀 있다")
d.state("엣지 서버", "layout cached 24h", 332, OK)
d.msg("엣지 서버", "오리진", "fetch dynamic parts", 388, MUTED, sub="개인화 추천 · 실시간 재고")
d.selfmsg("엣지 서버", "assemble", 448, ACC, sub="정적 조각과 동적 조각을 합친다")
d.msg("엣지 서버", "브라우저", "final HTML", 504, MUTED, sub="오리진 부하가 줄고 왕복이 짧아진다")
d.legend(536, [("엣지 서버가 스스로 하는 일", ACC), ("네트워크를 건너는 요청", MUTED)])
d.save("03-09.esi-assembly.svg")
print("h 필요:", 536 + 40, " 실제:", H)
