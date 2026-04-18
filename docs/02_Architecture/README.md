# Architecture 학습 문서

소프트웨어 아키텍처 핵심 주제를 체계적으로 정리한 학습 자료입니다.
(05_AIAgents는 추후 AI 관련 폴더로 이동 예정)

---

## 학습 경로

```
01_Architecture → 02_DDD → 03_EventDriven → 04_TestAutomation → 05_AIAgents
```

| 순서 | 주제 | 파일 수 | 핵심 내용 |
|------|------|---------|-----------|
| 1 | Architecture | 15 | 소프트웨어 아키텍처 기초, 패턴, Spring Cloud |
| 2 | DDD | 12 | 도메인 주도 설계, CQRS, 리팩토링 |
| 3 | EventDriven | 17 | 이벤트 기반 마이크로서비스, 스트리밍 |
| 4 | TestAutomation | 20 | Appium 기반 엔터프라이즈 테스트 프레임워크 |
| 5 | AIAgents | 13 | AI 에이전트 설계 및 구현 |

**총 파일 수**: 77개

---

## 01_Architecture

**출처**: Software Architecture with Spring (Packt)

소프트웨어 아키텍처의 기본 원칙부터 Spring 기반 구현까지 다룹니다.

| 파일 | 주제 |
|------|------|
| 01_Diving_into_Software_Architecture | 아키텍처 개요 |
| 02_Decision_Making_Processes | 의사결정 프로세스 |
| 03_Understanding_the_System_Context | 시스템 컨텍스트 이해 |
| 04_Monolithic_Architecture | 모놀리식 아키텍처 |
| 05_Client_Server_Architecture | 클라이언트-서버 아키텍처 |
| 06_Microservices_Architecture | 마이크로서비스 아키텍처 |
| 07_Microservices_Patterns_with_Spring_Cloud | Spring Cloud 패턴 |
| 08_Event_Driven_Architecture | 이벤트 기반 아키텍처 |
| 09_Pipe_and_Filter_and_Serverless_Architecture | 파이프/필터, 서버리스 |
| 10_Security | 보안 |
| 11_Observability | 관측성 |
| 12_Testing | 테스팅 |
| 13_Performance_and_Optimizations | 성능 최적화 |
| 14_Orchestration_with_Kubernetes | Kubernetes 오케스트레이션 |
| 15_Continuous_Integration_and_Continuous_Deployment | CI/CD |

---

## 02_DDD

