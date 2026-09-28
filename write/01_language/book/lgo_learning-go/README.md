---
title: Learning Go 2판 — 정독 인덱스
tags: [moc, study-index, book, go, golang, language]
status: draft
source:
  - 《Learning Go, 2nd Edition》(Jon Bodner, O'Reilly) — 본문 16장, 장별 PDF 16개 · 약 138,000단어(pdftotext 추출 기준)
  - 원본 PDF — GoogleDrive/내 드라이브/book/Learning Go, 2nd Edition/
related:
  - ./05-01.Go%20%ED%95%A8%EC%88%98%EB%8A%94%20%EC%97%AC%EB%9F%AC%20%EA%B0%92%EC%9D%84%20%EB%8F%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EC%98%A4%EB%A5%98%EB%8A%94%20%EB%A7%88%EC%A7%80%EB%A7%89%20%EA%B0%92%EC%9E%85%EB%8B%88%EB%8B%A4.md
  - ./05-02.%ED%95%A8%EC%88%98%EB%8A%94%20%EA%B0%92%EC%9D%B4%EA%B3%A0%20%ED%81%B4%EB%A1%9C%EC%A0%80%EB%8A%94%20%EB%B0%94%EA%B9%A5%20%EB%B3%80%EC%88%98%EB%A5%BC%20%EB%B6%99%EC%9E%A1%EC%8A%B5%EB%8B%88%EB%8B%A4.md
  - ./05-03.defer%20%EB%8A%94%20%ED%95%A8%EC%88%98%EA%B0%80%20%EB%81%9D%EB%82%A0%20%EB%95%8C%20%EC%A0%95%EB%A6%AC%ED%95%98%EA%B3%A0%20%EC%9D%B8%EC%9E%90%EB%8A%94%20%EB%8A%98%20%EB%B3%B5%EC%82%AC%EB%90%A9%EB%8B%88%EB%8B%A4.md
  - ./04-01.%EC%95%88%EC%AA%BD%20%EB%B8%94%EB%A1%9D%EC%9D%98%20%EA%B0%99%EC%9D%80%20%EC%9D%B4%EB%A6%84%EC%9D%80%20%EB%B0%94%EA%B9%A5%20%EB%B3%80%EC%88%98%EB%A5%BC%20%EA%B0%80%EB%A6%BD%EB%8B%88%EB%8B%A4.md
  - ./04-02.for%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%84%A4%20%EA%B0%80%EC%A7%80%20%EB%B0%98%EB%B3%B5%EC%9D%84%20%EC%94%81%EB%8B%88%EB%8B%A4.md
  - ./04-03.switch%20%EB%8A%94%20%EA%B8%B0%EB%B3%B8%EC%9C%BC%EB%A1%9C%20%EB%B9%A0%EC%A0%B8%EB%82%98%EA%B0%80%EA%B3%A0%20break%20%EB%8A%94%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EA%B3%A0%EB%A6%85%EB%8B%88%EB%8B%A4.md
  - ./03-01.slice%20%EB%8A%94%20%EB%B0%B0%EC%97%B4%EC%9D%84%20%EB%82%98%EB%88%A0%20%EC%93%B0%EB%8A%94%20%EC%B0%BD%EC%9E%85%EB%8B%88%EB%8B%A4.md
  - ./03-02.%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%80%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EC%9D%B4%EA%B3%A0%20map%20%EC%9D%80%20%EC%97%86%EB%8A%94%20%ED%82%A4%EC%97%90%20%EC%A0%9C%EB%A1%9C%20%EA%B0%92%EC%9D%84%20%EB%8F%8C%EB%A0%A4%EC%A4%8D%EB%8B%88%EB%8B%A4.md
  - ./03-03.struct%20%EB%8A%94%20%ED%83%80%EC%9E%85%EC%9D%B4%20%EB%8B%A4%EB%A5%B8%20%EA%B0%92%EC%9D%84%20%EC%9D%B4%EB%A6%84%EC%9C%BC%EB%A1%9C%20%EB%AC%B6%EC%8A%B5%EB%8B%88%EB%8B%A4.md
  - ./02-01.%ED%83%80%EC%9E%85%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%EC%84%9E%EC%9D%B4%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%EB%A6%AC%ED%84%B0%EB%9F%B4%EB%A7%8C%20%EC%9C%A0%EC%97%B0%ED%95%A9%EB%8B%88%EB%8B%A4.md
  - ./02-02.var%20%EC%99%80%20%EC%A7%A7%EC%9D%80%20%EC%84%A0%EC%96%B8%EC%9D%80%20%EC%9D%98%EB%8F%84%EB%A5%BC%20%EB%93%9C%EB%9F%AC%EB%82%B4%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%9E%85%EB%8B%88%EB%8B%A4.md
  - ./01-01.go%20%EB%AA%85%EB%A0%B9%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%8B%A4%EB%93%AC%EA%B3%A0%20%EA%B2%80%EC%82%AC%ED%95%A9%EB%8B%88%EB%8B%A4.md
  - ../../README.md
  - ../../../roadmap/go-roadmap.md
  - ../../../02_os/project/gonet-lab/README.md
  - ../../../02_os/project/netpath-lab/README.md
learning:
  topic: learning-go
  scope: durable
  level: 입문
  last_verified: null   # 아직 Phase 4 자답·복습 회차 없음
  blocked_count: null   # 검증 전이라 막힌 문항 수가 없음
  next_lesson: "1~13장 학습 세션(설명 → 회상 → 실습) — 노트는 작성됨. 이어서 14장 노트 작성"
updated: 2026-09-28
---

# Learning Go 2판 — 정독 인덱스

---

> Jon Bodner 의 『Learning Go』 2판을 장 단위로 정독하며 정리하는 책 종속 학습 노트 모음입니다. Go 문법을 처음 제대로 익히는 것이 목적이고, 이 폴더의 노트가 Go 로드맵 1~5단계의 노트 칸을 채웁니다.

## Go 문법 책을 01_language 에 두는 이유

> 이 책은 네트워크 책이 아니라 언어 책입니다. 문법·관용구·표준 라이브러리를 다루므로 `01_language/book/` 에 둡니다.

Go 를 쓰는 기존 문서는 모두 `02_os/project/` 의 실습 랩에 있습니다. [gonet-lab](../../../02_os/project/gonet-lab/README.md) 은 소켓과 커널 자원을, [netpath-lab](../../../02_os/project/netpath-lab/README.md) 은 에러 값이 이름표가 되는 경로를 다룹니다. 두 랩 모두 Go 문법을 안다고 보고 진행하기 때문에, 문법 자체를 차근차근 쌓을 자리가 따로 없었습니다.

이 책이 그 자리를 맡습니다. slice 가 배열을 어떻게 공유하는지, 인터페이스가 왜 암묵적으로 구현되는지를 여기서 먼저 익히면, 랩 코드에서 같은 문법을 만났을 때 이 노트로 돌아와 확인할 수 있습니다.

『Network Programming with Go』는 문법을 다 익힌 뒤 읽는 서비스 구현서라 이 폴더에 넣지 않습니다. 그 책은 로드맵 6단계 자리이고, 나중에 정독할 때 `02_os/book/` 에 둡니다.



## 장 구성과 로드맵 단계 대응

> 본문 16장 중 1~15장이 필수이고, 16장(reflect·unsafe·cgo)은 선택입니다. 단계는 [Go 학습 로드맵](../../../roadmap/go-roadmap.md)의 단계별 표를 그대로 따릅니다.

단어 수는 장별 PDF 를 `pdftotext` 로 추출해 센 값이라 웹 판형의 머리글·꼬리글이 조금 섞여 있습니다. 편을 몇 개로 나눌지 정하는 참고값으로만 씁니다.

| 장 | 원제 | PDF 쪽 | 단어 | 로드맵 단계 |
|:--:|------|:--:|--:|------|
| 1 | Setting Up Your Go Environment | 18 | 4,445 | 1단계 · 문법 |
| 2 | Predeclared Types and Declarations | 20 | 6,823 | 1단계 · 문법 |
| 3 | Composite Types | 36 | 10,214 | 1단계 · 문법 |
| 4 | Blocks, Shadows, and Control Structures | 31 | 7,947 | 1단계 · 문법 |
| 5 | Functions | 28 | 7,545 | 1단계 · 문법 |
| 6 | Pointers | 30 | 7,813 | 1단계 · 문법 |
| 7 | Types, Methods, and Interfaces | 41 | 12,040 | 2단계 · 타입 설계 |
| 8 | Generics | 25 | 6,447 | 2단계 · 타입 설계 |
| 9 | Errors | 22 | 5,800 | 2단계 · 타입 설계 |
| 10 | Modules, Packages, and Imports | 43 | 13,214 | 3단계 · 관용구와 도구 |
| 11 | Go Tooling | 28 | 7,768 | 3단계 · 관용구와 도구 |
| 12 | Concurrency in Go | 35 | 10,716 | 4단계 · 동시성 |
| 13 | The Standard Library | 33 | 9,307 | 3단계 · 관용구와 도구 |
| 14 | The Context | 23 | 6,462 | 3단계 · 관용구와 도구 |
| 15 | Writing Tests | 39 | 11,127 | 5단계 · 테스트와 성능 |
| 16 | Here Be Dragons: Reflect, Unsafe, and Cgo | 34 | 10,339 | 3단계 · 선택 |

읽는 순서는 책의 장 순서를 따릅니다. 12장 동시성은 로드맵에서 4단계지만 책에서는 3단계 장(13·14장)보다 먼저 나오는데, 저자가 정한 흐름을 바꾸지 않고 그대로 읽습니다.



## 작성된 정독 노트

> 1~13장 노트 마흔한 편을 썼습니다. 한 세션에 한 장씩 이어서 씁니다.

진척 표시는 ◻ 미착수, ⏳ 진행 중, ✅ 완료입니다. 한 장을 몇 편으로 나눌지는 그 장 원문을 읽은 뒤 분할안을 먼저 정하고, 빈 노트를 미리 만들어 두지 않습니다.

| 장 | 노트 | 진척 |
|:--:|------|:--:|
| 1 | [01-01.go 명령 하나로 만들고 다듬고 검사합니다](./01-01.go%20%EB%AA%85%EB%A0%B9%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%8B%A4%EB%93%AC%EA%B3%A0%20%EA%B2%80%EC%82%AC%ED%95%A9%EB%8B%88%EB%8B%A4.md) | ✅ 설치와 단일 바이너리 · go.mod · go build · go fmt 와 세미콜론 자동 삽입 · go vet · Makefile · 편집기와 Playground · 호환성 약속, 연습 문제 1~3 |
| 2 | [02-01.타입은 자동으로 섞이지 않고 리터럴만 유연합니다](./02-01.%ED%83%80%EC%9E%85%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%EC%84%9E%EC%9D%B4%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%EB%A6%AC%ED%84%B0%EB%9F%B4%EB%A7%8C%20%EC%9C%A0%EC%97%B0%ED%95%A9%EB%8B%88%EB%8B%A4.md), [02-02.var 와 짧은 선언은 의도를 드러내는 선택입니다](./02-02.var%20%EC%99%80%20%EC%A7%A7%EC%9D%80%20%EC%84%A0%EC%96%B8%EC%9D%80%20%EC%9D%98%EB%8F%84%EB%A5%BC%20%EB%93%9C%EB%9F%AC%EB%82%B4%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%9E%85%EB%8B%88%EB%8B%A4.md) | ✅ 2편: 02-01 제로 값 · 리터럴 · 정수·부동소수점·복소수 · 문자열과 rune · 명시적 변환과 truthy 없음 · 타입 없는 리터럴, 02-02 var 와 := · const · 타입 있는/없는 상수 · 쓰지 않는 변수 · 이름 짓기, 연습 문제 1~3 |
| 3 | [03-01.slice 는 배열을 나눠 쓰는 창입니다](./03-01.slice%20%EB%8A%94%20%EB%B0%B0%EC%97%B4%EC%9D%84%20%EB%82%98%EB%88%A0%20%EC%93%B0%EB%8A%94%20%EC%B0%BD%EC%9E%85%EB%8B%88%EB%8B%A4.md), [03-02.문자열은 바이트이고 map 은 없는 키에 제로 값을 돌려줍니다](./03-02.%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%80%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EC%9D%B4%EA%B3%A0%20map%20%EC%9D%80%20%EC%97%86%EB%8A%94%20%ED%82%A4%EC%97%90%20%EC%A0%9C%EB%A1%9C%20%EA%B0%92%EC%9D%84%20%EB%8F%8C%EB%A0%A4%EC%A4%8D%EB%8B%88%EB%8B%A4.md), [03-03.struct 는 타입이 다른 값을 이름으로 묶습니다](./03-03.struct%20%EB%8A%94%20%ED%83%80%EC%9E%85%EC%9D%B4%20%EB%8B%A4%EB%A5%B8%20%EA%B0%92%EC%9D%84%20%EC%9D%B4%EB%A6%84%EC%9C%BC%EB%A1%9C%20%EB%AC%B6%EC%8A%B5%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 03-01 배열 · slice · append 와 용량 증가 · make · slice 의 slice 와 완전 slice 식 · copy · 배열↔slice 변환, 03-02 문자열은 바이트 · 룬·바이트 변환 · UTF-8 · map · comma ok · delete·clear · 집합, 03-03 struct · 리터럴 · 익명 struct · 비교와 변환, 연습 문제 1~3. 원문 정오 1건(03-03 채널 필드 비교) |
| 4 | [04-01.안쪽 블록의 같은 이름은 바깥 변수를 가립니다](./04-01.%EC%95%88%EC%AA%BD%20%EB%B8%94%EB%A1%9D%EC%9D%98%20%EA%B0%99%EC%9D%80%20%EC%9D%B4%EB%A6%84%EC%9D%80%20%EB%B0%94%EA%B9%A5%20%EB%B3%80%EC%88%98%EB%A5%BC%20%EA%B0%80%EB%A6%BD%EB%8B%88%EB%8B%A4.md), [04-02.for 하나로 네 가지 반복을 씁니다](./04-02.for%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%84%A4%20%EA%B0%80%EC%A7%80%20%EB%B0%98%EB%B3%B5%EC%9D%84%20%EC%94%81%EB%8B%88%EB%8B%A4.md), [04-03.switch 는 기본으로 빠져나가고 break 는 라벨로 고릅니다](./04-03.switch%20%EB%8A%94%20%EA%B8%B0%EB%B3%B8%EC%9C%BC%EB%A1%9C%20%EB%B9%A0%EC%A0%B8%EB%82%98%EA%B0%80%EA%B3%A0%20break%20%EB%8A%94%20%EB%9D%BC%EB%B2%A8%EB%A1%9C%20%EA%B3%A0%EB%A6%85%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 04-01 블록 · universe 블록 · 섀도잉(:= · 패키지 이름 · true) · if 초기화 선언, 04-02 for 네 형태 · break·continue · for-range(map 순서 · 문자열 룬 · 값 사본 · Go 1.22 루프 변수) · 라벨 · 형태 고르기, 04-03 switch · fallthrough · switch 안 break 와 라벨 · 빈 switch · if 대 switch · goto, 연습 문제 1~3. 원문 정오 3건(04-02 오타 둘 · 04-03 채널 비교) |
| 5 | [05-01.Go 함수는 여러 값을 돌려주고 오류는 마지막 값입니다](./05-01.Go%20%ED%95%A8%EC%88%98%EB%8A%94%20%EC%97%AC%EB%9F%AC%20%EA%B0%92%EC%9D%84%20%EB%8F%8C%EB%A0%A4%EC%A3%BC%EA%B3%A0%20%EC%98%A4%EB%A5%98%EB%8A%94%20%EB%A7%88%EC%A7%80%EB%A7%89%20%EA%B0%92%EC%9E%85%EB%8B%88%EB%8B%A4.md), [05-02.함수는 값이고 클로저는 바깥 변수를 붙잡습니다](./05-02.%ED%95%A8%EC%88%98%EB%8A%94%20%EA%B0%92%EC%9D%B4%EA%B3%A0%20%ED%81%B4%EB%A1%9C%EC%A0%80%EB%8A%94%20%EB%B0%94%EA%B9%A5%20%EB%B3%80%EC%88%98%EB%A5%BC%20%EB%B6%99%EC%9E%A1%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [05-03.defer 는 함수가 끝날 때 정리하고 인자는 늘 복사됩니다](./05-03.defer%20%EB%8A%94%20%ED%95%A8%EC%88%98%EA%B0%80%20%EB%81%9D%EB%82%A0%20%EB%95%8C%20%EC%A0%95%EB%A6%AC%ED%95%98%EA%B3%A0%20%EC%9D%B8%EC%9E%90%EB%8A%94%20%EB%8A%98%20%EB%B3%B5%EC%82%AC%EB%90%A9%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 05-01 함수 선언 · struct 로 이름 붙은·선택 인자 · 가변 인자 · 여러 값 반환과 오류 · 이름 붙은 반환 값 · 빈 return, 05-02 함수 값·시그니처 · 계산기 · 함수 타입 · 익명 함수 · 클로저 · sort.Slice · makeMult, 05-03 defer(LIFO · 인자 평가 · 결과 변수 수정 · 정리 클로저) · 값에 의한 호출 · 연습 문제 1~3. 원문 정오 1건(05-03 SQL VALUES 괄호) |
| 6 | [06-01.포인터는 값이 놓인 주소를 담고 객체 변수도 사실 포인터입니다](./06-01.%ED%8F%AC%EC%9D%B8%ED%84%B0%EB%8A%94%20%EA%B0%92%EC%9D%B4%20%EB%86%93%EC%9D%B8%20%EC%A3%BC%EC%86%8C%EB%A5%BC%20%EB%8B%B4%EA%B3%A0%20%EA%B0%9D%EC%B2%B4%20%EB%B3%80%EC%88%98%EB%8F%84%20%EC%82%AC%EC%8B%A4%20%ED%8F%AC%EC%9D%B8%ED%84%B0%EC%9E%85%EB%8B%88%EB%8B%A4.md), [06-02.포인터 매개변수는 바꿔도 된다는 표시이고 slice 는 길이까지 복사됩니다](./06-02.%ED%8F%AC%EC%9D%B8%ED%84%B0%20%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98%EB%8A%94%20%EB%B0%94%EA%BF%94%EB%8F%84%20%EB%90%9C%EB%8B%A4%EB%8A%94%20%ED%91%9C%EC%8B%9C%EC%9D%B4%EA%B3%A0%20slice%20%EB%8A%94%20%EA%B8%B8%EC%9D%B4%EA%B9%8C%EC%A7%80%20%EB%B3%B5%EC%82%AC%EB%90%A9%EB%8B%88%EB%8B%A4.md), [06-03.값을 스택에 두면 가비지가 줄고 GOGC 와 GOMEMLIMIT 가 힙을 조절합니다](./06-03.%EA%B0%92%EC%9D%84%20%EC%8A%A4%ED%83%9D%EC%97%90%20%EB%91%90%EB%A9%B4%20%EA%B0%80%EB%B9%84%EC%A7%80%EA%B0%80%20%EC%A4%84%EA%B3%A0%20GOGC%20%EC%99%80%20GOMEMLIMIT%20%EA%B0%80%20%ED%9E%99%EC%9D%84%20%EC%A1%B0%EC%A0%88%ED%95%A9%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 06-01 주소와 포인터 · nil · & 와 * · new · 상수에 주소 없음과 makePointer · 다른 언어의 객체 변수와 값에 의한 전달, 06-02 포인터 매개변수와 불변성 · nil 포인터 갱신 실패 · 포인터는 마지막 수단(json.Unmarshal) · 전달 성능 · 제로 값과 값 없음 · map 과 slice 헤더 · slice 버퍼, 06-03 가비지 · 스택과 힙 · 탈출 분석 · 기계적 공감과 Java 비교 · GOGC · GOMEMLIMIT, 연습 문제 1~3. 원문 정오 1건(06-02 go test 명령의 말줄임표) |
| 7 | [07-01.메서드는 리시버로 타입에 붙고 포인터 리시버만 원본을 바꿉니다](./07-01.%EB%A9%94%EC%84%9C%EB%93%9C%EB%8A%94%20%EB%A6%AC%EC%8B%9C%EB%B2%84%EB%A1%9C%20%ED%83%80%EC%9E%85%EC%97%90%20%EB%B6%99%EA%B3%A0%20%ED%8F%AC%EC%9D%B8%ED%84%B0%20%EB%A6%AC%EC%8B%9C%EB%B2%84%EB%A7%8C%20%EC%9B%90%EB%B3%B8%EC%9D%84%20%EB%B0%94%EA%BF%89%EB%8B%88%EB%8B%A4.md), [07-02.타입 선언과 임베딩은 상속이 아니라 이름 붙이기와 승격입니다](./07-02.%ED%83%80%EC%9E%85%20%EC%84%A0%EC%96%B8%EA%B3%BC%20%EC%9E%84%EB%B2%A0%EB%94%A9%EC%9D%80%20%EC%83%81%EC%86%8D%EC%9D%B4%20%EC%95%84%EB%8B%88%EB%9D%BC%20%EC%9D%B4%EB%A6%84%20%EB%B6%99%EC%9D%B4%EA%B8%B0%EC%99%80%20%EC%8A%B9%EA%B2%A9%EC%9E%85%EB%8B%88%EB%8B%A4.md), [07-03.인터페이스는 암묵적으로 만족되고 nil 은 타입과 값이 모두 비어야 합니다](./07-03.%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%8A%94%20%EC%95%94%EB%AC%B5%EC%A0%81%EC%9C%BC%EB%A1%9C%20%EB%A7%8C%EC%A1%B1%EB%90%98%EA%B3%A0%20nil%20%EC%9D%80%20%ED%83%80%EC%9E%85%EA%B3%BC%20%EA%B0%92%EC%9D%B4%20%EB%AA%A8%EB%91%90%20%EB%B9%84%EC%96%B4%EC%95%BC%20%ED%95%A9%EB%8B%88%EB%8B%A4.md), [07-04.타입 단언은 아껴 쓰고 암묵 인터페이스로 의존성을 주입합니다](./07-04.%ED%83%80%EC%9E%85%20%EB%8B%A8%EC%96%B8%EC%9D%80%20%EC%95%84%EA%BB%B4%20%EC%93%B0%EA%B3%A0%20%EC%95%94%EB%AC%B5%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%A1%9C%20%EC%9D%98%EC%A1%B4%EC%84%B1%EC%9D%84%20%EC%A3%BC%EC%9E%85%ED%95%A9%EB%8B%88%EB%8B%A4.md) | ✅ 4편: 07-01 사용자 정의 타입 · 메서드와 리시버 · 포인터/값 리시버와 메서드 집합 · nil 리시버 · 메서드 값과 식 · 함수 대 메서드, 07-02 타입 선언은 상속이 아님 · 문서로서의 타입 · iota · 임베딩과 승격 · 동적 디스패치 없음, 07-03 인터페이스와 메서드 집합 · 암묵적 구현과 덕 타이핑 · 데코레이터 · 인터페이스 임베딩 · 인터페이스를 받고 struct 를 돌려주기 · 인터페이스와 nil · 비교와 panic · any, 07-04 타입 단언과 타입 스위치 · 선택적 인터페이스 · 함수 타입 다리(HandlerFunc) · 의존성 주입 웹 앱 · Wire, 연습 문제 1~3. 원문 정오 4건(07-03 func 누락 · io.File, 07-04 copyBuffer 설명의 짝 뒤바뀜 · 여는 중괄호 누락) |
| 8 | [08-01.제네릭은 타입 매개변수로 한 번 쓰고 컴파일 시점에 타입을 검사합니다](./08-01.%EC%A0%9C%EB%84%A4%EB%A6%AD%EC%9D%80%20%ED%83%80%EC%9E%85%20%EB%A7%A4%EA%B0%9C%EB%B3%80%EC%88%98%EB%A1%9C%20%ED%95%9C%20%EB%B2%88%20%EC%93%B0%EA%B3%A0%20%EC%BB%B4%ED%8C%8C%EC%9D%BC%20%EC%8B%9C%EC%A0%90%EC%97%90%20%ED%83%80%EC%9E%85%EC%9D%84%20%EA%B2%80%EC%82%AC%ED%95%A9%EB%8B%88%EB%8B%A4.md), [08-02.타입 요소는 쓸 수 있는 연산자를 정하고 ~ 는 바탕 타입까지 넓힙니다](./08-02.%ED%83%80%EC%9E%85%20%EC%9A%94%EC%86%8C%EB%8A%94%20%EC%93%B8%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%97%B0%EC%82%B0%EC%9E%90%EB%A5%BC%20%EC%A0%95%ED%95%98%EA%B3%A0%20~%20%EB%8A%94%20%EB%B0%94%ED%83%95%20%ED%83%80%EC%9E%85%EA%B9%8C%EC%A7%80%20%EB%84%93%ED%9E%99%EB%8B%88%EB%8B%A4.md), [08-03.Go 제네릭은 일부러 작게 만들었고 성능을 위해 바꿀 도구가 아닙니다](./08-03.Go%20%EC%A0%9C%EB%84%A4%EB%A6%AD%EC%9D%80%20%EC%9D%BC%EB%B6%80%EB%9F%AC%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EC%97%88%EA%B3%A0%20%EC%84%B1%EB%8A%A5%EC%9D%84%20%EC%9C%84%ED%95%B4%20%EB%B0%94%EA%BF%80%20%EB%8F%84%EA%B5%AC%EA%B0%80%20%EC%95%84%EB%8B%99%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 08-01 제네릭이 없을 때의 중복과 실행 중 panic · 타입 매개변수와 제약 · 제로 값 · comparable · Map·Filter·Reduce · 인터페이스 제약(Pair·Differ), 08-02 타입 요소와 ~ · cmp 패키지 · 불가능한 제약 · 타입 추론 · 상수 · 제네릭 트리 · comparable 과 인터페이스 panic, 08-03 빠진 기능(연산자 오버로딩 · 메서드 타입 매개변수) · 관용과 성능 · 바탕 타입별 함수 생성 · 표준 라이브러리 · 합 타입, 연습 문제 1~3. 원문 정오 3건(08-01 OrderableString 단언, 08-02 OrderedFunc · Comparer 주석) |
| 9 | [09-01.Go 오류는 마지막 반환 값이고 센티널과 사용자 정의 타입으로 뜻을 담습니다](./09-01.Go%20%EC%98%A4%EB%A5%98%EB%8A%94%20%EB%A7%88%EC%A7%80%EB%A7%89%20%EB%B0%98%ED%99%98%20%EA%B0%92%EC%9D%B4%EA%B3%A0%20%EC%84%BC%ED%8B%B0%EB%84%90%EA%B3%BC%20%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%A0%95%EC%9D%98%20%ED%83%80%EC%9E%85%EC%9C%BC%EB%A1%9C%20%EB%9C%BB%EC%9D%84%20%EB%8B%B4%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [09-02.오류를 감싸면 트리가 되고 errors.Is 와 As 가 그 안을 찾습니다](./09-02.%EC%98%A4%EB%A5%98%EB%A5%BC%20%EA%B0%90%EC%8B%B8%EB%A9%B4%20%ED%8A%B8%EB%A6%AC%EA%B0%80%20%EB%90%98%EA%B3%A0%20errors.Is%20%EC%99%80%20As%20%EA%B0%80%20%EA%B7%B8%20%EC%95%88%EC%9D%84%20%EC%B0%BE%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [09-03.panic 은 복구할 수 없을 때만 쓰고 recover 는 API 경계에서 씁니다](./09-03.panic%20%EC%9D%80%20%EB%B3%B5%EA%B5%AC%ED%95%A0%20%EC%88%98%20%EC%97%86%EC%9D%84%20%EB%95%8C%EB%A7%8C%20%EC%93%B0%EA%B3%A0%20recover%20%EB%8A%94%20API%20%EA%B2%BD%EA%B3%84%EC%97%90%EC%84%9C%20%EC%94%81%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 09-01 오류 반환의 기본과 예외를 쓰지 않는 이유 · errors.New·fmt.Errorf · 센티널 오류와 상수 센티널 · 사용자 정의 오류 타입과 nil 함정, 09-02 %w 감싸기와 Unwrap · %v · errors.Join·여러 %w · Unwrap() []error · errors.Is·As 와 사용자 정의 Is · defer 감싸기, 09-03 panic 과 defer 사슬 · recover · panic(nil) · recover 를 쓰는 경계 · 스택 트레이스와 -trimpath, 연습 문제 1~3. 원문 정오 1건(09-02 MyError 의 type 리시버) |
| 10 | [10-01.모듈은 go.mod 로 한 단위가 되고 go 지시어가 빌드할 Go 버전을 정합니다](./10-01.%EB%AA%A8%EB%93%88%EC%9D%80%20go.mod%20%EB%A1%9C%20%ED%95%9C%20%EB%8B%A8%EC%9C%84%EA%B0%80%20%EB%90%98%EA%B3%A0%20go%20%EC%A7%80%EC%8B%9C%EC%96%B4%EA%B0%80%20%EB%B9%8C%EB%93%9C%ED%95%A0%20Go%20%EB%B2%84%EC%A0%84%EC%9D%84%20%EC%A0%95%ED%95%A9%EB%8B%88%EB%8B%A4.md), [10-02.패키지는 대문자로 내보내고 이름으로 기능을 말하며 internal 로 감춥니다](./10-02.%ED%8C%A8%ED%82%A4%EC%A7%80%EB%8A%94%20%EB%8C%80%EB%AC%B8%EC%9E%90%EB%A1%9C%20%EB%82%B4%EB%B3%B4%EB%82%B4%EA%B3%A0%20%EC%9D%B4%EB%A6%84%EC%9C%BC%EB%A1%9C%20%EA%B8%B0%EB%8A%A5%EC%9D%84%20%EB%A7%90%ED%95%98%EB%A9%B0%20internal%20%EB%A1%9C%20%EA%B0%90%EC%B6%A5%EB%8B%88%EB%8B%A4.md), [10-03.서드파티 모듈은 go get 으로 들이고 최소 버전 선택으로 버전을 고릅니다](./10-03.%EC%84%9C%EB%93%9C%ED%8C%8C%ED%8B%B0%20%EB%AA%A8%EB%93%88%EC%9D%80%20go%20get%20%EC%9C%BC%EB%A1%9C%20%EB%93%A4%EC%9D%B4%EA%B3%A0%20%EC%B5%9C%EC%86%8C%20%EB%B2%84%EC%A0%84%20%EC%84%A0%ED%83%9D%EC%9C%BC%EB%A1%9C%20%EB%B2%84%EC%A0%84%EC%9D%84%20%EA%B3%A0%EB%A6%85%EB%8B%88%EB%8B%A4.md), [10-04.모듈은 태그로 게시하고 워크스페이스와 프록시로 다룹니다](./10-04.%EB%AA%A8%EB%93%88%EC%9D%80%20%ED%83%9C%EA%B7%B8%EB%A1%9C%20%EA%B2%8C%EC%8B%9C%ED%95%98%EA%B3%A0%20%EC%9B%8C%ED%81%AC%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%EB%8B%A4%EB%A3%B9%EB%8B%88%EB%8B%A4.md) | ✅ 4편: 10-01 저장소·모듈·패키지 · 모듈 경로 · go.mod · go 지시어와 toolchain·GOTOOLCHAIN · require, 10-02 대문자 내보내기 · import 경로와 패키지 이름 · 이름 짓기와 바꾸기 · Go Doc 주석 · internal · 순환 의존 · 모듈 정리 · 타입 별칭 · init, 10-03 go get 과 go.sum · pseudo-version · go mod tidy · 버전 내리기 · SemVer · 최소 버전 선택 · -u=patch·-u · /v2 import 경로 · 벤더링 · pkg.go.dev, 10-04 게시와 라이선스 · 프리릴리스 · 메이저 버전 올리기 · replace·exclude·retract · 워크스페이스 · 프록시와 체크섬 DB · GOPRIVATE, 연습 문제 1~3. 원문 정오 5건(10-01 %p 출력의 0x · toolchain 지시어 값과 local 의 뜻, 10-02 internal 범위, 10-03 go get 출력의 pseudo-version, 10-04 retract v.1.8.5) |
| 11 | [11-01.go run 은 임시로 빌드해 바로 실행하고 go install 은 @버전으로 도구를 설치합니다](./11-01.go%20run%20%EC%9D%80%20%EC%9E%84%EC%8B%9C%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%B4%20%EB%B0%94%EB%A1%9C%20%EC%8B%A4%ED%96%89%ED%95%98%EA%B3%A0%20go%20install%20%EC%9D%80%20%40%EB%B2%84%EC%A0%84%EC%9C%BC%EB%A1%9C%20%EB%8F%84%EA%B5%AC%EB%A5%BC%20%EC%84%A4%EC%B9%98%ED%95%A9%EB%8B%88%EB%8B%A4.md), [11-02.린터는 믿되 확인하며 쓰고 govulncheck 는 실제로 부르는 취약 코드를 짚습니다](./11-02.%EB%A6%B0%ED%84%B0%EB%8A%94%20%EB%AF%BF%EB%90%98%20%ED%99%95%EC%9D%B8%ED%95%98%EB%A9%B0%20%EC%93%B0%EA%B3%A0%20govulncheck%20%EB%8A%94%20%EC%8B%A4%EC%A0%9C%EB%A1%9C%20%EB%B6%80%EB%A5%B4%EB%8A%94%20%EC%B7%A8%EC%95%BD%20%EC%BD%94%EB%93%9C%EB%A5%BC%20%EC%A7%9A%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [11-03.embed 지시어는 파일을 바이너리에 넣고 go generate 는 코드를 만들어 냅니다](./11-03.embed%20%EC%A7%80%EC%8B%9C%EC%96%B4%EB%8A%94%20%ED%8C%8C%EC%9D%BC%EC%9D%84%20%EB%B0%94%EC%9D%B4%EB%84%88%EB%A6%AC%EC%97%90%20%EB%84%A3%EA%B3%A0%20go%20generate%20%EB%8A%94%20%EC%BD%94%EB%93%9C%EB%A5%BC%20%EB%A7%8C%EB%93%A4%EC%96%B4%20%EB%83%85%EB%8B%88%EB%8B%A4.md), [11-04.Go 바이너리는 빌드 정보를 품고 GOOS·GOARCH 와 빌드 태그로 대상을 가립니다](./11-04.Go%20%EB%B0%94%EC%9D%B4%EB%84%88%EB%A6%AC%EB%8A%94%20%EB%B9%8C%EB%93%9C%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%ED%92%88%EA%B3%A0%20GOOS%C2%B7GOARCH%20%EC%99%80%20%EB%B9%8C%EB%93%9C%20%ED%83%9C%EA%B7%B8%EB%A1%9C%20%EB%8C%80%EC%83%81%EC%9D%84%20%EA%B0%80%EB%A6%BD%EB%8B%88%EB%8B%A4.md) | ✅ 4편: 11-01 go run 과 임시 디렉터리 · go install 과 @버전 · GOBIN·GOROOT·GOPATH · hey · goimports · golang.org/x, 11-02 린터와 무시 주석 · staticcheck(S1039·SA4006) · revive · golangci-lint 와 .golangci.yml(v2 형식 보충) · 도입 순서 · govulncheck, 11-03 go:embed 와 embed.FS · 패턴 오류 · 숨김 파일(dir/* · all:) · go generate 와 protobuf · stringer · 생성 코드 커밋과 Makefile, 11-04 빌드 정보와 go version -m · govulncheck -mode binary · GOOS·GOARCH 교차 컴파일 · 파일 이름 접미사와 //go:build · 사용자 정의 태그 · golang.org/dl · go help, 연습 문제 1~3. 원문 정오 3건(11-03 비밀번호 1만 개 · string_demo, 11-04 ~/sdk/go.19.2). 편마다 학습 목표 뒤 키워드 개념도 |
| 12 | [12-01.고루틴은 런타임이 나눠 돌리는 가벼운 스레드이고 채널로 값을 주고받습니다](./12-01.%EA%B3%A0%EB%A3%A8%ED%8B%B4%EC%9D%80%20%EB%9F%B0%ED%83%80%EC%9E%84%EC%9D%B4%20%EB%82%98%EB%88%A0%20%EB%8F%8C%EB%A6%AC%EB%8A%94%20%EA%B0%80%EB%B2%BC%EC%9A%B4%20%EC%8A%A4%EB%A0%88%EB%93%9C%EC%9D%B4%EA%B3%A0%20%EC%B1%84%EB%84%90%EB%A1%9C%20%EA%B0%92%EC%9D%84%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [12-02.select 는 준비된 case 를 무작위로 고르고 고루틴은 반드시 끝나게 만듭니다](./12-02.select%20%EB%8A%94%20%EC%A4%80%EB%B9%84%EB%90%9C%20case%20%EB%A5%BC%20%EB%AC%B4%EC%9E%91%EC%9C%84%EB%A1%9C%20%EA%B3%A0%EB%A5%B4%EA%B3%A0%20%EA%B3%A0%EB%A3%A8%ED%8B%B4%EC%9D%80%20%EB%B0%98%EB%93%9C%EC%8B%9C%20%EB%81%9D%EB%82%98%EA%B2%8C%20%EB%A7%8C%EB%93%AD%EB%8B%88%EB%8B%A4.md), [12-03.버퍼 채널은 개수를 알 때 쓰고 WaitGroup 과 Once 가 기다림과 한 번 실행을 맡습니다](./12-03.%EB%B2%84%ED%8D%BC%20%EC%B1%84%EB%84%90%EC%9D%80%20%EA%B0%9C%EC%88%98%EB%A5%BC%20%EC%95%8C%20%EB%95%8C%20%EC%93%B0%EA%B3%A0%20WaitGroup%20%EA%B3%BC%20Once%20%EA%B0%80%20%EA%B8%B0%EB%8B%A4%EB%A6%BC%EA%B3%BC%20%ED%95%9C%20%EB%B2%88%20%EC%8B%A4%ED%96%89%EC%9D%84%20%EB%A7%A1%EC%8A%B5%EB%8B%88%EB%8B%A4.md), [12-04.채널로 파이프라인을 짜고 공유 필드는 뮤텍스로 지킵니다](./12-04.%EC%B1%84%EB%84%90%EB%A1%9C%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EC%9D%84%20%EC%A7%9C%EA%B3%A0%20%EA%B3%B5%EC%9C%A0%20%ED%95%84%EB%93%9C%EB%8A%94%20%EB%AE%A4%ED%85%8D%EC%8A%A4%EB%A1%9C%20%EC%A7%80%ED%82%B5%EB%8B%88%EB%8B%A4.md) | ✅ 4편: 12-01 동시성을 쓸 때 · 고루틴과 스케줄러 · 채널 읽기·쓰기·방향 · 버퍼 · for-range · close 와 comma ok · 채널 상태표, 12-02 select 와 기아·교착 · for-select 와 default · API 에서 동시성 감추기 · Go 1.22 루프 변수 · 고루틴 누수와 context 취소, 12-03 버퍼 채널 · 백프레셔 · nil 채널로 case 끄기 · 시간 제한 · WaitGroup 과 한 번만 닫기 · errgroup · WaitGroup.Go · Once·OnceValue, 12-04 세 서비스 파이프라인 · 뮤텍스 대 채널 · RWMutex · 재진입 없음 · sync.Map · atomic, 연습 문제 1~3. 원문 정오 4건(12-02 when every value is read, 12-03 to this goroutine · a function to run · is read to) |
| 13 | [13-01.io.Reader 는 버퍼를 받아 채우고 작은 인터페이스를 겹쳐 기능을 더합니다](./13-01.io.Reader%20%EB%8A%94%20%EB%B2%84%ED%8D%BC%EB%A5%BC%20%EB%B0%9B%EC%95%84%20%EC%B1%84%EC%9A%B0%EA%B3%A0%20%EC%9E%91%EC%9D%80%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%A5%BC%20%EA%B2%B9%EC%B3%90%20%EA%B8%B0%EB%8A%A5%EC%9D%84%20%EB%8D%94%ED%95%A9%EB%8B%88%EB%8B%A4.md), [13-02.time 은 Duration 과 Time 두 타입이고 형식은 2006년 1월 2일 기준 시각으로 씁니다](./13-02.time%20%EC%9D%80%20Duration%20%EA%B3%BC%20Time%20%EB%91%90%20%ED%83%80%EC%9E%85%EC%9D%B4%EA%B3%A0%20%ED%98%95%EC%8B%9D%EC%9D%80%202006%EB%85%84%201%EC%9B%94%202%EC%9D%BC%20%EA%B8%B0%EC%A4%80%20%EC%8B%9C%EA%B0%81%EC%9C%BC%EB%A1%9C%20%EC%94%81%EB%8B%88%EB%8B%A4.md), [13-03.encoding-json 은 구조체 태그로 이름을 정하고 Decoder 와 Encoder 로 스트림을 다룹니다](./13-03.encoding-json%20%EC%9D%80%20%EA%B5%AC%EC%A1%B0%EC%B2%B4%20%ED%83%9C%EA%B7%B8%EB%A1%9C%20%EC%9D%B4%EB%A6%84%EC%9D%84%20%EC%A0%95%ED%95%98%EA%B3%A0%20Decoder%20%EC%99%80%20Encoder%20%EB%A1%9C%20%EC%8A%A4%ED%8A%B8%EB%A6%BC%EC%9D%84%20%EB%8B%A4%EB%A3%B9%EB%8B%88%EB%8B%A4.md), [13-04.net-http 는 타임아웃을 직접 정하고 미들웨어는 Handler 를 감싸며 slog 로 구조화 로그를 남깁니다](./13-04.net-http%20%EB%8A%94%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%84%20%EC%A7%81%EC%A0%91%20%EC%A0%95%ED%95%98%EA%B3%A0%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20Handler%20%EB%A5%BC%20%EA%B0%90%EC%8B%B8%EB%A9%B0%20slog%20%EB%A1%9C%20%EA%B5%AC%EC%A1%B0%ED%99%94%20%EB%A1%9C%EA%B7%B8%EB%A5%BC%20%EB%82%A8%EA%B9%81%EB%8B%88%EB%8B%A4.md) | ✅ 4편: 13-01 io.Reader·Writer 와 버퍼 재사용 · io.EOF · gzip 데코레이터 · io 도우미 · Closer·Seeker 와 조합 인터페이스 · NopCloser · os 파일 함수, 13-02 Duration · Time 과 Equal · 기준 시각 형식 · 단조 시계 · 타이머와 Ticker(Go 1.23 회수 보충), 13-03 구조체 태그 · omitempty 와 omitzero · Marshal·Unmarshal · Decoder·Encoder 와 스트림 · 사용자 정의 파싱과 Dup · gob, 13-04 Client 타임아웃 · Server 와 ServeMux · Go 1.22 패턴과 go 지시어 · 미들웨어 · ResponseController · slog, 연습 문제 1~3. 원문 정오 2건(13-04 Headers 필드 · NewJSONHandler 메서드) |
| 14~16 | — | ◻ |



## 노트 작성 규칙

> 파일명·어체·검증 기준은 형제 정독 폴더(`jpf_`·`tsj_`)와 같습니다.

파일명은 `{장 번호}-{편 순번}.{제목}.md` 형식입니다. 앞 번호는 책의 장 번호이고 뒤 번호는 그 장을 쪼갠 편의 순번이며, 제목은 그 편이 푸는 문제가 드러나게 짓습니다. 도식 SVG 는 `_assets/{장-편}.{슬러그}.svg` 에 둡니다.

본문은 합니다체로 쓰고, Spring 위에서 Java 를 써 온 개발자가 Go 를 처음 배우는 관점에서 차이가 나는 자리를 짚습니다. 예를 들어 zero value 는 Java 필드가 `null`·`0` 으로 초기화되는 규칙과, 인터페이스의 암묵 구현은 `implements` 선언과 나란히 놓으면 무엇이 달라졌는지 바로 보입니다.

코드·명령·수치·인용은 원문과 한 글자도 다르지 않게 옮깁니다. 책의 예제 코드는 로컬 Go(`go1.25.1 darwin/arm64`)에서 실행해 결과를 확인한 뒤 노트에 싣습니다. 책이 설명한 동작이 현재 Go 버전에서 달라졌다면 원문을 고치지 않고 그 차이를 따로 적습니다.



## 학습 상태

> 노트 작성과 학습자의 이해 확인은 따로 셉니다. 지금은 노트만 있고 학습 세션은 아직 돌지 않았습니다.

| 항목 | 값 |
|---|---|
| 난이도 레벨 | 입문 — Go 를 처음 제대로 배우는 단계입니다 |
| 막힌 지점 | 아직 없음 — Phase 4 자답 전입니다 |
| 다음 레슨 후보 | 1~13장 학습 세션, 이어서 14장 노트 작성 |
| 최근 검증 결과 | 없음 |
| 복습 회차 | 없음 |
