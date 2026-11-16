# 06-01 §8 — 두 계보의 도구 층(배포판 · 고수준 · 저수준 · 파일 형식)과, 같은 세 동작의 실제 명령 · 출력.
# 원문("RPM Package Manager"): ".rpm file format is used in Linux Standard Base and can contain binary or
#       source files. The packages can be cryptographically verified and support delta updates via patch
#       files." 쓰는 관리자 — yum(Amazon Linux, CentOS, Fedora, RHEL), DNF(CentOS, Fedora, RHEL),
#       Zypper(openSUSE, SUSE Linux Enterprise).
# 원문("Debian deb"): "deb packages and the .deb file format originate from the Debian distro. The deb
#       packages can also contain binary or source files. Multiple package managers use deb, including
#       low-level, no-dependency-management ones such as dpkg, and high-level ones such as apt-get, apt,
#       and aptitude."
#  실제 값 — 본문 §8 출력: yum search golang(golang-bin.x86_64 · golang-docs.noarch),
#       yum install golang("Install 1 Package (+101 Dependent packages)", 183 M · 624 M),
#       yum info golang(Version 1.15.14 · From repo amzn2-core), apt search curl
#       ("curl/focal-updates,focal-security 7.68.0-1ubuntu2.6 amd64", "curlftpfs/focal 0.9.2-9build1"),
#       apt install curl("32 newly installed", 5447 kB · 16.7 MB), apt show curl
#       (Version 7.68.0-1ubuntu2.6 · Installed-Size 411 kB). 자동 승인 플래그 -y 는 양쪽 같다.
# 타입 스펙: type-swimlane — 레인이 계보, 세로 구획이 동작(검색 · 설치 · 확인). 레인 머리에는 그 계보의
#           실제 도구 층을 쌓았다. accent 는 두 레인에서 똑같은 -y 자리.
# 축약: 배포판은 대표만 적었다. RPM 쪽 저수준 도구는 원문이 이름을 들지 않아 빈 점선 칸으로 두었다.
#       칸 안의 출력은 각 명령 출력에서 값을 나르는 줄만 골랐다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 556
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §8",
      "도구 층은 다르게 쌓였고, 세 동작은 이름만 다르다",
      "RPM 계보는 .rpm 형식 위에 yum · DNF · Zypper 가, deb 계보는 .deb 형식 위에 저수준 dpkg 와 "
      "고수준 apt · apt-get · aptitude 가 선다. 검색은 yum search golang 과 apt search curl, "
      "설치는 yum install(1 + 의존 101 개, 183 M)과 apt install(32 개, 5447 kB), 확인은 "
      "yum info(1.15.14, amzn2-core)와 apt show(7.68.0-1ubuntu2.6)로 짝을 이루고 -y 는 양쪽 같다.",
      "저수준 dpkg 는 의존성을 풀지 않는다 — 푸는 쪽이 고수준이다")

X0, LW, CW, G = 24, 252, 212, 8
HY, RY, RH = 120, 136, 168
cx0 = X0 + LW + G
for i, c in enumerate(["검색", "설치", "확인"]):
    d.t(cx0 + i * (CW + G) + CW / 2, HY, c, 13, MUTED, KR, "middle", 600)
d.line(X0, HY + 8, W - 24, HY + 8, RULE, 1)

lanes = [
    ("RPM 계보", INFO,
     [("배포판", "Fedora · RHEL · openSUSE", False), ("고수준", "yum · DNF · Zypper", False),
      ("저수준", "원문에 이름 없음", True), ("형식", ".rpm · 서명 검증", False)],
     [("yum search golang", ["golang-bin.x86_64", "golang-docs.noarch"]),
      ("yum install golang", ["Install 1 Package", "(+101 Dependent packages)", "183 M → 624 M"]),
      ("yum info golang", ["Version   : 1.15.14", "From repo : amzn2-core"])]),
    ("deb 계보", OK,
     [("배포판", "Debian · Ubuntu", False), ("고수준", "apt · apt-get · aptitude", False),
      ("저수준", "dpkg — 의존성 안 풂", False), ("형식", ".deb", False)],
     [("apt search curl", ["curl/focal-updates", "7.68.0-1ubuntu2.6 amd64", "curlftpfs/focal …"]),
      ("apt install curl", ["32 newly installed", "5447 kB → 16.7 MB"]),
      ("apt show curl", ["Version: 7.68.0-1ubuntu2.6", "Installed-Size: 411 kB"])]),
]
for r, (name, col, stack, cells) in enumerate(lanes):
    y = RY + r * (RH + 12)
    d.box(X0, y, LW, RH, PAPER2, col, 1.2, 8)
    d.t(X0 + 14, y + 24, name, 14, col, KR, "start", 600)
    for k, (lv, val, dashed) in enumerate(stack):
        by = y + 36 + k * 32
        if dashed:
            d.o.append(f'<rect x="{X0 + 6}" y="{by}" width="{LW - 12}" height="26" rx="4" fill="none" '
                       f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
        else:
            d.o.append(f'<rect x="{X0 + 6}" y="{by}" width="{LW - 12}" height="26" rx="4" '
                       f'fill="{col}12" stroke="{col}" stroke-width="0.8"/>')
        d.t(X0 + 16, by + 18, lv, 12, SOFT, KR, "start")
        d.t(X0 + 58, by + 18, val, 12, SOFT if dashed else INK,
            KR if any('가' <= ch <= '힣' for ch in val) and not val.startswith(".") else MONO, "start")
    for i, (cmd, outs) in enumerate(cells):
        x = cx0 + i * (CW + G)
        d.box(x, y, CW, RH, PAPER, RULE, 1.0, 6)
        d.o.append(f'<rect x="{x + 10}" y="{y + 12}" width="{CW - 20}" height="28" rx="5" '
                   f'fill="{col}12" stroke="{col}" stroke-width="1.1"/>')
        d.t(x + 16, y + 31, cmd, 12, col, MONO, "start", 600)
        for j, o in enumerate(outs):
            d.t(x + 14, y + 64 + j * 22, o, 12, MUTED, MONO, "start")
        if i == 1:
            d.o.append(f'<rect x="{x + CW - 50}" y="{y + RH - 34}" width="36" height="22" rx="4" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + CW - 32, y + RH - 18, "-y", 13, ACC, MONO, "middle", 600)

d.t(X0, 504, "배포판은 대표만 · 칸 안 출력은 값을 나르는 줄만 · -y 는 스크립트에서 대화형 확인을 건너뛰는 자리",
    11, SOFT, KR, "start")
d.legend(516, [("RPM 계보", INFO), ("deb 계보", OK), ("두 계보가 같은 자리", ACC)])
d.save("06-01.rpm-vs-deb.svg")
print("ok 06-01.rpm-vs-deb")
