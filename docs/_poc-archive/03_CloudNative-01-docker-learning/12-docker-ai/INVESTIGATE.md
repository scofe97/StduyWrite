# Ch12. Docker & AI - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. GPU 패스스루(Passthrough) 메커니즘은 어떻게 작동하며, 컨테이너에서 GPU를 사용할 때의 제약사항은 무엇인가?

### 왜 이 질문이 중요한가
AI 워크로드는 대부분 GPU 가속이 필요하다. Docker Model Runner가 호스트에서 실행되는 이유를 이해하려면, 컨테이너 내부에서 GPU를 사용할 때 발생하는 근본적인 제약을 파악해야 한다. GPU 패스스루 메커니즘을 이해하면 AI 인프라 설계 시 올바른 아키텍처 결정을 내릴 수 있다.

### 답변
GPU 패스스루는 컨테이너가 호스트의 물리적 GPU에 접근하도록 하는 메커니즘이다. 하지만 이는 CPU 가상화보다 훨씬 복잡하다.

**컨테이너의 기본 격리 방식**
- 컨테이너는 리눅스 네임스페이스와 cgroups를 통해 프로세스, 네트워크, 파일시스템을 격리한다.
- CPU와 메모리는 cgroups로 제한 가능하지만, GPU는 일반적인 리눅스 커널 리소스가 아니다.
- GPU는 독자적인 드라이버와 사용자 공간 라이브러리(CUDA, ROCm 등)가 필요하다.

**NVIDIA Container Toolkit의 작동 방식**
1. **호스트 요구사항**: NVIDIA GPU 드라이버가 호스트에 설치되어 있어야 한다.
2. **nvidia-docker2 런타임**: 표준 Docker 런타임을 확장해 GPU 디바이스 파일(`/dev/nvidia*`)을 컨테이너에 마운트한다.
3. **라이브러리 바인딩**: 호스트의 CUDA 라이브러리(`libcuda.so`, `libnvidia-ml.so` 등)를 컨테이너에 볼륨으로 마운트한다.
4. **환경 변수**: `NVIDIA_VISIBLE_DEVICES`, `NVIDIA_DRIVER_CAPABILITIES` 같은 환경 변수로 어떤 GPU를 노출할지 제어한다.

**실행 예시**:
```bash
docker run --gpus all \
  -e NVIDIA_VISIBLE_DEVICES=0,1 \
  nvidia/cuda:12.0-base \
  nvidia-smi
```

이 명령은 다음을 수행한다:
- `--gpus all`: 모든 GPU를 컨테이너에 노출
- 호스트의 `/dev/nvidia0`, `/dev/nvidia1`, `/dev/nvidiactl`, `/dev/nvidia-uvm` 등을 컨테이너에 마운트
- 호스트의 CUDA 라이브러리를 컨테이너의 `/usr/lib/x86_64-linux-gnu`에 바인드

**주요 제약사항**

1. **벤더 종속성**: NVIDIA Container Toolkit은 NVIDIA GPU만 지원한다. AMD GPU는 ROCm, Intel GPU는 oneAPI 등 각각 다른 도구가 필요하다. Docker 생태계에서 모든 GPU를 통일된 방식으로 지원하기 어렵다.

2. **드라이버 버전 일치**: 컨테이너 내부의 CUDA 버전과 호스트의 GPU 드라이버 버전이 호환되어야 한다. 예를 들어 CUDA 12.0은 최소 드라이버 버전 525.60.13이 필요하다. 버전 불일치 시 "CUDA driver version is insufficient" 오류가 발생한다.

3. **권한 문제**: GPU 디바이스 파일은 root 권한이 필요하므로, 컨테이너를 privileged 모드로 실행하거나 디바이스 cgroup 설정이 필요하다. 이는 보안 위험을 증가시킨다.

4. **멀티테넌시 제한**: 한 GPU를 여러 컨테이너가 동시에 사용하면 메모리 충돌이 발생할 수 있다. NVIDIA MIG(Multi-Instance GPU)를 사용하면 물리 GPU를 논리적으로 분할할 수 있지만, A100 같은 고급 GPU만 지원한다.

5. **NPU/TPU 미지원**: Apple Neural Engine, Google TPU, Qualcomm NPU 같은 AI 가속기는 컨테이너 런타임이 표준 지원하지 않는다. 각 벤더가 별도 솔루션을 제공하거나, 아예 컨테이너 외부(호스트)에서 실행해야 한다.

**Docker Model Runner가 이 문제를 해결하는 방식**
- DMR은 컨테이너 내부가 아닌 호스트 프로세스로 실행된다.
- llama.cpp 같은 런타임이 호스트 하드웨어에 직접 접근하므로, NVIDIA CUDA뿐 아니라 Apple Metal, AMD ROCm, Intel oneAPI 등 다양한 백엔드를 플러그형으로 지원할 수 있다.
- 컨테이너는 OpenAI 호환 HTTP API를 통해 DMR에 접근하므로, GPU 드라이버나 라이브러리를 컨테이너에 포함할 필요가 없다.

### 실무 적용
컨테이너에서 GPU를 사용할 때는 다음을 확인해야 한다.
- 호스트 GPU 드라이버 버전 (`nvidia-smi`)
- 컨테이너 이미지의 CUDA 버전 (Dockerfile의 `FROM nvidia/cuda:X.Y-base`)
- 드라이버-CUDA 호환성 테이블 (NVIDIA 공식 문서)

