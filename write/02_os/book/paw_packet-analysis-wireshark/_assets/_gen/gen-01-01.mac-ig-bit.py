# 01-01 §4 — MAC 주소 첫 옥텟의 최하위 비트(IG 비트)가 한 대인지 무리인지 가른다.
# 본문 요구: "첫 옥텟을 8비트로 펼치면 맨 오른쪽 비트가 IG 비트입니다. 첫 옥텟이 홀수면 그룹 주소입니다."
#            표는 주소 값만 보여 주고 *어느 비트*가 판단 근거인지는 안 보인다. 세 주소의 첫 옥텟을
#            같은 8칸 격자로 펼쳐 IG 칸을 세로 한 줄로 맞추면, 그 한 칸만 0·1 로 갈리는 것이 보인다.
# 타입 스펙: type-layers — 주소 한 줄을 조각(첫 옥텟 → 8비트)으로 나눈 층. 가로 위치가 곧 비트 자리이고,
#           focal 은 세 줄을 관통하는 IG 비트 열 하나다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 468
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §4",
      "IG 비트 — MAC 첫 옥텟의 최하위 비트",
      "유니캐스트 00:00:5e:00:53:01, 브로드캐스트 ff:ff:ff:ff:ff:ff, mDNS 멀티캐스트 01:00:5e:00:00:fb 의 첫 옥텟을 "
      "8비트로 펼쳤다. 맨 오른쪽 비트가 IG 비트이고 0 이면 장비 한 대, 1 이면 무리를 가리키는 주소다.",
      "첫 옥텟이 홀수면 그룹 주소입니다 — 스위치와 NIC 는 이 한 비트로 받을 범위를 정합니다")

LX = 40                          # 종류·MAC 글자 x
OCT_CX, OCT_W = 284, 52          # 첫 옥텟 칸
BX0, BW, BG = 336, 40, 4         # 8비트 칸 시작 · 폭 · 간격
RX = 716                         # 결과 칸 글자 x
Y0, RS, CH = 164, 72, 44         # 첫 줄 위 · 줄 stride · 칸 높이
ROWS = [  # (종류, MAC, 첫 옥텟, 8비트, 결과, 받는 쪽)
    ("유니캐스트",       "00:00:5e:00:53:01", "00", "00000000", "개별 주소", "장비 한 대"),
    ("브로드캐스트",     "ff:ff:ff:ff:ff:ff", "ff", "11111111", "그룹 주소", "링크의 모두"),
    ("멀티캐스트 · mDNS", "01:00:5e:00:00:fb", "01", "00000001", "그룹 주소", "가입한 무리"),
]

def bx(i): return BX0 + i * (BW + BG) + (8 if i == 7 else 0)   # i 번째 비트 칸의 왼쪽 x (0 = 최상위) · IG 칸만 focal 테두리 몫 8 을 띄운다
IG_X = bx(7)

# 열 머리
d.t(LX, 124, "목적지 MAC", 13, INK, KR, "start", 600)
d.t(LX, 142, "종류 · 주소", 12, MUTED, KR, "start")
d.t(OCT_CX, 124, "첫 옥텟", 13, INK, KR, "middle", 600)
d.t(OCT_CX, 142, "16진수", 12, MUTED, KR, "middle")
d.t((BX0 + bx(6) + BW) / 2, 124, "첫 옥텟을 8비트로", 13, INK, KR, "middle", 600)
d.t((BX0 + bx(6) + BW) / 2, 142, "왼쪽이 상위 비트", 12, MUTED, KR, "middle")
d.t(IG_X + BW / 2, 124, "IG", 13, ACC, MONO, "middle", 600)
d.t(IG_X + BW / 2, 142, "최하위", 12, ACC, KR, "middle")
d.t(RX, 124, "판정", 13, INK, KR, "start", 600)
d.t(RX, 142, "받는 쪽", 12, MUTED, KR, "start")
d.line(24, 152, 856, 152, RULE, 0.8)

# focal — IG 열 하나가 세 줄을 관통한다. 칸보다 먼저 깔아 칸 테두리가 위에 오게 한다
top, bottom = Y0 + 12, Y0 + (len(ROWS) - 1) * RS + 12 + CH
d.o.append(f'<rect x="{IG_X - 6}" y="{top - 8}" width="{BW + 12}" height="{bottom - top + 16}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')

for r, (kind, mac, octet, bits, verdict, who) in enumerate(ROWS):
    y = Y0 + r * RS
    cy = y + 12                                  # 칸 위
    if r:
        d.line(24, y - 4, 856, y - 4, RULE, 0.6)
    # 종류 · 주소
    d.t(LX, y + 26, kind, 13, INK, KR, "start", 600)
    d.t(LX, y + 46, mac, 12, MUTED, MONO, "start")
    # 첫 옥텟
    d.tone(OCT_CX - OCT_W / 2, cy, OCT_W, CH, INFO, 6)
    d.t(OCT_CX, cy + 27, octet, 14, INFO, MONO, "middle", 600)
    # 8비트 — 앞 일곱 칸은 중립, 마지막 칸은 focal 열 안에서 강조
    for i, b in enumerate(bits):
        x = bx(i)
        if i == 7:
            d.box(x, cy, BW, CH, PAPER, ACC, 1.2, 6)
            d.t(x + BW / 2, cy + 28, b, 16, ACC, MONO, "middle", 700)
        else:
            d.box(x, cy, BW, CH, PAPER2, RULE, 1.0, 6)
            d.t(x + BW / 2, cy + 28, b, 14, MUTED, MONO, "middle")
    # 판정
    d.t(RX, y + 26, verdict, 13, INK, KR, "start", 600)
    d.t(RX, y + 46, who, 12, MUTED, KR, "start")

d.chip(W / 2 - 12, 392, "Wireshark 필드 eth.dst.ig — 1 이면 그룹 주소", MUTED, 12)

d.legend(H - 48, [("IG 비트 — 0 한 대 · 1 무리", ACC), ("첫 옥텟", INFO)])
d.save("01-01.mac-ig-bit.svg")
