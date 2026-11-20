---
title: Writing An Interpreter In Go — 정독 인덱스
tags: [moc, study-index, book, writing-an-interpreter-in-go, interpreter, go, lexer, parser, ast]
status: draft
source:
  - 《Writing An Interpreter In Go》 (Thorsten Ball) — 판 1.7 (2020-05-07, 책 뒤 Changelog 기준) · PDF 210쪽 · 본문 4장
  - 원본 PDF — GoogleDrive/내 드라이브/book/Writing An Interpreter in Go/ (2026-11-11 추가, 같은 파일이 book/Writing An Interpreter In Go.pdf 에도 있음, cmp 일치)
  - 책 사이트 — https://interpreterbook.com
related:
  - ../wacig_writing-a-compiler-in-go/README.md
  - ../ci_crafting-interpreters/README.md
  - ../lgo_learning-go/README.md
  - ../../README.md
  - ../../go-keywords.md
updated: 2026-11-11
---

# Writing An Interpreter In Go — 정독 인덱스

---

> 이 폴더는 Thorsten Ball 의 『Writing An Interpreter In Go』를 장 단위로 정독하며 정리하는 책 종속 학습 노트입니다. Monkey 라는 작은 언어의 렉서·파서·트리 워킹 인터프리터를 Go 표준 라이브러리만으로 처음부터 짭니다.

## 이 책을 읽는 이유

> DI 를 컴파일 시점에 하는 도구가 소스를 어떻게 읽어 트리로 만드는지, 실습할 언어인 Go 로 직접 짜 보려고 읽습니다.

동기는 [Crafting Interpreters 인덱스](../ci_crafting-interpreters/README.md)의 「이 책을 읽는 이유」와 같습니다. 실행 시점 DI 와 컴파일 시점 DI 의 갈림을 설명하려면, 생성기가 소스를 읽고 분석해 코드를 내는 과정을 손으로 한 번 거쳐야 합니다. Crafting Interpreters 는 그 과정을 Java 와 C 로 보여 주고, 이 책은 같은 과정을 Go 로 보여 줍니다. 나중에 만들 DI 코드 생성기도 Go 로 짤 계획이라, 렉서·파서·AST 를 같은 언어로 먼저 짜 두면 Go 의 `go/ast` 같은 실제 패키지와 견주기 쉽습니다.

저자는 서문에서 이 책을 900쪽짜리 컴파일러 교재와 50줄짜리 Lisp 인터프리터 블로그 글 사이에 두었다고 적습니다. 서드파티 도구와 라이브러리를 쓰지 않고, 파서 생성기 대신 파서를 직접 짭니다(2.2 「Why not a parser generator?」). 코드 생성 도구가 블랙박스로 남지 않게 하려는 이번 목적과 맞는 선택입니다.



## 원문과 판

> 책 뒤 Changelog 의 마지막 항목인 1.7 판(2020-05-07)을 정본으로 삼습니다.

서문에 따르면 1.7 판은 Go 1.14 로 다시 확인했습니다. 처음 쓸 때는 Go 1.7 이었습니다. 저자는 Go 1.0 이상이면 동작한다고 적지만 실습은 지금 쓰는 Go 판에서 다시 돌려 확인합니다. 책의 코드는 서문에 적힌 `waiig_code_1.7.zip` 으로 배포됩니다.

책 끝에는 「The Lost Chapter」 절이 있습니다. 본문에서 뺀 매크로 시스템 장(『The Lost Chapter: A Macro System For Monkey』)을 interpreterbook.com/lost 에서 무료로 공개한다는 안내입니다. 매크로는 AST 를 입력으로 받아 새 AST 를 내는 일이라, 코드 생성 목표와 가장 가까운 장일 수 있습니다. 이 PDF 에는 들어 있지 않으므로 읽을지는 4장을 마친 뒤 정합니다.

유료 책이므로 노트는 원문 문단을 길게 옮기지 않고, 짧게 인용할 때는 절 번호와 쪽수로 출처를 밝힙니다.



## 장 구성

> 본문 4장, 책 쪽 10–201 이 대상입니다. 앞 세 장이 렉서·파서·평가기를 하나씩 만들고, 4장이 그 위에 자료형을 더합니다.

| 장 | 제목 | 쪽 | 무엇을 만드나 |
|----|------|----|-------------|
| 1 | Lexing | 10–27 | 토큰 정의, 렉서, REPL 의 시작 |
| 2 | Parsing | 28–102 | 파서 생성기를 쓰지 않는 이유, let·return 문, Pratt 파싱(Top Down Operator Precedence)으로 식 파싱, AST 준비 |
| 3 | Evaluation | 103–151 | 평가 전략, 트리 워킹 인터프리터, 객체 표현, 조건·return·오류 처리, 바인딩과 환경, 함수 호출, GC 를 누가 하는가 |
| 4 | Extending the Interpreter | 152–201 | 문자열, 내장 함수, 배열, 해시 |

