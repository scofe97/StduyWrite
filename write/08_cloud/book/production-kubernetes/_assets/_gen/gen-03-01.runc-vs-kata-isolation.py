# 타입 스펙: type-nested
# 03-01.runc-vs-kata-isolation — runc 컨테이너와 Kata 경량 VM 의 격리 경계
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, ACC, INFO, OK, PAPER, KR, MONO

W, H = 1000, 496
d = D(W, H, "ISOLATION · 03-01",
      "컨테이너와 경량 VM 의 격리 경계",
      "runc 컨테이너는 호스트 커널을 함께 쓰고 Kata 파드는 VM 마다 게스트 커널을 따로 가집니다",
      lead="경계가 커널 안쪽에 있는가 커널 바깥쪽에 있는가")

TOP, OUT_H = 124, 292


def ring(x, y, w, h, c, label, op="08", sw=1.2, label_c=None):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}{op}" '
               f'stroke="{c}" stroke-width="{sw}"/>')
    lw = len(label) * 12.5 + 14
    d.o.append(f'<rect x="{x + 14}" y="{y - 9}" width="{lw}" height="18" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 12, label_c or c, KR, "start", 600)


# 왼쪽 — runc
LX, PW = 20, 460
d.t(LX, TOP - 14, "runc 컨테이너 — 커널 하나를 공유", 14, INK, KR, "start", 600)
ring(LX, TOP, PW, OUT_H, MUTED, "호스트 노드", "05", 1.0)
ring(LX + 24, TOP + 36, PW - 48, OUT_H - 60, INFO, "호스트 커널", "10", 1.4)
for i, nm in enumerate(["파드 A 컨테이너", "파드 B 컨테이너"]):
    x = LX + 48 + i * 196
    d.box(x, TOP + 96, 176, 100, "#161B22", MUTED, 1.0)
    d.t(x + 88, TOP + 142, nm, 13, INK, KR, "middle", 600)
    d.t(x + 88, TOP + 164, "cgroup · 네임스페이스", 11, MUTED, MONO)

# 오른쪽 — Kata
RX = 520
d.t(RX, TOP - 14, "Kata Containers — 파드마다 게스트 커널", 14, INK, KR, "start", 600)
ring(RX, TOP, PW, OUT_H, MUTED, "호스트 노드", "05", 1.0)
for i, nm in enumerate(["경량 VM · 파드 A", "경량 VM · 파드 B"]):
    x = RX + 24 + i * 216
    ring(x, TOP + 52, 196, 192, OK, nm, "08", 1.2)
    ring(x + 14, TOP + 84, 168, 140, ACC, "게스트 커널", "12", 1.4)
    d.box(x + 28, TOP + 124, 140, 84, "#161B22", MUTED, 1.0)
    d.t(x + 98, TOP + 162, "컨테이너", 13, INK, KR, "middle", 600)
    d.t(x + 98, TOP + 184, "cgroup · 네임스페이스", 11, MUTED, MONO)

d.tone(RX + 24, TOP + 252, PW - 48, 28, INFO, 6, "10", 1.4)
d.t(RX + PW / 2, TOP + 271, "호스트 커널", 13, INFO, KR, "middle", 600)

d.legend(452, [("호스트 커널", INFO), ("경량 VM 경계", OK), ("게스트 커널", ACC), ("컨테이너", MUTED)])
d.save(str(Path(__file__).resolve().parent.parent / "03-01.runc-vs-kata-isolation.svg"))
print("ok 03-01.runc-vs-kata-isolation")
