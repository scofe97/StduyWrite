---
title: 01_language/_writing MOC
tags: [moc, clean-code, refactoring, code-quality]
status: final
related:
  - ../README.md
  - ../java/03_DesignPatterns/README.md
updated: 2026-05-31
---

# 01_language/_writing — 코드 작성·리팩토링

> 특정 언어에 종속되지 않는 *코드 작성·리팩토링 원칙*을 모은다. 네이밍·함수·주석 같은 줄 단위 미시 규칙(클린 코드)과, 그 좋은 코드에 도달하는 리팩토링 절차·규칙이다. Java·Python처럼 언어 폴더(java/·python/)와 형제로 두되, 언어 무관 공통이라 `_` prefix로 맨 앞에 둔다.

## 하위

- [01-01.클린 코드 원칙](01-01.클린%20코드%20원칙.md) — 네이밍·함수·주석·예외·CQS·디미터·테스트 등 줄 단위 미시 규칙 (좋은 코드의 *기준*)
- [02-01.리팩토링 절차와 규칙](02-01.리팩토링%20절차와%20규칙.md) — Five Lines of Code Ch1 기반: 리팩토링 정의·Skills/Culture/Tools 세 축·6단계 워크플로·테스트 없이 안전하게 (그 기준에 *도달하는 법*)
- [02-02.리팩토링의 기술적 토대](02-02.리팩토링의%20기술적%20토대.md) — Five Lines of Code Ch2 기반: 가독성·유지보수성·불변식 지역화·상속보다 조합·추가에 의한 변경 (리팩토링이 *기술적으로 무엇을 좋게 만드는가*)
- [02-03.긴 함수 쪼개기](02-03.긴%20함수%20쪼개기.md) — Five Lines of Code Ch3 기반: Five lines 규칙·Extract method 패턴·Either call or pass·if only at the start (긴 함수를 *실제로 쪼개는 규칙과 절차*)
- [02-04.타입 코드를 다형성으로](02-04.타입%20코드를%20다형성으로.md) — Five Lines of Code Ch4 기반: Never use if with else·Replace type code with classes·Push code into classes·Never use switch·Specialize method·Only inherit from interfaces (enum/if-else를 *다형성으로 바꿔 if를 제거*)
- [02-05.유사 코드 통합](02-05.유사%20코드%20통합.md) — Five Lines of Code Ch5 기반: Unify similar classes·Combine ifs·조건 산술·Use pure conditions·Introduce strategy pattern·No interface with only one implementation·UML (비슷한 *코드를 하나로 합치는* 패턴)
- [02-06.데이터 방어](02-06.데이터%20방어.md) — Five Lines of Code Ch6 기반(1부 마지막): Do not use getters or setters·Eliminate getter or setter·Never have common affixes·Encapsulate data·Enforce sequence·private constructor enum (캡슐화로 *데이터를 방어*)
- [03-01.컴파일러와 협업](03-01.컴파일러와%20협업.md) — Five Lines of Code Ch7 기반(2부 시작): halting problem·컴파일러 강점 4(reachability·definite assignment·access control·type checking)·약점 6·싸우지 않기·불변식 6단계 사다리·경고 0 (컴파일러를 *팀의 일원으로*)
- [03-02.주석 멀리하기](03-02.주석%20멀리하기.md) — Five Lines of Code Ch8 기반: 주석의 위험·"코드가 말할 수 없는 것만"·주석 5분류(낡음·주석처리코드·trivial·메서드명화·불변식문서화)와 각각의 처리 (주석은 *리팩토링 단계에서 정리*)
- [03-03.코드 삭제를 사랑하라](03-03.코드%20삭제를%20사랑하라.md) — Five Lines of Code Ch9 기반: 코드는 부채·매몰비용 오류·incidental complexity 4갈래(무지·낭비·부채·끌림)·strangler fig로 레거시 측정·spike and stabilize·브랜치/문서/테스트/설정/라이브러리/기능 삭제 기준 (제 몫 못 하는 것을 *덜어내기*)
- [03-04.코드 추가를 두려워 말라](03-04.코드%20추가를%20두려워%20말라.md) — Five Lines of Code Ch10 기반: 코드 추가 공포 4증상(enter the danger·spike·80:20·developer life)·코드 추가가 수정보다 안전·중복의 global/local velocity·accidental vs essential complexity·하위 호환 versioning·feature toggle 5단계·branch by abstraction (수정 대신 *추가*로 위험 낮추기)
- [03-05.코드의 구조를 따르라](03-05.코드의%20구조를%20따르라.md) — Five Lines of Code Ch11 기반(2부 종합편): 구조 공간 4범주(scope×origin)·Conway's law·행동을 담는 세 자리(제어 흐름·자료구조·데이터)·예측 대신 관찰·코드 이해 없이 안전 얻는 5방법·미활용 구조 4신호(공백·중복·공통 접사·런타임 타입) (구조를 *읽고 따르는* 일관된 사고)
- [03-06.최적화와 일반성을 피하라](03-06.최적화와%20일반성을%20피하라.md) — Five Lines of Code Ch12 기반: 일반성·최적화가 coupling·invariant로 인지 부하를 늘림·최소로 짓기(Kent Beck)·비슷한 안정성끼리 통합·성능 테스트 3종(benchmark·load·approval)·제약 이론과 resource pooling·프로파일링과 80:20·자료구조 교체·캐싱 3종(멱등·임시 멱등·내부)·performance tuning 격리 (성능·유연성을 *증명 없이 사지 않기*)
- [03-07.나쁜 코드는 나빠 보이게](03-07.나쁜%20코드는%20나빠%20보이게.md) — Five Lines of Code Ch13 기반(2부 마지막): anti-refactoring으로 프로세스 이슈 신호·psychological safety(Project Aristotle)·pristine/legacy 분리와 broken window theory·나쁜 코드 정의 4접근(이 책 규칙·code smell·순환 복잡도·인지 복잡도)·안전한 vandalize 3규칙·10가지 실천 기법(enum·type code·magic number·주석·whitespace·affix 그룹화·context·긴 메서드·많은 파라미터·getter/setter) (좋게 못 만들 코드는 *눈에 띄게*)