실무 팁: 프로덕션 환경에서 AI 모델을 서빙할 때, 컨테이너 내부에서 직접 GPU를 사용하기보다 전용 모델 서버(TensorFlow Serving, TorchServe, DMR)를 호스트에서 실행하고, 애플리케이션 컨테이너는 HTTP API를 통해 접근하는 패턴이 더 안정적이다. 이렇게 하면 GPU 드라이버 버전 관리, 멀티테넌시, 벤더 종속성 문제를 줄일 수 있다.

---

## Q2. NVIDIA Container Toolkit은 어떻게 설계되었으며, 다른 GPU 벤더는 왜 유사한 도구를 제공하지 않는가?

### 왜 이 질문이 중요한가
NVIDIA Container Toolkit은 사실상 컨테이너 기반 GPU 워크로드의 표준이다. 하지만 AMD, Intel, Apple 같은 다른 벤더는 왜 비슷한 수준의 통합을 제공하지 않는가? 이를 이해하면 AI 인프라의 벤더 종속성을 파악하고, 멀티 벤더 전략을 수립할 수 있다.

### 답변
**NVIDIA Container Toolkit 아키텍처**

NVIDIA Container Toolkit은 다음 컴포넌트로 구성된다:
1. **nvidia-docker2**: Docker 데몬의 런타임을 확장하는 래퍼
2. **libnvidia-container**: GPU 디바이스 및 라이브러리를 컨테이너에 주입하는 C 라이브러리
3. **nvidia-container-runtime**: OCI(Open Container Initiative) 표준을 준수하는 런타임
4. **nvidia-container-cli**: GPU 관련 컨테이너 설정을 수행하는 CLI 도구

**작동 흐름**:
```
docker run --gpus all <image>
    ↓
Docker 데몬이 nvidia-container-runtime 호출
    ↓
libnvidia-container가 /proc, /sys에서 GPU 디바이스 정보 수집
    ↓
/dev/nvidia*, /dev/nvidiactl 등을 컨테이너 네임스페이스에 마운트
    ↓
호스트의 CUDA 라이브러리를 컨테이너 /usr/lib에 바인드
    ↓
환경 변수(NVIDIA_VISIBLE_DEVICES 등) 설정
    ↓
컨테이너 시작, 내부에서 nvidia-smi 실행 가능
```

**NVIDIA가 성공한 이유**

1. **CUDA 생태계 선점**: NVIDIA는 2006년부터 CUDA를 개발해 AI/HPC 시장을 장악했다. 대부분의 딥러닝 프레임워크(PyTorch, TensorFlow)가 CUDA를 기본 백엔드로 사용한다.

2. **엔터프라이즈 투자**: NVIDIA는 데이터센터 시장에 막대한 투자를 했다. DGX 시스템, GPU Cloud, Triton Inference Server 등 엔드투엔드 솔루션을 제공한다.

3. **표준화 노력**: NVIDIA는 OCI 표준을 준수하며, Kubernetes Device Plugin도 제공해 클라우드 네이티브 생태계와 긴밀히 통합했다.

**다른 벤더가 뒤처진 이유**

1. **AMD (ROCm)**:
   - AMD는 ROCm(Radeon Open Compute)을 통해 Docker 지원을 제공하지만, 문서와 도구가 NVIDIA만큼 성숙하지 않다.
   - ROCm Docker 이미지는 존재하지만, NVIDIA Container Toolkit만큼 자동화되지 않아 수동 설정이 많이 필요하다.
   - AMD GPU는 주로 게이밍 시장에 집중했고, 데이터센터 시장 점유율이 낮아 개발 우선순위가 떨어진다.

2. **Intel (oneAPI)**:
   - Intel은 oneAPI를 통해 CPU, GPU, FPGA를 통합 프로그래밍 모델로 지원하려 하지만, AI 시장에서 늦게 진입했다.
   - Intel GPU(Xe, Arc)는 아직 데이터센터용보다 클라이언트용이 주력이며, 컨테이너 통합은 초기 단계다.
   - Intel은 Habana Labs 인수 후 Gaudi AI 가속기에 집중하고 있지만, 생태계가 CUDA에 비해 미약하다.

3. **Apple (Metal)**:
   - Apple Silicon의 Neural Engine은 macOS/iOS에 특화되어 있고, 서버/클라우드 시장을 겨냥하지 않는다.
   - Metal은 컨테이너 환경보다 네이티브 앱(Swift, Objective-C)에 최적화되어 있다.
   - Apple은 Docker Desktop for Mac을 지원하지만, GPU 패스스루는 제공하지 않는다. (M 시리즈 칩의 통합 아키텍처 특성상 가상화 복잡도가 높음)

**벤더 중립적 접근의 어려움**

컨테이너 런타임이 모든 GPU 벤더를 동일하게 지원하기 어려운 이유:
- GPU마다 드라이버 인터페이스가 다르다 (NVIDIA: CUDA, AMD: ROCm, Intel: Level Zero, Apple: Metal)
- 각 벤더가 독자적인 최적화를 추구한다 (Tensor Core, Matrix Engine, XMX 등)
- AI 프레임워크가 대부분 CUDA 우선 개발되므로, 다른 백엔드는 성능과 기능이 뒤처진다

