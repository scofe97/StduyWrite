# Ch10. Groovy 커스터마이징과 Init Hook - 점검 질문

면접 대비 수준으로 답변할 수 있는지 스스로 확인하는 질문 모음입니다.
각 질문에 대해 구두로 2-3분 안에 설명할 수 있어야 합니다.

---

## Q1. Jenkins에서 Groovy가 사용되는 3가지 영역과 보안 수준 차이

**질문**: Jenkins에서 Groovy가 사용되는 3가지 영역을 설명하고, 각각의 보안 수준 차이를 설명하시오.

**핵심 포인트**:
- 3가지 영역: Pipeline DSL (Jenkinsfile), Script Console (Manage Jenkins), Init Hook (init.groovy.d/)
- Pipeline DSL은 Script Security Plugin의 Sandbox 환경에서 실행되며, 허용된 API만 호출 가능하다는 점
- Script Console은 Sandbox가 적용되지 않으며 Jenkins의 모든 Internal API에 무제한 접근이 가능하다는 점
- Init Hook은 Script Console과 동일한 권한이지만 Jenkins 시작 시 시스템이 자동으로 실행한다는 점
- 세 영역의 핵심 차이는 "누가 실행하느냐"와 "어떤 보안 경계 안에서 실행되느냐"
- Groovy가 선택된 이유: JVM 호환성으로 Jenkins Java 클래스에 직접 접근 가능, 동적 타이핑으로 스크립팅에 적합, 컴파일 없이 즉시 실행 가능

**심화 질문**: Pipeline DSL에서 Sandbox가 차단하는 API를 사용해야 하는 정당한 사유가 있을 때, Script Approval을 통해 승인하면 해당 메서드가 모든 Pipeline에서 사용 가능해진다. 이것이 보안 관점에서 왜 문제가 되며, 어떻게 완화할 수 있는가?

---

## Q2. init.groovy.d와 JCasC의 차이 및 선택 기준

**질문**: init.groovy.d와 JCasC(Configuration as Code)의 차이를 설명하고, 어떤 상황에서 각각을 사용해야 하는지 설명하시오.

**핵심 포인트**:
- JCasC는 선언적(YAML), init.groovy.d는 명령적(Groovy 코드)이라는 근본적 패러다임 차이
- JCasC의 장점: 버전 관리 용이(YAML diff가 명확), 재현성 보장(동일 YAML = 동일 결과), 디버깅이 쉬움, 학습 곡선이 낮음
- init.groovy.d의 장점: 무한한 유연성(Jenkins 전체 API 접근), 완전한 조건부 로직 가능, JCasC가 지원하지 않는 설정도 가능
- 우선순위 원칙: "JCasC로 할 수 있으면 JCasC, 안 되면 init.groovy.d"
- init.groovy.d를 써야 하는 실제 사례: 복잡한 조건부 크레덴셜 등록, JCasC가 미지원하는 플러그인 설정, 동적으로 결정되는 값에 기반한 설정
- init.groovy.d의 실행 시점이 "플러그인 로딩 후, UI 준비 전"인 이유와 이 타이밍의 중요성

**심화 질문**: JCasC와 init.groovy.d를 동시에 사용하는 환경에서 설정 충돌이 발생할 수 있다. 예를 들어 JCasC에서 보안 설정을 정의하고 init.groovy.d에서도 보안 설정을 변경한다면, 최종 상태는 어떻게 결정되며 이를 방지하기 위한 전략은 무엇인가?

---

## Q3. Jenkins Script Console의 보안 위험과 접근 제한

**질문**: Jenkins Script Console의 보안 위험을 설명하고, Script Console 접근을 제한해야 하는 이유를 설명하시오.

**핵심 포인트**:
- Script Console은 Jenkins 프로세스 내부에서 Groovy 코드를 직접 실행하는 REPL이며, Sandbox가 없다는 점
- 가장 심각한 위험: 크레덴셜 평문 노출. Jenkins는 크레덴셜을 암호화 저장하지만 복호화 키가 프로세스 메모리에 있으므로, Script Console에서 복호화 API를 호출하여 모든 비밀값을 읽을 수 있음
- 추가 위험: 모든 Job/빌드 삭제, 보안 설정 변경(인증 해제 등), 시스템 프로퍼티 변경으로 JVM 불안정화, 파일 시스템 접근
- 이것이 설계 결함이 아닌 이유: Jenkins가 빌드 중 크레덴셜을 사용해야 하므로 프로세스가 복호화 능력을 갖추어야 하며, 그 능력이 Script Console을 통해 노출되는 것
- 완화 방법: Matrix-based Security에서 "Administer"와 "Run Scripts" 권한 분리, Script Console 접근을 극소수 관리자에게만 부여, 감사 로그 활성화

**심화 질문**: 내부 직원이 Script Console을 통해 크레덴셜을 유출했다는 의심이 있다. 이를 탐지하고 사후 대응하기 위해 어떤 조치가 필요하며, 사전 예방을 위해 어떤 아키텍처 변경을 고려할 수 있는가? (Vault 연동, 크레덴셜 로테이션 등)

---

## Q4. Script Security Plugin의 Sandbox 역할과 부재 시 보안 문제

**질문**: Script Security Plugin의 Sandbox 모드가 하는 역할과, 이것이 없으면 어떤 보안 문제가 발생하는지 설명하시오.

