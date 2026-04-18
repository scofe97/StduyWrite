# 04-nexus: Nexus Repository Manager

Sonatype Nexus Repository Manager 3 학습 프로젝트. Docker 실습 중심으로, 아티팩트 관리부터 프로덕션 운영 패턴까지 다룬다.

## 챕터 목록

| Ch | 디렉토리 | 제목 | 핵심 질문 |
|----|----------|------|-----------|
| 01 | `01-artifact-management-fundamentals` | 아티팩트 관리의 기초 | JAR를 슬랙에 올려서 공유하면 안 되는 이유는? |
| 02 | `02-installation-deployment` | 설치와 배포 환경 | VM/Docker/K8s 중 어디에 띄워야 하며 그 이유는? |
| 03 | `03-repository-formats` | 리포지토리 포맷과 구성 | 20개 넘는 포맷 중 실무에서 꼭 알아야 할 것은? |
| 04 | `04-proxy-and-caching` | 프록시와 캐싱 전략 | 외부 레지스트리 다운 시 빌드가 멈추지 않으려면? |
| 05 | `05-rest-api-and-web-integration` | REST API와 웹 연동 | 커스텀 웹 UI에서 파일 검색/업로드/다운로드하려면? |
| 06 | `06-access-control` | 접근 제어와 인증 | 개발팀은 올리고 QA팀은 읽기만 가능하게 하려면? |
| 07 | `07-ci-cd-integration` | CI/CD 파이프라인 연동 | Jenkins에서 빌드 아티팩트를 자동으로 올리려면? |
| 08 | `08-docker-registry` | Docker Registry로서의 Nexus | 사내 Docker 이미지 저장소를 Nexus로 통합할 수 있는가? |
| 09 | `09-cleanup-and-storage` | 정리 정책과 스토리지 관리 | 디스크 가득 차기 전에 자동 정리하려면? |
| 10 | `10-backup-and-upgrade` | 백업, 복구, 업그레이드 | 서버를 날렸을 때 1시간 안에 복구할 수 있는가? |
| 11 | `11-monitoring-and-troubleshooting` | 모니터링과 트러블슈팅 | Nexus가 느려졌을 때 어디를 봐야 하는가? |
| 12 | `12-production-patterns` | 프로덕션 운영 패턴 | 10명 팀과 500명 조직의 운영 전략 차이는? |

## Quick Start

```bash
cd practice/
docker compose up -d

# 초기 비밀번호 확인 후 admin123으로 변경
docker exec nexus cat /nexus-data/admin.password

# 리포지토리 자동 생성
chmod +x nexus-config/setup-repos.sh
./nexus-config/setup-repos.sh
```

## 디렉토리 구조

```
04-nexus/
├── README.md                   # 이 파일
├── learning/                   # 학습 문서 (12챕터)
│   ├── 01-artifact-management-fundamentals/
│   │   ├── LEARN.md
│   │   └── INVESTIGATE.md
│   ├── ...
│   └── 12-production-patterns/
└── practice/                   # 실습 환경
    ├── docker-compose.yml      # Nexus + nginx
    ├── docker-compose.ci.yml   # Jenkins 연동
    ├── nexus-config/           # 설정, 초기화 스크립트
    ├── nginx/                  # Reverse proxy
    ├── monitoring/             # Prometheus + Grafana
    ├── web-file-manager/       # REST API 기반 파일 관리 UI
    ├── sample-projects/        # Maven/npm/Docker 샘플
    ├── scripts/                # 백업/복구/정리
    └── http/                   # REST API 테스트 (.http)
```

## 교차 참조

| 챕터 | 참조 대상 | 이유 |
|------|-----------|------|
| Ch02 | 01-docker Ch06 (Dockerfile) | Docker volume, 이미지 튜닝 |
| Ch07 | 01-jenkins Ch04 (Pipeline) | Jenkinsfile에서 Nexus publish |
| Ch07 | 02-cicd-patterns Ch02 (Pipeline as Code) | 아티팩트 저장소 통합 패턴 |
| Ch08 | 01-docker Ch05 (Lifecycle) | Docker push/pull, registry 개념 |
| Ch11 | 03-devops-fundamentals Ch10 (Monitoring) | Prometheus/Grafana 기초 |

## 기술 스택

- Nexus Repository Manager 3.75.0
- Docker Compose (Nexus + nginx + Prometheus + Grafana)
- REST API v1 (curl, IntelliJ HTTP Client)
- 순수 HTML/JS (web-file-manager)
