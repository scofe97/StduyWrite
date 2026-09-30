# 02-01 세부 도식 여섯 — 사용자 요청(2026-09-29) "도식은 더 적극적으로, 여러 장 그려도 됨".
# 각 도식은 그 ### 의 산문 뒤에 둔다(writing-method 1부 규칙 5 의 세부 도식).
# 타입 스펙: type-flowchart. 사실 출처: 02-01 본문, Phase 3 실험 1~5, man udp(7), Linux datagram.c.
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, RULE, MONO, KR
from ddk import node, harrow


def cell(d, x, y, w, h, txt, c=None, dash=False, size=13):
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="none" stroke="{c or SOFT}" stroke-width="1.1" stroke-dasharray="4 4"/>')
        d.t(x + w / 2, y + h / 2 + 5, txt, size, c or SOFT, MONO, "middle", 600)
    elif c:
        d.tone(x, y, w, h, c, 5, "10", 1.1)
        d.t(x + w / 2, y + h / 2 + 5, txt, size, c, MONO if txt.isascii() else KR, "middle", 600)
    else:
        d.box(x, y, w, h)
        d.t(x + w / 2, y + h / 2 + 5, txt, size, INK, MONO if txt.isascii() else KR, "middle", 600)


# A. Read 순간에 따라 달라지는 r (§1)
d = D(960, 412, "FLOWCHART · 02-01 READ TIMING", "Read 를 부른 순간이 정하는 r",
      "같은 hello 와 world 두 번의 쓰기라도 서버가 Read 를 부른 순간 커널에 이어서 도착해 있던 바이트 수가 곧 r 이다. "
      "h 한 바이트만 왔으면 1, hello 까지면 5, 뒤의 wo 까지면 7, 전부면 10 이다.",
      lead="채워진 칸은 Read 순간 이미 도착한 바이트, 점선 칸은 아직 오지 않은 바이트입니다.")
X0, CW, ST, CH = 230, 40, 46, 38
rows = [(120, "h 만 도착", 1), (186, "hello 도착", 5), (252, "hello + wo", 7), (318, "전부 도착", 10)]
for y, lab, n in rows:
    d.t(24, y + 24, lab, 12, MUTED, KR, "start", 600)
    for i, ch in enumerate("helloworld"):
        cell(d, X0 + i * ST, y, CW, CH, ch, None if i < n else SOFT, dash=i >= n)
    d.t(X0 + 10 * ST + 20, y + 25, f"r = {n}", 14, ACC, MONO, "start", 600)
d.save("02-01.read-timing.svg")

# B. 수신 버퍼와 buf, 그리고 윈도 (§1)
d = D(960, 340, "FLOWCHART · 02-01 TWO BUFFERS", "커널 수신 버퍼와 앱의 buf",
      "도착한 바이트는 먼저 소켓마다 있는 커널 수신 버퍼에 쌓이고, Read 가 그중 최대 32KB 를 앱의 buf 로 옮긴다. "
      "받는 쪽은 ACK 마다 수신 버퍼의 빈 공간을 윈도로 알려, 빈 공간이 0 이 되면 보내는 쪽이 멈춘다.",
      lead="넘쳐도 버리지 않습니다. 앱 쪽은 다음 Read 로, 보내는 쪽은 윈도 0 으로 기다립니다.")
Y = 124
node(d, 24, Y, 150, 64, "보내는 쪽", "클라이언트 커널")
harrow(d, 180, 254, Y + 32, label="세그먼트")
node(d, 260, Y, 240, 64, "수신 버퍼", "커널 · 소켓마다 · Recv-Q", ACC, True)
harrow(d, 506, 596, Y + 32, label="Read")
node(d, 602, Y, 180, 64, "buf", "앱 메모리 · 32KB")
d.t(692, Y + 88, "32KB 넘는 몫은 커널에 남음", 11, MUTED, KR, "middle")
d.path(f"M 380 {Y+64} L 380 {Y+140} L 99 {Y+140} L 99 {Y+70}", SOFT, 1.3, m="soft")
d.t(240, Y + 160, "ACK · 윈도 = 수신 버퍼 빈 공간", 12, MUTED, KR, "middle", 600)
d.t(240, Y + 180, "윈도 0 → 보내는 쪽 멈춤", 12, ACC, KR, "middle")
d.save("02-01.two-buffers.svg")

