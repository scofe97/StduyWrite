---

## 📌 핵심 요약
> 이 장에서는 **규제 산업(금융, 의료, 정부)**에서 **도메인 주도 설계(DDD)**를 CI/CD에 적용하는 패턴을 다룬다. 핵심은 **Bounded Context**로 도메인을 분리하고, **Ubiquitous Language**로 소통하며, **RBAC/ABAC**로 접근을 제어하고, **GDPR/HIPAA/PCI DSS** 등 규제 준수를 파이프라인에 통합하는 것이다.

## 🎯 학습 목표
이 내용을 읽고 나면:
- [ ] DDD의 핵심 개념(Bounded Context, Ubiquitous Language, Aggregate, Domain Events)을 설명할 수 있다
- [ ] 규제 산업에서 CI/CD 파이프라인에 DDD 원칙을 적용하는 방법을 이해할 수 있다
- [ ] RBAC와 ABAC의 차이점과 적용 시나리오를 구분할 수 있다
- [ ] 주요 규제(GDPR, HIPAA, PCI DSS)의 CI/CD 적용 방법을 설명할 수 있다
- [ ] 규제 액션을 CI/CD 파이프라인에 통합하는 전략을 수립할 수 있다

## 📖 본문 정리

### 1. 도메인 주도 설계(DDD) 개요

DDD는 **비즈니스 도메인의 복잡성**을 정확하게 반영하는 소프트웨어 설계 접근법이다.

```mermaid
flowchart TB
    subgraph DDD["도메인 주도 설계"]
        UL["Ubiquitous Language<br/>보편 언어"]
        BC["Bounded Context<br/>경계 컨텍스트"]
        Agg["Aggregates<br/>집합체"]
        DE["Domain Events<br/>도메인 이벤트"]
    end

    subgraph Benefits["핵심 이점"]
        B1["비즈니스 정렬"]
        B2["복잡성 관리"]
        B3["명확한 경계"]
        B4["효과적 소통"]
    end

    DDD --> Benefits
```

> 💬 **비유**: DDD는 건축 청사진과 같다. 건물의 각 구역(Bounded Context)에 적합한 설계를 적용하고, 모든 이해관계자가 같은 용어(Ubiquitous Language)로 소통한다.

---

### 2. 도메인 주도 CI/CD 설계 패턴

#### 2.1 Bounded Context와 CI/CD

각 Bounded Context는 독립적인 마이크로서비스로 매핑되며, 개별적으로 개발, 테스트, 배포된다.

```mermaid
flowchart TB
    subgraph Domain["도메인 레이어"]
        UL[Ubiquitous Language]
        SK[Shared Kernel]
        BC1[Bounded Context 1<br/>결제 처리]
        BC2[Bounded Context 2<br/>계정 관리]
        BC3[Bounded Context 3<br/>사기 탐지]
    end

    subgraph CI["CI 레이어"]
        SA[정적 분석]
        UT[단위 테스트]
        IT[통합 테스트]
        Build[아티팩트 빌드]
    end

    subgraph CD["CD 레이어"]
        Config[설정]
        Provision[환경 프로비저닝]
        SysTest[시스템 테스트]
        Release[프로덕션 릴리스]
    end

    Domain --> CI --> CD
```

#### 2.2 도메인 주도 CI/CD의 이점

| 이점 | 설명 |
|------|------|
| **커뮤니케이션 향상** | 공통 언어로 개발자, 도메인 전문가, 이해관계자 간 소통 개선 |
| **복잡성 감소** | 핵심 도메인에 집중하여 기술 부채 최소화 |
| **품질 향상** | DDD 패턴(Entity, Aggregate, Domain Event) 적용으로 신뢰성 증가 |
| **빠른 배포** | Feature Toggle, Canary, Blue-Green 배포 자동화 |
| **확장성** | 도메인 경계에 맞춘 독립적 확장 가능 |
| **문제 해결 용이** | 명확한 경계로 문제 식별 및 해결 간소화 |

---

### 3. DDD 원칙과 규제 액션 구현

규제 액션(Regulation Actions)은 코드 리뷰, 보안 스캔, 감사, 승인, 문서화 등 규정 준수를 보장하는 단계이다.

```mermaid
flowchart TB
    subgraph Principles["DDD 원칙"]
        UL2["Ubiquitous Language<br/>규제 용어 정의"]
        BC4["Bounded Contexts<br/>규제 영역 분리"]
        SD["Strategic Design<br/>핵심 도메인 우선순위"]
        CM["Context Mapping<br/>컨텍스트 간 조정"]
        DE2["Domain Events<br/>규제 액션 트리거"]
    end

    subgraph Flow["흐름"]
        UL2 --> BC4
        BC4 --> SD
        SD --> CM
        CM --> BC4
        DE2 --> Trigger[파이프라인 실행]
    end
```

