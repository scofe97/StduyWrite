# 06-01 학습 목표 뒤 전체 지도 — 6장 앞 절반의 절 아홉을 읽는 순서로 잇는다.
# 원문 6장 서두: "We discuss how Linux starts up and brings all the services we depend on into being.
#       This is also known as the boot process. We will focus on init systems, specifically on the
#       de-facto standard, the systemd ecosystem. We then move on to package management, where we first
#       review the application supply chain in general terms ... We discuss package management in
#       traditional Linux distros, from Red Hat to Debian-based systems, and also have a peek at
#       programming language–specific package managers such as Python or Rust."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 절 제목 · 그 절이 다루는 실제 대상)이 반복되고
#           읽는 순서가 화살표로 흐른다. 장 전체 지도라 실제 구조도로 바꾸지 않고, 핵심 요약의 두 갈래
#           (띄우는 일 · 가져오는 일)를 존으로 나누고 칸의 둘째 줄을 각 절 도식이 그린 실제 대상
#           (UEFI · GRUB 2 · /boot · systemd[1] · /run/systemd/system · greeter.sh[21071] · amzn2-core ·
#           yum · apt)과 같은 이름으로 맞췄다.
# 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다. 절 제목은 본문 H2 를 줄였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 580
d = D(W, H, "LEARNING MODERN LINUX · 06-01",
      "먼저 켜지는 것 하나가 나머지 전부를 켠다",
      "6장 앞 절반의 절 아홉을 읽는 순서로 이은 지도. 1~6절은 앱을 띄우는 일로 펌웨어 · GRUB 2 · "
      "/boot 의 커널 · systemd[1] · /run/systemd/system 의 단위 파일 · greeter 타이머를 다루고, "
      "7~9절은 앱을 가져오는 일로 저장소 · yum · apt · 언어별 관리자를 다룬다.",
      "3절이 이 노트의 제목이 가리키는 자리 — PID 1")


def zone(x, y, w, h, label, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{INK}05" '
               f'stroke="{c}" stroke-width="1" stroke-dasharray="5 4"/>')
    d.t(x + w - 16, y + 22, label, 12, c, KR, "end", 600)


CW, CH, GX, X0 = 280, 84, 16, 44
ROWY = [140, 252, 408]
cards = [
    ("§1", "이름부터 가르는 여덟", "프로그램 · 프로세스 · 데몬 · 패키지", KR),
    ("§2", "부팅 다섯 단계", "UEFI → GRUB 2 → /boot → PID 1", MONO),
    ("§3", "PID 1 자리의 주인", "SysV init → systemd[1]", MONO),
    ("§4", "systemd 단위", "/lib · /etc · /run 의 단위 파일", KR),
    ("§5", "손으로 만지는 도구", "systemctl · journalctl", MONO),
    ("§6", "greeter 를 한 시간마다", "greeter.timer → greeter.sh", MONO),
    ("§7", "apt install 뒤의 공급망", "관리자 → 저장소 → yum · apt", KR),
    ("§8", "두 계보 RPM 과 deb", "yum install · apt install", MONO),
    ("§9", "언어마다 따로", "maven · pip · cargo", MONO),
]


def pos(i):
    return X0 + (i % 3) * (CW + GX), ROWY[i // 3]


zone(24, 104, 912, 248, "앱을 띄우는 일 — 무엇을 켤 것인가", INFO)
zone(24, 372, 912, 136, "앱을 가져오는 일 — 어디서 받아 올 것인가", OK)

# 읽는 순서 — 글자보다 먼저
for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = (y1 + CH + y2) / 2
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, sub, fam) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 2)
    c = INFO if i < 6 else OK
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, c, 1.0, 8)
    d.t(x + 16, y + 24, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 48, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 70, sub, 12, MUTED, fam, "start")

d.legend(532, [("띄우는 일", INFO), ("가져오는 일", OK), ("PID 1 을 누가 차지하는가", ACC)])
d.save("06-01.chapter-overview.svg")
print("ok 06-01.chapter-overview")
