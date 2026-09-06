# 09-01 §3 — 컨테이너 중심 배포판 넷이 어디서 갈라져 나왔는가.
# 원문("Red Hat Enterprise Linux CoreOS"): "In 2013, a young start-up called CoreOS made CoreOS Linux
#       (later renamed Container Linux) available. Its main features included a dual-partition scheme
#       for system updates and the lack of a package manager. In other words, all apps would run as
#       containers natively. ... After Red Hat acquired CoreOS (the company), it announced the intention
#       to merge the CoreOS Linux with Red Hat's own Project Atomic (that had similar goals). This
#       merger led to Red Hat Enterprise Linux CoreOS (RHCOS), which is not meant to be used on its own
#       but in the context of the Red Hat Kubernetes distribution called OpenShift Container Platform."
# 원문("Flatcar Container Linux"): "a German startup called Kinvolk GmbH (now part of Microsoft)
#       announced that it would fork and continue to develop Container Linux under the new brand name
#       Flatcar Container Linux." · 자동 업그레이드는 Nebraska, 프로비저닝은 Ignition("also used by
#       RHCOS for that purpose") 이고 "there is no package manager; everything is running in containers".
# 원문("Bottlerocket"): AWS 가 만들고 Rust 로 쓰였으며 Amazon EKS·ECS 에 쓰인다. "instead of a package
#       manager, Bottlerocket uses an OCI image-based model for app upgrades and rollbacks" ·
#       "a (by and large) read-only, integrity-checked filesystem based on dm-verity" · control container.
# 원문("RancherOS"): "everything is a container managed by Docker" · "Sponsored by Rancher (now SUSE)" ·
#       "It runs two Docker instances: the system Docker, which runs as the first process, and the user
#       Docker, which is used to create application containers."
# 주의: 뿌리 칸의 "컨테이너 중심 배포판" 은 저자가 붙인 이름이 아니라 넷을 한 트리로 묶기 위한 이 노트의
#       묶음 이름이다. 저자의 정의(컨테이너 중심 · 불변성 · 자동 업그레이드)를 그 칸에 함께 적었다.
#       패키지 관리자 부재를 원문이 적은 대상은 CoreOS Linux · Flatcar · Bottlerocket 셋뿐이라 부제를
#       넷에서 셋으로 고쳤다. RHCOS 와 RancherOS 에는 그런 서술이 없다.
#       RHCOS 라벨도 원문이 "not meant to be used on its own but in the context of ... OpenShift" 라
#       적으므로 "만" 으로 굳히지 않는다.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 계보. Container Linux 에서 둘로 갈리는 분기가 논지라
#           timeline 이 아니라 tree 다. 직교 연결만 쓴다. accent 는 갈라지는 지점 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 664
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §3",
      "컨테이너 중심 배포판 넷 중 둘은 한 뿌리에서 갈렸다",
      "저자가 소개한 배포판 넷을 계보로 세운 것. 왼쪽 뿌리 이름은 저자의 정의를 옮긴 것이고, 가운데 "
      "갈림목에서 나온 둘이 지금도 나란히 쓰인다.",
      "패키지 관리자를 두지 않는다고 원문이 밝힌 것은 셋입니다")

RX, RW, RY, RH = 24, 188, 296, 104
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(RX + 16, RY + 26, "컨테이너 중심 배포판", 13, INK, KR, "start", 600)
d.t(RX + 16, RY + 46, "저자가 현대적이라 부르는 조건", 10.5, SOFT, KR, "start")
for k, line in enumerate(["컨테이너 중심", "불변성", "자동 업그레이드"]):
    d.t(RX + 16, RY + 64 + k * 17, f"· {line}", 11, MUTED, KR, "start")

MX, MW, MY, MH = 248, 216, 148, 104
d.tone(MX, MY, MW, MH, ACC, 8, "12", 1.4)
d.t(MX + 16, MY + 26, "CoreOS Linux", 13.5, ACC, KR, "start", 600)
d.t(MX + 16, MY + 46, "2013 · 스타트업 CoreOS 가 냈습니다", 10.5, ACC, KR, "start")
d.t(MX + 16, MY + 66, "뒤에 Container Linux 로 개명", 10.5, MUTED, KR, "start")
d.t(MX + 16, MY + 86, "이중 파티션 · 패키지 관리자 없음", 10.5, MUTED, KR, "start")

LX2, LW2, CH2 = 496, 360, 100
CARDS = [
    (108, "RHCOS", INFO, True, ["Red Hat 이 CoreOS 를 인수하고",
                                "Project Atomic 과 합쳐 나왔습니다",
                                "단독이 아니라 OpenShift 안에서 씁니다"]),
    (228, "Flatcar Container Linux", OK, True, ["Kinvolk GmbH — 지금은 Microsoft — 가 포크했습니다",
                                                "Nebraska 로 자동 업그레이드",
                                                "Ignition 으로 프로비저닝 — RHCOS 도 씁니다"]),
    (348, "Bottlerocket", WARN, False, ["AWS 가 Rust 로 만들었고 EKS·ECS 에 씁니다",
                                        "OCI 이미지로 업그레이드와 롤백을 합니다",
                                        "dm-verity 로 읽기 전용 무결성 검사"]),
    (468, "RancherOS", MUTED, False, ["Rancher — 지금은 SUSE — 가 후원합니다",
                                      "Docker 를 둘 돌립니다 — 시스템과 사용자",
                                      "발자국이 작아 임베디드와 엣지에 맞습니다"]),
]
for y, name, col, from_fork, lines in CARDS:
    d.box(LX2, y, LW2, CH2, PAPER2, col, 1.2, 8)
    d.t(LX2 + 16, y + 26, name, 13.5, col, KR, "start", 600)
    for k, line in enumerate(lines):
        d.t(LX2 + 16, y + 48 + k * 18, line, 10.5, MUTED, KR, "start")

BUS_R = (RX + RW + MX) / 2
d.line(BUS_R, MY + MH / 2, BUS_R, 518, MUTED, 1.2)
d.path(f"M {RX + RW} {RY + RH / 2} L {BUS_R} {RY + RH / 2}", MUTED, 1.2)
d.path(f"M {BUS_R} {MY + MH / 2} L {MX - 4} {MY + MH / 2}", MUTED, 1.2, m="ar")
for y in (398, 518):
    d.path(f"M {BUS_R} {y} L {LX2 - 4} {y}", MUTED, 1.2, m="ar")

BUS_F = (MX + MW + LX2) / 2
d.line(BUS_F, 158, BUS_F, 278, ACC, 1.2)
d.path(f"M {MX + MW} {MY + MH / 2} L {BUS_F} {MY + MH / 2}", ACC, 1.2)
for y in (158, 278):
    d.path(f"M {BUS_F} {y} L {LX2 - 4} {y}", ACC, 1.2, m="acc")

d.t(24, 442, "전통 배포판은 다섯 갈래입니다.", 12.5, INK, KR, "start", 600)
for k, line in enumerate(["Red Hat 계열 — RHEL · Fedora · CentOS/Rocky",
                          "Debian 계열 — Ubuntu · Mint · Kali 등",
                          "SUSE 계열 — openSUSE · Enterprise",
                          "Gentoo 와 Arch Linux"]):
    d.t(24, 464 + k * 20, line, 11, MUTED, KR, "start")

d.legend(596, [("갈림목", ACC), ("Red Hat 쪽", INFO), ("Microsoft 쪽", OK), ("AWS 쪽", WARN)])
d.save("09-01.distro-lineage.svg")
print("ok 09-01.distro-lineage")
