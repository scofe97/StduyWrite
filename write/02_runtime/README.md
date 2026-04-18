---
title: 02_runtime MOC
tags: [moc, runtime, jvm]
status: final
related: []
updated: 2026-04-19
---

# 02_runtime
---
> 언어 경계를 넘는 런타임 지식을 모은다. JVM, GC, 메모리 모델, 동시성 원리.

## 하위

- [jvm/](jvm/) — JDK 구조, 바이트코드, GC 알고리즘, JIT

## 경계 기준

Java 언어 자체의 문법·표준 API는 `01_language/java/`다. 여기는 "어떤 언어든 JVM 위에서 돌면 영향받는 내용"을 둔다. 예를 들어 `Stop-the-world` 의 메커니즘은 Kotlin에서도 동일하므로 여기에 속한다.
