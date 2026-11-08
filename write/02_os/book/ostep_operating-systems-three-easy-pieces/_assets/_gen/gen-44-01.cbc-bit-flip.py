# 44-01 「암호화만으로는 변조를 막지 못한다」 — CBC 모드에서 첫 암호문 블록의 한 비트를 뒤집으면 복호 결과가 어떻게 바뀌는지.
# 첫 평문 블록은 알아볼 수 없게 깨지고, 둘째 평문 블록은 같은 자리의 한 글자만 바뀐다. 복호는 오류 없이 끝난다.
# 검증 근거: openssl 3.6.4 로 AES-256-CBC 암호문 c.bin 의 4번째 바이트에 ^1 을 적용해 복호한 xxd 출력.
#   00000000: 8e70 c33f 8a20 c8d2 ...(첫 블록은 실행마다 다름)
#   00000010: 206d 7921 7361 7669 6e67 7320 6163 636f   my!savings acco
# 구조 근거: CBC 복호는 P2 = D(C2) XOR C1 이라 C1 의 바뀐 비트가 P2 의 같은 자리로 그대로 옮겨 간다.
# 타입 스펙: type-data-flow — 블록마다 값이 어떻게 바뀌어 흐르는지. 위 행은 C1 에서 P1', 아래 행은 C2 에서 P2' 이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 412
BH = 76
R1, R2 = 108, 252
CX, CW = 24, 192      # 암호문 블록
DX, DW = 288, 168     # 복호 상자
XX, XW = 528, 104     # XOR 상자
PX, PW = 760, 216     # 복호된 평문 블록

d = D(W, H, "OSTEP · 44-01 CBC",
      "첫 암호문 블록의 한 비트가 둘째 평문 블록의 같은 자리를 바꾼다",
      "위 행은 암호문 블록 C1 이 복호된 뒤 IV 와 XOR 되어 알아볼 수 없는 평문 블록 P1' 이 되는 흐름이다. "
      "아래 행은 C2 가 복호된 뒤 C1 과 XOR 되어 P2' 가 되는 흐름이고 C1 에서 뒤집힌 비트가 P2' 의 같은 자리에 그대로 나타난다. 복호는 오류 없이 끝난다.",
      lead="AES-256-CBC 로 암호화한 한 줄의 평문에서 C1 의 4번째 바이트를 0x01 과 XOR 한 실험이다.")


def cell(x, y, w, title, sub, c, mono_sub=False, focal=False):
    d.tone(x, y, w, BH, c, 6, "14", 1.4 if focal else 1.1)
    d.t(x + w / 2, y + 32, title, 14, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 56, sub, 13, MUTED, MONO if mono_sub else KR)


def hline(x1, x2, y, c=MUTED, m="ar"):
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.4)


# 위 행: C1 -> D -> P1'
cell(CX, R1, CW, "C1", "4번째 바이트 1비트 반전", ACC, focal=True)
cell(DX, R1, DW, "복호 D(K)", "같은 키 K", INFO)
cell(XX, R1, XW, "XOR", "IV 와 합침", INFO)
cell(PX, R1, PW, "P1' — 알아볼 수 없음", "8e70 c33f 8a20 c8d2 …", BAD, mono_sub=True)
hline(CX + CW, DX, R1 + BH / 2)
hline(DX + DW, XX, R1 + BH / 2)
hline(XX + XW, PX, R1 + BH / 2, BAD, "bad")
d.chip(PX + PW / 2, R1 - 16, "블록 전체가 깨짐", BAD, 12)

# 아래 행: C2 -> D -> XOR -> P2'
cell(CX, R2, CW, "C2", "바뀌지 않음", SOFT)
cell(DX, R2, DW, "복호 D(K)", "같은 키 K", INFO)
cell(XX, R2, XW, "XOR", "C1 과 합침", INFO)
cell(PX, R2, PW, "P2' — 한 글자만 바뀜", '" my!savings acco"', ACC, mono_sub=True, focal=True)
hline(CX + CW, DX, R2 + BH / 2)
hline(DX + DW, XX, R2 + BH / 2)
hline(XX + XW, PX, R2 + BH / 2, ACC, "acc")
d.chip(PX + PW / 2, R2 - 16, "원래 my savings", MUTED, 12)

# C1 이 아래 행의 XOR 로 들어가는 길 (위 행과 아래 행 사이를 가로지름)
GAP_Y = (R1 + BH + R2) // 2
d.arrow([(CX + CW / 2, R1 + BH + 2), (CX + CW / 2, GAP_Y), (XX + XW / 2, GAP_Y), (XX + XW / 2, R2 - 4)], ACC, "acc", 1.5)
d.chip(CX + CW / 2 + 240, GAP_Y - 16, "바뀐 비트가 그대로 XOR 로 들어감", ACC, 12)

d.legend(372, [("바뀐 비트와 그 결과", ACC), ("알아볼 수 없게 깨진 블록", BAD), ("연산", INFO), ("바뀌지 않은 입력", SOFT)])
d.save("44-01.cbc-bit-flip.svg")
