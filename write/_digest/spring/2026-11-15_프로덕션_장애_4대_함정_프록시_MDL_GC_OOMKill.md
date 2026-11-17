> 출처: NotebookLM · 2026-11-15 · 프로덕션 백엔드·인프라 장애 아키텍처 심층 분석 리포트 (영상 4편 통합) · 분야: spring-keywords, data-keywords, jvm-keywords, k8s-keywords · 미검증

## 요점

한 줄: 어노테이션·`ALTER`·YAML 한 줄은 아래 엔진(프록시·DB 락 매니저·JVM·커널)에 내리는 명령이라, 그 엔진이 어떻게 멈추고 잠그는지 알아야 한다고 봅니다.

- 프록시: 예외가 났는데 주문만 커밋되고 결제는 빠졌습니다. `this.save()` 가 프록시를 건너뛰어 트랜잭션이 아예 시작되지 않았기 때문입니다.
- 프록시 대응: 트랜잭션 메서드를 다른 빈(`OrderTxService`)으로 빼서 밖에서 부르게 합니다. `@Async`·`@Cacheable`·`@Retryable` 도 같은 제약을 받습니다.
- MDL: 끝나지 않은 트랜잭션이 테이블을 붙든 상태에서 `ALTER TABLE` 을 실행했습니다. DDL 이 MDL 을 기다리기 시작하자 뒤의 SELECT 까지 모두 줄을 서 서비스가 멈췄다고 합니다.
- MDL 대응: 실행 중 트랜잭션을 먼저 확인하고, `lock_wait_timeout` 을 짧게 둡니다. `INSTANT` DDL 이나 `pt-online-schema-change`·`gh-ost` 를 씁니다.
- MDL 주의: `INSTANT` 도 MDL 을 잠깐 잡아야 합니다. 그래서 긴 트랜잭션이 있으면 같은 대기 큐 문제가 생깁니다.
- GC: Full GC 가 2~3초 멈춘 동안 Liveness Probe(타임아웃 1초 × 3회)가 실패해 Pod 가 재시작됐다고 합니다. 남은 Pod 로 부하가 몰려 GC 가 이어지고 차례로 죽었습니다.
- GC 대응: 일시적 지연은 Readiness 로 트래픽만 빼고, Liveness 는 정말 멈춘 상태만 잡도록 느슨하게 둡니다. 저지연 GC(ZGC·Shenandoah)도 검토합니다.
- OOMKill: 힙 512MB 가운데 380MB 가 남았는데 하루 십수 번 재시작됐다고 합니다. 쿠버네티스는 힙이 아니라 컨테이너 전체 메모리(힙 + Off-Heap)를 봅니다.
- OOMKill 대응: memory limit 을 무작정 올리면 이웃 Pod 축출을 부릅니다. Off-Heap 영역마다 JVM 플래그로 상한을 걸라고 권합니다.
- 찾을 키워드: `performance_schema.metadata_locks`, `Waiting for table metadata lock`, `Generational ZGC`, `startupProbe`, `Load Shedding` 입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| Self-invocation | 같은 클래스 안 `this.save()` 호출이 프록시를 건너뛰어 트랜잭션이 시작되지 않는 문제 | [Spring과 디자인 패턴](../../09_spring/01_core/01-02.Spring과 디자인 패턴.md), [AOP — 프록시로 풀어내기](../../09_spring/05_aop/01-01.횡단 관심사와 AOP — 프록시로 풀어내기.md) |
| `AopContext.currentProxy()`·AspectJ | 자기 프록시를 꺼내 부르는 우회책과, 컴파일 때 코드를 엮어 프록시가 필요 없는 방식 | [Spring과 디자인 패턴](../../09_spring/01_core/01-02.Spring과 디자인 패턴.md) (일부: AopContext 만, AspectJ 위빙 없음) |
| 메타데이터 락 (MDL) | 테이블 구조를 바꾸는 동안 다른 세션이 그 테이블을 쓰지 못하게 MySQL 이 거는 잠금 | |
| MDL 대기 큐 | `ALTER TABLE` 이 끝나지 않은 트랜잭션을 기다리기 시작하면 뒤에 오는 일반 쿼리까지 그 뒤에 줄을 서는 현상 | |
| Online DDL·`ALGORITHM=INSTANT` | 테이블을 복사하지 않고 메타데이터만 바꿔 컬럼을 더하거나 빼는 MySQL 8.0 방식 | |
| `pt-online-schema-change`·`gh-ost` | 새 테이블로 데이터를 옮겨 스키마를 바꾸는 도구로, 트리거로 따라잡느냐 binlog 로 따라잡느냐가 다름 | |
| `lock_wait_timeout` | 메타데이터 락을 기다리는 최대 시간으로, 짧게 두면 DDL 이 줄을 오래 막지 않고 실패함 | |
| Full GC·Stop-The-World | 모든 애플리케이션 스레드를 멈추고 힙 전체를 정리하는 GC 와 그 정지 구간 | [tsj 11-03](../../01_language/book/tsj_troubleshooting-java/11-03.GC 로그로 문제 진단 네 시나리오.md) |
| ZGC·Shenandoah | 대부분의 작업을 애플리케이션과 동시에 해 정지 시간을 밀리초 아래로 줄이는 저지연 GC | [jpf 06-05](../../01_language/book/jpf_java-performance/06-05.실험 GC — ZGC·Shenandoah·Epsilon과 선택 가이드.md) |
| Liveness·Readiness Probe | 실패하면 컨테이너를 재시작하는 검사와, 실패하면 트래픽에서만 빼는 검사 | [kubernetes-in-action 06-02](../../08_cloud/book/kubernetes-in-action/06-02.liveness·startup probe로 컨테이너 건강 유지.md), [11-03](../../08_cloud/book/kubernetes-in-action/11-03.엔드포인트·DNS·토폴로지·readiness.md) |
| 연쇄 장애 (Cascading Failure) | 한 Pod 가 죽으면 남은 Pod 로 부하가 몰려 차례로 무너지는 현상 | [tsj 12-03](../../01_language/book/tsj_troubleshooting-java/12-03.시스템 장애 모드 — cascading·retry·timeout.md) |
| `OOMKilled`·cgroup `memory.max` | 컨테이너 메모리가 한도를 넘으면 커널이 `SIGKILL` 로 끝내고 종료 코드 137 을 남기는 동작 | [OOMKilled 사례](../../08_cloud/docs/kubernetes/operations/OOMKilled 사례 — Endowus Rebalance 서비스.md), [container-security 03-01](../../08_cloud/book/container-security/03-01.Control Group — 자원을 제한해 굶기기를 막다.md) |
| Off-Heap (Metaspace·Direct Buffer·Thread Stack·Code Cache) | 힙 밖에서 JVM 이 쓰는 메모리로, 힙이 여유로워도 컨테이너 RSS 를 키움 | [힙 밖에서 쌓이는 메모리](../../troubleshooting/_concepts/runtime-힙-밖에서-쌓이는-메모리.md) |
| Native Memory Tracking (NMT) | `-XX:NativeMemoryTracking=summary` 와 `jcmd <pid> VM.native_memory summary` 로 영역별 네이티브 메모리를 보는 기능 | [jpf 08-02](../../01_language/book/jpf_java-performance/08-02.Native Memory Tracking — NMT와 shared library 한계.md) |
| `MaxDirectMemorySize`·`MaxMetaspaceSize` | Off-Heap 영역마다 상한을 걸어, 커널 강제 종료 대신 JVM `OutOfMemoryError` 로 바꾸는 플래그 | [힙은 평평한데 몇 시간마다 죽는 컨테이너](../../troubleshooting/runtime/2026-09-14_힙은 평평한데 몇 시간마다 죽는 컨테이너.md) (일부: MaxDirectMemorySize 만, Metaspace 없음) |



