# 04-01 §4 ClientKeyExchange — TLS 1.2 최초 전체 핸드셰이크에서 같은 메시지의 다른 내용물.
# 본문 요구: "이 메시지가 보이면 pre_master_secret 이 정해졌다는 뜻이고, 그 방식은 고른 키 교환에 따라
#            갈립니다. RSA 로 암호화한 비밀을 전송하거나, Diffie-Hellman 파라미터를 보내거나 둘 중 하나입니다."
#            메시지 이름은 하나인데 안에 실리는 것과 서버가 그것으로 하는 일이 정반대라, 이름만으로는 안 갈린다.
# 타입 스펙: type-data-flow — 같은 단계에서 *무엇이* 흐르고 그것을 받아 *누가* 무엇을 하는지.
#           위아래 두 갈래가 같은 메시지의 두 내용물이고, 오른쪽 끝이 양쪽이 도달하는 같은 결과다.
#           focal 은 갈라지는 지점이 아니라 만나는 지점 — 어느 길이든 pre_master_secret 하나로 모인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 640
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §4",
      "같은 메시지, 안에 실리는 것은 정반대",
      "TLS 1.2 최초 전체 핸드셰이크에서 ClientKeyExchange 에 실리는 것은 정적 RSA 에서는 "
      "클라이언트가 만든 비밀의 암호문이고, DHE·ECDHE에서는 비밀이 아니라 클라이언트의 공개값이다. "
      "앞의 것은 서버가 개인키로 풀어 얻고, 뒤의 것은 양쪽이 각자 계산해 같은 값에 도달한다.",
      "TLS 1.2: RSA 는 암호화한 비밀을 보내고, DHE·ECDHE 는 공개값으로 같은 비밀을 계산합니다")

NW, NH = 248, 84
C0, C1, C2 = 152, 456, 776        # 클라이언트가 한 일 · 선에 실린 것 · 서버가 한 일
YA, YB = 232, 396                 # 정적 RSA · 임시 방식
MEET_Y = 540

def card(cx, cy, title, sub, c=None, focal=False, w=NW, h=NH):
    x, y = cx - w / 2, cy - h / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, w, h, c, 8)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(cx, y + 32, title, 13, col, KR, "middle", 600)
    d.t(cx, y + 56, sub, 11, MUTED, KR)

def hop(x1, x2, y, c):
    d.arrow([(x1 + NW / 2, y), (x2 - NW / 2 - 8, y)], c, "acc" if c is ACC else "ar", 1.5)

# 열 머리
for cx, lab in ((C0, "클라이언트가 한 일"), (C1, "ClientKeyExchange 에 실리는 것"), (C2, "서버가 하는 일")):
    d.t(cx, 148, lab, 13, SOFT, KR)

# A · 정적 RSA
d.t(24, YA - 58, "A · 정적 RSA", 12, INFO, KR, "start", 600)
card(C0, YA, "비밀을 직접 만듦", "pre_master_secret", c=INFO)
card(C1, YA, "비밀의 암호문", "서버 RSA 공개키로 암호화", c=INFO)
card(C2, YA, "개인키로 풀어 꺼냄", "받은 값이 곧 비밀", c=INFO)
hop(C0, C1, YA, INFO); hop(C1, C2, YA, INFO)

# B · 임시 방식
d.t(24, YB - 58, "B · DHE · ECDHE", 12, ACC, KR, "start", 600)
card(C0, YB, "임시 키 쌍을 만듦", "비밀은 안 보냄", c=ACC)
card(C1, YB, "공개값만", "이것만으로는 비밀이 안 나옴", c=ACC)
card(C2, YB, "자기 임시 키로 계산", "양쪽이 각자 도달", c=ACC)
hop(C0, C1, YB, ACC); hop(C1, C2, YB, ACC)

# 두 갈래가 만나는 곳.
# A 는 B 행 카드를 세로로 관통하지 않도록 오른쪽 바깥 통로로 내려오고,
# B 는 자기 카드 밑에서 바로 내려온다. 두 수평 진입선의 y 를 벌려 화살촉이 붙지 않게 한다.
FX = C1 + 160 + 8                 # focal 오른쪽 변 + 화살촉 여유
AISLE = C2 + NW / 2 + 24          # A 가 내려오는 바깥 통로
d.arrow([(C2, YB + NH / 2), (C2, 524), (FX, 524)], ACC, "ar", 1.4)
d.arrow([(C2 + NW / 2, YA), (AISLE, YA), (AISLE, 558), (FX, 558)], INFO, "ar", 1.4)
card(C1, MEET_Y, "pre_master_secret", "여기서부터 master_secret 과 세션 키", focal=True, w=320, h=76)

d.t(24, MEET_Y + 4, "A: 암호화된 비밀 전송", 12, INFO, KR, "start")
d.t(24, MEET_Y + 26, "B: 임시 공개값만 전송", 12, ACC, KR, "start")
d.t(24, MEET_Y + 48, "서버 개인키 복호화 조건은 04-02", 12, MUTED, KR, "start")

d.legend(H - 40, [("합의한 비밀", ACC), ("RSA 로 암호화된 비밀 전송", INFO)])
d.save("04-01.client-key-exchange.svg")
