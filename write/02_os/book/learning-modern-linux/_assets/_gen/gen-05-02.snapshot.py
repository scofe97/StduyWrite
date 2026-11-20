# 타입 스펙: type-state
# 05-02 §3 — LVM 스냅숏. 입구 둘(snapshot-origin, snapshot)과 저장소 둘(원본, COW 50M) 구조를 놓고,
#           1. 만든 직후(COW 비어 있음, Data% ≈ 0)
#           2. 원본 쓰기(청크가 처음 바뀔 때만 원래 블록을 COW 에 1회 복사, 이미 옮긴 청크는 재복사 없음)와
#              스냅숏 읽기 경로(안 바뀐 블록은 원본에서, 바뀐 청크는 COW 에서 읽어 특정 시점 상태 조합)
#           3. lvconvert --merge 로 되돌리기(COW 원래 블록을 원본에 되씀)를 세 컷으로 보인다.
# 근거: 커널 snapshot.rst 문서("Reads will come from COW or origin for unchanged data"),
#       커널 dm-snap.c 소스(__origin_write 의 dm_lookup_exception 확인),
#       lvcreate(8) 의 -c chunksize (기본 4KiB), lvs 의 Attr I(Invalid).
# 예시: 블록 A~H, 바뀐 청크 C·F, Data% 게이지는 원리 설명을 위한 도식적 표현이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 800
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "스냅숏의 저장소 둘 · 입구 둘과 청크 CoW 동작",
      "원본 입구(snapshot-origin)와 스냅숏 입구(snapshot)는 원본 저장소와 COW 저장소를 공유한다. "
      "원본 쓰기 시 청크가 처음 바뀔 때만 원래 데이터가 COW 로 1회 복사된다. "
      "스냅숏을 읽을 때는 안 바뀐 청크는 원본에서, 바뀐 청크는 COW 에서 읽어 시점 전체를 조합한다.",
      "스냅숏 크기는 원본 크기가 아니라 스냅숏 생성 후 바뀐 변경분의 누적량이다")

LX = 24
X0, CW, N = 184, 46, 8          # 블록 띠: 8칸 (184 ~ 552)
GX0, GX1 = 690, 896             # 오른쪽 열(Data% · 설명)
ROW_H, GAP = 36, 44


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
        d.t(cx(i), y + 24, lab, 13, INK if kind == "base" else c, MONO, "middle", 600)


def rowname(y, name, sub):
    d.t(LX, y + 15, name, 13, INK, MONO, "start", 600)
    d.t(LX, y + 31, sub, 12, SOFT, KR, "start")


def gauge(y, frac, c, note):
    d.t(GX0, y + 14, "Data%", 13, INK, MONO, "start", 600)
    d.box(GX0 + 56, y + 2, 140, 16, PAPER, RULE, 0.9, 3)
    if frac:
        d.o.append(f'<rect x="{GX0 + 56}" y="{y + 2}" width="{140 * frac:.1f}" height="16" rx="3" '
                   f'fill="{c}55" stroke="{c}" stroke-width="1"/>')
    d.t(GX0, y + 38, note, 12, c, KR, "start")


ORIG = [chr(65 + i) for i in range(N)]
CH, FH_ = 2, 5                      # 바뀌는 블록 C·F


def cut(top, title, cmd, c):
    d.t(LX, top + 14, title, 14, c, KR, "start", 600)
    d.t(270, top + 14, cmd, 12, MUTED, KR if any('가' <= ch <= '힣' for ch in cmd) else MONO, "start")
    oy = top + 30
    sy = oy + ROW_H + GAP
    rowname(oy, "data (origin)", "원본 저장소")
    rowname(sy, "snap (COW)", "COW 장치 50M")
    return oy, sy


# ── 1. 구조와 생성 직후 ──────────────────────────────────────────
oy1, sy1 = cut(104, "1. 구조와 생성 직후", "lvcreate -s -L 50M -n snap /dev/vg0/data", INFO)
cellrow(oy1, ORIG, ["base"] * N)
cellrow(sy1, [""] * N, ["empty"] * N)
d.t(X0 + N * CW + 14, sy1 + 23, "COW 비어 있음", 12, SOFT, KR, "start")
gauge(oy1 + 6, 0, MUTED, "0 근처에서 시작")
d.box(GX0, sy1 - 8, GX1 - GX0, 48, PAPER2, RULE, 1, 6)
d.t(GX0 + 12, sy1 + 12, "입구: vg0/data · vg0/snap", 12, INK, MONO, "start")
d.t(GX0 + 12, sy1 + 28, "저장소: 원본 볼륨 + COW 50M", 12, MUTED, KR, "start")
end1 = sy1 + ROW_H

