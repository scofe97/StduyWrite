# 01-01.encapsulation-roundtrip — 송신은 감싸며 내려가고 수신은 벗기며 올라간다
# 본문 요구(01-01 §2): "왼쪽은 계층을 내려가며 헤더를 하나씩 붙이고, 오른쪽은 같은 순서를
#           거꾸로 밟으며 그 헤더를 벗깁니다. 가운데 물리 매체는 자기가 나르는 비트가 어느
#           계층의 것인지 알지 못합니다." 본문이 세 가지를 규격으로 못 박은 자리다 —
#           (1) 두 기둥이 거울처럼 마주 볼 것, (2) 헤더가 한 겹씩 늘고 줄 것, (3) 가운데 매체가
#           아무것도 모른다는 것. 그래서 오른쪽 화살표는 위로 향하고, 가운데 칩은 왼쪽이 +,
#           오른쪽이 − 다.
#           "각 계층은 자기가 붙인 헤더만 읽으면 되고 위아래 계층이 무엇을 담았는지는 몰라도
#           된다"가 이 그림의 결론이라, payload 칸을 일곱 줄 내내 같은 색·같은 자리에 둔다 —
#           안쪽이 무엇이든 그 계층에는 그냥 payload 다.
# 타입 스펙: type-layers.md — 위아래로 쌓인 추상 수준 일곱. 다만 한 벌이 아니라 두 벌을
#           마주 세운 형태다. 계층 자체보다 계층을 오르내리며 헤더가 붙고 떨어지는 것이
#           논지라, 각 줄 오른쪽에 그 시점의 PDU 를 막대로 함께 그린다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 916, 652
TX, RX, COLW = 12, 538, 330       # 송신 기둥 · 수신 기둥
ROW_Y, ROW_H, STRIDE = 132, 52, 60
PAY_DX, PAY_W, HDR_W = 198, 118, 22   # 기둥 안에서 payload 칸이 시작하는 자리
MID = (TX + COLW + RX) / 2        # 두 기둥 사이 한가운데
MIDI = (TX + COLW + RX) // 2      # 칩은 정수 자리에 놓는다 — 원본 좌표를 그대로 옮겼다
TCX, RCX = TX + COLW / 2, RX + COLW / 2

d = D(W, H, "ENCAPSULATION · 01-01 OSI",
      "송신은 감싸며 내려가고 수신은 벗기며 올라간다",
      "OSI 캡슐화의 왕복. 송신 호스트는 계층을 내려가며 헤더를 하나씩 붙여 PDU를 키우고, "
      "수신 호스트는 같은 순서를 거꾸로 밟으며 그 헤더를 벗긴다. 가운데 물리 매체는 자기가 "
      "나르는 비트가 어느 계층의 것인지 알지 못한다.",
      lead="각 계층은 자기가 붙인 헤더만 읽습니다 — 위아래가 무엇을 담았는지는 몰라도 됩니다.")

d.t(TCX, 112, "송신 호스트 — 감싼다 (encapsulate)", 11, SOFT, MONO)
d.t(RCX, 112, "수신 호스트 — 벗긴다 (decapsulate)", 11, SOFT, MONO)

# (계층, PDU, 색, 이 계층에서 새로 붙는 헤더) — 헤더가 None 이면 앞 줄 것을 그대로 물려받는다
ROWS = [("Application",  "Data",    INFO, None),
        ("Presentation", "Data",    INFO, None),
        ("Session",      "Data",    INFO, None),
        ("Transport",    "Segment", OK,   "TCP"),
        ("Network",      "Packet",  WARN, "IP"),
        ("Data Link",    "Frame",   ACC,  "Eth"),
        ("Physical",     "Bit",     BAD,  None)]

hdrs = []                          # 지금까지 붙은 헤더 — 먼저 붙은 것이 바깥(왼쪽)이다
for i, (name, pdu, c, new_hdr) in enumerate(ROWS):
    y = ROW_Y + STRIDE * i
    if new_hdr:
        hdrs.append((new_hdr, c))
    for x0, cx in ((TX, TCX), (RX, RCX)):
        px = x0 + PAY_DX
        d.box(x0, y, COLW, ROW_H, PAPER2, RULE, 0.9)
        d.t(x0 + 14, y + 21, name, 12, c, KR, "start", 600)
        d.t(x0 + 14, y + 39, pdu, 9, MUTED, MONO, "start")
        for j, (_lab, hc) in enumerate(hdrs):
            d.tone(px - HDR_W * (len(hdrs) - j), y + 13, HDR_W, 26, hc, 2, "33", 0.9)
        d.tone(px, y + 13, PAY_W, 26, INFO, 2, "22", 0.9)
        d.t(px + PAY_W / 2, y + 30, "payload", 9, INFO, MONO)
    if i < len(ROWS) - 1:          # 왼쪽은 내려가고 오른쪽은 올라간다
        d.path(f"M {TCX} {y+ROW_H+2} L {TCX} {y+ROW_H+5}", MUTED, 1.4, m="ar")
        d.path(f"M {RCX} {y+ROW_H+5} L {RCX} {y+ROW_H+2}", MUTED, 1.4, m="ar")
    if new_hdr:                    # 왼쪽은 붙이고 오른쪽은 뗀다 — 같은 헤더의 두 방향
        d.chip(MIDI - 68, y + ROW_H / 2, f"+{new_hdr}", c, 9)
        d.chip(MIDI + 68, y + ROW_H / 2, f"−{new_hdr}", c, 9)

BOT = ROW_Y + STRIDE * 6 + ROW_H + 2
d.path(f"M {TCX} {BOT} L {TCX} {BOT+24} L {RCX} {BOT+24}", BAD, 1.5, m="bad")
d.t(MID, 592, "물리 매체 — 나르는 비트가 어느 계층 것인지 모른다", 11, SOFT)

d.legend(608, [("payload", INFO), ("+Transport", OK), ("+Network", WARN), ("+Link", ACC)])
d.save("01-01.encapsulation-roundtrip.svg")
print("ok encapsulation-roundtrip")
