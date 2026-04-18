# Ch08. Observability & Security - 면접 질문

---

## Q1. Jenkins 빌드 성능 저하 분석

**Jenkins 빌드 성능이 저하되었을 때 확인해야 하는 메트릭과 분석 방법을 설명하시오.**

### 핵심 포인트

- **빌드 시간 트렌드 분석**: 평균 빌드 시간만으로는 부족하고, P95를 함께 봐야 한다. 평균이 3분인데 P95가 15분이면 20번 중 1번은 극단적으로 느린 빌드가 발생하는 것이며, 이는 특정 조건(캐시 미스, 외부 서비스 타임아웃 등)에서만 나타나는 병목을 암시한다.
- **큐 대기시간 확인**: 빌드 자체는 빠른데 큐에서 오래 대기한다면 Agent 부족이 원인이다. `jenkins_queue_size`가 5분 이상 지속적으로 0보다 크면 Agent 스케일링이 필요하다.
- **Agent 활용률 분석**: 시간대별 활용률 패턴을 확인한다. 피크 시간에만 90%를 넘고 야간에는 10%라면 오토스케일링으로 대응할 수 있다. 전체 시간대에서 90% 이상이면 Agent 상시 증설이 필요하다.
- **단계별 소요 시간 분해**: Pipeline의 각 stage별 소요 시간을 측정하여 병목 stage를 식별한다. checkout이 느리면 Git shallow clone 도입, 테스트가 느리면 병렬화, Docker build가 느리면 레이어 캐싱 최적화 등 stage별로 대응 방법이 다르다.
- **인프라 리소스 확인**: Agent의 CPU, 메모리, 디스크 I/O를 함께 모니터링한다. 빌드 시간 증가와 Agent의 디스크 사용률 90% 초과가 동시에 나타나면 디스크 I/O 병목이 원인일 수 있다.

### 심화 질문

- 빌드 시간이 특정 시간대에만 느려진다면 어떤 원인을 의심하고, 어떻게 검증하겠는가?
- flaky 테스트가 빌드 성능에 미치는 간접적 영향은 무엇인가? (재시도로 인한 빌드 시간 증가, 실패 후 재빌드로 인한 큐 부하 등)

---

## Q2. Jenkins Credentials Store vs HashiCorp Vault

**Jenkins Credentials Store와 HashiCorp Vault의 차이를 설명하고, 언제 Vault를 도입해야 하는지 설명하시오.**

### 핵심 포인트

- **Jenkins Credentials Store**: Jenkins Controller 디스크에 AES-128로 암호화하여 저장한다. 설정이 간단하고 별도 인프라가 필요 없다는 장점이 있지만, Jenkins에 종속되어 다른 시스템과 시크릿을 공유할 수 없고, 시크릿 순환을 수동으로 해야 한다.
- **HashiCorp Vault**: 중앙 집중식 시크릿 관리 시스템이다. Jenkins뿐 아니라 Kubernetes, 애플리케이션 서버 등 모든 시스템이 동일한 Vault에서 시크릿을 가져온다. 동적 시크릿(Dynamic Secrets)으로 빌드마다 임시 크레덴셜을 생성하고 TTL 만료 시 자동 폐기하므로, 유출 시에도 피해 범위가 제한된다.
- **감사 추적의 차이**: Jenkins Store는 "누가 크레덴셜을 생성/수정했는지"는 기록하지만 "런타임에 어떤 빌드가 어떤 시크릿을 읽었는지"는 상세히 추적하지 못한다. Vault는 모든 시크릿 접근을 상세히 로깅하므로 컴플라이언스 감사에 대응할 수 있다.
- **Vault 도입 시점**: 시크릿을 관리하는 시스템이 3개 이상일 때, 시크릿 순환 주기를 90일 이하로 유지해야 할 때, SOC2/ISO 27001 감사에서 시크릿 접근 로그를 요구할 때 Vault 도입을 검토한다.
- **비용 대비 판단**: Vault 자체도 운영해야 하는 인프라이므로, 소규모 팀에서는 Jenkins Credentials Store + Folder 스코프로 팀별 격리하는 것이 현실적이다. 불필요한 복잡성을 도입하지 않는 판단도 중요하다.

### 심화 질문

- Vault의 Dynamic Secrets가 정적 시크릿 대비 보안상 유리한 구체적인 시나리오를 설명하시오.
- Jenkins Credentials Store의 마스터 키(`$JENKINS_HOME/secrets/`)가 유출되면 어떤 일이 발생하며, 이를 방지하기 위한 조치는 무엇인가?

---

## Q3. Jenkins RBAC 구현과 최소 권한 원칙

**Jenkins에서 RBAC를 구현하는 방법을 설명하고, 최소 권한 원칙을 어떻게 적용하는지 설명하시오.**

### 핵심 포인트

