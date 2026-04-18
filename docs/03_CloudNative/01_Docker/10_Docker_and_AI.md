# Chapter 10: Docker and AI

## 📌 핵심 요약

> **Docker Model Runner (DMR)**는 AI 모델을 **컨테이너 외부에서** 호스트 하드웨어에 직접 실행하는 Docker 통합 기술이다. GPU, NPU, TPU 등 AI 가속 하드웨어에 쉽게 접근하면서도 Docker 도구 및 클라우드 네이티브 생태계와 완벽히 통합된다. OpenAI 호환 엔드포인트를 통해 모델을 서빙하며, Docker Hub에서 모델을 pull/push할 수 있다.

---

## 🎯 학습 목표

- [ ] Docker Model Runner의 개념과 아키텍처 이해
- [ ] DMR이 컨테이너 외부에서 실행되는 이유 파악
- [ ] docker model 명령어로 모델 관리 실습
- [ ] DMR의 OpenAI 호환 API 엔드포인트 활용
- [ ] Compose를 통한 DMR 통합 앱 배포

---

## 📖 본문 정리

### 1. Docker에서 AI 앱 실행 방법

#### 💬 비유로 이해하기
> DMR은 **전용 고속도로**와 같다. 일반 도로(컨테이너)는 모든 차량이 다닐 수 있지만 속도 제한이 있다. AI 모델이라는 대형 트럭은 전용 고속도로(DMR)를 통해 하드웨어에 직접 접근해야 최고 속도로 달릴 수 있다.

#### 두 가지 방법 비교

| 방법 | 설명 | 권장 여부 |
|------|------|-----------|
| **Docker Model Runner** | 호스트에서 직접 실행, AI 가속 하드웨어 접근 용이 | ✅ **권장** |
| **컨테이너** | 컨테이너 내부 실행, 하드웨어 접근 제한적 | ❌ 비권장 |

#### 로컬 AI 실행이 필요한 경우
- 프라이버시 우려 (데이터 외부 전송 불가)
- 예측 불가능한 클라우드 비용 회피
- 지연 시간(Latency) 민감한 요구사항
- 프롬프트 커스터마이징 및 파인튜닝 제어

### 2. Docker Model Runner 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Docker Model Runner 아키텍처                      │
└─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │                        Applications                              │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
  │  │ Containers  │  │  Local Apps │  │     Remote Apps         │  │
  │  │             │  │             │  │                         │  │
  │  │ model-runner│  │ localhost   │  │ <host-ip>:12434         │  │
  │  │ .docker.    │  │ :12434      │  │                         │  │
  │  │ internal    │  │             │  │                         │  │
  │  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
  └─────────┼────────────────┼─────────────────────┼────────────────┘
            │                │                     │
            └────────────────┼─────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                    OpenAI-compatible APIs                        │
  │  ┌───────────────────────────────────────────────────────────┐  │
  │  │ /engines/v1/chat/completions   (채팅)                      │  │
  │  │ /engines/v1/completions        (텍스트 완성)               │  │
  │  │ /engines/v1/embeddings         (임베딩)                    │  │
  │  │ /engines/v1/models             (모델 목록)                 │  │
  │  └───────────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                  Docker Model Runner (Host Process)              │
  │  ┌───────────────────────────────────────────────────────────┐  │
  │  │              Pluggable Runtime Layer                       │  │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │  │
  │  │  │ llama.cpp   │  │    MLX      │  │   기타...    │        │  │
  │  │  │  (기본)     │  │  (예정)     │  │             │        │  │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘        │  │
  │  └───────────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                      Host Hardware                               │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
  │  │    GPU      │  │    NPU      │  │    CPU      │              │
  │  │ (NVIDIA,    │  │ (Neural     │  │             │              │
  │  │  Apple M)   │  │  Engine)    │  │             │              │
  │  └─────────────┘  └─────────────┘  └─────────────┘              │
  └─────────────────────────────────────────────────────────────────┘
