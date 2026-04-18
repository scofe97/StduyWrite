# Ch08: Docker Registry로서의 Nexus — 심화 탐구

## Q1: Docker 리포지토리마다 별도 포트가 필요한 기술적 이유는?

Docker Registry HTTP API V2의 엔드포인트 구조를 보면 이유가 명확해진다. `GET /v2/<name>/manifests/<reference>` 형태로 요청이 들어오는데, 여기서 `<name>`은 이미지 이름이지 리포지토리 이름이 아니다. 즉 Docker 클라이언트가 보내는 HTTP 요청에는 "hosted에서 가져와라" 또는 "proxy에서 가져와라"라는 정보가 없다.

Maven의 경우 `/repository/maven-releases/com/example/...` 형태로 URL 경로에 리포지토리 이름이 포함되므로 하나의 포트로 여러 리포지토리를 구분할 수 있지만, Docker는 그런 구조가 아니다. Nexus 입장에서 같은 포트로 들어온 `/v2/my-app/manifests/1.0` 요청이 hosted를 위한 건지 proxy를 위한 건지 알 방법이 없으니, 포트로 구분하는 수밖에 없는 것이다.

Nexus 3.x부터는 Repository Connector라는 개념으로 각 Docker 리포지토리에 전용 HTTP/HTTPS 커넥터를 할당하는 방식을 택했다. 이 제약은 nginx 서브도메인 라우팅으로 완화할 수 있는데, 서브도메인별로 다른 포트로 프록시하면 Docker 클라이언트는 표준 443 포트만 사용하면서도 내부적으로 올바른 리포지토리에 연결된다. Nexus Pro에서는 하나의 HTTPS 커넥터에서 경로 기반 라우팅을 지원하는 "Repository Path" 기능도 제공하지만, OSS에서는 포트 분리가 유일한 방법이다.

---

## Q2: docker-proxy로 Docker Hub rate limit을 우회할 수 있는가?

"우회"라기보다 "공유"에 가깝다. docker-proxy가 이미지를 한 번 캐싱하면, 이후 팀원들의 pull 요청은 Nexus 로컬 캐시에서 처리되므로 Docker Hub에 요청이 나가지 않는다. 팀원이 50명이어도 같은 이미지에 대해 Docker Hub 요청은 1회만 발생하니 rate limit 소모가 획기적으로 줄어든다.

다만 캐시 미스가 발생하면 여전히 Docker Hub에 요청이 나간다. 새로운 이미지를 처음 pull하거나, 캐시 만료(TTL) 후 재검증할 때가 해당된다. Nexus에서 proxy 리포지토리의 "Maximum Component Age"와 "Maximum Metadata Age" 설정으로 캐시 수명을 조절할 수 있는데, 길게 잡으면 rate limit은 아끼지만 upstream의 보안 패치 이미지 반영이 늦어지는 트레이드오프가 생긴다.

proxy에 Docker Hub 인증 정보를 넣으면 익명(100회/6시간) 대신 인증(200회/6시간) 한도가 적용되고, Docker Pro/Team 계정이면 5000회/일까지 올라간다. 실무적으로는 Docker Hub 무료 계정 하나를 팀 공유용으로 만들어서 proxy에 등록하는 것만으로도 rate limit 문제가 대부분 해소된다. CI/CD에서 대량의 이미지를 pull하는 환경이라면 Docker Pro 계정 투자를 고려해볼 만하다.

---

## Q3: 멀티 아키텍처 이미지(manifest list)를 Nexus에서 관리할 때 주의점은?

멀티 아키텍처 이미지는 하나의 태그가 여러 플랫폼(amd64, arm64 등)의 manifest를 가리키는 "fat manifest"(manifest list 또는 OCI image index) 구조다. `docker buildx build --platform linux/amd64,linux/arm64 --push`로 빌드하면 이런 구조가 만들어진다.

