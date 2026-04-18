# Ch13. SonarQube on Kubernetes - 심화 점검

## 점검 질문

---

### Q1: SonarQube의 Quality Gate가 CI/CD 파이프라인에서 하는 역할

**핵심 포인트:**

- **자동화된 품질 판단**: Quality Gate는 "이 코드를 배포해도 되는가?"라는 질문에 자동으로 답한다. 사람이 수백 개의 이슈를 일일이 검토하지 않고, 사전에 정의된 기준(커버리지 80%, Critical 버그 0개 등)으로 통과/실패를 판단한다. CI/CD 파이프라인의 "게이트키퍼" 역할을 한다.

- **빌드 차단 메커니즘**: Jenkins나 GitHub Actions에서 SonarQube 분석 후 `waitForQualityGate`를 호출하면, Quality Gate 결과를 폴링한다. "Failed"가 리턴되면 파이프라인을 중단하고, "Passed"면 다음 스테이지(배포)로 진행한다. 품질이 떨어지는 코드는 프로덕션에 도달할 수 없다.

- **신규 코드 중심 철학**: Quality Gate의 핵심은 "신규 코드(New Code)"에만 조건을 적용하는 것이다. 레거시 프로젝트는 수천 개의 기술 부채를 안고 있어서, 전체 코드를 기준으로 하면 항상 실패한다. 신규 코드만 체크하면, "과거는 용서하되, 미래는 깨끗하게"라는 현실적인 접근이 가능하다. 매 커밋마다 품질이 조금씩 개선된다.

- **팀 합의의 구체화**: Quality Gate는 팀의 품질 기준을 코드로 만든 것이다. "커버리지를 높이자"는 추상적인 목표가 "신규 코드 커버리지 80% 미만이면 배포 금지"라는 구체적인 규칙이 된다. 코드 리뷰에서 "이건 품질이 낮아요"라는 주관적 논쟁 대신, "Quality Gate가 실패했으니 수정하세요"라는 객관적 피드백을 줄 수 있다.

- **피드백 루프 단축**: Quality Gate를 CI/CD에 통합하면, 개발자가 코드를 푸시한 지 몇 분 만에 품질 결과를 받는다. 배포 후에 문제를 발견하는 것보다, 개발 중에 발견하는 것이 수정 비용이 훨씬 낮다. "Shift Left" 전략의 핵심이다.

- **메트릭 추적**: Quality Gate는 단순히 통과/실패만 알려주는 게 아니라, 각 조건의 실제 값을 보여준다. "커버리지 75% (기준: 80%)"라는 정보로 얼마나 부족한지 알 수 있고, 다음 커밋에서 개선할 수 있다. 시간에 따른 트렌드 그래프로 팀의 품질 개선 여정을 시각화할 수 있다.

**심화 질문:**

- Quality Gate가 너무 엄격하면 개발 속도가 느려지는데, 어떻게 균형을 맞추는가? (팀과 협의, 점진적 강화, 예외 처리)
- 레거시 코드를 대량으로 리팩토링할 때, Quality Gate를 일시적으로 완화해야 하는가? (별도 브랜치 전략, 임시 게이트)
- Community Edition은 브랜치 분석이 안 되는데, PR마다 Quality Gate를 체크할 수 있는가? (main 브랜치만 가능, 유료 버전 필요)

---

### Q2: Community Edition과 Developer Edition의 핵심 차이

**핵심 포인트:**

- **브랜치 분석 유무**: Community Edition은 단일 브랜치(`main` 또는 `master`)만 분석할 수 있다. Feature 브랜치, PR 브랜치를 분석하려고 하면 "Branch analysis is not supported in Community Edition" 에러가 발생한다. Developer Edition은 모든 브랜치를 독립적으로 분석하고, 브랜치 간 비교(예: feature vs main)를 제공한다. 팀이 Git Flow나 GitHub Flow를 사용한다면, Developer Edition이 필수다.

- **PR 데코레이션**: Developer Edition은 GitHub, GitLab, Bitbucket PR에 자동으로 코멘트를 단다. "3개의 버그가 발견되었습니다. 커버리지가 60%에서 70%로 증가했습니다." 같은 요약을 PR 페이지에 표시한다. 개발자가 SonarQube 서버에 별도로 접속하지 않아도, PR 리뷰 화면에서 바로 품질 정보를 볼 수 있다. Community Edition은 이 기능이 없어서, 개발자가 수동으로 SonarQube 링크를 클릭해야 한다.

