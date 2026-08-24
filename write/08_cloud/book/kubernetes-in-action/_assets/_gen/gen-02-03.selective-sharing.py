# 02-03 §골라서 공유 — 경계는 종류마다 다르게 그어진다
# 본문: "두 프로세스가 Network·UTS 네임스페이스는 공유하고 Mount 만 각자 씁니다.
#        그래서 같은 IP 로 통신하되 파일시스템은 격리됩니다."
#       "쿠버네티스 Pod 가 바로 이 방식입니다."
# 타입 스펙: type-nested.md — 경계가 종류마다 다르게 그어지는 것이 요점이므로, 공유하는
#           경계는 두 프로세스를 함께 감싸고 격리하는 경계는 따로 감싼다. 경계선의 모양
#           자체가 답이라 그림이 문장을 대신한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 644
d = D(W, H, "KUBERNETES IN ACTION · 02-03",
      "공유하는 경계는 둘을 함께 감싸고, 격리하는 경계는 따로 감싼다",
      "net·uts 네임스페이스는 두 프로세스를 하나로 묶어 같은 IP·호스트명을 보게 하고, mnt "
      "네임스페이스는 각자를 따로 감싸 파일시스템을 가른다.",
      lead="쿠버네티스 Pod 가 바로 이 방식이다 — 그래서 컨테이너 경계가 한 줄로 안 그어진다")

SHARE = (72, 208, 856, 176)
P1, P2 = (300, 296), (700, 296)
# mnt 그룹의 ring_label 마스크(그룹 top ±9)가 공유 경계 밑변(384)에 닿으면 그 선을 끊는다.
# 그래서 그룹을 480 으로 내려 마스크가 403~421 에 오게 했다.
M1, M2 = (300, 480), (700, 480)
BW, BH = 300, 84

ddx.band(d, 104, 588, "경계가 종류마다 다르게 그어지므로 '컨테이너 경계' 는 프로세스마다 딱 겹치지 않는다")

sx, sy, sw, sh = SHARE
d.o.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" '
           f'fill="{OK}08" stroke="{OK}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, sx, sy, "net · uts 네임스페이스 — 둘이 함께 쓴다 (같은 eth0 · lo · 호스트명)",
               11, OK, off=16)

def box(cx, cy, t, s, c, dash=False):
    d.o.append(f'<rect x="{cx-BW//2}" y="{cy-BH//2}" width="{BW}" height="{BH}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
               f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(cx, cy - 8, ddx.fit(t, 13, BW - 18, t), 13, c, KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, BW - 14, t), 10, SOFT, KR)

box(*P1, "Process 1", "같은 IP 에 바인딩한다", INFO)
box(*P2, "Process 2", "lo 로 P1 과 통신한다", INFO)
d.path(f"M {P1[0]+BW//2+6} {P1[1]} L {P2[0]-BW//2-10} {P2[1]}", OK, 1.6, m="ok")
# 두 상자 사이는 450~550 (100px) — 칩이 124px 이면 양쪽을 12px 씩 덮는다
d.chip(500, P1[1], "lo 로 통신", OK, 11)

for (cx, cy), name, fs in ((M1, "mnt 네임스페이스 A", "filesystem A"),
                           (M2, "mnt 네임스페이스 B", "filesystem B")):
    d.o.append(f'<rect x="{cx-BW//2-16}" y="{cy-BH//2-26}" width="{BW+32}" height="{BH+42}" '
               f'rx="8" fill="{WARN}08" stroke="{WARN}" stroke-width="1.4" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, cx - BW // 2 - 16, cy - BH // 2 - 26, name, 11, WARN, off=14)
    box(cx, cy, fs, "이 프로세스만 본다", WARN)

for cx in (P1[0], P2[0]):
    d.path(f"M {cx} {P1[1]+BH//2+6} L {cx} {M1[1]-BH//2-36}", MUTED, 1.4, m="ar")

d.t(36, 562, "net·uts 는 겹치고 mnt 는 갈린다 — 겹치는 만큼 한 머신처럼 통신하고, 갈리는 만큼 "
             "서로의 파일을 못 본다.", 12, MUTED, KR, "start")
d.legend(604, [("함께 쓰는 경계", OK), ("각자 쓰는 경계", WARN), ("프로세스", INFO)])
d.save("02-03-selective-sharing.svg")
print("ok selective-sharing")
