# Spec-Driven Development 워크플로우 조사 보고서

## 개요

DevOps 플랫폼 개발 과정에서 Figma 디자인, Jira 요구사항, DB 스키마를 기반으로 한 효율적인 개발 워크플로우를 설계하기 위한 조사 결과입니다.

---

## 1. 워크플로우 도구 비교: n8n vs Claude Skill

### 1.1 n8n 기반 워크플로우

**적합한 경우:**
- 외부 서비스 연동이 많은 경우 (Slack, GitHub, Jira, 데이터베이스 등)
- 스케줄링이나 웹훅 트리거가 필요한 경우
- 워크플로우를 시각적으로 관리하고 팀과 공유해야 할 때
- 장기 실행되는 백그라운드 작업
- Claude API를 여러 노드 사이에 끼워넣어 부분적으로 AI를 활용할 때

**장점:** 상태 관리, 에러 핸들링, 재시도 로직이 내장되어 있고, 실행 이력 추적이 용이함

### 1.2 Skill 기반 워크플로우 (Claude Computer Use)

**적합한 경우:**
- 파일 생성/변환 중심의 작업 (문서, 코드, 스프레드시트 등)
- 대화형으로 요구사항을 조정해가며 진행하는 작업
- 복잡한 판단이나 맥락 이해가 필요한 작업
- 일회성이거나 ad-hoc 성격의 작업
- 코드 분석, 리팩토링, 문서화 같은 개발 태스크

**장점:** 자연어로 복잡한 요구사항 전달 가능, 중간 결과 확인하며 방향 수정 가능

### 1.3 비교 요약

| 기준 | n8n | Skill |
|------|-----|-------|
| 반복 실행 빈도 | 높음 (정기적) | 낮음 (필요시) |
| 외부 API 연동 | 많음 | 적음 |
| 인간 개입 필요 | 최소화 | 빈번 |
| 실행 환경 | 서버에서 자율 실행 | 대화 세션 내 |
| 결과물 형태 | 데이터 파이프라인 | 파일/문서 |

---

## 2. 데이터 조회 방식 비교: MCP vs CLI

### 2.1 선택지 비교

| 관점 | MCP 서버 | CLI 개발 | n8n 네이티브 노드 |
|------|----------|----------|------------------|
| AI 통합 | ◎ 네이티브 | ○ bash로 호출 | △ 별도 레이어 |
| 개발 비용 | 중간 | 높음 | 낮음 |
| 유지보수 | MCP 스펙 따라감 | 직접 관리 | n8n이 관리 |
| 유연성 | 중간 | 높음 | 낮음 |
| 재사용성 | Claude 생태계 전체 | 팀 내부 | n8n 내부 |

### 2.2 CLI가 우위인 핵심 이유

#### 토큰 효율성

**Figma API 원본 응답** (전체 파일 조회 시):
```json
{
  "document": {
    "children": [
      // 수백~수천 개의 노드
      // 모든 스타일, 제약조건, 레이아웃 정보
      // 사용하지 않는 컴포넌트까지 전부 포함
    ]
  }
}
// 쉽게 수만 토큰
```

**CLI로 튜닝한 출력**:
```json
{
  "screen_name": "사용자 대시보드",
  "components": [
    {"type": "table", "columns": ["이름", "상태", "일자"], "actions": ["수정", "삭제"]},
    {"type": "button", "label": "신규 등록", "variant": "primary"}
  ],
  "api_hints": {
    "list_endpoint": true,
    "crud_operations": ["create", "read", "update", "delete"]
  }
}
// 수백 토큰
```

**토큰 차이: 10~100배**

#### 정확한 전처리

```bash
# CLI는 "개발에 필요한 정보"만 추출하도록 튜닝 가능
figma-cli extract DEV-123 \
  --output-format=dev-spec \
  --include=components,interactions,design-tokens \
  --exclude=raw-vectors,constraints,plugin-data
```

MCP 범용 서버는 이런 도메인 특화 전처리가 없음.

### 2.3 MCP의 실제 한계

기존 MCP 서버들은 대부분 API 프록시 수준이며, "요구사항 추출"이나 "개발 스펙 변환" 같은 도메인 로직이 없음.

```typescript
// 일반적인 Figma MCP 도구 - 그냥 API 래퍼
tools: [
  { name: "get_file", params: { file_key } },
  { name: "get_node", params: { file_key, node_id } }
]
```

### 2.4 CLI가 더 나은 경우