# C. 잘림 (§2)
d = D(960, 400, "FLOWCHART · 02-01 TRUNCATION", "버퍼 3 바이트에 5 바이트 데이터그램",
      "수신 대기열에 hello 와 world 데이터그램이 덩어리째 있다. 3 바이트 버퍼로 ReadFrom 을 부르면 hello 의 앞 3 바이트만 받고 "
      "남은 lo 는 버려지며, 다음 ReadFrom 은 lo 가 아니라 world 를 꺼낸다. 어느 쪽도 에러는 없다. 실험 2 의 결과다.",
      lead="초록 칸은 buf 에 들어간 바이트, 빨간 점선 칸은 버려진 바이트입니다.")
d.t(24, 138, "수신 대기열", 12, MUTED, KR, "start", 600)
for k, w in enumerate(("hello", "world")):
    x = 200 + k * 260
    d.tone(x, 116, 240, 44, SOFT, 6, "10", 1.0)
    d.chip(x + 44, 138, "len 13", MUTED)
    d.t(x + 150, 143, w, 14, INK, MONO, "middle", 600)
for y, lab, w in ((210, "1 번째 ReadFrom", "hello"), (290, "2 번째 ReadFrom", "world")):
    d.t(24, y + 24, lab, 12, MUTED, KR, "start", 600)
    for i, ch in enumerate(w):
        cell(d, 200 + i * 46, y, 40, 38, ch, OK if i < 3 else BAD, dash=i >= 3)
    d.t(200 + 5 * 46 + 16, y + 25, f'r = 3 "{w[:3]}"', 13, OK, MONO, "start", 600)
    d.t(560, y + 25, "err = nil", 13, MUTED, MONO, "start")
    d.t(690, y + 25, f'"{w[3:]}" 버림', 12, BAD, KR, "start", 600)
d.legend(360, [("buf 에 들어간 바이트", OK), ("버려진 바이트", BAD)])
d.save("02-01.truncation.svg")

# D. TCP connect 와 UDP connect (§3)
d = D(960, 420, "FLOWCHART · 02-01 CONNECT", "connect() 가 하는 일",
      "TCP 의 connect 는 SYN, SYN-ACK, ACK 세 세그먼트를 주고받아 양쪽 모두 ESTABLISHED 가 된다. "
      "UDP 의 connect 는 패킷을 보내지 않고 클라이언트 소켓에 상대 주소만 적는다. 커널이 그 소켓 상태 칸에 ESTABLISHED 를 넣어 "
      "ss 에는 ESTAB 으로 보이지만 서버 소켓은 UNCONN 그대로다.",
      lead="이름은 같은 ESTAB 이지만, 왼쪽은 양쪽이 합의한 상태이고 오른쪽은 한쪽의 메모입니다.")
for x0, title in ((24, "TCP"), (500, "UDP")):
    d.t(x0, 108, title, 13, SOFT, KR, "start", 600)
d.line(478, 100, 478, 380, RULE, 1.0, "3 6")
L = {"tc": 110, "ts": 390, "uc": 586, "us": 866}
for key, x in L.items():
    d.t(x, 138, "클라이언트" if key[1] == "c" else "서버", 12, INK, KR, "middle", 600)
    d.line(x, 148, x, 330, RULE, 1.0, "3 6")
for y, lab, a, b, c in ((178, "SYN", "tc", "ts", MUTED), (218, "SYN-ACK", "ts", "tc", MUTED), (258, "ACK", "tc", "ts", MUTED)):
    x1, x2 = L[a], L[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 8, lab, 12, c, MONO, "middle", 600)
