# 요구사항 — Jenkins JVM Tuning Lab

이 문서는 랩이 갖춰야 할 것을 기능(FR)과 비기능(NFR)으로 나눠 정의한다. 로드맵의 각 단계는 여기 적힌 요구사항을 하나씩 충족시키는 방향으로 진행한다.

## 한 줄 정의

Spring Boot 앱을 Jenkins가 빌드·배포·호출하는 구조에서, JVM 병목을 부하로 재현하고 진단해, 튜닝 전후를 같은 부하로 측정하는 재현 가능한 실험 랩.

## 기본 아키텍처

기본 틀은 **Spring Boot ↔ Jenkins 호출 구조**다. 세 덩어리가 한 docker-compose 안에 묶인다.

```
[부하 스크립트] --(200건 트리거)--> [Jenkins Controller (JVM 튜닝 대상)]
                                          |
                                     (빌드·배포)
                                          v
                                   [Spring Boot 앱 (JVM 튜닝 대상)]
                                          |
                                    (Actuator /metrics)
                                          v
                        [Prometheus] --> [Grafana]  <-- Jenkins /prometheus/
```

튜닝 대상 JVM이 둘이라는 점이 이 랩의 특징이다. 하나는 Jenkins Controller이고, 다른 하나는 그 Controller가 배포하는 Spring Boot 앱이다. 두 JVM은 성격이 다르다. Controller는 큐·Run 객체를 heap에 이고 사는 장기 실행 프로세스라 GC pause와 heap 여유가 핵심이고, Spring Boot 앱은 요청을 받아 외부를 호출하는 처리량 중심이라 스레드 모델과 커넥션풀이 핵심이다. 같은 "JVM 튜닝"이라도 어디를 만지느냐에 따라 보는 지표가 갈린다.

## 이력서 목표 문장

2차에서 before/after 수치가 확보되면 이력서 한 줄로 직결된다. 수치가 채워지기 전에는 이 문장을 이력서에 올리지 않는다.

> Jenkins Controller와 Spring Boot 앱의 JVM을 부하로 재현하고 GC 로그·thread dump로 진단해, G1 튜닝과 가상 스레드 전환으로 GC pause와 처리량을 개선 (재현 가능한 docker-compose 랩 + GitHub 공개)

## 기능 요구사항 (FR)

| # | 요구사항 | 상세 | 근거·재사용 |
|---|----------|------|------------|
| FR-1 | JVM 프로파일 토글 | Jenkins Controller와 Spring Boot 앱 각각에 baseline/tuned 두 프로파일을 두고 환경변수 하나로 전환한다. baseline은 병목을 끌어내도록 힙을 일부러 작게 두고, tuned는 힙 상향·G1 파라미터·Metaspace 상한으로 대응한다 | seed의 `JAVA_OPTS=-Xmx1g -Xms512m`을 출발점으로 |
| FR-2 | GC·safepoint 로깅 | 두 JVM 모두 `-Xlog:gc*,safepoint`로 GC pause와 safepoint 동기화를 파일에 남긴다. pause가 GC 때문인지 safepoint 때문인지 가릴 수 있어야 한다 | `01-01 §4`의 플래그 카탈로그를 실측으로 검증 |
| FR-3 | Spring Boot 앱 빌드·배포 | Jenkins가 대상 Spring Boot 앱을 빌드해 로컬 레지스트리에 올리고 배포한다. seed의 Go sample-app은 건드리지 않고, Spring Boot 앱을 별도 대상으로 추가한다 | seed `docker-compose.yml`의 registry·agent 재사용 |
| FR-4 | 부하 재현 | 두 종류의 부하를 건다. 하나는 Jenkins에 200건 트리거를 쏘아 Controller heap을 밀어 올리는 부하, 다른 하나는 Spring Boot 앱 엔드포인트에 동시 요청을 보내 스레드·커넥션풀을 압박하는 부하다 | `05-07 §6-3`의 crumb + `seq 1 200` 트리거 스크립트 그대로 |
| FR-5 | 덤프 채취 | 부하 중·후에 thread dump와 heap dump를 채취하는 스크립트를 둔다. thread dump로 빌드 행·블로킹 지점을, heap dump histogram으로 객체 점유를 본다 | `jvm-practice/ch04-troubleshooting` 진단 기법 |
| FR-6 | 관측 스택 | Prometheus가 Jenkins `/prometheus/`와 Spring Boot Actuator `/actuator/prometheus`를 함께 스크랩하고, Grafana가 두 JVM을 한 대시보드에서 보여 준다 | `06_observability/05_SpringActuator` 연동 노트 |
| FR-7 | before/after 산출 | 같은 부하를 baseline과 tuned에 각각 걸어, GC pause·처리량·heap 사용률의 두 회차 수치를 `RESULTS.md`에 표로 남긴다 | 이력서 목표 문장의 수치가 여기서 나온다 |

## 비기능 요구사항 (NFR)

| # | 요구사항 | 판단 기준 |
|---|----------|-----------|
| NFR-1 | 재현성 | 남이 저장소를 받아 `docker compose up` 한 번으로 랩 전체가 뜬다. 수동 설치 단계가 남으면 실패다. 공개 저장소 링크가 이력서 주장의 근거이므로 재현성이 최우선이다 |
| NFR-2 | 결정성 | before와 after에 *같은* 부하를 건다. 부하 스크립트·트리거 수·앱 시나리오가 두 회차에서 동일해야 수치 비교가 성립한다 |
| NFR-3 | 관측 즉시성 | 수 초짜리 스파이크를 놓치지 않는다. Prometheus 플러그인의 기본 수집 주기가 120초라, 순간 큐 길이·heap 스파이크는 `/metrics` 서블릿을 직접 봐야 한다 (`05-07 §1` 캐비엇) |
| NFR-4 | 정직성 | 측정하지 않은 수치는 문서에 적지 않는다. `RESULTS.md`가 채우기 전까지 개선율은 `{측정 필요}`로 남긴다. 검증하지 않은 기법은 "했다"가 아니라 "설계·검토" 톤으로만 쓴다 |
| NFR-5 | 공개 적합성 | 저장소에 자격증명·내부 IP·회사 식별 정보가 없다. 부하 대상은 로컬 Jenkins와 예제 앱뿐이라 실무 코드와 무관하게 공개할 수 있다 |

## 범위 밖

측정 토폴로지·지표 카탈로그·용량 산정식은 이 랩이 다시 설명하지 않는다. 그것은 `05-07`과 `01-01 §4`가 이미 다루므로 링크로 잇는다. 같은 내용을 다시 쓰지 않는 것이 격차를 메우는 신규 작업의 조건이다. 이 랩이 다루는 것은 오직 *튜닝·진단 루프*다.
