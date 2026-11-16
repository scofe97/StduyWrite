# 05-01 §8 — 유니온 마운트(OverlayFS). lowerdir·upperdir 두 디렉터리가 merged 한 곳으로 겹쳐
#           보이는 실제 배치를, 파일 세 개로 조회·수정(copy-up)·삭제(whiteout)를 나란히 보인다.
# 타입 스펙: type-layers — 아래(lowerdir)에서 위(merged)로 겹치는 디렉터리 층. accent 는 copy-up 된 b.txt.
# 근거: 본문 §8 「유니온 마운트와 OverlayFS」의 세 연산과 각주 [^whiteout](c 0 0 문자 장치, copy_up),
#       같은 절의 "읽기 전용 기본 이미지 레이어를 공유 · 각자 격리된 쓰기 층". 파일 이름 a·b·c.txt 와
#       열 머리의 명령은 본문에 없는 예시라 도식 아래 한 줄에 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "두 디렉터리를 겹쳐 merged 하나로 보인다",
      "아래에 읽기 전용 lowerdir, 그 위에 쓰기 층 upperdir, 맨 위에 둘을 겹친 merged 마운트 지점이 있다. "
      "a.txt 는 upperdir 에 없어 lowerdir 의 것이 보인다. b.txt 는 쓰기로 열리는 순간 upperdir 로 "
      "통째로 복사(copy-up)되고 merged 는 그 복사본을 보인다. c.txt 를 지우면 upperdir 에 같은 이름의 "
      "화이트아웃(c 0 0 문자 장치)이 생겨 lowerdir 의 원본을 가린다.",
      "lowerdir 은 바뀌지 않는다 — 조회는 위층부터, 쓰기와 삭제는 upperdir 에만 남는다")

BX0, BX1 = 176, 856                 # 층 띠의 가로 범위
COLS = (288, 516, 744)              # 열 = 파일 하나 = 연산 하나
CELL_W, CELL_H = 176, 44
BAND_H, BAND_GAP = 72, 56
HY = 112                            # 열 머리
MY = 168                            # merged 띠
UY = MY + BAND_H + BAND_GAP         # upperdir 띠
LY = UY + BAND_H + BAND_GAP         # lowerdir 띠


def cy(band_y):
    return band_y + (BAND_H - CELL_H) / 2


def cell(col, band_y, name, sub, c, kind="solid"):
    x, y = COLS[col] - CELL_W / 2, cy(band_y)
    if kind == "empty":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="5" fill="none" '
                   f'stroke="{c}" stroke-width="1" stroke-dasharray="4 3"/>')
        d.t(COLS[col], y + 27, name, 12, c, KR)
        return
    if kind == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="5" '
                   f'fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    elif kind == "tone":
        d.tone(x, y, CELL_W, CELL_H, c, 5)
    else:
        d.box(x, y, CELL_W, CELL_H, PAPER, c, 1.1, 5)
    d.t(COLS[col], y + 19, name, 13, INK if c == MUTED else c, MONO, "middle", 600)
    d.t(COLS[col], y + 36, sub, 12, MUTED, MONO if sub.isascii() else KR)


# 층 띠와 층 이름
for y, name, sub, note in ((MY, "merged", "마운트 지점", "하나의 디렉터리로 보임"),
                           (UY, "upperdir", "쓰기 층", "컨테이너마다 따로"),
                           (LY, "lowerdir", "읽기 전용", "이미지 층 · 공유")):
    d.box(BX0, y, BX1 - BX0, BAND_H, PAPER2, RULE, 0.9, 8)
    d.t(24, y + 26, name, 14, INK, MONO, "start", 600)
    d.t(24, y + 44, sub, 12, MUTED, KR, "start")
    d.t(24, y + 60, note, 12, SOFT, KR, "start")

# 열 머리 — 연산과 예시 명령
for col, (op, cmd, c) in enumerate((("1. 조회", "cat a.txt", INFO),
                                    ("2. 수정", "echo x >> b.txt", ACC),
                                    ("3. 삭제", "rm c.txt", WARN))):
    d.t(COLS[col] - 8, HY + 14, op, 14, c, KR, "end", 600)
    d.t(COLS[col], HY + 14, cmd, 12, MUTED, MONO, "start")
    d.line(COLS[col] - CELL_W / 2, HY + 28, COLS[col] + CELL_W / 2, HY + 28, c, 1.0)

# 화살표 — 칸보다 먼저 그린다
top_of = lambda band_y: cy(band_y) - 2
bot_of = lambda band_y: cy(band_y) + CELL_H + 2
# 1. a.txt: upperdir 에 없으니 lowerdir 의 것이 merged 로 올라온다
d.arrow([(COLS[0], top_of(LY)), (COLS[0], bot_of(MY) + 1)], INFO, "info", 1.4)
d.t(COLS[0] + 16, UY + 32, "upper 에 없음", 12, INFO, KR, "start")
d.t(COLS[0] + 16, UY + 50, "→ lower 로", 12, INFO, KR, "start")
# 2. b.txt: copy-up 뒤 merged 는 upper 의 것을 본다
d.arrow([(COLS[1], top_of(LY)), (COLS[1], bot_of(UY) + 1)], ACC, "acc", 1.6)
d.t(COLS[1] + 12, UY + BAND_H + BAND_GAP / 2 + 4, "copy-up", 13, ACC, MONO, "start", 600)
d.arrow([(COLS[1], top_of(UY)), (COLS[1], bot_of(MY) + 1)], ACC, "acc", 1.4)
# 3. c.txt: 화이트아웃이 lower 원본을 가린다
d.arrow([(COLS[2], top_of(UY)), (COLS[2], bot_of(MY) + 1)], WARN, "warn", 1.4, "4 3")
d.t(COLS[2] + 12, MY + BAND_H + BAND_GAP / 2 + 4, "가림", 12, WARN, KR, "start")

# 칸
cell(0, MY, "a.txt", "lower 의 것", INFO, "tone")
cell(1, MY, "b.txt", "upper 의 것", ACC, "tone")
cell(2, MY, "c.txt 안 보임", "", WARN, "empty")
cell(1, UY, "b.txt", "복사본 · 변경 기록", ACC, "focal")
cell(2, UY, "c.txt", "화이트아웃 c 0 0", WARN, "tone")
for col, name in enumerate(("a.txt", "b.txt", "c.txt")):
    cell(col, LY, name, "원본 그대로", MUTED)

d.t(BX0, LY + BAND_H + 28, "파일 이름 a·b·c.txt 와 열 머리의 명령은 예시 · c 0 0 = 장치 번호 0/0 인 문자 장치",
    11, SOFT, KR, "start")
LEG = LY + BAND_H + 48
d.legend(LEG, [("조회 경로", INFO), ("copy-up", ACC), ("화이트아웃", WARN), ("lowerdir 원본", MUTED)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.union-mount.svg")
print("ok 05-01.union-mount")