- **Matrix-based Security의 한계**: 사용자별로 개별 권한을 부여하는 방식은 사용자가 50명을 넘어가면 관리가 비현실적이다. 새 프로젝트 추가 시 50명의 권한을 개별 조정해야 하므로 인적 오류가 발생하기 쉽다.
- **Role Strategy Plugin의 3계층 역할**: Global Roles(전체 시스템), Project Roles(정규식으로 프로젝트 매칭), Agent Roles(특정 Agent 접근 제한)로 구분한다. Project Roles에서 `frontend-.*` 같은 정규식을 사용하면 네이밍 규칙만 지키면 새 프로젝트에 자동으로 권한이 적용된다.
- **최소 권한 적용 예시**: 개발자에게 `Job/Build`, `Job/Read`만 부여하고 `Job/Configure`는 부여하지 않는다. 빌드 실행과 결과 확인은 가능하지만 Job 설정 변경은 불가하므로, 실수로 빌드 트리거나 파라미터를 잘못 변경하는 것을 방지할 수 있다.
- **JCasC를 통한 코드화**: RBAC 설정을 YAML 파일로 관리하면 Git을 통한 변경 추적과 코드 리뷰가 가능하다. UI에서 수동으로 변경하면 "누가 권한을 바꿨는지" 추적이 어렵지만, JCasC를 사용하면 Git 히스토리로 모든 변경을 확인할 수 있다.
- **Folder 기반 팀 격리**: Jenkins Folder 플러그인과 결합하면 팀별로 폴더를 생성하고, 각 팀은 자기 폴더 내의 Job만 접근 가능하도록 격리할 수 있다. 크레덴셜도 Folder 스코프로 팀별로 분리한다.

### 심화 질문

- 개발자가 Jenkinsfile에서 `sh 'curl http://internal-api/admin'` 같은 명령을 실행하면 RBAC만으로 방어할 수 있는가? 추가로 필요한 보안 조치는?
- RBAC 설정을 JCasC로 관리할 때, 잘못된 YAML을 적용하여 관리자 자신의 접근이 차단되는 상황을 어떻게 방지하는가?

---

## Q4. Jenkins Prometheus Plugin 주요 메트릭

**Jenkins Prometheus Plugin으로 수집할 수 있는 주요 메트릭과 각각이 의미하는 바를 설명하시오.**

### 핵심 포인트

- **`jenkins_builds_total`** (Counter): 전체 빌드 수를 result 레이블(SUCCESS, FAILURE, UNSTABLE, ABORTED)별로 누적 카운팅한다. `rate()` 함수로 초당 빌드 수를 계산하고, SUCCESS/전체 비율로 성공률을 산출한다. 카운터이므로 값이 절대 감소하지 않으며, 재시작 시 0으로 리셋된다.
- **`jenkins_builds_duration_milliseconds`** (Histogram): 빌드 소요 시간을 버킷(bucket)별로 기록한다. 히스토그램이므로 `histogram_quantile()` 함수로 P50, P90, P95, P99를 계산할 수 있다. 평균만 보면 소수의 극단적으로 느린 빌드를 놓치므로, 분위수를 함께 모니터링해야 한다.
- **`jenkins_queue_size`** (Gauge): 현재 큐에서 대기 중인 빌드 수를 나타낸다. 순간 스파이크는 정상이지만 5분 이상 지속적으로 0보다 크면 Agent 부족 신호이다. 시계열로 기록하면 피크 시간대를 식별하여 스케일링 정책을 수립할 수 있다.
- **`jenkins_agents_online`** (Gauge): 현재 온라인 Agent 수이다. `jenkins_agents_online / jenkins_agents_total`로 Agent 가용률을 계산한다. 이 값이 갑자기 감소하면 Agent 장애를 의미하며, 70% 미만이면 인프라 점검이 필요하다.
- **메트릭 타입의 중요성**: Counter는 누적이므로 `rate()`로 변화율을 봐야 하고, Gauge는 현재 값 그대로 의미가 있으며, Histogram은 `histogram_quantile()`로 분위수를 계산해야 한다. 메트릭 타입을 이해하지 못하면 PromQL 쿼리를 올바르게 작성할 수 없다.

### 심화 질문

- `jenkins_builds_duration_milliseconds`의 P95와 P99의 차이가 크다면 무엇을 의미하며, 어떻게 대응하겠는가?
- Prometheus의 scrape_interval을 15초에서 5초로 줄이면 메트릭 정밀도는 올라가지만 어떤 부작용이 발생할 수 있는가?

---

## Q5. Jenkins 보안 베스트 프랙티스

**Jenkins 보안 베스트 프랙티스 5가지를 설명하고, 각각이 어떤 위협을 방어하는지 설명하시오.**

### 핵심 포인트

