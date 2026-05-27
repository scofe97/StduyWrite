# Enterprise Project Name

## Overview
[프로젝트의 목적, 대상 사용자, 핵심 가치 제안]

---

## Team & Ownership
- **Tech Lead**: [이름]
- **Domain**: [도메인, 예: 결제 시스템]
- **Stakeholders**: [이해관계자]

---

## Tech Stack

### Core
| 영역 | 기술 | 버전 |
|------|------|------|
| Language | TypeScript | 5.x |
| Frontend | React | 18.x |
| Backend | Node.js/Express | 20.x |
| Database | PostgreSQL | 15.x |
| Cache | Redis | 7.x |

### DevOps
| 영역 | 기술 |
|------|------|
| CI/CD | GitHub Actions |
| Container | Docker |
| Cloud | AWS |
| Monitoring | Datadog |

---

## Architecture

### System Overview
```
┌─────────────────────────────────────────────────────┐
│                    Client Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Web App   │  │ Mobile App  │  │   Admin     │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    API Gateway                       │
└─────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ User Service│  │Order Service│  │Payment Svc  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Project Structure
```
src/
├── api/              # API 라우트
│   └── v1/
├── services/         # 비즈니스 로직
├── repositories/     # 데이터 접근
├── models/           # 도메인 모델
├── middleware/       # 미들웨어
├── utils/            # 유틸리티
├── config/           # 설정
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

### Key Patterns
- **Repository Pattern**: 데이터 접근 추상화
- **Service Layer**: 비즈니스 로직 캡슐화
- **Dependency Injection**: 테스트 용이성
- **Event-Driven**: 느슨한 결합

---

## Architecture Decision Records (ADR)

### ADR-001: REST vs GraphQL
- **결정**: REST API
- **이유**: 팀 경험, 캐싱 용이성
- **날짜**: 2024-01-15

### ADR-002: State Management
- **결정**: Zustand
- **이유**: 단순성, 번들 크기
- **날짜**: 2024-01-20

---

## Domain Model

### Core Entities
| Entity | 설명 | 주요 속성 |
|--------|------|----------|
| User | 사용자 | id, email, role |
| Order | 주문 | id, userId, status, items |
| Product | 상품 | id, name, price, stock |
| Payment | 결제 | id, orderId, amount, status |

### Business Rules
1. **주문 생성**: 재고 확인 → 주문 생성 → 결제 요청
2. **결제 완료**: 재고 차감 → 주문 상태 업데이트
3. **환불**: 결제일 기준 7일 이내만 가능

---

## API Standards

### Response Format
```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "requestId": "uuid"
  }
}
```

### Error Codes
| 코드 | 의미 |
|------|------|
| E001 | 인증 실패 |
| E002 | 권한 없음 |
| E003 | 리소스 없음 |
| E004 | 유효성 검증 실패 |

---

## Rules

### MUST (Critical)
- [ ] 모든 API에 인증/인가 적용
- [ ] 모든 입력 검증
- [ ] Prepared Statement 사용 (SQL Injection 방지)
- [ ] 민감 정보 암호화
- [ ] 커밋 전 보안 스캔

### MUST NOT (Forbidden)
- [ ] 하드코딩된 시크릿
- [ ] `any` 타입 사용
- [ ] 직접 SQL 문자열 연결
- [ ] 프로덕션 DB 직접 접근
- [ ] Force push to main

### SHOULD (Best Practice)
- [ ] 100% 타입 커버리지
- [ ] 80% 테스트 커버리지
- [ ] API 응답 시간 <200ms
- [ ] 의미 있는 로깅

---

## Security

### Authentication
- JWT 기반 인증
- Access Token: 15분
- Refresh Token: 7일

### Authorization
- RBAC (Role-Based Access Control)
- Roles: admin, user, guest

### Data Protection
- PII 암호화 (AES-256)
- 로그에 민감 정보 제외
- GDPR 준수

---

## Testing Strategy

### Test Pyramid
```
        /\
       /E2E\        (10%)
      /------\
     /Integration\  (30%)
    /------------\
   /   Unit Tests  \ (60%)
  /------------------\
```

### Coverage Goals
| 유형 | 목표 | 현재 |
|------|------|------|
| Unit | 80% | - |
| Integration | 60% | - |
| E2E | Critical Paths | - |

### Test Commands
```bash
npm test              # 단위 테스트
npm run test:int      # 통합 테스트
npm run test:e2e      # E2E 테스트
npm run test:coverage # 커버리지 리포트
```

---

## Deployment

### Environments
| 환경 | URL | 용도 |
|------|-----|------|
| Dev | dev.example.com | 개발 |
| Staging | staging.example.com | QA |
| Production | example.com | 운영 |

### CI/CD Pipeline
```
Push → Lint → Test → Build → Deploy (Staging) → Approval → Deploy (Prod)
```

### Rollback
```bash
# 이전 버전으로 롤백
./scripts/rollback.sh <version>
```

---

## Monitoring & Alerting

### Metrics
- Response Time (P50, P95, P99)
- Error Rate
- Request Rate
- CPU/Memory Usage

### Alerts
| Alert | 조건 | 심각도 |
|-------|------|--------|
| High Error Rate | >5% | Critical |
| High Latency | P95 >500ms | Warning |
| Low Disk Space | <10% | Critical |

---

## Git Workflow

### Branch Strategy
```
main ──────────────────────────────────────→
  │
  └── feature/ABC-123-feature-name
        │
        └── (PR) → code review → merge
```

### Commit Convention
```
<type>(<scope>): <subject>

[optional body]

[optional footer]

Types: feat, fix, refactor, docs, test, chore
Scope: api, auth, order, payment, etc.
```

### PR Template
```markdown
## Summary
[변경 사항 요약]

## Type
- [ ] Feature
- [ ] Bug Fix
- [ ] Refactor

## Test Plan
- [ ] 단위 테스트 추가/수정
- [ ] 통합 테스트 확인
- [ ] 수동 테스트 완료

## Checklist
- [ ] 코드 리뷰 완료
- [ ] 테스트 통과
- [ ] 문서 업데이트
```

---

## Contacts

### On-Call
- **Primary**: [이름] (slack: @name)
- **Secondary**: [이름] (slack: @name)

### Escalation
1. 개발팀 Slack 채널
2. Tech Lead 호출
3. 운영팀 연락