1. MCP 서버가 없는 내부 시스템 (사내 API, 레거시 시스템)
2. 출력 포맷을 정밀하게 제어해야 할 때
3. Claude 외의 환경에서도 동일하게 사용해야 할 때 (Jenkins, GitHub Actions 등)
4. 오프라인/에어갭 환경에서 실행해야 할 때

### 2.5 결론

**CLI 직접 개발이 적합함**

| 관점 | CLI | MCP |
|------|-----|-----|
| 토큰 효율 | ◎ 필요한 것만 | △ 범용적 응답 |
| 도메인 튜닝 | ◎ 완전 제어 | △ 직접 구현 필요 |
| 개발 복잡도 | 단순 (Go/Python) | 프로토콜 오버헤드 |
| 재사용성 | CI/CD, 스크립트 등 | Claude 전용 |
| 디버깅 | 터미널에서 바로 | MCP Inspector 필요 |

---

## 3. 제안 워크플로우: 명세서 중심 개발

### 3.1 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  n8n (데이터 수집 레이어)                                     │
│  - Figma API → 화면 스펙                                     │
│  - DB 조회 → 스키마 정보                                      │
│  - Jira → 요구사항                                           │
│  - 주기적/수동 실행                                           │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  명세서 (Single Source of Truth)                             │
│  - 자동 생성된 문서를 인간이 검토/편집                          │
│  - Git 버전 관리                                             │
│  - 변경 이력 추적                                             │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude (구현)                                                │
│  - 명세서만 보고 백엔드/프론트엔드 개발                         │
│  - 재현 가능한 결과                                           │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 이 접근의 강점

| 관점 | 효과 |
|------|------|
| 토큰 | Figma 원본 대신 정제된 명세서만 전달 |
| 품질 | 명세서 단계에서 검토 후 개발 착수 |
| 추적 | Git diff로 "뭐가 바뀌었는지" 명확 |
| 재현 | 명세서 v1.2 → 항상 동일한 코드 생성 가능 |
| 분업 | 인간은 명세 검토, Claude는 구현 |

### 3.3 디렉토리 구조

```
project-specs/
├── screens/                    # Figma에서 추출
│   ├── dashboard.yaml
│   ├── user-list.yaml
│   └── settings.yaml
├── database/                   # DB에서 추출
│   ├── schema.yaml
│   └── relationships.yaml
├── requirements/               # Jira에서 추출 + 수동 보완
│   ├── DEV-123.yaml
│   └── DEV-124.yaml
├── specs/                      # 통합 명세서 (핵심)
│   ├── DEV-123-spec.yaml       # 화면 + DB + 요구사항 통합
│   └── changelog.md            # 변경 이력
└── generated/                  # Claude가 생성한 코드
    ├── backend/
    └── frontend/
```

### 3.4 명세서 포맷 예시

```yaml
# specs/DEV-123-spec.yaml
version: "1.2"
updated_at: "2025-01-26"
jira_key: "DEV-123"

# 1. 요구사항 요약
requirement:
  summary: "사용자 목록 화면 개발"
  acceptance_criteria:
    - 사용자 목록을 페이징하여 조회
    - 이름/상태로 필터링 가능
    - 행 클릭 시 상세 화면으로 이동

# 2. 화면 스펙 (Figma에서 추출)
screen:
  name: "사용자 목록"
  layout: "sidebar-main"
  components:
    - type: search-filter
      fields:
        - { name: "name", type: "text", placeholder: "이름 검색" }
        - { name: "status", type: "select", options: ["전체", "활성", "비활성"] }
    - type: data-table
      columns:
        - { key: "name", label: "이름", sortable: true }
        - { key: "email", label: "이메일" }
        - { key: "status", label: "상태", type: "badge" }
        - { key: "createdAt", label: "가입일", type: "date" }
      actions:
        row_click: "navigate:/users/{id}"
      pagination: { default_size: 20, options: [10, 20, 50] }

# 3. DB 스펙 (기존 테이블 참조)
database:
  primary_table: "users"
  columns_used:
    - { name: "id", type: "bigint" }
    - { name: "name", type: "varchar(100)" }
    - { name: "email", type: "varchar(255)" }
    - { name: "status", type: "enum('ACTIVE','INACTIVE')" }
    - { name: "created_at", type: "datetime" }
  new_columns: []
  indexes_needed:
    - { columns: ["name"], type: "btree" }

# 4. API 스펙
api:
  endpoints:
    - method: GET
      path: "/api/v1/users"
      query_params:
        - { name: "name", type: "string", required: false }
        - { name: "status", type: "string", required: false }
        - { name: "page", type: "int", default: 0 }
        - { name: "size", type: "int", default: 20 }
      response:
        type: "Page<UserListResponse>"
```

