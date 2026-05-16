---
title: 01_language/python MOC
tags: [moc, python]
status: final
related:
  - ../README.md
  - testing/README.md
updated: 2026-05-10
---

# 01_language/python

> Python 언어 자체보다 먼저 "어떤 시점에 Python을 고르는가"의 결정을 모은다. 현재 시점에서는 통합 테스트·자동화 스크립트 영역에서 Python을 쓴 사례가 많아 그쪽이 먼저 채워진다.

## 하위

- [testing/](testing/) — pytest 기반 통합 테스트 묶음. requests·pymysql·ThreadPoolExecutor·chaos fixture·cryptography까지 한 줄기로 엮여 있다.

## 경계 기준

`testing/`은 "Spring Boot 애플리케이션을 외부에서 검증하는 Python 클라이언트"의 결정을 담는다. Spring 측의 통합 테스트는 [`01_language/java/spring/05_testing/`](../java/spring/05_testing/README.md)에 별도로 있고, 두 묶음은 같은 시스템을 양쪽에서 검증하는 보완 관계다.

Django·FastAPI 같은 웹 프레임워크 문서는 채워지면 별도 하위 폴더(예: `web/fastapi/`)로 분리한다. 데이터 분석·과학 계산 영역은 5개 이상 쌓이면 `data/` 하위 폴더로 옮긴다.