#### 3.1 DDD 원칙별 규제 적용

| 원칙 | 규제 적용 방법 |
|------|---------------|
| **Ubiquitous Language** | 규제 액션의 기준, 규칙, 기대치를 공통 언어로 정의 |
| **Bounded Contexts** | 서브도메인별 규제 액션 격리, 의존성 충돌 방지 |
| **Strategic Design** | 핵심 도메인에 규제 액션 우선순위 부여 |
| **Context Mapping** | 컨텍스트 간 규제 액션 조정, 일관성 보장 |
| **Domain Events** | 이벤트를 트리거로 규제 액션 자동 실행 |

---

### 4. 접근 제어 (Access Control)

규제 산업에서 접근 제어는 DDD의 핵심 구성요소이다.

#### 4.1 RBAC (Role-Based Access Control)

역할에 권한을 연결하여 관리를 단순화한다.

```mermaid
flowchart LR
    subgraph Users["사용자"]
        U1[Alice]
        U2[Bob]
        U3[Carol]
    end

    subgraph Roles["역할"]
        R1[Developer]
        R2[Auditor]
        R3[Admin]
    end

    subgraph Permissions["권한"]
        P1[코드 읽기]
        P2[코드 쓰기]
        P3[배포 승인]
        P4[감사 로그 조회]
    end

    U1 --> R1 --> P1
    U1 --> R1 --> P2
    U2 --> R2 --> P1
    U2 --> R2 --> P4
    U3 --> R3 --> P1
    U3 --> R3 --> P2
    U3 --> R3 --> P3
    U3 --> R3 --> P4
```

#### 4.2 ABAC (Attribute-Based Access Control)

사용자, 액션, 리소스의 다양한 속성을 고려하여 세밀한 제어를 제공한다.

```mermaid
flowchart TB
    subgraph Attributes["속성"]
        UserAttr["사용자 속성<br/>부서, 직급, 인증 수준"]
        ActionAttr["액션 속성<br/>읽기, 쓰기, 삭제"]
        ResourceAttr["리소스 속성<br/>민감도, 분류, 소유자"]
        EnvAttr["환경 속성<br/>시간, 위치, 디바이스"]
    end

    subgraph Engine["정책 엔진"]
        Policy[정책 평가]
    end

    subgraph Decision["결정"]
        Allow[허용]
        Deny[거부]
    end

    Attributes --> Engine
    Engine --> Decision
```

#### 4.3 RBAC vs ABAC 비교

| 특성 | RBAC | ABAC |
|------|------|------|
| **복잡도** | 낮음 | 높음 |
| **유연성** | 제한적 | 매우 유연 |
| **세분화** | 역할 단위 | 속성 단위 |
| **관리** | 역할 관리 | 정책 관리 |
| **적합 환경** | 정적 조직 | 동적, 복잡한 환경 |

---

### 5. 의료 애플리케이션의 접근 제어 예시

```mermaid
flowchart TB
    subgraph Security["보안 컨텍스트"]
        SC[사용자 역할/권한/컨텍스트]
    end

    subgraph PolicyEngine["정책 평가 엔진"]
        PE[정책 평가]
    end

    subgraph AuthDecision["인가 결정"]
        Allow2[허용]
        Deny2[거부]
    end

    subgraph DataSec["데이터 보안"]
        Encrypt[데이터 암호화]
        Audit[감사 추적]
    end

    subgraph Compliance["규정 준수"]
        Reg[HIPAA/GDPR]
        Report[감사 보고서]
    end

    Security --> PolicyEngine
    PolicyEngine --> AuthDecision
    AuthDecision --> DataSec
    DataSec --> Compliance
```

**핵심 구성요소:**
- **세분화된 인가**: 사용자 컨텍스트 기반 동적 접근 결정
- **정책 평가 엔진**: 접근 제어 정책 평가
- **데이터 암호화**: 민감 데이터(환자 기록) 암호화
- **보안 감사 추적**: 모든 접근 이벤트 기록
- **규정 준수**: HIPAA, GDPR 준수 보장

---

### 6. 규제에 따른 아티팩트 빌드

#### 6.1 주요 규제 표준