> **번호 체계**: `01-`=클린 코드(Martin) / `02-`=Five Lines of Code 1부(Ch1~6, 게임 예제로 익히는 리팩토링 *절차*) / `03-`=Five Lines of Code 2부(Ch7~, 그 절차를 떠받치는 *일반 원칙*). prefix는 출처 묶음, 끝 번호는 챕터 순서다.

## 경계 기준

여기는 *언어중립* 코드 작성·리팩토링 원칙만 둔다. 언어에 종속된 코드 스타일은 각 언어 폴더에 둔다 — 일급객체·Optional/Stream 활용 같은 Java 코드 스타일은 [`../java/03_DesignPatterns/02-01`](../java/03_DesignPatterns/02-01.일급객체%20사상과%20Java%20코드%20스타일.md), 함수형 패턴이 Spring 인프라와 만나는 함정은 [`../java/03_DesignPatterns/02-03`](../java/03_DesignPatterns/02-03.함수형%20패턴%20도입의%20함정과%20경계%20설계.md)에 있다.

클래스·모듈 단위 거시 *설계* 원칙(SOLID·계층·의존성)은 코드 작성이 아니라 설계라, [`../java/03_DesignPatterns/01-01.SOLID 원칙`](../java/03_DesignPatterns/01-01.SOLID%20원칙.md)과 [`03_architecture/`](../../03_architecture/)가 맡는다. *도메인 모델* 차원의 리팩토링도 [`03_architecture/04_ddd/03-01`](../../03_architecture/04_ddd/03-01.리팩토링%20원칙%20—%20행동하기%20전에%20이해하기.md)에 별도로 있다. 이 폴더는 그보다 작은 *함수·줄 단위*의 작성·개선에 집중한다.
