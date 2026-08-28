# 00-03-arp-message-fields — 빈 칸 하나가 채워져 돌아온다
# 본문 요구: "아는 것을 적고 모르는 칸을 비워 보낸다" — 비었다가 채워지는 칸이 초점이다.
#           입력은 IP, 출력은 MAC 이라는 대조가 요점.
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 요청과 응답을 위아래로 두고 같은 칸끼리
#           세로로 맞춰 읽는다. 비어 있던 자리가 채워지는 것이 세로 대조로만 보인다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 1000, 640
FX, FW, FH, VX, NX = 120, 820, 36, 420, 920
REQ = [("보내는 쪽 IP", "10.0.0.5", "내 주소", None, False),
       ("보내는 쪽 MAC", "2a:4f:1b:8c:d2:e0", "랜카드에 이미 있다", None, False),
       ("찾는 쪽 IP", "10.0.0.1", "입력 — 이걸로 묻는다", INFO, True),
       ("찾는 쪽 MAC", "00:00:00:00:00:00", "비워 둔다 — 모르는 칸", ACC, True)]
RES = [("보내는 쪽 IP", "10.0.0.1", "아까 찾던 그 주소", None, False),
       ("보내는 쪽 MAC", "b8:27:eb:14:aa:03", "출력 — 비었던 값이 여기 담긴다", OK, True),
       ("찾는 쪽 IP · MAC", "10.0.0.5 · 2a:4f:1b:8c:d2:e0", "요청 프레임에서 이미 알았다", None, False)]

d = D(W, H, "ARP MESSAGE FIELDS",
      "빈 칸 하나가 채워져 돌아온다",
      "ARP 요청과 응답의 네 칸을 위아래로 나란히 둔 대조. 요청에서는 찾는 쪽 MAC 칸이 비어 있고, "
      "응답에서는 그 칸이 채워져 자리를 바꿔 돌아온다.",
      lead="ARP 메시지에는 칸이 넷입니다. 아는 것을 적고 모르는 칸을 비워 보냅니다.")

def block(y0, title, tc, who, rows):
    d.t(FX, y0, title, 13, tc, KR, "start", 600)
    d.t(NX, y0, who, 12, MUTED, KR, "end")
    for i, (label, val, note, c, bold) in enumerate(rows):
        y = y0 + 16 + i * 40
        if c:
            d.tone(FX, y, FW, FH, c, 4, "12", 1.2)
        else:
            d.o.append(f'<rect x="{FX}" y="{y}" width="{FW}" height="{FH}" rx="4" fill="{PAPER2}"/>')
        d.t(FX + 20, y + 24, label, 12, c or MUTED, KR, "start", 600 if bold else 400)
        d.t(VX, y + 24, val, 13, c or INK, MONO, "start", 600 if bold and c else 400)
        d.t(NX, y + 24, note, 11, c or SOFT, KR, "end", 600 if bold and c else 400)

block(156, "요청 — 브로드캐스트로 나간다", INFO, "보내는 쪽: 10.0.0.5", REQ)
d.t(530, 360, "10.0.0.1 이 받아서 자리를 바꿔 답한다", 13, MUTED, KR)
block(408, "응답 — 그 한 대에게만 유니캐스트", OK, "보내는 쪽: 10.0.0.1", RES)

d.t(FX - 20, 572, "입력은 IP, 출력은 MAC 입니다. 응답의 마지막 줄이 채워져 있어 양쪽이 한 번에 서로를 알게 됩니다.",
    12, MUTED, KR, "start")
d.legend(588, [("입력 — 묻는 값", INFO), ("비어 있는 칸", ACC), ("출력 — 채워진 값", OK)])
d.save("00-03-arp-message-fields.svg")
print("ok arp-message-fields")
