> 출처: ChatGPT · 2026-11-16 · Forgejo Runner 기반 자체 호스팅 CI/CD 구축 — 개발 키워드 정리 (개발자 대화 분석) · 분야: devops-keywords, k8s-keywords · 미검증

## 요점

한 줄: 외부 인터넷이 막힌 환경에서 Forgejo 를 중심으로 Git·Runner·레지스트리·의존성을 직접 운영하는 일은 Jenkins 교체가 아니라 빌드 환경 재현성·공급망 보안·아티팩트 관리를 통제하는 일이라고 봅니다.

- 풀려는 문제: 폐쇄망 빌드, Docker Hub 의존 줄이기, 런타임·의존성 버전 통제, CVE 때 빌드 환경 교체, 감사용 빌드 증적, 새 서버에서 같은 CI 재구축입니다.
- 흐름: push → Forgejo webhook → workflow → Runner 가 job 실행(빌드·테스트·이미지) → Forgejo 컨테이너 레지스트리 → 배포입니다. Forgejo 는 Git 저장소이자 플랫폼의 중심이 됩니다.
- Runner 에서 볼 것: job 할당 방식, 동시 실행 자원 제한, job 사이 파일·자격 증명 격리, Runner 가 죽었을 때 job 처리입니다. 격리는 namespace → cgroups → 컨테이너 런타임으로 이어집니다.
- 내부 레지스트리: Docker Hub·GHCR 대신 빌드·런타임·앱 이미지를 내부 레지스트리에 둡니다. 최초 이미지 반입, 취약점 DB·OS 패키지 갱신에는 여전히 외부 연결이나 반입 절차가 필요합니다.
- 대화의 핵심 설계: 런타임과 의존성을 통째로 담은 빌드 이미지를 미리 만들어 씁니다. `uv sync --extra <그룹>` 처럼 선택 의존성 그룹마다 이미지를 나눌 수 있습니다. 공통 이미지는 관리가 쉽고, 분리 이미지는 크기·의존성이 작습니다.
- 공급망 구분: SBOM 은 무엇이 들었나, SLSA 는 빌드 과정을 얼마나 믿나, provenance 는 어떤 소스·환경에서 만들었나, 서명은 누가 서명했나에 답합니다.
- CVE 대응: 베이스 이미지·lockfile 갱신 → 빌드 이미지 재생성 → 스캔·테스트 → 새 digest 로 배포입니다. 취약한 의존성을 품은 앱 이미지도 다시 빌드하고, `latest` 대신 digest 로 배포를 추적합니다.
- pull 실패 진단 순서: `dig` → `curl -I https://registry-1.docker.io/v2/` → `docker login` → `docker pull` → `docker events` 입니다. 401 은 인증 필요, 403 권한, 429 rate limit, 404 저장소·태그 없음입니다.
- 재구축 자동화: provisioning·configuration·verification 세 단계가 필요하고, 핵심 원칙은 멱등성입니다. 설치 성공과 서비스 정상 동작은 다른 상태입니다.
- 트레이드오프 1: 빌드 이미지에 의존성을 넣으면 네트워크 의존이 줄고 환경이 고정되지만 이미지가 커지고 종류가 늘어납니다. 재현성에는 베이스 이미지 digest·lockfile·OS 패키지·빌드 도구 고정과 빌드 중 다운로드 통제가 함께 필요합니다.
- 트레이드오프 2: `docker.sock` 마운트는 단순하지만 호스트 Docker 권한을 넘깁니다. DinD 는 데몬을 나누지만 privileged 가 필요한 경우가 많습니다. 신뢰할 수 없는 PR 을 돌리면 VM 격리까지 봅니다.
- 트레이드오프 3: Forgejo Registry 는 Git 플랫폼 통합, Harbor 는 이미지 공급망 관리, Nexus 는 범용 아티팩트 저장소에 맞습니다. npm·PyPI·Go module proxy 는 각자 배포 체계가 있어 Forgejo 패키지 레지스트리가 자동으로 대신하지 않습니다.
- 더 볼 도구: Trivy·Cosign·Syft·Grype·BuildKit·Buildx·Ansible·SOPS 입니다. BuildKit cache mount(`RUN --mount=type=cache`)는 의존성 다운로드를 줄이지만 재현성의 근거는 아닙니다.
- 관통하는 질문: 빌드 환경을 이미지로 고정하는 일과 빌드 결과물의 재현성은 다른 문제입니다. 이미지 digest 가 같아도 시간·외부 API·네트워크 데이터가 다르면 결과물이 달라집니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| Forgejo·Forgejo Actions | 경량 자체 호스팅 Git 서비스와 그 안의 GitHub Actions 형 workflow | |
| Self-hosted Runner (Forgejo Runner) | job 을 받아 실행하는 서버를 직접 등록·운영하는 CI 실행기 | |
| DinD vs `docker.sock` 마운트 | job 안 Docker 명령을 별도 데몬으로 돌릴지 호스트 데몬을 공유할지의 선택 | [컨테이너 이미지 빌드](../../07_devops/02_Jenkins/03_agent/01-04.컨테이너 이미지 빌드.md) |
| 소켓 마운트의 권한 위험 | 소켓을 꽂은 job 이 호스트 root 와 같은 힘을 갖는 이유와 완화 | [VM Jenkins 에서의 Docker 보안 모델](../../07_devops/02_Jenkins/03_agent/01-05.VM Jenkins에서의 Docker 보안 모델.md) |
| VM 격리 | 신뢰할 수 없는 코드를 컨테이너보다 강한 경계에서 돌리는 방식 | [가상머신](../../08_cloud/book/container-security/05-01.가상머신 — 왜 VM 격리가 더 강하다고 하는가.md) |
| OCI 이미지 (manifest·config·layer) | 이미지가 설정과 층 묶음이고 manifest 가 이를 기술한다는 구조 | [컨테이너 이미지 해부](../../08_cloud/book/container-security/06-01.컨테이너 이미지 해부 — 두 부분과 층과 식별자.md) |
| 태그 vs digest | 바뀔 수 있는 이름과, 내용 해시로 늘 같은 이미지를 가리키는 식별자 | [컨테이너 이미지 해부](../../08_cloud/book/container-security/06-01.컨테이너 이미지 해부 — 두 부분과 층과 식별자.md) |
| pull-through 캐시·레지스트리 미러 | 외부 이미지를 내부 프록시가 받아 두고 다음 pull 을 캐시로 주는 구조 | [Docker Registry 로서의 Nexus](../../07_devops/03_Nexus/04-02.Docker Registry로서의 Nexus.md) |
| Docker Hub rate limit | 익명·계정별 pull 횟수 제한과 429 응답, 인증 프록시로 여유를 만드는 법 | [Docker Registry 로서의 Nexus](../../07_devops/03_Nexus/04-02.Docker Registry로서의 Nexus.md) |
| Harbor | 프로젝트 격리·복제·스캔을 갖춘 클라우드 네이티브 컨테이너 레지스트리 | [Harbor](../../08_cloud/kubernetes/11_devtools/11-04.Harbor.md) |
| Nexus (범용 아티팩트 저장소) | hosted·proxy·group 으로 여러 패키지 형식을 한곳에서 다루는 저장소 | [아티팩트 관리의 기초](../../07_devops/03_Nexus/01-01.아티팩트 관리의 기초.md) |
| 의존성을 담은 빌드 이미지 | 런타임과 의존성을 미리 설치한 이미지로 빌드해 네트워크 의존을 줄이는 방식 | |
| uv 선택 의존성 그룹 | `pyproject.toml` 의 `optional-dependencies` 를 `--extra` 로 골라 설치하는 방식 | |
| 재현 가능한 빌드 | 같은 입력이면 같은 결과물이 나오게 입력을 모두 고정하는 빌드 | [컨테이너 이미지 해부](../../08_cloud/book/container-security/06-01.컨테이너 이미지 해부 — 두 부분과 층과 식별자.md) (일부: Bazel 이 결정론적 이미지를 낸다는 한 줄, 재현 조건 없음) |
| BuildKit 캐시 | 레이어 캐시와 cache mount 로 반복 빌드의 다운로드를 줄이는 빌드 엔진 기능 | [이미지 빌더 종류와 선택](../../07_devops/docs/artifact/container/01-03.이미지 빌더 종류와 선택.md) (일부: BuildKit 과 빌더별 캐시 비교, `--mount=type=cache` 없음) |
| SBOM | 이미지·소프트웨어에 든 구성 요소와 버전을 기계가 읽는 목록으로 남긴 것 | [이미지 속 소프트웨어 취약점](../../08_cloud/book/container-security/07-01.이미지 속 소프트웨어 취약점 — CVE부터 스캔 운영까지.md) |
| SLSA·provenance | 빌드 출처와 과정을 증명하고 그 신뢰 수준을 단계로 나눈 공급망 프레임워크 | [배포 전략](../../07_devops/book/cicd_cicd-patterns/06-01.Deployment Strategies for Structural Patterns.md) |
| 이미지 서명 (Cosign) | 이미지가 믿을 만한 주체가 서명한 뒤 바뀌지 않았음을 검증하는 방식 | [이미지 공급망 보안](../../08_cloud/book/container-security/06-02.이미지 공급망 보안 — 빌드부터 배포까지.md) |
| 이미지 스캔·재빌드 패치 | Trivy·Grype 로 CVE 를 찾고 베이스 이미지 교체·재빌드로 고치는 운영 | [이미지 속 소프트웨어 취약점](../../08_cloud/book/container-security/07-01.이미지 속 소프트웨어 취약점 — CVE부터 스캔 운영까지.md) |
| IaC·불변 인프라 | 서버를 고치지 않고 코드로 다시 만드는 운영 방식 | [How to Manage Your Infrastructure as Code](../../07_devops/book/fdsd_fundamentals-devops/02-01.How to Manage Your Infrastructure as Code.md) |
| 멱등 부트스트랩 | 여러 번 돌려도 같은 상태가 되게, 상태를 확인한 뒤 구성하는 설치 스크립트 | [How to Manage Your Infrastructure as Code](../../07_devops/book/fdsd_fundamentals-devops/02-01.How to Manage Your Infrastructure as Code.md) (일부: IaC 도구 비교표의 멱등성 행, 상태 확인 뒤 구성하는 스크립트 예 없음) |



