# Chapter 9. Deployment: AI 애플리케이션 프로덕션 배포

---

### 📌 핵심 요약
> AI 애플리케이션을 프로덕션 환경에 배포하려면 **LLM**, **Vector Store**, **Backend API**의 세 가지 핵심 컴포넌트를 적절히 구성해야 한다. **LangGraph Platform**은 LangGraph 에이전트를 대규모로 배포하고 호스팅하는 관리형 서비스로, 수평적 확장, 내결함성, 실시간 스트리밍, Human-in-the-Loop을 지원한다. **LangSmith**와 통합되어 디버깅, 협업, 테스트, 모니터링이 가능하며, **LangGraph Studio**를 통해 에이전트를 시각적으로 디버깅하고 상호작용할 수 있다.

---

### 🎯 학습 목표
- AI 애플리케이션 배포에 필요한 핵심 서비스들을 이해한다
- Supabase를 Vector Store로 설정하고 사용하는 방법을 안다
- LangGraph Platform의 데이터 모델과 기능을 설명할 수 있다
- LangGraph CLI로 로컬 테스트 후 LangSmith UI에서 배포할 수 있다
- AI 애플리케이션의 보안 모범 사례를 적용할 수 있다

---

### 📖 본문 정리

#### 1. 배포 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────┐
│                    Production Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │     LLM     │    │ Vector Store│    │   Backend API   │ │
│  │   (OpenAI)  │    │  (Supabase) │    │(LangGraph Plat.)│ │
│  └──────┬──────┘    └──────┬──────┘    └────────┬────────┘ │
│         │                  │                     │          │
│         └──────────────────┼─────────────────────┘          │
│                            │                                │
│                    ┌───────▼───────┐                        │
│                    │   LangSmith   │                        │
│                    │  (Monitoring) │                        │
│                    └───────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

##### 필수 환경 변수

```bash
# .env 파일
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

# LangSmith 트레이싱
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=
```

---

#### 2. Vector Store 설정 (Supabase)

Supabase는 PostgreSQL 기반 데이터베이스로, **pgvector** 확장을 통해 벡터 저장 및 유사도 검색을 지원한다.

##### SQL 설정 스크립트

```sql
-- 1. pgvector 확장 활성화
create extension vector;

-- 2. documents 테이블 생성
create table documents (
  id bigserial primary key,
  content text,              -- Document.pageContent
  metadata jsonb,            -- Document.metadata
  embedding vector(1536)     -- OpenAI 임베딩 차원
);

-- 3. 유사도 검색 함수 생성
create function match_documents (
  query_embedding vector(1536),
  match_count int DEFAULT null,
  filter jsonb DEFAULT '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  embedding jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    (embedding::text)::jsonb as embedding,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

##### Python 사용 예시

```python
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
)

vector_store = SupabaseVectorStore(
    embedding=OpenAIEmbeddings(),
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)

