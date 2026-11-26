# 01-01 §6 컨테이너·Kubernetes 환경의 FHS 적용 경계.
# 타입 스펙: type-deployment — Docker 호스트 존, Kubernetes 워커 노드 존, 노드 외부 클러스터 스토리지(PVC) 배치 대조.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 560
d = D(W, H, "DOCKER & KUBERNETES · FHS BOUNDARY",
      "컨테이너 rootfs FHS 와 호스트·클러스터 스토리지 경계",
      "왼쪽 Docker 호스트에서는 자유 경로가 바인드 마운트로 컨테이너 rootfs 에 연결되고, 오른쪽 Kubernetes 워커 노드에서는 파드가 노드 밖 클러스터 PVC 를 마운트하며 hostPath 는 노드 로컬 예외로 제한된다.",
      "FHS 는 컨테이너 내부 트리에 적용되고, 호스트 마운트 위치와 노드 독립 PVC 는 별도 규약을 따릅니다")

def badge(x, y, txt, c):
    bw = len(txt) * 7 + 12
    d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="18" rx="2" fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(x + bw / 2, y + 13, txt, 10, c, MONO, "middle", 600)

# 1. 환경 존 3개 (bg → zones → arrows → nodes)
Z1X, Z1W = 20, 396     # 20..416
Z2X, Z2W = 440, 296    # 440..736  (Worker Node)
Z3X, Z3W = 768, 192    # 768..960  (Cluster Storage — outside worker node!)
ZY, ZH = 104, 380

for zx, zw, label in [
    (Z1X, Z1W, "ZONE 1 · DOCKER HOST"),
    (Z2X, Z2W, "ZONE 2 · K8S WORKER NODE"),
    (Z3X, Z3W, "CLUSTER STORAGE"),
]:
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{zw}" height="{ZH}" rx="8" fill="#F5F5F305" stroke="{RULE}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    mw = len(label) * 6.5 + 16
    d.o.append(f'<rect x="{zx + 14}" y="{ZY - 6}" width="{mw}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(zx + 22, ZY + 4, label, 8, SOFT, MONO, "start", 500)

# 2. 화살표 먼저 (z-order)
# Zone 1: Host → Container bind mount
d.arrow([(218, 240), (218, 294)], INFO, "info", 1.6)
d.t(234, 272, "바인드 마운트", 13, INFO, KR, "start", 500)

# Zone 2 (inside Worker Node): Pod → hostPath (BAD dashed)
d.arrow([(588, 260), (588, 326)], BAD, "bad", 1.6, dash="5 4")
d.t(604, 298, "예외 직접 연결", 13, BAD, KR, "start", 500)

# Zone 2 → Zone 3 (crosses Worker Node boundary to Cluster Storage): Pod → PVC (OK solid)
d.arrow([(716, 200), (782, 200)], OK, "ok", 1.6)
d.t(752, 184, "PVC", 11, OK, MONO, "middle", 600)

# 3. Zone 1 노드 (Docker Host)
d.box(40, 140, 356, 100, PAPER2, RULE, 1.0, 6)
badge(52, 152, "HOST", INFO)
d.t(108, 166, "호스트 경로 (FHS 강제 없음)", 14, INK, KR, "start", 600)
d.t(218, 198, "$GITLAB_HOME/config · logs · data", 12, INFO, MONO)
d.t(218, 224, "예: ~/gitlab-docker 또는 /srv/gitlab", 13, MUTED, KR)

# Container node (FOCAL)
d.o.append(f'<rect x="40" y="296" width="356" height="164" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
badge(52, 308, "CONTAINER", ACC)
d.t(144, 322, "컨테이너 rootfs (FHS 기반)", 14, ACC, KR, "start", 600)

chips = [
    ("/etc/gitlab",     "설정 파일"),
    ("/var/log/gitlab", "로그 파일"),
    ("/var/opt/gitlab", "애플리케이션 데이터"),
]
for i, (cp, desc) in enumerate(chips):
    cy = 340 + i * 36
    d.box(56, cy, 324, 28, PAPER, RULE, 0.9, 4)
    d.t(68, cy + 19, cp, 12, INK, MONO, "start", 600)
    d.t(368, cy + 19, desc, 13, MUTED, KR, "end")

# 4. Zone 2 노드 (K8s Worker Node)
d.box(460, 140, 256, 120, PAPER2, RULE, 1.0, 6)
badge(472, 152, "POD", ACC)
d.t(524, 166, "파드 컨테이너 rootfs", 14, INK, KR, "start", 600)
d.t(588, 200, "베이스 이미지 FHS 기반", 13, MUTED, KR)
d.t(588, 226, "워커 노드 비고정 · 재배치", 13, MUTED, KR)

# hostPath node (inside Worker Node — BAD)
d.tone(460, 328, 256, 132, BAD, r=6, op="12", sw=1.2)
badge(472, 340, "HOSTPATH", BAD)
d.t(588, 382, "노드 로컬 /var/log", 14, BAD, KR, "middle", 600)
d.t(588, 412, "노드 장악 위험", 13, INK, KR)
d.t(588, 438, "로그 수집기·노드 에이전트 예외", 13, MUTED, KR)

# 5. Zone 3 노드 (Cluster Storage — OUTSIDE Worker Node! — OK)
d.tone(784, 140, 160, 164, OK, r=6, op="12", sw=1.2)
badge(796, 152, "PVC", OK)
d.t(864, 198, "PVC 추상화", 15, OK, KR, "middle", 600)
d.t(864, 232, "일반 워크로드 권장", 13, INK, KR)
d.t(864, 260, "노드 독립 영구 볼륨", 13, MUTED, KR)
d.t(864, 286, "파드 이동성 유지", 13, MUTED, KR)

d.legend(512, [("FHS 기반 (rootfs)", ACC), ("바인드 마운트", INFO), ("PVC (노드 외부)", OK), ("hostPath (노드 내부 예외)", BAD)])
d.save("01-01.container-k8s-boundary.svg")