**Docker Model Runner의 접근**

DMR은 이 문제를 런타임 레이어를 플러그형으로 만들어 해결했다:
- 기본: llama.cpp (CUDA, Metal, ROCm, AVX2 등 다양한 백엔드 지원)
- 예정: MLX (Apple Silicon 최적화), 기타 런타임
- 컨테이너는 GPU 종류와 무관하게 동일한 OpenAI 호환 API 사용

### 실무 적용
멀티 벤더 GPU 전략을 고려할 때:
- **NVIDIA GPU**: CUDA 생태계 성숙도가 압도적. 프로덕션 AI 워크로드는 대부분 NVIDIA.
- **AMD GPU**: 가격 대비 성능이 좋지만, 소프트웨어 생태계 제한. PyTorch ROCm 지원이 개선되고 있음.
- **Apple Silicon**: 개발/추론 로컬 환경에 적합. 서버 배포는 부적합.
- **Intel**: Gaudi 가속기는 학습에 유망하지만, 생태계가 아직 초기 단계.

실무 권장: 프로덕션은 NVIDIA GPU + NVIDIA Container Toolkit 또는 DMR 사용. 비용 절감이 중요하면 AMD GPU + ROCm 검토. 로컬 개발은 Apple Silicon + DMR이 최적. 벤더 종속성을 줄이려면 ONNX Runtime 같은 벤더 중립 추론 엔진 사용.

---

## Q3. AI 모델 이미지의 크기 최적화는 왜 중요하며, 어떤 전략을 사용할 수 있는가?

### 왜 이 질문이 중요한가
AI 모델은 수 GB에 달하는 경우가 많다. 이를 컨테이너 이미지에 포함하면 빌드, 푸시, 풀 시간이 크게 증가하고, 레지스트리 스토리지 비용도 상승한다. DMR은 모델을 OCI Artifact로 저장해 이미지 크기를 KB 단위로 줄였다. 이미지 최적화 전략을 이해하면 CI/CD 파이프라인 속도를 개선하고 인프라 비용을 절감할 수 있다.

### 답변
**AI 모델 이미지 크기 문제**

전형적인 AI 모델 이미지 구성:
```dockerfile
FROM python:3.11
RUN pip install torch torchvision  # ~2GB
COPY model.pth /app/model.pth       # ~500MB
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

이 이미지의 크기는 약 3GB가 된다. 문제점:
- Docker Hub 무료 tier는 pull rate limit (익명: 100회/6시간)
- CI/CD에서 매번 3GB 다운로드는 파이프라인 병목
- Kubernetes에서 새 노드가 추가될 때 이미지 pull로 인한 지연
- 멀티 리전 배포 시 네트워크 전송 비용

**최적화 전략**

**1. 모델과 코드 분리**

컨테이너 이미지는 애플리케이션 코드만 포함하고, 모델은 외부 스토리지에서 로드한다.

```dockerfile
FROM python:3.11-slim  # slim 이미지 사용
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu  # CPU 버전 (~100MB)
COPY app.py /app/
ENV MODEL_PATH=/models/model.pth
CMD ["python", "/app/app.py"]
```

```python
# app.py
import os
import torch
model_path = os.getenv('MODEL_PATH')
model = torch.load(model_path)  # 볼륨 또는 S3에서 로드
```

배포 시:
```bash
docker run -v /host/models:/models myapp
```

장점: 이미지 크기 ~300MB로 감소, 모델 업데이트 시 이미지 재빌드 불필요
단점: 모델 다운로드 로직 추가 필요, 초기 시작 시간 증가

**2. 멀티 스테이지 빌드**

학습과 추론 이미지를 분리한다.

```dockerfile
# 학습 스테이지
FROM python:3.11 AS trainer
RUN pip install torch torchvision
COPY train.py /app/
RUN python /app/train.py  # 모델 학습, model.pth 생성

# 추론 스테이지
FROM python:3.11-slim
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
COPY --from=trainer /app/model.pth /app/
COPY inference.py /app/
CMD ["python", "/app/inference.py"]
```

장점: 학습 도구(CUDA, cuDNN)를 추론 이미지에서 제거, 최종 이미지 크기 감소
단점: 빌드 시간 증가

**3. 모델 양자화 및 압축**

모델 크기 자체를 줄인다.

- **Quantization**: FP32 → FP16 또는 INT8로 변환 (크기 50~75% 감소, 정확도 약간 하락)
- **Pruning**: 중요도가 낮은 가중치 제거
- **Distillation**: 큰 모델의 지식을 작은 모델로 전이

예: PyTorch 양자화
```python
import torch
model = torch.load('model.pth')
model.eval()
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
torch.save(quantized_model.state_dict(), 'model_quantized.pth')
```

GGUF 형식(llama.cpp): FP16, Q8, Q4 등 다양한 양자화 레벨 지원
- `gemma3:4B-Q4_K_M`: 4-bit 양자화, ~2.3GB
- `gemma3:4B-FP16`: 16-bit, ~8GB

**4. Docker Model Runner 방식**

모델을 OCI Artifact로 저장하고, 애플리케이션 이미지와 분리한다.

```bash
# 모델 pull (별도)
docker model pull ai/gemma3:4B-Q4_K_M  # 2.3GB