```

#### 핵심 구성 요소

| 구성 요소 | 설명 |
|-----------|------|
| **Docker Model Runner** | Docker Engine과 별개의 호스트 프로세스 |
| **Runtime Layer** | 플러그형 추론 엔진 (기본: llama.cpp) |
| **Local Model Store** | `~/.docker/models`에 모델 저장 |
| **OpenAI API** | 호환 엔드포인트 제공 |
| **Docker CLI Plugin** | `docker model` 명령어 제공 |

### 3. DMR이 컨테이너 외부에서 실행되는 이유

```
┌─────────────────────────────────────────────────────────────────┐
│                 컨테이너 vs DMR 하드웨어 접근                     │
└─────────────────────────────────────────────────────────────────┘

  컨테이너 방식 (제한적)                DMR 방식 (권장)
  ─────────────────────                ─────────────────────

  ┌─────────────┐                      ┌─────────────┐
  │  Container  │                      │     DMR     │
  │  ─────────  │                      │  ─────────  │
  │   AI Model  │                      │   AI Model  │
  └──────┬──────┘                      └──────┬──────┘
         │                                    │
         │ ❌ 제한적 접근                      │ ✅ 직접 접근
         │ (NVIDIA CUDA만)                    │ (다양한 하드웨어)
         ▼                                    ▼
  ┌─────────────┐                      ┌─────────────────────────┐
  │ NVIDIA GPU  │                      │ GPU | NPU | TPU | CPU   │
  │    only     │                      │ (Apple, NVIDIA, etc.)   │
  └─────────────┘                      └─────────────────────────┘
```

**컨테이너의 한계**:
- GPU, NPU, TPU 등 AI 가속 하드웨어는 독점적 드라이버/SDK 사용
- Docker 생태계에서 모든 하드웨어 지원 개발/유지가 어려움
- NVIDIA Container Toolkit 설치 시 CUDA GPU만 제한적 접근 가능

**DMR의 장점**:
- Docker 도구 및 클라우드 네이티브 생태계 통합
- AI 가속 하드웨어에 쉬운 접근
- 동적 모델 로드/언로드 (온디맨드)

### 4. DMR vs Ollama vs LM Studio

| 기능 | DMR | Ollama | LM Studio |
|------|-----|--------|-----------|
| 추론 엔진 | llama.cpp | llama.cpp | llama.cpp |
| OpenAI 호환 API | ✅ | ✅ | ✅ |
| Docker 통합 | ✅ **네이티브** | ❌ | ❌ |
| Compose 통합 | ✅ **provider** | 컨테이너로 | ❌ |
| Docker Hub 연동 | ✅ | ❌ | ❌ |

**DMR 선택 권장 상황**:
- 기존 Docker 사용자 + 로컬 모델 운영 중
- Docker 사용자 + 로컬 모델 도입 예정
- 로컬 모델 운영 중 + Docker 도입 예정

### 5. DMR 설치 및 설정

#### 시스템 요구사항
- Mac 또는 Windows (Apple Silicon 또는 NVIDIA GPU 권장)
- Docker Desktop v4.41 이상
- GPU 없어도 CPU로 실행 가능 (느림)

#### 활성화 방법
```
Docker Desktop → Settings → Features in development
  ☑ Enable Docker Model Runner
  ☑ Enable host-side TCP support
  Port: 12434
  → Apply & restart
```

#### 상태 확인
```bash
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp latest-metal (sha256:ad58230f548...)
```

### 6. 모델 관리 명령어

#### 모델 Pull/List/Inspect

```bash
# Docker Hub에서 모델 다운로드
$ docker model pull ai/gemma3:4B-Q4_K_M
Model pulled successfully

# 로컬 모델 목록 확인
$ docker model ls
MODEL NAME            PARAMS   QUANTIZATION     ARCH     SIZE
ai/gemma3:4B-Q4_K_M   3.88 B   IQ2_XXS/Q4_K_M   gemma3   2.31G
ai/qwen3:0.6B-Q4_K_M  751.63 M IQ2_XXS/Q4_K_M   qwen3    456.11 MiB

