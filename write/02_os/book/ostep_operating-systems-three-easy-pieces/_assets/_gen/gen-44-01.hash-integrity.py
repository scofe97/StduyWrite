# 44-01 「해시를 서명하면 변조가 비교에서 드러난다」 — 받는 쪽은 서명에서 복호한 해시 S 와 받은 문장의 해시를 계산해 비교하고, 다르면 변조로 본다.
# 본문 근거: 이 노트 「3. 해시만 서명해 무결성을 싸게 확인한다」.
# 검증 근거: openssl 3.6.4 로 'Transfer $100 to my savings account' 와 '$101' 의 SHA-256 을 계산해 256비트 중 126비트가 달라짐을 확인.
#   $100 -> d9f26f8ef8b97c12..., $101 -> f560acf0ee15e698... (이 도식은 앞 8자리만 쓴다).
# 구조 근거: 보내는 쪽은 P 의 해시 S 를 서명해 P 와 함께 보낸다. 공격자가 P 를 P' 로 바꿔도 서명된 S 는 만들 수 없다.
# 타입 스펙: type-flowchart — 입력 둘이 비교 분기 하나로 모이고, 같음과 다름으로 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 404
BW, BH = 192, 76
R1, R2 = 108, 252
LX, MX = 24, 288          # 왼쪽 열, 가운데 열
DCX, DCY = 576, 218       # 분기 마름모 중심
DHW, DHH = 72, 44
FX = 716                  # 분기 뒤 갈림 지점
OX = 792                  # 결과 열

d = D(W, H, "OSTEP · 44-01 HASH",
      "서명된 해시와 다시 계산한 해시가 다르면 변조이다",
      "위 줄은 받은 서명에서 해시 S 를 복호하는 흐름이고 아래 줄은 받은 문장 P' 의 해시를 계산하는 흐름이다. "
      "두 값이 마름모에서 만나 같으면 변조 없음이고 다르면 변조 의심이다. 공격자가 문장을 $100 에서 $101 로 바꾸면 SHA-256 의 256비트 중 126비트가 달라진다.",
      lead="SHA-256 으로 'Transfer $100 …' 과 'Transfer $101 …' 을 해시한 실제 값이다.")


def cell(x, y, w, title, sub, c, mono_sub=False, focal=False):
    d.tone(x, y, w, BH, c, 6, "14", 1.4 if focal else 1.1)
    d.t(x + w / 2, y + 32, title, 14, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 56, sub, 13, MUTED, MONO if mono_sub else KR)


def hline(x1, x2, y, c=MUTED, m="ar"):
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.4)


# 위 줄: 받은 서명 -> 복호한 S
cell(LX, R1, BW, "받은 서명", "보낸 쪽이 만든 값", SOFT)
cell(MX, R1, 208, "서명에서 복호한 S", "d9f26f8e …", INFO, mono_sub=True)
hline(LX + BW, MX, R1 + BH / 2)

# 아래 줄: 받은 문장 -> 해시 계산
cell(LX, R2, BW, "받은 문장 P'", "Transfer $101 …", ACC, mono_sub=True, focal=True)
cell(MX, R2, 208, "H(P') 계산", "f560acf0 …", INFO, mono_sub=True)
hline(LX + BW, MX, R2 + BH / 2, ACC, "acc")
d.chip(LX + BW + 48, R2 - 16, "$100 에서 바뀜", ACC, 12)

# 두 값이 마름모로 모인다
TOPX = DCX
d.arrow([(MX + 208 + 2, R1 + BH / 2), (TOPX, R1 + BH / 2), (TOPX, DCY - DHH - 4)], MUTED, "ar", 1.4)
d.arrow([(MX + 208 + 2, R2 + BH / 2), (TOPX, R2 + BH / 2), (TOPX, DCY + DHH + 4)], MUTED, "ar", 1.4)

d.o.append(f'<path d="M {DCX} {DCY - DHH} L {DCX + DHW} {DCY} L {DCX} {DCY + DHH} L {DCX - DHW} {DCY} Z" '
           f'fill="{SOFT}14" stroke="{SOFT}" stroke-width="1.1"/>')
d.t(DCX, DCY + 5, "S 와 같은가", 12, INK, KR, "middle", 600)

# 갈림: 같음은 위, 다름은 아래
d.path(f"M {DCX + DHW + 2} {DCY} L {FX} {DCY}", MUTED, 1.4)
d.arrow([(FX, DCY), (FX, R1 + BH / 2), (OX - 4, R1 + BH / 2)], OK, "ok", 1.4)
d.arrow([(FX, DCY), (FX, R2 + BH / 2), (OX - 4, R2 + BH / 2)], BAD, "bad", 1.4)
d.chip(FX + 36, R1 + BH / 2 - 16, "같음", OK, 12)
d.chip(FX + 36, R2 + BH / 2 + 16, "다름", BAD, 12)

cell(OX, R1, BW, "변조 없음", "받은 문장을 받아들임", OK)
cell(OX, R2, BW, "변조 의심", "126비트가 다름", BAD)

d.legend(364, [("받은 값", SOFT), ("계산하는 연산", INFO), ("바뀐 문장", ACC), ("같음", OK), ("다름", BAD)])
d.save("44-01.hash-integrity.svg")