d.tone(L["uc"] + 14, 168, 220, 50, ACC, 6, "10", 1.2)
d.t(L["uc"] + 124, 188, "소켓에 상대 주소 기록", 12, ACC, KR, "middle", 600)
d.t(L["uc"] + 124, 207, "peer = [::1]:8080", 11, MUTED, MONO, "middle")
d.t((L["uc"] + L["us"]) / 2, 262, "주고받는 패킷 없음", 12, MUTED, KR, "middle")
for key, st, c in (("tc", "ESTAB", OK), ("ts", "ESTAB", OK), ("uc", "ESTAB", ACC), ("us", "UNCONN", MUTED)):
    d.chip(L[key], 350, st, c)
d.save("02-01.udp-connect.svg")

# E. 순서가 뒤바뀌었을 때 앱의 두 전략 (§4)
d = D(960, 380, "FLOWCHART · 02-01 REORDER STRATEGIES", "5 가 4 보다 먼저 왔을 때",
      "데이터그램이 1 2 3 5 4 6 순서로 도착했다. 재정렬 버퍼 전략은 5 를 잠시 보관했다가 4 를 처리한 뒤 꺼내 1 부터 6 까지 순서대로 "
      "처리한다. 늦으면 버리기 전략은 5 를 먼저 처리하고 뒤늦게 온 4 는 버린다.",
      lead="위는 도착 순서, 아래 두 줄은 앱이 처리하는 순서입니다.")
X0, CW, ST, CH = 200, 56, 66, 40
d.t(24, 144, "도착 순서", 12, MUTED, KR, "start", 600)
for i, n in enumerate("123546"):
    cell(d, X0 + i * ST, 120, CW, CH, n, ACC if n in "54" else None, size=14)
d.t(24, 234, "재정렬 버퍼", 12, MUTED, KR, "start", 600)
for i, n in enumerate("123"):
    cell(d, X0 + i * ST, 210, CW, CH, n, size=14)
d.tone(X0 + 3 * ST, 210, ST + CW, CH, ACC, 5, "14", 1.4)
d.t(X0 + 3 * ST + (ST + CW) / 2, 235, "5 보관", 13, ACC, KR, "middle", 600)
for k, n in enumerate("456"):
    cell(d, X0 + 5 * ST + k * ST, 210, CW, CH, n, OK, size=14)
d.t(24, 314, "늦으면 버리기", 12, MUTED, KR, "start", 600)
for i, n in enumerate("1235"):
    cell(d, X0 + i * ST, 290, CW, CH, n, size=14)
cell(d, X0 + 4 * ST, 290, CW, CH, "4", BAD, dash=True, size=14)
cell(d, X0 + 5 * ST, 290, CW, CH, "6", size=14)
d.t(X0 + 4 * ST + CW / 2, 350, "늦어서 버림", 12, BAD, KR, "middle")
d.t(X0 + 8 * ST + 10, 235, "파일 전송", 12, MUTED, KR, "start")
d.t(X0 + 8 * ST + 10, 315, "음성 · 게임", 12, MUTED, KR, "start")
d.save("02-01.reorder-strategies.svg")

# F. HTTP 판마다 막히는 층 (§4) — 맨 위에 "요청 셋 → 응답 조각" 구성을 먼저 보인다
d = D(960, 700, "FLOWCHART · 02-01 HTTP HOL", "HTTP/1.1 · 2 · 3 에서 막히는 자리",
      "한 페이지를 그리려고 브라우저가 서로 무관한 요청 A(이미지), B(CSS), C(JS) 셋을 보내고, 서버는 응답마다 조각으로 나눠 보낸다. "
      "HTTP/1.1 은 응답을 요청 순서대로 통째로 보내 A 가 B 와 C 를 막는다. HTTP/2 는 세 응답의 조각을 한 TCP 연결에 섞어 보내지만 "
      "A2 가 사라지면 이미 도착한 B2, C2, A3 도 커널에 묶인다. HTTP/3 은 QUIC 이 스트림마다 따로 순서를 맞춰 A 만 멈춘다.",
      lead="A·B·C 는 서로 다른 요청 셋이고, A1·A2·A3 는 응답 A 하나를 자른 조각입니다.")
