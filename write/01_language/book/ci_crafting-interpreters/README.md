---
title: Crafting Interpreters — 정독 인덱스
tags: [moc, study-index, book, crafting-interpreters, interpreter, compiler, ast, code-generation]
status: draft
source:
  - 《Crafting Interpreters》 (Robert Nystrom, © 2015–2021) — 본문 3부 30장 · 부록 2편
  - 웹판 전문(무료) — https://craftinginterpreters.com/contents.html (2026-11-11 목차 확인)
  - 원 저장소 — https://github.com/munificent/craftinginterpreters (LICENSE 2026-11-11 확인)
related:
  - ../sicp_structure-and-interpretation-of-computer-programs/README.md
  - ../lgo_learning-go/README.md
  - ../waiig_writing-an-interpreter-in-go/README.md
  - ../wacig_writing-a-compiler-in-go/README.md
  - ../../README.md
  - ../../go-keywords.md
updated: 2026-11-11
---

# Crafting Interpreters — 정독 인덱스

---

> 이 폴더는 Robert Nystrom 의 『Crafting Interpreters』를 장 단위로 정독하며 정리하는 책 종속 학습 노트입니다. 책은 Lox 라는 작은 스크립트 언어를 Java 로 구문 트리를 걷는 인터프리터와 C 로 짠 바이트코드 가상 머신, 두 방식으로 구현합니다.

## 이 책을 읽는 이유

> DI(의존성 주입)를 실행 시점에 하는 방식과 컴파일 시점에 하는 방식이 어디서 갈리는지 설명하고 싶어서 읽습니다. 그 갈림은 프로그램을 데이터로 읽고 분석해 다시 코드로 내는 일에 있고, 이 책이 그 부품을 직접 만들게 합니다.

Spring 은 주로 실행 중에 리플렉션으로 빈을 찾아 연결합니다. Go 의 Wire 는 반대로 실행 전에 연결 코드를 생성해 둡니다. Wire README 는 자신을 코드 생성 도구(code generation tool)라고 소개하고, 실행 시점 상태나 리플렉션 없이 동작한다고 적습니다.