**핵심 포인트**:
- Sandbox의 동작 원리: 허용된 API 목록(whitelist)을 유지하고, Pipeline Groovy 코드가 목록에 없는 API를 호출하면 실행을 차단
- 허용되는 API 예시: sh, echo, stage, parallel 같은 Pipeline DSL 기본 기능
- 차단되는 API 예시: java.lang.Runtime.exec(), System.exit(), Jenkins.getInstance() 같은 시스템 레벨 API
- Script Approval 프로세스: 차단된 API가 정당한 용도로 필요할 때 관리자가 메서드 시그니처를 승인하면 허용 목록에 추가됨
- Sandbox가 없다면: 개발자가 Jenkinsfile에서 Jenkins Master의 파일 시스템 접근, 크레덴셜 외부 전송, 내부 네트워크 스캔, 임의 프로세스 실행 등이 모두 가능해짐
- Multibranch Pipeline에서 외부 기여자의 PR을 자동 빌드할 때 Sandbox 없이는 외부 공격자가 악성 Jenkinsfile을 통해 내부 인프라를 공격할 수 있다는 점

**심화 질문**: Script Approval에서 한 번 승인된 메서드는 모든 Pipeline에서 사용 가능하다. 팀 A를 위해 승인한 위험한 메서드를 팀 B가 악용할 수 있는 상황에서, 팀별로 다른 보안 정책을 적용하려면 어떤 접근이 필요한가? (Folder-level 권한, 별도 Jenkins 인스턴스 등)

---

## Q5. 전역 Hook 구현: init.groovy.d vs Shared Library

**질문**: Jenkins 전역 Hook을 init.groovy.d로 구현하는 것과 Shared Library로 구현하는 것의 차이와 권장 방법을 설명하시오.

**핵심 포인트**:
- init.groovy.d 전역 Hook: Jenkins 시스템 레벨에서 동작하여 모든 빌드에 강제 적용됨. 개별 팀이 opt-out 할 수 없음
- Shared Library 전역 Hook: 각 팀이 `@Library`로 opt-in하여 사용. 버전 관리가 되고 테스트 가능
- init.groovy.d의 문제점: 부작용 제어가 어려움, 디버깅 난이도 높음, 특정 Job에서만 문제가 생겨도 원인 파악이 힘듦
- Shared Library의 장점: 버전 태깅으로 안정 버전 관리, 단위 테스트 가능, 팀별로 다른 버전 사용 가능
- 권장 방법: Shared Library에서 `standardPipeline` 같은 래퍼를 제공하고, 팀이 자발적으로 사용하도록 유도. 강제 적용이 필요하면 Organization Folder의 기본 Jenkinsfile 설정 활용
- 예외 상황: 보안 정책처럼 모든 빌드에 반드시 적용해야 하고 우회가 불가능해야 하는 경우에는 init.groovy.d가 적절할 수 있음

**심화 질문**: Shared Library로 전역 빌드 래퍼를 제공하는데, 일부 팀이 이를 사용하지 않아 보안 정책(빌드 아티팩트 스캔 등)이 적용되지 않는 문제가 있다. 강제 적용과 팀 자율성 사이에서 어떻게 균형을 잡을 수 있는가?

---

## Q6. Groovy 커스터마이징이 안티패턴이 되는 경우

**질문**: Groovy를 통한 Jenkins 커스터마이징이 "안티패턴"이 되는 경우를 구체적인 예시와 함께 설명하시오.

**핵심 포인트**:
- **안티패턴 1: init.groovy.d에서 외부 URL 호출** — `new GroovyShell().evaluate(new URL(...).text)` 패턴은 공급망 공격의 벡터가 됨. 외부 서버가 해킹당하면 Jenkins 시작 시마다 악성 코드가 실행됨
- **안티패턴 2: Script Console을 정기적 관리 도구로 사용** — 일회성 조사용인 Script Console을 매주 실행하는 운영 작업에 사용하면 실행 기록이 남지 않고, 실수로 잘못된 스크립트를 실행해도 롤백이 불가능함
- **안티패턴 3: JCasC로 가능한 설정을 init.groovy.d로 구현** — 보안 설정, 크레덴셜, 도구 설정 등 JCasC가 지원하는 영역을 굳이 Groovy 코드로 작성하면 유지보수 부채가 쌓이고 Jenkins 업그레이드 시 Internal API 변경으로 스크립트가 깨질 수 있음
- **안티패턴 4: Pipeline에서 Sandbox 우회를 위한 과도한 Script Approval** — 편의를 위해 위험한 메서드를 무분별하게 승인하면 Sandbox의 보안 의미가 사라짐
- **안티패턴 5: 시스템 프로퍼티 무분별 변경** — `System.setProperty()`로 JVM 설정을 변경하면 예측 불가능한 부작용이 발생하며, Jenkins 재시작 시 원래대로 돌아가므로 일관성이 깨짐
- 공통된 근본 원인: "Groovy로 할 수 있다"와 "Groovy로 해야 한다"를 구분하지 않는 것. 선언적 대안(JCasC, Shared Library, Plugin 설정)이 있으면 선언적 방법을 우선해야 함

**심화 질문**: 레거시 Jenkins 환경에서 init.groovy.d 스크립트가 20개 이상 쌓여 있고, 어떤 스크립트가 어떤 설정을 담당하는지 파악이 어려운 상황이다. 이를 JCasC 기반으로 마이그레이션하려면 어떤 단계를 거쳐야 하며, 마이그레이션 중 다운타임을 어떻게 최소화할 수 있는가?
