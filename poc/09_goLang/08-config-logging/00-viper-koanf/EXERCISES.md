# Koanf 실습 과제

## 목표

koanf를 활용하여 유연한 설정 관리 시스템을 구현합니다.

---

## Phase 1: 기본 파일 로드

### Task 1.1: 프로젝트 초기화
- [ ] `go mod tidy` 실행하여 의존성 정리
- [ ] 필요한 패키지 설치:
  ```bash
  go get -u github.com/knadh/koanf/v2
  go get -u github.com/knadh/koanf/parsers/yaml
  go get -u github.com/knadh/koanf/providers/file
  go get -u github.com/knadh/koanf/providers/env
  ```
- [ ] go.mod 파일에 의존성 추가 확인

### Task 1.2: Load 함수 구현 (config/config.go)
- [ ] `file.Provider(path)` 로 파일 제공자 생성
- [ ] `yaml.Parser()` 로 YAML 파서 사용
- [ ] `k.Load(provider, parser)` 로 설정 로드
- [ ] `k.Unmarshal("", &cfg)` 로 구조체에 바인딩
- [ ] 테스트: `go run main.go` → 설정 값 출력

### Task 1.3: main.go에서 설정 사용
- [ ] `config.Load("configs/config.yaml")` 호출
- [ ] 에러 처리 추가
- [ ] 각 설정 값 출력 (Server.Port, Database.Host, Log.Level)
- [ ] 테스트: 출력 값이 config.yaml과 일치하는지 확인

---

## Phase 2: 환경변수 오버라이드

### Task 2.1: LoadWithEnv 함수 구현
- [ ] 파일 먼저 로드
- [ ] `env.Provider("APP_", ".", envKeyReplacer)` 사용
- [ ] 환경변수 키 변환 규칙 구현:
  - `APP_SERVER_PORT` → `server.port`
  - `APP_DATABASE_HOST` → `database.host`
  - `APP_LOG_LEVEL` → `log.level`
- [ ] 테스트:
  ```bash
  APP_SERVER_PORT=9090 go run main.go
  # Server Port: 9090 (8080이 아닌)
  ```

### Task 2.2: 우선순위 확인
- [ ] config.yaml: port=8080
- [ ] 환경변수: APP_SERVER_PORT=9090
- [ ] 확인: 환경변수 값(9090)이 적용됨
- [ ] 테스트: 환경변수 제거 시 파일 값(8080)으로 복원

---

## Phase 3: 다중 환경 설정

### Task 3.1: LoadMultiple 함수 구현
- [ ] 여러 파일 경로를 받아 순서대로 로드
- [ ] 나중에 로드한 파일이 이전 값을 덮어씀
- [ ] 테스트:
  ```go
  cfg, _ := LoadMultiple("configs/config.yaml", "configs/config.dev.yaml")
  // config.dev.yaml의 값이 우선
  ```

### Task 3.2: LoadWithProfile 함수 구현
- [ ] 기본 설정 파일 경로와 프로파일 이름을 받음
- [ ] 프로파일 파일명 생성: `config.yaml` → `config.dev.yaml`
- [ ] 기본 → 프로파일 순서로 로드
- [ ] 테스트:
  ```go
  cfg, _ := LoadWithProfile("configs/config.yaml", "dev")
  // port=3000, level="debug" (config.dev.yaml 값)
  ```

### Task 3.3: 프로파일 환경변수 연동
- [ ] `APP_PROFILE` 환경변수로 프로파일 선택
- [ ] main.go에서 환경변수 읽어서 프로파일 결정
- [ ] 테스트:
  ```bash
  APP_PROFILE=dev go run main.go
  # 개발 환경 설정 적용됨
  ```

---

## Phase 4: 동적 설정 조회

### Task 4.1: Get 함수들 구현
- [ ] `Get(key string) interface{}` 구현
- [ ] `GetString(key string) string` 구현
- [ ] `GetInt(key string) int` 구현
- [ ] 테스트:
  ```go
  port := config.GetInt("server.port")
  host := config.GetString("database.host")
  ```

