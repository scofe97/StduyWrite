# Ch11. 모니터링과 트러블슈팅 — 심화 탐구

## Q1. Nexus의 Prometheus 엔드포인트는 기본으로 활성화되어 있는가?

아니다. Nexus 3의 Prometheus 메트릭 엔드포인트(`/service/metrics/prometheus`)는 기본 비활성 상태다. `nexus.properties`에 `nexus.metrics.enabled=true`를 명시적으로 추가해야 활성화된다. 이 설계는 보안과 성능 양쪽을 고려한 결과인데, 메트릭 엔드포인트가 내부 상태를 노출하고, 수집 자체가 미세한 오버헤드를 발생시키기 때문이다.

Docker 환경에서의 설정 방법을 구체적으로 살펴보면, `nexus-data/etc/nexus.properties` 파일을 직접 마운트하는 방식이 권장된다. 설정 후 `curl -u admin:admin123 http://localhost:8081/service/metrics/prometheus`로 응답이 오는지 확인하면 된다. 응답이 없다면 Nexus 재시작이 필요할 수 있다.

프로덕션에서는 활성화하되, 인증(Basic Auth)을 반드시 설정하고 네트워크 레벨에서 Prometheus 서버만 접근 가능하도록 제한해야 한다. Prometheus의 `scrape_configs`에서 `basic_auth` 블록으로 인증 정보를 넣고, Nexus 앞단 Reverse Proxy에서 `/service/metrics/` 경로를 Prometheus IP만 허용하는 ACL을 거는 식이다.

메트릭이 노출하는 정보에는 JVM 힙 사용량, HTTP 요청 수, Blob Store 용량 등이 포함되어 있어서, 외부에 공개되면 인프라 구조를 추론할 수 있는 단서가 된다.

---

## Q2. JVM Heap과 DirectMemory를 합쳐 컨테이너 메모리 제한과 맞추는 공식은?

공식은 `Container Memory Limit = Heap(-Xmx) + DirectMemory(-XX:MaxDirectMemorySize) + Metaspace + Thread Stacks + OS Overhead`다. 실무에서 자주 쓰는 간이 공식은 `Xmx * 2 + 512MB` 정도를 컨테이너 제한으로 잡는 것이다.

각 구성 요소를 분해해 보자. Heap은 `-Xmx`로 지정한 값 그대로다. DirectMemory는 Nexus가 Blob I/O에 NIO를 사용하므로 Heap의 50~100% 수준으로 잡는 게 일반적이다. Metaspace는 OSGi 번들 수에 비례하는데, 보통 256~512MB면 충분하다.

Thread Stack은 스레드당 1MB가 기본이고, Nexus가 동시 요청 처리를 위해 200~400개 스레드를 사용하므로 200~400MB가 필요하다. OS Overhead는 커널 매핑, JNI 라이브러리, 각종 native 코드용으로 300~500MB를 잡아야 한다.

구체적으로 Heap 2GB 환경을 계산하면 이렇다: 2G(Heap) + 2G(Direct) + 0.3G(Metaspace) + 0.3G(Threads) + 0.4G(OS) = 5.0GB. 컨테이너 제한을 5GB로 딱 맞추면 스파이크 때 OOMKill이 발생하니, 20% 여유를 두고 6GB로 설정하는 것이 안전하다.

왜 이 여유가 필요할까? JVM은 GC 직전에 일시적으로 Heap 사용량이 `-Xmx` 근처까지 올라가고, 이 시점에 Direct Memory도 피크를 치면 합산 메모리가 순간적으로 예상치를 초과할 수 있기 때문이다.

---

## Q3. request.log에서 느린 요청을 찾는 방법은?

request.log의 마지막 필드가 응답 시간(밀리초)이다. 로그 한 줄의 구조는 대략 `IP - user [timestamp] "METHOD /path HTTP/1.1" status size elapsed_ms` 형태인데, 정확한 포맷은 Nexus 버전에 따라 다를 수 있으므로 먼저 샘플 줄을 확인하는 게 좋다.

기본적인 분석 명령어부터 살펴보자. 3초 이상 걸린 요청을 찾으려면 `awk '$NF > 3000' request.log`를 쓰면 된다. 가장 느린 상위 20개를 뽑으려면 `awk '{print $NF}' request.log | sort -n | tail -20`이 유용하다.

평균 응답 시간은 `awk '{sum+=$NF; count++} END {print sum/count}' request.log`로 계산할 수 있다. 특정 리포지토리만 느린지 확인하려면 `grep '/repository/maven-central/' request.log | awk '$NF > 3000'`처럼 URL 경로 기준으로 grep을 조합하면 된다.

