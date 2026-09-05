# 06-01 학습 목표 뒤 전체 지도 — 6장 앞 절반의 절 아홉을 읽는 순서로 잇는다.
# 원문 6장 서두: "We discuss how Linux starts up and brings all the services we depend on into being.
#       This is also known as the boot process. We will focus on init systems, specifically on the
#       de-facto standard, the systemd ecosystem. We then move on to package management, where we first
#       review the application supply chain in general terms ... We discuss package management in
#       traditional Linux distros, from Red Hat to Debian-based systems, and also have a peek at
#       programming language–specific package managers such as Python or Rust."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 06-01",
      "먼저 켜지는 것 하나가 나머지 전부를 켠다",
      "6장 앞 절반의 절 아홉을 읽는 순서로 이은 지도. 1~6절이 앱을 띄우는 일이고 "
      "7~9절이 앱을 가져오는 일이다.",
      "3절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "이름부터 가르는 여덟", "프로그램 · 프로세스 · 데몬 · 앱"),
    ("§2", "부팅은 다섯 단계다", "제어권이 세 번 넘어간다"),
    ("§3", "PID 1 자리의 주인", "SysV init 에서 systemd 로"),
    ("§4", "단위로 말한다", "종류 넷과 파일 세 자리"),
    ("§5", "손으로 만지는 도구", "systemctl · journalctl"),
    ("§6", "greeter 를 한 시간마다", "단위 파일 둘이 로그 한 줄로"),
    ("§7", "apt install 뒤의 셋", "관리자 · 저장소 · 도구"),
    ("§8", "두 계보", "RPM 과 deb 의 같은 세 동작"),
    ("§9", "언어마다 따로", "maven 이 서는 자리"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("PID 1 을 누가 차지하는가", ACC)])
d.save("06-01.chapter-overview.svg")
print("ok 06-01.chapter-overview")
