# 01-01 §3 — "리눅스" 라고 말할 때 무엇을 가리키는가.
# 원문("Linux Distributions"): 이 책은 syscall 과 디바이스 드라이버의 집합을 가리킬 때만
#       "Linux kernel" 또는 "kernel" 이라 쓴다. 배포판은 "a concrete bundling of kernel and related
#       components, including package management, file system layout, init system, and a shell,
#       preselected for you" 다. 직접 말아 쓸 수도 있고(Arch Linux), 전통 배포판은 6장, 모던 배포판은 9장이다.
# 타입 스펙: type-nested — 포함 관계로 드러나는 경계. 바깥 링이 배포판, 안이 묶인 것 다섯,
#           그중 커널만 다시 두 겹으로 열어 "커널이라는 말의 범위" 를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING MODERN LINUX · 01-01 §3",
      "배포판이 묶어 주는 것과 커널이라는 말의 범위",
      "원서가 쓰는 어휘를 포함 관계로 편 것. 바깥 링이 배포판이고 안에 묶인 다섯 가운데 "
      "커널만 다시 열어, 이 책이 커널이라 부르는 범위가 시스템 콜과 디바이스 드라이버임을 보인다.",
      "셸도 패키지 관리자도 커널이 아니라 배포판이 골라 준 것입니다")

RX, RY, RW, RH = 28, 132, 800, 248
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
_lbl = "배포판(distro) — 미리 골라 묶어 준 한 벌"
_w = sum(12 if "가" <= c <= "힣" else 7 for c in _lbl) + 16
d.o.append(f'<rect x="{RX + 16}" y="{RY - 8}" width="{_w}" height="16" fill="{PAPER}"/>')
d.t(RX + 24, RY + 4, _lbl, 12, INFO, KR, "start", 600)

# 커널 — focal. 안에 두 겹을 더 연다.
KX, KY, KW, KH = 56, 168, 316, 180
d.o.append(f'<rect x="{KX}" y="{KY}" width="{KW}" height="{KH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(KX + KW / 2, KY + 30, "커널", 16, ACC, KR, "middle", 600)
d.t(KX + KW / 2, KY + 50, "이 책이 커널이라 부르는 범위", 12, MUTED, KR)
for i, (name, sub) in enumerate((("시스템 콜", "프로그램이 부르는 API"),
                                 ("디바이스 드라이버", "하드웨어를 다루는 코드"))):
    iy = KY + 68 + i * 56
    d.box(KX + 20, iy, KW - 40, 48, PAPER2, ACC, 1.0, 6)
    d.t(KX + KW / 2, iy + 21, name, 13, INK, KR, "middle", 600)
    d.t(KX + KW / 2, iy + 38, sub, 12, MUTED, KR)

# 배포판이 함께 묶는 나머지 넷
rest = [("패키지 관리", "무엇을 어떻게 설치하나"),
        ("파일시스템 레이아웃", "무엇이 어느 경로에 놓이나"),
        ("init 시스템", "부팅 뒤 무엇이 먼저 뜨나"),
        ("셸", "사람이 치는 명령을 받는 것")]
BW, BH = 200, 84
for i, (name, sub) in enumerate(rest):
    x = 396 + (i % 2) * (BW + 16)
    y = 168 + (i // 2) * 96
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, y + 34, name, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 56, sub, 12, MUTED, KR)

d.t(RX, 412, "직접 말아 쓸 수도 있습니다. 원서는 그 길을 택할 사람에게 Arch Linux 를 권합니다.",
    12, MUTED, KR, "start")
d.t(RX, 434, "전통 배포판(Ubuntu · RHEL · CentOS)은 원서 6장이, 모던 배포판(Bottlerocket · Flatcar)은 9장이 다룹니다.",
    12, SOFT, KR, "start")

d.legend(456, [("배포판이 묶는 경계", INFO), ("커널이라 부르는 범위", ACC)])
d.save("01-01.distro-bundle.svg")
print("ok 01-01.distro-bundle")
