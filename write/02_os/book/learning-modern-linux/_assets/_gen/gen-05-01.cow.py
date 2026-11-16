# 05-01 §8 — CoW(Copy-on-Write). 두 파일의 메타데이터가 디스크의 같은 데이터 블록 A·B·C 를
#           가리키다가, file2 가 C 를 고치는 순간 C 만 새 블록 C′ 으로 갈라지는 실제 구조.
# 타입 스펙: type-architecture-delta — 같은 블록 배치의 전(복사 직후)·후(file2 수정 뒤) 두 컷.
#           생긴 것(C′, +)과 다시 이어진 것(file2 의 세 번째 포인터)을 표시한다. accent 는 C′.
# 근거: 본문 §8 「CoW — 복사 없는 복사」의 두 단계(블록 A·B·C 로 된 file1, 포인터만 복제,
#       수정 때 대상 블록만 복사되어 C′, file1 은 기존 블록 유지). 블록 크기·번호는 본문에 없어
#       적지 않는다. 디스크 띠에서 블록의 자리와 빈 칸은 예시다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 792
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "복사는 포인터만, 쓰기는 고친 블록 하나만",
      "위 컷은 file1 을 file2 로 복사한 직후다. 두 파일의 메타데이터가 디스크의 같은 블록 "
      "A·B·C 를 가리킨다. 아래 컷은 file2 가 C 를 고친 뒤다. C 의 사본 C′ 이 빈 블록에 "
      "새로 생기고 file2 의 세 번째 포인터만 C′ 으로 옮겨 간다. file1 은 그대로 A·B·C 를 가리킨다.",
      "데이터 블록은 그대로 두고 메타데이터의 블록 포인터만 복제했다가, 쓰는 블록만 갈라 낸다")

LX = 24                      # 컷 이름 열
CX0, CX1 = 184, 576          # 메타데이터 카드의 가로 범위
X0, CW, NC = 360, 72, 7      # 디스크 띠: 칸 7개(A·B·C·빈·C′자리·빈·빈)
CARD_H, STRIP_H, GAP = 44, 44, 48


def cx(i):
    return X0 + i * CW + CW / 2


def card(y, name, slots, c):
    """파일 메타데이터 카드. slots: (칸 번호, 라벨, 색)"""
    d.box(CX0, y, CX1 - CX0, CARD_H, PAPER2, c, 1.2, 6)
    d.t(CX0 + 14, y + 20, name, 14, c, MONO, "start", 600)
    d.t(CX0 + 14, y + 36, "메타데이터", 12, MUTED, KR, "start")
    for i, lab, sc in slots:
        x = X0 + i * CW + 8
        d.o.append(f'<rect x="{x}" y="{y + 8}" width="{CW - 16}" height="{CARD_H - 16}" rx="4" '
                   f'fill="{sc}1F" stroke="{sc}" stroke-width="1"/>')
        d.t(cx(i), y + 27, "→ " + lab, 13, sc, MONO, "middle", 600)


def strip(y, cells):
    """디스크 데이터 블록 띠. cells: 칸 번호 → (라벨, 종류)"""
    d.t(CX0, y + 20, "데이터 블록", 13, INK, KR, "start", 600)
    d.t(CX0, y + 36, "디스크", 12, SOFT, KR, "start")
    for i in range(NC):
        x = X0 + i * CW + 2
        lab, kind = cells.get(i, ("", "free"))
        if kind == "free":
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW - 4}" height="{STRIP_H}" rx="4" fill="none" '
                       f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 3"/>')
            d.t(cx(i), y + 27, "빈", 12, SOFT, KR)
        elif kind == "new":
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW - 4}" height="{STRIP_H}" rx="4" '
                       f'fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(cx(i), y + 28, lab, 15, ACC, MONO, "middle", 600)
        else:
            d.box(x, y, CW - 4, STRIP_H, PAPER, MUTED, 1.1, 4)
            d.t(cx(i), y + 28, lab, 15, INK, MONO, "middle", 600)


def cut(top, title, sub, after):
    d.t(LX, top + 14, title, 14, INK, KR, "start", 600)
    d.t(LX, top + 34, sub, 12, MUTED, KR, "start")
    f1y = top + 52
    sy = f1y + CARD_H + GAP
    f2y = sy + STRIP_H + GAP
    # 포인터 화살표는 칸·카드보다 먼저 그린다(글자를 덮지 않게)
    for i in range(3):
        d.arrow([(cx(i), f1y + CARD_H + 2), (cx(i), sy - 3)], INFO, "info", 1.3)
    for i in range(2):
        d.arrow([(cx(i), f2y - 2), (cx(i), sy + STRIP_H + 3)], OK, "ok", 1.3)
    if after:
        ry = f2y - 22
        d.arrow([(cx(2), f2y - 2), (cx(2), ry), (cx(4), ry), (cx(4), sy + STRIP_H + 3)],
                ACC, "acc", 1.5)
        # C 를 읽어 C′ 에 복사한 뒤 고친다
        cy = sy - 18
        d.arrow([(cx(2) + 16, sy - 2), (cx(2) + 16, cy), (cx(4), cy), (cx(4), sy - 3)],
                ACC, "acc", 1.2, "4 3")
        d.t(cx(4) + 12, cy - 6, "복사 후 쓰기", 12, ACC, KR, "start")
    else:
        d.arrow([(cx(2), f2y - 2), (cx(2), sy + STRIP_H + 3)], OK, "ok", 1.3)

    card(f1y, "file1", [(0, "A", INFO), (1, "B", INFO), (2, "C", INFO)], INFO)
    cells = {0: ("A", "data"), 1: ("B", "data"), 2: ("C", "data")}
    if after:
        cells[4] = ("C′", "new")
    strip(sy, cells)
    slots = [(0, "A", OK), (1, "B", OK), (2, "C′" if after else "C", ACC if after else OK)]
    card(f2y, "file2", slots, OK)
    if after:
        d.t(CX1 + 14, f2y + 27, "← 이 포인터만 바뀜", 12, ACC, KR, "start")
    return f2y + CARD_H


end1 = cut(104, "1. 복사 직후", "포인터만 복제 · 블록 A·B·C 공유", False)
end2 = cut(end1 + 40, "2. file2 가 C 를 고친 뒤", "C 만 C′ 으로 갈라짐 · A·B 는 계속 공유", True)
d.line(LX, end1 + 20, W - 24, end1 + 20, RULE, 0.8, "2 4")

d.t(LX, end2 + 30, "블록 이름 A·B·C 는 본문 그대로 · 디스크 띠의 자리와 빈 칸은 예시", 11, SOFT, KR, "start")
d.legend(end2 + 48, [("file1 포인터", INFO), ("file2 포인터", OK), ("새로 생긴 블록 C′", ACC)])
assert end2 + 48 + 40 <= H, (end2, H)
d.save("05-01.cow.svg")
print("ok 05-01.cow")
