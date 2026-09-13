# 07-01 §1·§4 — 유저와 커널이 한 주소 공간을 어떤 비율로 나눠 갖는가.
# 본문이 요구한 형태: "같은 box 안에 User:Kernel 비율로 나눠 둔다" + "가운데는 거대한 non-canonical hole".
# 타입 스펙: type-layers — 주소가 높은 쪽이 위. 32비트와 x86_64 를 같은 눈금으로 나란히 세운다.
#           축약: 두 아키텍처를 두 열로 병치해 같은 층 이름이 서로 다른 크기를 갖는 것을 보인다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 552
AX, AW = 136, 384
BX, BW = 560, 384
Y0 = 152

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-01 §1·§4",
       "한 주소 공간을 둘이 나눠 씁니다",
       "VM split — 유저 VAS 와 커널 VAS 는 별도 공간이 아니라 같은 주소 공간을 User:Kernel 비율로 나눠 가진다. 32비트는 보통 3:1 GB, x86_64 는 48비트 주소로 128TB : 128TB 이고 그 사이는 쓸 수 없는 non-canonical hole 이다.",
       "커널 VAS 가 같은 box 안에 있어야 시스템 콜이 커널 코드를 부를 수 있습니다")

d.t(AX, 124, "AArch32 · x86-32 — 3:1 GB", 13, INK, KR, "start", 600)
d.t(AX + AW, 124, "주소 32비트", 13, SOFT, KR, "end")
d.t(BX, 124, "x86_64 — 128TB : 128TB", 13, INK, KR, "start", 600)
d.t(BX + BW, 124, "주소 48비트", 13, SOFT, KR, "end")

def band(x, w, y, h, name, size, lo, hi, c, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, h, c, 6, "12", 1.1)
    d.t(x + 16, y + 26, name, 13, ACC if focal else c, KR, "start", 600)
    d.t(x + 16, y + 46, size, 13, MUTED, KR, "start")
    d.t(x + w - 16, y + 26, hi, 12, MUTED, MONO, "end")
    d.t(x + w - 16, y + 46, lo, 12, MUTED, MONO, "end")

# 32비트 3:1 — 커널 1GB 위, 유저 3GB 아래. 높이 비율이 곧 크기 비율이다.
band(AX, AW, Y0, 64, "커널 VAS", "1GB — 모든 프로세스가 공유", "0xc000_0000", "0xffff_ffff", INFO)
band(AX, AW, Y0 + 64, 160, "유저 VAS", "3GB — 프로세스마다 따로", "0x0000_0000", "0xbfff_ffff", OK)

# x86_64 48비트 — 위아래 canonical 절반이 같고 가운데가 비어 있다.
band(BX, BW, Y0, 64, "커널 VAS", "128TB — 상위 절반", "0xffff_8000_0000_0000", "0xffff_ffff_ffff_ffff", INFO)
band(BX, BW, Y0 + 64, 96, "non-canonical hole", "쓸 수 없는 sparse 구간", "0x0000_8000_0000_0000", "0xffff_7fff_ffff_ffff", WARN)
band(BX, BW, Y0 + 160, 64, "유저 VAS", "128TB — 하위 절반", "0x0000_0000_0000_0000", "0x0000_7fff_ffff_ffff", OK)

# PAGE_OFFSET — 커널 VAS 가 시작하는 경계. 이 편의 논점이라 focal 은 여기 하나.
BY = Y0 + 64
d.line(24, BY, AX - 8, BY, ACC, 1.4, "4 4")
d.t(24, BY - 10, "PAGE_OFFSET", 13, ACC, MONO, "start", 600)
d.t(24, BY + 20, "커널 VAS 가", 13, ACC, KR, "start")
d.t(24, BY + 40, "시작하는 주소", 13, ACC, KR, "start")
d.line(AX + AW + 8, BY, BX - 8, BY, ACC, 1.2, "4 4")

BOT = Y0 + 224
d.t(24, BOT + 34, "32비트에서 3:1 split 이면 PAGE_OFFSET 은 0xc0000000 입니다. 빌드 시 CONFIG_VMSPLIT_* 로 바꿀 수 있습니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 58, "64비트에서는 상위 16비트가 커널은 1, 유저는 0 이라 주소만 보고 어느 쪽인지 가릅니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 82, "48비트면 16EB 중 실제로 쓰는 곳은 0.002% 뿐이라, VAS 는 대부분 비어 있습니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("커널 VAS", INFO), ("유저 VAS", OK), ("쓸 수 없는 구간", WARN), ("이 절의 논점", ACC)])
d.save("07-01.vm-split-layout.svg")
print("ok 07-01.vm-split-layout")