# 애플리케이션 이미지 (모델 미포함)
docker pull myapp:latest  # 100MB
```

Compose 파일:
```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      - dmr
  dmr:
    provider:
      type: model
      options:
        model: ai/gemma3:4B-Q4_K_M
```

장점: 모델과 앱 버전 독립 관리, 레지스트리 레이어 캐싱 효율 극대화
단점: DMR 의존성

**5. Layer 캐싱 최적화**

자주 변경되는 레이어를 뒤로 배치한다.

```dockerfile
# 나쁜 예
FROM python:3.11
COPY . /app  # 코드 변경 시 아래 레이어도 재빌드
RUN pip install -r requirements.txt

# 좋은 예
FROM python:3.11
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt  # 의존성 변경 시에만 재빌드
COPY . /app  # 코드 변경은 이 레이어만 재빌드
```

### 실무 적용
프로덕션 권장 전략:
1. **모델 < 100MB**: 이미지에 직접 포함 (간편함 우선)
2. **모델 100MB~1GB**: 멀티 스테이지 빌드 + slim 베이스 이미지
3. **모델 > 1GB**: S3/GCS + init container로 다운로드, 또는 DMR 사용
4. **초대형 모델 (> 10GB)**: 양자화 필수, DMR + GGUF 형식 권장

실제 사례: OpenAI Whisper 모델
- Original FP32: ~3GB
- FP16: ~1.5GB
- INT8 양자화: ~800MB
- llama.cpp GGUF Q4: ~400MB (정확도 허용 범위 내)

CI/CD 최적화: GitHub Actions에서 모델을 별도 artifact로 관리하고, 이미지 빌드 시 캐시에서 로드. 모델 변경이 없으면 재다운로드 스킵.

---

## Q4. ML 파이프라인(학습, 검증, 배포)을 컨테이너화할 때 주의할 점은 무엇인가?

### 왜 이 질문이 중요한가
AI 모델은 "한 번 만들고 끝"이 아니라 지속적으로 학습, 검증, 배포되는 라이프사이클을 가진다. 이를 컨테이너화하면 재현성과 확장성이 향상되지만, 데이터 접근, GPU 스케줄링, 모델 버저닝 같은 새로운 문제가 발생한다. ML 파이프라인 컨테이너화를 이해하면 MLOps 인프라를 효과적으로 설계할 수 있다.

### 답변
**ML 파이프라인의 세 단계**

1. **학습(Training)**: 데이터를 읽어 모델을 학습시킨다. GPU 집약적, 장시간 실행 (수시간~수일)
2. **검증(Validation)**: 학습된 모델을 테스트 데이터로 평가한다. 정확도, F1 스코어 등 메트릭 계산
3. **배포(Deployment)**: 검증된 모델을 프로덕션에 서빙한다. 추론 최적화, 낮은 지연시간 요구

**컨테이너화 시 주요 고려사항**

**1. 데이터 접근 패턴**

학습 데이터는 대용량(수십 GB~TB)이므로 컨테이너 이미지에 포함 불가.

옵션:
- **볼륨 마운트**: `-v /data:/data` (로컬/온프레미스)
- **클라우드 스토리지**: S3, GCS 마운트 (s3fs, gcsfuse)
- **데이터 버전 관리**: DVC(Data Version Control) 사용

예:
```yaml
# Kubernetes PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-data
spec:
  accessModes:
    - ReadOnlyMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd
```

```yaml
# Pod에서 사용
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: training-data
```

**2. GPU 스케줄링**

학습은 GPU가 필수지만, 검증/배포는 CPU로도 가능한 경우가 많다.

Kubernetes에서 GPU 리소스 요청:
```yaml
resources:
  limits:
    nvidia.com/gpu: 2  # 2개 GPU 요청
  requests:
    memory: "16Gi"
    cpu: "4"
```

주의사항:
- GPU는 **정수 단위**로만 요청 가능 (0.5 GPU 불가, MIG 제외)
- GPU 노드는 비싸므로, 학습 완료 후 즉시 Pod 종료해 리소스 해제
- Spot/Preemptible 인스턴스 사용 시 체크포인트 저장 필수 (중간에 종료될 수 있음)

**3. 재현성(Reproducibility)**

동일한 데이터와 하이퍼파라미터로 학습해도 결과가 달라질 수 있다 (랜덤 시드, GPU 연산 순서).

재현성 확보:
```python
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)
```

Dockerfile에서:
```dockerfile
ENV PYTHONHASHSEED=42
ENV CUBLAS_WORKSPACE_CONFIG=:4096:8
```

**4. 체크포인트 저장**

장시간 학습 시 중간 결과를 저장해야 한다.

```python
# 주기적으로 체크포인트 저장
for epoch in range(num_epochs):
    train(model, dataloader)
    if epoch % 10 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
        }, f'/checkpoints/model_epoch_{epoch}.pth')
```

Kubernetes에서 PVC 사용:
```yaml
volumes:
  - name: checkpoints
    persistentVolumeClaim:
      claimName: training-checkpoints
