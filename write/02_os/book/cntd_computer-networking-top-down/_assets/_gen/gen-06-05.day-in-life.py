# 타입 스펙: type-journey — 단계마다 무엇을 하고 무엇을 얻는가. 한 요청이 밟는 여정을 네 국면으로 자른다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.7 —
#   Bob 의 노트북이 웹 페이지 하나를 받기까지. 주소·포트·MAC 값은 원문 예 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 544
d = D(W, H, "SECTION 6.7 · A DAY IN THE LIFE OF A WEB PAGE REQUEST",
      "웹 페이지 하나에 프로토콜 열이 붙습니다",
      "Bob 이 학교 이더넷 스위치에 노트북을 꽂고 구글 첫 페이지를 받기까지. 네 국면마다 쓰는 프로토콜과 그때 얻는 것이 다르다.",
      "주소와 포트는 원문 §6.7 의 예 그대로입니다")

STAGES = [
    (20, "1 · 주소를 얻습니다", "DHCP · UDP · IP · Ethernet", INFO,
     [("보내는 것", "DHCP 요청을 브로드캐스트"),
      ("UDP 포트", "목적지 67 · 출발지 68"),
      ("IP 출발지 · 목적지", "0.0.0.0 · 255.255.255.255"),
      ("MAC 목적지", "FF:FF:FF:FF:FF:FF")],
     ["IP 68.85.2.101", "DNS 68.87.71.226", "게이트웨이 68.85.2.1"]),
    (266, "2 · 이름을 풉니다", "ARP · DNS", OK,
     [("먼저 할 일", "게이트웨이 MAC 을 ARP"),
      ("ARP 질의", "브로드캐스트 프레임"),
      ("그다음", "DNS 질의를 게이트웨이로"),
      ("UDP 포트", "목적지 53")],
     ["게이트웨이 MAC", "00:22:6B:45:1F:1B"]),
    (512, "3 · 도메인 안팎을 지납니다", "forwarding · OSPF · BGP", MUTED,
     [("학교 라우터", "표를 보고 Comcast 로"),
      ("Comcast 안", "도메인 내부 프로토콜"),
      ("도메인 사이", "BGP"),
      ("DNS 서버", "캐시된 레코드를 찾습니다")],
     ["www.google.com", "64.233.169.105"]),
    (758, "4 · 주고받습니다", "TCP · HTTP", ACC,
     [("먼저", "TCP 3-way 핸드셰이크"),
      ("TCP 포트", "목적지 80"),
      ("보내는 것", "HTTP GET"),
      ("받는 것", "응답 본문의 html")],
     ["웹 페이지가", "화면에 뜹니다"]),
]
SW = 224
for x, title, protos, c, steps, gain in STAGES:
    d.tone(x, 116, SW, 52, c, 6, "1E" if c is ACC else "14", 1.5 if c is ACC else 1.1)
    d.t(x + SW / 2, 138, title, 11, c, KR, "middle", 600)
    d.t(x + SW / 2, 157, protos, 9, MUTED, MONO)
    d.box(x, 180, SW, 152, PAPER2, RULE, 0.9)
    for i, (label, value) in enumerate(steps):
        y = 204 + i * 34
        d.t(x + 14, y, label, 10, SOFT, KR, "start")
        fam = MONO if any(ch.isdigit() or ch == ":" for ch in value) else KR
        d.t(x + 14, y + 16, value, 10, INK, fam, "start")
    d.tone(x, 344, SW, 76, c, 6, "14", 1.1)
    d.t(x + SW / 2, 366, "이 국면이 남기는 것", 10, SOFT, KR)
    for i, g in enumerate(gain):
        fam = MONO if any(ch.isdigit() for ch in g) else KR
        d.t(x + SW / 2, 384 + i * 14, g, 10, c, fam)
    if x < 758:
        d.arrow([(x + SW + 2, 142), (x + SW + 18, 142)], MUTED, "ar", 1.4)

d.line(24, 442, W - 48, 442, RULE, 0.8)
d.t(24, 464, "스위치는 1 국면의 첫 프레임에서 Bob 의 MAC 을 배웁니다. 그래서 DHCP 응답은 브로드캐스트가 아니라 그 포트로만 갑니다.",
     11, MUTED, KR, "start")
d.t(24, 482, "원문은 이 예에서도 NAT, 무선 접속, 보안 프로토콜, 웹 캐싱, DNS 계층을 뺐다고 밝힙니다. 빼고도 프로토콜이 이만큼입니다.",
     11, MUTED, KR, "start")

d.legend(500, [("마지막 국면", ACC), ("주소 얻기", INFO), ("이름 풀기", OK), ("라우팅", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-05.day-in-life.svg"
d.save(out)
print("→", out)
