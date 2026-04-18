# Learning Go, 2nd Edition 참조 가이드

**문서 위치**: `~/내 드라이브/study/runners-high/docs/Learning Go, 2nd Edition/`

---

## 챕터별 매핑

| 챕터 | 파일명 | 관련 학습 모듈 |
|------|--------|---------------|
| 01 | Setting_Up_Your_Go_Environment.md | **20-docker-k8s** (빌드 환경) |
| 02 | Primitive_Types_and_Declarations.md | 기초 (타입 시스템) |
| 03 | Predeclared_Types_and_Declarations.md | **13-config** (구조체 정의) |
| 04 | Composite_Types.md | **15-generics** (슬라이스, 맵) |
| 05 | Functions.md | **10-cobra-cli** (함수, 다중 반환값) |
| 06 | Pointers.md | 기초 (포인터 이해) |
| 07 | Types_Methods_and_Interfaces.md | **11-http-server**, **12-testing** (인터페이스, Mock) |
| 08 | Generics.md | **15-generics** ⭐ 핵심 |
| 09 | Errors.md | **10-cobra-cli**, **12-testing**, **17-database** (에러 처리) |
| 10 | Modules_Packages_and_Imports.md | **10-cobra-cli**, **13-config**, **20-docker-k8s** (패키지 구조) |
| 11 | Go_Tooling.md | **20-docker-k8s** (빌드, 린트) |
| 12 | Concurrency_in_Go.md | **18-worker-pool** ⭐ 핵심, **14-observability**, **19-websocket** |
| 13 | The_Standard_Library.md | **11-http-server** ⭐ 핵심, **14-observability**, **17-database**, **19-websocket** |
| 14 | The_Context.md | **16-context** ⭐ 핵심, **11-http-server**, **17-database**, **18-worker-pool** |
| 15 | Writing_Tests.md | **12-testing** ⭐ 핵심 |
| 16 | Reflect_Unsafe_Cgo.md | 고급 (리플렉션, unsafe) |

---

## 학습 모듈별 필독 챕터

### 10. Cobra CLI
```
필독: 05_Functions.md, 09_Errors.md
참조: 10_Modules_Packages_and_Imports.md
```

### 11. HTTP Server (Gin)
```
필독: 13_The_Standard_Library.md
참조: 07_Types_Methods_and_Interfaces.md, 14_The_Context.md
```

### 12. Testing
```
필독: 15_Writing_Tests.md
참조: 07_Types_Methods_and_Interfaces.md, 09_Errors.md
```

### 13. Config (Viper)
```
필독: 10_Modules_Packages_and_Imports.md
참조: 03_Predeclared_Types_and_Declarations.md
```

### 14. Observability
```
필독: 13_The_Standard_Library.md
참조: 12_Concurrency_in_Go.md, 14_The_Context.md
```

### 15. Generics
```
필독: 08_Generics.md
참조: 04_Composite_Types.md, 07_Types_Methods_and_Interfaces.md
```

### 16. Context
```
필독: 14_The_Context.md
참조: 12_Concurrency_in_Go.md, 13_The_Standard_Library.md
```

### 17. Database
```
필독: 13_The_Standard_Library.md
참조: 14_The_Context.md, 09_Errors.md
```

### 18. Worker Pool
```
필독: 12_Concurrency_in_Go.md
참조: 14_The_Context.md, 09_Errors.md
```

### 19. WebSocket
```
필독: 12_Concurrency_in_Go.md
참조: 13_The_Standard_Library.md, 14_The_Context.md
```

### 20. Docker & K8s
```
필독: 11_Go_Tooling.md
참조: 01_Setting_Up_Your_Go_Environment.md, 10_Modules_Packages_and_Imports.md
```

---

## 면접 대비 핵심 챕터

| 주제 | 챕터 | 키워드 |
|------|------|--------|
| **동시성** | 12_Concurrency_in_Go.md | 고루틴, 채널, select, mutex, race condition |
| **에러 처리** | 09_Errors.md | sentinel error, error wrapping, errors.Is/As |
| **인터페이스** | 07_Types_Methods_and_Interfaces.md | 암시적 구현, nil interface, type assertion |
| **제네릭** | 08_Generics.md | 타입 파라미터, 제약 조건, any/comparable |
| **컨텍스트** | 14_The_Context.md | 취소 전파, 타임아웃, 값 전달 |
| **테스팅** | 15_Writing_Tests.md | table-driven, 벤치마크, 커버리지 |

---

## 추천 학습 순서 (책 기준)

1. **기초 강화** (이미 학습한 경우 복습용)
   - 02, 03: 타입 시스템
   - 04: 복합 타입
   - 05, 06: 함수와 포인터

2. **객체지향 → Go 방식**
   - 07: 인터페이스 (Java의 interface와 비교)
   - 08: 제네릭 (Java Generics와 비교)

3. **실무 필수**
   - 09: 에러 처리
   - 12: 동시성 (가장 중요!)
   - 14: Context

4. **프로덕션 준비**
   - 15: 테스팅
   - 13: 표준 라이브러리
   - 11: 도구

5. **고급 (선택)**
   - 16: Reflect, Unsafe, Cgo

---

## 추가 학습 자료

### 분산 시스템 (Go)

| 자료 | 설명 |
|------|------|
| [Go로 배우는 분산 시스템 (GopherCon Korea 2024)](https://www.youtube.com/watch?v=4awGzz9IhyQ) | 김수빈(당근) - Go로 분산 시스템 구현 |
| [Containers from Scratch (GOTO 2018)](https://www.youtube.com/watch?v=8fi7uSYlOdc) | Liz Rice - Go로 컨테이너 구현 |
| [Build a Container in Go (InfoQ)](https://www.infoq.com/articles/build-a-container-golang/) | 100줄 Go 코드로 컨테이너 |

**관련 학습 모듈**:
- **18-worker-pool**: 동시성 패턴 (분산 시스템 기초)
- **16-context**: 취소 전파, 타임아웃 (분산 환경 필수)
- **20-docker-k8s**: 컨테이너화, 배포

**분산 시스템 핵심 개념**:
- 합의 알고리즘 (Raft, Paxos)
- 분산 트랜잭션
- 서비스 디스커버리
- 로드 밸런싱
- Circuit Breaker 패턴
