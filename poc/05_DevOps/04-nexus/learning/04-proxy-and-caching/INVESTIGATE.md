# Ch04: 프록시와 캐싱 전략 — 심화 탐구

> LEARN.md의 개념을 더 깊이 파고드는 Q&A

---

## Q1: Metadata Max Age를 너무 짧게 설정하면 생기는 문제는?

Metadata Max Age를 5분으로 설정했다고 하자. 20명의 개발자가 하루 평균 10번씩 빌드하면, 매 빌드마다 메타데이터 캐시가 만료되어 있을 가능성이 높다. 의존성이 200개인 프로젝트라면, 한 번의 빌드에서 최대 200건의 메타데이터 요청이 Maven Central로 나간다. 하루 총 200 × 200 = 40,000건의 외부 요청이 발생하는 셈이다.

문제는 세 가지다. 첫째, **빌드 속도 저하**. 메타데이터 파일은 작지만(수 KB), HTTP 왕복 시간(RTT)은 파일 크기와 무관하다. 한국에서 Maven Central(US)까지 RTT가 200ms라면 200개 × 200ms = 40초가 메타데이터 확인에만 소비된다. 실제로는 HTTP 커넥션 재사용(keep-alive)으로 좀 나아지지만, 체감할 수 있는 수준의 지연이 발생한다.

둘째, **외부 저장소 rate limit**. npmjs.org나 Docker Hub는 단위 시간당 요청 수를 제한한다. 메타데이터 요청이 이 한도를 소진하면 실제 아티팩트 다운로드가 거부될 수 있다. 특히 Docker Hub의 free tier는 6시간당 100회(anonymous) 제한이 있으므로, 메타데이터 조회만으로도 한도를 금방 채울 수 있다.

셋째, **장애 노출 면적 증가**. 메타데이터를 자주 확인할수록 외부 장애에 영향받을 빈도가 높아진다. 1440분(24시간) 주기라면 하루 한 번 외부를 확인하고, 그 사이에 장애가 발생해도 캐시로 버틸 수 있다. 5분 주기라면 하루 288번 외부에 의존하며, 그만큼 장애에 취약하다.

1440분(24시간)이 기본값인 이유가 여기 있다. 대부분의 프로젝트에서 의존성 버전은 하루에 한두 번 바뀌면 많은 편이니까. 새 라이브러리가 급히 필요하면 캐시 무효화로 해결하고, 일상적인 빌드에서는 기본값으로 충분하다.

---

## Q2: Negative Cache TTL과 빌드 실패의 관계는?

Negative cache는 "없다"는 응답을 캐싱한다. 이것이 의도치 않은 빌드 실패를 유발하는 시나리오가 있다.

팀원 A가 내부 라이브러리 `com.mycompany:auth-sdk:2.0.0`을 개발 중이다. 팀원 B가 이 라이브러리를 의존성에 추가하고 빌드했지만, A가 아직 deploy하지 않아서 Nexus에서 404가 반환됐다. 이 404가 negative cache에 저장된다. 30분 후 A가 deploy를 완료했지만, B가 다시 빌드해도 여전히 404가 나온다. negative cache의 TTL(기본 1440분)이 남아 있기 때문이다.

이런 상황이 반복되면 팀에서 "Nexus가 이상하다"는 불신이 생긴다. 해결 방법은 세 가지다. 하나는 negative cache의 TTL을 짧게(60-120분) 설정하는 것이고, 두 번째는 deploy 직후 해당 경로의 캐시를 수동으로 무효화하는 것이다. 세 번째이자 가장 체계적인 방법은 CI 파이프라인에서 deploy 후 자동으로 캐시를 무효화하는 API 호출을 추가하는 것이다:

```bash
# deploy 후 negative cache 무효화 (CI 스크립트에 추가)
curl -u $NEXUS_USER:$NEXUS_PASS -X DELETE \
  "$NEXUS_URL/service/rest/v1/repositories/maven-central/invalidate-cache"
```

근본적으로는 **hosted에 올라간 아티팩트는 negative cache와 무관하다**는 점을 이해해야 한다. negative cache는 proxy 리포지토리에만 적용된다. group을 통해 요청하면 hosted를 먼저 탐색하므로, hosted에 있는 아티팩트가 negative cache에 가려지지는 않는다. 문제가 되는 건 proxy에서 찾아야 하는 외부 아티팩트, 또는 아직 hosted에 올라가지 않은 내부 아티팩트뿐이다.

---

## Q3: Auto-blocking이 트리거되는 조건과 해제 방법은?

Auto-blocking은 원격 저장소 연결 실패가 **연속으로** 발생할 때 트리거된다. 정확한 임계값은 Nexus 버전마다 다르지만, 일반적으로 connection timeout이나 HTTP 5xx 응답이 여러 번 반복되면 해당 proxy를 blocked 상태로 전환한다.

blocked 상태에서 Nexus는 주기적으로(기본 300초 간격) 원격 저장소에 재연결을 시도한다. 성공하면 자동으로 online으로 돌아간다. 이 "자동 복구" 덕분에 관리자가 새벽에 깨어나 수동 해제할 필요가 없다.