# 유사도 검색 테스트
matched_docs = vector_store.similarity_search("What is this document about?")
print(matched_docs[0].page_content)
```

---

#### 3. LangGraph Platform

LangGraph Platform은 LangGraph 에이전트를 **대규모로 배포하고 호스팅**하는 관리형 서비스이다.

##### 핵심 데이터 모델

| 데이터 모델 | 설명 | 용도 |
|------------|------|------|
| **Assistants** | CompiledGraph의 구성된 인스턴스 | 그래프의 인지 아키텍처 추상화, 설정/메타데이터 포함 |
| **Threads** | 실행 그룹의 누적 상태 | 상태 영속화, 체크포인트 저장 |
| **Runs** | 어시스턴트의 호출 | 입력, 설정, 메타데이터로 그래프 실행 |
| **Cron Jobs** | 스케줄 기반 그래프 실행 | 정기적 작업 자동화 |

##### 데이터 모델 관계도

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph Platform                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐         ┌─────────────┐               │
│  │  Assistant  │────────▶│    Run      │               │
│  │ (Graph 설정) │         │  (실행 단위) │               │
│  └─────────────┘         └──────┬──────┘               │
│                                 │                       │
│                          ┌──────▼──────┐               │
│                          │   Thread    │               │
│                          │ (상태 저장)  │               │
│                          └──────┬──────┘               │
│                                 │                       │
│                          ┌──────▼──────┐               │
│                          │ Checkpoint  │               │
│                          │(특정 시점 상태)│               │
│                          └─────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

#### 4. LangGraph Platform 주요 기능

##### 4.1 Streaming Modes (5가지)

| 모드 | 설명 | 사용 사례 |
|------|------|----------|
| **values** | 각 super-step 후 전체 그래프 상태 스트리밍 | 상태 변화 추적 |
| **messages** | 완료된 메시지 + 생성 중인 토큰 스트리밍 | 챗 애플리케이션 |
| **updates** | 각 노드 실행 후 상태 업데이트 스트리밍 | 증분 업데이트 |
| **events** | 모든 이벤트 스트리밍 (토큰 단위 포함) | 토큰별 스트리밍 |
| **debug** | 디버그 이벤트 스트리밍 | 개발/디버깅 |

##### 4.2 Double Texting 처리 (4가지 전략)

사용자가 그래프 실행 중 추가 메시지를 보낼 때의 처리 방식:

| 전략 | 동작 | 적합한 상황 |
|------|------|------------|
| **Reject** | 후속 실행 거부 | 순차 처리 필수 시 |
| **Enqueue** | 첫 실행 완료 후 새 입력 별도 실행 | 모든 입력 처리 필요 시 |
| **Interrupt** | 현재 실행 중단, 저장 후 새 입력으로 계속 | 최신 입력 우선 시 |
| **Rollback** | 모든 작업 롤백 후 새 입력으로 재시작 | 깨끗한 상태 필요 시 |

##### 4.3 기타 기능

- **Human-in-the-Loop**: 체크포인트에서 인간 개입 삽입
- **Stateless Runs**: 스레드 없이 실행 (체크포인트 스킵)
- **Webhooks**: 실행 완료 시 알림 URL 제공

---

#### 5. 배포 프로세스

##### Step 1: langgraph.json 설정

```json
{
    "dependencies": ["./my_agent"],
    "graphs": {
        "agent": "./my_agent/agent.py:graph"
    },
    "env": ".env"
}
```

##### 프로젝트 구조

```
my-app/
├── my_agent/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── requirements.txt
│   ├── __init__.py
│   └── agent.py          # CompiledGraph 정의
├── .env
└── langgraph.json        # LangGraph 설정 파일
```

##### Step 2: 로컬 테스트

```bash
# CLI 설치 (Python 3.11+)
pip install -U "langgraph-cli[inmem]"

# 또는 JavaScript
npm i @langchain/langgraph-cli

# 로컬 서버 시작
langgraph dev
# → API: http://localhost:2024
# → Docs: http://localhost:2024/docs
```

##### Step 3: SDK로 테스트

```python
from langgraph_sdk import get_client

client = get_client()
assistant_id = "agent"
thread = await client.threads.create()

input = {"messages": [{"role": "user", "content": "what's the weather in sf"}]}

async for chunk in client.runs.stream(
    thread["thread_id"],
    assistant_id,
    input=input,
    stream_mode="updates",
):
    print(f"Event type: {chunk.event}")
    print(chunk.data)
```

##### Step 4: LangSmith UI에서 배포

```
1. LangSmith 대시보드 → Deployments 탭
2. New Deployment 클릭
3. 설정 입력:
   - GitHub 저장소 연결
   - langgraph.json 경로 지정
   - 배포 타입: Production (최대 500 req/sec)
   - 환경 변수 입력 (Secret 체크)
4. Submit 클릭 → 빌드 완료 대기
```

---

#### 6. LangGraph Studio

에이전트를 **시각적으로 디버깅하고 상호작용**하는 IDE:

```
┌─────────────────────────────────────────────────────────┐
│                   LangGraph Studio                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐          ┌────────────────────────┐  │
│  │   Input      │          │    Graph Visualization │  │
│  │              │          │                        │  │
│  │ + Message    │          │    ┌───┐    ┌───┐     │  │
│  │              │    ───▶  │    │ A │───▶│ B │     │  │
│  │ [Submit]     │          │    └───┘    └─┬─┘     │  │
│  │              │          │              │        │  │
│  └──────────────┘          │         ┌────▼────┐   │  │
│                            │         │ Output  │   │  │
│  Thread History            │         └─────────┘   │  │
│  ├─ Thread 1               │                        │  │
│  ├─ Thread 2               └────────────────────────┘  │
│  └─ Thread 3                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

##### 주요 기능

- 그래프 실행 시각화
- 실행 중 상태 편집
- Human-in-the-Loop 개입
- 스레드 생성/관리
- 설정 변경
- 코드 수정 (핫 리로드)

---

#### 7. 보안 모범 사례

##### 3가지 핵심 원칙

| 원칙 | 설명 | 예시 |
|------|------|------|
| **Limit Permissions** | 애플리케이션 필요에 맞게 권한 제한 | 읽기 전용 자격 증명 사용 |
| **Anticipate Misuse** | 모든 액세스가 허용된 방식으로 사용될 수 있다고 가정 | DB 삭제 권한 → LLM이 삭제할 수 있음 |
| **Defense in Depth** | 단일 방어가 아닌 다층 보안 적용 | 읽기 전용 + 샌드박싱 결합 |