Nexus 3.x는 manifest list를 지원하지만, 몇 가지 주의가 필요하다. Cleanup Policy에서 manifest list를 삭제하면 하위 플랫폼별 manifest도 함께 참조가 끊기므로, 정리 후에도 dangling manifest가 남을 수 있다. Compact Blob Store를 실행해야 실제 디스크가 회수된다. manifest list → platform manifest → layer라는 3단 참조 구조이므로, 한 번의 Cleanup으로 전체 체인이 정리되지 않을 수 있다. Cleanup을 2~3회 연속 실행해야 orphan layer까지 완전히 제거되는 경우도 있으니, 정리 태스크를 한 번만 돌리고 끝내지 말고 디스크 사용량을 확인하는 습관이 필요하다.

또한 docker-proxy를 통해 캐싱된 멀티 아키텍처 이미지는 pull한 플랫폼의 레이어만 캐싱될 수 있다. amd64 서버에서 pull하면 arm64 레이어는 캐싱되지 않으므로, arm64 개발자가 같은 이미지를 pull할 때 다시 Docker Hub에 요청이 나갈 수 있다는 점을 알아두자. 이건 Docker Hub rate limit 계산 시 간과하기 쉬운 부분이다.

---

## Q4: Docker layer가 여러 이미지에서 공유될 때 스토리지 절약 효과는?

Docker 레이어는 SHA256 다이제스트로 식별된다. 동일한 `FROM ubuntu:22.04`를 사용하는 10개의 서비스 이미지가 있다면, 베이스 레이어는 Nexus에 한 번만 저장되고 10개의 manifest가 이를 참조하는 구조가 된다.

실제 절약 효과는 베이스 이미지 표준화에 비례한다. 팀에서 공통 베이스 이미지(예: `company-base:jdk17`)를 정의하고 모든 서비스가 이를 상속하면, 서비스별로 추가되는 레이어만 별도 저장되므로 스토리지 효율이 높아진다. 구체적 수치로 보면, `ubuntu:22.04` 베이스(약 77MB)를 10개 서비스가 공유하면 770MB 대신 77MB만 저장되니 약 90%의 절약이 가능하다. 물론 각 서비스의 애플리케이션 레이어가 추가되지만, 베이스 레이어가 전체의 50~70%를 차지하는 경우가 많으니 절약 효과는 상당하다.

반면 서비스마다 다른 베이스를 쓰면 공유 레이어가 거의 없어서 절약 효과도 미미하다. Blob Store의 "Total Size"와 "Available Space"를 모니터링하면 현재 얼마나 효율적으로 레이어가 공유되고 있는지 간접적으로 파악할 수 있다. 이미지 수 대비 Blob Store 크기가 선형보다 느리게 증가한다면 레이어 공유가 잘 되고 있다는 신호다.

---

## Q5: insecure-registries 없이 HTTP 레지스트리를 사용하는 방법이 있는가?

Docker가 HTTP를 거부하는 건 MITM(중간자) 공격 방지를 위함이므로, 근본적으로는 TLS를 설정하는 게 올바른 해결책이다. 자체 서명 인증서라도 Docker 데몬에 CA 인증서를 등록하면 insecure-registries 없이 동작한다.

```bash
# Linux: /etc/docker/certs.d/<registry-host>:<port>/ca.crt에 CA 인증서 배치
mkdir -p /etc/docker/certs.d/nexus.company.com:8082
cp company-ca.crt /etc/docker/certs.d/nexus.company.com:8082/ca.crt

# 동일하게 group 포트도
mkdir -p /etc/docker/certs.d/nexus.company.com:8083
cp company-ca.crt /etc/docker/certs.d/nexus.company.com:8083/ca.crt
```

이 방식의 장점은 `daemon.json`을 건드리지 않아도 된다는 것이다. 데몬 재시작 없이 인증서 파일만 배치하면 즉시 적용된다. macOS Docker Desktop에서는 `~/.docker/certs.d/` 경로를 사용하고, 시스템 키체인에 CA를 등록하는 방법도 있다.

Let's Encrypt를 쓰면 무료로 공인 인증서를 발급받을 수 있어 클라이언트 측 설정이 전혀 필요 없어진다. nginx에서 certbot으로 자동 갱신하는 것이 가장 간편한 방식이며, 내부 DNS가 있다면 와일드카드 인증서(`*.company.com`)를 발급받아서 모든 서브도메인에 적용하는 것도 가능하다.

