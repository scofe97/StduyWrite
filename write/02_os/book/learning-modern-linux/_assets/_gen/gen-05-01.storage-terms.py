# 05-01 §2 — 경로 하나가 마운트 지점부터 데이터 블록까지 내려가는 저장 계층 흐름.
# 타입 스펙: type-process — 경로 조회 시 마운트 지점 → 블록 장치 → 파일시스템 → 아이노드 → 블록으로 내려가는 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §2",
      "경로 조회로 따라가는 드라이브에서 아이노드까지의 계층",
      "파일 myfile 조회가 마운트 지점, 볼륨, 슈퍼블록, 아이노드를 거쳐 데이터 블록에 도달하는 흐름. "
      "아이노드는 이름과 데이터를 담지 않고 메타데이터만 쥡니다.",
      "아이노드는 파일 이름과 실제 데이터를 저장하지 않습니다")

CW = 158
CH = 220
GAP = 14
X0 = 20
Y0 = 120

steps = [
    ("1. 마운트 지점", "Mount Point", INFO, [
        ("경로", "myfile", MONO, INK),
        ("마운트", "상위 마운트 지점", KR, INFO),
        ("조회", "findmnt 매핑", KR, MUTED),
        ("역할", "트리 진입점", KR, SOFT),
    ]),
    ("2. 파티션 · 볼륨", "Block Device (lsblk 예)", OK, [
        ("LV", "elementary--vg-root", MONO, OK),
        ("크기", "222.1G (LVM)", MONO, MUTED),
        ("파티션", "sda2 (223.1G)", MONO, MUTED),
        ("드라이브", "sda (223.6G 물리)", KR, SOFT),
    ]),
    ("3. 파일시스템", "Superblock", INFO, [
        ("종류", "ext4", MONO, INFO),
        ("메타데이터", "슈퍼블록 구획", KR, INK),
        ("관리 정보", "블록 크기 4096B", MONO, MUTED),
        ("아이노드 수", "블록 그룹당 개수", KR, SOFT),
    ]),
    ("4. 아이노드", "Inode (Focal)", ACC, [
        ("번호", "Inode 555036", MONO, ACC),
        ("속성", "권한 0664 · 크기 0B", MONO, INK),
        ("소유", "UID 1000 · GID 1001", MONO, MUTED),
        ("핵심", "이름·데이터 미포함", KR, ACC),
    ]),
    ("5. 데이터 블록", "Data Blocks", MUTED, [
        ("저장소", "디스크 섹터 구역", KR, INK),
        ("내용", "바이트 스트림", KR, MUTED),
        ("이름 보관", "디렉터리 항목", KR, INFO),
        ("연결", "아이노드 포인터", KR, SOFT),
    ]),
]

for i, (title, sub, col, items) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y0}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(x, Y0, CW, CH, PAPER2, col, 1.1, 8)

    d.t(x + CW / 2, Y0 + 24, title, 13, col, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 44, sub, 11, SOFT, MONO, "middle")
    d.line(x + 10, Y0 + 54, x + CW - 10, Y0 + 54, RULE, 0.8)

    for j, (k, v, fam, c) in enumerate(items):
        iy = Y0 + 74 + j * 36
        d.box(x + 8, iy, CW - 16, 30, PAPER, RULE, 0.6, 4)
        d.t(x + 14, iy + 12, k, 11, SOFT, KR, "start")
        d.t(x + 14, iy + 26, v, 11, c, fam, "start", 600 if c == ACC else 400)

    if i < len(steps) - 1:
        nx = x + CW
        d.arrow([(nx, Y0 + CH / 2), (nx + GAP - 2, Y0 + CH / 2)], MUTED, "ar", 1.4)

BY = 368
BW = W - 40
BH = 130
d.box(X0, BY, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(X0 + 20, BY + 26, "stat myfile 출력이 가리키는 층위", 13.5, INK, KR, "start", 600)

stat_boxes = [
    ("Device: fc01h/64513d", "어느 볼륨인지 식별", "주:부 번호 252:1", OK),
    ("Inode: 555036", "볼륨 내 메타데이터 인덱스", "크기 · 권한 · 위치 포인터", ACC),
    ("Links: 1", "아이노드를 가리키는 이름 수", "디렉터리 항목 개수", INFO),
    ("IO Block: 4096", "권장 입출력 크기", "st_blksize 값", MUTED),
]

for k, (hdr, sub1, sub2, c) in enumerate(stat_boxes):
    bx = X0 + 16 + k * 206
    d.box(bx, BY + 40, 196, 76, PAPER, c, 1.0, 6)
    d.t(bx + 10, BY + 60, hdr, 11, c, MONO, "start", 600)
    d.t(bx + 10, BY + 80, sub1, 11, INK, KR, "start")
    d.t(bx + 10, BY + 100, sub2, 11, MUTED, KR, "start")

d.legend(524, [("경로와 마운트", INFO), ("블록 장치 및 볼륨", OK),
               ("이 장의 핵심 — 아이노드", ACC), ("데이터 블록", MUTED)])
d.save("05-01.storage-terms.svg")
print("ok 05-01.storage-terms")