```

**5. 모델 버저닝**

학습된 모델을 버전 관리한다.

옵션:
- **MLflow Model Registry**: 모델 메타데이터, 메트릭, 아티팩트 관리
- **DVC**: Git과 연동된 모델 버저닝
- **Docker Hub**: 모델을 OCI Artifact로 푸시 (DMR 방식)

예: MLflow
```python
import mlflow
mlflow.log_param("learning_rate", 0.001)
mlflow.log_metric("accuracy", 0.95)
mlflow.pytorch.log_model(model, "model")
```

**6. 파이프라인 오케스트레이션**

학습 → 검증 → 배포를 자동화한다.

도구:
- **Kubeflow Pipelines**: Kubernetes 네이티브 ML 워크플로우
- **Apache Airflow**: 범용 워크플로우 엔진
- **Argo Workflows**: Kubernetes 기반 DAG 실행

Kubeflow 예시:
```python
@dsl.component
def train_op():
    return dsl.ContainerOp(
        name='Train Model',
        image='myregistry/trainer:v1',
        arguments=['--epochs', '100'],
    )

@dsl.component
def validate_op(model_path):
    return dsl.ContainerOp(
        name='Validate Model',
        image='myregistry/validator:v1',
        arguments=['--model', model_path],
    )

@dsl.pipeline(name='ML Pipeline')
def ml_pipeline():
    train_task = train_op()
    validate_task = validate_op(train_task.outputs['model'])
```

### 실무 적용
프로덕션 ML 파이프라인 권장 아키텍처:
1. **학습**: Kubernetes Job + GPU 노드 + PVC (데이터 + 체크포인트)
2. **검증**: Kubernetes Job + CPU 노드 + MLflow 메트릭 로깅
3. **배포**: 검증 통과 시 자동으로 모델을 레지스트리에 푸시, CI/CD가 추론 서비스 업데이트

실제 사례: Spotify의 ML 파이프라인
- Luigi로 DAG 정의
- Docker 컨테이너로 각 단계 실행
- HDFS에 데이터 저장, S3에 모델 저장
- 학습 완료 후 Slack 알림

주의사항: GPU 노드는 비싸므로 autoscaling 필수. AWS에서 p3.2xlarge (V100 1개)는 시간당 $3.06이므로, 10시간 학습 시 $30. Spot 인스턴스 사용 시 70% 절감 가능하지만 체크포인트 저장 필수.

---

## Q5. 분산 학습(Distributed Training)과 컨테이너의 조합에서 발생하는 네트워크 병목은 어떻게 해결하는가?

### 왜 이 질문이 중요한가
대규모 모델(GPT, LLaMA 등)은 단일 GPU로 학습이 불가능하며, 여러 노드에 걸친 분산 학습이 필수다. 컨테이너 환경에서 분산 학습을 수행하면 네트워크 오버헤드가 발생하며, 이는 학습 속도를 크게 저하시킨다. 네트워크 병목을 이해하고 최적화하면 학습 비용과 시간을 크게 절감할 수 있다.

### 답변
**분산 학습의 두 가지 패러다임**

1. **Data Parallelism**: 같은 모델을 여러 GPU에 복제하고, 데이터를 분할해 병렬 학습. 주기적으로 그래디언트를 동기화.
2. **Model Parallelism**: 모델이 너무 커서 한 GPU 메모리에 안 들어갈 때, 모델을 레이어별로 분할해 여러 GPU에 배치.

**네트워크 병목의 원인**

Data Parallelism에서 각 GPU는 forward/backward pass 후 그래디언트를 다른 GPU와 동기화해야 한다. 이 과정에서:
- **All-Reduce 연산**: N개 GPU가 각각의 그래디언트를 평균내는 집단 통신
- **대역폭 요구**: GPT-3 (175B 파라미터, FP16) → 350GB 그래디언트, 매 iteration마다 동기화
- **지연 시간**: 노드 간 네트워크 지연이 GPU 연산보다 느리면 GPU가 idle 상태로 대기

컨테이너 환경의 추가 오버헤드:
- CNI(Container Network Interface) 플러그인의 추가 hop
- Overlay 네트워크(Calico, Flannel)의 캡슐화 오버헤드
- NodePort/LoadBalancer의 NAT 비용

**해결 전략**

**1. 고속 네트워크 하드웨어**

- **InfiniBand**: 100~400 Gbps 대역폭, 마이크로초 지연. NVIDIA DGX 시스템 표준.
- **RoCE (RDMA over Converged Ethernet)**: Ethernet에서 RDMA 지원, InfiniBand보다 저렴.
- **AWS EFA (Elastic Fabric Adapter)**: AWS에서 제공하는 고성능 네트워크 인터페이스, p4d 인스턴스에서 400 Gbps.

Kubernetes에서 RDMA 사용:
```yaml
resources:
  limits:
    rdma/hca: 1  # RDMA 디바이스 요청
```

**2. NCCL (NVIDIA Collective Communications Library)**

NVIDIA가 제공하는 GPU 간 통신 최적화 라이브러리.

기능:
- Ring All-Reduce: 대역폭 효율적인 집단 통신 알고리즘
- GPU Direct RDMA: CPU를 거치지 않고 GPU ↔ NIC 직접 통신
- 자동 토폴로지 감지: NVLink, PCIe, InfiniBand 등 최적 경로 선택

PyTorch에서 NCCL 사용:
```python
import torch.distributed as dist
dist.init_process_group(backend='nccl')  # NCCL 백엔드 사용
```

환경 변수 튜닝:
```bash
export NCCL_DEBUG=INFO  # 디버그 로그
export NCCL_IB_DISABLE=0  # InfiniBand 활성화
export NCCL_NET_GDR_LEVEL=5  # GPU Direct RDMA 최대 레벨
```

**3. Host Network 모드**

컨테이너가 호스트 네트워크 네임스페이스를 직접 사용해 CNI 오버헤드 제거.

```yaml
# Kubernetes Pod
spec:
  hostNetwork: true  # 호스트 네트워크 사용
  dnsPolicy: ClusterFirstWithHostNet
