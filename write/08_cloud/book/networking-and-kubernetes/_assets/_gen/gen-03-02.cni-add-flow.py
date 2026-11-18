# 03-02.cni-add-flow — Pod 하나에 네트워크가 붙을 때 누가 누구를 부르는가
# 본문 요구: §5 가 "CNI 플러그인을 실행하는 쪽은 kubelet 이 아니라 컨테이너 런타임"이라고 말하고,
#           호출이 실행 파일 + 환경 변수 + stdin JSON 이라는 점을 CNM 과의 차이로 든다. 주체가 넷이고
#           순서가 있으므로 산문보다 시퀀스가 맞다.
# 타입 스펙: type-sequence.md — 참여자 레인 넷과 시간축.
# 근거(버전 고정): containernetworking/cni v1.3.1 SPEC.md Section 2(실행 프로토콜 · CNI_COMMAND ·
#       CNI_NETNS · stdin 설정 · stdout 결과), kubernetes/website network-plugins.md(1.24 부터 CNI 관리는
#       kubelet 범위 밖), kubernetes/cri-api v0.34.0 api.proto(RunPodSandbox),
#       containerd v2.1.4 docs/cri/config.md(conf_dir /etc/cni/net.d · bin_dirs /opt/cni/bin).
# 이력: 2026-11-18 신설.
import ddx
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 520
d = Seq(W, H, "CNI ADD · WHO CALLS WHOM",
        "CNI 플러그인을 실행하는 쪽은 컨테이너 런타임이다",
        "kubelet 이 CRI 로 Pod 샌드박스를 요청하면 컨테이너 런타임이 네트워크 네임스페이스를 만들고 "
        "CNI 설정을 읽어 플러그인 실행 파일을 ADD 로 실행한다. 플러그인은 그 네임스페이스에 인터페이스를 만들고 "
        "주소와 경로를 넣은 뒤 결과를 표준 출력으로 돌려준다.",
        lead="kubelet 은 CRI 까지만 말합니다 · 플러그인은 떠 있는 서버가 아니라 그때마다 실행되는 파일입니다")

ddx.lanes(d, [("kubelet", "CRI 클라이언트"), ("컨테이너 런타임", "containerd · CRI-O"),
              ("CNI 플러그인", "실행 파일"), ("Pod netns", "새 네임스페이스")], lane_w=200)
K, R, P, N = "kubelet", "컨테이너 런타임", "CNI 플러그인", "Pod netns"
d.rails(432)

d.msg(K, R, "RunPodSandbox", 196, sub="CRI 호출")
d.msg(R, N, "netns 생성", 244, c=INFO, mk="info")
d.selfmsg(R, "/etc/cni/net.d", 292, sub="설정 파일을 읽음")
d.msg(R, P, "CNI_COMMAND=ADD", 340, c=ACC, mk="acc", sub="CNI_NETNS · 설정은 stdin")
d.msg(P, N, "eth0 · IP · route", 372, c=OK, mk="ok")
d.msg(P, R, "result JSON", 404, dash="5 5", sub="stdout")
d.msg(R, K, "sandbox ready", 428, dash="5 5")

d.legend(456, [("플러그인을 실행하는 호출", ACC), ("netns 를 만드는 쪽", INFO),
               ("netns 안을 채우는 쪽", OK)])
d.save("03-02.cni-add-flow.svg")
print("ok cni-add-flow")
