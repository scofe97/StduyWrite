# 08-02 §2 — /dev/shm(tmpfs)에 400MiB 를 쓰기 전과 뒤의 free -m 을 total 의 네 조각으로 나눈다.
# 실측: debian:12 컨테이너 --shm-size=600m, `free -m` → dd 400MiB to /dev/shm → `free -m` (2026-11-10).
#   전: total 8004 used 2026 free 4899 shared 79  buff/cache 1361 available 5977
#   뒤: total 8004 used 2429 free 4495 shared 479 buff/cache 1762 available 5574
# 조각(계산값): A = total − free − buff/cache, B = buff/cache − (available − free),
#              C = available − free, D = free. used ≈ A+B, buff/cache = B+C, available = C+D.
# 1차 자료: free(1) used "calculated as total - available", shared "Shmem", tmpfs 문서 "all tmpfs pages
#           will be shown as Shmem in /proc/meminfo and Shared in free(1)".
# 타입 스펙: type-bar — stacked bars. 조각을 total 까지 쌓고 focal 조각(B)만 accent, 나머지는 muted tint.
#           가로 방향만 쓰고 값 축은 왼쪽→오른쪽(0 → 8004 MiB)이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, RULE, KR, MONO

W, H = 960, 488
X0, PW, TOTAL, BH = 168, 760, 8004, 40
K = PW / TOTAL

ROWS = [
    ("쓰기 전", "shared 79", 150, dict(A=1744, B=283, C=1078, D=4899, sh=79,
                                       used=2026, bc=1361, av=5977)),
    ("400MiB 쓴 뒤", "shared 479", 316, dict(A=1747, B=683, C=1079, D=4495, sh=479,
                                            used=2429, bc=1762, av=5574)),
]
SEG = [("A", INFO, "2E"), ("B", ACC, "2E"), ("C", SOFT, "3A"), ("D", OK, "22")]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §2",
      "tmpfs 400MiB 가 옮겨 놓는 free 의 칸",
      "같은 total 8004MiB 를 네 조각으로 나눴다. /dev/shm 에 400MiB 를 쓰면 내어 줄 수 없는 캐시 조각이 "
      "커지고, 그 조각이 used 와 buff/cache 양쪽에 함께 잡힌다.",
      "used 와 shared 가 함께 컸다면 tmpfs·공유 메모리를 먼저 봅니다")


def bracket(x1, x2, y, up, label, c):
    h = 6 if up else -6
    d.path(f"M {x1} {y + h} L {x1} {y} L {x2} {y} L {x2} {y + h}", c, 1.2)
    d.t((x1 + x2) / 2, y - 8 if up else y + 18, label, 12, c, MONO, "middle", 600)


for name, sub, y, v in ROWS:
    d.t(24, y + 18, name, 13, INK, KR, "start", 600)
    d.t(24, y + 36, sub, 12, ACC, MONO, "start")
    x = X0
    xs = {}
    for key, c, op in SEG:
        w = v[key] * K
        xs[key] = (x, x + w)
        if key == "B":
            d.tone(x, y, w, BH, ACC, 2, "33", 1.4)
            d.o.append(f'<rect x="{x + w - v["sh"] * K}" y="{y + 4}" width="{v["sh"] * K - 2}" '
                       f'height="{BH - 8}" rx="1" fill="{ACC}88"/>')
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="2" fill="{c}{op}" '
                       f'stroke="{c}" stroke-width="0.8"/>')
        if w > 44 and key != "B":
            d.t(x + w / 2, y + 25, str(v[key]), 12, INK, MONO)
        x += w
    if xs["B"][1] - xs["B"][0] > 44:
        d.t((xs["B"][0] + xs["B"][1]) / 2, y + 25, str(v["B"]), 12, INK, MONO)
    bracket(xs["A"][0], xs["B"][1] - 2, y - 12, True, f"used {v['used']}", INFO)
    bracket(xs["C"][0] + 2, xs["D"][1], y - 12, True, f"available {v['av']}", OK)
    bracket(xs["B"][0], xs["C"][1], y + BH + 12, False, f"buff/cache {v['bc']}", MUTED)

AY = 412
d.line(X0, AY, X0 + PW, AY, RULE, 1)
for m in (0, 2000, 4000, 6000, 8004):
    xx = X0 + m * K
    d.line(xx, AY, xx, AY - 6, RULE, 1)
    d.t(xx, AY + 16, str(m), 11, SOFT, MONO)
d.t(X0 - 16, AY + 16, "MiB", 11, SOFT, MONO, "end")

d.legend(H - 44, [("프로세스·커널", INFO), ("내어 줄 수 없는 캐시", ACC), ("내어 줄 캐시", SOFT),
                  ("free", OK)])
d.save("08-02.free-split.svg")
print("ok 08-02.free-split")
