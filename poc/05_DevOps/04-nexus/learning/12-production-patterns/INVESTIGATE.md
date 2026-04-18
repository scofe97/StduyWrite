# Ch12. 프로덕션 운영 패턴 — 심화 탐구

## Q1. Nexus HA(고가용성)의 Active-Active vs Active-Passive 방식 차이는?

Nexus Pro의 HA는 Active-Passive 방식이다. 하나의 노드가 모든 읽기/쓰기를 담당하고, 나머지 노드는 대기하다가 Active 노드 장애 시 승격되는 구조다.

왜 Active-Active가 아닐까? 핵심 제약은 Nexus의 내부 데이터베이스에 있다. OrientDB나 H2는 단일 프로세스 전용 임베디드 DB이므로, 두 노드가 동시에 쓰기를 처리하면 데이터 정합성이 깨진다. 외부 PostgreSQL을 사용하는 최신 버전에서도, Nexus의 캐시 레이어와 Blob Store 메타데이터 관리가 단일 writer를 전제로 설계되어 있어 Active-Active는 지원되지 않는다.

Active-Active를 구현하려면 분산 락, 캐시 무효화 전파, 충돌 해소(conflict resolution) 같은 복잡한 메커니즘이 필요하다. Nexus가 이런 아키텍처를 채택하지 않은 것은 기술적 한계이기도 하고, "아티팩트 저장소에 Active-Active 수준의 처리량이 과연 필요한가?"라는 현실적 판단이기도 하다.

대부분의 조직에서 Nexus 장애 시 요구되는 것은 "높은 처리량"이 아니라 "빠른 복구"이므로, Active-Passive가 적절한 선택인 셈이다.

읽기 트래픽만 분산하고 싶다면 두 가지 방법이 있다. Nexus Pro의 읽기 replica를 활용하거나, OSS 환경에서 Reverse Proxy가 GET 요청을 여러 Nexus 인스턴스에 분산하되 각 인스턴스가 같은 Proxy 리포지토리를 바라보도록 구성하는 것이다.

---

## Q2. S3 Blob Store의 비용 구조와 File Blob Store 대비 성능 트레이드오프는?

S3 Blob Store는 저장 비용은 저렴하지만(S3 Standard 기준 GB당 월 $0.023), API 호출 비용이 숨은 지출이 된다. PUT/POST는 1,000건당 $0.005, GET은 1,000건당 $0.0004다.

CI/CD가 빈번하게 아티팩트를 올리고 내리면 이 비용이 무시하기 어려운 수준으로 올라갈 수 있다. 하루에 Maven 의존성 해결로 GET이 10만 건이면 월간 $1.2 수준이니 미미하지만, Docker 이미지 layer push로 PUT이 하루 1만 건이면 월간 $1.5에 data transfer 비용이 추가된다. 대규모 조직에서는 이 금액이 자릿수가 달라질 수 있다.

성능 면에서의 차이가 더 중요하다. File Blob Store는 로컬 SSD 기준 수 밀리초의 지연인 반면, S3는 수십~수백 밀리초가 기본이다.

대용량 파일(Docker 이미지 레이어) 다운로드에서는 대역폭이 병목이라 지연 차이가 체감되지 않는다. 하지만 Maven 의존성 해결처럼 작은 파일을 수백 개 순차적으로 요청하는 패턴에서는 누적 지연이 빌드 시간을 크게 늘린다. 100개 파일 × 50ms = 5초 추가 지연이다.

실무적인 해결 전략은 계층화(tiering)다. `maven-snapshots`는 File Blob Store에, `maven-releases`는 S3에 분리하는 것이 가능하다. S3 Intelligent-Tiering을 활용하면 접근 빈도에 따라 자동으로 스토리지 클래스가 전환되어 비용을 더 절감할 수 있다.

---

## Q3. IaC로 Nexus를 관리할 때 drift 감지 방법은?

Drift란 코드에 정의된 상태와 실제 Nexus 상태가 어긋나는 것이다. 주로 누군가 UI에서 수동 변경을 했을 때 발생한다. "잠깐만 이것만 바꿀게"라는 긴급 변경이 쌓이면 어느 순간 Git의 정의 파일이 실제 상태와 완전히 동떨어진다.

감지 방법으로는 세 가지가 있다.

**첫째, 주기적 비교 스크립트.** REST API(`/service/rest/v1/repositories`)로 현재 설정을 JSON으로 가져온 뒤, Git의 정의 파일과 `jq` + `diff`로 비교한다. 이 스크립트를 Jenkins나 cron으로 매일 돌려서 차이가 발견되면 Slack 알림을 보내는 구조다.

