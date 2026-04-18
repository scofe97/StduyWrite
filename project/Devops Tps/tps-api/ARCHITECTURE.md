# TPS-API 아키텍처 및 폴더 구조

## 개요

TPS-API는 **Hexagonal Architecture(육각형 아키텍처)**, 또는 **Ports and Adapters** 패턴을 적용한 Spring Boot 애플리케이션입니다.

### 왜 Hexagonal Architecture인가?

```
장점:
├── 비즈니스 로직이 외부 기술에 의존하지 않음
├── 테스트 용이성 (Mock 쉽게 적용)
├── 기술 교체 용이 (MyBatis → JPA, PostgreSQL → MongoDB)
└── 명확한 책임 분리
```

---

## 폴더 구조

```
tps-api/
├── build.gradle                          # 빌드 설정
├── settings.gradle                       # Gradle 설정
├── README.md                             # API 명세 및 실행 가이드
├── ARCHITECTURE.md                       # 현재 문서
│
├── api-test/                             # HTTP 테스트 파일
│   ├── connection-api.http
│   ├── repository-api.http
│   └── branch-api.http
│
└── src/main/
    ├── java/com/runnershigh/tps/
    │   │
    │   ├── TpsApiApplication.java        # Spring Boot 진입점
    │   │
    │   ├── domain/                       # 📦 도메인 레이어
    │   │   ├── common/                   #    공통 엔티티
    │   │   │   └── BaseEntity.java
    │   │   ├── connection/               #    Connection 도메인
    │   │   │   ├── Connection.java
    │   │   │   ├── ConnectionStatus.java
    │   │   │   └── ProviderType.java
    │   │   ├── repository/               #    Repository 도메인
    │   │   │   ├── Repository.java
    │   │   │   ├── RepositoryStatus.java
    │   │   │   └── BranchStrategyType.java
    │   │   ├── branch/                   #    Branch 도메인
    │   │   │   ├── Branch.java
    │   │   │   ├── BranchStatus.java
    │   │   │   └── BranchType.java
    │   │   ├── user/                     #    User 도메인 (예정)
    │   │   └── project/                  #    Project 도메인 (예정)
    │   │
    │   ├── application/                  # 📦 애플리케이션 레이어
    │   │   ├── port/                     #    포트 정의
    │   │   │   ├── in/                   #    인바운드 포트 (UseCase)
    │   │   │   │   ├── ConnectionUseCase.java
    │   │   │   │   ├── RepositoryUseCase.java
    │   │   │   │   └── BranchUseCase.java
    │   │   │   └── out/                  #    아웃바운드 포트 (Repository)
    │   │   │       ├── ConnectionRepository.java
    │   │   │       ├── RepositoryRepository.java
    │   │   │       └── BranchRepository.java
    │   │   └── service/                  #    서비스 구현체
    │   │       ├── ConnectionService.java
    │   │       ├── RepositoryService.java
    │   │       └── BranchService.java
    │   │
    │   ├── adapter/                      # 📦 어댑터 레이어
    │   │   ├── in/                       #    인바운드 어댑터
    │   │   │   └── web/                  #    REST API
    │   │   │       ├── ConnectionController.java
    │   │   │       ├── RepositoryController.java
    │   │   │       ├── BranchController.java
    │   │   │       ├── GlobalExceptionHandler.java
    │   │   │       └── dto/              #    요청/응답 DTO
    │   │   │           ├── ApiResponse.java
    │   │   │           ├── connection/
    │   │   │           ├── repository/
    │   │   │           └── branch/
    │   │   └── out/                      #    아웃바운드 어댑터
    │   │       └── persistence/          #    영속성 어댑터
    │   │           ├── ConnectionMapper.java      # MyBatis Mapper 인터페이스
    │   │           ├── ConnectionPersistenceAdapter.java
    │   │           ├── RepositoryMapper.java
    │   │           ├── RepositoryPersistenceAdapter.java
    │   │           ├── BranchMapper.java
    │   │           └── BranchPersistenceAdapter.java
    │   │
    │   └── infrastructure/               # 📦 인프라 레이어
    │       └── config/                   #    설정
    │           └── MyBatisConfig.java
    │
    └── resources/
        ├── application.yml               # 애플리케이션 설정
        ├── mapper/                       # MyBatis XML 매퍼
        │   ├── ConnectionMapper.xml
        │   ├── RepositoryMapper.xml
        │   └── BranchMapper.xml
        └── db/migration/                 # Flyway 마이그레이션
            └── V1__init_schema.sql
```