`localhost`와 `127.0.0.1`은 Docker가 예외적으로 HTTP를 허용하므로, 개발 환경에서는 insecure-registries 설정 없이도 `localhost:8082`로 접근할 수 있다. 이 예외는 Docker 데몬에 하드코딩되어 있어서 별도 설정이 필요 없다.

---

## Q6: Harbor와 Nexus Docker Registry의 기능 비교는?

Harbor는 Docker 이미지 관리에 특화된 오픈소스 레지스트리로, Trivy 기반 취약점 스캔, Cosign 이미지 서명, replication(원격 복제), garbage collection UI, 프로젝트 단위 quota 관리 등 컨테이너 보안과 운영에 초점을 맞추고 있다.

Nexus는 "범용 아티팩트 저장소"로서 Docker를 지원하는 것이므로, 컨테이너 특화 기능은 Harbor에 비해 부족하다. 하지만 Maven, npm, PyPI, raw 등 여러 포맷을 한 곳에서 관리할 수 있고, 사용자/역할 관리가 통합되어 있다는 장점이 있다.

| 기능 | Nexus OSS | Harbor |
|------|-----------|--------|
| 취약점 스캔 | 없음 (Pro에서 일부) | Trivy 내장 |
| 이미지 서명 | 외부 Notary 필요 | Cosign/Notation 내장 |
| Garbage Collection | Cleanup + Compact (2단계) | UI에서 원클릭 |
| 프로젝트 Quota | 없음 | 프로젝트별 스토리지 제한 |
| 멀티 포맷 | Maven, npm, Docker 등 | Docker/OCI 전용 |
| Replication | Pro에서 지원 | 내장 (push/pull 모드) |

판단 기준은 명확하다. 이미 Nexus를 운영 중이고 Docker 이미지 관리가 부수적 요구사항이라면 Nexus에서 처리하고, 컨테이너 보안이 핵심 요구사항이거나 이미지 관리가 주 업무라면 Harbor를 별도로 운영하는 것이 합리적 선택이다. 둘 다 운영하면서 Nexus를 Harbor의 upstream proxy로 연결하는 하이브리드 구성도 가능하긴 하지만, 운영 복잡도가 올라가므로 신중해야 한다.

---

## 심화 질문

> Nexus Docker Registry를 K8s의 기본 이미지 소스로 설정하려면?

Kubernetes에서 Pod가 이미지를 pull할 때는 각 노드의 containerd(또는 CRI-O)가 레지스트리에 접근한다. Nexus를 기본 소스로 쓰려면 두 가지를 설정해야 한다.

첫째, 모든 워커 노드의 containerd 설정(`/etc/containerd/config.toml`)에 Nexus를 mirror로 등록한다.

```toml
[plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
  endpoint = ["https://docker-group.company.com"]

[plugins."io.containerd.grpc.v1.cri".registry.configs."docker-group.company.com".auth]
  username = "k8s-puller"
  password = "secret"
```

이렇게 설정하면 `docker.io`에서 pull하는 모든 요청이 Nexus를 경유하게 된다. Pod spec에서 `image: nginx:1.27`이라고 써도 실제로는 Nexus docker-group에서 가져오는 것이다.

둘째, 인증이 필요한 경우 Kubernetes Secret(`docker-registry` 타입)을 생성하고 Pod spec의 `imagePullSecrets`에 지정하거나, ServiceAccount에 연결해서 자동 적용되게 한다.

```bash
kubectl create secret docker-registry nexus-docker \
  --docker-server=docker-group.company.com \
  --docker-username=k8s-puller \
  --docker-password=secret \
  -n my-namespace
```

네임스페이스별로 다른 인증 정보를 사용할 수 있어, 팀별 접근 제어가 가능해진다. TLS 인증서 문제도 중요한데, 자체 서명 인증서를 쓰면 모든 노드에 CA 인증서를 배포해야 한다. 노드 수가 많으면 DaemonSet이나 cloud-init으로 자동화하는 것이 실수를 줄이는 방법이다.