- **Controller에서 빌드 실행 금지 → 시크릿 탈취 방어**: Controller는 모든 크레덴셜, 설정, 빌드 히스토리를 저장하는 노드이다. 여기서 빌드를 실행하면 악의적 Jenkinsfile이 `$JENKINS_HOME/secrets/`를 읽거나 다른 Job의 크레덴셜을 탈취할 수 있다. `numExecutors: 0`으로 설정하여 Controller에서의 빌드 실행을 원천 차단해야 한다.
- **Agent → Controller 접근 제한 → 내부 횡이동 방어**: 기본 설정에서 Agent는 Controller의 파일 시스템에 접근하는 API를 호출할 수 있다. Agent가 침해되면 Controller까지 공격이 확산(lateral movement)될 수 있으므로, Agent → Controller Access Control을 활성화하여 화이트리스트 방식으로 API 호출을 제한한다.
- **CSRF Protection 활성화 → 요청 위조 방어**: 인증된 관리자가 악성 웹사이트를 방문하면, 해당 사이트의 JavaScript가 관리자의 세션을 이용하여 Jenkins에 "Job 삭제", "설정 변경" 같은 요청을 보낼 수 있다. CSRF 토큰(crumb)을 요구하면 외부에서의 위조 요청을 차단할 수 있다.
- **Script Security Plugin → 임의 코드 실행 방어**: 샌드박스 없는 Groovy 스크립트는 Jenkins JVM의 모든 권한으로 실행된다. 운영체제 명령 실행, 파일 시스템 접근, 네트워크 요청이 모두 가능하므로 사실상 서버 탈취와 동일하다. Script Security Plugin의 샌드박스가 허용된 API만 호출 가능하도록 제한하고, 새 API 사용 시 관리자 승인을 요구한다.
- **정기적 플러그인 업데이트 → 알려진 취약점(CVE) 방어**: Jenkins 보안 취약점의 대부분은 플러그인에서 발생한다. Jenkins Security Advisory에서 공개하는 취약점에 대해 최소 월 1회 패치를 적용해야 한다. 오래된 플러그인은 알려진 CVE가 패치되지 않은 상태이므로 공격자의 쉬운 진입점이 된다.

### 심화 질문

- Jenkins를 인터넷에 노출해야 하는 상황(외부 GitHub Webhook 수신 등)에서 네트워크 레이어의 보안을 어떻게 설계하겠는가?
- 심층 방어(Defense in Depth) 관점에서 Jenkins 보안 레이어 중 하나가 뚫렸을 때 나머지 레이어가 어떻게 피해를 제한하는지 시나리오를 들어 설명하시오.

---

## Q6. Jenkins 감사 로그와 컴플라이언스

**Jenkins에서 감사 로그(Audit Trail)가 필요한 이유를 설명하고, 컴플라이언스 관점에서의 가치를 설명하시오.**

### 핵심 포인트

- **운영 사고 원인 추적**: "어제 저녁에 누군가 설정을 바꿨는데 오늘 빌드가 다 깨진다"는 상황에서 감사 로그가 없으면 모든 팀원에게 물어봐야 한다. 감사 로그가 있으면 "19:32에 user-A가 JDK 경로를 변경했다"는 사실을 즉시 확인하여 원인을 분 단위로 추적할 수 있다.
- **추적 대상**: 시스템/Job 설정 변경, 빌드 트리거(누가 실행했는지), 크레덴셜 CRUD, 플러그인 설치/삭제, 사용자 권한 변경이 기본 추적 대상이다.
- **컴플라이언스 프레임워크 요구사항**: SOC2, ISO 27001, GDPR은 "누가, 언제, 무엇을 했는지"에 대한 추적 가능성(Traceability)을 요구한다. CI/CD 파이프라인은 프로덕션 코드를 변경하는 핵심 경로이므로, 감사 로그 없이는 컴플라이언스 감사에서 지적 사항이 된다.
- **로그 저장 전략**: Jenkins 로컬 파일에만 저장하면 디스크 부족이나 재설치 시 유실된다. Syslog 또는 Elasticsearch로 전송하여 중앙 집중 로그 시스템에 보관하는 것이 운영 환경의 기본이다. Elasticsearch + Kibana 조합이면 "지난 한 달간 크레덴셜을 수정한 모든 이벤트"를 즉시 검색할 수 있다.
- **Audit + RBAC 시너지**: RBAC로 "누가 무엇을 할 수 있는지"를 제어하고, Audit Trail로 "누가 실제로 무엇을 했는지"를 기록한다. 이 둘이 결합되면 권한 남용을 사후에 감지하고, RBAC 정책이 적절한지 검증하는 피드백 루프가 형성된다.

### 심화 질문

- 감사 로그의 무결성(Integrity)을 보장하기 위해 어떤 조치를 취할 수 있는가? (로그 자체가 변조되면 감사의 의미가 없으므로)
- Jenkins 감사 로그와 Git 커밋 히스토리를 결합하면 어떤 추가적인 인사이트를 얻을 수 있는가?
