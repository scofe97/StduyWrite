# 01-minimal-lgtm-lab

`learning/`에서 정리한 OTLP, Alloy, Loki, Tempo 개념을 가장 짧은 경로로 만져보는 실습입니다.  
기존 `demo/`나 루트의 복잡한 자산을 건드리지 않고, **단일 Flask 앱 + Alloy + Loki + Tempo + Grafana**만 띄워서 로그와 트레이스를 연결해 봅니다.

## 실습 목표

이 실습을 끝내면 다음을 바로 확인할 수 있습니다.

1. 애플리케이션이 OTLP/HTTP로 로그와 트레이스를 Alloy에 보낸다.
2. Alloy가 traces는 Tempo로, logs는 Loki로 라우팅한다.
3. Grafana에서 로그를 보고 `trace_id`로 trace를 연다.
4. `fail=true` 요청으로 에러 로그와 에러 trace를 함께 본다.

## 디렉토리 구조

```text
01-minimal-lgtm-lab/
├── README.md
├── docker-compose.yml
├── configs/
│   ├── alloy/config.alloy
│   ├── grafana/provisioning/datasources/datasources.yml
│   ├── loki/config.yml
│   └── tempo/config.yml
└── sample-app/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## 빠른 시작

```bash
cd practice/01-minimal-lgtm-lab
docker compose up --build -d
```

## 확인 포인트

### 1. 앱 호출

정상 요청:

```bash
curl http://localhost:18080/work
```

에러 요청:

```bash
curl -i "http://localhost:18080/work?fail=true"
```

### 2. Alloy UI

- `http://localhost:12345`

Alloy가 살아 있고 OTLP receiver가 떠 있는지 확인합니다.

### 3. Grafana

- `http://localhost:3000`
- 기본 계정: `admin / admin`

Grafana에서 다음 순서로 봅니다.

1. Explore로 이동
2. Loki datasource 선택
3. `simple-practice-app` 로그 조회
4. 로그 본문에서 `trace_id=` 값을 확인
5. Tempo datasource에서 같은 trace ID 조회

## 실습 시나리오

### 시나리오 1. 정상 흐름 보기

```bash
curl http://localhost:18080/work
```

기대 결과:

- Loki에 `start work`, `calling internal endpoint`, `work completed` 로그가 보입니다.
- Tempo에서 하나의 trace 안에 Flask server span과 내부 HTTP client span이 보입니다.

### 시나리오 2. 에러 흐름 보기

```bash
curl -i "http://localhost:18080/work?fail=true"
```

기대 결과:

- Loki에 `downstream call failed` 에러 로그가 보입니다.
- Tempo trace 안에 error 상태 span이 남습니다.

### 시나리오 3. 로그에서 trace로 이동

1. Grafana Explore에서 에러 로그 검색
2. 로그 메시지의 `trace_id` 복사
3. Tempo에서 trace ID 조회
4. 어떤 span에서 실패했는지 확인

## 서비스 구성

| 서비스 | 포트 | 역할 |
|--------|------|------|
| sample-app | `18080` | OTLP 로그/트레이스 생성 |
| alloy | `4317`, `4318`, `12345` | OTLP receiver + routing |
| loki | `3100` | 로그 저장소 |
| tempo | `3200`, `4320` | trace 저장소 |
| grafana | `3000` | 조회 UI |

## 트러블슈팅

### Grafana에 로그가 안 보임

```bash
docker compose logs alloy
docker compose logs sample-app
```

확인 포인트:

- sample-app이 Alloy `4318`로 보냈는지
- Alloy가 Loki로 export 실패를 내지 않는지

### Trace가 안 보임

```bash
docker compose logs tempo
docker compose logs alloy
```

확인 포인트:

- Alloy가 `tempo:4317`로 trace를 밀어 넣는지
- 앱에서 `/v1/traces`로 OTLP export가 되는지

### 완전 초기화

```bash
docker compose down -v
```

## learning 연결

- OTLP 개념: `../../learning/02-otlp-and-signal-flow/LEARN.md`
- Alloy 역할: `../../learning/03-grafana-alloy/LEARN.md`
- Loki 역할: `../../learning/04-grafana-loki/LEARN.md`
- Tempo 역할: `../../learning/05-grafana-tempo/LEARN.md`
- 통합 흐름: `../../learning/06-alloy-loki-tempo-integration/LEARN.md`