**출처**: Domain-Driven Refactoring (O'Reilly)

DDD 전략적/전술적 패턴과 레거시 시스템 리팩토링 방법을 다룹니다.

| 파일 | 주제 |
|------|------|
| 01_Evolution_of_Domain_Driven_Design | DDD 발전 과정 |
| 02_Understanding_Complexity_Problem_Solution_Space | 복잡성 이해 |
| 03_Strategic_Patterns | 전략적 패턴 |
| 04_Tactical_Patterns | 전술적 패턴 |
| 05_Introducing_Refactoring_Principles | 리팩토링 원칙 |
| 06_Transitioning_from_Chaos | 혼돈에서 전환 |
| 07_Integrating_Events_with_CQRS | CQRS와 이벤트 통합 |
| 08_Refactoring_the_Database | 데이터베이스 리팩토링 |
| 09_DDD_Patterns_for_CI_CD | CI/CD를 위한 DDD 패턴 |
| 10_Transition_to_Microservices | 마이크로서비스 전환 |
| 11_Dealing_with_Events_and_Their_Evolution | 이벤트 진화 |
| 12_Orchestrating_Complexity | 복잡성 오케스트레이션 |

---

## 03_EventDriven

**출처**: Building Event-Driven Microservices (O'Reilly)

이벤트 기반 마이크로서비스의 설계, 구현, 운영 방법을 다룹니다.

| 파일 | 주제 |
|------|------|
| 01_이벤트_기반_마이크로서비스_필요성 | 필요성 |
| 02_이벤트_기반_마이크로서비스_기초 | 기초 개념 |
| 03_통신과_데이터_계약 | 통신 및 계약 |
| 04_기존_시스템과의_통합 | 레거시 통합 |
| 05_이벤트_기반_처리_기초 | 처리 기초 |
| 06_결정적_스트림_처리 | 결정적 처리 |
| 07_상태_기반_스트리밍 | 상태 기반 스트리밍 |
| 08_마이크로서비스_워크플로우_구축 | 워크플로우 구축 |
| 09_FaaS_기반_마이크로서비스 | FaaS 활용 |
| 10_기본_프로듀서_컨슈머_마이크로서비스 | 기본 프로듀서/컨슈머 |
| 11_헤비웨이트_프레임워크_마이크로서비스 | 헤비웨이트 프레임워크 |
| 12_라이트웨이트_프레임워크_마이크로서비스 | 라이트웨이트 프레임워크 |
| 13_이벤트_기반과_요청-응답_마이크로서비스_통합 | 통합 패턴 |
| 14_지원_도구 | 지원 도구 |
| 15_이벤트_기반_마이크로서비스_테스팅 | 테스팅 |
| 16_이벤트_기반_마이크로서비스_배포 | 배포 |
| 17_결론 | 결론 |

---

## 04_TestAutomation

**출처**: Create an Enterprise-Level Test Automation Framework with Appium (Packt)

Appium 기반 엔터프라이즈급 테스트 자동화 프레임워크 구축 방법을 다룹니다.

| 파일 | 주제 |
|------|------|
| 01_Automation_Framework_Overview | 프레임워크 개요 |
| 02_Creating_Wireframe_with_Spring_Boot | Spring Boot 와이어프레임 |
| 03_Configuring_Gradle | Gradle 설정 |
| 04_Creating_the_Properties_Files | 속성 파일 생성 |
| 05_Creating_Android_iOS_Web_Drivers | 드라이버 생성 |
| 06_Common_Mobile_Actions | 공통 모바일 액션 |
| 07_Creating_Page_Objects | 페이지 오브젝트 |
| 08_Writing_Your_First_Test_Suite | 첫 테스트 스위트 |
| 09_Importing_Test_Data | 테스트 데이터 임포트 |
| 10_Adding_BDD_Capabilities_with_Cucumber | Cucumber BDD |
| 11_Adding_Allure_and_Extent_Reports | 리포트 추가 |
| 12_Creating_PDF_Report_with_Screenshots | PDF 리포트 |
| 13_Enhancing_Framework_Screenshots | 스크린샷 향상 |
| 14_Testing_Multiple_Apps_and_Versions | 다중 앱/버전 테스트 |
| 15_Running_Scripts_or_Batch_Files | 스크립트 실행 |
| 16_API_Testing | API 테스팅 |
| 17_Device_Management_Functions | 디바이스 관리 |
| 18_Integrating_with_HP_ALM | HP ALM 통합 |
| 19_Localization_Testing | 지역화 테스팅 |
| 20_Parallel_Test_Execution | 병렬 실행 |

---

## 05_AIAgents

**출처**: Building Applications with AI Agents (O'Reilly)

AI 에이전트 시스템의 설계, 구현, 운영 방법을 다룹니다.

| 파일 | 주제 |
|------|------|
| 01_Introduction_to_Agents | 에이전트 소개 |
| 02_Designing_Agent_Systems | 시스템 설계 |
| 03_User_Experience_Design_for_Agentic_Systems | UX 설계 |
| 04_Tool_Use | 도구 사용 |
| 05_Orchestration | 오케스트레이션 |
| 06_Knowledge_and_Memory | 지식과 메모리 |
| 07_Learning_in_Agentic_Systems | 학습 |
| 08_From_One_Agent_to_Many | 단일→다중 에이전트 |
| 09_Validation_and_Measurement | 검증과 측정 |
| 10_Monitoring_in_Production | 프로덕션 모니터링 |
| 11_Improvement_Loops | 개선 루프 |
| 12_Protecting_Agentic_Systems | 보안 |
| 13_Human_Agent_Collaboration | 인간-에이전트 협업 |

---

## 학습 권장 순서

### 기초 단계
1. **01_Architecture** 전체 학습 - 아키텍처 기초 확립

### 중급 단계
2. **02_DDD** (01-06) - DDD 전략/전술 패턴
3. **03_EventDriven** (01-08) - 이벤트 기반 기초

### 심화 단계
4. **02_DDD** (07-12) - CQRS, 리팩토링
5. **03_EventDriven** (09-17) - 프레임워크, 운영

### 실무 적용
6. **04_TestAutomation** - 테스트 자동화 프레임워크
7. **05_AIAgents** - AI 에이전트 시스템

---

## 출처

| 섹션 | 도서 | 출판사 |
|------|------|--------|
| Architecture | Software Architecture with Spring | Packt |
| DDD | Domain-Driven Refactoring | O'Reilly |
| EventDriven | Building Event-Driven Microservices | O'Reilly |
| TestAutomation | Create an Enterprise-Level Test Automation Framework with Appium | Packt |
| AIAgents | Building Applications with AI Agents | O'Reilly |
