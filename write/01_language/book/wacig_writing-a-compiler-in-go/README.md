---
title: Writing A Compiler In Go — 정독 인덱스
tags: [moc, study-index, book, writing-a-compiler-in-go, compiler, bytecode, virtual-machine, symbol-table, go]
status: draft
source:
  - 《Writing A Compiler In Go》 (Thorsten Ball) — 판 1.2 (2019-05-07, 책 뒤 Changelog 기준) · PDF 284쪽 · 본문 10장
  - 원본 PDF — GoogleDrive/내 드라이브/book/Writing A Compiler In Go/ (2026-11-11 추가, 같은 파일이 book/Writing A Compiler In Go.pdf 에도 있음, cmp 일치)
  - 책 사이트 — https://compilerbook.com
related:
  - ../waiig_writing-an-interpreter-in-go/README.md
  - ../ci_crafting-interpreters/README.md
  - ../../README.md
  - ../../go-keywords.md
updated: 2026-11-11
---

# Writing A Compiler In Go — 정독 인덱스

---

> 이 폴더는 Thorsten Ball 의 『Writing A Compiler In Go』를 장 단위로 정독하며 정리하는 책 종속 학습 노트입니다. 앞 권에서 만든 Monkey 인터프리터의 평가기를 바이트코드 컴파일러와 스택 기반 가상 머신으로 바꿉니다.

## 이 책을 읽는 이유

> 트리를 실행 중에 해석하던 프로그램이, 실행 전에 트리를 분석해 다른 형태의 코드를 내도록 바뀌는 과정을 Go 로 따라가려고 읽습니다.

실행 시점 DI 와 컴파일 시점 DI 의 차이는 연결을 실행 중에 해석하느냐, 실행 전에 분석해 코드로 내 두느냐에 있습니다. 동기 전체는 [Crafting Interpreters 인덱스](../ci_crafting-interpreters/README.md)의 「이 책을 읽는 이유」에 적었습니다. 이 책은 같은 언어를 두고 바로 그 전환을 합니다. [앞 권](../waiig_writing-an-interpreter-in-go/README.md)의 렉서·파서·AST 는 그대로 두고, 트리를 걷던 평가기 자리에 바이트코드를 내는 컴파일러와 그것을 실행하는 VM 을 넣습니다.

DI 목표와 가장 가까운 곳은 5장 「Keeping Track of Names」입니다. 컴파일러가 이름을 만날 때마다 어디에 정의됐는지 기억해 두는 심볼 테이블(5장 「Introducing: the Symbol Table」, 114쪽)을 만듭니다. 9장은 클로저가 쓰는 자유 변수를 컴파일 시점에 찾아 묶습니다(「Compiling and resolving free variables」, 246쪽). 이름과 정의를 실행 전에 이어 두는 일이라, DI 생성기가 생성자 매개변수를 제공자에 잇는 일과 견줄 수 있습니다. 이 대응은 노트의 해석이고, 어디까지 맞는지는 노트를 쓰며 확인합니다.



## 원문과 판

> 책 뒤 Changelog 의 마지막 항목인 1.2 판(2019-05-07)을 정본으로 삼습니다. 앞 권을 먼저 읽었다고 전제하는 책입니다.

서문에 따르면 적어도 Go 1.10 이 필요합니다. 1.2 판은 코드 폴더에 `go.mod` 를 넣어 Go 1.13 이상에서는 `$GOPATH` 없이 돌릴 수 있게 했습니다. 책의 코드는 서문에 적힌 `wacig_code_1.2.zip` 으로 배포됩니다.

서문 「Evolving Monkey」는 앞 권에서 만든 것을 다시 정리합니다. 문자열에서 토큰으로, 토큰에서 트리로, 트리에서 평가 결과로 이어지는 변환 사슬입니다. 이 책은 그 사슬의 마지막 고리를 바꿉니다. 그래서 앞 권의 1~2장(렉서·파서)은 이 책의 전제이고, 3장(평가기)은 이 책이 대체하는 대상입니다.

유료 책이므로 노트는 원문 문단을 길게 옮기지 않고, 짧게 인용할 때는 장·절 제목과 쪽수로 출처를 밝힙니다.



## 장 구성

> 본문 10장, 책 쪽 10–276 이 대상입니다. 1장이 컴파일러와 VM 의 관계를 설명하고, 2장부터 기능을 하나씩 바이트코드로 옮깁니다.

| 장 | 제목 | 쪽 | 무엇을 만드나 |
|----|------|----|-------------|
| 1 | Compilers & Virtual Machines | 10–25 | 컴파일러, 실제 기계와 가상 기계, 바이트코드, VM 과 컴파일러의 짝 |
| 2 | Hello Bytecode! | 26–56 | 첫 명령어, 가장 작은 컴파일러, 역어셈블러, 스택에 더하기, REPL 연결 |
| 3 | Compiling Expressions | 57–81 | 스택 정리, 중위·전위 식, 불리언, 비교 연산자 |
| 4 | Conditionals | 82–109 | 점프 명령, 조건문 컴파일과 실행, null |
| 5 | Keeping Track of Names | 110–124 | 바인딩 컴파일, 심볼 테이블, VM 의 전역 변수 |
| 6 | String, Array and Hash | 125–145 | 문자열·배열·해시, 인덱스 연산자 |
| 7 | Functions | 146–215 | 함수 표현과 호출 opcode, 지역 바인딩, 인자 |
| 8 | Built-in Functions | 216–232 | 내장 함수를 위한 새 스코프 |
| 9 | Closures | 233–272 | 모든 함수를 클로저로, 자유 변수 컴파일과 해석, 재귀 클로저 |
| 10 | Taking Time | 273–276 | 인터프리터와 컴파일러·VM 의 실행 시간 비교 |

