# 07-01 §2 — 층을 갈아 끼워도 가운데가 안 고쳐지는 이유.
# 원문("The TCP/IP Stack"): "Each layer must be aware of and able to communicate with only the layers
#       right above and below itself." 그리고 "the internet layer takes the packet it gets from the
#       transport layer, treats it as an opaque chunk of bytes, and can focus on its function, the
#       routing of the packet to the target machine."
# 노트의 읽기: 원서는 규칙과 불투명성까지만 적고, 그 규칙이 무엇을 사게 하는지는 말하지 않는다.
#       이 도식이 그 자리를 채운다 — 위(전송)와 아래(링크)를 둘 다 갈아 끼운 뒤에도 가운데(인터넷)가
#       그대로라는 것을 나란히 놓고 보인다. 교체 사례는 원서 밖이므로 전부 노트의 읽기다.
# 타입 스펙: type-layers — 같은 계층 스택을 두 구성으로 나란히 놓은 두 열 변형이다. 행은 계층이라
#       위계가 있고, 열은 교체 전후다. coral 은 하나뿐이며 그 자리가 갈아 끼우지 않은 인터넷 계층이다.
#       축약: 헤더 필드와 캡슐화 방향은 07-01.tcp-ip-stack.svg 가 이미 맡았으므로 반복하지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, KR, MONO

W, H = 880, 706
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §2",
      "위아래를 갈아 끼워도 가운데는 고쳐지지 않는다",
      "각 층은 바로 위와 바로 아래만 알면 되므로, 전송 계층을 TCP 에서 QUIC 으로 바꾸고 "
      "링크 계층을 이더넷에서 WiFi 로 바꿔도 인터넷 계층의 코드는 그대로다. "
      "서로를 모르는 것이 곧 교체 가능성이다.",
      "각 층이 바로 위아래만 알기 때문에 생기는 성질입니다")

AX, BX, CW = 64, 530, 286
Y0, LH, GAP = 160, 76, 12
MID_L, MID_R, MID_C = AX + CW + 6, BX - 6, (AX + CW + BX) / 2
CHIP_SIZE = 11.5

d.t(AX + CW / 2, 140, "교체 전", 12, MUTED, KR, "middle", 600)
d.t(BX + CW / 2, 140, "교체 후", 12, MUTED, KR, "middle", 600)

# 색은 계층에 붙는다 — 형제 도식 07-01.tcp-ip-stack.svg 와 같은 배정이라 두 장을 겹쳐 읽을 수 있다.
# 그래서 교체 표시는 색이 아니라 화살표와 칩의 글자가 나른다. 색을 겸용하면 범례가 거짓말을 한다.
rows = [
    # (L번호, 색, 왼쪽 이름·설명, 오른쪽 이름·설명, 가운데 칩, 칩 색, 화살표 여부)
    ("7", WARN, ("HTTP", "웹 요청과 응답"), ("HTTP", "전송이 바뀐 줄 모른다"),
     "그대로", SOFT, False),
    ("4", OK, ("TCP", "순서와 재전송을 보장한다"), ("QUIC", "UDP 위에 얹은 전송"),
     "갈아 끼움", MUTED, True),
    ("3", ACC, ("IP", "목적지 IP 로 다음 홉을 고른다"), ("IP", "코드 한 줄 고치지 않는다"),
     "손대지 않음", ACC, False),
    ("2", INFO, ("이더넷", "랜선 위를 지나는 프레임"), ("WiFi", "공기를 가르는 프레임"),
     "갈아 끼움", MUTED, True),
]

for i, (num, col, left, right, chip, chip_col, swap) in enumerate(rows):
    y = Y0 + i * (LH + GAP)
    cy = y + LH / 2
    focal = (col is ACC)
    for x, (name, note) in ((AX, left), (BX, right)):
        if focal:
            d.tone(x, y, CW, LH, ACC, 8, "12", 1.5)
        else:
            d.box(x, y, CW, LH, PAPER2, col, 1.2, 8)
        d.t(x + 18, y + 30, name, 15, col, KR, "start", 600)
        d.t(x + CW - 18, y + 30, f"L{num}", 14, col, MONO, "end", 600)
        d.t(x + 18, y + 54, note, 11.5, MUTED, KR, "start")
    # 칩이 선 위에 얹히면 lint 가 text-line 으로 잡는다. 선을 칩 좌우로 끊어 둔다.
    hw = (len(chip) * CHIP_SIZE + 14) / 2 + 6
    if swap:
        d.line(MID_L, cy, MID_C - hw, cy, chip_col, 1.5)
        d.path(f"M {MID_C + hw} {cy} L {MID_R} {cy}", chip_col, 1.5, m="ar")
    else:
        d.line(MID_L, cy, MID_C - hw, cy, chip_col, 1.2, "4 5")
        d.line(MID_C + hw, cy, MID_R, cy, chip_col, 1.2, "4 5")
    d.chip(MID_C, cy, chip, chip_col, CHIP_SIZE)

BOT = Y0 + 4 * (LH + GAP) - GAP

d.tone(24, BOT + 18, W - 48, 126, INFO)
d.t(44, BOT + 48, "IP 가 이웃에 대해 아는 것은 이 둘이 전부입니다", 12.5, INK, KR, "start", 600)
d.t(44, BOT + 78,
    "위쪽 — 덩어리가 내려온다. Protocol 칸에 6(TCP)이나 17(UDP)을 적어 둘 뿐, 그 안을 열어 보지 않습니다.",
    11.5, MUTED, KR, "start")
d.t(44, BOT + 100,
    "아래쪽 — 이 MAC 으로 보내 달라. 그 아래가 이더넷인지 WiFi 인지는 묻지 않습니다.",
    11.5, MUTED, KR, "start")
d.t(44, BOT + 122,
    "그래서 위든 아래든 갈아 끼워도 IP 층은 고쳐지지 않습니다 — 서로를 모르는 것이 곧 교체 가능성입니다.",
    11.5, INK, KR, "start")

d.legend(BOT + 164, [("애플리케이션 L7", WARN), ("전송 L4", OK),
                     ("인터넷 L3 — 안 고쳐지는 층", ACC), ("링크 L2", INFO)])
d.save("07-01.layer-swap.svg")
print("ok 07-01.layer-swap")