## 자료와 실습

- 자료:
  - [Forgejo Actions](https://forgejo.org/docs/latest/user/actions/)·[Forgejo Runner](https://code.forgejo.org/forgejo/runner): 워크플로 문법과 Runner 등록·실행 방식입니다.
  - [OCI Image Spec](https://github.com/opencontainers/image-spec)·[OCI Distribution Spec](https://github.com/opencontainers/distribution-spec): 이미지 형식과 레지스트리 API 표준입니다.
  - [Docker Build](https://docs.docker.com/build/)·[BuildKit](https://github.com/moby/buildkit): 빌드 캐시와 cache mount 동작입니다.
  - [SLSA](https://slsa.dev/)·[Syft](https://github.com/anchore/syft): 빌드 출처 증명과 SBOM 생성입니다.
  - [Trivy](https://trivy.dev/)·[Cosign](https://docs.sigstore.dev/cosign/overview/): 이미지 취약점 검사와 서명입니다.
  - [uv](https://docs.astral.sh/uv/): Python 의존성을 lockfile 로 고정하는 도구입니다.
- 실습:
  - 프로젝트: Private CI Platform, 목표는 빈 Linux 서버에서 CI/CD 환경을 자동으로 다시 짓는 것입니다.
  - Phase 1~2: Forgejo 설치·저장소·권한·Webhook 다음 Runner 등록, Docker Job 실행, 동시 실행 제한입니다. Job 실패와 Runner 재시작도 시험합니다.
  - Phase 3~4: Go·Node.js·Python 빌드 이미지에 의존성을 미리 넣고 레이어 캐시를 적용합니다. Forgejo 레지스트리에 push·pull 하고 digest 로 배포합니다.
  - Phase 5~6: Trivy·Syft·Cosign 으로 검사·SBOM·서명을 하고 CVE 가 나오면 재빌드합니다. Ansible·Shell 로 설치와 백업·복구를 자동화합니다. 완료: 빈 서버에서 재구축이 됩니다.
  - Phase 7: Job 실행 시간·성공률, 레지스트리 용량, 이미지 pull 지연, Runner CPU·메모리, 큐 대기 시간, CVE 수를 잽니다.
  - 장애 실험: 레지스트리 중단, Runner 강제 종료, 같은 워크플로 동시 10개, 태그 변경 뒤 재현, lockfile 은 같고 빌드 이미지만 다를 때 결과를 봅니다.



## 경고

- ⚠ 원인 미확인: 대화 속 이미지 pull 실패를 Docker Hub rate limit 으로 추정했지만, 리포트도 원인은 확인되지 않았다고 적습니다.
- ⚠ 레지스트리 비교표: Forgejo Registry 의 패키지 지원 범위는 리포트도 "확인 필요" 로 둡니다. Harbor·Nexus 와의 운영 복잡도 비교도 근거 없는 일반론입니다.
- ⚠ cache mount 예시: Dockerfile 예시는 cache mount 를 쓰는 `RUN` 에서 `pip install uv` 와 `uv sync --frozen --no-dev` 를 함께 실행합니다. 이 구성이 재현 가능한지는 리포트도 보장하지 않는다고 적습니다.
- ⚠ 멱등 예시: `docker ps -a … | grep -qx forgejo` 로 이름만 확인하는 스크립트는 리포트가 "단순 예시" 라고 밝힙니다. 실제로는 설정·버전·볼륨·네트워크까지 검증해야 합니다.
- ⚠ DinD 격리: DinD 가 호스트 엔진과 "논리적으로 분리" 된다는 말은 privileged 로 띄우면 격리가 약해진다는 단서와 함께 읽어야 합니다.
- ⚠ 우선순위표: "더 볼 도구" 의 높음·중간 판정은 리포트 의견이고 근거가 없습니다.
- ⚠ 개인 정보 정리: 대화 속 프로젝트 이름이 든 `uv sync` 명령과 패키지 이름은 `<그룹>` 으로 바꿨습니다. 이미지 링크와 링크 끝의 유입 추적 매개변수는 버렸습니다.