### 3.5 변경 추적 워크플로우

```bash
# 1. Figma 변경 감지 및 추출 (n8n 또는 수동)
$ figma-cli extract-spec --file=XXX --frame="사용자 목록" \
    --output=screens/user-list.yaml

# 2. 이전 버전과 비교
$ diff screens/user-list.yaml.bak screens/user-list.yaml
> + - { key: "role", label: "역할", type: "badge" }  # 컬럼 추가됨

# 3. 변경사항을 명세서에 반영
$ spec-cli update DEV-123 --sync-screen --bump-version

# 4. changelog 자동 기록
$ cat specs/changelog.md
## DEV-123 v1.2 → v1.3 (2025-01-26)
- [screen] 테이블에 '역할' 컬럼 추가
- [database] users.role 컬럼 참조 필요
```

### 3.6 Claude에게 개발 요청 예시

```markdown
## 개발 요청

첨부된 명세서(DEV-123-spec.yaml v1.3)를 기반으로 개발해주세요.

### 변경사항 (v1.2 → v1.3)
- 테이블에 '역할' 컬럼 추가

### 생성 요청
1. Backend: UserController, UserService, UserMapper 수정
2. Frontend: UserListPage 컴포넌트 수정

### 컨벤션
- Spring Boot 3.x + MyBatis
- React + Ant Design
```

---

## 4. 업계 사례: Spec-Driven Development (SDD)

### 4.1 개념 정의

Spec-Driven Development는 "코드를 먼저 짜고 문서를 나중에 쓰는" 대신, **스펙을 먼저 작성하고 이를 AI 에이전트가 코드 생성, 테스트, 검증에 사용하는 source of truth로 삼는 방식**입니다.

> "In spec-driven development, you start with a spec. This is a contract for how your code should behave and becomes the source of truth your tools and AI agents use to generate, test, and validate code."
> — GitHub Blog (2025.09)

### 4.2 주요 도구 및 사례

#### GitHub Spec-Kit (2025년 9월 오픈소스)

**워크플로우:**
```
Specify → Plan → Tasks → Implement
```

**핵심 특징:**
- 명세서가 변경되면 영향받는 구현 계획이 자동으로 업데이트
- 사용자 스토리가 수정되면 해당 API 엔드포인트가 재생성
- GitHub Copilot, Claude Code, Gemini CLI와 통합 지원

#### Amazon Kiro

- AWS에서 개발한 spec-driven development IDE
- 사전 정의된 워크플로우 제공

#### JetBrains Junie

- JetBrains의 AI 코딩 에이전트
- spec-driven 접근 방식 지원
- `requirements.md → plan.md → tasks.md` 흐름

### 4.3 실무자 경험담

> "제가 매일 spec-driven development를 쓰고 있는데, 가장 큰 깨달음은 AI 모델이 아니라 **도구 전환에도 살아남는 단일하고 지속적인 스펙**을 갖는 것이었습니다. 제 워크플로우에서 스펙은 IDE 외부에 있고 레포지토리와 함께 버전 관리됩니다."
> — Microsoft Developer Blog 댓글

### 4.4 Thoughtworks 분석 (2025년 12월)

> "SDD의 핵심은 vibe coding을 넘어 **설계와 구현 단계를 분리**하는 것입니다. 계획 단계에서 요구사항을 AI 코딩 에이전트로 분석하여 설계 및 구현 계획을 생성합니다. 보통 이 요구사항 명세는 여러 Markdown 파일로 형식화됩니다. 이 명세를 검토하고 검증하는 것은 일반적으로 **인간이 개입하는 반복 과정**입니다."

### 4.5 SDD의 장점

| 장점 | 설명 |
|------|------|
| 조기 오류 방지 | 요구사항을 상세히 미리 캡처하여 오해 방지 |
| 살아있는 문서 | 명세서가 프로젝트와 함께 진화하는 버전 관리 문서 |
| 일관된 품질 | 주니어/시니어 모두 동일한 흐름 → 코드 품질 일관성 |
| 재현 가능성 | 동일 명세 → 동일 결과 |

> "주니어 개발자도 시니어 개발자와 동일한 spec → plan → tasks → implement 흐름을 따르기 때문에 코드 품질이 일관되게 유지됩니다."
> — Zencoder Docs

---

## 5. 제안 워크플로우 vs 업계 표준 비교

