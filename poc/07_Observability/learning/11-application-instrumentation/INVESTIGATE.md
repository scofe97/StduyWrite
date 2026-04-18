# Ch09. Application Instrumentation - 점검 질문

## Q1. OTel API 호출이 기본적으로 no-op인 이유는 무엇인가?

**핵심 포인트**:
- API/SDK 분리 구조
- Provider 미등록 시 데이터 손실이 아니라 무시
- 라이브러리가 SDK에 의존하지 않게 하는 설계

## Q2. Java Agent와 Spring Boot Starter를 동시에 쓰면 왜 문제가 되는가?

**핵심 포인트**:
- 중복 span 생성
- 두 개의 TracerProvider 충돌
- 환경당 하나만 선택

## Q3. Breadth-first 계측 전략이 Depth-first보다 나은 이유는 무엇인가?

**핵심 포인트**:
- 분산 환경에서 end-to-end 가시성 확보 우선
- 한 서비스의 세부 계측은 나중에 추가 가능
- 프로덕션 이슈 추적에는 전체 경로가 더 중요

## Q4. service.name과 service.version을 직접 지정해야 하는 이유는 무엇인가?

**핵심 포인트**:
- Resource Detector가 자동 발견할 수 없는 값
- Grafana 필터와 버전별 비교의 기본 축
- 누락 시 분석 도구의 핵심 기능 사용 불가

## Q5. 새 span을 만드는 것보다 기존 span에 속성을 추가하는 것이 나을 때는 언제인가?

**핵심 포인트**:
- auto-instrumentation이 이미 span을 생성한 경우
- span 수 증가는 비용과 복잡도 증가
- 속성 추가만으로 충분한 컨텍스트 확보 가능
