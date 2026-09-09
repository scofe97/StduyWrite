# 01-03.pmtu-blackhole — 크면 버리고 알려 준다, 그 알림이 막히면 조용히 사라진다
# 본문 요구: 헤더 필드 목록에 `Flags`(Do not Fragment)가 이름으로만 있고, 그 비트가 만드는
#           사건이 노트 어디에도 없었다(2026-09-02 전수 확인). 같은 왕복이 ICMP 회신 유무로
#           정상과 블랙홀로 갈리는 것이 요점이라, 결과 표가 아니라 두 왕복을 나란히 둔다.
# 타입 스펙: type-sequence.md — 세로가 시간, 가로가 주체. 위 묶음은 ICMP 가 돌아오고 아래 묶음은
#           같은 자리에 화살표가 없다. 그 빈자리가 이 그림의 논지다.
# 좌표: Layout conventions 타입이라 공식이 없다. 메시지 stride 52 하나, 묶음 사이만 +16.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 668
Y0, STRIDE, RAIL_BOT = 176, 52, 512

d = Seq(W, H, "PATH MTU DISCOVERY · AND ITS BLACK HOLE",
        "크면 버리고 크기를 알려 준다 — 그 알림이 막히면 조용히 사라진다",
        "DF 비트를 세운 패킷이 링크 MTU 를 넘었을 때의 두 갈래. 위는 라우터의 ICMP 가 돌아와 "
        "송신이 크기를 줄이는 정상 경로이고, 아래는 그 ICMP 가 차단돼 같은 크기로 재전송만 반복하는 경우다.",
        lead="두 묶음의 차이는 화살표 하나입니다 · 아래 묶음에는 돌아오는 알림이 없습니다")

d.lanes([("송신 호스트", "MTU 1500"), ("중간 라우터", "다음 링크 MTU 1450"), ("목적지", "웹 서버")])
A, R, B = "송신 호스트", "중간 라우터", "목적지"
d.rails(RAIL_BOT)

y = Y0
d.msg(A, R, "1500B  DF=1", y, INFO, sub="쪼개지 말라는 표시를 세워 보낸다")
y += STRIDE
d.state(R, "1450 을 넘는다 — 버린다", y, WARN)
y += STRIDE
d.msg(R, A, "ICMP  Frag Needed  MTU=1450", y, OK, dash="4 4", sub="버렸다 + 이만큼으로 줄여라")
y += STRIDE
d.msg(A, B, "1450B  DF=1", y, OK, sub="줄여서 다시 — 통과한다")

y += STRIDE + 16
d.msg(A, R, "1500B  DF=1", y, INFO, sub="같은 패킷, 같은 표시")
y += STRIDE
d.state(R, "버린다 — 그런데 ICMP 가 차단돼 있다", y, BAD)
y += STRIDE
d.selfmsg(A, "재전송 · 재전송 · 재전송", y, BAD, sub="줄이라는 말을 못 들었으니 크기를 안 바꾼다")

d.t(24, RAIL_BOT + 44, "위 묶음은 라우터가 두 번 말합니다 — 버렸다는 사실과 얼마로 줄이라는 값을 함께 보냅니다. "
                       "그래서 통신이 이어집니다.", 12, MUTED, KR, "start")
d.t(24, RAIL_BOT + 68, "아래 묶음에는 그 말이 없습니다. 송신은 왜 안 가는지 모른 채 같은 크기로 재전송하다 멈춥니다. "
                       "이것이 PMTU 블랙홀입니다.", 12, BAD, KR, "start")
d.t(24, RAIL_BOT + 92, "작은 요청은 잘 되고 응답이 큰 것만 멈추므로 \"네트워크가 안 된다\"가 아니라 "
                       "\"어떤 API 만 가끔 멈춘다\"로 나타납니다.", 12, MUTED, KR, "start")
d.legend(RAIL_BOT + 116, [("알림이 돌아온다", OK), ("보낸 패킷", INFO),
                          ("버리는 판단", WARN), ("알림이 없다", BAD)])
d.save("01-03.pmtu-blackhole.svg")
print("ok pmtu-blackhole")
