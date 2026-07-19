---
title: "ConfigMap으로 설정 분리하기 — 복습 회차 1"
tags: [review, kubernetes, configmap]
status: in_progress
source: "../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap으로 설정 분리하기.md"
round: 1
round_date: 2026-07-14
prev_round_date: null
next_round_date: 2026-07-17
quality: 3
metacog:
  interview: null
  speak_without_diagram: null
  apply_to_other_env: null
updated: 2026-07-14
---

# ConfigMap으로 설정 분리하기 — 복습 회차 1

> 원본: [ConfigMap으로 설정 분리하기](../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md)
> 회차 1 · 2026-07-14 · 이전 회차: 첫 회차

## 학습 목표

ConfigMap의 생성 방식을 구분하고, 선택·전체 환경변수 주입과 누락 시 상태를 설명하며, 환경변수·볼륨·immutable 설정의 갱신 전략을 판단합니다.

## 결과

| 질문 축 | 점수 | 확인 결과 |
|---------|------|-----------|
| 동기 | 4/5 | 같은 이미지와 Pod 매니페스트를 유지하고 환경별 설정만 분리하는 이유를 설명했습니다. |
| 생성 구조 | 2/5 | `--from-file`과 `--from-env-file`을 처음에는 원문과 치환의 차이로 혼동했으나 재인출에서 교정했습니다. |
| 주입 방식 | 3/5 | 단일 키에는 `configMapKeyRef`를 선택했지만 환경변수 이름 변경과 `envFrom`의 전체 주입 차이를 바로 설명하지 못했습니다. |
| 누락 상태 | 3/5 | optional의 실행 여부는 알았지만 Pod phase와 컨테이너 waiting reason을 구분하지 못했습니다. |
| 갱신 | 3/5 | 기존 Pod와 새 Pod의 값이 달라짐은 예측했으나 롤링 교체와 `subPath` 예외를 처음에는 설명하지 못했습니다. |

**SM-2 quality**: 3

## 핵심 교정

1. `--from-file`은 파일명 하나를 키로, 파일 전체를 값으로 저장합니다. `--from-env-file`은 각 `KEY=value` 줄을 별도 엔트리로 만들며 값을 치환하지 않습니다.
2. `configMapKeyRef`는 한 키를 선택하고 환경변수 이름을 바꿀 수 있습니다. `envFrom`은 모든 키를 원래 이름으로 가져옵니다.
3. 필수 ConfigMap이 없으면 Pod phase는 `Pending`이고 참조 컨테이너의 waiting reason은 `CreateContainerConfigError`입니다.
4. 환경변수는 Pod 롤링 교체로 통일합니다. 일반 ConfigMap 볼륨은 kubelet 동기화 후 갱신되지만 `subPath` 마운트는 갱신되지 않습니다.

## 실습 증거

- 필수 참조 Pod: 독립 컨테이너는 Running, 참조 컨테이너는 `CreateContainerConfigError`
- optional Pod: Running, 누락된 환경변수의 `printenv` 종료 코드 1
- 환경변수 갱신: 기존 Pod 둘은 `info`, 새 Pod 하나는 `debug`
- 롤링 교체: 새 ReplicaSet의 Pod 셋이 모두 `debug`
- 볼륨 갱신: 일반 마운트는 `after`, `subPath`는 `before`
- immutable 수정: API 서버가 `field is immutable`로 거부

## 다음 회차

quality 3을 기준으로 2026-07-17에 다시 확인합니다. 다음 회차에서는 생성 방식별 키 구조, Pod phase와 컨테이너 waiting reason, 일반 볼륨과 `subPath`의 갱신 차이를 우선 질문합니다.

## 관련 자료

- [원본 학습 문서](../../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md)
- 실습: `study/k8s_in_action/08-configuring-apps/configmap/`
