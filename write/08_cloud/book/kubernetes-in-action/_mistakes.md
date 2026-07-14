---
title: Kubernetes in Action 오답 노트
tags: [kubernetes, mistakes, review]
status: in_progress
updated: 2026-07-14
---

# Kubernetes in Action 오답 노트

## 2026-07-14 — ConfigMap 생성 방식: --from-file과 --from-env-file

- **자기 답**: 두 방식의 차이를 파일 원문과 값 치환의 차이라고 설명했습니다.
- **정답**: `--from-file`은 파일명을 키로, 파일 전체를 값으로 저장합니다. `--from-env-file`은 각 `KEY=value` 줄을 별도 엔트리로 만들며 어느 쪽도 값을 치환하지 않습니다.
- **원인 추정**: ConfigMap의 `data`가 key-value 맵이라는 구조보다 명령 옵션의 이름만 기억했습니다.
- **재방문 트리거**: 2026-07-17 복습에서 두 명령이 만드는 `data` 구조를 YAML 없이 말로 설명합니다.

## 2026-07-14 — ConfigMap 누락: Pod phase와 컨테이너 waiting reason

- **자기 답**: 필수 ConfigMap이 없으면 실행에 실패하고 optional이면 성공한다고만 설명했습니다.
- **정답**: 참조 컨테이너는 `state.waiting.reason=CreateContainerConfigError`이고 Pod phase는 `Pending`입니다. `optional: true`면 컨테이너는 실행되지만 해당 환경변수는 존재하지 않습니다.
- **원인 추정**: `kubectl get pod`의 STATUS 열을 Pod phase로 받아들여 상태 계층을 구분하지 못했습니다.
- **재방문 트리거**: 2026-07-17 복습에서 phase, container state, waiting reason을 세 줄로 구분합니다.

## 2026-07-14 — ConfigMap 볼륨: 일반 마운트와 subPath 갱신

- **자기 답**: ConfigMap을 수정했을 때 일반 볼륨과 `subPath`가 어떻게 달라지는지 설명하지 못했습니다.
- **정답**: 일반 ConfigMap 볼륨은 kubelet 동기화 후 갱신되지만 `subPath`로 마운트한 파일은 갱신되지 않습니다. 일반 파일이 바뀌어도 애플리케이션이 다시 읽어야 실제 동작이 바뀝니다.
- **원인 추정**: 볼륨의 파일 갱신과 애플리케이션 설정 재로딩을 하나의 동작으로 묶어 생각했습니다.
- **재방문 트리거**: 2026-07-17 복습에서 파일 갱신 주체와 애플리케이션 반영 주체를 각각 답합니다.

## 2026-07-14 — label selector: equality-based와 set-based의 구분

- **자기 답**: Phase 4 Q2(셀렉터 두 종류)와 Q3(nodeSelector vs nodeAffinity)에서 연달아 "모르겠다"로 막혔습니다. `in`·`OR` 조건이 된다는 것만 알았고, 이것이 두 종류 중 어디에 속하는지, AND(콤마)가 별도 종류인지 아닌지를 구분하지 못했습니다.
- **정답**: 셀렉터는 두 종류뿐입니다. **equality-based**는 등호로 끝나는 것(`=`, `!=`)이고, **set-based**는 등호로 안 되는 것 넷(`in`·`notin`·키 존재(`rel`)·키 부재(`!rel`))입니다. 콤마(`app=payment,rel=stable`)는 세 번째 종류가 아니라 두 종류를 잇는 AND 연결일 뿐입니다. `nodeSelector`는 equality-based만, `nodeAffinity`는 set-based까지 쓰는 확장이라, 둘의 차이도 결국 이 한 구분에서 나옵니다.
- **원인 추정**: `in`을 개별 기능으로만 외웠고 "등호로 되나 안 되나"라는 상위 분류 축을 잡지 못했습니다. Q2·Q3이 같은 뿌리에서 함께 막힌 것이 그 증거입니다.
- **참고 챕터**: 07-02 §4(셀렉터 두 종류)·§5(nodeSelector/nodeAffinity). 다지기 세션에서 "등호로 되면 equality, 안 되면 set-based, 콤마는 AND" 한 줄로 정리함.
- **재방문 트리거**: 2026-07-15 복습에서 다섯 요구(값 일치·여러 값 중 하나·키 존재·키 부재·값 불일치)를 셀렉터 문법으로 빈칸 채우기. set-based 4형제를 문서 안 보고 나열.

## 2026-07-13 — command·args와 환경변수: 미해결 참조와 미정의 변수 조회

- **자기 답**: 미정의 환경변수에 `printenv`를 실행하면 참조 표현이 그대로 남는다고 답했습니다.
- **정답**: Kubernetes가 확장하지 못한 `$(UNKNOWN)`은 문자열로 남지만, 실행 중 `printenv UNKNOWN`은 출력 없이 종료 코드 1을 반환합니다.
- **원인 추정**: Pod 스펙을 구성하는 시점과 컨테이너 안에서 명령을 실행하는 시점을 혼동했습니다.
- **재방문 트리거**: 2026-07-16 복습에서 두 상황을 나란히 비교합니다.

## 2026-07-13 — command·args와 환경변수: exec와 종료 신호

- **자기 답**: 셸이 PID 1이면 종료 문제가 생긴다는 방향은 알았지만 과정을 구체적으로 설명하지 못했습니다.
- **정답**: `exec`는 셸을 JVM으로 교체해 JVM이 PID 1이 되게 하며, JVM이 SIGTERM을 직접 받아 graceful shutdown을 수행할 수 있게 합니다.
- **원인 추정**: PID 1의 중요성을 결과로만 기억하고 프로세스 교체와 신호 전달 메커니즘을 연결하지 못했습니다.
- **재방문 트리거**: 2026-07-16 복습에서 `sh → java`와 `exec java`의 프로세스 트리를 말로 설명합니다.