##### 시나리오별 완화 전략

```
파일 시스템 접근:
├─ 위험: 민감한 파일 읽기/삭제
├─ 완화: 특정 디렉토리만 접근 허용
└─ 추가: 컨테이너 샌드박싱

API 접근:
├─ 위험: 악성 데이터 쓰기/삭제
├─ 완화: 읽기 전용 API 키 사용
└─ 추가: 안전한 엔드포인트만 허용

데이터베이스 접근:
├─ 위험: 테이블 삭제, 스키마 변경
├─ 완화: 필요한 테이블만 접근 허용
└─ 추가: 읽기 전용 자격 증명
```

##### 추가 보안 조치

| 조치 | 설명 |
|------|------|
| **계정 생성 검증** | 이메일/전화번호 인증 |
| **Rate Limiting** | 일정 시간 내 요청 수 제한 |
| **Prompt Injection 방어** | 권한 범위 제한 + 엄격한 프롬프트 |

---

### 🔍 심화 학습

#### LangGraph Platform vs 직접 배포

```
LangGraph Platform (관리형):
├─ 장점
│   ├─ 수평적 확장 자동화
│   ├─ 내결함성 보장
│   ├─ LangSmith 통합 모니터링
│   └─ One-click 배포
├─ 단점
│   ├─ 비용 (Plus 플랜 필요)
│   └─ 벤더 종속성
│
직접 호스팅 (Self-hosted):
├─ 장점
│   ├─ 완전한 제어권
│   ├─ 비용 절감 가능
│   └─ 커스터마이징 자유
├─ 단점
│   ├─ 인프라 관리 필요
│   ├─ DB/Redis 직접 설정
│   └─ 확장성 직접 구현
```

#### Streaming Mode 선택 가이드

```
사용 사례별 권장 모드:
├─ 챗봇 UI → messages (토큰 단위 + 완료 메시지)
├─ 상태 디버깅 → values (전체 상태)
├─ 실시간 업데이트 → updates (노드별 변화)
├─ 세밀한 제어 → events (모든 이벤트)
└─ 개발 중 → debug (디버그 정보)
```

#### Double Texting 전략 선택

```
상황별 권장 전략:
├─ 엄격한 순서 필요 → Reject
├─ 모든 입력 처리 → Enqueue
├─ 최신 입력 우선 → Interrupt
└─ 깨끗한 재시작 → Rollback
```

---

### 💡 실무 적용 포인트

1. **점진적 배포**: 로컬 테스트 → LangGraph Studio → 프로덕션 순서로 검증
2. **환경 변수 관리**: 민감한 키는 반드시 Secret으로 설정
3. **모니터링 설정**: LangSmith 트레이싱 활성화로 성능/오류 추적
4. **권한 최소화**: Defense in Depth 원칙으로 다층 보안 적용
5. **Rate Limiting**: 비용 폭증 방지를 위한 요청 제한 필수
6. **Vector Store 최적화**: 적절한 임베딩 차원 및 인덱스 설정
7. **Streaming 활용**: UX 향상을 위해 적절한 스트리밍 모드 선택

---

### ✅ 정리 체크리스트

- [ ] LLM, Vector Store, Backend API 세 컴포넌트의 역할을 안다
- [ ] Supabase에서 pgvector를 설정하고 유사도 검색 함수를 만들 수 있다
- [ ] LangGraph Platform의 4가지 데이터 모델(Assistants, Threads, Runs, Cron Jobs)을 설명할 수 있다
- [ ] 5가지 Streaming 모드의 차이를 안다
- [ ] Double Texting의 4가지 처리 전략을 안다
- [ ] langgraph.json 설정 파일을 작성할 수 있다
- [ ] LangGraph CLI로 로컬 테스트를 수행할 수 있다
- [ ] LangSmith UI에서 배포하는 과정을 안다
- [ ] LangGraph Studio의 용도와 기능을 안다
- [ ] 보안 3원칙(Limit Permissions, Anticipate Misuse, Defense in Depth)을 적용할 수 있다

---

### 🔗 참고 자료

- [LangGraph Platform Documentation](https://langchain-ai.github.io/langgraph/cloud/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Supabase Vector Store Guide](https://supabase.com/docs/guides/ai)
- [LangGraph CLI Reference](https://langchain-ai.github.io/langgraph/cloud/reference/cli/)
- [LangGraph Studio Guide](https://langchain-ai.github.io/langgraph/cloud/how-tos/test_deployment/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
