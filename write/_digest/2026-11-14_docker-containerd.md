> 출처: Gemini · 2026-11-14 · Docker vs containerd 및 Kubernetes 런타임 생태계 심층 분석 리포트 · 분야: k8s · 미검증

## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| Docker Engine | CLI·API·빌드·볼륨·네트워크를 묶은 올인원 컨테이너 플랫폼 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| containerd | 이미지 관리·수명주기 감독을 전담하는 CNCF 표준 컨테이너 런타임 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| runc | OCI 런타임 명세대로 리눅스 커널 격리(namespace·cgroups)를 실행하는 저수준 바이너리 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| CRI | Kubelet과 컨테이너 런타임 사이의 통신 규약을 정의한 gRPC 인터페이스 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| OCI | 컨테이너 이미지 규격과 실행 방식을 정의한 개방형 산업 표준 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| dockershim | CRI 이전의 Docker 데몬을 Kubelet에 연결하던 임시 어댑터 계층 | [컨테이너의 탄생](../08_cloud/book/networking-and-kubernetes/03-01.컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브.md) |
| ctr | containerd에 내장된 저수준 네이티브 디버깅 CLI | |
| nerdctl | containerd 위에서 Docker CLI 문법과 동일한 사용자 경험을 제공하는 도구 | |
| crictl | Kubernetes CRI 호환 런타임을 점검하고 노드를 디버깅하는 전용 CLI | [Service 5유형](../08_cloud/book/networking-and-kubernetes/05-02.Service 5유형 — ClusterIP에서 LoadBalancer까지.md) |



## 요점

- 플랫폼과 런타임 분리: Docker는 개발 생산성 중심의 종합 도구이며, Kubernetes 프로덕션은 containerd와 runc 계층만 직결합니다.
- dockershim 제거 효과: 중간 Docker 데몬을 거치지 않고 `kubelet -> CRI -> containerd -> runc`로 연결해 메모리와 지연을 줄입니다.
- OCI 표준 호환성: Dockerfile로 빌드한 이미지도 OCI Image Spec을 따르므로 containerd 환경에서 동일하게 동작합니다.
- CLI 역할과 네임스페이스 격리:
  - `ctr`: containerd 네이티브 gRPC 소켓과 직접 통신하는 최소 디버깅 도구입니다.
  - `nerdctl`: Docker CLI 호환 명령어와 BuildKit 연동을 제공하며 기본 네임스페이스(`default`)를 조회합니다.
  - `crictl`: CRI gRPC 소켓과 통신하며 Kubelet과 동일한 시야(`k8s.io` 네임스페이스의 Pod 및 컨테이너)를 조회합니다.
- 노드 트러블슈팅: 제어 평면 장애 시 노드에 접속해 `crictl pods`, `crictl ps`, `crictl logs`, `crictl exec`로 진단합니다.



## 경고

- ⚠ crictl 컨테이너 생성 시 Kubelet의 즉시 삭제 단정: 원문은 crictl로 만든 컨테이너를 Kubelet이 비인가로 보아 즉시 제거한다고 단정합니다(20·106~109행). 네임스페이스와 라벨에 따른 실제 동작은 다를 수 있습니다. — 확인됨: [Kubernetes crictl 문서](https://raw.githubusercontent.com/kubernetes/website/release-1.28/content/en/docs/tasks/debug/debug-cluster/crictl.md)
- ⚠ crictl 기본 소켓 탐색 순서: 원문은 설정 파일 부재 시 구형 dockershim 소켓부터 순차 탐색한다고 설명합니다(48행). dockershim 제거 이후 최신 cri-tools 버전의 기본 탐색 동작과 다를 수 있습니다. — 확인됨: [cri-tools v1.35.0 crictl.md](https://raw.githubusercontent.com/kubernetes-sigs/cri-tools/v1.35.0/docs/crictl.md)
- ⚠ 모든 Dockerfile 이미지의 완벽 호환성 단정: 원문은 모든 Dockerfile 이미지가 수정 없이 containerd에서 실행된다고 단정합니다(14·35행). 레거시 v1 schema 이미지나 독점 설정이 든 경우 동작하지 않을 수 있습니다. — 확인됨: [containerd RELEASES v2.0.0](https://raw.githubusercontent.com/containerd/containerd/v2.0.0/RELEASES.md)
- ⚠ CI 환경 BuildKit의 데몬리스 구동 단정: 원문은 nerdctl build와 BuildKit을 데몬 없는 사용자 공간 빌드로 설명합니다(32행). BuildKit은 통상 buildkitd 데몬을 요구하므로 비특권 Pod 구성 시 검증이 필요합니다. — 확인됨: [BuildKit README v0.17.0](https://raw.githubusercontent.com/moby/buildkit/v0.17.0/README.md)
