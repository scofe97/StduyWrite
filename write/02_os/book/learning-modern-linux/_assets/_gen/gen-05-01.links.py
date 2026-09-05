# 05-01 §3 — 하드 링크와 심볼릭 링크가 실제로 가리키는 곳.
# 원문("Basics"):
#   Hard links: "Reference inodes and can't refer to directories. They also do not work across
#                filesystems."
#   Symbolic links: "Special files with their content being a string representing the path of another
#                file."
#   실증은 저자의 출력 — `-rw-rw-r-- 2 mh9 mh9 0 Sep 5 12:15 somealias` 와
#   `lrwxrwxrwx 1 mh9 mh9 6 Sep 5 12:45 somesoftalias -> myfile`,
#   `stat somealias` 의 `Inode: 6302071  Links: 2`,
#   `stat somesoftalias` 의 `Size: 6 ... symbolic link`, `Inode: 6303540  Links: 1`.
#   저자는 "We could also have used ls -ali *alias, which would show that the inodes were the same on
#   the two names associated with the hard link" 이라 덧붙인다.
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결. accent 는 두 방식이 갈리는 한 곳,
#           곧 심볼릭 링크가 아이노드가 아니라 경로 문자열을 들고 있다는 사실.
#           축약: 데이터 블록은 한 덩어리로 뭉쳤다 — 이 도식의 논점이 블록 배치가 아니라 참조 방향이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §3",
      "하드 링크는 아이노드를, 심볼릭 링크는 경로를 붙든다",
      "이름 셋이 같은 파일을 가리키는 것처럼 보이지만 실제로 붙드는 대상이 다르다. "
      "그 차이가 stat 출력의 아이노드 번호와 링크 수와 크기 세 곳에 동시에 드러난다.",
      "원본을 지우면 둘의 운명이 갈립니다")

NX, NW, NH = 32, 224, 60
names = [
    ("myfile", "원본 이름", INFO, 152),
    ("somealias", "ln myfile somealias", INFO, 232),
    ("somesoftalias", "ln -s myfile somesoftalias", ACC, 336),
]
for label, sub, col, y in names:
    d.box(NX, y, NW, NH, PAPER2, col, 1.2, 6)
    d.t(NX + 16, y + 26, label, 14, col, MONO, "start", 600)
    d.t(NX + 16, y + 46, sub, 11.5, MUTED, MONO, "start")

IX, IY, IW, IH = 372, 152, 216, 140
d.box(IX, IY, IW, IH, PAPER2, OK, 1.3, 8)
d.t(IX + IW / 2, IY + 30, "아이노드 6302071", 14, OK, MONO, "middle", 600)
d.t(IX + IW / 2, IY + 54, "크기 · 소유자 · 위치", 12, MUTED, KR)
d.t(IX + IW / 2, IY + 74, "날짜 · 권한", 12, MUTED, KR)
d.o.append(f'<rect x="{IX + 20}" y="{IY + 92}" width="{IW - 40}" height="32" rx="5" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
d.t(IX + IW / 2, IY + 113, "Links: 2", 12.5, OK, MONO, "middle", 600)

SX, SY, SW, SH = 372, 336, 216, 96
d.o.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SX + SW / 2, SY + 28, "아이노드 6303540", 13.5, ACC, MONO, "middle", 600)
d.t(SX + SW / 2, SY + 52, "내용이 경로 문자열이다", 12, ACC, KR)
d.t(SX + SW / 2, SY + 74, "Size: 6 · Links: 1", 12, MUTED, MONO)

BX, BY, BW, BH = 664, 176, 188, 92
d.box(BX, BY, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(BX + BW / 2, BY + 32, "데이터 블록", 14, INK, KR, "middle", 600)
d.t(BX + BW / 2, BY + 58, "실제 바이트가 있는 곳", 11.5, MUTED, KR)

BUSX = 314
d.path(f"M {NX + NW} {182} L {BUSX} {182} L {BUSX} {IY + 40} L {IX - 8} {IY + 40}", INFO, 1.5, m="info")
d.path(f"M {NX + NW} {262} L {BUSX} {262} L {BUSX} {IY + 90} L {IX - 8} {IY + 90}", INFO, 1.5, m="info")
d.path(f"M {NX + NW} {366} L {BUSX} {366} L {BUSX} {SY + 34} L {SX - 8} {SY + 34}", ACC, 1.5, m="acc")
d.path(f"M {IX + IW} {IY + 70} L {BX - 8} {BY + 46}", OK, 1.5, m="ok")
d.path(f"M {SX + SW / 2} {SY} L {SX + SW / 2} {IY + IH + 8}", ACC, 1.5, m="acc", dash="6 5")
d.t(SX + SW / 2 + 12, SY - 18, "이름으로 다시 찾아간다", 11.5, ACC, KR, "start")

d.tone(28, 452, W - 56, 84, ACC)
d.t(48, 480, "myfile 을 지우면", 13, INK, KR, "start", 600)
d.t(48, 502, "somealias 는 여전히 같은 아이노드를 붙들고 있어 데이터에 닿습니다.", 12, MUTED, KR, "start")
d.t(48, 522, "somesoftalias 는 존재하지 않는 경로를 담은 파일로 남습니다.", 12, MUTED, KR, "start")

d.legend(568, [("아이노드를 붙드는 이름", INFO), ("아이노드와 데이터", OK),
               ("경로를 붙드는 이름", ACC)])
d.save("05-01.links.svg")
print("ok 05-01.links")