시간대별 느린 요청 분포도 유용하다. `awk '$NF > 3000 {print substr($4,2,14)}' request.log | sort | uniq -c | sort -rn | head`는 느린 요청이 특정 시간대에 몰리는지 보여주는데, Scheduled Task가 돌아가는 시간대와 겹치면 원인이 명확해진다.

만약 request.log에 응답 시간이 기록되지 않는다면, `$NEXUS_DATA/etc/logback/logback-access.xml`에서 `%D`(밀리초) 또는 `%T`(초) 패턴이 포함되어 있는지 확인해야 한다.

---

## Q4. GC 로그를 활성화하여 Full GC 빈도를 모니터링하려면?

JVM 옵션에 `-Xlog:gc*:file=/nexus-data/log/gc.log:time,uptime:filecount=10,filesize=10m`을 추가하면 된다(Java 11+). Docker 환경에서는 `INSTALL4J_ADD_VM_PARAMS` 환경변수에 이 옵션을 넣는다.

Java 8 환경이라면 `-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:/nexus-data/log/gc.log`를 사용해야 하지만, 현재 Nexus 3은 Java 11+이므로 Unified Logging 형식을 쓰는 게 맞다.

활성화 후 `grep 'Pause Full' gc.log`로 Full GC 발생을 확인할 수 있고, `grep -c 'Pause Full' gc.log`로 총 횟수를 셀 수 있다. Full GC가 시간당 2~3회 이상이면 Heap 증설을 고려해야 한다.

더 정밀한 분석이 필요하면 GCViewer나 GCEasy(gceasy.io) 같은 도구에 gc.log를 업로드하면 GC 빈도, pause time 분포, heap 사용 추이를 시각적으로 볼 수 있다.

GC 로그에서 특히 주의해서 볼 지표가 두 가지 있다. 첫째는 "Allocation Failure"로 인한 Young GC 빈도인데, 이것이 초당 여러 번이면 `-Xmn`(Young Gen 크기)을 늘려야 한다.

둘째는 Full GC의 "Pause" 시간이다. 1초를 넘기면 사용자 요청이 멈추는 것이므로 G1GC의 `-XX:MaxGCPauseMillis`를 튜닝하거나, Heap을 더 크게 잡아야 한다.

GC 로그 자체의 성능 오버헤드는 무시할 수준이므로, 프로덕션에서도 항상 켜두는 것을 권장한다.

참고로, GC 로그 파일이 디스크를 과도하게 점유하는 것을 방지하기 위해 `filecount`와 `filesize` 옵션을 반드시 설정해야 한다. 위 예시에서 `filecount=10,filesize=10m`은 10MB 파일 10개를 로테이션하며 최대 100MB를 사용한다는 뜻이다.

---

## Q5. Nexus Task가 실행 중일 때 성능 저하가 발생하는 이유는?

Nexus의 Scheduled Task(Compact Blob Store, Rebuild Index, Cleanup 등)는 메인 애플리케이션과 같은 JVM에서 실행된다. 별도 프로세스나 워커가 아니라 동일한 스레드 풀에서 돌아가기 때문에, 무거운 Task가 실행되면 사용자 요청 처리에 쓸 수 있는 리소스가 줄어든다.

각 Task별로 어떤 리소스를 집중적으로 사용하는지 구분하면 대응이 수월해진다.

**Compact Blob Store**는 삭제 마킹된 블롭을 실제로 정리하면서 대량의 디스크 I/O를 발생시킨다. 수십 GB의 blob이 삭제 대상이면 compact 과정에서 디스크 write가 폭증하고, 같은 디스크에서 아티팩트를 다운로드하려는 사용자 요청은 I/O wait로 느려진다.

**Rebuild Index**는 DB(H2/OrientDB)를 집중적으로 사용하면서 DB 락 경합을 유발할 수 있다. 메타데이터를 전수 스캔하면서 인덱스를 재구성하므로, 이 동안 리포지토리 브라우징이나 검색이 느려진다.

**Cleanup Policy Task**는 대량의 컴포넌트를 순회하면서 삭제 대상을 판별하는데, 컴포넌트 수가 수만 개 이상이면 CPU와 메모리를 상당량 소비한다.

해결책은 명확하다. Task 스케줄을 업무 시간 밖(새벽 2~5시)으로 옮기고, 여러 Task가 동시에 실행되지 않도록 시간을 분산시키는 것이다. 예를 들어 Compact는 새벽 2시, Cleanup은 3시, Rebuild Index는 4시로 배치한다.