| 규제 | 적용 영역 | 핵심 요구사항 |
|------|-----------|---------------|
| **GDPR** | EU 개인정보 보호 | 데이터 수집/처리 지침, 삭제권 |
| **HIPAA** | 미국 의료정보 보호 | 환자 건강 정보 보호 표준 |
| **PCI DSS** | 결제 카드 보안 | 카드 정보 저장/전송 보안 표준 |

#### 6.2 규제 준수 CI/CD 파이프라인

```mermaid
flowchart TB
    subgraph Analysis["1. 규제 분석"]
        RA[규제 요구사항 식별]
        DP[데이터 보호]
        Privacy[프라이버시]
        Sec[보안]
        Audit2[감사]
    end

    subgraph Modeling["2. 도메인 모델링"]
        Entity[Entity 설계]
        VO[Value Object]
        Agg2[Aggregate]
        AC[접근 제어 내장]
        Encrypt2[암호화 내장]
    end

    subgraph Pipeline["3. CI/CD 파이프라인"]
        AutoTest[자동화된 테스트]
        StaticAnalysis[정적 분석]
        SecScan[보안 스캔]
        CompAudit[규정 준수 감사]
    end

    subgraph Monitoring["4. 모니터링"]
        ContMon[지속적 모니터링]
        CompReport[규정 준수 보고서]
        AuditLog[감사 로그]
    end

    subgraph Deploy["5. 배포"]
        SecDeploy[보안 배포]
        RBAC2[RBAC]
        Approval[승인 워크플로우]
    end

    Analysis --> Modeling --> Pipeline --> Monitoring --> Deploy
```

#### 6.3 규제 준수 통합 도구

| 도구 | 용도 |
|------|------|
| **SonarQube** | 코드 품질 및 보안 분석 |
| **OWASP ZAP** | 보안 취약점 스캔 |
| **ComplianceAsCode** | 규정 준수 자동화 |
| **Trivy** | 컨테이너 취약점 스캔 |

---

### 7. DDD와 CI/CD 통합 예시

#### 7.1 전자상거래 회사 사례

```mermaid
flowchart TB
    A["1. 핵심 도메인 식별<br/>(온라인 쇼핑)"] --> B["2. Ubiquitous Language<br/>생성"]
    B --> C["3. Bounded Context 정의"]

    subgraph BC["Bounded Contexts"]
        INV[재고 관리]
        ORD[주문 처리]
        CUS[고객 관계]
    end

    C --> BC

    subgraph CICD["CI/CD 파이프라인"]
        Commit[코드 커밋]
        Test[자동화 테스트]
        BuildDeploy[빌드 & 배포]
    end

    BC --> CICD

    subgraph Feedback["피드백 루프"]
        Toggle[Feature Toggle]
        Gather[피드백 수집]
        Refine[도메인 모델 개선]
    end

    CICD --> Feedback
    Feedback --> Outcome["탄력적이고<br/>적응 가능한<br/>소프트웨어"]
```

#### 7.2 금융 서비스 결제 시스템 예시

```mermaid
flowchart LR
    subgraph VCS["버전 관리"]
        Git[Git Repository]
    end

    subgraph CI2["CI"]
        Build2[빌드]
        UnitTest[단위 테스트]
        CodeQuality[코드 품질]
        Artifact[아티팩트 생성]
    end

    subgraph CD2["CD"]
        IaC[IaC<br/>Terraform]
        Container[컨테이너화<br/>Docker]
        K8s[Kubernetes<br/>배포]
        BlueGreen[Blue-Green<br/>배포]
    end

    subgraph DDD2["DDD"]
        Domain[도메인 모델]
        BoundedCtx[Bounded Context<br/>결제, 계정, 사기탐지]
        Events[Domain Events]
    end

    subgraph Collab["협업"]
        DevOps[DevOps 팀]
        DomainExpert[도메인 전문가]
        Ops[운영 팀]
    end

    subgraph Monitor["모니터링"]
        Logging[로깅]
        Metrics[메트릭]
        Tracing[분산 추적]
        Alerts[알림]
    end

    Git --> CI2 --> CD2
    DDD2 --> CI2
    Collab --> DDD2
    CD2 --> Monitor
```

---

### 8. DDD 구현 시 성능 고려사항

#### 8.1 주요 도전과제

| 도전과제 | 해결 방안 |
|----------|----------|
| **복잡한 도메인 모델** | 모듈식 아키텍처로 분리 테스트/배포 |
| **학습 곡선** | 팀 교육 투자, 점진적 도입 |
| **DDD-CI/CD 불일치** | DDD 모델과 CI/CD 목표 정렬 |
| **과도한 세분화** | 핵심 도메인에 집중 |
| **커뮤니케이션 부족** | 정기적인 도메인 워크숍 |

