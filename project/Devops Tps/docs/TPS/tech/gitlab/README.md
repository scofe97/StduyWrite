# GitLab API 스펙

TPS Pipeline API의 GitLab 연동 API 서비스입니다.

## 프로젝트 정보

| 항목 | 값 |
|------|-----|
| **프로젝트** | pipeline-api |
| **포트** | 8085 |
| **컨텍스트 경로** | `/pipeline/api` |
| **API 버전** | V2 (운영), V3 (개발 중) |

## API 클라이언트 구성

| 방식 | 클래스 | 용도 |
|------|--------|------|
| **Feign** | `GitLabFeignClient` | 대부분의 REST API 호출 |
| **WebClient** | `GitLabWebClient` | Merge Request 생성 (비동기) |
| **GitLab4j** | `GitLabApiComponent` | 고수준 API 작업 |

## 도메인별 API 문서

| 도메인 | 문서 | 설명 |
|--------|------|------|
| 사용자 | [01-user-api.md](./01-user-api.md) | 사용자 생성/수정/삭제, 활성화/차단 |
| 그룹 | [02-group-api.md](./02-group-api.md) | 그룹 관리, 멤버십 |
| 프로젝트 | [03-project-api.md](./03-project-api.md) | 프로젝트/저장소 관리 |
| 브랜치 | [04-branch-api.md](./04-branch-api.md) | 브랜치 생성/삭제/보호 |
| 병합 | [05-merge-api.md](./05-merge-api.md) | Merge Request 관리 |
| 저장소 | [06-repository-api.md](./06-repository-api.md) | 파일/트리 관리 |
| 변경사항 | [07-changes-api.md](./07-changes-api.md) | 커밋/diff 추적 |
| 클론 | [08-clone-api.md](./08-clone-api.md) | 소스 다운로드 |

## 외부 시스템 연계

- **PMS**: 브랜치 생성/삭제, 업무코드 기반 저장소 관리
- **Workflow Engine**: 병합 요청, 변경파일 이력, 롤백
- **공통 모듈**: 사용자 정보 동기화

## 인증 방식

```
Authorization: {gitlab-token}
userId: {request-user-id}
```