```bash
# drift 감지 스크립트 핵심 로직
ACTUAL=$(curl -s -u admin:$PASS $NEXUS_URL/service/rest/v1/repositories | jq 'sort_by(.name)')
EXPECTED=$(cat repos-definition.json | jq 'sort_by(.name)')
DIFF=$(diff <(echo "$ACTUAL") <(echo "$EXPECTED"))
if [ -n "$DIFF" ]; then
  echo "DRIFT DETECTED:" && echo "$DIFF"
  # Slack webhook 호출
fi
```

**둘째, Terraform plan.** `datadrivers/nexus` 프로바이더를 사용하면 리포지토리, 역할, Blob Store 등을 Terraform state로 관리할 수 있고, `plan` 결과에 "changed outside of Terraform"이 뜨면 drift가 발생한 것이다.

**셋째, 감사 로그 모니터링.** Nexus의 `audit.log`를 모니터링하여 수동 변경이 발생하면 알림을 보내는 방식이다. drift가 발생한 후 감지하는 게 아니라 발생하는 순간 잡는 것이므로 가장 선제적이다.

가장 근본적인 해결은 admin UI 접근을 최소 인원으로 제한하고, 모든 변경을 Git PR → 파이프라인 → API 호출의 경로로 강제하는 것이다.

---

## Q4. Artifactory에서 Nexus로 마이그레이션 시 가장 큰 장벽은?

기술적으로 가장 어려운 부분은 메타데이터 보존이다. 아티팩트 파일 자체는 양쪽 모두 REST API로 추출/재배포가 가능하다.

하지만 다운로드 횟수, 프로퍼티(태그), 빌드 정보 같은 메타데이터는 두 제품의 데이터 모델이 완전히 달라서 1:1 매핑이 안 되는 경우가 많다. Artifactory의 "Properties"는 key-value 쌍인데, Nexus에는 동일한 개념이 없다(Pro의 Tagging이 유사하긴 하지만 구조가 다르다).

체크섬(SHA-1, MD5)은 파일 내용에서 재계산하면 되지만, 최초 업로드 타임스탬프를 보존하려면 별도 처리가 필요하다.

조직적으로 가장 큰 장벽은 CI/CD 파이프라인 변경이다. 수십 개의 프로젝트가 `settings.xml`, `build.gradle`, `.npmrc`, `Dockerfile`에 Artifactory URL을 하드코딩하고 있다면, 이를 모두 찾아서 바꿔야 한다.

DNS CNAME으로 `artifactory.company.com`을 Nexus IP로 리다이렉트하면 충격을 줄일 수 있지만, Docker Registry의 경우 인증 토큰 형식이 달라서 CNAME만으로는 해결되지 않는다. `docker login`부터 다시 해야 하는 것이다.

검증 단계도 만만치 않다. 양쪽의 아티팩트 목록을 비교하고, 체크섬을 대조하고, 실제로 의존성 해결이 되는지 테스트 빌드를 돌려봐야 한다.

마이그레이션 기간 동안 두 시스템을 병렬 운영하면서 새 빌드는 Nexus로, 기존 아티팩트는 Artifactory에서 점진적으로 가져오는 방식이 리스크를 줄여준다. Nexus에서 Artifactory를 Proxy 리포지토리의 remote로 등록하면, 기존 아티팩트가 최초 요청 시 자동으로 캐싱되므로 명시적 마이그레이션 없이도 자연스럽게 이전이 진행된다.

---

## Q5. Smart Proxy로 글로벌 분산 시 캐시 일관성 보장 방법은?

Smart Proxy는 pull-through 캐시 방식으로 동작한다. 원본 Nexus(upstream)에 아티팩트가 있고, 각 리전의 Nexus가 처음 요청 시 원본에서 가져와 로컬에 캐싱하는 구조다.

CDN과 비슷하다고 생각하면 이해가 쉬운데, 차이점은 CDN은 주로 읽기 전용이지만 Smart Proxy는 각 리전에서 hosted 리포지토리에 쓰기도 가능하고, 이 변경이 다른 리전으로 전파될 수 있다는 점이다.

일관성은 TTL(Time-to-Live) 기반으로 관리된다. 캐싱된 아티팩트의 메타데이터가 TTL을 초과하면 다음 요청 시 원본에 조건부 GET(If-Modified-Since 또는 If-None-Match/ETag)을 보내서 변경 여부를 확인한다.

