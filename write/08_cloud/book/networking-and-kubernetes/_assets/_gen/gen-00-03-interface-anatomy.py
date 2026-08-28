# 00-03-interface-anatomy — 실제 `ip addr show` 출력에 어느 줄이 무엇인지 주석을 단다
# 본문 요구: "인터페이스 하나에 주소가 둘 붙는다" — 이름·MAC·IP 가 각각 어느 줄에 나오는지.
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 왼쪽 열이 출력 줄, 오른쪽 열이 그 줄의 정체다.
#           다만 왼쪽은 칸으로 나뉘지 않은 출력 한 덩어리라 격자가 아니다. 카탈로그에
#           "실제 출력에 주석 달기(annotated output)" 타입이 없어 세로 대조로 축약했다
#           — visual-diagram-selection.md 의 "알려진 공백" 에 적어 두었다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 출력 문자열을 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER2, KR, MONO

W, H = 1000, 460
BX, BY, BW, BH, TX, NX = 48, 128, 512, 256, 68, 644
# (y, 출력 줄, 색, 오른쪽 주석, 주석 색)
LINES = [(160, "$ ip addr show", SOFT, None, None),
         (196, "1: lo: <LOOPBACK,UP> mtu 65536", INK, None, None),
         (218, "    inet 127.0.0.1/8 scope host lo", MUTED, "루프백 · 선을 타지 않는다", MUTED),
         (254, "2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500", INK, "인터페이스 이름", MUTED),
         (276, "    link/ether 2a:4f:1b:8c:d2:e0", ACC, "MAC · L2 주소", ACC),
         (298, "    inet 192.168.0.15/24 scope global eth0", INFO, "IP · L3 주소와 마스크", INFO),
         (334, "7: cali3f2a@if4: <BROADCAST,MULTICAST,UP> mtu 1450", INK, "veth 쌍 · @if4 가 짝 번호", MUTED),
         (356, "    link/ether ee:ee:ee:ee:ee:ee", MUTED, None, None)]

d = D(W, H, "ANNOTATED OUTPUT · ip addr show",
      "인터페이스 하나에 주소가 둘 붙는다",
      "리눅스 ip addr show 출력을 그대로 두고, 인터페이스 이름과 MAC·IP 가 각각 어느 줄에 나타나는지 "
      "오른쪽에 표시한 주석 도식.",
      lead="실제 출력입니다. 이름은 왼쪽에, MAC 은 link/ether 줄에, IP 는 inet 줄에 나옵니다.")

d.box(BX, BY, BW, BH, PAPER2, RULE, 1.0, 6)
for y, line, c, note, nc in LINES:
    # SVG 는 앞 공백을 접으므로 들여쓰기를 x 오프셋으로 낸다 — 원본은 공백에 기대 접혀 있었다
    indent = 24 if line.startswith("    ") else 0
    d.t(TX + indent, y, line.strip(), 12, c, MONO, "start")
    if note:
        d.line(BX + BW + 12, y - 4, NX - 12, y - 4, RULE, 0.8, "3 5")
        d.t(NX, y, note, 12, nc, KR, "start")

d.t(BX, 404, "MAC 은 커널이 만들어 붙인 값이라, 인터페이스가 사라지면 함께 사라집니다.", 12, MUTED, KR, "start")
d.legend(420, [("MAC · L2", ACC), ("IP · L3", INFO)])
d.save("00-03-interface-anatomy.svg")
print("ok interface-anatomy")