#### 8.2 성공적인 DDD 구현 단계

```mermaid
flowchart LR
    A["1. 도메인<br/>깊이 이해"] --> B["2. Ubiquitous<br/>Language 생성"]
    B --> C["3. Bounded<br/>Context 정의"]
    C --> D["4. CI/CD<br/>파이프라인 설계"]
    D --> E["5. 자동화<br/>테스트 구축"]
    E --> F["6. Feature<br/>Toggle 적용"]
    F --> G["7. 모니터링<br/>& 로깅"]
    G --> H["8. 지속적<br/>개선"]
```

---

### 9. 규제 산업별 DDD 적용 예시

| 산업 | 적용 사례 |
|------|-----------|
| **금융** | 결제 처리 Bounded Context 분리, 계정 관리/사기 탐지와 격리 |
| **의료** | 환자 기록 관리와 치료 프로토콜 분리, HIPAA 준수 |
| **정부** | 사업자 등록과 규정 준수 검사 분리, 복잡한 워크플로우 반영 |

---

## 🔍 심화 학습

### 추가 조사 내용

- **Event Sourcing과 CQRS**: DDD와 함께 사용되는 이벤트 기반 아키텍처 패턴
- **Saga Pattern**: 분산 트랜잭션 관리를 위한 마이크로서비스 패턴
- **Anti-Corruption Layer**: 레거시 시스템과 새 도메인 모델 간 번역 계층

### 출처
- "Domain-Driven Design" by Eric Evans
- "Implementing Domain-Driven Design" by Vaughn Vernon
- [ComplianceAsCode 문서](https://complianceascode.readthedocs.io/)
- [OWASP 보안 가이드](https://owasp.org/)

---

## 💡 실무 적용 포인트

### 이런 상황에서 사용하세요

- **복잡한 비즈니스 로직**: 단순 CRUD가 아닌 복잡한 도메인 규칙이 있을 때
- **규제 산업**: 금융, 의료, 정부 등 엄격한 규정 준수가 필요할 때
- **마이크로서비스 전환**: 모놀리식에서 마이크로서비스로 전환 시 경계 정의
- **대규모 팀**: 여러 팀이 동일 도메인에서 작업할 때

### 주의할 점 / 흔한 실수

- ⚠️ **단순 도메인에 DDD 적용**: 복잡한 비즈니스 규칙이 없으면 과도한 오버헤드
- ⚠️ **Ubiquitous Language 무시**: 기술팀과 비즈니스팀 간 용어 불일치
- ⚠️ **Bounded Context 과다 분할**: 너무 세분화하면 관리 복잡성 증가
- ⚠️ **규제 액션 자동화 부족**: 수동 규제 검증은 병목 현상 유발

### 면접에서 나올 수 있는 질문

- Q: Bounded Context란 무엇이며 마이크로서비스와 어떤 관계가 있나요?
- Q: RBAC와 ABAC의 차이점은 무엇이며 언제 각각을 사용하나요?
- Q: DDD에서 Ubiquitous Language가 왜 중요한가요?
- Q: 규제 산업에서 CI/CD 파이프라인에 규정 준수를 어떻게 통합하나요?
- Q: Domain Events를 활용한 규제 액션 자동화 방법을 설명해주세요.

---

## ✅ 핵심 개념 체크리스트

- [ ] DDD의 핵심 개념(Bounded Context, Aggregate, Entity, Value Object)을 설명할 수 있는가?
- [ ] Ubiquitous Language의 중요성과 적용 방법을 이해하고 있는가?
- [ ] 규제 산업에서 DDD 원칙을 CI/CD에 적용하는 방법을 알고 있는가?
- [ ] RBAC와 ABAC의 차이를 구분하고 적절한 상황에 적용할 수 있는가?
- [ ] GDPR, HIPAA, PCI DSS의 기본 요구사항을 알고 있는가?
- [ ] Domain Events를 활용한 규제 액션 트리거 방법을 설명할 수 있는가?

---

## 🔗 참고 자료

- 📚 필수 도서: "Domain-Driven Design" by Eric Evans
- 📚 실무 도서: "Implementing Domain-Driven Design" by Vaughn Vernon
- 📄 공식 문서: [ComplianceAsCode](https://complianceascode.readthedocs.io/)
- 📄 공식 문서: [OWASP Security Guidelines](https://owasp.org/)
- 🎬 추천 영상: [Domain-Driven Design Europe](https://www.youtube.com/@daboraddevconf)

---
