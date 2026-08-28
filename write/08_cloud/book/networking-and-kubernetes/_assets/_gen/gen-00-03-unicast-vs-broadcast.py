# 00-03-unicast-vs-broadcast — 목적지 MAC 칸 하나가 받는 쪽 처리를 가른다
# 본문 요구: "허브에 붙은 같은 네 대. 프레임이 다른 곳은 목적지 MAC 칸 하나뿐이다."
#           값이 달라지는 그 칸이 초점이고, 오른쪽 끝의 처리 대수가 결과다.
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 행이 두 프레임, 열이 목적지 MAC 칸과
#           랜카드 세 대의 처리 결과. 같은 열끼리 세로로 맞춰 읽는 것이 논지다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, PAPER, KR, MONO

W, H = 1000, 528
RX, RW, RH, Y0 = 100, 840, 132, 164
CARDS = [420, 564, 708]                      # 2·3·4 번 랜카드 열
ROWS = [("유니캐스트", "2a:4f:1b:8c:d2:e0", "2 번 랜카드의 MAC 을 적었습니다",
         [(OK, "처리"), (BAD, "버림"), (BAD, "버림")], "1 / 3"),
        ("브로드캐스트", "ff:ff:ff:ff:ff:ff", "예약된 값이라 전원이 자기 것으로 봅니다",
         [(OK, "처리"), (OK, "처리"), (OK, "처리")], "3 / 3")]

d = D(W, H, "FRAME COMPARISON · ONE FIELD",
      "한 칸의 값이 바뀌면 받는 쪽 처리가 갈린다",
      "같은 허브에 붙은 네 대에 같은 프레임을 두 번 보낸 결과를 위아래로 나란히 둔 비교. "
      "위는 목적지 MAC 칸에 특정 MAC 을 적은 유니캐스트로 한 대만 처리하고 두 대가 버린다. "
      "아래는 같은 칸에 FF:FF:FF:FF:FF:FF 를 적은 브로드캐스트로 세 대 모두 처리한다.",
      lead="허브에 붙은 같은 네 대. 프레임이 다른 곳은 목적지 MAC 칸 하나뿐입니다.")

# 열 머리
d.line(RX, 128, RX + RW, 128, RULE, 0.8)
d.t(120, 152, "목적지 MAC 칸", 9, SOFT, KR, "start")
for cx, no in zip(CARDS, ("2 번", "3 번", "4 번")):
    d.t(cx + 32, 152, no, 9, SOFT, KR, "start")
d.t(RX + RW - 20, 152, "처리한 대수", 9, SOFT, KR, "end")

for r, (kind, mac, note, cells, tally) in enumerate(ROWS):
    y = Y0 + r * RH
    d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" fill="{PAPER}"/>')
    d.line(RX, y, RX + RW, y, RULE, 0.8)
    d.t(120, y + 32, kind, 15, INK, KR, "start", 600)
    d.tone(120, y + 48, 248, 36, ACC, 4, "12", 1.2)
    d.t(136, y + 72, mac, 13, ACC, MONO, "start")
    d.t(120, y + 112, note, 12, MUTED, KR, "start")
    for cx, (c, verb) in zip(CARDS, cells):
        d.tone(cx, y + 32, 112, 64, c, 6, "12", 1.2)
        d.t(cx + 56, y + 60, "받아서", 13, c, KR, "middle", 600)
        d.t(cx + 56, y + 82, verb, 13, c, KR, "middle", 600)
    d.t(RX + RW - 20, y + 70, tally, 18, INK, MONO, "end", 600)
d.line(RX, Y0 + 2 * RH, RX + RW, Y0 + 2 * RH, RULE, 0.8)

# 원본과 같이 두 줄로 나눈다 — 한 줄로 두면 오른쪽 여백을 넘는다
d.t(RX, 448, "허브는 아무것도 읽지 않아 두 경우 모두 세 대에 그대로 도착합니다.", 12, MUTED, KR, "start")
d.t(RX, 468, "갈리는 것은 받은 쪽이 처리하는가 버리는가뿐이고, 그 판정은 받는 랜카드가 합니다.", 12, MUTED, KR, "start")
d.legend(484, [("값이 갈리는 칸", ACC), ("처리", OK), ("버림", BAD)])
d.save("00-03-unicast-vs-broadcast.svg")
print("ok unicast-vs-broadcast")
