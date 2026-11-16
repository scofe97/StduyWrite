# 05-01 §3 — 하드 링크와 심볼릭 링크의 실제 배치. 디렉터리 항목 myfile·somealias 가 같은 아이노드
#           6302071 을 가리키고(Links: 2), somesoftalias 는 자기 아이노드 6303540 에 경로 문자열
#           "myfile"(6 바이트)을 담아 그 이름을 디렉터리에서 다시 찾는다. 아래 줄은 rm myfile 뒤.
# 타입 스펙: type-architecture — 디렉터리 항목 → 아이노드 → 데이터·내용으로 이어지는 참조 구조.
#           accent 는 두 이름이 함께 가리키는 아이노드 6302071.
# 근거: 본문 §3 의 ln·ls -al·stat 출력(somealias Inode 6302071 Links 2 Size 0 regular empty file,
#       somesoftalias Inode 6303540 Links 1 Size 6 symbolic link -> myfile, Device fd00h)과
#       원본 삭제 표(하드 링크는 링크 수만 줄고 데이터 보존, 심볼릭 링크는 깨진 링크).
# 축약: 디렉터리의 다른 항목은 그리지 않았다. rm 뒤 Links: 1 은 본문 표의 "링크 수만 줄고"를 숫자로 적은 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 656
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §3",
      "하드 링크는 같은 아이노드를, 심볼릭 링크는 이름을 가리킨다",
      "디렉터리 항목 myfile 과 somealias 는 같은 아이노드 6302071 을 가리켜 Links 가 2 다. "
      "somesoftalias 는 자기 아이노드 6303540 을 따로 갖고 그 내용은 경로 문자열 myfile 6 바이트다. "
      "cat somesoftalias 는 이 문자열을 읽어 디렉터리에서 myfile 을 다시 찾는다. rm myfile 뒤에는 "
      "somealias 가 Links 1 로 데이터를 지키고 somesoftalias 는 찾을 이름이 없어 깨진 링크가 된다.",
      "아이노드는 이름을 갖지 않는다 — 이름은 디렉터리 항목이 쥐고 있다")

# ── 위 컷: 지금 ─────────────────────────────────────────────
DX0, DX1, DY0, DY1 = 24, 300, 96, 268
ROWS = [("myfile", "6302071", 148, ACC), ("somealias", "6302071", 192, ACC),
        ("somesoftalias", "6303540", 236, INFO)]
I1 = (380, 640, 120, 212)            # inode 6302071
I2 = (380, 640, 252, 340)            # inode 6303540
R1 = (704, 896, 120, 212)            # 데이터
R2 = (704, 896, 252, 340)            # 내용 "myfile"
BACK = 376                           # 이름으로 다시 찾는 길

# 연결선 먼저
d.arrow([(DX1 + 2, 148), (I1[0] - 3, 148)], ACC, "acc", 1.6)
d.arrow([(DX1 + 2, 192), (I1[0] - 3, 192)], ACC, "acc", 1.6)
d.arrow([(DX1 + 2, 236), (340, 236), (340, 296), (I2[0] - 3, 296)], INFO, "info", 1.4)
d.t(352, 270, "1", 12, INFO, MONO, "start", 600)
d.arrow([(I1[1] + 2, 166), (R1[0] - 3, 166)], MUTED, "ar", 1.2)
d.arrow([(I2[1] + 2, 296), (R2[0] - 3, 296)], INFO, "info", 1.4)
d.t((I2[1] + R2[0]) / 2, 286, "2 읽기", 12, INFO, KR)
cxr = (R2[0] + R2[1]) / 2
cxd = (DX0 + DX1) / 2
d.arrow([(cxr, R2[3] + 2), (cxr, BACK), (cxd, BACK), (cxd, DY1 + 3)], INFO, "info", 1.4, "5 3")
d.t((cxd + cxr) / 2, BACK - 8, '3 이름 "myfile" 을 디렉터리에서 다시 찾음', 12, INFO, KR)

# 디렉터리
d.box(DX0, DY0, DX1 - DX0, DY1 - DY0, PAPER2, RULE, 1.0, 8)
d.t(DX0 + 14, DY0 + 21, "디렉터리", 13, INK, KR, "start", 600)
d.t(DX1 - 14, DY0 + 21, "장치 fd00h", 12, SOFT, MONO, "end")
for name, ino, cy, c in ROWS:
    d.o.append(f'<rect x="{DX0 + 12}" y="{cy - 16}" width="{DX1 - DX0 - 24}" height="32" rx="4" '
               f'fill="none" stroke="{c}" stroke-width="1"/>')
    d.t(DX0 + 24, cy + 5, name, 13, INK, MONO, "start", 600)
    d.t(DX1 - 24, cy + 5, ino, 12, c, MONO, "end")