---

## 레이어 상세 설명

### 1. Domain Layer (도메인 레이어)

```
목적: 비즈니스 핵심 로직과 엔티티 정의
의존성: 없음 (순수 Java)
```

**구성 이유**:
- 비즈니스 규칙을 캡슐화하여 외부 기술 변경에 영향받지 않음
- 도메인 엔티티는 데이터베이스나 프레임워크에 의존하지 않음
- 상태 변경 메서드(activate, deactivate)는 도메인 내부에서 관리

**예시**:
```java
// Connection 도메인 - 비즈니스 로직 포함
public class Connection extends BaseEntity {
    public void activate() {
        this.status = ConnectionStatus.ACTIVE;  // 비즈니스 규칙
        updateTimestamp();
    }
}
```

---

### 2. Application Layer (애플리케이션 레이어)

```
목적: 유스케이스 정의 및 도메인 조합
의존성: Domain Layer에만 의존
```

#### 2.1 Port-In (인바운드 포트)

**위치**: `application/port/in/`

**목적**:
- 외부에서 애플리케이션을 호출하는 인터페이스 정의
- Controller가 의존하는 계약 (Contract)
- Command 객체로 입력 데이터 캡슐화

**구성 이유**:
- Controller가 Service 구현체에 직접 의존하지 않음
- 유스케이스 단위로 API 명세 파악 가능
- Command/Query 분리로 의도 명확화

---

#### 2.2 Port-Out (아웃바운드 포트)

**위치**: `application/port/out/`

**목적**:
- 애플리케이션이 외부 시스템에 요청하는 인터페이스 정의
- Service가 의존하는 저장소/외부 서비스 계약
- 실제 구현은 Adapter에서 담당

**구성 이유**:
- Service가 MyBatis나 JPA에 직접 의존하지 않음
- 테스트 시 Mock 객체로 쉽게 대체 가능
- 저장소 기술 교체 시 Service 코드 변경 불필요

---

#### 2.3 Service (서비스)

**위치**: `application/service/`

**목적**:
- UseCase(Port-In) 구현체
- 비즈니스 유스케이스 오케스트레이션
- 트랜잭션 경계 관리

**구성 이유**:
- 도메인 객체를 조합하여 유스케이스 완성
- 여러 Repository를 조합하는 비즈니스 흐름 관리
- @Transactional로 데이터 일관성 보장

---

### 3. Adapter Layer (어댑터 레이어)

```
목적: 외부 세계와 애플리케이션 연결
의존성: Application Layer의 Port에 의존
```

#### 3.1 Adapter-In (인바운드 어댑터)

**위치**: `adapter/in/web/`

**목적**:
- HTTP 요청을 UseCase 호출로 변환
- 요청 유효성 검증
- 응답 DTO 변환

**구성 이유**:
- REST API 외에 gRPC, CLI, 이벤트 핸들러 등 추가 가능
- Controller는 Port-In에만 의존하므로 Service 구현 변경에 영향 없음
- DTO와 Domain 분리로 API 버전 관리 용이

---

#### 3.2 Adapter-Out (아웃바운드 어댑터)

**위치**: `adapter/out/persistence/`

**목적**:
- Port-Out 인터페이스 구현
- 도메인 객체와 영속성 계층 연결
- MyBatis Mapper 호출