수동 해제가 필요한 경우도 있다. 원격 저장소의 URL이 변경되었거나, 인증 정보가 만료되어 auto-retry가 계속 실패하는 상황이다. 이때는 원인을 수정한 뒤 `Administration → Repositories → [proxy] → Health check` 에서 상태를 online으로 변경한다. REST API로도 가능하다:

```bash
# proxy 상태를 online으로 변경
curl -u admin:pass -X PUT \
  -H "Content-Type: application/json" \
  -d '{"online": true}' \
  "https://nexus.example.com/service/rest/v1/repositories/maven-central"
```

운영 팁: proxy 상태를 모니터링 시스템(Prometheus, Grafana)에 연동해두면 blocked 전환 시 즉시 알림을 받을 수 있다. Nexus의 `/service/rest/v1/repositories` API에서 proxy 상태를 조회할 수 있으므로, 스크립트로 주기적 점검하는 방법도 실용적이다. blocked 상태가 30분 이상 지속되면 Slack 알림을 보내는 식의 자동화를 구성하면 운영 부담이 줄어든다.

---

## Q4: Air-gapped 환경에서 의존성을 효율적으로 반입하는 방법은?

proxy 리포지토리를 만들되, 원격 URL을 실제 외부 저장소가 아닌 **내부의 다른 Nexus 인스턴스**를 가리키게 하는 방법이 있다. 이 "내부 원본 Nexus"에 아티팩트를 주기적으로 반입하면, 격리 환경의 proxy가 이 내부 원본에서 캐싱하는 구조가 된다.

실제 구현은 이렇다. DMZ(비무장지대)에 "중개 Nexus"를 두고, 외부 인터넷과 내부 네트워크 양쪽에서 접근 가능하게 한다. 중개 Nexus의 proxy가 Maven Central을 캐싱하고, 내부 Nexus의 proxy가 중개 Nexus를 바라본다. 방화벽 규칙은 내부→DMZ 단방향만 열면 된다.

완전히 물리적으로 격리된 환경이라면 proxy 자체가 무의미하다. hosted에 직접 아티팩트를 넣는 수밖에 없는데, 이때 가장 효율적인 방법은 **인터넷 환경에서 프로젝트 빌드를 실행하여 로컬 캐시를 채운 뒤 통째로 업로드하는 것**이다. `~/.m2/repository/`에는 전이 의존성까지 빠짐없이 포함되므로 하나씩 올리는 것보다 누락이 줄어든다.

의존성이 변경될 때마다 이 과정을 반복해야 하므로, 자동화가 필수다. "의존성 목록 추출 → 인터넷 환경에서 다운로드 → 물리 매체로 전달 → Nexus에 업로드"를 스크립트화하고, 변경 감지를 `package-lock.json`이나 `gradle.lockfile`의 diff로 판단하면 불필요한 반입을 줄일 수 있다.

---

## Q5: Maven SNAPSHOT의 캐싱과 RELEASE 캐싱의 차이는?

근본적인 차이는 **동일 좌표의 내용이 바뀔 수 있느냐**다.

RELEASE `commons-lang3:3.14.0`은 한번 릴리스되면 영원히 같은 바이너리다. 캐시를 무기한 유지해도 절대 stale(오래된 캐시)이 되지 않는다. 이것이 Content Max Age를 -1로 설정하는 근거다. 3년 후에 같은 버전을 요청해도 캐시에서 바로 반환하면 된다.

SNAPSHOT `my-lib:1.0-SNAPSHOT`은 개발자가 deploy할 때마다 내용이 바뀐다. Maven은 SNAPSHOT을 `1.0-20240301.143052-7` 같은 타임스탬프 버전으로 저장하는데, 클라이언트가 "최신 SNAPSHOT"을 요청하면 `maven-metadata.xml`에서 가장 최근 타임스탬프를 찾아서 반환한다.

proxy에서 외부 SNAPSHOT을 캐싱하는 경우(드물지만 오픈소스 프로젝트의 SNAPSHOT 저장소를 proxy할 때), 메타데이터와 아티팩트 모두 짧은 Max Age가 필요하다. 그렇지 않으면 오래된 SNAPSHOT이 계속 내려오는데, 이건 "최신 개발 버전"을 쓰려는 SNAPSHOT의 목적 자체를 부정하는 셈이다.

실무 권장: 외부 SNAPSHOT proxy는 가능한 피하라. 외부 프로젝트의 SNAPSHOT에 의존하면 빌드 재현성이 보장되지 않는다. 어제 잘 되던 빌드가 오늘 실패할 수 있고, 원인은 외부 프로젝트에서 SNAPSHOT을 바꿨기 때문이다. 꼭 필요하다면 특정 시점의 SNAPSHOT을 hosted에 올려서 "고정"하는 것이 더 안전한 접근이다. 이를 "SNAPSHOT pinning"이라 부르기도 한다.

---

## Q6: 여러 proxy를 group으로 묶었을 때 캐시 충돌 가능성은?