- **신규 코드 정의의 유연성**: Developer Edition은 "신규 코드"를 정의하는 방법이 다양하다. 특정 날짜 이후, 특정 버전 이후, PR 기준 등. Community Edition은 이전 분석 대비 변경된 코드만 신규 코드로 본다. 릴리즈 주기가 긴 프로젝트에서는 "이번 스프린트에 작성된 코드"를 신규 코드로 정의하고 싶은데, Community Edition으로는 어렵다.

- **언어 지원**: Community Edition도 주요 언어(Java, JavaScript, Python, C#, Go 등 29개)를 지원한다. Developer Edition은 추가로 Apex, COBOL, PL/SQL, Swift 등을 지원하지만, 대부분의 팀에게는 Community Edition의 언어 지원만으로 충분하다. 언어 차이보다는 브랜치 분석 차이가 더 결정적이다.

- **보안 리포트**: Developer Edition은 OWASP Top 10, CWE 카테고리별 보안 리포트를 제공한다. 예를 들어, "SQL Injection 취약점이 5개, XSS가 3개"라는 요약을 볼 수 있다. Community Edition은 개별 보안 이슈만 보여주고, 카테고리별 집계는 없다. 보안 감사가 필요한 조직에서는 Developer 이상이 필요하다.

- **가격과 라이선스**: Community Edition은 완전 무료 오픈소스(LGPL)다. Developer Edition은 코드 라인 수 기준으로 과금한다. 10만 라인까지 연 $150, 50만 라인까지 연 $2,000 정도다. 소규모 팀이나 개인 프로젝트는 Community Edition으로 충분하고, 브랜치 전략을 적극 사용하는 팀은 Developer Edition을 고려해야 한다.

**심화 질문:**

- Community Edition에서 브랜치별 분석을 "흉내"낼 수 있는가? (별도 프로젝트 키로 분석 가능하지만, 비교 기능 없음)
- Developer Edition을 Self-hosted로 운영할 수 있는가? (가능, Docker나 Kubernetes에 설치)
- Enterprise Edition과 Data Center Edition은 언제 필요한가? (Portfolio 관리, HA 클러스터, 대규모 조직)

---

### Q3: SonarQube가 PostgreSQL을 필요로 하는 이유 (H2의 한계)

**핵심 포인트:**

- **H2는 인메모리 DB**: SonarQube에 내장된 H2 데이터베이스는 기본적으로 인메모리 모드로 동작한다. 프로세스가 종료되면 모든 데이터가 사라진다. 파일 모드로 설정할 수도 있지만, 동시성 제어가 약하고 성능이 떨어진다. SonarQube가 재시작되면 지난 분석 기록, 이슈, 사용자 설정이 모두 사라지므로, 프로덕션에서는 절대 사용할 수 없다.

- **트랜잭션과 무결성**: SonarQube는 수백만 개의 이슈, 메트릭, 스냅샷을 저장한다. Compute Engine이 분석 리포트를 처리할 때, 여러 테이블에 트랜잭션을 걸고 원자적으로 커밋해야 한다. PostgreSQL은 ACID 트랜잭션을 완벽히 지원하지만, H2는 제약 조건 체크나 트랜잭션 격리가 약하다. 동시에 여러 분석이 실행되면 데이터 무결성이 깨질 수 있다.

- **동시성과 락**: 여러 사용자가 동시에 SonarQube에 접속하고, 여러 분석이 동시에 실행되면, DB 레벨에서 동시성 제어가 필요하다. PostgreSQL은 MVCC(Multi-Version Concurrency Control)로 읽기-쓰기 간 락 충돌을 최소화한다. H2는 단순한 락 메커니즘을 사용해서, 동시성이 높아지면 병목이 생긴다.

- **성능과 인덱싱**: SonarQube는 복잡한 쿼리를 실행한다. "이 프로젝트의 지난 30일간 Critical 이슈 트렌드"를 조회하려면, 수십만 행을 스캔하고 집계해야 한다. PostgreSQL은 B-tree, GIN, GiST 같은 다양한 인덱스를 지원하고, 쿼리 최적화기가 강력하다. H2는 기본 인덱스만 지원하고, 대용량 데이터에서는 느리다.

- **백업과 복구**: 프로덕션 SonarQube는 분석 기록과 품질 트렌드가 중요한 자산이다. PostgreSQL은 `pg_dump`, PITR(Point-In-Time Recovery), 복제 같은 엔터프라이즈급 백업 기능을 제공한다. H2는 파일을 복사하는 것 외에는 백업 방법이 없고, 복구도 수동이다.

- **스키마 마이그레이션**: SonarQube가 업그레이드되면 DB 스키마도 변경된다. PostgreSQL은 `ALTER TABLE` 같은 DDL을 안전하게 실행하고, 트랜잭션으로 롤백할 수 있다. H2는 스키마 변경 시 제약 조건이 깨지거나, 마이그레이션 스크립트가 실패하는 경우가 있다.

**심화 질문:**

- MySQL이나 Oracle을 사용할 수 있는가? (가능하지만, PostgreSQL보다 최적화가 덜 됨)
- PostgreSQL의 어떤 기능을 SonarQube가 활용하는가? (JSON 타입, Full-Text Search, 파티셔닝)
- CloudNativePG(CNPG)로 PostgreSQL HA를 구성하면 SonarQube도 HA가 되는가? (DB는 HA지만, SonarQube 자체는 단일 인스턴스)

---

### Q4: sonar-scanner의 동작 과정 (분석 → 리포트 → CE 처리)

**핵심 포인트:**

- **1단계: 소스코드 스캔**: sonar-scanner는 프로젝트 디렉토리를 재귀적으로 탐색하고, `sonar.sources`에 정의된 파일들을 읽는다. 각 파일의 언어를 감지하고(확장자나 shebang으로), 해당 언어의 파서를 사용해서 AST(Abstract Syntax Tree)를 생성한다. 예를 들어, Java 파일이면 JavaParser, JavaScript 파일이면 ESLint Parser를 사용한다.

- **2단계: 규칙 적용**: Quality Profile에 정의된 규칙들을 AST에 적용한다. 예를 들어, "Cognitive Complexity > 15" 규칙이 활성화되어 있으면, 각 메서드의 복잡도를 계산하고, 15를 넘으면 이슈를 생성한다. 수백 개의 규칙이 병렬로 실행되며, 각 규칙은 패턴 매칭이나 데이터 플로우 분석을 수행한다.

- **3단계: 메트릭 계산**: 코드 라인 수, 주석 비율, 중복 라인, Cyclomatic Complexity 같은 메트릭을 계산한다. 테스트 커버리지는 별도 리포트(JaCoCo, Istanbul 등)를 읽어서 통합한다. sonar-scanner는 `sonar.coverage.jacoco.xmlReportPaths` 같은 설정으로 커버리지 파일 경로를 받는다.

- **4단계: 리포트 생성**: 모든 이슈, 메트릭, 소스코드 하이라이트 정보를 JSON 형태의 분석 리포트로 패키징한다. 이 리포트는 수 MB에서 수십 MB까지 클 수 있다. 리포트에는 파일별 이슈 목록, 라인별 커버리지, 중복 블록 정보 등이 담긴다.

- **5단계: 서버 업로드**: 리포트를 HTTP POST로 SonarQube Web Server에 업로드한다. 엔드포인트는 `/api/ce/submit`이고, 인증은 토큰으로 한다. Web Server는 리포트를 받으면, DB의 작업 큐에 넣고, Task ID를 리턴한다. sonar-scanner는 이 Task ID를 출력하고 종료한다.

- **6단계: Compute Engine 처리**: Web Server가 종료된 후에도, Compute Engine은 백그라운드에서 작업 큐를 폴링한다. 새 작업을 발견하면, 리포트를 파싱하고, 이전 분석과 비교해서 "신규 이슈"와 "해결된 이슈"를 구분한다. Quality Gate 조건을 평가하고, 결과를 DB에 저장한다. Elasticsearch에 인덱싱해서 검색 가능하게 만든다.

**흐름 다이어그램:**

```
[소스코드] → [sonar-scanner]
                ↓
          [AST 생성 + 규칙 적용]
                ↓
          [메트릭 계산 + 리포트 생성]
                ↓
          [Web Server /api/ce/submit]
                ↓
          [Task Queue (DB)]
                ↓
          [Compute Engine 폴링]
                ↓
          [분석 결과 저장 + Elasticsearch 인덱싱]
                ↓
          [Quality Gate 평가]
                ↓
          [사용자 UI에서 조회 가능]
```

**심화 질문:**

- sonar-scanner가 네트워크가 끊겨서 업로드에 실패하면? (리포트는 `.scannerwork/` 디렉토리에 남음, 재시도 필요)
- Compute Engine이 처리 중에 크래시하면? (작업이 큐에 남아있고, 재시작 시 재처리)
- 대용량 프로젝트(100만 라인 이상)는 분석 시간이 얼마나 걸리는가? (수십 분~시간, 병렬화와 인크리멘탈 분석으로 최적화)

---

### Q5: Quality Profile 커스터마이징 방법과 팀 표준화

**핵심 포인트:**

- **기본 프로필 복사**: SonarQube는 언어별로 "Sonar way"라는 기본 Quality Profile을 제공한다. 이 프로필은 수백 개의 규칙 중 중요한 것들만 활성화한다. 팀 표준을 만들려면 기본 프로필을 복사해서 수정한다. "Quality Profiles" → 언어 선택 → "Copy" → 이름 입력 (예: "My Team Java Profile").

- **규칙 추가/제거**: "Activate More" 버튼으로 비활성화된 규칙을 검색해서 추가할 수 있다. 예를 들어, "Constant names should comply with a naming convention" 규칙을 추가하고, 정규식을 `^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$`로 설정하면, 상수가 `UPPER_SNAKE_CASE`를 따르지 않으면 이슈가 생긴다. 반대로, 팀이 동의하지 않는 규칙은 "Deactivate"할 수 있다.

- **심각도 조정**: 규칙의 심각도(Severity)를 Blocker, Critical, Major, Minor, Info로 조정할 수 있다. 예를 들어, "TODO 주석이 남아있음" 규칙은 기본적으로 Info인데, 팀이 TODO를 허용하지 않는다면 Critical로 올릴 수 있다. Quality Gate는 심각도별로 조건을 설정할 수 있다 (예: "Critical 이상 이슈가 0개").

- **임계값 커스터마이징**: 일부 규칙은 임계값을 조정할 수 있다. "Cognitive Complexity should not be too high" 규칙의 기본 임계값은 15인데, 팀이 더 엄격하게 관리하고 싶으면 10으로 낮추거나, 레거시 코드에서는 20으로 높일 수 있다. 규칙을 클릭하고 "Change" 버튼으로 파라미터를 수정한다.

- **프로필 비교**: 두 개의 Quality Profile을 비교해서 어떤 규칙이 다른지 볼 수 있다. "Compare" 기능으로 "Sonar way"와 "My Team Profile"을 비교하면, "10개 규칙 추가, 5개 규칙 제거, 3개 규칙 심각도 변경"이라는 요약이 나온다. 이 정보로 팀의 품질 기준이 업계 표준과 얼마나 다른지 파악할 수 있다.

- **백업과 공유**: Quality Profile을 XML로 내보내고, 다른 SonarQube 인스턴스에 가져올 수 있다. "Backup" 버튼으로 XML을 다운로드하고, Git에 커밋한다. 새로운 SonarQube를 설치하면, "Restore" 버튼으로 XML을 업로드하면 프로필이 자동으로 생성된다. API로도 가능하다: `GET /api/qualityprofiles/backup`, `POST /api/qualityprofiles/restore`.

- **프로젝트에 적용**: 프로젝트마다 다른 Quality Profile을 사용할 수 있다. "Project Settings" → "Quality Profiles" → 언어별로 프로필 선택. 기본값은 "Sonar way"지만, "My Team Profile"로 변경하면 다음 분석부터 새 규칙이 적용된다. 팀 전체가 같은 프로필을 사용하면, 일관된 품질 기준을 강제할 수 있다.

**심화 질문:**

- 여러 프로젝트가 다른 Java 버전을 사용하는데, Quality Profile을 분리해야 하는가? (가능, 버전별 규칙 활성화)
- 규칙을 커스터마이징할 때, 정규식이나 AST 패턴을 직접 작성할 수 있는가? (기본 규칙은 불가, 커스텀 플러그인 개발 필요)
- Sonar way 프로필이 업데이트되면 내 프로필도 자동으로 업데이트되는가? (안 됨, 수동으로 규칙 추가 필요)

---

### Q6: SonarQube와 Jenkins 통합 시 필요한 설정

**핵심 포인트:**

- **SonarQube Scanner 플러그인**: Jenkins에서 SonarQube를 사용하려면 "SonarQube Scanner for Jenkins" 플러그인을 설치해야 한다. 이 플러그인은 `withSonarQubeEnv` 스텝과 `waitForQualityGate` 스텝을 제공한다. 플러그인이 없으면 수동으로 `sonar-scanner` CLI를 실행해야 하고, Quality Gate 결과를 폴링하는 로직을 직접 작성해야 한다.

- **SonarQube 서버 등록**: Jenkins 시스템 설정에서 SonarQube 서버를 등록한다. "Manage Jenkins" → "Configure System" → "SonarQube servers" 섹션. 서버 이름(예: `sonarqube`), 서버 URL(예: `http://sonarqube:9000`), 인증 토큰(Secret text로 저장)을 입력한다. 이 정보는 Jenkinsfile에서 `withSonarQubeEnv('sonarqube')`로 참조된다.

- **Webhook 설정**: Quality Gate 결과를 Jenkins에 알려주려면, SonarQube에 Webhook을 설정해야 한다. SonarQube UI → "Administration" → "Configuration" → "Webhooks" → "Create". URL은 `http://jenkins:8080/sonarqube-webhook/`이고, Secret은 선택 사항이다. Webhook이 없으면 `waitForQualityGate`가 타임아웃까지 폴링하면서 시간을 낭비한다.

- **프로젝트 키와 토큰**: sonar-scanner를 실행할 때 프로젝트 키(`-Dsonar.projectKey=my-app`)와 토큰(`-Dsonar.login=<token>`)을 전달해야 한다. 토큰은 Jenkins Credentials로 저장하고, Jenkinsfile에서 `credentials('sonarqube-token')`으로 주입한다. 프로젝트 키는 SonarQube에서 미리 생성해야 하는데, "Automatic Project Creation" 옵션을 활성화하면 첫 분석 시 자동으로 생성된다.

- **빌드와 테스트 선행**: SonarQube 분석은 컴파일된 바이너리와 테스트 리포트를 필요로 한다. Maven/Gradle 빌드 후에 `sonar:sonar`를 실행해야 한다. Jenkins 파이프라인에서는 "Build" 스테이지 다음에 "SonarQube Analysis" 스테이지를 배치한다. JaCoCo나 Istanbul 같은 커버리지 도구를 활성화해서 테스트 리포트를 생성해야 커버리지 메트릭이 나온다.

- **waitForQualityGate 타임아웃**: `waitForQualityGate`는 기본적으로 1분 동안 결과를 폴링한다. 대형 프로젝트는 Compute Engine 처리 시간이 길어서 타임아웃이 발생할 수 있다. `timeout(time: 5, unit: 'MINUTES')`로 타임아웃을 늘리거나, Webhook을 설정해서 폴링을 줄인다. `abortPipeline: true` 옵션으로 Quality Gate 실패 시 빌드를 중단한다.

- **멀티브랜치 파이프라인**: Jenkins의 멀티브랜치 파이프라인을 사용하면, 각 브랜치마다 자동으로 빌드가 생성된다. SonarQube Community Edition은 브랜치 분석이 안 되므로, `sonar.projectKey`를 브랜치별로 다르게 설정해야 한다 (예: `my-app-feature-login`). Developer Edition을 사용하면 `sonar.branch.name`으로 브랜치를 전달하고, 브랜치별 분석과 비교가 자동으로 된다.

**심화 질문:**

- Jenkins가 Kubernetes Pod에서 실행될 때, SonarQube 서버 URL은 어떻게 설정하는가? (Kubernetes Service 이름 사용)
- Quality Gate 실패 시 Slack으로 알림을 보내려면? (Jenkins Slack 플러그인 + post 블록)
- 여러 프로젝트가 같은 SonarQube 서버를 공유하는데, 토큰을 프로젝트별로 분리해야 하는가? (프로젝트별 토큰으로 권한 제한 가능)

---

## 정리

SonarQube on Kubernetes는 코드 품질을 자동화하고, CI/CD 파이프라인에 품질 게이트를 통합하는 강력한 방법이다. Quality Gate로 배포 가부를 자동 판단하고, Quality Profile로 팀의 품질 기준을 코드화하며, Jenkins와 통합해서 모든 빌드마다 품질을 체크한다.

Community Edition과 Developer Edition의 핵심 차이는 브랜치 분석과 PR 데코레이션이다. 소규모 팀은 Community Edition으로 충분하지만, 브랜치 전략을 적극 사용하는 팀은 Developer Edition이 필요하다.

PostgreSQL은 SonarQube의 안정성과 성능을 보장한다. H2는 테스트 용도일 뿐 프로덕션에서는 사용하면 안 된다. sonar-scanner는 소스코드를 분석하고 리포트를 업로드하며, Compute Engine은 백그라운드에서 처리한다.

Quality Profile 커스터마이징으로 팀의 코딩 스타일과 품질 기준을 강제하고, Jenkins 통합으로 품질이 떨어지는 코드가 프로덕션에 도달하지 못하게 막는다. 이것이 진정한 "Shift Left" 전략이다.