| 구분 | 업계 표준 (Spec-Kit 등) | 제안 방식 |
|------|------------------------|-----------|
| 스펙 생성 | AI가 요구사항에서 생성 | **n8n이 Figma/DB에서 자동 수집** |
| 인간 역할 | 스펙 검토/수정 | 동일 |
| 구현 | AI가 스펙 기반 코드 생성 | 동일 |
| 차별점 | - | **디자인 시스템과 직접 연동** |

**제안 방식의 강점:** 업계 표준은 "요구사항 → 스펙"을 AI가 생성하지만, 제안 방식은 **Figma/DB라는 실제 소스에서 직접 추출**하므로 더 정확함.

---

## 6. 개선된 최종 워크플로우

### 6.1 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│  n8n (데이터 수집)                                           │
│  - Figma API 호출 → 원시 JSON                               │
│  - DB 스키마 조회 → DDL/메타데이터                           │
│  - Jira API → 요구사항                                      │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude (1차): 원시 데이터 → 정형화된 명세서 초안 생성          │
│  (선택적 단계)                                               │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  인간: 명세서 검토/수정 ← 핵심 판단 포인트                     │
│  - 요구사항 정확성 확인                                       │
│  - 기술적 결정 (API 설계, DB 변경 등)                         │
│  - Git 커밋으로 버전 관리                                    │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude (2차): 확정된 명세서 → 코드 생성                      │
│  - 백엔드: Controller, Service, Mapper                      │
│  - 프론트엔드: React 컴포넌트                                 │
│  - 테스트 코드                                               │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 권장 파일 구조 (Spec-Kit 스타일 차용)

```
project/
├── .spec/                      # 명세서 홈
│   ├── constitution.md         # 불변 원칙 (코딩 컨벤션, 아키텍처)
│   ├── sources/                # n8n이 수집한 원시 데이터
│   │   ├── figma-raw/
│   │   └── db-schema/
│   └── specs/                  # 정형화된 명세서
│       ├── DEV-123/
│       │   ├── requirement.md  # 요구사항
│       │   ├── screen.md       # 화면 스펙
│       │   ├── api.md          # API 설계
│       │   └── tasks.md        # 구현 태스크 목록
│       └── changelog.md
├── backend/
└── frontend/
```

### 6.3 CLI 개발 우선순위

```
Phase 1: 정보 추출 CLI
├── figma-cli extract-spec   # 화면 → YAML
├── db-cli dump-schema       # DB → YAML  
└── jira-cli get-requirement # Jira → YAML

Phase 2: 명세서 관리 CLI
├── spec-cli init            # 새 명세서 생성
├── spec-cli merge           # 화면 + DB + Jira 통합
├── spec-cli diff            # 버전 간 비교
└── spec-cli changelog       # 변경 이력 생성

Phase 3: 자동화 (선택)
├── watch 모드 (Figma 변경 감지)
└── n8n 연동 (Jira 이슈 생성 시 자동 초기화)
```

---

## 7. 결론 및 권장사항

### 7.1 워크플로우 평가

| 평가 항목 | 결과 |
|----------|------|
| 흐름 타당성 | ◎ 업계 트렌드(SDD)와 정확히 일치 |
| 차별점 | Figma/DB 직접 연동으로 스펙 정확도 ↑ |
| 사례 존재 | GitHub Spec-Kit, Amazon Kiro, JetBrains Junie 등 |
| 실용성 | ◎ 토큰 절약 + 품질 관리 + 추적성 확보 |

### 7.2 핵심 권장사항

1. **n8n은 데이터 수집에만 집중**: Figma/DB/Jira에서 원시 데이터 수집
2. **CLI로 도메인 특화 추출**: 범용 MCP 대신 개발에 필요한 정보만 추출하는 CLI 개발
3. **명세서가 Single Source of Truth**: 모든 개발은 검토된 명세서 기반으로 진행
4. **인간 검토 단계 유지**: AI가 생성한 것도 반드시 인간이 검토 후 확정
5. **Git으로 버전 관리**: 명세서 변경 이력 추적

### 7.3 다음 단계

1. figma-cli 프로토타입 개발
2. 명세서 YAML 스키마 확정
3. n8n 워크플로우 설계
4. constitution.md (코딩 컨벤션) 작성

---

## 참고 자료

- [GitHub Spec-Kit](https://github.com/github/spec-kit)
- [GitHub Blog: Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Thoughtworks: Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: Understanding Spec-Driven-Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [JetBrains Junie: Spec-Driven Approach](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/)
- [Figma Dev Mode](https://www.figma.com/dev-mode/)
- [Figma MCP Server](https://help.figma.com/hc/en-us/articles/36189347137047)
