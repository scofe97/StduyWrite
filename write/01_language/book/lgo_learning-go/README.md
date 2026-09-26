---
title: Learning Go 2판 — 정독 인덱스
tags: [moc, study-index, book, go, golang, language]
status: draft
source:
  - 《Learning Go, 2nd Edition》(Jon Bodner, O'Reilly) — 본문 16장, 장별 PDF 16개 · 약 138,000단어(pdftotext 추출 기준)
  - 원본 PDF — GoogleDrive/내 드라이브/book/Learning Go, 2nd Edition/
related:
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
  next_lesson: "1~3장 학습 세션(설명 → 회상 → 실습) — 노트는 작성됨. 이어서 4장 노트 작성"
updated: 2026-09-27
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

> 1~3장 노트 여섯 편을 썼습니다. 한 세션에 한 장씩 이어서 씁니다.

진척 표시는 ◻ 미착수, ⏳ 진행 중, ✅ 완료입니다. 한 장을 몇 편으로 나눌지는 그 장 원문을 읽은 뒤 분할안을 먼저 정하고, 빈 노트를 미리 만들어 두지 않습니다.

| 장 | 노트 | 진척 |
|:--:|------|:--:|
| 1 | [01-01.go 명령 하나로 만들고 다듬고 검사합니다](./01-01.go%20%EB%AA%85%EB%A0%B9%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%8B%A4%EB%93%AC%EA%B3%A0%20%EA%B2%80%EC%82%AC%ED%95%A9%EB%8B%88%EB%8B%A4.md) | ✅ 설치와 단일 바이너리 · go.mod · go build · go fmt 와 세미콜론 자동 삽입 · go vet · Makefile · 편집기와 Playground · 호환성 약속, 연습 문제 1~3 |
| 2 | [02-01.타입은 자동으로 섞이지 않고 리터럴만 유연합니다](./02-01.%ED%83%80%EC%9E%85%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%EC%84%9E%EC%9D%B4%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%EB%A6%AC%ED%84%B0%EB%9F%B4%EB%A7%8C%20%EC%9C%A0%EC%97%B0%ED%95%A9%EB%8B%88%EB%8B%A4.md), [02-02.var 와 짧은 선언은 의도를 드러내는 선택입니다](./02-02.var%20%EC%99%80%20%EC%A7%A7%EC%9D%80%20%EC%84%A0%EC%96%B8%EC%9D%80%20%EC%9D%98%EB%8F%84%EB%A5%BC%20%EB%93%9C%EB%9F%AC%EB%82%B4%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%9E%85%EB%8B%88%EB%8B%A4.md) | ✅ 2편: 02-01 제로 값 · 리터럴 · 정수·부동소수점·복소수 · 문자열과 rune · 명시적 변환과 truthy 없음 · 타입 없는 리터럴, 02-02 var 와 := · const · 타입 있는/없는 상수 · 쓰지 않는 변수 · 이름 짓기, 연습 문제 1~3 |
| 3 | [03-01.slice 는 배열을 나눠 쓰는 창입니다](./03-01.slice%20%EB%8A%94%20%EB%B0%B0%EC%97%B4%EC%9D%84%20%EB%82%98%EB%88%A0%20%EC%93%B0%EB%8A%94%20%EC%B0%BD%EC%9E%85%EB%8B%88%EB%8B%A4.md), [03-02.문자열은 바이트이고 map 은 없는 키에 제로 값을 돌려줍니다](./03-02.%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%80%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EC%9D%B4%EA%B3%A0%20map%20%EC%9D%80%20%EC%97%86%EB%8A%94%20%ED%82%A4%EC%97%90%20%EC%A0%9C%EB%A1%9C%20%EA%B0%92%EC%9D%84%20%EB%8F%8C%EB%A0%A4%EC%A4%8D%EB%8B%88%EB%8B%A4.md), [03-03.struct 는 타입이 다른 값을 이름으로 묶습니다](./03-03.struct%20%EB%8A%94%20%ED%83%80%EC%9E%85%EC%9D%B4%20%EB%8B%A4%EB%A5%B8%20%EA%B0%92%EC%9D%84%20%EC%9D%B4%EB%A6%84%EC%9C%BC%EB%A1%9C%20%EB%AC%B6%EC%8A%B5%EB%8B%88%EB%8B%A4.md) | ✅ 3편: 03-01 배열 · slice · append 와 용량 증가 · make · slice 의 slice 와 완전 slice 식 · copy · 배열↔slice 변환, 03-02 문자열은 바이트 · 룬·바이트 변환 · UTF-8 · map · comma ok · delete·clear · 집합, 03-03 struct · 리터럴 · 익명 struct · 비교와 변환, 연습 문제 1~3 |
| 4~16 | — | ◻ |



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
| 다음 레슨 후보 | 1~3장 학습 세션, 이어서 4장 노트 작성 |
| 최근 검증 결과 | 없음 |
| 복습 회차 | 없음 |