# 모델 상세 정보
$ docker model inspect ai/gemma3:4B-Q4_K_M
```

#### 모델 저장 구조 (OCI Artifact)

```
~/.docker/models/blobs/sha256/
├── 09b370de51ad3...  (GGUF 모델 파일, ~2.3GB)
├── 22273fd2f4e6d...  (모델 설정 JSON, 372B)
└── a4b03d96571f0...  (라이선스, 8.2KB)
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    OCI Model Manifest 구조                       │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │ Manifest (application/vnd.oci.image.manifest.v1+json)       │
  ├─────────────────────────────────────────────────────────────┤
  │ config:                                                     │
  │   mediaType: application/vnd.docker.ai.model.config.v0.1    │
  │   digest: sha256:22273fdf...                                │
  ├─────────────────────────────────────────────────────────────┤
  │ layers:                                                     │
  │   [0] mediaType: application/vnd.docker.ai.gguf.v3          │
  │       digest: sha256:09b370de... (모델 파일)                │
  │   [1] mediaType: application/vnd.docker.ai.license          │
  │       digest: sha256:a4b03d96... (라이선스)                 │
  └─────────────────────────────────────────────────────────────┘
```

### 7. 모델 테스트

#### CLI를 통한 테스트

```bash
$ docker model run ai/gemma3:4B-Q4_K_M

Interactive chat mode started. Type '/bye' to exit.

> How long is a day on Mars?
A day on Mars, also known as a "sol," is approximately 24 hours,
39 minutes, and 35 seconds long...

> /bye
```

#### Docker Desktop UI를 통한 테스트
- Models 탭 → 모델 선택 → 채팅 인터페이스
- 대화 기록 유지됨 (CLI보다 나은 경험)

### 8. DMR API 엔드포인트

#### 엔드포인트 종류

| 카테고리 | 엔드포인트 | 메서드 | 설명 |
|----------|-----------|--------|------|
| **모델 관리** | `/models` | GET | 모델 목록 |
| | `/models/create` | POST | 모델 생성 |
| | `/models/{ns}/{name}` | GET/DELETE | 모델 조회/삭제 |
| **OpenAI 호환** | `/engines/v1/models` | GET | 모델 목록 |
| | `/engines/v1/chat/completions` | POST | 채팅 완성 |
| | `/engines/v1/completions` | POST | 텍스트 완성 |
| | `/engines/v1/embeddings` | POST | 임베딩 |

#### 접근 방법별 호스트명

| 접근 위치 | 호스트명 | 포트 |
|-----------|----------|------|
| 컨테이너 내부 | `model-runner.docker.internal` | 기본 |
| 로컬 앱 | `localhost` | 12434 |
| 원격 앱 | `<host-ip>` | 12434 |

#### API 호출 예시

```bash
# 모델 목록 조회
$ curl -s localhost:12434/engines/v1/models | jq
{
  "data": [{
    "id": "ai/gemma3:4B-Q4_K_M",
    "object": "model",
    "owned_by": "docker"
  }]
}