releases 리포지토리처럼 불변(immutable)인 경우는 TTL을 길게(24시간 이상) 잡아도 문제가 없다. 반면 snapshots는 같은 좌표에 새 빌드가 계속 올라오므로, TTL을 짧게(1시간 이하) 설정해야 최신 버전을 받을 수 있다.

강제 동기화가 필요한 상황도 있다. 보안 패치가 적용된 라이브러리를 즉시 전파해야 하거나, 잘못 올라간 아티팩트를 모든 리전에서 제거해야 할 때다. 이 경우 로컬 캐시를 무효화(invalidate)하는 API를 호출할 수 있다.

하지만 무효화는 "다음 요청 시 원본에서 다시 가져오겠다"는 뜻이지, 즉시 삭제를 의미하지는 않는다. 이미 개발자의 로컬 캐시(~/.m2)에도 남아 있으므로, 완전한 제거는 클라이언트 측 캐시까지 정리해야 달성된다.

---

## Q6. Nexus Firewall로 Log4Shell 같은 취약점을 사전 차단하려면?

Nexus Firewall(IQ Server 연동)은 Proxy 리포지토리를 통해 들어오는 컴포넌트를 Sonatype의 취약점 데이터베이스와 실시간으로 대조한다. 이 데이터베이스는 NVD보다 더 빠르게 업데이트되는 것이 특징이다.

정책(Policy)을 설정하여 CVSS 점수가 특정 임계값(예: 9.0) 이상인 컴포넌트를 자동 차단(quarantine)할 수 있다. 차단된 컴포넌트는 다운로드가 거부되고, 개발자에게 보안 취약점 안내 메시지가 표시된다.

정책은 단순 CVSS 임계값 외에도, 특정 라이선스(GPL 등) 차단, 오래된 버전 차단, 알려진 악성 패키지 차단 등 다양한 조건을 조합할 수 있다.

Log4Shell(CVE-2021-44228)의 경우, CVE 공개 후 수 시간 내에 Sonatype 데이터베이스에 반영되었으므로 Firewall이 활성화되어 있었다면 취약한 log4j-core 2.0~2.14.1 버전의 신규 다운로드가 자동 차단되었을 것이다.

하지만 여기서 간과하기 쉬운 점이 있다. 이미 Nexus 캐시에 존재하는 아티팩트는 Firewall의 실시간 차단 대상이 아니다. 기존 캐시를 소급 검사하려면 "Audit" 모드를 활성화하여 전체 저장소를 스캔해야 한다.

이 스캔 결과를 바탕으로 취약한 버전을 quarantine하거나 삭제하고, 영향받는 프로젝트에 업그레이드를 요청하는 프로세스까지 갖춰야 완전한 방어가 된다.

OSS 환경에서 Firewall이 없다면? CI/CD 파이프라인에 Trivy, Grype, OWASP Dependency-Check를 넣어서 빌드 시점에 검사하는 것이 현실적인 대안이다.

---

## 심화 질문

> "Nexus를 '아티팩트 플랫폼'으로 발전시키려면 어떤 추가 도구/프로세스가 필요한가?"

단순 저장소를 넘어 플랫폼이 되려면 네 가지 축이 필요하다.

**(1) 공급망 보안.** Nexus Firewall 또는 Snyk/Trivy를 연동하여 모든 유입 아티팩트의 취약점을 검사하고, SBOM(Software Bill of Materials)을 자동 생성하는 것이 첫 단계다. SBOM은 미국 정부의 행정명령(EO 14028) 이후 많은 조직에서 필수 요구사항이 되었다.

**(2) 거버넌스 자동화.** Promotion 파이프라인으로 dev → staging → prod 승격을 자동화하고, 승인 게이트를 Jira/Slack과 연동한다. "QA 승인 없이 프로덕션 리포지토리에 배포할 수 없다"는 규칙을 기술적으로 강제하는 것이다.

**(3) 개발자 경험.** 내부 패키지 검색 포탈, 사용 가이드 문서, IDE 설정 자동화가 필요하다. 온보딩 스크립트로 `settings.xml`과 `.npmrc`를 자동 생성해주면 신규 입사자의 환경 설정 시간을 30분에서 3분으로 줄일 수 있다.

**(4) 운영 성숙도.** IaC로 전체 설정을 관리하고, Prometheus/Grafana 대시보드로 실시간 모니터링을 하며, 용량 예측(growth trend) 자동화까지 갖추는 것이다.

이 네 축이 갖춰지면 Nexus는 "파일 올리는 곳"에서 "소프트웨어 공급망의 중심 허브"로 진화한다. 도입 순서는 보안(1) → 개발자 경험(3) → 거버넌스(2) → 운영 성숙도(4)가 ROI가 높은 순서다.
