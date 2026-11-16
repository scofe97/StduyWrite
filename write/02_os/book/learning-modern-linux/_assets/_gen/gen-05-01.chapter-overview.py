# 05-01 학습 목표 뒤 전체 지도 — 5장 개념 편의 절 여덟과 05-02 연계를 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 다루는 객체 · 그 절 도식의 실측 값)이
#           반복되고 읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
# 판단: 본문이 이 자리에 "읽는 순서로 이은 지도"를 요구하고, 절 순서(용어 → 링크 → VFS → LVM → …)는
#       저장 장치의 층 순서와 다르다. 층 순서로 다시 놓으면 읽는 순서가 사라지므로 순서 지도는 두고,
#       카드마다 그 절 도식이 쓰는 객체 이름과 실측 값(Inode 555036, PE 57105, 2664 B 등)을 칩으로 붙여
#       다른 도식과 용어를 맞췄다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO, INFO

W, H = 920, 568
d = D(W, H, "LEARNING MODERN LINUX · 05-01",
      "모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다",
      "5장 개념 편의 절 여덟을 읽는 순서로 이은 지도. 1~3절이 용어와 링크, 4~5절이 VFS 와 LVM 간접 층, "
      "6~8절이 디렉터리 배치와 가짜 파일시스템 및 CoW · 유니온 마운트다. 카드마다 그 절이 다루는 객체와 "
      "그 절 도식에 나오는 실측 값을 붙였다.",
      "7절 가짜 파일시스템이 이 장의 제목이 가리키는 핵심 자리")

CW, CH, GAPX, GAPY, X0, Y0 = 280, 112, 16, 24, 24, 104
cards = [
    ("§1", "전제 다섯", "계층형 트리 · 권한 내장 · 커널 공간", "ls · cd · pwd"),
    ("§2", "드라이브에서 아이노드까지", "sda → 볼륨 → 슈퍼블록 → 아이노드", "Inode: 555036"),
    ("§3", "하드 링크와 심볼릭 링크", "같은 아이노드 · 경로 문자열", "6302071 · Links: 2"),
    ("§4", "VFS 추상 층", "file · dentry · inode · super_block", "연산자 테이블"),
    ("§5", "LVM", "PE 를 VG 풀에 모아 LV 로 나눔", "PE 57105"),
    ("§6", "디렉터리 배치", "FHS 와 바인드 마운트", "man hier"),
    ("§7", "가짜 파일시스템", "procfs · sysfs · devtmpfs", "/proc/cpuinfo · 2664 B"),
    ("§8", "보통 파일과 CoW", "CoW 블록 · OverlayFS copy-up", "C′ · lowerdir · upperdir"),
    ("05-02 연계", "키울 때는 아래 층부터", "디스크 → LVM → mkfs → mount → fstab", "/dev/vg0/data"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW + 2, y1 + CH / 2), (x2 - 3, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH + 2} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 3}", MUTED, 1.3, m="ar")

for i, (n, title, sub, chip) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 6)
    is_next = (i == 8)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif is_next:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{INFO}08" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)

    col = ACC if focal else (INFO if is_next else SOFT)
    tcol = ACC if focal else (INFO if is_next else INK)
    d.t(x + 16, y + 24, n, 12, col, MONO if not is_next else KR, "start", 600)
    d.t(x + 16, y + 48, title, 14, tcol, KR, "start", 600)
    d.t(x + 16, y + 70, sub, 12, MUTED, KR, "start")
    kr = any("가" <= ch <= "힣" for ch in chip)
    cwid = sum(12 if "가" <= ch <= "힣" else 7.4 for ch in chip) + 20
    d.o.append(f'<rect x="{x + 16}" y="{y + 82}" width="{cwid:.0f}" height="20" rx="4" fill="{PAPER}" '
               f'stroke="{col}" stroke-width="0.9"/>')
    d.t(x + 26, y + 96, chip, 12, ACC if focal else (INFO if is_next else MUTED), KR if kr else MONO, "start")

d.legend(516, [("균일한 손잡이가 블록 장치 밖으로 뻗는 자리", ACC), ("운영 절차를 다루는 다음 편", INFO)])
d.save("05-01.chapter-overview.svg")
print("ok 05-01.chapter-overview")