# 채팅 완성 요청
$ curl -s http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/gemma3:4B-Q4_K_M",
    "messages": [
      {"role": "system", "content": "Keep responses to one sentence."},
      {"role": "user", "content": "How long is a day on Mars?"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }' | jq -r '.choices[0].message.content'

A day on Mars, also known as a sol, is approximately 24.6 hours long.
```

### 9. Compose와 DMR 통합

#### 챗봇 앱 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    Compose Chatbot 아키텍처                      │
└─────────────────────────────────────────────────────────────────┘

  User Browser
       │
       │ :3000
       ▼
  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
  │  frontend   │         │   backend   │         │     dmr     │
  │ ─────────── │  :8000  │ ─────────── │  HTTP   │ ─────────── │
  │   Remix     │────────►│   FastAPI   │────────►│   Docker    │
  │  Chat UI    │         │   Server    │         │   Model     │
  │             │◄────────│             │◄────────│   Runner    │
  └─────────────┘ stream  └─────────────┘ stream  └─────────────┘
                                │
                                │ model-runner.docker.internal
                                ▼
                         ┌─────────────┐
                         │  AI Model   │
                         │ (Gemma3 등) │
                         └─────────────┘
```

#### Compose 파일 (provider 확장)

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - dmr

  dmr:                           # DMR 서비스 선언
    provider:                    # provider 확장 사용
      type: model                # 타입: model
      options:
        model: ${LLM_MODEL_NAME} # 사용할 모델

# .env 파일
# MODEL_HOST=http://model-runner.docker.internal/engines/v1
# LLM_MODEL_NAME=ai/gemma3:4B-Q4_K_M
```

#### 배포 및 실행

```bash
$ docker compose up --build --detach

[+] Building 3.3s (25/25) FINISHED
[+] Running 6/6
 - Network dmr_default         Created
 - dmr                         Created    # DMR 서비스
 - Container dmr-backend-1     Started
 - Container dmr-frontend-1    Started
```

### 10. Open WebUI와 DMR 통합

#### Open WebUI Compose 파일

```yaml
volumes:
  open-webui:

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - DEFAULT_MODELS=${MODEL_NAME}
      - WEBUI_AUTH=False
      - OPENAI_API_KEY=${OPENAI_KEY}        # DMR은 키 불필요 ("na")
      - OPENAI_API_BASE_URL=${MODEL_HOST}   # DMR 엔드포인트
    volumes:
      - open-webui:/app/backend/data
    ports:
      - "3001:8080"
    depends_on:
      - dmr

  dmr:
    provider:
      type: model
      options:
        model: ${MODEL_NAME}

# .env 파일
# MODEL_HOST=http://model-runner.docker.internal/engines/v1
# MODEL_NAME=ai/qwen3:0.6B-Q4_K_M
# OPENAI_KEY=na
```

```
┌─────────────────────────────────────────────────────────────────┐
│                   Open WebUI + DMR 통합                          │
└─────────────────────────────────────────────────────────────────┘

  Browser :3001
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                       Open WebUI                             │
  │  ┌─────────────────────────────────────────────────────────┐│
  │  │ 모델 선택 ▼ │  ai/gemma3:4B-Q4_K_M              Active ││
  │  ├─────────────────────────────────────────────────────────┤│
  │  │                                                         ││
  │  │  User: How far away is the moon?                        ││
  │  │  AI: The Moon is approximately 384,400 km...            ││
  │  │                                                         ││
  │  │  User: What about the sun?                              ││
  │  │  AI: The Sun is about 150 million km (1 AU)...          ││
  │  │                                                         ││
  │  ├─────────────────────────────────────────────────────────┤│
  │  │ [Prompt Box]                              [Send] [Voice]││
  │  └─────────────────────────────────────────────────────────┘│
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 │ OpenAI-compatible API
                                 ▼
                         ┌─────────────┐
                         │     DMR     │
                         │ (ai/gemma3) │
                         └─────────────┘
```

### 11. 컨테이너에서 모델 실행 (비권장)

```
⚠️ 권장하지 않음

컨테이너 방식의 한계:
- NVIDIA Container Toolkit 설치 필요 (복잡)
- CUDA 지원 NVIDIA GPU만 가속 가능
- 다른 GPU/NPU/TPU → CPU 폴백 (느림)

Ollama 컨테이너 방식:
┌────────────────────────────────────────────────────────────┐
│ services:                                                  │
│   ollama:                                                  │
│     image: nigelpoulton/gsd-book:chat-model                │
│     volumes:                                               │
│       - ollama_data:/root/.ollama                          │
│     deploy:                                                │
│       resources:                                           │
│         limits:                                            │
│           memory: 8G                                       │
│         reservations:                    # GPU 사용 시     │
│           devices:                                         │
│             - driver: nvidia                               │
│               count: all                                   │
│               capabilities: [gpu]                          │
└────────────────────────────────────────────────────────────┘
```

---

## 🔍 심화 학습

### OCI Artifact로서의 AI 모델
- 컨테이너 이미지와 동일한 레지스트리에 저장 가능
- 기존 클라우드 네이티브 도구/파이프라인과 통합
- 레지스트리 스프롤(sprawl) 감소

### 추가 학습 주제
- **Docker MCP Toolkit**: AI 에이전트 도구 통합
- **Model Quantization**: 모델 경량화 기법 (Q4_K_M 등)
- **Fine-tuning**: 로컬 모델 커스터마이징
- **Prompt Engineering**: 시스템 프롬프트 최적화

---

## 💡 실무 적용 포인트

### 면접 대비 질문

**Q1: Docker Model Runner가 컨테이너 외부에서 실행되는 이유는?**
> **A**: AI 가속 하드웨어(GPU, NPU, TPU)는 독점적 드라이버와 SDK를 사용하여 컨테이너 내부에서 접근하기 어렵다. DMR은 호스트에서 직접 실행되어 다양한 AI 가속 하드웨어에 쉽게 접근하면서도 Docker 생태계와 완벽히 통합된다.

**Q2: DMR의 OpenAI 호환 엔드포인트에 컨테이너가 접근하는 방법은?**
> **A**: 컨테이너는 `http://model-runner.docker.internal/` 특수 호스트명을 통해 DMR에 접근한다. 로컬 앱은 `localhost:12434`, 원격 앱은 `<host-ip>:12434`를 사용한다.

**Q3: Compose에서 DMR을 통합하는 방법은?**
> **A**: `provider` 확장을 사용하여 DMR 서비스를 선언한다. `type: model`과 `options.model`로 사용할 모델을 지정하면, Compose가 DMR을 자동으로 설정하고 다른 서비스의 의존성으로 관리한다.

**Q4: DMR vs Ollama vs LM Studio의 차이점은?**
> **A**: 세 도구 모두 llama.cpp 기반 추론과 OpenAI 호환 API를 제공한다. 핵심 차이는 DMR이 Docker 도구(CLI, Compose, Hub)와 네이티브 통합되어 기존 Docker 워크플로우에 AI를 쉽게 추가할 수 있다는 점이다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Docker Model Runner의 목적과 장점 설명 가능
- [ ] DMR이 컨테이너 외부에서 실행되는 이유 이해
- [ ] 플러그형 런타임 레이어 (llama.cpp 등) 개념 파악
- [ ] OCI Artifact로서의 AI 모델 저장 방식 이해

### DMR 설정 및 관리
- [ ] Docker Desktop에서 DMR 활성화
- [ ] `docker model status`: DMR 상태 확인
- [ ] `docker model pull`: Docker Hub에서 모델 다운로드
- [ ] `docker model ls`: 로컬 모델 목록 확인
- [ ] `docker model inspect`: 모델 상세 정보 조회
- [ ] `docker model run`: CLI에서 모델 테스트
- [ ] `docker model rm`: 모델 삭제

### API 활용
- [ ] OpenAI 호환 엔드포인트 구조 이해
- [ ] `/engines/v1/chat/completions` API 호출
- [ ] 컨테이너/로컬/원격 접근 방법 구분

### Compose 통합
- [ ] `provider` 확장으로 DMR 서비스 선언
- [ ] `depends_on`으로 서비스 의존성 설정
- [ ] 환경 변수로 모델 및 엔드포인트 설정

### 실무 적용
- [ ] 프라이버시/비용/지연시간 요구사항에 따른 로컬 AI 선택
- [ ] Open WebUI 같은 서드파티 앱과 DMR 통합
- [ ] 시스템 프롬프트를 통한 모델 응답 커스터마이징

---

## 🔗 참고 자료

- [Docker Model Runner 공식 문서](https://docs.docker.com/model-runner/)
- [Docker Hub AI Models Catalog](https://hub.docker.com/catalogs/models)
- [Open WebUI](https://github.com/open-webui/open-webui)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 10
