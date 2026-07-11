---
title: 02_configuration — 설정
tags: [moc, kubernetes, configmap, secret, resource-management]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 02_configuration — 설정

> 애플리케이션에 설정과 자원 한도를 주입하는 방법을 봅니다. ConfigMap·Secret으로 설정을 분리하고, Requests/Limits로 자원을 통제합니다.



## 문서 목록
> 공식 concepts의 Configuration에 대응합니다. 파일 번호(`02-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 02-01 | [K8s 환경변수와 Spring 설정 주입](02-01.K8s%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EC%99%80%20Spring%20%EC%84%A4%EC%A0%95%20%EC%A3%BC%EC%9E%85.md) | ConfigMap 환경변수가 Spring `application.yml`에 어떻게 적용되는지, 설정 주입의 두 세계를 잇습니다. |
| 02-02 | [자원 관리](02-02.%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC.md) | Requests/Limits와 QoS로 안정성을 어떻게 확보하는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
