# 05-02 §3 — LVM 스냅숏. 원본 LV vg0/data 의 블록 띠와 스냅숏 snap 의 COW 영역(50M) 띠를 나란히 놓고,
#           1. 만든 직후(COW 비어 있음, Data% ≈ 0) 2. 원본에 쓰기(바뀌기 전 블록을 COW 에 먼저 저장, Data% 상승)
#           3. lvconvert --merge 로 되돌리기(COW 의 원래 블록을 원본에 되씀)를 같은 객체로 세 컷에 보인다.
# 타입 스펙: type-state — 같은 두 띠가 생성 → 쓰기 누적 → 병합으로 옮겨 가는 상태. 끝 갈래(무효·lvremove)는
#           오른쪽 열에 둔다. accent 는 COW 로 먼저 복사되는 원래 블록.
# 근거: 본문 §3 「LVM 스냅샷과 Data% 상태 전이」 — lvcreate -s -L 50M -n snap /dev/vg0/data, Data% 0 근처 시작,
#       "For each write, the original data will be saved in the <COW device>", COW 가 차면 무효·lvs Attr I,
#       lvconvert --merge vg0/snap(열려 있으면 다음 활성화로 미룸), lvremove vg0/snap.
# 예시: 블록 이름 A~H, 바뀐 블록 C·F, Data% 막대의 길이는 그림을 위한 것이다. 이 노트의 실측 환경(OrbStack)에는
#       dm-snapshot 타깃이 없어 Data% 를 재지 못했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 756
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "스냅숏은 바뀌기 전 블록만 COW 영역에 모은다",
      "원본 LV vg0/data 와 스냅숏 snap 의 COW 영역 50M 를 블록 띠로 놓았다. 만든 직후 COW 는 비어 있고 "
      "Data% 는 0 근처다. 원본의 C·F 에 쓰기가 오면 바뀌기 전 C·F 가 먼저 COW 로 복사되고 원본은 C′·F′ 이 "
      "되어 Data% 가 오른다. lvconvert --merge 는 COW 의 C·F 를 원본에 되써 되돌리고 스냅숏을 지운다. "
      "COW 가 가득 차면 스냅숏은 무효(Attr I)가 되고, 작업이 잘 끝났으면 lvremove 로 지운다.",
      "스냅숏의 크기는 원본 크기가 아니라 그동안 바뀐 양이다")

LX = 24
X0, CW, N = 184, 48, 8          # 블록 띠: 8칸
GX0, GX1 = 696, 896             # 오른쪽 열(Data%·끝 갈래)
ROW_H, GAP = 40, 52


def cx(i):
    return X0 + i * CW + CW / 2


def cellrow(y, labels, kinds):
    for i in range(N):
        x = X0 + i * CW + 2
        lab, kind = labels[i], kinds[i]
        if kind == "empty":
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW - 4}" height="{ROW_H}" rx="3" fill="none" '
                       f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
            continue
        c = {"base": MUTED, "new": INFO, "saved": ACC, "back": OK}[kind]
        if kind == "base":
            d.box(x, y, CW - 4, ROW_H, PAPER2, MUTED, 1, 3)
        elif kind == "saved":
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW - 4}" height="{ROW_H}" rx="3" '
                       f'fill="{ACC}24" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.tone(x, y, CW - 4, ROW_H, c, 3)
        d.t(cx(i), y + 26, lab, 14, INK if kind == "base" else c, MONO, "middle", 600)


def rowname(y, name, sub):
    d.t(LX, y + 17, name, 13, INK, MONO, "start", 600)
    d.t(LX, y + 34, sub, 12, SOFT, KR, "start")


def gauge(y, frac, c, note):
    d.t(GX0, y + 14, "Data%", 13, INK, MONO, "start", 600)
    d.box(GX0 + 56, y + 2, 140, 16, PAPER, RULE, 0.9, 3)
    if frac:
        d.o.append(f'<rect x="{GX0 + 56}" y="{y + 2}" width="{140 * frac:.1f}" height="16" rx="3" '
                   f'fill="{c}55" stroke="{c}" stroke-width="1"/>')
    d.t(GX0, y + 40, note, 12, c, KR, "start")


ORIG = [chr(65 + i) for i in range(N)]
CH, FH_ = 2, 5                      # 바뀌는 블록 C·F


def cut(top, title, cmd, c):
    d.t(LX, top + 14, title, 14, c, KR, "start", 600)
    d.t(LX + 140, top + 14, cmd, 13, MUTED, KR if any('가' <= ch <= '힣' for ch in cmd) else MONO, "start")
    oy = top + 32
    sy = oy + ROW_H + GAP
    rowname(oy, "vg0/data", "원본 LV")
    rowname(sy, "snap", "COW 영역 50M")
    return oy, sy


