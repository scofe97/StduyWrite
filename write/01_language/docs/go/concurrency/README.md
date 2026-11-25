---
title: 01_language/docs/go/concurrency — Go 동시성 패턴 정리
tags: [moc, go, concurrency, channel]
status: draft
related:
  - ../../README.md
  - ../net-http/README.md
  - ../../../book/lgo_learning-go/README.md
updated: 2026-11-25
---

# 01_language/docs/go/concurrency — Go 동시성 패턴 정리

---

> 채널·`select`·`sync`·`sync/atomic` 로 짜는 동시성 패턴을 공식문서와 직접 돌려 본 실측으로 정리하는 섹션입니다. 코드는 go1.25.1 에서 확인합니다.

## 문서 목록

> 파일 번호가 읽기 순서입니다. 각 문서는 한 가지 패턴을 문제, 동작 원리, 대안 비교, 함정 순으로 다룹니다.

| 장 묶음 | 번호 | 제목 | 한 줄 소개 |
|---------|------|------|-----------|
| 01 채널 패턴 | 01-01 | [최신값만 전달하는 채널·drop-oldest](01-01.%EC%B5%9C%EC%8B%A0%EA%B0%92%EB%A7%8C%20%EC%A0%84%EB%8B%AC%ED%95%98%EB%8A%94%20%EC%B1%84%EB%84%90%C2%B7drop-oldest.md) | 버퍼 1 채널과 뮤텍스로 느린 소비자에게 최신 값만 넘기는 법, 락 없는 변형이 `-race` 에 안 잡히고 멈추는 실측, `sync.Cond`·`atomic.Pointer` 와의 비교 |



## 이 섹션이 다른 노트와 나누는 일

> 동시성 지식이 나뉘는 기준입니다.

Learning Go [12 장](../../../book/lgo_learning-go/README.md)의 고루틴·채널·`sync` 입문과 겹치는 부분은 해당 편으로 링크하여 연결합니다. 이 섹션은 입문 설명이 아니라 책이 다루지 않은 패턴과 그 실패 조건에 집중합니다.



## 관련 문서

> 이 폴더가 딛고 서는 이웃입니다.

- [docs MOC](../../README.md) — 언어 공식문서 정독 전체 목록
- [net/http 섹션](../net-http/README.md) — 서버 종료와 컨텍스트 전파
- [Learning Go 정독본](../../../book/lgo_learning-go/README.md) — Go 언어 문법과 표준 라이브러리 기초
