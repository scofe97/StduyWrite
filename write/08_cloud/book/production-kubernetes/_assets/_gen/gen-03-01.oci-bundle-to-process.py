# 타입 스펙: type-data-flow
# 03-01.oci-bundle-to-process — 고수준 런타임이 OCI 번들을 만들고 runc 가 프로세스로 띄우는 길
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, ACC, INFO, OK, KR, MONO

W, H = 1000, 452
LANE_X, LANE_W = 12, 116
COL_X0, SLOT, CARD_W, CARD_H = 160, 216, 164, 60
LANE_Y0, LANE_STRIDE = 124, 100

d = D(W, H, "OCI BUNDLE · 03-01",
      "OCI 번들이 runc 를 거쳐 프로세스가 되는 길",
      "이미지 계층과 config.json 이 번들이 되고 runc create 와 start 가 그 번들을 프로세스로 바꾸는 순서",
      lead="번들 준비 → runc create → runc start")

LANES = [("고수준 런타임", "containerd 등", INFO),
         ("OCI 런타임", "runc", MUTED),
         ("리눅스 커널", "격리와 실행", OK)]
for k, (nm, sub, c) in enumerate(LANES):
    y = LANE_Y0 + LANE_STRIDE * k
    d.box(LANE_X, y, LANE_W, 76, "#161B22", c + "88", 1.0)
    d.t(LANE_X + LANE_W / 2, y + 32, nm, 12, INK, KR, "middle", 600)
    d.t(LANE_X + LANE_W / 2, y + 54, sub, 11, MUTED, MONO)


def cx(col):
    return COL_X0 + SLOT * col + CARD_W / 2


def top(lane):
    return LANE_Y0 + LANE_STRIDE * lane + 8


# 번들 경계 (focal)
bx, by = cx(0) - CARD_W / 2 - 12, top(0) - 20
bw, bh = SLOT + CARD_W + 24, CARD_H + 32
d.o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{ACC}12" '
           f'stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 4"/>')
d.t(bx + 12, by + 14, "OCI 번들 = rootfs + config.json", 11, ACC, MONO, "start")

NODES = [
    (0, 0, "이미지 계층 병합", "TAR 계층 → rootfs", INFO),
    (0, 1, "config.json 작성", "args · env · mounts", INFO),
    (1, 2, "runc create", "<id> <번들 경로>", MUTED),
    (1, 3, "runc start", "<id>", MUTED),
    (2, 2, "격리 환경 구성", "네임스페이스 · cgroup", OK),
    (2, 3, "사용자 프로세스 실행", "config.json 의 process", OK),
]
for lane, col, title, sub, c in NODES:
    x = cx(col) - CARD_W / 2
    y = top(lane)
    d.tone(x, y, CARD_W, CARD_H, c, 6, "10", 1.2)
    fam = MONO if title.startswith(("runc", "config")) else KR
    d.t(cx(col), y + 26, title, 13, c, fam, "middle", 600)
    d.t(cx(col), y + 46, sub, 12, MUTED, MONO if sub.startswith("<") else KR)

# 화살표 — 직각만 쓴다
y0 = top(0) + CARD_H / 2
d.arrow([(cx(0) + CARD_W / 2 + 4, y0), (cx(1) - CARD_W / 2 - 6, y0)], MUTED, "ar", 1.5)
d.arrow([(cx(1) + CARD_W / 2 + 4, y0), (cx(2), y0), (cx(2), top(1) - 4)], ACC, "acc", 1.6)
d.chip((cx(1) + CARD_W / 2 + cx(2)) / 2, y0 - 18, "번들 경로", ACC, 12)
y1 = top(1) + CARD_H / 2
d.arrow([(cx(2) + CARD_W / 2 + 4, y1), (cx(3) - CARD_W / 2 - 6, y1)], MUTED, "ar", 1.5)
d.chip(cx(2) + 56, top(1) + CARD_H + 20, "created", MUTED, 12)
d.arrow([(cx(2), top(1) + CARD_H + 2), (cx(2), top(2) - 4)], MUTED, "ar", 1.5)
d.arrow([(cx(3), top(1) + CARD_H + 2), (cx(3), top(2) - 4)], MUTED, "ar", 1.5)
d.chip(cx(3) + 44, top(1) + CARD_H + 20, "running", OK, 12)

d.legend(412, [("고수준 런타임이 준비", INFO), ("runc 의 OCI 연산", MUTED),
               ("커널에서 일어나는 일", OK), ("OCI 번들", ACC)])
d.save(str(Path(__file__).resolve().parent.parent / "03-01.oci-bundle-to-process.svg"))
print("ok 03-01.oci-bundle-to-process")
