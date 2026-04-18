# Git Provider 문서

문서가 프로젝트 루트 `docs/` 디렉토리로 이동했다.

## 프로젝트 리뷰

| 문서 | 설명 |
|------|------|
| [architecture.md](./architecture.md) | 프로젝트 목적, 전체 아키텍처, 이벤트 흐름, 빌드/배포 |
| [go-patterns.md](./go-patterns.md) | Go 문법, 디자인 패턴, 동시성, 에러 처리 (코드 예시 포함) |

## 도메인별 문서

```
docs/
├── Architecture/    # 전체 아키텍처, 서비스 간 통신
├── Provider/        # Provider 추상화 (GitHub/GitLab/Bitbucket)
├── Repository/      # Repository CRUD
├── Branch/          # Branch 비교/분석/정리
├── Contents/        # 코드 브라우징 (파일 트리, 내용 조회)
├── MergeRequest/    # PR/MR 라이프사이클
├── CICD/            # 파이프라인, 빌드, Jenkins
├── Workflow/        # E2E 워크플로우 오케스트레이션
└── README.md        # 전체 인덱스
```

각 도메인 폴더에 api-design, usecase-model, review, test 문서가 있다.
