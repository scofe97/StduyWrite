---
title: Spring Start Here — 책 요약 MOC
tags: [moc, spring, spring-framework, spring-boot, book-summary]
status: draft
source:
  - "Spring Start Here, Laurențiu Spilcă (Manning, 2021)"
related:
  - ../../README.md
  - ../../01_core/01-01.객체지향 원리 적용 — DI와 IoC.md
updated: 2026-06-15
---


# Spring Start Here — 책 요약 MOC
---
> Laurențiu Spilcă의 *Spring Start Here*(Manning, 2021)를 정리하는 학습 노트 모음입니다. 이 페이지가 책의 진입점이 됩니다.


## 왜 책 전용 폴더인가

`11_spring/`의 다른 폴더(`01_core`, `08_transaction` 등)는 주제 축으로 묶입니다. 반면 이 폴더는 **책 한 권의 흐름**을 보존합니다. 이 책은 프레임워크가 무엇인지에서 출발해 Spring Context와 IoC, AOP, 데이터 접근, 웹 개발, 테스트까지 입문 골격을 한 계단씩 쌓아 올립니다. 저자가 머리말에서 밝혔듯 학습 경로가 선형이 아니라, 앞 장에서 던진 조각을 뒤 장에서 맞춰야 그림이 완성되는 구조입니다. 그래서 주제별로 흩어 놓기보다 책 순서를 그대로 따라가는 쪽이 입문 단계에서는 잘 맞습니다.

각 편을 다 쓴 뒤에는 같은 주제의 정식 카테고리 폴더(IoC/DI는 `01_core`, AOP는 `05_aop`, 트랜잭션은 `08_transaction`)로 교차참조를 겁니다. 책 흐름은 이 폴더가, 주제별 깊이는 카테고리 폴더가 맡는 역할 분담입니다.


## 챕터 목록

받은 순서대로 채웁니다. 파일명은 책의 실제 챕터 번호를 그대로 씁니다.

| # | 파일 | 상태 |
|---|------|------|
| 01 | [Spring과 프레임워크 — 생태계·IoC·실무 시나리오](01.Spring과%20프레임워크.md) | draft |
| 02 | [Spring Context와 Bean 등록 — @Bean·스테레오타입·프로그래밍 방식](02.Spring%20Context와%20Bean%20등록.md) | draft |
| 03 | [Bean 와이어링과 의존성 주입 — wiring·@Autowired·순환 의존·@Qualifier](03.Bean%20와이어링과%20의존성%20주입.md) | draft |
| 04 | [추상화와 의존성 주입 — 인터페이스 계약·다중 구현체·@Service·@Repository](04.추상화와%20의존성%20주입.md) | draft |
| 05 | [Bean 스코프와 생애주기 — singleton·prototype·eager·lazy](05.Bean%20스코프와%20생애주기.md) | draft |
| 06 | [Spring AOP와 Aspect — 프록시·weaving·advice·실행 체인](06.Spring%20AOP와%20Aspect.md) | draft |
| 07 | [Spring Boot와 Spring MVC — 서블릿 컨테이너·DispatcherServlet 흐름](07.Spring%20Boot와%20Spring%20MVC.md) | draft |
| 08 | [동적 뷰와 HTTP 데이터 — Thymeleaf·요청 파라미터·경로 변수·HTTP 메서드](08.동적%20뷰와%20HTTP%20데이터.md) | draft |
| 09 | [웹 스코프와 로그인 — request·session·application 스코프와 리다이렉트](09.웹%20스코프와%20로그인.md) | draft |
| 10 | [REST 서비스 — @RestController·ResponseEntity·예외 처리·@RequestBody](10.REST%20서비스.md) | draft |
| 11 | [REST 엔드포인트 소비 — OpenFeign·RestTemplate·WebClient](11.REST%20엔드포인트%20소비.md) | draft |
| 12 | [데이터 소스와 JdbcTemplate — data source·JDBC 드라이버·update·query·RowMapper](12.데이터%20소스와%20JdbcTemplate.md) | draft |


## 작성 규약

이 폴더의 모든 노트는 writing 스킬 `07-04-book-summary.md` 정본의 7단 구조를 따릅니다. 핵심요약·학습목표·본문정리·심화학습·실무적용·면접대비·체크리스트를 갖추고, 설명은 면접에서 말할 수 있는 완전한 문장으로 씁니다. 핵심 개념은 다크 테마 SVG로 도식화하며, 원서 그림을 옮길 때는 구조만 재현하고 라벨을 한글로 병기합니다.