**구성 이유**:
- MyBatis 대신 JPA, R2DBC 등으로 쉽게 교체 가능
- PersistenceAdapter가 Mapper를 래핑하여 도메인 객체 반환
- 도메인이 영속성 기술에 오염되지 않음

**구조**:
```
PersistenceAdapter (Port-Out 구현)
       │
       ▼
    Mapper (MyBatis Interface)
       │
       ▼
  Mapper.xml (SQL)
       │
       ▼
   PostgreSQL
```

---

### 4. Infrastructure Layer (인프라 레이어)

**위치**: `infrastructure/`

**목적**:
- 기술적 설정 및 구성
- 프레임워크 설정

**현재 구성**:
- `config/MyBatisConfig.java`: MyBatis Mapper 스캔 설정

**향후 추가 예정**:
- `security/`: Spring Security 설정
- `kafka/`: Kafka Producer/Consumer 설정
- `observability/`: OpenTelemetry 설정

---

## 의존성 방향

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Controller ──────────────────────┐                        │
│   (Adapter-In)                     │                        │
│                                    ▼                        │
│                              ┌──────────────┐               │
│                              │   UseCase    │               │
│                              │  (Port-In)   │               │
│                              └──────┬───────┘               │
│                                     │                        │
│                                     ▼                        │
│                              ┌──────────────┐               │
│                              │   Service    │               │
│                              │ (implements  │               │
│                              │   UseCase)   │               │
│                              └──────┬───────┘               │
│                                     │                        │
│                                     ▼                        │
│                              ┌──────────────┐               │
│                              │  Repository  │               │
│                              │  (Port-Out)  │               │
│                              └──────┬───────┘               │
│                                     │                        │
│   PersistenceAdapter ◄──────────────┘                        │
│   (Adapter-Out)                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘

핵심: 화살표 방향이 안쪽(Domain)을 향함 = 의존성 역전
```

---

## 파일 명명 규칙

| 구분 | 패턴 | 예시 |
|------|------|------|
| 도메인 엔티티 | `{Domain}.java` | `Connection.java` |
| 상태 Enum | `{Domain}Status.java` | `ConnectionStatus.java` |
| 인바운드 포트 | `{Domain}UseCase.java` | `ConnectionUseCase.java` |
| 아웃바운드 포트 | `{Domain}Repository.java` | `ConnectionRepository.java` |
| 서비스 | `{Domain}Service.java` | `ConnectionService.java` |
| 컨트롤러 | `{Domain}Controller.java` | `ConnectionController.java` |
| Mapper 인터페이스 | `{Domain}Mapper.java` | `ConnectionMapper.java` |
| Persistence Adapter | `{Domain}PersistenceAdapter.java` | `ConnectionPersistenceAdapter.java` |
| 요청 DTO | `{Domain}Request.java` | `ConnectionRequest.java` |
| 응답 DTO | `{Domain}Response.java` | `ConnectionResponse.java` |

---

## 새 도메인 추가 시 체크리스트

1. **Domain Layer**
   - [ ] `domain/{domain}/` 폴더 생성
   - [ ] `{Domain}.java` 엔티티 생성
   - [ ] `{Domain}Status.java` 등 Enum 생성

2. **Application Layer**
   - [ ] `port/in/{Domain}UseCase.java` 생성
   - [ ] `port/out/{Domain}Repository.java` 생성
   - [ ] `service/{Domain}Service.java` 생성

3. **Adapter Layer**
   - [ ] `adapter/in/web/{Domain}Controller.java` 생성
   - [ ] `adapter/in/web/dto/{domain}/` DTO 생성
   - [ ] `adapter/out/persistence/{Domain}Mapper.java` 생성
   - [ ] `adapter/out/persistence/{Domain}PersistenceAdapter.java` 생성

4. **Resources**
   - [ ] `mapper/{Domain}Mapper.xml` 생성
   - [ ] `db/migration/V{n}__{domain}.sql` 마이그레이션 추가
