# 03-04.three-addresses — 세 주소가 각각 어디까지 가서 어떻게 끝나는가
# 본문 요구: §5 의 요점은 결과가 아니라 "어디까지 갔느냐"다. 거부는 목적지까지 갔다는 증거이고
#           타임아웃은 도중에 사라졌다는 뜻이라, 두 실패의 종착지가 서로 달라야 한다.
#           그래서 결과 표가 아니라 여정을 그린다.
# 타입 스펙: type-sequence.md — 세로가 시간, 가로가 주체. 응답이 돌아오는 화살표가 있는 것과
#           없는 것이 갈리는 게 논지라, 마지막 왕복만 응답 화살표가 없다.
# 좌표: Layout conventions 타입이라 공식이 없다. 메시지 stride 56 하나로 고정.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 620
Y0, STRIDE, RAIL_BOT = 168, 56, 468

d = Seq(W, H, "THREE ADDRESSES · HOW FAR DID IT GET",
        "다른 호스트에서 세 주소 — 둘은 답을 받고 하나는 사라진다",
        "ubuntu2 에서 같은 컨테이너를 세 가지 주소로 부른 여정. 앞의 둘은 목적지 호스트까지 도달해 "
        "각각 응답과 거부를 받고, 컨테이너 IP 로 간 것만 게이트웨이 너머에서 응답 없이 사라진다.",
        lead="거부는 도달했다는 증거입니다 · 응답 화살표가 없는 마지막 한 줄만 성격이 다릅니다")

LANES = d.lanes([("ubuntu2", "192.168.139.238"),
                 ("게이트웨이", "192.168.139.1"),
                 ("ubuntu1 · go-web", "192.168.139.208 · 172.17.0.4")])
A, G, B = "ubuntu2", "게이트웨이", "ubuntu1 · go-web"
d.rails(RAIL_BOT)

y = Y0
d.msg(A, B, "192.168.139.208:80", y, OK, sub="같은 랜이라 게이트웨이를 안 거친다")
y += STRIDE
d.msg(B, A, "200 OK", y, OK, dash="4 4", sub="DNAT 이 컨테이너 8080 으로 넘겼다")

y += STRIDE + 12
d.msg(A, B, "192.168.139.208:8080", y, WARN, sub="호스트 포트 8080 을 잡은 것이 없다")
y += STRIDE
d.msg(B, A, "TCP RST", y, WARN, dash="4 4", sub="exit 7 — 거절도 답이다")

y += STRIDE + 12
d.msg(A, G, "172.17.0.4:80", y, BAD, sub="경로가 없어 기본 경로로 떨어진다")
y += STRIDE
d.state(G, "172.17.0.0/16 을 모른다 — 버린다", y, BAD)

d.t(24, RAIL_BOT + 40,
    "앞의 두 줄은 응답 화살표가 있습니다. 목적지 호스트까지 갔다는 뜻이고, 거부도 그 증거입니다.",
    12, MUTED, KR, "start")
d.t(24, RAIL_BOT + 64,
    "마지막 줄만 돌아오는 화살표가 없습니다. exit 28 타임아웃이며, 아무도 이 대역이 ubuntu1 것이라고 알려 준 적이 없기 때문입니다.",
    12, BAD, KR, "start")
d.t(24, RAIL_BOT + 88,
    "그 사실을 알려 주는 일을 오버레이나 경로 광고가 맡습니다. 손댈 곳이 목적지 포트가 아니라 출발지 경로라는 것을 exit 코드가 가릅니다.",
    12, MUTED, KR, "start")
d.legend(RAIL_BOT + 112, [("성공", OK), ("거부 — 도달했다는 증거", WARN), ("타임아웃 — 도중에 사라짐", BAD)])
d.save("03-04.three-addresses.svg")
print("ok three-addresses")