```

주의: 포트 충돌 가능, 보안 약화. 프로덕션보다 학습 워크로드에 적합.

**4. Gradient Accumulation**

그래디언트 동기화 빈도를 줄여 네트워크 부담 감소.

```python
accumulation_steps = 4
for i, (inputs, labels) in enumerate(dataloader):
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    loss = loss / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()  # 4번에 한 번만 동기화
        optimizer.zero_grad()
```

트레이드오프: 메모리 사용량 증가, effective batch size 증가로 수렴 특성 변화.

**5. Mixed Precision Training**

FP32 대신 FP16 사용으로 전송 데이터 크기 50% 감소.

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for inputs, labels in dataloader:
    with autocast():  # FP16 연산
        outputs = model(inputs)
        loss = criterion(outputs, labels)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

**6. 분산 학습 프레임워크**

- **Horovod**: Uber 개발, MPI 기반, Ring All-Reduce
- **PyTorch DDP (DistributedDataParallel)**: PyTorch 네이티브, NCCL 백엔드
- **DeepSpeed**: Microsoft 개발, ZeRO optimizer로 메모리 효율 극대화

Horovod 예시:
```python
import horovod.torch as hvd
hvd.init()
model = DistributedDataParallel(model)
optimizer = hvd.DistributedOptimizer(optimizer)
```

### 실무 적용
클라우드 환경 분산 학습 권장 설정:
- **AWS**: p4d.24xlarge (A100 8개 + EFA 400Gbps) + FSx for Lustre (데이터)
- **GCP**: a2-megagpu-16g (A100 16개 + 100 Gbps 네트워크)
- **Azure**: NDv4 시리즈 (A100 8개 + InfiniBand 200 Gbps)

Kubernetes 설정:
```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: distributed-training
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
          - name: pytorch
            image: myregistry/trainer:v1
            resources:
              limits:
                nvidia.com/gpu: 8
    Worker:
      replicas: 3  # 총 4노드 x 8GPU = 32 GPU
      template:
        spec:
          hostNetwork: true  # 네트워크 최적화
          containers:
          - name: pytorch
            env:
            - name: NCCL_DEBUG
              value: "INFO"
```

벤치마크: ResNet-50 학습 (ImageNet)
- 단일 V100: 350 images/sec
- 8 V100 (Data Parallel, Ethernet 10Gbps): 2100 images/sec (선형 확장 대비 75%)
- 8 V100 (Data Parallel, InfiniBand 100Gbps): 2700 images/sec (선형 확장 대비 96%)

결론: 분산 학습에서 네트워크는 병목이 될 수 있지만, InfiniBand/EFA + NCCL + Host Network + FP16으로 대부분 해결 가능.

---

## Q6. Docker Model Runner의 플러그형 런타임 아키텍처는 어떻게 설계되었으며, 새로운 런타임을 추가하는 것이 가능한가?

### 왜 이 질문이 중요한가
DMR의 핵심 장점은 다양한 AI 가속 하드웨어를 지원하는 플러그형 런타임 레이어다. 이 아키텍처를 이해하면, AI 인프라가 특정 벤더에 종속되지 않고 유연하게 확장 가능한 이유를 파악할 수 있다. 또한 자체 커스텀 런타임을 추가할 수 있는지 여부는 엔터프라이즈 도입 결정에 중요하다.

### 답변
**DMR 아키텍처 계층**

```
Application (Container/Local)
        ↓ OpenAI-compatible HTTP API
Docker Model Runner (Host Process)
        ↓ Runtime Abstraction Layer
Pluggable Runtime (llama.cpp, MLX, ...)
        ↓ Hardware Abstraction
GPU/NPU/CPU (Metal, CUDA, ROCm, AVX2)
```

**런타임 추상화 인터페이스**

DMR은 다음 인터페이스를 런타임이 구현하도록 요구한다:
1. **모델 로드**: GGUF, Safetensors 등 포맷에서 모델 읽기
2. **추론 실행**: 텍스트 입력 → 토큰 생성 (스트리밍 지원)
3. **리소스 관리**: GPU 메모리 할당/해제, 모델 언로드
4. **메타데이터 제공**: 모델 파라미터 수, 양자화 레벨, 지원 하드웨어

**llama.cpp 런타임 (기본)**

llama.cpp는 C++로 작성된 경량 LLM 추론 엔진으로, 다양한 백엔드를 지원한다:
- **Metal**: Apple Silicon GPU (M1/M2/M3)
- **CUDA**: NVIDIA GPU
- **ROCm**: AMD GPU
- **Vulkan**: 크로스 플랫폼 GPU
- **OpenCL**: 범용 GPU
- **AVX2/AVX512**: x86 CPU SIMD
- **NEON**: ARM CPU SIMD

llama.cpp는 런타임에 하드웨어를 감지하고 최적 백엔드를 자동 선택한다.

**DMR이 런타임과 통신하는 방식**

DMR은 런타임을 별도 프로세스로 실행하고, gRPC 또는 Unix socket으로 통신한다.

예상 흐름:
```
1. 사용자: docker model pull ai/gemma3:4B-Q4_K_M
2. DMR: 모델 blob을 ~/.docker/models/blobs/에 다운로드
3. 사용자: docker model run ai/gemma3:4B-Q4_K_M
4. DMR: llama.cpp 프로세스 시작
   $ llama-server --model ~/.docker/models/blobs/sha256:09b370de... --port 12435
