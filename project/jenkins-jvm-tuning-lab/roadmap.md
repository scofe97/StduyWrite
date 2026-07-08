# 로드맵 — Jenkins JVM Tuning Lab

처음부터 크게 만들지 않고 세 단계로 자른다. 코드가 먼저 나오고 그 측정 결과가 학습편을 낳는 순서다. 각 단계는 [`requirements.md`](requirements.md)의 FR를 하나씩 충족시킨다.

## 단계 개요

| 단계 | 한 일의 결과 | 충족하는 FR | 산출물 |
|:--:|------|-----------|--------|
| 1차 | 랩이 뜬다 | FR-1, FR-2, FR-3, FR-6 | 동작하는 docker-compose |
| 2차 | 튜닝 루프를 한 번 완주한다 | FR-4, FR-5, FR-7 | `RESULTS.md`의 before/after |
| 3차 | 실측을 학습편으로 정리한다 | — | 학습 `.md` 1편 |

## 1차 — 랩 골격

docker-compose에 세 덩어리를 배선한다. Jenkins Controller, Jenkins가 배포할 Spring Boot 앱, 그리고 둘을 함께 보는 관측 스택이다.

- **JVM 프로파일 배선 (FR-1, FR-2).** Jenkins Controller와 Spring Boot 앱 각각에 `baseline`/`tuned` 환경변수 프로파일을 두고, `-Xlog:gc*,safepoint`로 GC와 safepoint를 파일에 남긴다. baseline은 힙을 일부러 작게(예: Controller `-Xmx512m`) 둬 병목을 끌어낸다.
- **Spring Boot 앱 도입 (FR-3).** seed의 Go sample-app은 손대지 않는다. 외부 호출을 흉내 내는 엔드포인트(지연을 주는 원격 호출 모킹)를 가진 최소 Spring Boot 앱을 새로 두고, Jenkins가 이 앱을 빌드해 로컬 레지스트리에 올리고 배포하게 한다.
- **관측 스택 (FR-6).** Prometheus가 Jenkins `/prometheus/`와 앱 `/actuator/prometheus`를 함께 스크랩하고, Grafana에 두 JVM 패널을 올린다.

**재사용.** seed `_practice/poc/docker-compose.yml`의 registry·agent 구성을 출발점으로 삼되 그 폴더는 건드리지 않고 이 폴더 안에 확장본을 만든다. 관측 배선은 [`06_observability/05_SpringActuator/01-03.프로메테우스·그라파나 연동.md`](../../write/06_observability/05_SpringActuator/01-03.프로메테우스·그라파나%20연동.md)를 따른다.

**끝났다고 보는 기준.** `docker compose up` 한 번으로 Jenkins·앱·Prometheus·Grafana가 모두 뜨고, Grafana에서 두 JVM의 heap과 GC 지표가 보인다 (NFR-1 재현성).

## 2차 — 튜닝 루프 완주

같은 부하를 baseline과 tuned에 각각 걸어 숫자를 얻는다. 이 단계가 이력서 수치를 만든다.

- **부하 재현 (FR-4).** Jenkins에는 200건 트리거 부하를, Spring Boot 앱에는 동시 요청 부하를 건다. Jenkins 부하는 [`05-07 §6-3`](../../write/07_devops/02_Jenkins/06_infra/05-07.Jenkins%20성능%20모니터링%20—%20지표·수집%20토폴로지·부하%20실측.md)의 crumb 발급 + `for i in $(seq 1 200)` 트리거 스크립트를 그대로 쓴다. 앱 부하는 별도 스크립트로 동시성을 올려 스레드·커넥션풀을 압박한다.
- **병목 재현 (baseline).** baseline 프로파일로 Full GC·긴 pause·Metaspace 압박을 끌어내고, 그 순간의 thread dump와 heap dump를 채취한다 (FR-5). heap 스파이크는 수집 주기 120초에 묻히므로 `/metrics` 서블릿을 직접 본다 (NFR-3).
- **재측정 (tuned).** 힙 상향과 G1 파라미터, Metaspace 상한을 적용한 tuned 프로파일로 *같은* 부하를 다시 건다. 부하 스크립트와 트리거 수가 동일해야 비교가 성립한다 (NFR-2 결정성).
- **결과 정리 (FR-7).** 두 회차의 GC pause·처리량·heap 사용률을 `RESULTS.md`에 표로 남긴다. 여기서 나온 개선율이 이력서 목표 문장의 수치를 채운다.

**재사용.** 진단 기법(GC 로그 판독·heap dump histogram·누수 추적)은 [`jvm-practice/ch04-troubleshooting`](file:///Users/simbohyeon/jvm-practice/ch04-troubleshooting)의 실습 자산을 근거로 한다.

**끝났다고 보는 기준.** `RESULTS.md`에 baseline과 tuned 두 회차의 수치가 같은 부하 기준으로 채워지고, 개선이 GC 로그와 덤프로 설명된다.

## 3차 — 학습편 저작

2차의 실측을 학습 노트 1편으로 정리한다.

- `write/07_devops/02_Jenkins/06_infra/`에 `01-04.…JVM 튜닝·진단…` 신규 1편을 저작한다. 번호대는 `01-01`(용량)·`01-02`(배포)·`01-03`(IaC) 다음의 빈자리다.
- 본문 근거는 오직 `RESULTS.md`의 실측이다. 측정하지 않은 것은 쓰지 않는다 (NFR-4 정직성).
- **중복 회피 게이트.** 측정 토폴로지나 용량 산정을 또 설명하고 있으면 범위를 벗어난 것이다. 그 내용은 `05-07`·`01-01 §4`로 링크하고, 이 편은 튜닝·진단 루프만 다룬다.

## 진입점

다음 세션은 1차부터 시작한다. seed `_practice/poc/`의 docker-compose와 `05-07 §6`의 부하 스크립트가 출발점이며, 그 둘을 건드리지 않고 이 폴더 안에서 확장본을 만드는 것이 1차의 범위다. 고도화를 얹고 싶으면 [`enhancements.md`](enhancements.md)에서 하나를 골라 해당 단계에 끼운다.
