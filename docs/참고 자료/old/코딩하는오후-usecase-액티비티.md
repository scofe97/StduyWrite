# 누가 내 Usecase를 옮겼을까

> 코딩하는오후 YouTube 영상 요약
> 주제: Activity Interface를 통한 비즈니스 플로우 보존

## 핵심 문제 제기

### 사라지는 비즈니스 플로우

```
[설계 단계]
요구사항 정의서 → 유스케이스 → 화면 설계

[구현 결과]
- 정적 데이터 → 데이터베이스 테이블
- 비즈니스 프로세스 → 프론트엔드 기능에 의존
- 백엔드 → CRUD만 남음
```

**문제**: 현업과 도출한 비즈니스 플로우가 구현 단계에서 CRUD로 단순화됨

**원인**: Controller → Service → Repository 구조에서 Service의 역할이 모호해짐

---

## Activity Interface 개념

### 용어 정의

| 용어 | 정의 | 추상화 수준 |
|------|------|-------------|
| **UseCase** | 시스템이 무엇을 할 수 있는지 (상호작용 중심) | 높음 (개괄적) |
| **Activity** | 구체적인 활동 단위 (회원가입, 로그인 등) | 중간 |
| **Action** | Activity 내 세부 작업 (검증, 조회 등) | 낮음 (구체적) |

### 관계 구조

```
UseCase (높은 추상화)
    └── Activity (구체적 활동)
            └── Action (세부 작업)
```

**핵심 아이디어**: Service Interface를 Activity Interface로 재정의

---

## Activity 다이어그램과 코드 매핑

### 설계 예시 (강의 계획서 작성)

```
[Activity Diagram]
관리자: 학습 과정 등록
    ↓
교수자: 강의 계획서 작성
    ├── 과목 조회 (searchSubject)
    ├── 커리큘럼 초기화 (initCurriculum)
    └── 강의 내용 업데이트 (updateCurriculum)
```

### 코드 매핑

```java
// Activity Interface - 비즈니스 플로우 표현
public interface LecturePlanActivity {
    Subject searchSubject(Long subjectId);
    Curriculum initCurriculum(CurriculumInit init);
    Curriculum updateCurriculum(CurriculumUpdate update);
}
```

**장점**: 메서드명에서 비즈니스 흐름이 드러남
- `init` → 초기 설정
- `update` → 내용 수정

---

## 아키텍처 전제 조건

### 1. 모듈 분리

```
[Component 모듈] - 시스템을 위한 공통 컴포넌트
├── auditing/     # 감사 (생성자, 수정자, 히스토리)
├── container/    # 데이터 이동 객체 (DTO, VO)
├── sign/         # 인증/인가
└── datasource/   # 데이터 소스 설정

[Business Domain 모듈] - 비즈니스 로직
├── activity/     # Activity Interface
├── entity/       # 도메인 엔티티
├── port/         # 포트 (Hexagonal)
├── service/      # Activity 구현체
└── infra/        # 인프라 어댑터
```

### 2. 테스트 코드 필수

| 테스트 대상 | 필수 여부 | 이유 |
|-------------|-----------|------|
| Entity + Activity | **필수** | 순수 비즈니스 로직 검증 |
| API | 선택 | 프레임워크 의존 |
| Infrastructure | 선택 | 구현 아키텍처 의존 |
| Component | 필요시 | 별도 서브 프로젝트로 분리 권장 |

---

## Hexagonal Architecture 통합

### 폴더 구조 (Business Domain)

```
domain/
├── activity/           # Activity Interface
│   ├── CreateFaraActivity.java
│   └── UpdateFaraActivity.java
├── entity/             # 도메인 엔티티
│   └── Fara.java
├── port/               # 포트 정의
│   ├── in/             # Inbound (Driving)
│   └── out/            # Outbound (Driven)
├── service/            # Activity 구현
│   └── FaraService.java  // implements Activity
└── infra/              # 인프라 어댑터
    ├── api/
    └── persistence/
```

### Port와 Activity 관계

```java
// Port를 통해 외부 의존성 추상화
public class FaraService implements CreateFaraActivity {
    private final FaraPort faraPort;  // Outbound Port

    @Override
    public Fara create(FaraCreate command) {
        // 비즈니스 로직
        return faraPort.save(fara);
    }
}
```

---

## 도메인 간 통신

### 이벤트 기반 통신

```
[Fara 도메인] ─── Event ───→ [결제 도메인]
         (직접 참조 X)
```

**원칙**: 도메인 간 직접 참조 대신 이벤트 통신 사용

---

## Component vs Business Domain

### Component 모듈 특징

| 항목 | 설명 |
|------|------|
| **Auditing** | 생성/수정 정보, 변경 이력 추적 |
| **Container** | Response, Search(Input DTO), VO(Output) |
| **DataSource** | DB 종류별 설정 (Oracle, MySQL, Redis, File) |
| **Sign** | 인증/인가 관련 |

### Business Domain 모듈 특징

- Activity Interface로 비즈니스 플로우 표현
- Hexagonal Architecture 적용
- 테스트 코드 필수
- 도메인 간 이벤트 통신

---

## Rule vs Domain

**발표자 관점**: Rule은 비즈니스 도메인이 아니라 Component

```
Rule (조건 → 결과)
    └── Component로 분류
    └── 도메인이 아님
```

---

## 핵심 정리

### 소리치는 아키텍처 (Screaming Architecture)

1. **설계 문서와 코드의 일치**: Activity 다이어그램 ↔ Activity Interface
2. **비즈니스 플로우 보존**: CRUD로 사라지지 않음
3. **명확한 역할 분리**: Component vs Business Domain

### 적용 효과

| Before | After |
|--------|-------|
| Service 인터페이스 불필요 논쟁 | Activity Interface로 명확한 역할 |
| CRUD로 비즈니스 플로우 소실 | 코드에서 비즈니스 흐름 파악 가능 |
| 설계 문서와 코드 불일치 | 다이어그램 ↔ 구현 매칭 |

---

## 참고 리포지토리

- 발표자 GitHub: 구현 아키텍처 예제 (작업 진행 중, 약 50-60% 완성)

---

## 학습 포인트

1. **Service Interface 재해석**: Activity Interface로서의 역할 부여
2. **계층 구조**: UseCase → Activity → Action
3. **모듈 분리**: Component와 Business Domain 명확히 구분
4. **테스트 전략**: Business Domain은 테스트 필수
5. **도메인 통신**: 이벤트 기반으로 느슨한 결합 유지