group은 멤버를 순서대로 탐색한다. 같은 좌표의 아티팩트가 두 proxy에 모두 캐시되어 있다면, 순서가 앞인 proxy의 캐시가 반환된다. 이것 자체는 문제가 아니다.

문제가 되는 경우는 두 proxy가 **다른 버전의 메타데이터**를 캐시하고 있을 때다. 예를 들어 Maven Central proxy와 JCenter proxy(현재는 읽기 전용)를 group에 묶었다고 하자. `commons-lang3`의 최신 버전이 Maven Central에서는 3.14.0인데, JCenter 캐시에는 오래된 메타데이터로 3.12.0까지만 보인다면? group이 JCenter를 먼저 탐색하면 3.14.0이 안 보일 수 있다.

Nexus는 이를 완화하기 위해 group의 메타데이터를 **멤버 전체에서 병합(merge)**한다. 각 proxy의 `maven-metadata.xml`을 가져와서 버전 목록을 합친 결과를 반환하는 것이다. 하지만 병합 시점은 메타데이터 캐시 유효기간에 의존하므로, 각 proxy의 Metadata Max Age가 다르면 병합 결과가 일시적으로 불일치할 수 있다.

이 문제를 예방하는 방법은 간단하다. 같은 생태계의 proxy를 최소한으로 유지하고, 모든 proxy의 Metadata Max Age를 동일하게 설정하는 것이다. Maven이라면 Maven Central proxy 하나면 대부분 충분하고, 특수한 저장소(Spring Milestone, JBoss 등)가 필요할 때만 추가한다.

---

## Q7: Docker Hub rate limit을 Nexus proxy로 효과적으로 회피하는 방법은?

Docker Hub의 rate limit은 pull 요청 기준이다. Anonymous는 6시간당 100회, Free 인증은 200회, Pro는 5,000회. 핵심은 Nexus proxy를 통하면 **여러 클라이언트의 pull이 하나의 외부 요청으로 대체**된다는 점이다.

20명 개발자가 `openjdk:17-slim`을 pull한다고 하자. proxy가 없으면 20번의 Docker Hub 요청이 발생하지만, proxy가 있으면 첫 번째 요청만 외부로 나가고 나머지 19번은 캐시에서 서빙된다. rate limit 소비는 1회로 줄어든다.

추가로 Docker proxy에 인증 계정을 설정하면 rate limit이 IP 기준이 아닌 계정 기준으로 적용된다. 사무실 NAT 뒤에 20명이 있으면 IP는 하나이므로 100회를 공유하지만, 인증 계정은 개별 한도를 갖는다.

실무 구성 포인트:
1. Docker proxy에 유료 계정(Pro/Team) 인증 설정 → rate limit 5,000회 확보
2. CI 빌드도 반드시 proxy를 통하게 설정 (`daemon.json`의 `registry-mirrors`)
3. Content Max Age -1 유지 → RELEASE 태그(`openjdk:17.0.9-slim`)는 불변이므로 무기한 캐시
4. `latest` 같은 mutable 태그는 주의 → 주기적으로 캐시 갱신이 필요할 수 있음

---

## 심화: 글로벌 팀이 여러 리전에 Nexus를 둘 때 캐시 전략은?

서울, 프랑크푸르트, 버지니아에 개발팀이 있다고 하자. 각 리전에 Nexus 인스턴스를 두는 것이 빌드 속도 측면에서 유리하다. 문제는 hosted 아티팩트의 동기화와 캐시 일관성이다.

**Nexus Pro의 Replication** 기능을 쓰면 한 인스턴스의 hosted 아티팩트를 다른 인스턴스로 자동 복제할 수 있다. 서울에서 deploy한 내부 라이브러리가 프랑크푸르트와 버지니아에도 자동으로 전파되는 것이다.

OSS에서는 이런 선택지가 있다. 첫째, **단일 원본(Single Source of Truth) 패턴**. hosted는 서울 Nexus에만 두고, 다른 리전의 Nexus는 서울 Nexus를 proxy한다. 내부 라이브러리도 proxy 캐싱의 대상이 되므로, 첫 요청만 서울까지 가고 이후는 로컬 캐시에서 서빙된다. 단점은 서울 Nexus가 SPOF(Single Point of Failure)라는 것이다.

둘째, **CI 기반 멀티 배포**. CI 파이프라인에서 deploy를 세 리전의 hosted에 동시에 수행한다. 일관성은 보장되지만 배포 스크립트가 복잡해진다. 한 리전의 deploy가 실패하면 부분적 불일치가 생길 수 있으므로 배포 후 검증 단계가 필요하다.

캐시 전략은 리전별로 독립 운영하되, Content Max Age는 동일하게 -1로 유지한다. Metadata Max Age는 각 리전의 빌드 패턴에 맞게 조정하되, 너무 큰 차이를 두면 "서울에서는 보이는데 프랑크푸르트에서는 안 보여요"라는 혼란이 생기므로 전 리전 동일 값을 쓰는 것이 관리가 편하다. 결국 멀티 리전 운영의 복잡성은 Nexus Pro의 비용을 정당화하는 주요 근거 중 하나다.
