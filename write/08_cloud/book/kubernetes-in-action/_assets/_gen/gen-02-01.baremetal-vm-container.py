# 02-01 §셋 비교 — 앱 셋을 돌리는 세 가지 방식
# 본문: "베어메탈에서는 세 애플리케이션이 같은 커널을 쓰고 전혀 격리되지 않습니다.
#        VM 두 개 사례에서는 A·B 가 같은 VM 에서 돌아 커널을 공유하고, C 는 자기만의 커널을
#        쓰므로 나머지 둘과 격리됩니다." 컨테이너는 커널 하나를 공유하되 격리는 적용한다.
# 타입 스펙: type-layers.md 를 세 벌 나란히 — 커널이 어디에 몇 개 있는가가 요점이라
#           층 구조 자체가 답이다. 세 스택의 층 높이·폭을 같게 두어 커널 칸의 위치와
#           개수만 눈에 남게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 748
d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "커널이 몇 개이고 어디에 있는가",
      "베어메탈은 커널 하나를 격리 없이 나눠 쓰고, VM 은 커널을 나눠 강하게 격리하며, "
      "컨테이너는 커널 하나를 공유하면서 격리를 적용한다.",
      lead="왼쪽으로 갈수록 가볍고 무방비, 오른쪽으로 갈수록 무겁고 강한 격리 — 컨테이너는 그 사이다")

CX = [186, 500, 814]
SW, ROW_H, GAP = 280, 46, 8
TOP = 214

ddx.band(d, 104, 692, "컨테이너의 점선은 커널은 공유하되 namespace·cgroup 으로 격리한다는 뜻이다")

def stack(cx, title, sub, rows):
    d.t(cx, 186, title, 13, INK, KR, "middle", 600)
    d.t(cx, 204, sub, 10, SOFT, KR)
    y = TOP
    for label, c, dash, h in rows:
        d.o.append(f'<rect x="{cx-SW//2}" y="{y}" width="{SW}" height="{h}" rx="5" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
                   f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
        d.t(cx, y + h // 2 + 4, ddx.fit(label, 11, SW - 20, label), 11, c, KR)
        y += h + GAP
    return y

def apps(cx, y, names, c, dash=False):
    n = len(names)
    w = (SW - (n - 1) * 8) // n
    for i, nm in enumerate(names):
        x = cx - SW // 2 + i * (w + 8)
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ROW_H}" rx="5" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
                   f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
        d.t(x + w // 2, y + 29, nm, 11, c, KR)
    return y + ROW_H + GAP

# ① 베어메탈
y = apps(CX[0], TOP, ["App A", "App B", "App C"], WARN)
d.t(CX[0], 186, "① 베어메탈", 13, INK, KR, "middle", 600)
d.t(CX[0], 204, "격리가 없다", 10, SOFT, KR)
for label, c, h in [("커널 하나 — 격리 없음", BAD, ROW_H), ("물리 하드웨어", MUTED, ROW_H)]:
    d.o.append(f'<rect x="{CX[0]-SW//2}" y="{y}" width="{SW}" height="{h}" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(CX[0], y + h // 2 + 4, label, 11, c, KR)
    y += h + GAP

# ② VM 두 개
# 그룹 경계가 없으면 App C 가 게스트 커널 1 아래에 있어 VM1 소속처럼 읽힌다.
# 두 VM 을 점선으로 묶고 사이를 벌려 소속을 못 박는다.
d.t(CX[1], 186, "② VM 두 개", 13, INK, KR, "middle", 600)
d.t(CX[1], 204, "커널이 나뉜다", 10, SOFT, KR)
y2 = TOP + 6
for gi, (names, tag) in enumerate(((["App A", "App B"], "게스트 커널 1"),
                                   (["App C"], "게스트 커널 2"))):
    gtop = y2 - 8
    y2 = apps(CX[1], y2, names, INFO)
    d.o.append(f'<rect x="{CX[1]-SW//2}" y="{y2}" width="{SW}" height="{ROW_H}" rx="5" '
               f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.1"/>')
    d.t(CX[1], y2 + 29, tag, 11, BAD, KR)
    y2 += ROW_H
    d.o.append(f'<rect x="{CX[1]-SW//2-12}" y="{gtop}" width="{SW+24}" height="{y2-gtop+8}" '
               f'rx="8" fill="none" stroke="{RULE}" stroke-width="1.1" stroke-dasharray="7 6"/>')
    # 그룹 라벨은 상자 옆에 두면 App 상자에 가린다 — 테두리 위 마스크(ring_label)로 얹는다
    ddx.ring_label(d, CX[1] - SW // 2 - 12, gtop, f"VM {gi+1}", 10, SOFT, off=14)
    y2 += 26
for label in ("하이퍼바이저", "물리 하드웨어"):
    d.o.append(f'<rect x="{CX[1]-SW//2}" y="{y2}" width="{SW}" height="{ROW_H}" rx="5" '
               f'fill="{MUTED}12" stroke="{MUTED}" stroke-width="1.1"/>')
    d.t(CX[1], y2 + 29, label, 11, MUTED, KR)
    y2 += ROW_H + GAP

# ③ 컨테이너 셋
d.t(CX[2], 186, "③ 컨테이너 셋", 13, INK, KR, "middle", 600)
d.t(CX[2], 204, "공유하되 격리한다", 10, SOFT, KR)
y3 = apps(CX[2], TOP, ["Ctr A", "Ctr B", "Ctr C"], OK, dash=True)
for label, c in (("호스트 커널 하나 — 격리 적용", OK), ("물리 하드웨어", MUTED)):
    d.o.append(f'<rect x="{CX[2]-SW//2}" y="{y3}" width="{SW}" height="{ROW_H}" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(CX[2], y3 + 29, ddx.fit(label, 11, SW - 20, label), 11, c, KR)
    y3 += ROW_H + GAP

for cx, tag, c in ((CX[0], "커널 1개 · 격리 0", WARN), (CX[1], "커널 2개 · 격리 강함", BAD),
                   (CX[2], "커널 1개 · 격리 있음", OK)):
    # VM 열이 가장 높다(6단 → 530 까지) — 칩과 산문은 그 아래로
    d.chip(cx, 604, tag, c, 11)

d.t(36, 644, "VM 은 커널을 하나 더 얹어 격리를 사고, 컨테이너는 커널을 공유한 채 커널의 기능으로 "
             "격리를 만든다.", 12, MUTED, KR, "start")
d.t(36, 668, "베어메탈은 그 격리를 아예 사지 않은 상태다.", 12, MUTED, KR, "start")
d.legend(708, [("격리되지 않은 앱", WARN), ("추가로 얹은 커널", BAD),
               ("격리된 컨테이너와 공유 커널", OK)])
d.save("02-01-baremetal-vm-container.svg")
print("ok baremetal-vm-container")
