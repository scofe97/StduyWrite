---
title: SICP JavaScript Edition — 정독 인덱스
tags: [moc, study-index, book, sicp, abstraction, interpreter, javascript]
status: draft
source:
  - 《Structure and Interpretation of Computer Programs, JavaScript Edition》 (Harold Abelson · Gerald Jay Sussman, adapted to JavaScript by Martin Henz · Tobias Wrigstad, with Julie Sussman, MIT Press, 2022) — PDF 640쪽 · 본문 5장 · 연습문제 356개
  - 원본 PDF — GoogleDrive/내 드라이브/book/Structure and Interpretation of Computer Programs, JavaScript Edition/Structure and Interpretation of Computer Programs, JavaScript Edition.pdf (https://sicp.sourceacademy.org/sicpjs.pdf 에서 2026-09-23 받음, 9,507,522 bytes)
  - 대조판 — http://sicp.sourceacademy.org (1996년 Scheme 2판에서 달라진 곳을 표시)
related:
  - ../five-lines-of-code/README.md
  - ../Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/README.md
  - ../../README.md
updated: 2026-09-23
---

# SICP JavaScript Edition — 정독 인덱스

---

> 이 폴더는 Abelson·Sussman 의 『Structure and Interpretation of Computer Programs』 JavaScript판을 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 함수와 데이터로 추상화를 쌓아 올린 뒤, 마지막 두 장에서 그 프로그램을 실행하는 인터프리터와 기계를 직접 만듭니다.

## 이 책을 여기 두는 이유

> 이 책은 언어 교재가 아니라 프로그래밍 원리서입니다. 원리서를 맡는 대분류가 따로 없어서, 언어 중립 원칙서가 이미 있는 `01_language/book/` 에 둡니다.

책은 JavaScript 로 쓰였지만 JavaScript 를 가르치지 않습니다. JavaScript판 서문에서 Guy L. Steele Jr. 가 이 점을 짚습니다. SICP 는 처음부터 특정 언어에 관한 책이 아니었고, 어느 언어에서나 쓸모 있는 프로그램 조직의 일반 원리를 보여 준다는 것입니다("SICP was never about a programming language").

1~3장은 함수·데이터·상태로 추상화를 쌓는 법을 다룹니다. 4·5장은 방향을 바꿔 언어 자체를 만듭니다. 인터프리터를 짜고, 그것을 레지스터 머신으로 내려 메모리 할당과 GC, 컴파일러까지 구현합니다.

`01_language/` README 는 범위를 "언어 레퍼런스에 나오는 내용"으로 적어 두었으니, 엄밀히는 이 책과 맞지 않습니다. 그래도 새 대분류는 만들지 않았습니다. 책 한 권을 위해 분류를 먼저 세우는 일은 대개 실패한다는 것이 이 저장소의 배치 규약이고, CS 교재가 더 쌓이면 그때 분할합니다.

이웃 폴더와는 이렇게 나뉩니다. [`five-lines-of-code/`](../five-lines-of-code/README.md) 가 코드 한 줄 단위의 작성 원칙을 다룬다면, 이 책은 그 아래에 있는 추상화의 원리를 다룹니다. 5장의 GC 와 컴파일은 [JVM 정독본](../Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/README.md) 의 실제 구현과 겹치므로, 겹치는 자리에는 교차 참조를 답니다.



## 왜 JavaScript판을 정본으로 삼는가

> 2022년 MIT Press 판이 가장 최근 공식판입니다. 1996년 Scheme 2판을 같은 목차로 옮긴 판이고, Scheme 원문은 대조판으로 봅니다.

Scheme판에는 3판이 없습니다. JavaScript판은 새 판이 아니라 번안판입니다. 싱가포르국립대(NUS)의 입문 과목 CS1101S 에서 만들었고, 옮긴이 감사의 글에 따르면 9년 동안 300명이 넘는 학부 조교의 피드백을 받아 다듬었습니다.

정본으로 고른 이유는 셋입니다.

- 문법이 Java 와 가깝습니다. 옮긴이들은 ES2015 에 들어온 `const`·`let` 선언과 람다 표현식 덕분에 원서의 핵심 아이디어를 거의 그대로 옮길 수 있었다고 씁니다.
- 실행 환경을 따로 꾸리지 않아도 됩니다. 책의 프로그램은 [Source Academy](https://sourceacademy.org) 에서 돌아가고, 3.4절 동시성·4.2절 지연 평가·4.3절 비결정 계산용 실행기도 그곳에 따로 구현돼 있습니다.
- 원문을 잃지 않습니다. [대조판](http://sicp.sourceacademy.org)이 Scheme 2판과 달라진 곳을 표시하므로, Scheme판 PDF 를 따로 두지 않아도 원문을 확인할 수 있습니다.

읽을 때 달라지는 곳이 하나 있습니다. Scheme 에서는 코드가 곧 리스트라서 인터프리터가 그대로 해석합니다. JavaScript판은 4.1.2절에서 책이 제공하는 `parse` 함수로 프로그램 텍스트를 tagged list 로 먼저 바꿉니다. 파서를 직접 짜는 것은 아니므로, 해석 전에 표현을 한 번 거친다는 점만 다릅니다.

라이선스는 셋으로 나뉩니다. 책은 CC BY-NC-SA 4.0, Scheme 2판에서 옮긴 본문은 CC BY-SA 4.0, 프로그램은 GPL v3 입니다. 노트에 원문을 인용할 때는 절 번호로 출처를 밝힙니다.



## 장 구성

> 본문 5장, 책 쪽 1–564가 대상입니다. 쪽수는 책 쪽번호이고, PDF 쪽번호는 여기에 32를 더한 값입니다.

| 장 | 제목 | 책 쪽 | 단어 | 연습문제 | 무엇을 다루나 |
|----|------|------|------|---------|-------------|
| 1 | Building Abstractions with Functions | 1–68 | 27,139 | 46 | 식과 이름, 치환 모델, 재귀 과정과 반복 과정, 함수를 인자로 받고 돌려주는 고차 함수 |
| 2 | Building Abstractions with Data | 69–188 | 42,615 | 97 | 인터페이스 뒤에 표현을 숨기는 데이터 추상화, 리스트와 트리, 심볼 데이터, 같은 연산을 여러 표현에 거는 제네릭 연산 |
| 3 | Modularity, Objects, and State | 189–316 | 44,076 | 82 | 대입과 지역 상태, 환경 모델, 가변 데이터(큐·테이블), 동시성과 직렬화, 지연 평가 스트림 |
| 4 | Metalinguistic Abstraction | 317–448 | 43,610 | 76 | 메타순환 평가기, 지연 평가, 비결정 계산, 논리 프로그래밍 |
| 5 | Computing with Register Machines | 449–564 | 39,458 | 55 | 레지스터 머신 설계와 시뮬레이터, 메모리 할당과 GC, 명시적 제어 평가기, 컴파일러 |

단어 수는 장 쪽 범위를 `pdftotext` 로 뽑아 `wc -w` 로 센 값이라 코드와 각주가 들어 있습니다. 연습문제 수는 본문의 `Exercise n.m` 표제를 센 값이고, 장마다 마지막 번호와 개수가 일치합니다. 본문 앞의 서문과 머리말 다섯 편(2021년 Steele 서문, 1984년 Perlis 서문, 옮긴이 머리말, 1996년·1984년 원서 머리말)과 감사의 글, 뒤쪽의 References·Index·List of Exercises 는 정독 대상에서 뺍니다.



## 장 ↔ 정독 노트

> 아직 쓴 노트가 없습니다. 장을 시작할 때 원문 분량을 보고 분할안을 먼저 정한 뒤 노트를 만듭니다.

진척 컬럼은 ⏳ 진행 중, ✅ 완료, ◻ 미착수입니다.

| 장 | 절 | 노트 | 진척 |
|----|----|------|------|
| 1 | 1.1 The Elements of Programming · 1.2 Functions and the Processes They Generate · 1.3 Formulating Abstractions with Higher-Order Functions | — | ◻ |
| 2 | 2.1 Introduction to Data Abstraction · 2.2 Hierarchical Data and the Closure Property · 2.3 Symbolic Data · 2.4 Multiple Representations for Abstract Data · 2.5 Systems with Generic Operations | — | ◻ |
| 3 | 3.1 Assignment and Local State · 3.2 The Environment Model of Evaluation · 3.3 Modeling with Mutable Data · 3.4 Concurrency: Time Is of the Essence · 3.5 Streams | — | ◻ |
| 4 | 4.1 The Metacircular Evaluator · 4.2 Lazy Evaluation · 4.3 Nondeterministic Computing · 4.4 Logic Programming | — | ◻ |
| 5 | 5.1 Designing Register Machines · 5.2 A Register-Machine Simulator · 5.3 Storage Allocation and Garbage Collection · 5.4 The Explicit-Control Evaluator · 5.5 Compilation | — | ◻ |

빈 노트를 미리 만들지 않는 이유는 분할이 분량에 달려 있기 때문입니다. 1장은 2만 7천 단어이고 2~4장은 4만 2천~4만 4천 단어라서, 같은 밀도로 쓰면 편 수가 장마다 크게 달라집니다.



## 작성 규칙

> 이 폴더의 노트를 쓸 때 지키는 규칙입니다. 원문이 1차 자료라는 것이 그 중심입니다.

- 파일명은 `{장}-{편}.{제목}.md` 입니다. 앞 번호는 책의 장 번호, 뒤 번호는 그 장을 여러 편으로 나눈 순번입니다.
- 본문은 합니다체로 씁니다. 문단형 설명을 우선하고, 주장마다 왜 그런지를 함께 적습니다.
- 코드·연습문제 번호·인용은 JavaScript판 원문과 1:1 로 맞춥니다. Scheme 원문과 뜻이 갈리는 자리는 대조판으로 확인한 뒤 나란히 적습니다.
- 사실은 `pdftotext` 로 추출한 본문에서 가져옵니다. 표와 그림은 추출본이 열을 섞을 수 있으니 페이지 이미지로 판독합니다.
- 실습 코드는 `write/` 밖의 별도 저장소에 두고, 노트에는 저장소 이름과 경로만 적습니다.
- 도식은 `_assets/` 에 두고, 생성기 선언을 원본으로 삼아 SVG 를 손으로 고치지 않습니다.
