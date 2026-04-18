# 03. Makefile 기초

## 학습 목표
Go 프로젝트에서 Makefile을 활용하여 빌드, 설치, 정리 작업을 자동화하는 방법을 이해한다.

---

## Makefile이란?

> **면접 답변**: Makefile은 `make` 명령어와 함께 사용하는 빌드 자동화 도구입니다. 원래 C/C++ 프로젝트의 컴파일 과정을 자동화하기 위해 만들어졌지만, 현재는 언어와 무관하게 반복적인 명령어를 자동화하는 데 널리 사용됩니다. Go 프로젝트에서는 빌드, 테스트, 설치, 정리 등의 작업을 `make build`, `make test`처럼 간단한 명령으로 실행할 수 있게 해줍니다.

**왜 사용하는가?**
- 긴 명령어를 짧게: `go build -o bin/myapp -ldflags "-s -w" .` → `make build`
- 여러 명령어를 하나로: 빌드 + 테스트 + 설치를 `make install` 하나로
- 팀 전체가 동일한 방식으로 빌드

---

## Makefile 기본 구조

```makefile
타겟: 의존성
	명령어(탭 필수)
```

> **면접 답변**: Makefile은 타겟, 의존성, 명령어로 구성됩니다. 타겟은 실행할 작업의 이름이고, 의존성은 해당 타겟 실행 전에 먼저 실행되어야 할 다른 타겟입니다. 명령어는 반드시 탭으로 들여쓰기해야 하며, 스페이스를 사용하면 오류가 발생합니다.

```makefile
build:
	go build -o myapp .

run: build          # build가 먼저 실행됨
	./myapp
```

---

## 변수

### 변수 정의 방식

> **면접 답변**: Makefile에서 `:=`는 즉시 평가로 정의 시점의 값이 고정되고, `=`는 지연 평가로 사용 시점에 값이 결정됩니다. `?=`는 변수가 정의되지 않았을 때만 값을 할당하며, 환경 변수로 오버라이드할 수 있어 유연한 설정에 유용합니다.

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `:=` | 즉시 평가 (권장) | `BINARY := myapp` |
| `=` | 지연 평가 | `BINARY = myapp` |
| `?=` | 미정의시만 할당 | `BINARY ?= myapp` |

```makefile
BINARY := myapp
INSTALL_DIR := $(HOME)/.local/bin

build:
	go build -o $(BINARY) .
```

### 환경 변수 참조

```makefile
# 쉘 환경 변수 사용
INSTALL_DIR := $(HOME)/.local/bin
```

---

## .PHONY

> **면접 답변**: `.PHONY`는 해당 타겟이 실제 파일이 아니라 항상 실행되어야 하는 작업임을 선언합니다. Make는 기본적으로 타겟 이름과 같은 파일이 존재하면 "이미 최신"이라 판단하고 실행하지 않습니다. `.PHONY`에 등록하면 같은 이름의 파일이 있어도 항상 명령을 실행합니다.

```makefile
.PHONY: build clean run install

build:
	go build -o myapp .
```

**문제 상황:**
```bash
touch build          # build라는 파일 생성
make build           # "make: 'build' is up to date." 출력
```

**해결:** `.PHONY: build` 선언 → 파일 존재 여부 무관하게 항상 실행

---

## 출력 제어

### @ - 명령어 숨김

> **면접 답변**: Makefile에서 `@` 접두사는 명령어 자체의 출력을 숨깁니다. 기본적으로 Make는 실행하는 명령어를 먼저 출력하고 그 결과를 출력하는데, `@`를 붙이면 명령어는 숨기고 결과만 보여줍니다. 주로 echo 문에 사용하여 깔끔한 출력을 만듭니다.

```makefile
# @ 없이
build:
	echo "빌드 중..."    # 출력: echo "빌드 중..."
	                      #       빌드 중...

# @ 사용
build:
	@echo "빌드 중..."   # 출력: 빌드 중...
```

### - (하이픈) - 오류 무시

> **면접 답변**: `-` 접두사는 해당 명령이 실패해도 Make를 계속 진행하게 합니다. 예를 들어 `rm` 명령에서 파일이 없으면 오류가 발생하는데, `-rm`으로 작성하면 파일 유무와 관계없이 다음 명령을 실행합니다.

```makefile
clean:
	-rm -f myapp        # 파일 없어도 오류 무시
	@echo "정리 완료"
```

---

## 여러 줄 셸 명령

