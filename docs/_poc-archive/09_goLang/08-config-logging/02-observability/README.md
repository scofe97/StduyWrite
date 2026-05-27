# 14. 로깅 및 메트릭 (Observability)

애플리케이션의 상태를 모니터링하고 추적하기 위한 로깅과 메트릭을 학습합니다.

## 학습 목표

- 구조화된 로깅 (Structured Logging)
- 로깅 레벨 관리
- Prometheus 메트릭 수집
- 성능 모니터링

## 주요 라이브러리

### uber-go/zap
```bash
go get go.uber.org/zap
```

고성능 구조화 로깅:
- 타입 안전한 필드
- 성능 최적화 (alloc 최소화)
- 구조화된 JSON 출력

### rs/zerolog (대안)
```bash
go get github.com/rs/zerolog
```

Zero allocation 로거:
- 매우 빠른 성능
- 체이닝 API
- JSON 기본 출력

### prometheus/client_golang
```bash
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/client_golang/prometheus/promhttp
```

메트릭 수집:
- Counter, Gauge, Histogram, Summary
- HTTP 엔드포인트 자동 노출
- 표준 Prometheus 형식

## 주요 개념

### 로깅 레벨
- DEBUG: 상세 디버깅 정보
- INFO: 일반 정보성 메시지
- WARN: 경고 메시지
- ERROR: 오류 메시지
- FATAL/PANIC: 치명적 오류

### 메트릭 타입
- Counter: 증가만 하는 값 (요청 수)
- Gauge: 증감 가능한 값 (메모리 사용량)
- Histogram: 분포 측정 (요청 지연 시간)
- Summary: 백분위 계산

## 프로젝트 구조

```
14-observability/
├── README.md
├── EXERCISES.md
├── HINTS.md
├── LEARNED.md
├── go.mod
├── main.go
├── logging/
│   └── logger.go        # 로거 설정
└── metrics/
    └── metrics.go       # 메트릭 정의
```

## 학습 순서

1. zap 로거 초기화 및 기본 사용법
2. 구조화된 로그 메시지 작성
3. Prometheus 메트릭 정의
4. HTTP 서버에 메트릭 통합
5. 로그와 메트릭 상관관계

## 참조 자료

### 📚 Learning Go, 2nd Edition 참조
- **13_The_Standard_Library.md**: log 패키지, io 패키지
- **12_Concurrency_in_Go.md**: 동시성 환경에서의 로깅 안전성
- **14_The_Context.md**: 컨텍스트 기반 추적 ID 전파

## 다음 단계

다음 모듈 [15-generics](../15-generics/)에서 제네릭과 함수형 유틸리티를 학습합니다.