5. llama.cpp: Metal 백엔드 감지, GPU 메모리에 모델 로드
6. DMR: llama.cpp의 /v1/chat/completions을 프록시해 OpenAI 호환 API 노출
7. 클라이언트: curl localhost:12434/engines/v1/chat/completions
8. DMR: 요청을 llama.cpp (localhost:12435)로 전달
9. llama.cpp: 추론 실행, 스트리밍 응답
10. DMR: 응답을 클라이언트로 반환
```

**새로운 런타임 추가 가능성**

현재 DMR은 플러그형 아키텍처지만, **공식적인 런타임 플러그인 SDK는 공개되지 않았다**. 하지만 다음 방식으로 확장 가능할 것으로 예상된다:

1. **Docker Desktop Extension**: DMR이 Docker Desktop의 확장 메커니즘을 사용한다면, 서드파티가 런타임 확장을 개발할 수 있다.

2. **런타임 설정 파일**: DMR 설정에서 커스텀 런타임 바이너리와 지원 모델 포맷을 등록.
```json
{
  "runtimes": {
    "mlx": {
      "binary": "/usr/local/bin/mlx-server",
      "supported_formats": ["safetensors", "gguf"],
      "default_port": 12436
    }
  }
}
```

3. **OCI Hooks**: OCI(Open Container Initiative) 표준의 prestart/poststart 훅을 사용해 커스텀 런타임 주입.

**예상되는 확장 런타임**

- **MLX**: Apple이 개발한 ML 프레임워크, Apple Silicon 최적화
- **vLLM**: 고성능 LLM 서빙 엔진, PagedAttention으로 메모리 효율 극대화
- **TensorRT-LLM**: NVIDIA의 LLM 추론 최적화 엔진
- **ONNX Runtime**: 벤더 중립 추론 엔진

**커스텀 런타임 개발 시 고려사항**

만약 조직이 자체 런타임을 개발한다면:
1. **OpenAI 호환 API 구현**: `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`
2. **스트리밍 지원**: Server-Sent Events (SSE) 또는 WebSocket
3. **모델 포맷 지원**: 최소한 GGUF 또는 Safetensors
4. **에러 처리**: OOM, 타임아웃 시 적절한 HTTP 에러 코드 반환
5. **메트릭 노출**: Prometheus 형식의 추론 지연시간, 처리량 메트릭

### 실무 적용
현재 DMR은 초기 단계이므로, 프로덕션에서는 다음을 고려해야 한다:
- **공식 지원 런타임만 사용**: llama.cpp가 유일하게 안정적
- **미래 확장성 대비**: DMR이 MLX, vLLM 등을 지원하면 즉시 전환 가능한 아키텍처 설계
- **폴백 옵션**: DMR이 불안정하면 Ollama 또는 TensorRT-LLM 같은 성숙한 도구로 롤백

장기적으로 DMR이 런타임 플러그인 생태계를 형성하면, AI 인프라의 벤더 종속성이 크게 감소할 것이다. 현재는 기대 단계지만, Docker의 생태계 영향력을 고려하면 주목할 가치가 있다.

---

## Q7. AI 모델 서빙(Serving) 패턴은 무엇이며, 각각 어떤 트레이드오프를 가지는가?

### 왜 이 질문이 중요한가
학습된 모델을 프로덕션에 배포할 때, "어떻게 서빙할 것인가"는 성능, 비용, 운영 복잡도에 직접적인 영향을 미친다. DMR, TensorFlow Serving, Triton, FastAPI 등 다양한 옵션이 있으며, 각각 다른 트레이드오프를 가진다. 서빙 패턴을 이해하면 워크로드 특성에 맞는 최적의 솔루션을 선택할 수 있다.

### 답변
**AI 모델 서빙의 주요 패턴**

**1. 사이드카 패턴 (Sidecar)**

애플리케이션 컨테이너와 모델 서버 컨테이너를 같은 Pod에 배치.

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: MODEL_URL
      value: "http://localhost:8501/v1/models/my_model:predict"
  - name: tf-serving
    image: tensorflow/serving:latest
    ports:
    - containerPort: 8501
```

장점: 네트워크 지연 최소화 (localhost 통신), 모델과 앱이 라이프사이클 공유
단점: 리소스 효율 낮음 (각 앱마다 모델 서버 복제), 모델 업데이트 시 전체 Pod 재시작

**적합 사례**: 지연시간이 극도로 중요한 실시간 추론, 모델이 작고 앱과 1:1 대응

**2. 마이크로서비스 패턴 (Microservice)**

모델 서버를 독립 서비스로 배포, 여러 애플리케이션이 공유.

