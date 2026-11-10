# 05-02 전체 개요 — 디스크 감지부터 영구 마운트까지의 6단계 흐름.
# 타입 스펙: type-process — 순서가 화살표로 흐르고 단계마다 입력 · 명령 · 산출 슬롯이 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
d = D(W, H, "LEARNING MODERN LINUX · 05-02 OVERVIEW",
      "디스크 핫애드부터 영구 마운트까지의 6단계 운영 파이프라인",
      "물리 디스크 인식, 파티셔닝, LVM 계층화, 파일시스템 생성, 마운트 및 fstab 등록까지 "
      "스토리지를 운영 트리에 편입하는 표준 절차.",
      "새로 붙일 때는 아래 층(물리)에서 위 층(VFS/마운트)으로 진행")

CW, CH, GAPX, GAPY, X0, Y0 = 268, 168, 18, 22, 16, 120
steps = [
    ("1. 커널 재스캔", "sysfs / rescan", "echo 1 > /sys/class/.../rescan", "dmesg 장치 등록 (sdb, loop)", INFO),
    ("2. 파티셔닝", "parted / GPT", "parted -s /dev/sdb mklabel gpt", "lsblk 파티션 분할 (sdb1, sdb2)", INFO),
    ("3. LVM 계층화", "pv · vg · lv", "pvcreate -> vgcreate -> lvcreate", "블록 볼륨 생성 (/dev/vg0/data)", OK),
    ("4. 파일시스템 생성", "mkfs 포맷", "mkfs.ext4 -L datalv /dev/vg0/data", "슈퍼블록 및 아이노드 테이블 생성", OK),
    ("5. 마운트 연결", "mount / 트리 결합", "mount /dev/vg0/data /mnt/lv", "VFS 경로 노출 (/mnt/lv, 182M)", ACC),
    ("6. 영구 마운트", "fstab 등록", "UUID=... /mnt/lv ext4 defaults 0 2", "부팅 시 systemd mount 유닛 자동화", ACC),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(steps) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 11
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (title, sub, cmd, res, col) in enumerate(steps):
    x, y = pos(i)
    d.box(x, y, CW, CH, PAPER2, col, 1.2, 8)
    d.t(x + 16, y + 26, title, 13.5, col, KR, "start", 600)
    d.t(x + CW - 16, y + 26, sub, 11, SOFT, MONO, "end")
    d.line(x + 14, y + 38, x + CW - 14, y + 38, RULE, 1)

    d.t(x + 16, y + 62, "실행 명령", 11, SOFT, KR, "start")
    d.o.append(f'<rect x="{x + 14}" y="{y + 72}" width="{CW - 28}" height="28" rx="5" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
    d.t(x + 22, y + 90, cmd, 10, INK, MONO, "start")

    d.t(x + 16, y + 124, "생성 결과", 11, SOFT, KR, "start")
    d.t(x + 16, y + 146, res, 11, MUTED, KR, "start")

d.legend(508, [("하드웨어 / 파티션 계층", INFO), ("LVM 볼륨 / 포맷 계층", OK), ("마운트 / 시스템 부팅 계층", ACC)])
d.save("05-02.overview.svg")
print("ok 05-02.overview")
