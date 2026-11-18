# 타입 스펙: type-sequence
# 03-01.cri-pod-startup-sequence — CRI 파드 기동 호출 순서
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import Seq, OK, INFO, ACC, MUTED

s = Seq(1000, 636, "CRI SEQUENCE · 03-01",
        "kubelet 과 containerd 간의 파드 기동 호출 순서",
        "RunPodSandbox 부터 StartContainer 까지 gRPC 메서드 호출 흐름",
        lead="샌드박스 준비 → 이미지 확인·풀 → 컨테이너 생성 → 시작")

lx = s.lanes([("kubelet", "k8s 노드 에이전트"),
              ("containerd CRI", "gRPC Unix 소켓 서버"),
              ("runc", "OCI 저수준 런타임")],
             y0=104, lane_w=180)
s.rails(560)

s.msg("kubelet", "containerd CRI", "1. RunPodSandbox()", 170, c=INFO, sub="파드 이름·UID·네임스페이스·DNS 설정")
s.msg("containerd CRI", "runc", "pause 생성 · 기동", 205, c=MUTED, sub="공유 netns 인프라 컨테이너")
s.msg("containerd CRI", "kubelet", "podSandboxID 반환", 245, c=OK, sub="샌드박스 핸들 획득")

s.msg("kubelet", "containerd CRI", "2. ImageStatus() / PullImage()", 295, c=INFO, sub="노드 로컬 이미지 확인 및 풀")
s.msg("containerd CRI", "kubelet", "imageRef(sha256 digest) 반환", 340, c=OK, sub="이미지 준비 완료")

s.msg("kubelet", "containerd CRI", "3. CreateContainer(podSandboxID, config)", 390, c=INFO, sub="환경변수·마운트·인자 전달")
s.msg("containerd CRI", "kubelet", "containerID 반환", 435, c=OK, sub="상태 필드용 식별자 응답")

s.msg("kubelet", "containerd CRI", "4. StartContainer(containerID)", 485, c=INFO, sub="앱 컨테이너 실행 요청")
s.msg("containerd CRI", "runc", "컨테이너 프로세스 기동", 525, c=MUTED, sub="앱 프로세스 생성")

s.legend(574, [("kubelet gRPC 요청", INFO), ("런타임 응답 / 결과", OK), ("저수준 OCI 실행", MUTED)])

out_path = Path(__file__).resolve().parent.parent / "03-01.cri-pod-startup-sequence.svg"
s.save(str(out_path))
print("ok 03-01.cri-pod-startup-sequence")
