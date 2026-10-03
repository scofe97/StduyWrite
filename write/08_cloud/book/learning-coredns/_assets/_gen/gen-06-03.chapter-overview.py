# 06-03 학습 목표 뒤 전체 지도 — 기본 매니페스트에 박힌 값마다 출처(호환·동작·편의)와 이유를 놓는다.
# 본문 근거: 이 노트 핵심 요약과 §2~§6, 결정 치트시트. replicas 의 kubeadm/애드온 차이는
#            kubeadm dns.go `coreDNSReplicas = 2` 와 coredns.yaml.sed `# replicas: not specified here:` 로 확인(2026-10-03).
# 타입 스펙: type-dp-security-matrix — 값(행) × 출처·이유(열) 격자에서 출처 열이 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 값이 든 격자로 다시 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 668
d = D(W, H, "LEARNING COREDNS · 06-03",
      "기본 매니페스트의 값은 어디서 왔나",
      "설명 없이 박힌 값마다 출처를 셋으로 갈랐다. 호환은 kube-dns 에서 무중단으로 넘어오려고 정한 값, "
      "동작상 필요는 CoreDNS 가 제대로 돌려면 그래야 하는 값, 배포 편의는 나중에 고치지 않으려고 미리 넣은 값이다.",
      "주황 열이 그 값의 출처입니다")

COLS = [(20, 210, "값"), (240, 150, "출처"), (400, 360, "이유"), (770, 90, "절")]
rows = [
    (("Service 이름", "kube-dns"), "호환", "불변 필드 · 바꾸면 끊긴다", "§3"),
    (("clusterIP", "10.7.240.10"), "동작상 필요", "kubelet 이 resolv.conf 에 쓴다", "§3"),
    (("ClusterRole", "pods · nodes"), "배포 편의", "pods 는 verified 때만 · nodes 는 federation 용", "§2"),
    (("replicas", "2"), "작은 클러스터 기준", "kubeadm 만 2 · 애드온은 비움", "§4 · §5"),
    (("memory limit", "170Mi"), "호환", "kube-dns 와 같은 값 · 식으로 116,000 개", "§4"),
    (("dnsPolicy", "Default"), "동작상 필요", "노드의 상류로 외부 이름을 푼다", "§4"),
    (("cache 30", "한 블록"), "개선 대상", "클러스터 이름에는 중복 · 블록 분리", "§6"),
]
Y0, PITCH, RH = 132, 60, 52

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, ACC if k == 1 else SOFT, KR, "start", 600)

d.tone(236, Y0 - 4, 158, PITCH * (len(rows) - 1) + RH + 8, ACC, 8, "12", 1.4)

for i, ((vm, vs), src, why, sec) in enumerate(rows):
    y = Y0 + i * PITCH
    for k, (x, w, _) in enumerate(COLS):
        if k != 1:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    d.t(32, y + 22, vm, 14, INK, KR, "start", 600)
    d.t(32, y + 42, vs, 12, MUTED, KR if any("가" <= c <= "힣" for c in vs) else MONO, "start")
    d.t(252, y + 31, src, 13, ACC, KR, "start", 600)
    d.t(412, y + 31, why, 13, INK, KR, "start")
    d.t(815, y + 31, sec, 13, MUTED, KR)

d.t(20, 576, "1~4절 · 값이 왜 그 값인가 · 5~6절 · 클러스터에 맞춰 다시 고른다", 13, MUTED, KR, "start")
d.t(20, 600, "10.7.240.10 은 원서 예제 값 · 클러스터마다 다르다", 12, SOFT, KR, "start")

d.legend(620, [("값의 출처", ACC)])
d.save("06-03.chapter-overview.svg")
