# 07-02 §1 — /proc/PID/maps 한 줄의 일곱 필드가 각각 무엇을 말하고, 언제 비는가.
# 본문이 요구한 형태: "각 줄은 7개 필드로 구성됩니다" + "inode 0 이면 anonymous — 파일/익명 구분의 빠른 방법".
# 타입 스펙: type-dp-security-matrix — 격자 문법을 필드 × 읽는 법 행렬로 쓴다. 행은 필드, 열은 읽는 축.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 1000, 632
LX, LW = 24, 152
C1, C1W = 184, 200
C2, C2W = 392, 320
C3, C3W = 720, 256
HY, RH, RS = 116, 40, 48

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-02 §1",
       "maps 한 줄을 일곱으로 가릅니다",
       "/proc/PID/maps 한 줄은 유저 VAS 의 매핑 하나다. 일곱 필드가 각각 무엇을 말하는지와, 익명 매핑일 때 어느 필드가 비는지를 나란히 둔다. inode 가 0 이면 파일이 아니라 익명 매핑이라는 것이 가장 빠른 판별법이다.",
       "샘플: 558822d66000-558822d6a000  r-xp  00002000  08:01  7340181  /usr/bin/cat")

ROWS = [
    ("start_uva", "558822d66000", "매핑이 시작하는 UVA", "그대로 있습니다", INFO),
    ("end_uva", "558822d6a000", "끝 UVA — 길이는 end - start", "그대로 있습니다", INFO),
    ("mode/mapping", "r-xp", "권한 rwx + p(private)/s(shared)", "그대로 있습니다", INFO),
    ("offset", "00002000", "파일 시작에서의 오프셋", "0 입니다", WARN),
    ("major:minor", "08:01", "이미지가 있는 블록 디바이스", "00:00 입니다", WARN),
    ("inode#", "7340181", "이미지 파일의 inode 번호", "0 입니다 — 익명의 표식", ACC),
    ("pathname", "/usr/bin/cat", "매핑된 파일의 경로", "빈칸입니다", WARN),
]

for x, w, lab in ((LX, LW, "필드"), (C1, C1W, "샘플 값"), (C2, C2W, "무엇을 말하나"), (C3, C3W, "익명 매핑이면")):
    d.box(x, HY, w, RH, PAPER2, RULE, 0.9)
    d.t(x + w / 2, HY + 25, lab, 13, SOFT, KR)

for i, (name, val, means, anon, c) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    focal = c is ACC
    if focal:
        d.tone(LX, y, LW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + LW / 2, y + 25, name, 12, ACC if focal else INK, MONO, "middle", 600)
    d.box(C1, y, C1W, RH, PAPER2, RULE, 0.9)
    d.t(C1 + C1W / 2, y + 25, val, 12, MUTED, MONO)
    d.box(C2, y, C2W, RH, PAPER2, RULE, 0.9)
    d.t(C2 + 16, y + 25, means, 13, INK, KR, "start")
    d.tone(C3, y, C3W, RH, ACC if focal else c, 6, "12" if focal else "14", 1.4 if focal else 1.1)
    d.t(C3 + 16, y + 25, anon, 13, ACC if focal else c, KR, "start")

BOT = HY + RH + 8 + len(ROWS) * RS
d.t(LX, BOT + 30, "모든 주소는 가상 주소이고, 그 프로세스의 페이징 테이블로 변환됩니다. 매핑은 전부 mmap() 이 만듭니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 54, "[vsyscall]·[vdso]·[vvar] 같은 특수 매핑도 보입니다 — 커널 모드 전환 없이 도는 시스템 콜 최적화입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("파일 매핑에서도 채워짐", INFO), ("파일 매핑일 때만 채워짐", WARN), ("익명 판별의 열쇠", ACC)])
d.save("07-02.maps-fields.svg")
print("ok 07-02.maps-fields")
