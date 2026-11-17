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
# 주의: 예전 판은 "컨테이너 중심 배포판" 이라는 묶음 칸을 뿌리로 두었는데, 그 칸은 조상이 아니라 분류라서
#       뿌리 자리를 실제로 만든 곳(CoreOS · AWS · Rancher)으로 바꿨다. Rust · EKS·ECS · 롤백 · 전통
#       배포판 갈래는 본문에 없어 뺐다.
#       패키지 관리자 부재를 원문이 적은 대상은 CoreOS Linux · Flatcar · Bottlerocket 셋뿐이라 부제를
#       넷에서 셋으로 고쳤다. RHCOS 와 RancherOS 에는 그런 서술이 없다.
#       RHCOS 라벨도 원문이 "not meant to be used on its own but in the context of ... OpenShift" 라
#       적으므로 "만" 으로 굳히지 않는다.
# 타입 스펙: type-tree — 만든 곳에서 배포판으로 내려가는 실제 계보. CoreOS Linux(Container Linux)에서
#           RHCOS 와 Flatcar 로 갈리는 분기가 논지이고, Bottlerocket 과 RancherOS 는 따로 선 뿌리다.
#           직교 연결만 쓴다. accent 는 갈림목 하나.
# 근거: 본문 §4 표(누가 · 앱을 올리는 방식 · 특징)와 계보 문단(2013 · 개명 · 이중 파티션 ·
#       패키지 관리자 부재 · etcd · Red Hat 인수 + Project Atomic · Kinvolk GmbH 포크), 패키지 관리자
#       부재를 책이 명시한 셋(CoreOS Linux · Flatcar · Bottlerocket).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 652
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §4",
      "컨테이너 중심 배포판 넷 중 둘은 한 뿌리에서 갈렸다",
      "만든 곳에서 배포판으로 내려가는 계보. 스타트업 CoreOS 가 2013년 내놓은 CoreOS Linux 는 Container "
      "Linux 로 이름을 바꿨고, Red Hat 이 인수해 Project Atomic 과 합친 것이 RHCOS, Kinvolk GmbH 가 포크한 "
      "것이 Flatcar 다. Bottlerocket 은 AWS, RancherOS 는 Rancher 가 따로 만들었다. 패키지 관리자가 없다고 "
      "책이 명시한 것은 CoreOS Linux, Flatcar, Bottlerocket 셋이다.",
      "갈림목은 Container Linux 하나, 거기서 RHCOS 와 Flatcar 가 나옵니다")

AX0, AX1 = 24, 164            # 만든 곳
BX0, BX1 = 212, 432           # 갈림목
CX0, CX1 = 520, 856           # 배포판
BR = 476                      # 분기 수직선
RH = 92
rows = {"rhcos": 112, "flatcar": 224, "bottle": 352, "rancher": 464}

d.t(AX0, 100, "만든 곳", 12, SOFT, KR, "start")
d.t(CX0, 100, "배포판", 12, SOFT, KR, "start")

# 선 먼저
ROOT_Y = 214
d.arrow([(AX1, ROOT_Y), (BX0 - 4, ROOT_Y)], MUTED, "ar", 1.3)
d.path(f"M {BX1} {ROOT_Y} L {BR} {ROOT_Y}", ACC, 1.4)
for key in ("rhcos", "flatcar"):
    yc = rows[key] + RH / 2
    d.arrow([(BR, ROOT_Y), (BR, yc), (CX0 - 4, yc)], ACC, "acc", 1.4)
for key, c, m in (("bottle", WARN, "warn"), ("rancher", MUTED, "ar")):
    yc = rows[key] + RH / 2
    d.arrow([(AX1, yc), (CX0 - 4, yc)], c, m, 1.3)

# 만든 곳
for yc, name, sub, c in ((ROOT_Y, "CoreOS", "스타트업", MUTED), (rows["bottle"] + RH / 2, "AWS", "", WARN),
                         (rows["rancher"] + RH / 2, "Rancher", "지금 SUSE", MUTED)):
    d.box(AX0, yc - 26, AX1 - AX0, 52, PAPER2, c, 1.1, 6)
    if sub:
        d.t((AX0 + AX1) / 2, yc - 4, name, 13, INK, MONO, "middle", 600)
        d.t((AX0 + AX1) / 2, yc + 15, sub, 12, MUTED, KR)
    else:
        d.t((AX0 + AX1) / 2, yc + 5, name, 13, INK, MONO, "middle", 600)

# 갈림목
d.tone(BX0, ROOT_Y - 60, BX1 - BX0, 120, ACC, 8, "14", 1.4)
d.t(BX0 + 14, ROOT_Y - 34, "CoreOS Linux · 2013", 13, ACC, MONO, "start", 600)
d.t(BX0 + 14, ROOT_Y - 12, "→ Container Linux 개명", 12, INK, KR, "start")
d.t(BX0 + 14, ROOT_Y + 10, "이중 파티션 업데이트", 12, MUTED, KR, "start")
d.t(BX0 + 14, ROOT_Y + 32, "패키지 관리자 없음", 12, MUTED, KR, "start")
d.box(BX0, ROOT_Y + 84, BX1 - BX0, 32, PAPER, RULE, 1.0, 6)
d.t(BX0 + 14, ROOT_Y + 105, "etcd", 12, INK, MONO, "start", 600)
d.t(BX0 + 56, ROOT_Y + 105, "이 생태계에서 나옴", 12, MUTED, KR, "start")
d.line((BX0 + BX1) / 2, ROOT_Y + 60, (BX0 + BX1) / 2, ROOT_Y + 84, RULE, 1.0, "3 3")

# 배포판
dist = [("rhcos", "RHCOS", INFO, "Red Hat 인수 + Project Atomic",
         "OpenShift Container Platform 용", "앱 = 컨테이너 · 패키지 관리자 언급 없음"),
        ("flatcar", "Flatcar Container Linux", OK, "Kinvolk GmbH 포크 → 지금 Microsoft",
         "Nebraska 자동 업그레이드 · Ignition", "앱 = 컨테이너 · 패키지 관리자 없음"),
        ("bottle", "Bottlerocket", WARN, "dm-verity · 대체로 읽기 전용",
         "제어 컨테이너 (containerd)", "앱 = OCI 이미지 · 패키지 관리자 없음"),
        ("rancher", "RancherOS", MUTED, "시스템 Docker (첫 프로세스)",
         "+ 사용자 Docker (앱)", "앱 = Docker 컨테이너 · 패키지 관리자 언급 없음")]
for key, name, c, l1, l2, l3 in dist:
    y = rows[key]
    d.box(CX0, y, CX1 - CX0, RH, PAPER2, c, 1.2, 8)
    d.t(CX0 + 14, y + 22, name, 13, c, MONO, "start", 600)
    d.t(CX0 + 14, y + 42, l1, 12, INK, KR, "start")
    d.t(CX0 + 14, y + 60, l2, 12, MUTED, KR, "start")
    d.t(CX0 + 14, y + 80, l3, 12, MUTED, KR, "start")

d.t(AX0, 588, "Bottlerocket · RancherOS 는 Container Linux 와 이어지지 않은 따로 선 뿌리",
    11, SOFT, KR, "start")
d.legend(604, [("갈림목", ACC), ("Red Hat 쪽", INFO), ("Microsoft 쪽", OK), ("AWS 쪽", WARN)])
d.save("09-01.distro-lineage.svg")
print("ok 09-01.distro-lineage")
