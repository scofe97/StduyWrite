# 05-01 §9 — 유니온 마운트가 만드는 합집합과, 겹치는 자리에서 생기는 문제.
# 원문("Copy-on-Write Filesystems"): "This is the idea that you can combine (mount) multiple directories
#       into one location so that, to the user of the resulting directory, it appears that said directory
#       contains the combined content (or: union) of all the participating directories. With union mounts,
#       you often come across the terms upper filesystem and lower filesystem, hinting at the layering
#       order of the mounts."
#       "With union mounts, the devil is in the details. You have to come up with rules around what happens
#       when a file exists in multiple places or what writing to or removing files means."
# 주의: 겹치는 자리에서 어느 쪽이 이기는지를 원문은 규칙으로 적지 않는다. 상위·하위라는 층 순서만
#       밝히므로 도식도 "정해야 한다" 까지만 적고 승패를 단정하지 않는다.
# 타입 스펙: type-venn — 두 집합과 그 교집합이 논점일 때. accent 는 교집합, 곧 저자가
#           "세부에 악마가 있다" 고 적은 자리. 축약: 참여 디렉토리는 둘로 줄였다(원문은 여럿).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 688
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §9",
      "겹쳐 놓으면 하나로 보이고, 겹친 자리에서 규칙이 필요해진다",
      "여러 디렉토리를 한 자리에 마운트하면 쓰는 사람에게는 합집합 하나로 보인다. "
      "문제는 같은 이름이 양쪽에 있을 때다.",
      "상위와 하위라는 말은 마운트의 층 순서를 가리킵니다")

CY, R = 300, 120
LCX, RCX = 436, 606
MID = (LCX + RCX) / 2
d.o.append(f'<circle cx="{LCX}" cy="{CY}" r="{R}" fill="{INFO}10" stroke="{INFO}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{RCX}" cy="{CY}" r="{R}" fill="{OK}10" stroke="{OK}" stroke-width="1.4"/>')

d.t(LCX - 58, CY - 84, "상위 파일시스템", 13, INFO, KR, "middle", 600)
d.t(RCX + 58, CY - 84, "하위 파일시스템", 13, OK, KR, "middle", 600)

for i, txt in enumerate(["cache/", "run.log"]):
    d.t(LCX - 58, CY - 6 + i * 26, txt, 12, INK, MONO)
for i, txt in enumerate(["bin/", "lib/", "etc/"]):
    d.t(RCX + 58, CY - 18 + i * 26, txt, 12, INK, MONO)

d.t(MID, CY - 40, "같은 이름", 12.5, ACC, KR, "middle", 600)
d.t(MID, CY - 16, "app.conf", 12, ACC, MONO)
d.t(MID, CY + 12, "어느 쪽이", 11.5, ACC, KR)
d.t(MID, CY + 32, "보일지", 11.5, ACC, KR)

d.box(32, 248, 224, 104, PAPER2, RULE, 1.0, 8)
d.t(48, 276, "쓰는 사람이 보는 것", 14, INK, KR, "start", 600)
d.t(48, 300, "디렉토리 하나", 12, MUTED, KR, "start")
d.t(48, 322, "app.conf · cache/ · run.log", 11.5, SOFT, MONO, "start")
d.t(48, 340, "bin/ · lib/ · etc/", 11.5, SOFT, MONO, "start")
d.path(f"M 256 300 L {LCX - R - 8} 300", MUTED, 1.4, m="ar")

RY = 448
d.o.append(f'<rect x="292" y="{RY}" width="336" height="100" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(312, RY + 28, "정해야 하는 규칙 둘", 13.5, ACC, KR, "start", 600)
d.t(312, RY + 52, "파일이 여러 곳에 있을 때 어떻게 할지", 11.5, ACC, KR, "start")
d.t(312, RY + 72, "쓰거나 지우는 것이 무슨 뜻인지", 11.5, ACC, KR, "start")
d.t(312, RY + 92, "저자는 세부에 악마가 있다고 적습니다", 11.5, MUTED, KR, "start")
d.path(f"M {MID} {CY + R} L {MID} {RY - 2}", ACC, 1.3, m="acc", dash="6 5")

d.tone(32, 568, W - 64, 44, OK)
d.t(52, 596, "구현은 넷 — Unionfs · OverlayFS · AUFS · btrfs. 오늘날 Docker 의 기본은 overlay2 입니다.",
    12, MUTED, KR, "start")

d.legend(628, [("위에 얹히는 층", INFO), ("아래에 깔리는 층", OK), ("규칙이 필요한 자리", ACC)])
d.save("05-01.union-mount.svg")
print("ok 05-01.union-mount")
