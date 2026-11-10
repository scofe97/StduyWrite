# 05-01 §8 — CoW(Copy-on-Write) 의 2단계 상태 전이.
# 타입 스펙: type-state — 복사 시점(포인터 공유)과 수정 시점(신규 블록 분기)의 전후 상태 비교.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 576
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "복사할 때는 메타데이터 포인터만, 수정할 때에야 신규 블록 할당",
      "CoW 메커니즘의 전후 상태. 1단계에서는 블록 포인터만 복제해 공간을 아끼고, "
      "2단계에서 쓰기 발생 시에만 수정 블록 C' 이 신규 생성되는 과정.",
      "빠른 입출력과 디스크 공간 절약의 핵심 기법")

PW, PX1, PX2 = 404, 24, 452
PY, PH = 120, 260
BW, BGAP, BY, BH = 80, 10, 280, 72
FY, FH = 190, 32


def panel(x, title, sub, changed):
    d.box(x, PY, PW, PH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, PY + 26, title, 14, INK, KR, "start", 600)
    d.t(x + 20, PY + 46, sub, 11, MUTED, KR, "start")

    for fx, name, col in [(x + 20, "file1 (원본)", INFO), (x + 200, "file2 (복사본)", OK)]:
        d.o.append(f'<rect x="{fx}" y="{FY}" width="124" height="{FH}" rx="5" '
                   f'fill="{col}12" stroke="{col}" stroke-width="1.2"/>')
        d.t(fx + 62, FY + 21, name, 12, col, KR, "middle", 600)

    labels = [("Block A", "4096B"), ("Block B", "4096B"),
              ("Block C", "4096B"), ("Block C′", "4096B 신규")] if changed else [
        ("Block A", "4096B"), ("Block B", "4096B"), ("Block C", "4096B")]
    xs = []
    for j, (b, note) in enumerate(labels):
        bx = x + 20 + j * (BW + BGAP)
        xs.append(bx + BW / 2)
        focal = changed and j == 3
        if focal:
            d.o.append(f'<rect x="{bx}" y="{BY}" width="{BW}" height="{BH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
            d.t(bx + BW / 2, BY + 26, b, 13, ACC, MONO, "middle", 600)
            d.t(bx + BW / 2, BY + 46, note, 11, ACC, KR)
            d.t(bx + BW / 2, BY + 62, "쓰기 복사본", 11, ACC, KR)
        else:
            d.box(bx, BY, BW, BH, PAPER, MUTED, 1.1, 6)
            d.t(bx + BW / 2, BY + 28, b, 13, INK, MONO, "middle", 600)
            d.t(bx + BW / 2, BY + 50, note, 10, MUTED, MONO)

    f1_targets = xs[:3]
    f2_targets = (xs[:2] + [xs[3]]) if changed else xs[:3]
    for tx in f1_targets:
        d.path(f"M {x + 82} {FY + FH} L {tx} {BY - 2}", INFO, 1.0, dash="4 4")
    for k, tx in enumerate(f2_targets):
        col = ACC if (changed and k == 2) else OK
        d.path(f"M {x + 262} {FY + FH} L {tx} {BY - 2}", col, 1.2)


panel(PX1, "1단계 — 초기 복사 (cp file1 file2)", "물리 블록 복제 없이 메타데이터 포인터만 복제", False)
panel(PX2, "2단계 — file2 블록 C 수정", "수정 대상 블록 C 만 복사(C′) · 블록 A·B 는 공유 유지", True)

d.arrow([(432, 240), (448, 240)], MUTED, "ar", 1.4)

# 하단 컨테이너 이미지 연결 카드
BY2 = 400
d.box(PX1, BY2, W - 48, 104, PAPER2, INFO, 1.2, 8)
d.t(PX1 + 20, BY2 + 26, "컨테이너 이미지와 CoW 메커니즘 연결", 13.5, INK, KR, "start", 600)
d.t(PX1 + 20, BY2 + 50, "읽기 전용 베이스 이미지 — 컨테이너 간 기본 레이어 공유",
    11.5, OK, KR, "start")
d.t(PX1 + 20, BY2 + 70, "쓰기 시점의 copy-up — 고칠 파일 전체를 상위 층으로 복사",
    11.5, ACC, KR, "start")
d.t(PX1 + 20, BY2 + 90, "저장 공간 절약 — 고치지 않은 파일은 하위 층을 그대로 공유",
    11, MUTED, KR, "start")

d.legend(524, [("file1 참조 포인터", INFO), ("file2 참조 포인터", OK),
               ("수정 시 신규 할당 블록", ACC)])
d.save("05-01.cow.svg")
print("ok 05-01.cow")
