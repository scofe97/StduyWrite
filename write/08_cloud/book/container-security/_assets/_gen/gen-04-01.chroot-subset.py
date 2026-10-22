# 타입 스펙: type-nested — 호스트 파일시스템 / 안에 new_root/ 와 alpine/ 이 들어 있고, chroot alpine 뒤에는 alpine/ 안쪽만 프로세스의 / 로 보이며 바깥으로 올라갈 길이 막힌다. focal 은 alpine/.
# 사실 출처: 노트 L152~L156(루트보다 위로 올라갈 방법 없음), L162~L167(mkdir new_root, chroot new_root 실패), L173~L179(alpine, ls, /bin, PATH), L203~L206(mount -t proc proc /proc).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, BAD, INFO, KR, MONO, PAPER2

W, H = 984, 500


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def inner_label(x, y, txt, fill=MUTED, size=12):
    d.t(x, y, txt, size, fill, kr(txt), "start", 600)


d = D(W, H, "NESTED · 04-01 §4",
      "루트를 바꾸면 그보다 위로 올라갈 길이 없어 파일시스템의 일부만 보입니다",
      "호스트 파일시스템 / 안에 new_root/ 와 alpine/ 두 디렉토리가 있다. new_root/ 는 비어 있어 chroot 뒤 /bin/bash 를 실행하지 못한다. "
      "sudo chroot alpine ls 처럼 alpine/ 으로 루트를 바꾸면 alpine/bin 이 /bin 으로 보이고, 그 위의 호스트 나머지 영역으로는 올라갈 길이 막힌다.",
      lead="chroot 한 프로세스에게는 새 루트 안쪽만 파일시스템 전체로 보입니다.")

# 바깥 고리: 호스트 파일시스템
OX, OY, OW, OH = 36, 108, 912, 296
d.box(OX, OY, OW, OH, PAPER2, "rgba(191,192,192,0.45)", 1.0, 8)
inner_label(OX + 24, OY + 28, "호스트 파일시스템 / · chroot 전에 보이는 범위")

# 왼쪽 열: new_root/ 와 호스트의 나머지
LX, LW = 60, 208
d.tone(LX, 156, LW, 104, BAD, 6, "14", 1.1)
d.t(LX + LW / 2, 156 + 30, "new_root/", 14, BAD, MONO, "middle", 600)
fit("비어 있음 → /bin/bash 없음", 12, LW - 16)
d.t(LX + LW / 2, 156 + 54, "비어 있음 → /bin/bash 없음", 12, MUTED, KR, "middle")
d.t(LX + LW / 2, 156 + 78, "sudo chroot new_root", 12, INFO, MONO, "middle")

d.o.append(f'<rect x="{LX}" y="284" width="{LW}" height="96" rx="6" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 4"/>')
d.t(LX + LW / 2, 284 + 40, "호스트의 나머지", 13, MUTED, KR, "middle", 600)
d.t(LX + LW / 2, 284 + 64, "chroot 뒤에는 닿지 않음", 12, MUTED, KR, "middle")

# 안쪽 고리(focal): alpine/
AX, AY, AW, AH = 396, 148, 528, 232
d.tone(AX, AY, AW, AH, ACC, 8, "14", 1.4)
inner_label(AX + 24, AY + 28, "alpine/ · chroot 뒤 프로세스에게는 이곳이 /", ACC)

IW, IH, IY = 232, 84, 196
for k, (name, sub, mono_sub) in enumerate((("/bin", "alpine/bin 이 /bin 으로 보임", False),
                                           ("/proc", "mount -t proc proc /proc", True))):
    x = AX + 32 + k * (IW + 24)
    d.box(x, IY, IW, IH)
    fit(sub, 12, IW - 16)
    d.t(x + IW / 2, IY + 34, name, 14, INK, MONO, "middle", 600)
    d.t(x + IW / 2, IY + 60, sub, 12, INFO if mono_sub else MUTED, MONO if mono_sub else KR, "middle")

d.t(AX + 32, AY + 156, "PATH 에 /bin 포함 → ls 만 쳐도 실행", 12, MUTED, KR, "start")
d.t(AX + 32, AY + 188, "sudo chroot alpine ls", 12, INFO, MONO, "start")

# 막힌 길: alpine/ 에서 호스트의 나머지로 가는 점선과 차단 막대
ay = 284 + 48
d.arrow([(AX - 4, ay), (320, ay)], BAD, "bad", 1.4, "5 4")
d.line(312, ay - 14, 312, ay + 14, BAD, 3)
d.chip(332, ay - 28, "올라갈 길 없음", BAD, 11, 7)

d.legend(436, [("chroot 뒤 보이는 범위", ACC), ("실행 실패", BAD), ("명령", INFO)])
d.save(str(ASSETS / "04-01.chroot-subset.svg"))
print("ok 04-01 chroot-subset")