X0, CW, ST, CH = 250, 60, 68, 32
# 구성: 요청 셋 → 응답 조각
d.t(24, 116, "요청 셋 (한 페이지)", 13, SOFT, KR, "start", 600)
for r, (name, kind) in enumerate((("A", "이미지"), ("B", "CSS"), ("C", "JS"))):
    y = 130 + r * 40
    d.box(24, y, 150, CH, r=5)
    d.t(99, y + 21, f"요청 {name} · {kind}", 12, INK, KR, "middle", 600)
    d.arrow([(182, y + CH / 2), (X0 - 8, y + CH / 2)], SOFT, "soft", 1.2)
    for i in range(3):
        cell(d, X0 + i * ST, y, 60 if False else CW, CH, f"{name}{i+1}")
    d.t(X0 + 3 * ST + 6, y + 21, f"응답 {name} 를 조각 셋으로", 11, MUTED, KR, "start")
d.line(24, 262, 936, 262, RULE, 0.8)
# HTTP/1.1
y = 286
d.t(24, y + 20, "HTTP/1.1", 13, INK, MONO, "start", 600)
d.t(24, y + 38, "앱 계층", 11, MUTED, KR, "start")
d.box(X0, y, 3 * ST - 8, CH, r=5)
d.t(X0 + (3 * ST - 8) / 2, y + 21, "응답 A 전체", 12, INK, KR, "middle", 600)
d.tone(X0 + 3 * ST, y, 2 * ST - 8, CH, ACC, 5, "14", 1.2)
d.t(X0 + 3 * ST + (2 * ST - 8) / 2, y + 21, "응답 B", 12, ACC, KR, "middle", 600)
d.tone(X0 + 5 * ST, y, 2 * ST - 8, CH, ACC, 5, "14", 1.2)
d.t(X0 + 5 * ST + (2 * ST - 8) / 2, y + 21, "응답 C", 12, ACC, KR, "middle", 600)
d.t(X0 + 7 * ST + 6, y + 13, "손실 없어도", 12, ACC, KR, "start")
d.t(X0 + 7 * ST + 6, y + 30, "A 가 끝나야 B · C", 12, ACC, KR, "start")
# HTTP/2
y = 370
d.t(24, y + 20, "HTTP/2", 13, INK, MONO, "start", 600)
d.t(24, y + 38, "TCP 한 줄", 11, MUTED, KR, "start")
for i, (t, c, dash) in enumerate((("A1", None, False), ("B1", None, False), ("C1", None, False), ("A2", BAD, True), ("B2", ACC, False), ("C2", ACC, False), ("A3", ACC, False))):
    cell(d, X0 + i * ST, y, CW, CH, t, c, dash)
d.t(X0 + 7 * ST + 6, y + 13, "도착했지만", 12, ACC, KR, "start")
d.t(X0 + 7 * ST + 6, y + 30, "커널이 붙잡음", 12, ACC, KR, "start")
# HTTP/3
d.t(24, 474, "HTTP/3", 13, INK, MONO, "start", 600)
d.t(24, 492, "QUIC 스트림별", 11, MUTED, KR, "start")
for r, (name, items) in enumerate((("A", (("A1", None, False), ("A2", BAD, True), ("A3", ACC, False))),
                                    ("B", (("B1", None, False), ("B2", OK, False), ("B3", OK, False))),
                                    ("C", (("C1", None, False), ("C2", OK, False), ("C3", OK, False))))):
    y = 454 + r * 44
    d.t(X0 - 14, y + 21, f"스트림 {name}", 11, MUTED, KR, "end", 600)
    for i, (t, c, dash) in enumerate(items):
        cell(d, X0 + i * ST, y, CW, CH, t, c, dash)
d.t(X0 + 3 * ST + 6, 474, "A 만 대기", 12, ACC, KR, "start")
d.t(X0 + 3 * ST + 6, 518, "B · C 는 진행", 12, OK, KR, "start")
d.legend(630, [("사라진 조각", BAD), ("도착했거나 준비됐지만 기다림", ACC), ("계속 진행", OK)])
d.save("02-01.http-hol.svg")

print("ok 02-01 details")