> **면접 답변**: Makefile에서 각 줄은 별도의 셸에서 실행됩니다. 여러 줄을 하나의 셸 명령으로 연결하려면 줄 끝에 백슬래시(`\`)로 줄을 이어야 하고, 셸 문법상 문장 끝에는 세미콜론(`;`)이 필요합니다.

```makefile
# 잘못된 예 - 각 줄이 별도 셸에서 실행
check:
	if [ -f myapp ]; then
		echo "존재"      # 오류: 별도 셸이라 if 문맥 없음
	fi

# 올바른 예 - 한 셸에서 실행
check:
	@if [ -f $(BINARY) ]; then \
		echo "$(BINARY) 존재함"; \
	else \
		echo "$(BINARY) 없음"; \
	fi
```

**규칙:**
- 마지막 줄 제외 모든 줄 끝에 `; \`
- 들여쓰기는 탭 사용

---

## 의존성

> **면접 답변**: Makefile에서 타겟 뒤에 콜론과 함께 다른 타겟을 나열하면 의존성이 됩니다. `run: build`라고 하면 run 실행 전에 build가 먼저 실행됩니다. 이를 통해 빌드 → 실행 순서를 보장할 수 있습니다.

```makefile
run: build           # build 먼저, 그다음 run
	./$(BINARY)

install: build       # build 먼저, 그다음 install
	cp $(BINARY) $(INSTALL_DIR)/
```

### 복수 의존성

> **면접 답변**: 여러 의존성을 지정할 때는 반드시 공백으로 구분해야 합니다. 쉼표를 사용하면 `clean,`처럼 쉼표가 타겟 이름의 일부로 인식되어 오류가 발생합니다. 의존성은 왼쪽에서 오른쪽 순서로 실행됩니다.

```makefile
# ❌ 잘못된 문법 - 쉼표 사용 불가
install: clean, build

# ✅ 올바른 문법 - 공백으로 구분
install: clean build
```

**실행 순서:** `clean` → `build` → `install`

---

## 설치/제거 패턴

> **면접 답변**: CLI 도구를 배포할 때 `~/.local/bin`에 설치하는 것이 일반적입니다. 이 디렉토리는 사용자 권한으로 접근 가능하고, 대부분의 시스템에서 기본 PATH에 포함됩니다. Makefile의 install 타겟은 빌드 후 바이너리를 이 경로에 복사하고, uninstall은 제거합니다.

```makefile
BINARY := myapp
INSTALL_DIR := $(HOME)/.local/bin

.PHONY: build clean install uninstall

build:
	@echo "빌드 중..."
	go build -o $(BINARY) .
	@echo "완료: $(BINARY)"

clean:
	@echo "정리 중..."
	-rm -f $(BINARY)

install: build
	@mkdir -p $(INSTALL_DIR)
	@cp $(BINARY) $(INSTALL_DIR)/
	@echo "설치 완료: $(INSTALL_DIR)/$(BINARY)"

uninstall:
	@rm -f $(INSTALL_DIR)/$(BINARY)
	@echo "제거 완료"
```

---

## 실습 결과

### 최종 Makefile

```makefile
BINARY := myapp
INSTALL_DIR := $(HOME)/.local/bin

.PHONY: build clean run check install uninstall

build:
	@echo "빌드 중..."
	go build -o $(BINARY) .
	@echo "완료: $(BINARY)"

clean:
	@echo "정리 중..."
	-rm -f $(BINARY)

run: build
	@echo "실행 중..."
	./$(BINARY)

check:
	@if [ -f $(BINARY) ]; then \
		echo "$(BINARY) 존재함"; \
	else \
		echo "$(BINARY) 없음 - make build 필요"; \
	fi

install: build
	@mkdir -p $(INSTALL_DIR)
	@cp $(BINARY) $(INSTALL_DIR)/
	@echo "설치 완료: $(INSTALL_DIR)/$(BINARY)"

uninstall:
	@rm -f $(INSTALL_DIR)/$(BINARY)
	@echo "제거 완료"
```

### 사용법

```bash
make build      # 빌드
make run        # 빌드 + 실행
make check      # 바이너리 존재 확인
make install    # ~/.local/bin에 설치
make uninstall  # 제거
make clean      # 정리
```

---

## 정리: 핵심 문법

| 문법 | 의미 |
|------|------|
| `타겟: 의존성` | 의존성 먼저 실행 |
| `:=` | 변수 즉시 평가 |
| `$(VAR)` | 변수 참조 |
| `.PHONY` | 항상 실행할 타겟 |
| `@` | 명령어 숨김 |
| `-` | 오류 무시 |
| `; \` | 여러 줄 연결 |

---

## 참고 자료
- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [Makefile Tutorial](https://makefiletutorial.com/)
