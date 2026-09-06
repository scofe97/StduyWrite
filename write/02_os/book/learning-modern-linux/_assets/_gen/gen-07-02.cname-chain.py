# 07-02 §6 — CNAME 이 사는 이유. 한 겹을 두었기 때문에 아래를 갈아 끼울 수 있다.
# 원문("Record Types and Zone Files"): CNAME 은 "Canonical name record: an alias of one name to
#       another." 이고, 저자가 든 존 파일에 "www  IN  CNAME  example.com." 한 줄이 있다.
#       저자는 그 줄을 "makes www.example.com an alias of this domain" 까지만 설명한다.
# 노트의 읽기: 왜 별칭이 필요한가를 저자는 말하지 않는다. 2026-09-06 학습 세션에서 학습자가
#       직접 요청한 도식이라 그 자리를 채운다 — 이름 하나를 사이에 끼워 두면 그 아래의 주소를
#       내 설정을 건드리지 않고 갈아 끼울 수 있다는 것이 CNAME 의 값이다.
#       대가는 RFC 1034 §3.6.2 가 두 문장으로 적어 둔다. 이름 서버는 CNAME 을 만나면 그 이름으로
#       질의를 다시 시작하므로(restarts the query) 체인이 길수록 왕복이 늘고, CNAME 이 있는
#       노드에는 다른 데이터를 둘 수 없어(no other data should be present) 존 꼭대기는 별칭이
#       될 수 없다. cdn.example.net 은 RFC 2606 이 문서용으로 예약한 이름이라 예시로 안전하다.
# 타입 스펙: type-layers — 같은 체인을 두 구성으로 나란히 놓은 두 열 변형이다. 앞 편의
#       07-01.layer-swap.svg 와 같은 논지(한 겹 두면 아래를 갈아 끼울 수 있다)를 같은 표현형으로
#       말해야 두 장이 서로를 가리킬 수 있어, 캔버스·열 좌표·칩 문법을 그 도식에서 그대로 가져왔다.
#       coral 은 하나뿐이며 그 자리가 갈아 끼우지 않는 내 존 파일의 한 줄이다.
#       축약: 조회 왕복의 시간 순서는 07-02.dns-lookup.svg 가 맡으므로 여기서는 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, KR, MONO

W, H = 880, 724
d = D(W, H, "LEARNING MODERN LINUX · 07-02 §6",
      "아래를 갈아 끼워도 내 존 파일은 그대로다",
      "www 에 주소를 직접 적는 대신 CDN 의 이름을 가리키게 해 두면, CDN 이 서버를 옮겨 "
      "주소가 바뀌어도 내가 고칠 줄은 없다. 한 겹을 둔 값이 그것이다.",
      "저자는 별칭이라고만 적고 왜 필요한지는 말하지 않습니다")

AX, BX, CW = 64, 530, 286
Y0, LH, GAP = 160, 76, 44
MID_L, MID_R, MID_C = AX + CW + 6, BX - 6, (AX + CW + BX) / 2
CHIP_SIZE = 11.5

d.t(AX + CW / 2, 140, "오늘", 12, MUTED, KR, "middle", 600)
d.t(BX + CW / 2, 140, "CDN 이 서버를 옮긴 뒤", 12, MUTED, KR, "middle", 600)

rows = [
    # (mono 태그, 색, 왼쪽 이름·설명, 오른쪽 이름·설명, 가운데 칩, 칩 색, 교체 여부)
    ("CNAME", ACC, ("www.example.com", "내 존 파일이 정하는 한 줄"),
                   ("www.example.com", "고칠 일이 생기지 않는다"),
     "손대지 않음", ACC, False),
    ("A", INFO, ("cdn.example.net", "CDN 이 관리하는 이름"),
                ("cdn.example.net", "이름은 그대로 남는다"),
     "그대로", SOFT, False),
    ("IPv4", OK, ("1.2.3.4", "오늘 이 이름이 가리키는 서버"),
                 ("5.6.7.8", "CDN 이 말없이 갈아 끼운다"),
     "갈아 끼움", MUTED, True),
]

for i, (tag, col, left, right, chip, chip_col, swap) in enumerate(rows):
    y = Y0 + i * (LH + GAP)
    cy = y + LH / 2
    focal = (col is ACC)
    for x, (name, note) in ((AX, left), (BX, right)):
        if focal:
            d.tone(x, y, CW, LH, ACC, 8, "12", 1.5)
        else:
            d.box(x, y, CW, LH, PAPER2, col, 1.2, 8)
        d.t(x + 18, y + 30, name, 14, col, MONO, "start", 600)
        d.t(x + CW - 18, y + 30, tag, 12, col, MONO, "end", 600)
        d.t(x + 18, y + 54, note, 11.5, MUTED, KR, "start")
    # 체인 — 한 줄이 다음 줄을 가리킨다. 마지막 행 아래에는 가리킬 것이 없다.
    if i < len(rows) - 1:
        for x in (AX, BX):
            d.arrow([(x + 40, y + LH + 8), (x + 40, y + LH + GAP - 6)], SOFT, "soft", 1.3)
            d.t(x + 54, y + LH + 28, f"{tag} 레코드가 가리킨다", 11, SOFT, KR, "start")
    # 칩이 선 위에 얹히면 lint 가 text-line 으로 잡는다. 선을 칩 좌우로 끊어 둔다.
    hw = (len(chip) * CHIP_SIZE + 14) / 2 + 6
    if swap:
        d.line(MID_L, cy, MID_C - hw, cy, chip_col, 1.5)
        d.path(f"M {MID_C + hw} {cy} L {MID_R} {cy}", chip_col, 1.5, m="ar")
    else:
        d.line(MID_L, cy, MID_C - hw, cy, chip_col, 1.2, "4 5")
        d.line(MID_C + hw, cy, MID_R, cy, chip_col, 1.2, "4 5")
    d.chip(MID_C, cy, chip, chip_col, CHIP_SIZE)

BOT = Y0 + 3 * (LH + GAP) - GAP

d.tone(24, BOT + 18, W - 48, 148, INFO)
d.t(44, BOT + 48, "한 겹을 둔 값과 그 대가", 12.5, INK, KR, "start", 600)
d.t(44, BOT + 78,
    "값 — CNAME 이 없으면 www 에 주소를 직접 적어야 하고, 주소가 바뀔 때마다 내 존 파일을 고쳐야 합니다.",
    11.5, MUTED, KR, "start")
d.t(44, BOT + 100,
    "대가 하나 — 이름 서버는 CNAME 을 만나면 그 이름으로 질의를 다시 시작합니다. 체인이 길수록 왕복이 늡니다.",
    11.5, MUTED, KR, "start")
d.t(44, BOT + 122,
    "대가 둘 — CNAME 이 있는 노드에는 다른 데이터를 두지 못합니다. 그래서 존 꼭대기는 별칭이 될 수 없습니다.",
    11.5, MUTED, KR, "start")
d.t(44, BOT + 144,
    "앞 편의 07-01.layer-swap 과 같은 논지입니다 — 사이에 한 겹을 두면 그 아래를 갈아 끼울 수 있습니다.",
    11.5, INK, KR, "start")

d.legend(BOT + 186, [("내가 쥔 한 줄 — 안 바뀝니다", ACC), ("CDN 이 쥔 이름", INFO),
                     ("실제 주소 — 갈립니다", OK)])
d.save("07-02.cname-chain.svg")
print("ok 07-02.cname-chain")