---

## Q6. Docker 환경에서 Nexus 로그를 중앙 로그 시스템(ELK)으로 보내려면?

세 가지 접근이 있다.

**첫째, Docker 로그 드라이버.** `--log-driver=fluentd`나 `--log-driver=gelf`를 설정하면 stdout 로그가 자동으로 전송된다. 설정이 간단하지만, Nexus의 stdout에는 nexus.log 내용만 나오고 request.log는 포함되지 않는다는 한계가 있다. JSON으로 구조화되지 않은 로그가 그대로 전송되므로 Logstash/Fluentd에서 grok 파싱이 추가로 필요하다.

**둘째, Filebeat 사이드카.** `/nexus-data/log/` 볼륨을 공유하여 nexus.log와 request.log를 직접 수집한다. docker-compose에서 Nexus와 Filebeat가 같은 volume을 마운트하도록 구성하면 된다. Filebeat의 `filebeat.inputs`에서 각 로그 파일별로 별도 input을 설정하고, request.log는 공백 구분자로 파싱하여 응답 시간, URL, HTTP 메서드 등을 별도 필드로 추출할 수 있다.

**셋째, Fluentd/Fluent Bit DaemonSet.** 쿠버네티스 환경에서 주로 사용한다. Pod의 stdout/stderr을 노드 레벨에서 수집하는 구조라 애플리케이션 변경이 불필요하다. 다만 request.log 같은 파일 기반 로그는 별도 sidecar로 수집해야 한다는 점은 동일하다.

실무에서는 두 번째 방식(Filebeat sidecar)을 권장하는 편인데, request.log의 응답 시간 필드를 숫자로 파싱하여 Kibana에서 느린 요청 대시보드를 만들 수 있고, nexus.log에서 ERROR/WARN 레벨만 필터링하여 알림을 설정하는 것도 가능하기 때문이다.

비용이 걱정된다면 Fluent Bit(경량)로 수집하고 직접 Elasticsearch로 보내는 구성도 괜찮다. Filebeat 대비 메모리 사용량이 1/10 수준이므로 사이드카로 띄우기에 부담이 적다.

---

## 심화 질문

> "Nexus가 갑자기 응답 불가가 됐을 때 5분 안에 원인을 파악하는 절차는?"

5분 타임박스라면 체계적인 진단 흐름이 필수다. 순서를 어기면 시간을 낭비하게 되니, 이 절차를 체화해두는 게 좋다.

**(1분) 프로세스 생존 확인.** `curl -s -o /dev/null -w '%{http_code}' http://localhost:8081/service/rest/v1/status/writable`로 HTTP 응답 코드를 확인한다. 200이면 살아있으나 느린 것이고, 연결 자체가 안 되면 프로세스가 죽었거나 포트가 막힌 것이다. `docker stats nexus`로 CPU/메모리 사용률도 한눈에 파악한다.

**(1분) 최근 에러 로그 확인.** `docker logs nexus --tail 50`으로 최근 에러를 본다. `OutOfMemoryError`가 있으면 힙 부족이 원인이고, `Cannot acquire lock`이면 DB 잠금 문제, `BlobStoreException`이면 디스크 문제다. 이 단계에서 원인의 80%가 드러나는 경우가 많다.

**(1분) JVM 상태 확인.** `jcmd $(pgrep -f nexus) GC.heap_info`로 힙 사용량을 본다. Old Gen이 90% 이상이면 Full GC 루프에 빠진 상태일 가능성이 높다.

**(1분) 디스크/Task 상태 확인.** `df -h /nexus-data`로 디스크 여유를 본다. 디스크가 100%이면 Nexus는 아무것도 할 수 없다. `curl -u admin:admin123 http://localhost:8081/service/rest/v1/tasks`로 현재 실행 중인 Task가 있는지도 확인한다.

**(1분) 트래픽 패턴 확인.** `request.log` 마지막 100줄에서 비정상 패턴을 탐색한다. `awk '{print $1}' request.log | tail -100 | sort | uniq -c | sort -rn`으로 IP별 요청 수를 빠르게 집계하면, 특정 IP의 폭주인지 전반적 과부하인지 구분할 수 있다.

이 5단계로 해결되지 않으면, thread dump(`jcmd $(pgrep -f nexus) Thread.print`)를 떠서 데드락이나 스레드 고갈을 확인하는 것이 다음 단계다. 모든 스레드가 WAITING 상태이고 특정 lock을 기다리고 있다면 데드락이 확정적이며, 이 경우 Nexus 재시작이 유일한 즉각 대응이다.