```yaml
# 모델 서빙 서비스
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: triton
        image: nvcr.io/nvidia/tritonserver:latest
        resources:
          limits:
            nvidia.com/gpu: 1
---
# 애플리케이션
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: MODEL_URL
          value: "http://model-server:8000/v2/models/my_model/infer"
```

장점: 리소스 효율 (모델 서버 공유), 독립 스케일링, 모델 업데이트 시 앱 무중단
단점: 네트워크 hop 추가 (지연 증가), 서비스 간 의존성 관리 필요

**적합 사례**: 여러 앱이 같은 모델 사용, 모델이 대용량 (GPU 필요), 독립 운영팀

**3. 서버리스 패턴 (Serverless)**

요청이 있을 때만 모델 서버가 자동으로 시작되고, 유휴 시 스케일 다운.

```yaml
# Knative Serving
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: model-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"  # 0으로 스케일 다운
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containers:
      - image: myregistry/model-server:v1
        resources:
          limits:
            nvidia.com/gpu: 1
```

장점: 비용 효율 (사용한 만큼만 과금), 자동 스케일링
단점: Cold start 지연 (첫 요청 시 수초~수십초), GPU 환경에서 스케일링 느림

**적합 사례**: 간헐적 트래픽, 비용 민감, 지연시간 허용치 큼 (수 초)

**4. 배치 추론 패턴 (Batch Inference)**

실시간 응답이 아닌, 주기적으로 대량 데이터를 배치 처리.

```yaml
# Kubernetes CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: batch-inference
spec:
  schedule: "0 2 * * *"  # 매일 오전 2시
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: inference
            image: myregistry/batch-inference:v1
            env:
            - name: INPUT_PATH
              value: "s3://mybucket/input/"
            - name: OUTPUT_PATH
              value: "s3://mybucket/output/"
```

장점: GPU 활용률 극대화, 비용 효율 (배치 크기로 최적화), 오프피크 시간 활용
단점: 실시간 응답 불가, 결과 지연 (시간~일 단위)

**적합 사례**: 추천 시스템 (매일 업데이트), 이미지 처리 (대량 사진 분석), 로그 분석

**5. Docker Model Runner 패턴**

호스트에서 모델 서버 실행, 컨테이너가 OpenAI 호환 API로 접근.

```yaml
services:
  app:
    image: myapp:latest
    environment:
      - MODEL_HOST=http://model-runner.docker.internal/engines/v1
  dmr:
    provider:
      type: model
      options:
        model: ai/gemma3:4B-Q4_K_M
```

장점: 하드웨어 접근 최적화 (Metal, CUDA, ROCm 등), Docker 도구 통합, 이미지 크기 최소화
단점: 아직 초기 단계, Kubernetes 지원 미정, 프로덕션 검증 부족

**적합 사례**: 로컬 개발, 소규모 배포, 다양한 하드웨어 지원 필요

**서빙 프레임워크 비교**

| 프레임워크 | 장점 | 단점 | 적합 사례 |
|-----------|------|------|----------|
| **TensorFlow Serving** | TF 네이티브, 배치 처리 최적화 | TF 전용, 복잡한 설정 | TF 모델, 고성능 |
| **TorchServe** | PyTorch 네이티브, A/B 테스트 지원 | 문서 부족 | PyTorch 모델 |
| **Triton Inference Server** | 다중 프레임워크, GPU 최적화 | 설정 복잡 | 멀티 모델, NVIDIA GPU |
| **FastAPI + 직접 구현** | 유연성, 간단함 | 최적화 직접 구현 | 프로토타입, 커스텀 로직 |
| **Docker Model Runner** | 하드웨어 중립, Docker 통합 | 초기 단계 | 로컬 개발, LLM |
| **ONNX Runtime** | 벤더 중립, 경량 | 모델 변환 필요 | 엣지 디바이스, 크로스 플랫폼 |

**트레이드오프 축**

- **지연시간 vs 처리량**: 사이드카는 지연 낮고, 배치는 처리량 높음
- **비용 vs 응답성**: 서버리스는 비용 낮고, 상시 실행은 응답 빠름
- **유연성 vs 성능**: FastAPI는 유연하고, TF Serving/Triton은 성능 최적화
- **벤더 종속성 vs 최적화**: DMR/ONNX는 중립적, CUDA 전용은 NVIDIA에 최적화

### 실무 적용
워크로드별 권장 패턴:
1. **실시간 채팅봇 (< 100ms)**: 사이드카 + TorchServe/Triton
2. **추천 시스템 (< 1s)**: 마이크로서비스 + Redis 캐싱
3. **이미지 분류 API (< 500ms)**: 마이크로서비스 + Triton + 배치 처리
4. **일간 리포트 생성**: 배치 추론 + CronJob
5. **개발/테스트**: DMR + Compose

실제 아키텍처 예시: Netflix 추천 시스템
- 온라인 추론: Zuul Gateway → Model Server (마이크로서비스) → Redis 캐시
- 오프라인 배치: Spark 배치 잡 → S3 → 모델 업데이트
- A/B 테스트: 여러 모델 버전을 Triton에서 동시 서빙, 트래픽 분할

결론: AI 서빙 패턴은 워크로드 특성(지연시간, 처리량, 비용)에 따라 선택해야 하며, 단일 패턴보다 하이브리드 접근이 현실적이다.