쪽 범위는 목차의 장 시작 쪽에서 계산했습니다. 4장 끝 쪽은 Resources(202쪽) 바로 앞으로 잡았습니다. 「The Lost Chapter」 안내 절(200쪽)도 그 범위 안에 있습니다. 단어 수는 PDF 전체를 `pdftotext -layout` 으로 뽑아 `wc -w` 로 센 값이 63,512 이고 코드가 많이 섞여 있습니다.



## 장 ↔ 정독 노트

> 아직 쓴 노트가 없습니다. 장을 시작할 때 분량을 보고 편 수를 정합니다.

진척 컬럼은 ⏳ 진행 중, ✅ 완료, ◻ 미착수입니다.

| 장 | 절 | 노트 | 진척 |
|----|----|------|------|
| 1 | 1.1 Lexical Analysis · 1.2 Defining Our Tokens · 1.3 The Lexer · 1.4 Extending our Token Set and Lexer · 1.5 Start of a REPL | — | ◻ |
| 2 | 2.1 Parsers · 2.2 Why not a parser generator? · 2.3 Writing a Parser for the Monkey Programming Language · 2.4 Parser's first steps: parsing let statements · 2.5 Parsing Return Statements · 2.6 Parsing Expressions · 2.7 How Pratt Parsing Works · 2.8 Extending the Parser · 2.9 Read-Parse-Print-Loop | — | ◻ |
| 3 | 3.1 Giving Meaning to Symbols · 3.2 Strategies of Evaluation · 3.3 A Tree-Walking Interpreter · 3.4 Representing Objects · 3.5 Evaluating Expressions · 3.6 Conditionals · 3.7 Return Statements · 3.8 Error Handling · 3.9 Bindings & The Environment · 3.10 Functions & Function Calls · 3.11 Who's taking the trash out? | — | ◻ |
| 4 | 4.1 Data Types & Functions · 4.2 Strings · 4.3 Built-in Functions · 4.4 Array · 4.5 Hashes · 4.6 The Grand Finale | — | ◻ |



## 이웃 책과 나눠 읽기

> Crafting Interpreters 2부와 범위가 겹칩니다. 이 책은 Go 로 짜는 실습의 뼈대로, Crafting Interpreters 는 설계 판단을 읽는 쪽으로 씁니다.

두 책 모두 렉서·파서·트리를 걷는 평가기 순서로 갑니다. 갈리는 곳은 셋입니다. 이 책은 처음부터 Pratt 파서를 씁니다. Crafting Interpreters 는 2부에서 재귀 하강 파서를 쓴 뒤 3부 17장에서 Pratt 파서로 옮깁니다. Crafting Interpreters 11장에는 실행 전에 변수를 선언에 묶는 resolver 가 있습니다. 이 책의 평가기는 그런 단계 없이 실행 중에 환경을 따라 이름을 찾습니다(3.9). 실행 전에 이름을 정리하는 일은 후속작 [Writing A Compiler In Go](../wacig_writing-a-compiler-in-go/README.md) 5장의 심볼 테이블이 맡습니다.

어느 책을 먼저 읽을지는 첫 노트를 쓸 때 정합니다. 같은 개념을 두 책에서 두 번 정리하지 않도록, 한 개념의 정본 노트는 한 곳에 두고 다른 쪽은 링크로 넘깁니다.



## 작성 규칙

> 이 폴더의 노트를 쓸 때 지키는 규칙입니다. 원본 PDF 가 1차 자료라는 것이 그 중심입니다.

- 파일명은 `{장}-{편}.{제목}.md` 입니다. 앞 번호는 원서의 장 번호(1~4), 뒤 번호는 그 장을 여러 편으로 나눈 순번입니다.
- 본문은 합니다체로 씁니다. 문단형 설명을 우선하고, 주장마다 왜 그런지를 함께 적습니다.
- 사실은 `pdftotext` 로 추출한 본문에서 가져오고 절 번호와 쪽수로 출처를 밝힙니다.
- 실습 코드는 `write/` 밖의 별도 저장소에 두고, 노트에는 저장소 이름과 경로만 적습니다. 원서 코드와 다르게 짠 곳은 노트에 그 차이를 적습니다.
- 도식은 `_assets/` 에 두고, 생성기 선언을 원본으로 삼아 SVG 를 손으로 고치지 않습니다.



## 관련 문서

- [Writing A Compiler In Go 정독 인덱스](../wacig_writing-a-compiler-in-go/README.md) — 같은 Monkey 를 바이트코드 컴파일러와 VM 으로 옮기는 후속작
- [Crafting Interpreters 정독 인덱스](../ci_crafting-interpreters/README.md) — 같은 과정을 Java·C 로, 설계 판단과 resolver 를 함께
- [Learning Go 정독 인덱스](../lgo_learning-go/README.md) — `go generate` 와 Wire 를 쓰는 쪽
- [Go 로드맵](../../go-keywords.md) — 「로드맵에 넣지 않은 것」의 lexer·parser·AST 축
- [01_language MOC](../../README.md)



## 참고 자료

- Thorsten Ball, 『Writing An Interpreter In Go』 1.7 판 — https://interpreterbook.com
- 같은 저자, 『The Lost Chapter: A Macro System For Monkey』 — https://interpreterbook.com/lost