## 자료와 실습

- 자료:
  - [Spring Framework Reference — Transaction Management & AOP Proxies](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html): 프록시 기반 AOP 의 자기 호출(Self-invocation) 제약과 `@Transactional` 전파 원리 명세입니다.
  - [MySQL 8.0 Reference Manual — Metadata Locking & Online DDL](https://dev.mysql.com/doc/refman/8.0/en/metadata-locking.html): 메타데이터 락 획득 우선순위 큐와 `ALGORITHM=INSTANT` 지원 연산 매트릭스 공식 명세입니다.
  - [Kubernetes Documentation — Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/): STW 현상과 실제 행(Hang) 상태를 구분해 프로브를 분리 설계하는 공식 가이드입니다.
  - [Java 21 Native Memory Tracking (NMT)](https://docs.oracle.com/en/java/javase/21/vm/native-memory-tracking.html): JVM Off-Heap 영역 구성과 저지연 가비지 컬렉터 튜닝 공식 레퍼런스입니다.
  - [Percona Database Performance Blog](https://www.percona.com/blog/): `performance_schema.metadata_locks` 로 장기 트랜잭션을 찾고 무중단 스키마 변경을 하는 실무 글이 모인 곳입니다. 리포트는 블로그 첫 화면만 걸었습니다.
  - [Spring 블로그](https://spring.io/blog): 리포트는 컨테이너 `memory.limits` 에서 Heap·Off-Heap 비율을 잡아 `OOMKilled` 를 막는 글로 소개합니다. 제목은 「Netflix TechBlog / Cloud Native Java」 인데 링크는 Spring 블로그 첫 화면이라 둘이 맞지 않습니다.
  - 『Real MySQL 8.0』 1권 4장(아키텍처)·5장(트랜잭션과 잠금)·11장(스키마 변경과 Online DDL): MySQL 엔진 아키텍처, 메타데이터 락(MDL)과 잠금 경합, Online DDL 내부 동작을 다룹니다.
  - 『Optimizing Java』 6장(가비지 컬렉션 기초)·7장(고급 가비지 컬렉션)·12장(동시성 및 메모리 성능 튜닝): JVM 메모리 모델, Stop-The-World 메커니즘, Full GC 와 Off-Heap RSS 폭증을 다룹니다.
  - 『Release It!』 2판 4장(안티패턴: 연쇄 장애)·5장(안정성 패턴): 단일 Pod 장애가 전체 다운으로 번지는 연쇄 장애 패턴과 격리·방어책을 다룹니다.
  - 코드: spring-framework `TransactionInterceptor.java` 와 `CglibAopProxy.java` 를 봅니다. percona-toolkit `pt-online-schema-change` 와 `gh-ost` 의 `go/logic/applier.go` 를 봅니다. openjdk `src/hotspot/share/services/memTracker.cpp` 와 linux `mm/memcontrol.c` 의 `mem_cgroup_out_of_memory` 도 봅니다.
- 실습:
  - Level 1: Java 21 과 Spring Boot 로 `@Transactional` 내부 호출(`this`)의 부분 커밋 버그를 재현하고 `PaymentTxService` 빈으로 분리합니다. 함정은 테스트 메서드에 `@Transactional` 이 붙어 있으면 자동 롤백돼 버그가 가려지는 것입니다. 완료: `this` 호출 시 `isActualTransactionActive() == false` 와 부분 커밋을 확인하고, 빈 분리 후 전체 롤백을 검증합니다.
  - Level 2: Heap `-Xmx128m`·한도 `256Mi` 환경에서 `allocateDirect()` 로 Direct Memory 를 지속 할당해 `OOMKilled` 를 재현하고 JVM 플래그로 방어합니다. 완료: `-XX:MaxDirectMemorySize=64m` 과 `-XX:MaxMetaspaceSize=64m` 을 적용해 커널 강제 종료 대신 JVM `OutOfMemoryError` 로 전환되고 RSS 가 한도를 넘지 않습니다.
  - Level 3: Kubernetes 에 2.5초 STW 지연 엔드포인트를 둔 클러스터에서 Probe 를 분리하고 MySQL 8.0 에서 MDL 대기열을 재현합니다. 완료: k6 부하 중에도 Pod 재시작 0회를 유지하고, MDL 경합 시 `lock_wait_timeout` 내에 안전하게 실패 처리됨을 입증합니다.



## 경고

- ⚠ Probe 계산: 쿠버네티스 기본 `periodSeconds` 는 10초입니다. 그래서 "1초 × 3회" 실패에는 정지 한 번이 아니라 약 30초에 걸친 연속 실패가 필요합니다. GC 정지가 반복됐거나 설정이 달랐을 것입니다(확인하지 않음).
- ⚠ Readiness 한계: Readiness 실패도 Pod 를 엔드포인트에서 빼므로 남은 Pod 로 부하가 몰립니다. Probe 분리만으로 연쇄를 다 막지는 못하고, 부하 차단·여유 용량이 함께 필요합니다.
- ⚠ INSTANT 버전: 컬럼 추가 `INSTANT` 는 8.0.12 부터 끝에만 됐고, 8.0.29 부터 아무 위치 추가와 `DROP COLUMN` 까지 됩니다(확인하지 않음).
- ⚠ 책 장 번호: 『Real MySQL 8.0』 "11장 스키마 변경과 Online DDL" 과 『Optimizing Java』 "12장 메모리 성능 튜닝" 은 목차와 대조하지 않았습니다. 그래서 요점에는 장 번호를 일부만 남겼습니다.
- ⚠ 소스 경로: `src/hotspot/share/services/memTracker.cpp` 는 옛 경로일 수 있습니다. 최근 JDK 는 NMT 코드를 `src/hotspot/share/nmt/` 로 옮겼습니다(확인하지 않음).
- ⚠ 자료 링크: "Netflix TechBlog — Tuning JVM Memory in Containers" 의 링크는 Spring 블로그 첫 화면이고, Percona 링크도 블로그 첫 화면뿐이라 넣지 않았습니다.
- ⚠ 겹침: Self-invocation 은 백엔드 핵심 메커니즘 요약과 겹칩니다. 이 요약에서는 롤백 누락 사례로만 다룹니다.
