# 07-02 §2·§3 — 헤더 필드가 곧 그 프로토콜이 무엇을 보장하는지다.
# 원문(TCP, RFC 793 기준 저자 목록): Source port(16) · Destination port(16) · Sequence number(32) ·
#       Acknowledgment number(32) · Flags(9) · Window(16) · Checksum(16) · Data.
#       "This number and the SYN and ACK flags are the core of the so-called TCP/IP three-way handshake."
#       "From a security perspective, TCP is without any defense mechanisms. In other words, the payload
#       is sent in plain text."
# 원문(UDP, RFC 768 기준): Source port(16, "optional, and if not, use 0") · Destination port(16) ·
#       Length(16, "The total length of the UDP header and data") · Checksum(16, "Can optionally be used
#       for error checking") · Data.
#       "UDP is a very simple protocol and requires the higher-level protocol that works on top of it to
#       take care of many of the things that TCP would handle itself. On the other hand, UDP has very
#       little overhead and can achieve high throughput."
# 타입 스펙: type-bar — 값(비트 폭)을 길이로 견주는 형태. 같은 축 위에 두 프로토콜의 필드를 놓으면
#           무엇이 빠졌는지가 길이의 부재로 드러난다. accent 는 TCP 에만 있는 것들.
#           축약: 저자가 꼽은 필드만 그렸다 — 실제 헤더에는 이 밖의 필드도 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 684
d = D(W, H, "LEARNING MODERN LINUX · 07-02 §2·§3",
      "UDP 에 없는 필드가 곧 UDP 가 보장하지 않는 것이다",
      "저자가 꼽은 헤더 필드를 비트 폭 그대로 견준 것. 순서 번호와 확인 응답 번호와 윈도가 "
      "빠진 자리가 UDP 의 단순함이자 한계다.",
      "빠진 만큼 위층이 대신 해야 합니다")

LX, LABW, SCALE, RH = 32, 190, 8.0, 34
TCP_Y = 176
fields_tcp = [
    ("Source port", 16, OK), ("Destination port", 16, OK),
    ("Sequence number", 32, ACC), ("Acknowledgment number", 32, ACC),
    ("Flags", 9, ACC), ("Window", 16, ACC), ("Checksum", 16, OK),
]
fields_udp = [
    ("Source port", 16, OK), ("Destination port", 16, OK),
    ("Length", 16, INFO), ("Checksum", 16, OK),
]
# TCP 블록의 실제 아래끝에서 UDP 블록의 시작을 산출한다. 상수로 박아 두었던 400 은
# TCP 7행(176 + 7×34 = 414)의 안쪽이라 마지막 행과 UDP 제목이 겹쳤다. 겹침 검사기는
# 글자끼리만 보므로 이 상자 겹침을 잡지 못한다 — 렌더해서 눈으로 확인해 찾았다.
UDP_Y = TCP_Y + len(fields_tcp) * RH + 38


def block(y, title, sub, fields, col):
    d.t(LX, y - 14, title, 15, col, KR, "start", 600)
    d.t(LX + 78, y - 14, sub, 11, MUTED, KR, "start")
    for i, (name, bits, c) in enumerate(fields):
        yy = y + i * RH
        d.t(LX + LABW - 10, yy + 20, name, 11.5, INK, MONO, "end")
        w = bits * SCALE
        if c is ACC:
            d.o.append(f'<rect x="{LX + LABW}" y="{yy + 4}" width="{w}" height="24" rx="4" '
                       f'fill="{ACC}22" stroke="{ACC}" stroke-width="1.3"/>')
        else:
            d.o.append(f'<rect x="{LX + LABW}" y="{yy + 4}" width="{w}" height="24" rx="4" '
                       f'fill="{c}18" stroke="{c}" stroke-width="1.1"/>')
        d.t(LX + LABW + w + 12, yy + 20, f"{bits} bit", 11, MUTED if c is not ACC else ACC,
            MONO, "start")


block(TCP_Y, "TCP", "RFC 9293(구 793) · 연결 지향 · 순서와 재전송을 보장", fields_tcp, OK)
block(UDP_Y, "UDP", "RFC 768 · 비연결", fields_udp, INFO)

RX = 560
d.o.append(f'<rect x="{RX}" y="{TCP_Y}" width="288" height="204" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(RX + 20, TCP_Y + 30, "TCP 에만 있는 넷", 14, ACC, KR, "start", 600)
for i, (n, why) in enumerate([("Sequence number", "순서대로 전달"),
                              ("Acknowledgment number", "3방향 핸드셰이크의 핵심"),
                              ("Flags", "SYN 과 ACK"),
                              ("Window", "받을 수 있는 양")]):
    yy = TCP_Y + 56 + i * 40
    d.t(RX + 20, yy, n, 11, ACC, MONO, "start")
    d.t(RX + 20, yy + 17, why, 11.5, MUTED, KR, "start")

d.tone(RX, TCP_Y + 220, 288, 84, WARN)
d.t(RX + 20, TCP_Y + 248, "TCP 에는 방어 장치가 없습니다", 12.5, INK, KR, "start", 600)
d.t(RX + 20, TCP_Y + 270, "페이로드가 평문으로 갑니다. 사이의", 11, MUTED, KR, "start")
d.t(RX + 20, TCP_Y + 288, "누구든 볼 수 있으니 TLS 1.3 을 씁니다.", 11, MUTED, KR, "start")

RIGHT3_Y = TCP_Y + 320
d.tone(RX, RIGHT3_Y, 288, 84, INFO)
d.t(RX + 20, RIGHT3_Y + 28, "UDP 가 얻는 것", 12.5, INK, KR, "start", 600)
d.t(RX + 20, RIGHT3_Y + 50, "오버헤드가 아주 적어 높은 처리량을", 11, MUTED, KR, "start")
d.t(RX + 20, RIGHT3_Y + 68, "냅니다. NTP · DHCP · DNS 가 씁니다.", 11, MUTED, KR, "start")

d.legend(620, [("두 프로토콜에 공통", OK), ("TCP 에만 있는 것", ACC),
               ("UDP 고유", INFO), ("암호화가 필요한 이유", WARN)])
d.save("07-02.tcp-udp-header.svg")
print("ok 07-02.tcp-udp-header")