# 아이노드 둘
x0, x1, y0, y1 = I1
d.tone(x0, y0, x1 - x0, y1 - y0, ACC, 8, "1F", 1.4)
d.t(x0 + 14, y0 + 24, "inode 6302071", 14, ACC, MONO, "start", 600)
d.t(x0 + 14, y0 + 50, "regular empty file", 12, MUTED, MONO, "start")
d.t(x0 + 14, y0 + 74, "Links: 2 · Size: 0", 13, INK, MONO, "start", 600)
x0, x1, y0, y1 = I2
d.box(x0, y0, x1 - x0, y1 - y0, PAPER2, INFO, 1.2, 8)
d.t(x0 + 14, y0 + 24, "inode 6303540", 14, INFO, MONO, "start", 600)
d.t(x0 + 14, y0 + 50, "symbolic link", 12, MUTED, MONO, "start")
d.t(x0 + 14, y0 + 74, "Links: 1 · Size: 6", 13, INK, MONO, "start", 600)

# 데이터와 내용
x0, x1, y0, y1 = R1
d.o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(x0 + 14, y0 + 24, "데이터 블록", 13, INK, KR, "start", 600)
d.t(x0 + 14, y0 + 50, "Blocks: 0", 12, MUTED, MONO, "start")
d.t(x0 + 14, y0 + 74, "빈 파일", 12, SOFT, KR, "start")
x0, x1, y0, y1 = R2
d.box(x0, y0, x1 - x0, y1 - y0, PAPER2, INFO, 1.1, 6)
d.t(x0 + 14, y0 + 24, "내용", 13, INK, KR, "start", 600)
d.t(x0 + 14, y0 + 52, '"myfile"', 15, INFO, MONO, "start", 600)
d.t(x0 + 14, y0 + 74, "경로 문자열 6 바이트", 12, MUTED, KR, "start")

# ── 아래 컷: rm myfile 뒤 ─────────────────────────────────
TY = 412
d.line(24, TY, W - 24, TY, RULE, 0.8)
d.t(24, TY + 26, "rm myfile 뒤", 13, INK, MONO, "start", 600)
d.t(140, TY + 26, "디렉터리 항목 myfile 이 사라짐", 12, MUTED, KR, "start")
RA, RB = TY + 64, TY + 120            # 두 줄의 중심 y
NX0, NX1 = 24, 220
IX0, IX1 = 268, 500
XX0, XX1 = 548, 896

# 연결선 먼저
for cy, c, m in ((RA, OK, "ok"), (RB, BAD, "bad")):
    d.arrow([(NX1 + 2, cy), (IX0 - 3, cy)], c, m, 1.4)
d.arrow([(IX1 + 2, RA), (XX0 - 3, RA)], OK, "ok", 1.4)
d.line(IX1 + 2, RB, XX0 - 2, RB, BAD, 1.2, "3 4")
d.t((IX1 + XX0) / 2, RB + 5, "✕", 14, BAD, MONO)

for cy, name, ino, sub, c in ((RA, "somealias", "inode 6302071", "Links: 2 → 1", OK),
                              (RB, "somesoftalias", "inode 6303540", '내용 "myfile"', BAD)):
    d.o.append(f'<rect x="{NX0}" y="{cy - 18}" width="{NX1 - NX0}" height="36" rx="4" fill="none" '
               f'stroke="{c}" stroke-width="1"/>')
    d.t(NX0 + 14, cy + 5, name, 13, INK, MONO, "start", 600)
    d.box(IX0, cy - 22, IX1 - IX0, 44, PAPER2, c, 1.1, 6)
    d.t(IX0 + 12, cy - 3, ino, 13, c, MONO, "start", 600)
    d.t(IX0 + 12, cy + 15, sub, 12, MUTED, MONO if sub.startswith("L") else KR, "start")
d.tone(XX0, RA - 22, XX1 - XX0, 44, OK, 6)
d.t(XX0 + 14, RA + 5, "데이터 보존", 13, OK, KR, "start", 600)
d.t(XX0 + 112, RA + 5, "링크 수만 줄어듦", 12, MUTED, KR, "start")
d.o.append(f'<rect x="{XX0}" y="{RB - 22}" width="{XX1 - XX0}" height="44" rx="6" fill="none" '
           f'stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 3"/>')
d.t(XX0 + 14, RB + 5, "찾을 이름 없음", 13, BAD, KR, "start", 600)
d.t(XX0 + 136, RB + 5, "깨진 링크 (dangling link)", 12, MUTED, KR, "start")

d.t(24, 584, "아이노드 번호·Links·Size 는 본문 stat 출력 · rm 뒤 Links: 1 은 본문 표의 \"링크 수만 줄고\" 를 숫자로 적음",
    11, SOFT, KR, "start")
LEG = 604
d.legend(LEG, [("같은 아이노드", ACC), ("경로 문자열로 찾음", INFO), ("보존", OK), ("깨짐", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.links.svg")
print("ok 05-01.links")
