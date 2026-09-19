# 04-01 §3 「SNI — 인증서를 고르려고 도메인 이름이 먼저, 그것도 평문으로」 — 이름이 필요한 때와 도착하는 때.
# 본문 요구: "한 IP 와 한 포트에 사이트가 여럿 얹혀 있으면, 서버는 인증서를 내밀기 전에 클라이언트가 어느
#            사이트를 찾는지 알아야 합니다. 그 이름을 적는 자리는 원래 HTTP Host: 헤더인데, 그것은 암호화가
#            시작된 뒤에 옵니다." 순서 역전은 RFC 문장이 아니라 노트의 해설이다(본문이 밝힌다) — 도식도 그 해설을 그린다.
# 타입 스펙: type-timeline — 사건 넷이 한 축 위에 놓인다. 축은 시간이 아니라 순서라 간격을 같게 두고,
#           그 사실을 축 아래에 적는다(스펙 안티패턴 "what unit is this?").
#           같은 축을 두 번 그리고 '이름 도착' 칩만 옮긴다 — 위는 Host 헤더 자리, 아래는 ClientHello 자리.
#           focal 은 인증서 선택 — 이름이 필요한 단 한 시점. stride: 사건 간격 224, 행 간격 196.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 600
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §3",
      "이름이 필요한 때와 이름이 도착하는 때",
      "TLS 1.2 연결에서 일어나는 사건 넷을 순서대로 놓았다. 서버가 인증서를 고르는 때는 암호화보다 앞인데, "
      "HTTP 의 Host 헤더는 암호화가 시작된 뒤에야 온다. 위 줄은 이름이 Host 헤더로만 올 때의 어긋남이고, "
      "아래 줄은 ClientHello 의 server_name 확장에 이름을 실어 필요한 때보다 앞서 도착하게 한 해결이다.",
      "이름이 필요한 때가 암호화보다 앞이라, 이름을 ClientHello 로 옮겼습니다")

X0, STEP = 200, 224
EX = [X0 + i * STEP for i in range(4)]          # 200 · 424 · 648 · 872
ROWS = [(264, "A · Host 헤더로만", BAD), (460, "B · server_name 확장", OK)]
EVENTS = [("ClientHello", "평문"), ("인증서 선택", "Certificate 전송"),
          ("암호화 시작", "CCS · Finished"), ("HTTP 요청", "Host 헤더")]
CS = 12                                          # 칩 글자 크기

def chip_w(txt, size=CS, pad=7):
    # dd.chip 과 같은 폭 식 — 화살표 끝을 칩 가장자리에 맞추려고 쓴다
    kr = any("가" <= ch <= "힣" for ch in txt)
    return len(txt) * (size * 1.0 if kr else size * 0.62) + pad * 2

# 사건 머리 — 한 번만 적고 세로 안내선으로 두 줄에 내린다
for i, (x, (name, sub)) in enumerate(zip(EX, EVENTS)):
    focal = (i == 1)
    d.t(x, 128, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x, 146, sub, 12, MUTED, MONO if sub.isascii() else KR)
    d.line(x, 160, x, ROWS[1][0] + 12, RULE, 0.8, "3 5")

for y, label, c in ROWS:
    # 암호화된 구간 음영 — 암호화 시작 사건부터 오른쪽
    d.tone(EX[2], y - 52, W - 24 - EX[2], 92, INFO, 6, "0c", 0.6)
    d.t(24, y - 8, label, 13, c, KR, "start", 600)
    d.line(188, y, W - 48, y, SOFT, 1.0)
    for i, x in enumerate(EX):
        d.o.append(f'<circle cx="{x}" cy="{y}" r="{6 if i == 1 else 4}" fill="{ACC if i == 1 else MUTED}"/>')
d.t(EX[2] + 12, ROWS[0][0] - 36, "암호화된 구간", 12, INFO, KR, "start")

def pair(y, arrive_x, need_x, c, mk, dash):
    cy = y + 26
    d.chip(arrive_x, cy, "이름 도착", c, CS)
    d.chip(need_x, cy, "이름 필요", ACC, CS)
    half = chip_w("이름 도착") / 2
    if arrive_x > need_x:   # 늦게 온다 — 오른쪽에서 왼쪽으로
        d.arrow([(arrive_x - half - 4, cy), (need_x + half + 4 + 8, cy)], c, mk, 1.4, dash)
    else:                   # 먼저 와 있다 — 왼쪽에서 오른쪽으로
        d.arrow([(arrive_x + half + 4, cy), (need_x - half - 4 - 8, cy)], c, mk, 1.4, dash)

# A 행은 사건 머리가 이미 'Host 헤더' 라 칩 밑 주석을 두지 않는다 — 두면 x=872 안내선이 그 글자를 관통한다
pair(ROWS[0][0], EX[3], EX[1], BAD, "bad", "5 4")
d.t((EX[1] + EX[2]) / 2, ROWS[0][0] + 50, "필요한 때보다 늦음", 12, BAD, KR)
pair(ROWS[1][0], EX[0], EX[1], OK, "ok", None)
d.t(EX[0], ROWS[1][0] + 52, "server_name", 12, MUTED, MONO)   # 안내선은 ROWS[1]+12 에서 끝나 이 글자와 안 만난다

d.t(188, ROWS[1][0] + 76, "축은 순서 · 간격은 시간에 비례하지 않음", 12, SOFT, KR, "start")

d.legend(H - 40, [("이름이 필요한 때", ACC), ("늦게 도착", BAD), ("앞서 도착", OK), ("암호화된 구간", INFO)])
d.save("04-01.sni-order.svg")