두 방식의 대비는 [Learning Go 07-04 「Wire 는 연결 코드를 생성합니다」](../lgo_learning-go/07-04.%ED%83%80%EC%9E%85%20%EB%8B%A8%EC%96%B8%EC%9D%80%20%EC%95%84%EA%BB%B4%20%EC%93%B0%EA%B3%A0%20%EC%95%94%EB%AC%B5%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%A1%9C%20%EC%9D%98%EC%A1%B4%EC%84%B1%EC%9D%84%20%EC%A3%BC%EC%9E%85%ED%95%A9%EB%8B%88%EB%8B%A4.md#wire-%EB%8A%94-%EC%97%B0%EA%B2%B0-%EC%BD%94%EB%93%9C%EB%A5%BC-%EC%83%9D%EC%84%B1%ED%95%A9%EB%8B%88%EB%8B%A4) 에서 한 문단으로 짚었습니다. 하지만 "컴파일 전에 코드를 만든다"는 말만으로는 생성기가 소스를 어떻게 읽고 무엇을 분석해 어떤 코드를 내는지 보이지 않습니다.

이 책은 그 단계를 처음부터 손으로 짜게 합니다. 2장은 언어 구현을 스캐닝·파싱·정적 분석·중간 표현·최적화·코드 생성 순으로 나눠 보여 줍니다. 정적 분석의 첫 일로는 이름마다 선언된 곳을 찾아 둘을 잇는 binding(resolution)을 듭니다.

5장은 구문 트리 클래스 21개를 손으로 쓰지 않고, 트리 이름과 필드 목록을 받아 Java 코드를 출력하는 작은 스크립트로 생성합니다. 11장은 실행하기 전에 트리를 한 번 훑어 변수를 선언에 묶는 resolver 를 만듭니다. 소스를 읽고 관계를 분석해 코드를 출력하는 생성기의 일을 장난감 크기로 한 번씩 거치는 셈입니다.

Wire 저장소는 지금 보관(archived) 상태이고, README 첫머리에 더는 유지보수하지 않는다고 적혀 있습니다(GitHub API `archived: true`, 마지막 push 2025-08-22, 2026-11-11 확인). 그래서 Wire 는 도구로 익힐 대상이 아니라 컴파일 시점 DI 의 구조를 보여 주는 사례로 봅니다.



## 이 책을 여기 두는 이유

> 언어 하나를 가르치는 책이 아니라 언어를 만드는 책입니다. 같은 성격의 SICP 가 이미 `01_language/book/` 에 있어 그 옆에 둡니다.

`02_os/` 는 README 에서 범위를 "언어가 아닌 실행 환경(OS·커널)"으로 정해 두었으니 이 책과 맞지 않습니다. `01_language/` 의 범위인 "언어별 문법·관용구·표준 라이브러리·빌드 도구"와도 엄밀히는 어긋납니다. 그래도 [SICP 정독 인덱스](../sicp_structure-and-interpretation-of-computer-programs/README.md)가 같은 이유로 여기에 놓였고, CS 교재가 더 쌓이면 그때 분할한다고 적어 두었습니다. 이 책도 그 결정을 따릅니다.

이웃 폴더와는 보는 쪽이 다릅니다. SICP 4장은 평가기를 직접 짜지만 프로그램 텍스트를 트리로 바꾸는 일은 책이 준 `parse` 함수에 맡깁니다. 이 책은 그 앞 단계인 스캐너와 파서부터 짭니다. [Learning Go](../lgo_learning-go/README.md) 는 `go generate` 와 Wire 를 쓰는 쪽에서 보고, 이 책은 생성기를 만드는 쪽에서 봅니다.



## 원문과 판

> 웹판 전문이 무료로 공개돼 있어 그것을 정본으로 삼습니다.

저자 사이트는 인쇄판(640쪽)·eBook·PDF·웹 네 형태를 안내하고 웹판에 "Read the whole book for free" 라고 적습니다. 웹판은 장마다 절 번호와 Challenges 가 있고, 일부 장 끝에는 설계 판단을 다루는 Design Note 가 붙습니다. 노트에서 출처를 절 번호로 가리키기 좋은 구조입니다.

책의 두 인터프리터 이름은 jlox 와 clox 입니다. 1장에 따르면 jlox 는 개념에 집중하려고 Java 로 씁니다. clox 는 C 로 쓰는데, Java 가 대신해 주던 동적 배열·해시 테이블·객체의 메모리 표현·GC 를 직접 만들어 보기 위해서입니다. 저자는 독자들이 이 코드를 다른 여러 언어로 옮겼다고도 적습니다.

라이선스는 둘로 나뉩니다. 저장소 LICENSE 에 따르면 `.java`·`.c`·`.h`·`.lox` 같은 코드 파일은 MIT 이고, 산문·그림·사이트 디자인은 CC BY-NC-ND 4.0 입니다. ND(변경 금지) 조건이 있으므로 노트는 원문 문단을 통째로 옮기거나 번역해 싣지 않습니다. 짧게 인용할 때는 장·절 번호로 출처를 밝힙니다.



## 장 구성

> 3부 30장과 부록 둘입니다. 1부가 지도를 그리고, 2부와 3부가 같은 언어 Lox 를 서로 다른 두 방식으로 구현합니다.

| 부 | 장 | 구현 | 무엇을 만드나 |
|----|----|------|-------------|
| I. Welcome | 1–3 | — | 언어 구현의 단계 지도, 구현할 언어 Lox 소개 |
| II. A Tree-Walk Interpreter | 4–13 | jlox (Java) | 스캐너, 구문 트리와 Visitor, 재귀 하강 파서, 트리를 걷는 평가기, 문장과 상태, 제어 흐름, 함수와 클로저, resolver, 클래스와 상속 |
| III. A Bytecode Virtual Machine | 14–30 | clox (C) | 바이트코드 청크와 VM, 한 번에 컴파일하는 Pratt 파서, 값 표현·문자열·해시 테이블, 변수·점프·호출, 클로저, GC, 클래스와 메서드, 최적화 |
| 부록 | A1–A2 | — | Lox 문법 전체, 5장 스크립트가 생성한 구문 트리 클래스 |

2부와 3부를 나눈 까닭은 2장 「2.2 Shortcuts and Alternate Routes」에서 볼 수 있습니다. 트리를 걷는 인터프리터는 짜기 쉽지만 느리고, 바이트코드 VM 은 할 일이 많지만 실제 언어 구현에 가깝습니다. 같은 언어를 두 번 구현하면 이 갈림을 코드로 견줄 수 있습니다.



## 장 ↔ 정독 노트

> 아직 쓴 노트가 없습니다. 장을 시작할 때 원문 분량을 보고 편 수를 정한 뒤 노트를 만듭니다.

진척 컬럼은 ⏳ 진행 중, ✅ 완료, ◻ 미착수입니다.

| 장 | 제목 | Design Note | 노트 | 진척 |
|----|------|-------------|------|------|
| 1 | Introduction | What's in a Name? | — | ◻ |
| 2 | A Map of the Territory | — | — | ◻ |
| 3 | The Lox Language | Expressions and Statements | — | ◻ |
| 4 | Scanning | Implicit Semicolons | — | ◻ |
| 5 | Representing Code | — | — | ◻ |
| 6 | Parsing Expressions | Logic Versus History | — | ◻ |
| 7 | Evaluating Expressions | Static and Dynamic Typing | — | ◻ |
| 8 | Statements and State | Implicit Variable Declaration | — | ◻ |
| 9 | Control Flow | Spoonfuls of Syntactic Sugar | — | ◻ |
| 10 | Functions | — | — | ◻ |
| 11 | Resolving and Binding | — | — | ◻ |
| 12 | Classes | Prototypes and Power | — | ◻ |
| 13 | Inheritance | — | — | ◻ |
| 14 | Chunks of Bytecode | Test Your Language | — | ◻ |
| 15 | A Virtual Machine | Register-Based Bytecode | — | ◻ |
| 16 | Scanning on Demand | — | — | ◻ |
| 17 | Compiling Expressions | It's Just Parsing | — | ◻ |
| 18 | Types of Values | — | — | ◻ |
| 19 | Strings | String Encoding | — | ◻ |
| 20 | Hash Tables | — | — | ◻ |
| 21 | Global Variables | — | — | ◻ |
| 22 | Local Variables | — | — | ◻ |
| 23 | Jumping Back and Forth | Considering Goto Harmful | — | ◻ |
| 24 | Calls and Functions | — | — | ◻ |
| 25 | Closures | Closing Over the Loop Variable | — | ◻ |
| 26 | Garbage Collection | Generational Collectors | — | ◻ |
| 27 | Classes and Instances | — | — | ◻ |
| 28 | Methods and Initializers | Novelty Budget | — | ◻ |
| 29 | Superclasses | — | — | ◻ |
| 30 | Optimization | — | — | ◻ |
| A1 | Lox Grammar | — | — | ◻ |
| A2 | Generated Syntax Tree Classes | — | — | ◻ |

빈 노트를 미리 만들지 않는 이유는 분할이 분량에 달려 있기 때문입니다. 장마다 길이가 크게 다르니, 같은 밀도로 쓰면 편 수도 장마다 달라집니다.



## DI·코드 생성 목표와 닿는 절

> 읽는 동기인 질문마다 먼저 볼 절입니다. 왼쪽 질문은 노트의 해석이고, 오른쪽 절 번호는 원문 목차에서 확인했습니다.

| 질문 | 먼저 볼 절 |
|------|-----------|
| 언어 구현은 어떤 단계로 나뉘고, 코드 생성은 그중 어디에 있는가 | 2.1 The Parts of a Language (2.1.3 Static analysis, 2.1.6 Code generation) |
| 다른 언어의 소스 코드를 출력하는 생성기를 무엇이라 부르는가 | 2.2.3 Transpilers |
| 소스 텍스트는 어떻게 토큰이 되고 트리가 되는가 | 4 Scanning, 6.2 Recursive Descent Parsing |
| 트리를 어떻게 표현하고, 노드마다 다른 연산을 어떻게 붙이는가 | 5.2 Implementing Syntax Trees, 5.3.2 The Visitor pattern |
| 코드를 출력하는 작은 생성기는 어떻게 생겼는가 | 5.2.2 Metaprogramming the trees, 부록 A2 |
| 실행하기 전에 프로그램을 훑어 이름을 선언에 묶으려면 무엇이 필요한가 | 11.2 Semantic Analysis, 11.3 A Resolver Class |
| 실행 중에 확인하는 것과 미리 검사하는 것은 무엇을 맞바꾸는가 | 7장 Design Note: Static and Dynamic Typing |
| 트리를 걷지 않고 다른 형태의 코드를 내려면 무엇을 바꾸는가 | 17.3 Emitting Bytecode |

실행 시점 DI 는 실행 중에 연결 정보를 읽어 객체를 잇고, 컴파일 시점 DI 는 실행 전에 소스를 분석해 연결 코드를 냅니다. 이 갈림은 2부(실행 중에 트리를 해석)와 11장·17장(실행 전에 분석하고 코드를 냄)의 갈림과 닮았습니다. 다만 비유가 어디까지 맞는지는 노트를 쓰며 따로 확인합니다. DI 생성기가 다루는 것은 언어의 문법이 아니라 타입과 생성자 사이의 의존 그래프이기 때문입니다.



## 읽는 범위와 실습

> 목표에 가장 가까운 곳은 1·2부와 3부 17장까지입니다. 3부 나머지는 그 뒤에 계속할지 정합니다.

1부는 2부와 3부가 어디로 가는지 보여 주는 지도입니다. 2부는 스캐너부터 resolver 까지 생성기에 필요한 부품을 모두 담습니다.

3부에서 DI 목표와 바로 닿는 곳은 바이트코드를 내는 17장입니다. GC(26장)나 최적화(30장)는 언어 런타임 축이라 [JVM 정독본](../Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/README.md)과 견줄 거리가 많지만, 이번 동기와는 거리가 있습니다.

실습 언어는 2부를 시작할 때 정합니다. 원서처럼 Java 로 짜면 원문 코드와 1:1 로 대조하기 쉽습니다. jlox 를 Go 로 옮기면 Go 표준 라이브러리의 `go/ast` 같은 실제 구문 트리 패키지와 견주기 쉽습니다. 책을 마친 뒤에는 Go 로 작은 DI 코드 생성기를 만드는 실습으로 잇는 것이 처음 계획입니다.

[Go 로드맵](../../go-keywords.md)과는 두 자리에서 닿습니다. 6단계 서비스 조립의 「의존성 주입 — 생성자 주입과 컨테이너의 갈림」 행은 아직 노트 칸이 비어 있습니다. 「로드맵에 넣지 않은 것」 표는 lexer·parser·AST 로 DSL 을 만드는 일을 컴파일러 축이라며 뺐는데, 이 책이 바로 그 축을 맡습니다.



## 작성 규칙

> 이 폴더의 노트를 쓸 때 지키는 규칙입니다. 웹판 원문이 1차 자료라는 것이 그 중심입니다.

- 파일명은 `{장}-{편}.{제목}.md` 입니다. 앞 번호는 원서의 장 번호(1~30), 뒤 번호는 그 장을 여러 편으로 나눈 순번입니다.
- 본문은 합니다체로 씁니다. 문단형 설명을 우선하고, 주장마다 왜 그런지를 함께 적습니다.
- 사실은 웹판 원문에서 가져오고 절 번호로 출처를 밝힙니다. 웹판에는 판 번호가 없으니 조회일을 함께 적습니다.
- 코드는 MIT 라서 노트에 옮길 수 있지만, 원 저장소의 파일 경로를 같이 적습니다. 산문은 CC BY-NC-ND 라 짧은 인용만 합니다.
- 실습 코드는 `write/` 밖의 별도 저장소에 두고, 노트에는 저장소 이름과 경로만 적습니다.
- 도식은 `_assets/` 에 두고, 생성기 선언을 원본으로 삼아 SVG 를 손으로 고치지 않습니다.



## 관련 문서

- [SICP JavaScript Edition 정독 인덱스](../sicp_structure-and-interpretation-of-computer-programs/README.md) — 같은 언어를 해석하는 평가기와 레지스터 머신
- [Learning Go 정독 인덱스](../lgo_learning-go/README.md) — `go generate` 와 Wire 를 쓰는 쪽
- [Writing An Interpreter In Go 정독 인덱스](../waiig_writing-an-interpreter-in-go/README.md) — 2부와 같은 과정을 Go 로, 처음부터 Pratt 파서
- [Writing A Compiler In Go 정독 인덱스](../wacig_writing-a-compiler-in-go/README.md) — 3부와 같은 전환을 Go 로, 심볼 테이블과 클로저
- [Go 로드맵](../../go-keywords.md) — 6단계 의존성 주입, 「로드맵에 넣지 않은 것」의 컴파일러 축
- [01_language MOC](../../README.md)



## 참고 자료

- Robert Nystrom, 『Crafting Interpreters』 웹판 목차 — https://craftinginterpreters.com/contents.html
- 같은 책 1장 「Introduction」 — https://craftinginterpreters.com/introduction.html
- 원 저장소 LICENSE — https://github.com/munificent/craftinginterpreters/blob/master/LICENSE
- Google Wire 저장소 — https://github.com/google/wire