# ── 2. 원본 쓰기와 스냅숏 읽기 경로 ─────────────────────────────
top2 = end1 + 34
d.line(LX, top2 - 16, W - 24, top2 - 16, RULE, 0.8, "2 4")
oy2, sy2 = cut(top2, "2. 청크 CoW 쓰기와 읽기", "C · F 청크 첫 수정", ACC)

# CoW 복사 화살표 (청크가 처음 바뀔 때만 원래 블록 복사)
y1, y2 = oy2 + ROW_H + 12, oy2 + ROW_H + 24
d.arrow([(cx(CH), oy2 + ROW_H + 2), (cx(CH), y1), (cx(0), y1), (cx(0), sy2 - 3)], ACC, "acc", 1.4)
d.arrow([(cx(FH_), oy2 + ROW_H + 2), (cx(FH_), y2), (cx(1), y2), (cx(1), sy2 - 3)], ACC, "acc", 1.4)

labels2 = ORIG[:]
labels2[CH], labels2[FH_] = "C′", "F′"
kinds2 = ["base"] * N
kinds2[CH] = kinds2[FH_] = "new"
cellrow(oy2, labels2, kinds2)
cellrow(sy2, ["C", "F"] + [""] * (N - 2), ["saved", "saved"] + ["empty"] * (N - 2))

d.t(X0 + N * CW + 14, oy2 + 15, "첫 수정 때 1회 복사", 12, ACC, KR, "start", 600)
d.t(X0 + N * CW + 14, oy2 + 31, "재수정 시 복사 없음", 12, MUTED, KR, "start")

gauge(oy2 + 6, 2 / N, WARN, "바뀐 청크만큼 누적")

d.tone(GX0, sy2 - 8, GX1 - GX0, 48, BAD, 6)
d.t(GX0 + 12, sy2 + 12, "50M 다 차면 무효화", 12, BAD, KR, "start", 600)
d.t(GX0 + 12, sy2 + 28, "snapshot disabled (Attr I)", 12, BAD, MONO, "start")

# 읽기 경로 설명 텍스트
d.t(X0, sy2 + ROW_H + 18, "스냅숏 읽기: 안 바뀐 블록(A·B·D·E·G·H)은 원본에서, 바뀐 청크(C·F)는 COW 에서 읽어 합침", 12, OK, KR, "start")
end2 = sy2 + ROW_H + 24

# ── 3. 되돌리기와 해제 ──────────────────────────────────────────
top3 = end2 + 34
d.line(LX, top3 - 16, W - 24, top3 - 16, RULE, 0.8, "2 4")
oy3, sy3 = cut(top3, "3. 병합과 해제", "lvconvert --merge vg0/snap", OK)

# 되돌리기 화살표
y1m, y2m = sy3 - 24, sy3 - 12
d.arrow([(cx(0), sy3 - 2), (cx(0), y1m), (cx(CH), y1m), (cx(CH), oy3 + ROW_H + 3)], OK, "ok", 1.4)
d.arrow([(cx(1), sy3 - 2), (cx(1), y2m), (cx(FH_), y2m), (cx(FH_), oy3 + ROW_H + 3)], OK, "ok", 1.4)

cellrow(oy3, ORIG, ["back" if i in (CH, FH_) else "base" for i in range(N)])
cellrow(sy3, ["C", "F"] + [""] * (N - 2), ["base", "base"] + ["empty"] * (N - 2))

d.t(X0 + N * CW + 14, sy3 + 15, "병합 완료 시", 12, SOFT, KR, "start")
d.t(X0 + N * CW + 14, sy3 + 31, "snap 자동 제거", 12, SOFT, KR, "start")

d.box(GX0, oy3 - 4, GX1 - GX0, 44, PAPER2, RULE, 1, 6)
d.t(GX0 + 12, oy3 + 15, "열려 있으면 (마운트 중)", 12, MUTED, KR, "start")
d.t(GX0 + 12, oy3 + 31, "다음 활성화 때로 미룸", 12, MUTED, KR, "start")

d.box(GX0, sy3 - 4, GX1 - GX0, 44, PAPER2, RULE, 1, 6)
d.t(GX0 + 12, sy3 + 15, "작업 정상 완료 시", 12, MUTED, KR, "start")
d.t(GX0 + 12, sy3 + 31, "lvremove 로 수동 삭제", 12, INK, KR, "start")
end3 = sy3 + ROW_H

d.t(LX, end3 + 24, "블록 A~H · C·F · 게이지는 도식적 표현 · 청크 기본값 4KiB(lvcreate -c) · 실측 VM 에는 스냅숏 미존재",
    11, SOFT, KR, "start")

LEG = end3 + 42
d.legend(LEG, [("COW 복사 · 변경분", ACC), ("새로 쓴 블록", INFO), ("되쓴 블록", OK), ("COW 잔여량 · 경고", WARN), ("무효 · 한계", BAD)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.snapshot.svg")
print("ok 05-02.snapshot")
