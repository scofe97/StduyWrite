# 06-01 §7 — 소프트웨어가 내 기계에 닿기까지: 관리자가 발행하고, 저장소가 패키지와 메타데이터를 쌓아
#           두고, 대상 시스템의 패키지 관리자가 의존성까지 끌어온다.
# 원문("Linux Application Supply Chains"):
#   Software maintainers: "These include individual developers, open source projects, and companies, such
#       as independent software vendors (ISVs), that produce software artifacts and publish them, for
#       example, as packages to a repository (repo)."
#   Repository: "This lists the package that contains all or part of an app together with metadata. The
#       package usually captures the dependencies of an app. ... Keeping these dependencies up to date is
#       hard."
#   Tooling (a package manager): "On the target-system side, this can look up packages in the repository
#       and install, update, and remove apps as instructed by the human user."
#  실제 값 — §8 출력: yum search golang(golang-bin.x86_64 · golang-docs.noarch ·
#       golang-googlecode-net-devel.noarch), yum info golang(Version 1.15.14, Arch x86_64,
#       From repo amzn2-core), yum install golang("Install 1 Package (+101 Dependent packages)",
#       "Total download size: 183 M", "Installed size: 624 M"), apt search curl
#       ("curl/focal-updates,focal-security 7.68.0-1ubuntu2.6 amd64"), apt show curl
#       ("Depends: libc6 (>= 2.17), libcurl4 (= 7.68.0-1ubuntu2.6), zlib1g (>= 1:1.1"),
#       apt install curl("32 newly installed", "Need to get 5447 kB", "16.7 MB of additional disk space").
# 타입 스펙: type-architecture — 세 행위자를 존 셋으로 두고 발행 · 조회 흐름을 화살표로 싣는다.
#           accent 는 golang 한 개에 딸려 오는 의존 패키지 101 개, 곧 저자가 어렵다고 못 박은 자리.
# 축약: 대상 시스템의 칸 하나가 패키지 하나다(golang 102 칸, curl 32 칸). 의존 패키지가 어느 저장소에서
#       오는지는 출력에 없어 저장소 쪽에는 대표 패키지만 적었다. 서명 · 검증 경로는 그리지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 552
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §7",
      "패키지 하나를 부르면 의존 패키지가 줄줄이 딸려 온다",
      "소프트웨어 관리자(개별 개발자 · 오픈소스 프로젝트 · 회사)가 패키지를 저장소에 발행한다. "
      "저장소 amzn2-core 에는 golang 1.15.14 가, focal-updates 에는 curl 7.68.0-1ubuntu2.6 이 "
      "의존성 메타데이터(Depends: libc6 · libcurl4 · zlib1g)와 함께 있다. 대상 시스템의 yum 은 "
      "golang 1 개에 의존 패키지 101 개를 더해 183 M 를 받아 624 M 를 쓰고, apt 는 curl 과 함께 "
      "32 개를 새로 깔며 5447 kB 를 받는다.",
      "의존성을 최신으로 유지하는 일이 어려운 이유가 칸 수로 보인다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{INK}05" '
               f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 4"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, KR, "start", 600)


ZY, ZH = 104, 352
zone(24, ZY, 220, ZH, "소프트웨어 관리자")
zone(284, ZY, 328, ZH, "저장소")
zone(652, ZY, 284, ZH, "대상 시스템")

# 흐름 — 글자보다 먼저
for i in range(3):
    d.line(228, 174 + i * 56, 264, 174 + i * 56, INFO, 1.4)
d.line(264, 174, 264, 372, INFO, 1.4)
d.arrow([(264, 206), (298, 206)], INFO, "info", 1.4)
d.arrow([(264, 372), (298, 372)], INFO, "info", 1.4)
d.arrow([(596, 206), (666, 206)], WARN, "warn", 1.4)
d.t(631, 196, "조회", 12, WARN, KR, "middle", 600)
d.arrow([(596, 372), (666, 372)], WARN, "warn", 1.4)
d.t(631, 362, "조회", 12, WARN, KR, "middle", 600)

# 관리자
for i, who in enumerate(["개별 개발자", "오픈소스 프로젝트", "회사 · ISV"]):
    y = 152 + i * 56
    d.box(40, y, 188, 44, PAPER2, INFO, 1.1, 6)
    d.t(56, y + 27, who, 13, INK, KR, "start", 600)
d.t(40, 340, "산출물을 패키지로", 12, INFO, KR, "start", 600)
d.t(40, 360, "저장소에 발행", 12, INFO, KR, "start", 600)


def repo(y, h, name, lines):
    d.box(300, y, 296, h, PAPER2, OK, 1.2, 8)
    d.t(316, y + 24, name, 13, OK, MONO, "start", 600)
    d.line(308, y + 34, 588, y + 34, RULE, 1)
    for i, (txt, c) in enumerate(lines):
        d.t(316, y + 54 + i * 20, txt, 12, c, MONO if c is not SOFT else KR, "start")


repo(140, 140, "amzn2-core",
     [("golang 1.15.14 · x86_64", INK), ("golang-bin · golang-docs", MUTED),
      ("golang-googlecode-net-devel", MUTED), ("패키지 + 메타데이터", SOFT)])
repo(304, 140, "focal-updates · focal-security",
     [("curl 7.68.0-1ubuntu2.6 · amd64", INK), ("Depends: libc6 (>= 2.17)", MUTED),
      ("libcurl4 (= 7.68.0-1ubuntu2.6)", MUTED), ("zlib1g (>= 1:1.1 …", MUTED)])


def grid(x, y, n, c_first, c_rest, cols=18, cell=10, gap=2):
    for i in range(n):
        cx, cy = x + (i % cols) * (cell + gap), y + (i // cols) * (cell + gap)
        c = c_first if i == 0 else c_rest
        d.o.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="2" '
                   f'fill="{c}44" stroke="{c}" stroke-width="0.8"/>')
    return y + ((n - 1) // cols + 1) * (cell + gap)


# 대상 시스템 — yum
d.box(668, 140, 252, 164, PAPER2, WARN, 1.2, 8)
d.t(682, 164, "yum install golang", 13, WARN, MONO, "start", 600)
gy = grid(682, 178, 102, WARN, ACC)
d.t(682, gy + 18, "golang 1 + 의존 101", 12, ACC, KR, "start", 600)
d.t(682, gy + 38, "받기 183 M → 설치 624 M", 12, MUTED, KR, "start")

# 대상 시스템 — apt
d.box(668, 320, 252, 120, PAPER2, WARN, 1.2, 8)
d.t(682, 344, "apt install curl", 13, WARN, MONO, "start", 600)
gy = grid(682, 358, 32, WARN, MUTED)
d.t(682, gy + 18, "32 newly installed", 12, INK, MONO, "start")
d.t(682, gy + 38, "받기 5447 kB → 디스크 +16.7 MB", 12, MUTED, KR, "start")

d.t(24, 484, "대상 시스템의 칸 하나 = 패키지 하나 · 저장소 쪽 패키지는 대표만 · 서명 검증 경로 생략",
    11, SOFT, KR, "start")
d.legend(500, [("만드는 쪽", INFO), ("쌓아 두는 쪽", OK), ("날라 오는 쪽", WARN), ("딸려 오는 의존 패키지", ACC)])
d.save("06-01.supply-chain.svg")
print("ok 06-01.supply-chain")
