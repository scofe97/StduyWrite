# 인프라 · GitOps · 관측성 (tps_manifest) — 작업 정리

> 저장소: `tps_manifest` · 기간 2024 ~ 2026-05
> 스택: Ansible · Kubespray · ArgoCD · Helm · Kubernetes · Grafana · Loki · Alloy · Prometheus · Jenkins · Groovy

운영 자체를 코드와 함께 형상관리한다는 기준으로 작업했습니다. 초기에는 Ansible 로 STG 환경의 VM CI/CD 와 쿠버네티스 클러스터 구축을 자동화했고, 이후 애플리케이션 모듈의 Helm 차트, 관측성 스택 통합, 305P Jenkins GitOps 부트스트랩, 운영 대시보드 코드화로 이어졌습니다.

> 참고: 아래 Ansible 섹션은 본인이 주도한 작업이지만, 저장소 사정으로 일부 커밋이 다른 팀원(장성필·이찬웅) 이름으로 올라가 있습니다. 코드 author 로는 본인 기여가 드러나지 않으므로 면접에서 구두로 설명할 수 있도록 별도 기록합니다.

---

## STG 환경 VM CI/CD 자동화 (Ansible)

> 2024 · 본인 주도 (커밋 author 상이)

3.0.4 STG 환경을 Ansible 로 프로비저닝하고 무중단 배포까지 자동화했습니다. 인벤토리는 미들웨어 8대(HAProxy·Jenkins·SonarQube·GitLab·MariaDB·Nexus·Harbor·Storage)와 애플리케이션 3대로 구성했습니다.

컴포넌트 설치 playbook 을 25종 작성했습니다(haproxy·nginx·nfs server/client·mariadb·jenkins·gitlab·nexus·harbor·sonarqube·minio·openldap·docker·jdk·go·node 등). 핵심은 통합 CI/CD playbook 입니다. 백엔드는 git clone → gradlew 모듈 빌드(`-Pprofile -x test`) → JAR 배포 → systemd 서비스 생성 후 실행 상태에 따라 start/restart 하는 흐름으로, 여러 Spring Boot 모듈(api-gateway·cloud-config 등)을 import_tasks 와 vars 로 파라미터화해 한 playbook 에서 처리했습니다. 프런트엔드는 clone → yarn berry 설치·빌드 → nginx 설정·배포로 묶었습니다. role(cicd·gitlab·jenkins·mariadb)로 재사용 단위를 분리하고 secret 은 vars 로 격리했습니다.

## 쿠버네티스 클러스터 구축 (Kubespray)

> 2024 ~ 2025 · 본인 주도 (커밋 author 상이)

개발(DEV) 환경 쿠버네티스 클러스터를 Kubespray 로 구축했습니다. 인벤토리는 master 3대 + worker 7대 + etcd 3 멤버 구성이고, Kubespray 를 v1.28.6 과 v1.30.4 두 버전으로 운용해 클러스터 생성·스케일·업그레이드를 코드로 관리했습니다. 이 VM·K8s 자동화 경험이 이후 GitOps(ArgoCD/Helm) 기반 운영으로 넘어가는 토대가 됐습니다.

---

## 관측성 스택 통합

> 2026-03

Grafana 가 loki-stack 과 kube-prometheus-stack 두 곳에 따로 떠 있어 대시보드와 데이터소스가 분산돼 있었습니다. loki-stack 의 Grafana 를 비활성화하고 kube-prometheus-stack 의 Grafana 에 Loki datasource 를 붙여 로그·메트릭을 한 화면으로 통합했습니다. 로그 수집기 Promtail 이 EOL 되어 Grafana Alloy 로 전환해 ArgoCD Application 으로 등록했고, readOnlyRootFilesystem 환경의 /tmp 쓰기 오류를 해결했습니다. 이미지 태그·차트 버전을 클러스터 실버전과 정합하고, 폐쇄망 대비 Nexus 프록시 레지스트리 설정을 적용했습니다.

## 305P Jenkins app-of-apps GitOps 부트스트랩

> 2026-04

운영 환경(PPP)의 Jenkins 컨트롤러·플러그인·콜백이 수기 절차로 관리되던 것을 코드로 옮겼습니다. trb-oss app-of-apps 부트스트랩과 Jenkins 컨트롤러 StatefulSet 을 한 번에 구성하고(단일 커밋 +1,246줄), Job 완료 이벤트를 메시지 브로커로 발행하는 webhook listener(Groovy 328줄)를 자동 설치하도록 묶었습니다. 폐쇄망 대비로 플러그인 해석 고정·Update Center 비활성·기존 home 플러그인 재사용을 적용했고, PVC storageClass 보존·releaseName 고정·이미지 소스 정합 등 ArgoCD sync 안정화 가드레일을 두었습니다. webhook listener 는 ESC 바이트 이스케이프·failureReason 새니타이즈·cluster 내부 DNS 전환으로 견고화했습니다.

## 305P 운영 · Outbox 모니터링 대시보드

> 2026-05

운영 대시보드도 코드로 형상관리했습니다. operator/executor 의 ERROR 로그 대시보드(monitoring-error-logs)는 LogQL 로 trb-app 네임스페이스의 컨테이너를 타겟하고 ANSI 이스케이프·대괄호 ERROR 패턴을 매칭합니다. message-lib 의 Outbox 메트릭 대시보드(monitoring-outbox, IGMU-1040)는 published/failed/dead/pending 을 7패널로 시각화합니다. 두 차트 모두 Grafana sidecar 가 grafana_dashboard 라벨로 자동 import 하고, trb-mgm app-of-apps 에 Application 으로 와이어링했습니다.

## 애플리케이션 모듈 Helm 차트 · 배포 파이프라인

> 2024-05 ~ 2024-08

신규 모듈이 운영에 올라가도록 Helm 차트와 배포 파이프라인을 직접 깔았습니다. sse 모듈(Server-Sent Events, Go)의 Helm 차트 전체(deployment/service/ingress/hpa/pdb/pvc/servicemonitor)와 Jenkinsfile 을 작성하고 PVC·볼륨·로그 경로를 구성했습니다. notificator·scheduler 모듈의 Dockerfile·Helm 차트를 추가하고, ppln-logging-api 볼륨과 공통 CI(Docker Credential, react-app Dockerfile)를 다뤘습니다.