쪽 범위는 목차의 장 시작 쪽에서 계산했습니다. 단어 수는 PDF 전체를 `pdftotext -layout` 으로 뽑아 `wc -w` 로 센 값이 82,602 이며, 코드가 많이 섞여 있습니다. 7장이 70쪽으로 가장 길어 여러 편으로 나눠야 할 가능성이 큽니다.



## 장 ↔ 정독 노트

> 아직 쓴 노트가 없습니다. 장을 시작할 때 분량을 보고 편 수를 정합니다.

진척 컬럼은 ⏳ 진행 중, ✅ 완료, ◻ 미착수입니다.

| 장 | 절 | 노트 | 진척 |
|----|----|------|------|
| 1 | Compilers · Virtual and Real Machines · What We're Going to Do, or: the Duality of VM and Compiler | — | ◻ |
| 2 | First Instructions · Adding on the Stack · Hooking up the REPL | — | ◻ |
| 3 | Cleaning Up the Stack · Infix Expressions · Booleans · Comparison Operators · Prefix Expressions | — | ◻ |
| 4 | Jumps · Compiling Conditionals · Executing Jumps · Welcome Back, Null! | — | ◻ |
| 5 | The Plan · Compiling Bindings · Introducing: the Symbol Table · Using Symbols in the Compiler · Adding Globals to the VM | — | ◻ |
| 6 | String · Array · Hash · Adding the index operator | — | ◻ |
| 7 | Dipping Our Toes: a Simple Function · Local Bindings · Arguments | — | ◻ |
| 8 | Making the Change Easy · Making the Change: the Plan · A New Scope for Built-in Functions · Executing built-in functions | — | ◻ |
| 9 | The Problem · The Plan · Everything's a closure · Compiling and resolving free variables · Creating real closures at run time · Recursive Closures | — | ◻ |
| 10 | Taking Time | — | ◻ |



## 이웃 책과 나눠 읽기

> Crafting Interpreters 3부와 범위가 겹칩니다. 이 책은 Go 로 따라 짜는 실습 쪽, Crafting Interpreters 3부는 C 로 메모리 표현과 GC 까지 내려가는 쪽입니다.

두 책 모두 트리를 걷는 인터프리터 다음에 바이트코드 컴파일러와 스택 VM 을 만듭니다. 이 책은 Go 의 GC 위에서 짜므로 객체의 메모리 표현이나 GC 를 직접 만들지 않습니다. Crafting Interpreters 3부는 C 로 짜면서 해시 테이블(20장)과 GC(26장)까지 직접 만듭니다. DI 목표에는 이 책의 5장과 9장이 더 가깝고, 런타임 내부를 보고 싶을 때 Crafting Interpreters 3부로 갑니다.

같은 개념을 두 번 정리하지 않도록, 한 개념의 정본 노트는 한 곳에 두고 다른 쪽은 링크로 넘깁니다.



## 작성 규칙

> 이 폴더의 노트를 쓸 때 지키는 규칙입니다. 원본 PDF 가 1차 자료라는 것이 그 중심입니다.

- 파일명은 `{장}-{편}.{제목}.md` 입니다. 앞 번호는 원서의 장 번호(1~10), 뒤 번호는 그 장을 여러 편으로 나눈 순번입니다.
- 본문은 합니다체로 씁니다. 문단형 설명을 우선하고, 주장마다 왜 그런지를 함께 적습니다.
- 사실은 `pdftotext` 로 추출한 본문에서 가져오고 장·절 제목과 쪽수로 출처를 밝힙니다.
- 실습 코드는 `write/` 밖의 별도 저장소에 두고, 앞 권 실습 코드를 이어 씁니다. 노트에는 저장소 이름과 경로만 적습니다.
- 도식은 `_assets/` 에 두고, 생성기 선언을 원본으로 삼아 SVG 를 손으로 고치지 않습니다.



## 관련 문서

- [Writing An Interpreter In Go 정독 인덱스](../waiig_writing-an-interpreter-in-go/README.md) — 이 책의 전제인 렉서·파서·AST 와, 이 책이 대체하는 평가기
- [Crafting Interpreters 정독 인덱스](../ci_crafting-interpreters/README.md) — 같은 전환을 C 로, 메모리 표현과 GC 까지
- [Go 로드맵](../../go-keywords.md) — 「로드맵에 넣지 않은 것」의 컴파일러 축
- [01_language MOC](../../README.md)



## 참고 자료

- Thorsten Ball, 『Writing A Compiler In Go』 1.2 판 — https://compilerbook.com
