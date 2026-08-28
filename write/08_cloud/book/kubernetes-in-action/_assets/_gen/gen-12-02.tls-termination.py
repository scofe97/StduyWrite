# 12-02 §1 — 암호가 어디서 풀리는가
# 구간마다 실린 것이 다르다는 게 요점이라, 경로 위에 구간별 라벨을 얹고 암호화 범위를
# 대괄호로 묶는다. 파드가 HTTPS 를 몰라도 되는 이유가 그 범위의 끝에서 나온다.
# 타입 스펙: type-data-flow.md — 한 요청이 지나는 세 구간과 각 구간의 암·복호 상태. 구간 라벨이 곧 무엇이 평문이고
#           무엇이 암호문인지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1140, 560, "KUBERNETES IN ACTION · 12-02",
      "프록시가 TLS 를 끝낸다",
      "클라이언트와 프록시 사이만 암호화되고, 프록시는 복호화한 HTTP 를 백엔드로 보낸다. "
      "인증서와 개인 키를 쥔 것이 프록시라서 그 자리에서 풀린다.",
      "spec.tls 에 붙인 Secret 하나가 이 구간을 덮는다")

ddx.node(d, 160, 300, "클라이언트", "브라우저", 210, 84, INFO)
ddx.node(d, 570, 300, "L7 프록시", "인증서·개인 키를 쥔다", 260, 84, focal=True)
ddx.node(d, 980, 300, "백엔드 파드", "HTTPS 를 몰라도 된다", 210, 84, OK)
d.path("M 268 300 L 432 300", ACC, 1.6, m="acc")
d.path("M 704 300 L 868 300", OK, 1.6, m="ok")
d.chip(350, 272, "HTTPS  ·  암호문", ACC, 9)
d.chip(786, 272, "HTTP  ·  평문", OK, 9)

ddx.bracket(d, 120, 356, 500, "여기까지가 암호화 구간", ACC)
d.t(24, 424, "TLS 가 보장하는 것은 셋이다 — 암호화 · 무결성 · 신원 확인. 그중 신원 확인이 인증서의 몫이라, "
             "Secret 이 인증서와 개인 키를 둘 다 요구한다.", 11, MUTED, KR, "start")
d.t(24, 446, "한 Ingress 에 서비스가 여럿이면 Secret 하나로 그 전부가 HTTPS 로 보호된다 — 백엔드가 평문만 다뤄도 된다.",
     11, MUTED, KR, "start")
d.legend(482, [("암호문 구간", ACC), ("평문 구간", OK), ("양 끝", INFO)])
d.save("12-02-tls-termination.svg")
print("ok")
