# Redpanda Go (franz-go)

Go + Redpanda 통합 실습 프로젝트. [franz-go](https://github.com/twmb/franz-go) 클라이언트 사용.

## 선행 조건

- Go 1.23+
- Docker (Redpanda 실행용)
- `../docker-compose.yml`로 인프라 실행

## 빌드 & 실행

```bash
# 인프라 시작
cd .. && docker compose up -d

# 빌드
make build

# 챕터별 실행
make run-ch01
make run-ch03

# 테스트
make test
make test-ch05
```

## 구조

```
redpanda-go/
├── cmd/app/main.go          # 엔트리포인트 (챕터별 서브커맨드)
├── internal/
│   ├── config/kafka.go      # franz-go 클라이언트 팩토리
│   ├── common/              # 공유 타입
│   ├── ch01/ ~ ch12/        # 챕터별 패키지
│   └── testutil/            # testcontainers 공통
├── avro/                    # .avsc 스키마 (Spring 프로젝트와 공유)
├── go.mod
├── Makefile
└── README.md
```

## 학습 문서

`../../learning/08-go-integration/` 참조.

## 기술 스택

| 라이브러리 | 용도 |
|-----------|------|
| franz-go | Kafka/Redpanda 클라이언트 (순수 Go) |
| franz-go/pkg/sr | Schema Registry 클라이언트 |
| hamba/avro/v2 | Avro 직렬화 |
| zerolog | 구조화 로깅 |
| testcontainers-go | 통합 테스트 |
