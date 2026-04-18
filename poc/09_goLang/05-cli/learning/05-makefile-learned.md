# Makefile 문법 학습 정리

## 1. 기본 구조

```makefile
타겟: 의존성
	명령어
```

- **타겟**: `make 타겟명`으로 실행할 이름
- **의존성**: 이 타겟 실행 전에 먼저 실행할 타겟들
- **명령어**: 실행할 셸 명령 (반드시 **Tab**으로 시작!)

## 2. 핵심 규칙

### Tab vs Space

```makefile
# ✅ 올바름 (Tab)
build:
⇥go build .

# ❌ 에러 (Space)
build:
    go build .
```

> "missing separator" 에러 = Tab 대신 Space 사용

### 의존성

```makefile
run: build        # build 먼저 실행 후 run 실행
	./myapp

install: build    # build 먼저 실행 후 install 실행
	cp myapp ~/.local/bin/
```

## 3. 변수

### 정의와 사용

```makefile
# 변수 정의
BINARY_NAME := myapp
GO := go
FLAGS := -ldflags="-s -w"

# 변수 사용 (괄호로 감싸기)
build:
	$(GO) build $(FLAGS) -o $(BINARY_NAME) .

clean:
	rm -f $(BINARY_NAME)
```

### 변수 종류

| 문법 | 설명 |
|------|------|
| `=` | 재귀적 확장 (늦은 평가) |
| `:=` | 단순 확장 (즉시 평가) |
| `?=` | 값이 없을 때만 할당 |
| `+=` | 기존 값에 추가 |

```makefile
NAME := hello      # 즉시 평가 (권장)
NAME ?= default    # NAME이 없을 때만 default
NAME += world      # "hello world"
```

## 4. .PHONY

파일이 아닌 **명령어**임을 선언합니다.

```makefile
.PHONY: build test clean run

build:
	go build .
```

### 왜 필요한가?

```bash
# 만약 "clean"이라는 파일이 있다면?
touch clean

# .PHONY 없으면
make clean  # → "clean is up to date" (실행 안 됨!)

# .PHONY 있으면
make clean  # → 정상 실행
```

## 5. 자동 변수

| 변수 | 의미 |
|------|------|
| `$@` | 현재 타겟 이름 |
| `$<` | 첫 번째 의존성 |
| `$^` | 모든 의존성 |
| `$?` | 변경된 의존성만 |

```makefile
myapp: main.go utils.go
	go build -o $@ $^
# $@ = myapp
# $^ = main.go utils.go
```

## 6. 조건문

```makefile
OS := $(shell uname -s)

ifeq ($(OS), Darwin)
	BINARY := myapp-mac
else
	BINARY := myapp-linux
endif

build:
	go build -o $(BINARY) .
```

## 7. 셸 명령 실행

```makefile
# 셸 명령 결과를 변수에 저장
GIT_HASH := $(shell git rev-parse --short HEAD)
BUILD_TIME := $(shell date +%Y-%m-%d)

build:
	go build -ldflags="-X main.version=$(GIT_HASH)" .
```

## 8. 출력 제어

| 접두사 | 효과 |
|--------|------|
| `@` | 명령어 자체를 출력하지 않음 |
| `-` | 에러가 나도 계속 진행 |

```makefile
build:
	@echo "빌드 시작..."        # echo 명령 안 보임
	go build -o myapp .
	@echo "빌드 완료!"

clean:
	-rm myapp                   # 파일 없어도 에러 무시
	-rm *.log
```

**출력 비교:**

```bash
# @ 없을 때
$ make build
echo "빌드 시작..."
빌드 시작...

# @ 있을 때
$ make build
빌드 시작...
```

## 9. 패턴 규칙

```makefile
# %.o: %.c → 모든 .c 파일을 .o로 컴파일
%.o: %.c
	gcc -c $< -o $@

# 사용 예: main.c → main.o
```

## 10. 실전 예제 (Go 프로젝트)

```makefile
# 변수 정의
BINARY := jira-worklog-hook
GO := go
GOFLAGS := -ldflags="-s -w"
INSTALL_PATH := ~/.local/bin

# .PHONY 선언
.PHONY: all build test clean install help

# 기본 타겟
all: build

# 빌드
build:
	@echo "🔨 빌드 중..."
	$(GO) build $(GOFLAGS) -o $(BINARY) .
	@echo "✅ 빌드 완료: $(BINARY)"

# 테스트
test:
	@echo "🧪 테스트 실행..."
	$(GO) test -v ./...

# 정리
clean:
	@echo "🧹 정리 중..."
	-rm -f $(BINARY)

# 설치
install: build
	@echo "📦 설치 중..."
	cp $(BINARY) $(INSTALL_PATH)/
	@echo "✅ 설치 완료: $(INSTALL_PATH)/$(BINARY)"

# 도움말
help:
	@echo "사용 가능한 명령어:"
	@echo "  make build   - 바이너리 빌드"
	@echo "  make test    - 테스트 실행"
	@echo "  make clean   - 빌드 결과물 삭제"
	@echo "  make install - 시스템에 설치"
```

## 11. 자주 하는 실수

| 실수 | 해결 |
|------|------|
| Space 사용 | Tab 사용 |
| 변수에 `$` 빠뜨림 | `$(VARIABLE)` 형식 사용 |
| 파일과 타겟 이름 충돌 | `.PHONY` 추가 |
| 명령어 에러로 중단 | `-` 접두사 추가 |

## 12. 참고 자료

- [GNU Make 공식 문서](https://www.gnu.org/software/make/manual/)
- [Make 튜토리얼](https://makefiletutorial.com/)