# 1. 만든 직후
oy, sy = cut(104, "1. 만든 직후", "lvcreate -s -L 50M -n snap /dev/vg0/data", INFO)
cellrow(oy, ORIG, ["base"] * N)
cellrow(sy, [""] * N, ["empty"] * N)
d.t(X0 + N * CW + 16, sy + 26, "비어 있음", 12, SOFT, KR, "start")
gauge(oy + 8, 0, MUTED, "0 근처에서 시작")
end1 = sy + ROW_H

# 2. 원본에 쓰기
top2 = end1 + 36
d.line(LX, top2 - 18, W - 24, top2 - 18, RULE, 0.8, "2 4")
oy, sy = cut(top2, "2. 원본에 쓰기", "C · F 를 고침", ACC)
y1, y2 = oy + ROW_H + 16, oy + ROW_H + 32
d.arrow([(cx(CH), oy + ROW_H + 2), (cx(CH), y1), (cx(0), y1), (cx(0), sy - 3)], ACC, "acc", 1.4)
d.arrow([(cx(FH_), oy + ROW_H + 2), (cx(FH_), y2), (cx(1), y2), (cx(1), sy - 3)], ACC, "acc", 1.4)
labels = ORIG[:]
labels[CH], labels[FH_] = "C′", "F′"
kinds = ["base"] * N
kinds[CH] = kinds[FH_] = "new"
cellrow(oy, labels, kinds)
cellrow(sy, ["C", "F"] + [""] * (N - 2), ["saved", "saved"] + ["empty"] * (N - 2))
d.t(X0 + N * CW + 16, sy + 17, "쓰기 전에", 12, ACC, KR, "start", 600)
d.t(X0 + N * CW + 16, sy + 34, "원래 블록 복사", 12, ACC, KR, "start", 600)
gauge(oy + 8, 2 / N, WARN, "바뀐 블록만큼 오름")
d.tone(GX0, sy - 4, GX1 - GX0, 48, BAD, 6)
d.t(GX0 + 12, sy + 16, "50M 다 차면 무효", 12, BAD, KR, "start", 600)
d.t(GX0 + 12, sy + 34, "lvs Attr I", 12, BAD, MONO, "start")
end2 = sy + ROW_H

# 3. 되돌리기
top3 = end2 + 36
d.line(LX, top3 - 18, W - 24, top3 - 18, RULE, 0.8, "2 4")
oy, sy = cut(top3, "3. 되돌리기", "lvconvert --merge vg0/snap", OK)
y1, y2 = sy - 32, sy - 16      # 왼쪽 칸이 더 높이 돌아 선이 엇갈리지 않게
d.arrow([(cx(0), sy - 2), (cx(0), y1), (cx(CH), y1), (cx(CH), oy + ROW_H + 3)], OK, "ok", 1.4)
d.arrow([(cx(1), sy - 2), (cx(1), y2), (cx(FH_), y2), (cx(FH_), oy + ROW_H + 3)], OK, "ok", 1.4)
kinds = ["base"] * N
kinds[CH] = kinds[FH_] = "back"
cellrow(oy, ORIG, kinds)
cellrow(sy, ["C", "F"] + [""] * (N - 2), ["base", "base"] + ["empty"] * (N - 2))
d.t(X0 + N * CW + 16, sy + 17, "병합이 끝나면", 12, SOFT, KR, "start")
d.t(X0 + N * CW + 16, sy + 34, "snap 제거", 12, SOFT, KR, "start")
d.box(GX0, oy - 4, GX1 - GX0, 48, PAPER2, RULE, 1, 6)
d.t(GX0 + 12, oy + 16, "열려 있으면", 12, MUTED, KR, "start")
d.t(GX0 + 12, oy + 34, "다음 활성화로 미룸", 12, MUTED, KR, "start")
d.box(GX0, sy - 4, GX1 - GX0, 48, PAPER2, RULE, 1, 6)
d.t(GX0 + 12, sy + 16, "잘 끝났으면", 12, MUTED, KR, "start")
d.t(GX0 + 12, sy + 34, "lvremove vg0/snap", 12, INK, MONO, "start")
end3 = sy + ROW_H

d.t(LX, end3 + 30, "블록 이름 A~H·바뀐 C·F·막대 길이는 예시 · 실측 환경(OrbStack)엔 dm-snapshot 이 없어 Data% 는 못 잼",
    11, SOFT, KR, "start")
LEG = end3 + 48
d.legend(LEG, [("COW 로 먼저 복사", ACC), ("새로 쓴 블록", INFO), ("되쓴 블록", OK), ("무효", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.snapshot.svg")
print("ok 05-02.snapshot")
