# 05-01 §9 — CoW 의 두 단계, 곧 복사할 때와 고칠 때 무엇이 실제로 생기는가.
# 원문("Copy-on-Write Filesystems"): "Copy-on-write (CoW) is a nifty concept to increase I/O speed and at
#       the same time use less space."
#   1단계 — "The original file, File 1, consisting of blocks A, B, and C, is copied to a file called
#            File 2. Rather than copying the actual blocks, only the metadata (pointers to the blocks) is
#            copied. This is fast and doesn't use up much space since only metadata is created."
#   2단계 — "When File 2 is modified (let's say something in block C is changed), only then is block C
#            copied: a new block called C′ is created, and while File 2 still points to (uses) the
#            unmodified blocks A and B, it now uses a new block (C′) to capture new data."
#   따라서 2단계에서도 블록 C 는 사라지지 않는다. 파일 1 이 여전히 C 를 쓰고, 파일 2 만 C′ 로 옮겨 간다.
# 주의: 원문의 CoW 설명에는 삭제가 없다. 화이트아웃 같은 표식은 이 장에 나오지 않으므로 그리지 않는다.
# 타입 스펙: type-state — 같은 대상의 앞뒤 상태를 나란히 두고 무엇이 달라졌는지만 보인다.
#           accent 는 실제로 블록이 생기는 단 한 곳.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §9",
      "복사할 때는 포인터만, 고칠 때에야 블록이 생긴다",
      "저자가 두 단계로 나눠 그린 CoW 를 앞뒤 상태로 놓은 것. 오른쪽에서도 블록 C 는 그대로 있고, "
      "파일 2 만 새 블록으로 옮겨 갔다.",
      "빠르고 공간을 덜 쓰는 이유가 이 그림 안에 있습니다")

PW, PX1, PX2 = 400, 24, 456
PY, PH = 148, 244
BW, BGAP, BY, BH = 80, 10, 300, 60
F1Y, F2Y, FH = 208, 248, 32


def panel(x, title, sub, changed):
    d.box(x, PY, PW, PH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, PY + 28, title, 15, INK, KR, "start", 600)
    d.t(x + 20, PY + 50, sub, 11.5, MUTED, KR, "start")

    for fy, name, col in [(F1Y, "파일 1", INFO), (F2Y, "파일 2", OK)]:
        d.o.append(f'<rect x="{x + 24}" y="{fy}" width="112" height="{FH}" rx="5" '
                   f'fill="{col}12" stroke="{col}" stroke-width="1.2"/>')
        d.t(x + 80, fy + 21, name, 12.5, col, KR, "middle", 600)

    labels = ["A", "B", "C", "C′"] if changed else ["A", "B", "C"]
    xs = []
    for j, b in enumerate(labels):
        bx = x + 24 + j * (BW + BGAP)
        xs.append(bx + BW / 2)
        focal = changed and j == 3
        if focal:
            d.o.append(f'<rect x="{bx}" y="{BY}" width="{BW}" height="{BH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
            d.t(bx + BW / 2, BY + 30, b, 17, ACC, MONO, "middle", 600)
            d.t(bx + BW / 2, BY + 48, "새로 생긴 블록", 10, ACC, KR)
        else:
            d.box(bx, BY, BW, BH, PAPER, MUTED, 1.1, 6)
            d.t(bx + BW / 2, BY + 36, b, 17, INK, MONO, "middle", 600)

    f1_targets = xs[:3]
    f2_targets = (xs[:2] + [xs[3]]) if changed else xs[:3]
    for tx in f1_targets:
        d.path(f"M {x + 80} {F1Y + FH} L {tx} {BY - 2}", INFO, 1.0, dash="4 4")
    for k, tx in enumerate(f2_targets):
        col = ACC if (changed and k == 2) else OK
        d.path(f"M {x + 80} {F2Y + FH} L {tx} {BY - 2}", col, 1.2)


panel(PX1, "1단계 — 복사", "실제 블록 대신 블록을 가리키는 포인터만 복사합니다.", False)
panel(PX2, "2단계 — 파일 2 의 블록 C 를 고침", "고쳐진 블록만 새로 생기고 A 와 B 는 그대로 공유합니다.", True)

d.arrow([(432, 270), (448, 270)], MUTED, "ar", 1.4)

d.tone(24, 412, W - 48, 62, INFO)
d.t(44, 440, "같은 베이스 이미지를 쓰는 컨테이너가 여럿이어도 읽기 전용 층은 한 벌이면 됩니다.",
    12.5, INK, KR, "start", 600)
d.t(44, 462, "각 컨테이너가 무언가를 쓰는 순간에만 그 블록이 위쪽 층으로 복사됩니다.", 12, MUTED, KR, "start")

d.legend(496, [("파일 1 이 쓰는 블록", INFO), ("파일 2 가 쓰는 블록", OK),
               ("실제로 블록이 생기는 곳", ACC)])
d.save("05-01.cow.svg")
print("ok 05-01.cow")
