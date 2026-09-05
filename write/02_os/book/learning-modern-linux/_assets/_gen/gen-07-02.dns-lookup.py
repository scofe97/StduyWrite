# 07-02 §7 — 질문 하나가 네 절의 답으로 돌아온다.
# 원문("DNS Lookups"): host 와 dig 의 실제 출력. dig 헤더가
#       ";; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 2, ADDITIONAL: 5" 이고
#       ANSWER 에 A 레코드 넷, AUTHORITY 에 NS 둘, ADDITIONAL 에 그 네임서버의 A·AAAA 가 온다.
#       ";; Query time: 58 msec", ";; SERVER: 172.16.173.64#53(172.16.173.64)".
#   Resolvers: "Programs that extract information from name servers in response to client requests. They
#       are machine local, and no explicit protocol is defined for the interaction between a resolver and
#       a client."
#   "In the query process, the resolver would iteratively query authoritative name servers (NS) starting
#       from the root or, if supported, using a recursive query where an NS queries others on behalf of a
#       resolver."
#   저자의 격언 — "It's always DNS." 이유는 캐시가 여러 층에 있기 때문.
# 타입 스펙: type-sequence — 시간축 위의 주고받음. accent 는 캐시가 끼어드는 자리, 곧 저자가
#           문제를 파고들 때 살피라고 한 곳. 축약: 반복 질의의 중간 단계는 한 번으로 뭉쳤다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 684
d = Seq(W, H, "LEARNING MODERN LINUX · 07-02 §7",
        "질문 하나가 네 절의 답으로 돌아온다",
        "dig 한 줄이 리졸버를 거쳐 네임서버에 닿고, 돌아온 응답이 QUESTION · ANSWER · "
        "AUTHORITY · ADDITIONAL 네 절로 나뉜다.",
        "저자는 언제나 DNS 탓이라는 격언을 인용합니다")

d.lanes([("앱 · dig", "클라이언트"), ("리졸버", "기계에 딸림"),
         ("권한 있는 NS", "dns1.registrar"), ("응답", "네 절")], y0=116, lane_w=190)

d.msg("앱 · dig", "리졸버", "mhausenblas.info. IN A", 184, INFO,
      sub="둘 사이에 정해진 프로토콜은 없다")
d.selfmsg("리졸버", "캐시에 있으면 여기서 끝난다 — TTL 이 남았는가", 232, ACC)
d.msg("리졸버", "권한 있는 NS", "루트에서부터 반복 질의", 296, OK, mk="ok",
      sub="지원되면 재귀 질의로 대신 물어 준다")
d.state("권한 있는 NS", "authoritative", 340, OK)
d.msg("권한 있는 NS", "응답", "A 레코드 넷 · NS 둘 · 추가 다섯", 388, INFO, mk="info")
d.state("응답", "Query time: 58 msec", 432, INFO)
d.msg("응답", "앱 · dig", "NOERROR · ANSWER 4", 480, INFO, mk="info")

d.rails(512)

d.tone(24, 528, W - 48, 78, ACC)
d.t(44, 556, "언제나 DNS 탓이라는 말의 뜻", 12.5, INK, KR, "start", 600)
d.t(44, 578, "DNS 는 움직이는 부품이 많은 분산 데이터베이스입니다. 앱 안의 로컬 캐시부터 리졸버까지,",
    11.5, MUTED, KR, "start")
d.t(44, 596, "그리고 나와 네임서버 사이의 모든 것에 캐시가 있습니다. 레코드의 TTL 을 먼저 보십시오.",
    11.5, MUTED, KR, "start")

d.legend(620, [("사람과 응답", INFO), ("네임서버까지", OK), ("문제가 숨는 자리", ACC)])
d.save("07-02.dns-lookup.svg")
print("ok 07-02.dns-lookup")
