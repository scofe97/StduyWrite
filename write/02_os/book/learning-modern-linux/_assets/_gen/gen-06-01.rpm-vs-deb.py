# 06-01 §8 — 같은 세 동작을 두 계보가 다른 이름으로 부른다.
# 원문("RPM Package Manager"): ".rpm file format is used in Linux Standard Base and can contain binary or
#       source files. The packages can be cryptographically verified and support delta updates via patch
#       files." 쓰는 관리자 — yum(Amazon Linux, CentOS, Fedora, RHEL), DNF(CentOS, Fedora, RHEL),
#       Zypper(openSUSE, SUSE Linux Enterprise).
# 원문("Debian deb"): "deb packages and the .deb file format originate from the Debian distro. The deb
#       packages can also contain binary or source files. Multiple package managers use deb, including
#       low-level, no-dependency-management ones such as dpkg, and high-level ones such as apt-get, apt,
#       and aptitude."
#   실측 출력 — yum: "Install 1 Package (+101 Dependent packages)" / "Total download size: 183 M".
#              apt: "0 upgraded, 32 newly installed, 0 to remove and 2 not upgraded." /
#                   "Need to get 5447 kB of archives."
#   저자 노트 — 스크립트에서는 `yum install golang -y`, `apt install curl -y` 로 대화형 확인을 건너뛴다.
# 타입 스펙: type-swimlane — 같은 절차를 두 주체가 각자 자기 레인에서 수행할 때. 세로 구획이 동작이고
#           가로 레인이 계보다. accent 는 두 레인에서 이름만 다르고 뜻이 같은 자리.
#           축약: 각 계보의 관리자 목록은 대표만 레인 머리에 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §8",
      "이름만 다르고 하는 일은 같다",
      "두 계보를 나란히 놓으면 검색과 설치와 확인이라는 세 동작이 하나씩 짝을 이룬다. "
      "자동 승인 플래그까지 -y 로 같다.",
      "저수준 도구는 의존성을 해결하지 않습니다")

LW, CW, GAP, X0 = 176, 216, 8, 24
HY, RY, RH = 168, 196, 132
cols = ["검색", "설치", "확인"]
for i, c in enumerate(cols):
    d.t(X0 + LW + i * (CW + GAP) + CW / 2, HY, c, 13, MUTED, KR, "middle", 600)
d.line(X0, HY + 12, X0 + LW + 3 * (CW + GAP) - GAP, HY + 12, RULE, 1)

lanes = [
    ("RPM 계보", "yum · DNF · Zypper", "Red Hat · Fedora", INFO,
     [("yum search golang", "golang-bin.x86_64"),
      ("yum install golang", "1 package + 101 deps · 183 M"),
      ("yum info golang", "Version 1.15.14 · amzn2-core")]),
    ("deb 계보", "apt · apt-get · dpkg", "Debian · Ubuntu", OK,
     [("apt search curl", "curl/focal-updates"),
      ("apt install curl", "32 newly installed · 5447 kB"),
      ("apt show curl", "Version 7.68.0-1ubuntu2.6")]),
]
for r, (name, tools, distros, col, cells) in enumerate(lanes):
    y = RY + r * (RH + 12)
    d.box(X0, y, LW, RH, PAPER2, col, 1.2, 8)
    d.t(X0 + 16, y + 32, name, 15, col, KR, "start", 600)
    d.t(X0 + 16, y + 58, tools, 11.5, INK, MONO, "start")
    d.t(X0 + 16, y + 80, distros, 11.5, MUTED, KR, "start")
    for i, (cmd, out) in enumerate(cells):
        x = X0 + LW + i * (CW + GAP)
        d.box(x, y, CW, RH, PAPER, RULE, 1.0, 6)
        d.o.append(f'<rect x="{x + 12}" y="{y + 22}" width="{CW - 24}" height="28" rx="5" '
                   f'fill="{col}12" stroke="{col}" stroke-width="1.1"/>')
        d.t(x + CW / 2, y + 41, cmd, 11.5, col, MONO, "middle", 600)
        d.t(x + CW / 2, y + 74, out, 11, MUTED, MONO)
        if i == 1:
            d.t(x + CW / 2, y + 104, "-y 로 확인을 건너뛴다", 11, ACC, KR)

AY = 500
d.tone(X0, AY, LW + 3 * (CW + GAP) - GAP, 46, ACC)
d.t(X0 + 20, AY + 28,
    "고수준과 저수준을 가르는 기준은 의존성입니다. dpkg 는 deb 를 다루지만 의존성을 해결하지 않습니다.",
    12, MUTED, KR, "start")

d.legend(572, [("RPM 계보", INFO), ("deb 계보", OK), ("두 계보가 같은 자리", ACC)])
d.save("06-01.rpm-vs-deb.svg")
print("ok 06-01.rpm-vs-deb")
