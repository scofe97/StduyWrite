---
title: Spring 컨테이너 학습 묶음
tags: [moc, spring, spring-boot, ioc, di, container]
status: draft
related:
  - ../README.md
updated: 2026-05-23
---

# Spring 컨테이너 학습 묶음
---

> Spring 의 시작점인 IoC 컨테이너를 다룬다. 어떤 면에서 본 묶음은 `04_webflux/`, `05_testing/` 보다 *먼저* 와야 하지만, 11_spring 정식 폴더로는 가장 늦게 신설됐다. 본 폴더의 1편은 노션 학습 노트(`_notion_import/study/`) 의 다섯 편(01-4 DI/IoC, 03-1 컨테이너·빈 등록, 03-2 싱글톤, 03-3 의존관계 주입, 03-4 생명주기·스코프) 을 재작성해 묶은 통합본이다.

## 학습 순서

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [객체지향 원리 적용 — DI와 IoC](01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) | AppConfig 등장 배경, IoC 와 DI 의 관계, BeanFactory / ApplicationContext, 빈 등록 세 방식, 생성자 주입 권장 이유, 다중 빈 처리(@Qualifier, @Primary, Map/List), CGLIB 싱글톤 보장, 생명주기 7단계, 스코프 7종과 프록시 |

## 원본 학습 자료

본 묶음의 첫 편은 다음 노션 노트를 통합 재작성한 산출물이다. 원본은 `_notion_import/study/` 에 그대로 보관되어 있다.

- `[Spring Study] 01-4 객체지향 원리 적용(DI, IoC) ⭐`
- `[Spring Study] 03-1 스프링 컨테이너, 빈 등록 조회, 컴포넌트 스캔`
- `[Spring Study] 03-2 싱글톤 컨테이너, 스레드 로컬`
- `[Spring Study] 03-3 의존관계 주입, 조건 및 복수 빈 처리`
- `[Spring Study] 03-4 빈 생명주기(@Post, @Destroy) 스코프`

## 환경과 버전

| 항목 | 값 |
|------|----|
| Spring Framework | 6.2.x |
| Spring Boot | 3.3.x |
| Java | 17 LTS |
| 검증 코드 | 학습 단계 — 별도 샘플 프로젝트 없이 본문 스니펫이 자체 완결 |

## 후속 묶음 (예정)

- `02_servlet/` — WAS·Servlet·멀티 스레드·Cookie/Session (`_notion_import/study/02-* `)
- `03_mvc/` — DispatcherServlet, FrontController 진화, MVC 전체 구조 (`_notion_import/study/04-*`, `05-*`, `06-*`)
- `06_aop/` — 횡단 관심사, JDK 동적 프록시, 빈 후처리기, @Aspect AOP (`_notion_import/study/08-*`, `09-*`)
- `08_exception-handling/` — 서블릿 예외 처리, HandlerExceptionResolver (`_notion_import/study/07-*`)
