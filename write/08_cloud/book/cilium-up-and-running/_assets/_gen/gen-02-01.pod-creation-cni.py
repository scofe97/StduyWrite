# 타입 스펙: type-sequence — Pod 생성 시 컨테이너 런타임과 Cilium CNI 플러그인·에이전트 호출 흐름.
# 사실 출처: Cilium Up and Running 2장 The Cilium CNI Plugin (§Figure 2-3).
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
s = Seq(W, H, "CILIUM UP AND RUNNING · 02-01 §3", "Pod 생성 시 CNI 네트워크 연결 흐름",
        "kubelet 과 런타임에서 cilium-cni 바이너리 및 cilium-agent 로 이어지는 배선 시퀀스",
        "런타임이 CNI 바이너리를 호출하고 바이너리는 로컬 에이전트 소켓으로 위임합니다")

s.lanes([
    ("Kubelet / CRI", "containerd / CRI-O"),
    ("cilium-cni", "/opt/cni/bin/"),
    ("cilium-agent", "cilium.sock"),
    ("리눅스 커널", "netns & eBPF 맵"),
], y0=104, lane_w=190)

s.rails(ybot=436)

# 메시지 흐름
s.msg("Kubelet / CRI", "cilium-cni", "1. CNI ADD 요청", 168, INFO, "info", sub="컨테이너 ID · NetNS 경로 전달")
s.msg("cilium-cni", "cilium-agent", "2. IPAM IP 할당 요청", 210, ACC, "acc", sub="UDS REST API 로 Pod IP 요청")
s.msg("cilium-cni", "리눅스 커널", "3. veth 생성 및 NetNS 배선", 252, OK, "ok", sub="호스트 lxc... 및 Pod eth0 링크 생성")
s.msg("cilium-cni", "cilium-agent", "4. EndpointCreate 요청", 294, ACC, "acc", sub="UDS REST 로 엔드포인트 생성 위임")
s.msg("cilium-agent", "리눅스 커널", "5. eBPF 적재 및 맵 등록", 336, OK, "ok", sub="cilium_lxc · cilium_ipcache_v2 갱신")
s.msg("cilium-agent", "cilium-cni", "6. 엔드포인트 등록 완료", 378, OK, "ok", dash="3 3", sub="엔드포인트 등록 결과 응답")
s.msg("cilium-cni", "Kubelet / CRI", "7. CNI Result JSON 반환", 418, INFO, "info", dash="3 3", sub="cniVersion 규격 응답")

# 범례
s.legend(454, [
    ("런타임 호출", INFO),
    ("로컬 REST 위임 (핵심)", ACC),
    ("커널 인터페이스 배선", OK),
    ("반환 스트림", MUTED),
])

s.save("02-01.pod-creation-cni.svg")
