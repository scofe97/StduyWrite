---
title: Python 통합 테스트 학습 묶음
tags: [moc, python, testing, pytest, integration-test, qa]
status: final
related:
  - ../README.md
  - ../../java/spring/05_testing/README.md
updated: 2026-05-10
---

# Python 통합 테스트 학습 묶음

Spring Boot 애플리케이션을 외부에서 pytest로 검증하는 Python 클라이언트 코드를 한 줄기로 정리한 묶음이다. 표면적으로는 "pytest 사용법"이지만, 실제로 들여다보면 fixture 계층 설계, requests Session 재사용, pymysql 직접 폴링, ThreadPoolExecutor + pytest-xdist 동시성, bash subprocess 기반 chaos engineering, Java `CryptoService`와 호환되는 cryptography AES/CBC/PKCS7, 시드 SQL 템플릿 자동화까지 한 시스템을 외부에서 검증하기 위한 결정이 차곡차곡 쌓여 있다.

레퍼런스 코드는 TPS 사내 저장소의 `qa/python/` 디렉토리이며, executor → 실 dev Jenkins로 이어지는 dispatch 흐름을 외부에서 직접 HTTP로 두드리는 통합 테스트가 들어 있다. 한 챕터씩 따로 읽어도 닫히도록 썼지만 순서대로 따라가면 "왜 이런 결정을 내렸는가"가 누적된다.



## 이 묶음의 위치

[`01_language/java/spring/05_testing/`](../../java/spring/05_testing/README.md) 묶음이 Spring Boot 애플리케이션 *내부*에서 단위·슬라이스·통합·E2E를 어떻게 쌓는지 다룬다면, 이 묶음은 같은 애플리케이션을 *외부* 프로세스에서 두드려 검증하는 시각을 담는다. 두 묶음은 같은 시스템을 안에서 보는 눈과 밖에서 보는 눈으로, 한쪽으로는 못 잡는 결함을 다른 쪽이 잡는다. 예컨대 컨테이너 인프라 단절(Redpanda stop, Jenkins 차단)이나 동시 50건 burst 부하 같은 시나리오는 외부 검증이 아니면 진짜로 잡기 어렵다.



## 학습 곡선

읽는 순서는 인프라 의존도가 낮은 것부터 높은 것까지로 정렬했다. pytest 자체와 fixture 계층은 개념만 잡으면 어떤 환경에서도 똑같이 동작한다. requests Session과 pymysql 단계는 실 HTTP/DB가 살아 있어야 검증 가능하지만 단일 프로세스로 끝난다. ThreadPoolExecutor + xdist 단계는 같은 시스템을 동시에 두드려 race condition을 끌어내고, chaos 단계는 OS 레벨 권한(sudo)과 docker 인프라가 추가로 필요하다. cryptography 단계는 코드 하나만 보면 되지만 Java 측 구현과 비트 단위로 맞춰야 하므로 디테일 밀도가 가장 높다. 마지막 confluent-kafka Avro Producer 단계는 REST 진입점이 없는 운영 경로(예: cancel 메시지)를 직접 두드려야 닫을 수 있는 분기를 다룬다. 이 순서를 의식해 읽으면 "이 챕터는 어떤 환경에서 이득을 보는가"가 자연스럽게 따라온다.



## 챕터 (총 8편)

| # | 제목 | 핵심 |
|---|------|------|
| 01-01 | [pytest 기초와 마커·parametrize](01-01.pytest%20기초와%20마커·parametrize.md) | 디스커버리 규칙, `pytest.ini`(markers·addopts·log_cli), `@pytest.mark.<name>` + 등록의 의미, parametrize로 happy 10건/chaos vsrn 3건 표현 |
| 01-02 | [conftest 계층과 fixture 설계](01-02.conftest%20계층과%20fixture%20설계.md) | 루트/주제 2단 conftest, scope=session vs function, yield 기반 setup/teardown, fixture가 의존성 주입인 이유 |
| 01-03 | [requests Session으로 HTTP 통합 테스트](01-03.requests%20Session으로%20HTTP%20통합%20테스트.md) | Session 재사용으로 connection pool과 기본 헤더 통합, basic auth, timeout, 5xx와 4xx 단언 분리 |
| 01-04 | [pymysql 직접 검증과 폴링 패턴](01-04.pymysql%20직접%20검증과%20폴링%20패턴.md) | raw SQL로 DB가 진짜 무엇을 저장했는지 보기, placeholder 안전성, IN 절 동적 생성, `wait_status` 폴링, `FOR UPDATE` 락 경합 시뮬레이션 |
| 01-05 | [ThreadPoolExecutor와 pytest-xdist 동시성](01-05.ThreadPoolExecutor와%20pytest-xdist%20동시성.md) | 한 테스트 안의 50 병렬과 테스트들끼리의 병렬을 분리, GIL과 I/O bound, race condition 검증으로 QUEUE_ID 충돌 잡기 |
| 01-06 | [chaos fixture—bash subprocess와 인프라 단절](01-06.chaos%20fixture—bash%20subprocess와%20인프라%20단절.md) | fixture가 외부 인프라를 조작하는 패턴, `/etc/hosts` swap·docker compose stop, yield/finally 복구, `SKIP_NET_CHAOS=1` 안전망 |
| 01-07 | [cryptography로 Java AES 호환과 시드 자동화](01-07.cryptography로%20Java%20AES%20호환과%20시드%20자동화.md) | Java `CryptoService`(AES/CBC/PKCS5)와 비트 단위 같은 결과 만들기, 키/IV 파생 정책, 시드 템플릿 + placeholder + render 스크립트로 평문 .env 격리 |
| 01-08 | [confluent-kafka Avro Producer로 운영 경로 검증](01-08.confluent-kafka%20Avro%20Producer로%20운영%20경로%20검증.md) | REST 가 아닌 Kafka 가 운영 진입점일 때 SerializingProducer + Schema Registry 자동 등록 + generated SCHEMA$ 임베드, cancel 분기 검증을 위한 wait 조건의 의미 (RUNNING 단독 vs SUBMITTED 포함) |



## 묶음의 톤

각 챕터는 다음 4단을 따른다.

1. **왜 이 단계가 필요한가** — 다른 단계로는 잡지 못하는 결함이 무엇인지를 한 문단으로 보인다.
2. **핵심 API와 결정** — 표 또는 짧은 코드로 결정적 차이를 보인다.
3. **함정과 회피** — 실제 사고 사례를 정리한다. SQL placeholder 누락, fixture scope 오용, /etc/hosts 잔류 같은 것이 자주 등장한다.
4. **TPS 사례** — `qa/python/` 의 실 코드를 짧게 인용한다. 패턴이 본질인 인용은 일반화하고, 흐름이 본질인 인용은 그대로 둔다.



## 사전 지식 (이 묶음을 읽기 전 권장)

- Python 함수와 데코레이터 기본
- HTTP 메서드와 상태 코드의 의미(특히 4xx/5xx 분리)
- SQL 기초(SELECT·INSERT·트랜잭션)
- pytest를 한 번이라도 실행해 본 경험(없어도 01-01에서 디스커버리 규칙부터 다룬다)



## 관련 문서

- [Spring 테스트 학습 묶음](../../java/spring/05_testing/README.md) — 같은 시스템을 안에서 검증. Testcontainers·EmbeddedKafka·ArchUnit 중심.
- [01_language/python](../README.md) — 상위 카테고리 MOC.
