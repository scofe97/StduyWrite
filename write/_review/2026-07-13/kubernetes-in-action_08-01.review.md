---
title: "command·args와 환경변수 — 복습 회차 1"
tags: [review, kubernetes, command, args, environment-variable]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/08-01.command·args와 환경변수.md"
round: 1
round_date: 2026-07-13
prev_round_date: 2026-07-10
next_round_date: 2026-07-16
quality: 3
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-07-13
---

# command·args와 환경변수 — 복습 회차 1

> 원본: [command·args와 환경변수](../../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md)
> 회차 1 · 2026-07-13 · 이전 학습: 2026-07-10

## 학습 목표

Dockerfile의 ENTRYPOINT·CMD와 Pod의 command·args를 대응하고, Kubernetes와 셸의 환경변수 확장을 구분하며, exec 유무에 따른 PID 1과 종료 신호 전달 차이를 설명합니다.

## 결과

| 질문 축 | 점수 | 확인 결과 |
|---------|------|-----------|
| 정의 | 4/5 | ENTRYPOINT-command, CMD-args 대응과 생략 시 이미지 기본값 적용을 설명했습니다. |
| 메커니즘 | 4/5 | 앞서 선언된 env만 확장되고 나머지는 참조 표현으로 남음을 설명했습니다. |
| 확장 주체 | 3/5 | Kubernetes와 셸의 확장 시점은 구분했으나 exec의 프로세스 교체 설명이 빠졌습니다. |
| 적용 | 3/5 | Spring Boot CLI 우선순위는 설명했으나 미정의 printenv의 종료 코드를 혼동했습니다. |
| 함정 | 3/5 | 셸이 PID 1이면 정상 종료 문제가 생김을 알았으나 신호 전달 과정을 구체화하지 못했습니다. |

**SM-2 quality**: 3

## 핵심 교정

1. Kubernetes가 해석하지 못한 `$(UNKNOWN)`은 문자열 그대로 남습니다. 반면 실행 중 존재하지 않는 변수를 `printenv UNKNOWN`으로 조회하면 출력 없이 종료 코드 1을 반환합니다.
2. `exec`는 자식 프로세스를 추가하지 않고 현재 셸을 대상 프로그램으로 교체합니다. `exec java ...`를 사용하면 JVM이 PID 1이 되어 종료 신호를 직접 받습니다.
3. Spring Boot의 커맨드라인 프로퍼티와 환경변수 충돌은 Kubernetes가 아니라 Spring Boot의 PropertySource 우선순위가 해결합니다.
4. ENTRYPOINT와 CMD의 구분 목적은 고정 실행 프로그램과 교체 가능한 기본 인자를 분리하는 것입니다.

## 실습 증거

- `args-only`: `/entrypoint.sh` 유지, 포트 9090으로 CMD 교체
- `env-expansion`: 앞선 `EARLY`만 Kubernetes가 확장하고 이미지 변수는 셸에서 확인
- `printenv UNKNOWN`: 출력 없음, 종료 코드 1
- exec 없음: PID 1은 `sh`, `sleep`의 PPID는 1
- exec 사용: PID 1은 `sleep`

## 다음 회차

quality 3을 기준으로 2026-07-16에 다시 확인합니다. 다음 회차에서는 미해결 참조와 미정의 환경변수 조회의 차이, exec의 프로세스 교체와 신호 전달을 우선 질문합니다.

## 관련 자료

- [원본 학습 문서](../../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md)
- 실습: `study/k8s_in_action/08-configuring-apps/command-env/`