### Task 4.2: 중첩 키 조회
- [ ] 점(.) 표기법으로 중첩 키 접근
- [ ] `server.port`, `database.host` 등
- [ ] 존재하지 않는 키 처리 (기본값 반환)
- [ ] 테스트:
  ```go
  value := config.Get("server.port")      // 8080
  missing := config.Get("nonexistent")    // nil
  ```

### Task 4.3: 기본값 지원
- [ ] `GetWithDefault(key string, defaultValue interface{})` 구현
- [ ] 키가 없을 때 기본값 반환
- [ ] 테스트:
  ```go
  timeout := config.GetIntWithDefault("server.timeout", 30)
  // config에 없으면 30 반환
  ```

---

## Phase 5: 고급 기능

### Task 5.1: 설정 검증
- [ ] 필수 설정 값 검증 함수 구현
- [ ] 포트 범위 검증 (1-65535)
- [ ] 필수 필드 검증 (빈 문자열 체크)
- [ ] 테스트: 잘못된 설정 시 에러 반환

### Task 5.2: Watch (설정 변경 감지) - 선택
- [ ] 파일 변경 시 자동 리로드
- [ ] `file.Provider` 대신 watch 사용
- [ ] 콜백으로 변경 알림
- [ ] 테스트: 실행 중 파일 수정 → 자동 반영

### Task 5.3: 설정 덤프
- [ ] 현재 설정을 출력하는 함수
- [ ] 민감 정보 마스킹 (password)
- [ ] 테스트: 설정 전체 출력 (password는 ***로 표시)

---

## Bonus Tasks

### Bonus 1: JSON 지원
- [ ] JSON 파일 로드 지원 추가
- [ ] 파일 확장자로 파서 자동 선택
- [ ] 테스트: config.json 파일 로드

### Bonus 2: 플래그 연동
- [ ] `basicflag.Provider` 사용
- [ ] CLI 플래그가 모든 설정을 오버라이드
- [ ] 테스트:
  ```bash
  go run main.go --server.port=7000
  # 파일과 환경변수보다 플래그 우선
  ```

### Bonus 3: 설정 구조체 생성기
- [ ] YAML 파일에서 Go 구조체 자동 생성
- [ ] 타입 추론 (숫자, 문자열, 불리언)
- [ ] 테스트: 새 설정 파일로 구조체 생성

---

## 학습 체크리스트

### 기본 개념
- [ ] koanf.New()로 인스턴스 생성
- [ ] Provider와 Parser 개념 이해
- [ ] k.Load()로 설정 로드
- [ ] k.Unmarshal()로 구조체 바인딩

### 다중 소스
- [ ] 파일 Provider 사용
- [ ] 환경변수 Provider 사용
- [ ] 키 변환 함수 작성
- [ ] 소스 병합 순서 이해

### 고급 기능
- [ ] 동적 키 조회 (k.Get, k.String, k.Int)
- [ ] 중첩 키 접근 ("server.port")
- [ ] 부분 언마샬링 (특정 섹션만)
- [ ] 설정 검증

---

## 성공 기준

모든 Task를 완료하면:

```bash
$ go run main.go
Config loaded from: configs/config.yaml
Server Port: 8080
Database Host: localhost
Log Level: info

$ APP_SERVER_PORT=9090 go run main.go
Config loaded from: configs/config.yaml
Environment variables applied
Server Port: 9090          # 오버라이드됨
Database Host: localhost
Log Level: info

$ APP_PROFILE=dev go run main.go
Config loaded from: configs/config.yaml
Profile config merged: configs/config.dev.yaml
Server Port: 3000          # dev 설정
Database Host: localhost
Database Name: myapp_dev   # dev 설정
Log Level: debug           # dev 설정
```

---

**진행 방법**:
1. Phase 1부터 순서대로 진행
2. 각 Task의 체크박스를 완료하면 체크
3. 막히면 `HINTS.md` 참고 (스포일러 주의!)
4. 모든 Phase 완료 후 Bonus 도전
5. `LEARNED.md`에 학습 내용 정리

**예상 소요 시간**: 1.5-2시간
