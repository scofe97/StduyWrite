# 03-01 §2 — IP 가 보장하지 않는 셋이 그 위 둘의 성격을 정한다.
# 본문 근거: "서비스 모델은 최선 노력 배달이며, 보장하지 않는 것이 셋입니다" — 배달·순서·무결성.
#   그리고 §1 의 "이 두 최소 서비스가 UDP 가 제공하는 전부입니다. 나머지는 전부 TCP 가 더하는 것".
# 논점은 UDP 칸의 빈자리다 — UDP 가 안 더한 것은 IP 의 결함이 그대로 올라온 자리다.
# 타입 스펙: type-layers — 바닥 층이 무엇을 안 주느냐가 위층의 할 일을 정한다는 관계를 세로로 세운다.
#            축약: 혼잡 제어의 공익적 성격은 아래 띠에 한 줄로만 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 700
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §2",
      "UDP 의 빈칸이 곧 IP 의 결함입니다",
      "IP 가 보장하지 않는 셋 위에서 UDP 는 둘만 더하고 TCP 는 넷을 더 얹는다. "
      "UDP 가 안 더한 자리는 메워지지 않고 그대로 애플리케이션까지 올라온다.",
      "그래서 UDP 를 고르면 그 자리를 앱이 맡습니다")

# ── 위층 둘 ──
COLS = [
    (24, 466, "UDP", "비연결 · 최소한만", INFO,
     [("더하는 것", OK, ["프로세스 사이 역다중화", "세그먼트 오류 검사"]),
      ("더하지 않는 것", BAD, ["배달 보장", "순서 보장", "흐름 제어", "혼잡 제어"])]),
    (510, 466, "TCP", "연결 지향 · 다 얹음", OK,
     [("더하는 것", OK, ["프로세스 사이 역다중화", "세그먼트 오류 검사",
                     "신뢰적 전송 — 배달과 순서", "흐름 제어", "혼잡 제어"]),
      ("더하지 않는 것", SOFT, ["시간 보장", "최소 대역폭 보장"])]),
]
for x, w, name, sub, c, groups in COLS:
    d.tone(x, 140, w, 268, c, 8, "0C", 1.4)
    d.t(x + 24, 172, name, 15, c, MONO, "start", 700)
    d.t(x + 72, 172, sub, 11, MUTED, KR, "start")
    y = 202
    for head, hc, items in groups:
        d.t(x + 24, y, head, 11, hc, KR, "start", 600)
        for i, it in enumerate(items):
            d.t(x + 36, y + 22 + i * 19, f"· {it}", 11, INK if hc is OK else MUTED, KR, "start")
        y += 30 + len(items) * 19

d.arrow([(257, 432), (257, 414)], INFO, "info", 1.4)
d.arrow([(743, 432), (743, 414)], OK, "ok", 1.4)

# ── 바닥 층 ──
d.tone(24, 440, W - 48, 128, WARN, 8, "0C", 1.4)
d.t(48, 472, "IP · 최선 노력 배달", 14, WARN, KR, "start", 600)
d.t(48, 494, "호스트 사이까지만 데려다줍니다. 보장하지 않는 것이 셋입니다.", 11, MUTED, KR, "start")
for i, (lab, note) in enumerate([("배달", "세그먼트가 도착한다는 보장이 없습니다"),
                                 ("순서", "보낸 순서대로 온다는 보장이 없습니다"),
                                 ("무결성", "안의 데이터가 그대로라는 보장이 없습니다")]):
    x = 48 + i * 306
    d.chip(x + 34, 534, lab, BAD)
    d.t(x + 74, 538, note, 11, SOFT, KR, "start")

d.t(24, 604, "UDP 의 '더하지 않는 것' 칸을 아래 셋과 겹쳐 보면 같은 말입니다. UDP 는 IP 의 결함을 고치지 않고 포트와 체크섬만 얹습니다.",
    11, ACC, KR, "start")
d.t(24, 626, "TCP 의 혼잡 제어만 성격이 다릅니다. 부른 앱을 위한 서비스라기보다 인터넷 전체를 위한 것이라, 앱이 원해서 얻는 기능이 아닙니다.",
    11, MUTED, KR, "start")

d.legend(H - 44, [("IP 가 안 주는 것", BAD), ("최소만 더함", INFO), ("다 얹음", OK), ("빈칸이 뜻하는 것", ACC)])
d.save("03-01.ip-and-two-above.svg")
print("ok ip-and-two-above")
