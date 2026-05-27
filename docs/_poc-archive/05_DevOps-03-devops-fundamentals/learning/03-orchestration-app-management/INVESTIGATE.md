# Ch03. 오케스트레이션과 앱 관리 — 탐구 질문

탐구 질문은 단순 복습이 아니라 LEARN.md에서 다루지 않은 깊이를 파고드는 연습이다.
각 질문에 답하기 전에 직접 조사하고, 경험을 통해 검증할 것.

---

## Q1. Docker Compose vs Kubernetes — 언제 전환하는가?

Docker Compose는 단일 호스트에서만 동작하고, Kubernetes는 다중 호스트를 지원한다.
그러나 "다중 서버가 필요해지면 K8s로"라는 단순한 기준은 실무에서 충분하지 않다.

조사할 것:
- Compose의 `--scale` 옵션은 왜 프로덕션에 부적합한가? (로드밸런서 설정과의 연관성)
- Docker Swarm은 K8s의 대안이 될 수 있는가? 왜 업계에서 채택률이 낮아졌는가?
- "10개 서비스 이하면 Compose"라는 기준은 어디서 왔으며, 실제로 적절한 기준인가?
- 팀 규모(엔지니어 수)와 오케스트레이터 선택의 상관관계를 조사하라

검증 방법: 실제로 Compose로 운영 중인 서비스를 K8s로 마이그레이션한 사례를 찾아 전환 비용을 분석한다.

---

## Q2. K8s Deployment 롤링 업데이트 — 실패 시 무슨 일이 일어나는가?

LEARN.md에서 `maxSurge`와 `maxUnavailable`로 롤링 업데이트를 구성했다.
그러나 새 버전이 배포됐는데 readinessProbe가 계속 실패하면 어떻게 되는가?

조사할 것:
- `kubectl rollout status`가 중간에 hang되는 조건은 무엇인가?
- `.spec.progressDeadlineSeconds`의 기본값은 얼마이며, 초과 시 어떤 상태가 되는가?
- `kubectl rollout undo`는 어디까지 되돌리는가? 이전 ReplicaSet이 얼마나 보존되는가?
- 카나리(Canary) 배포를 K8s 기본 기능으로 구현하려면 어떤 한계가 있고, Argo Rollouts는 이를 어떻게 해결하는가?

검증 방법: `minReadySeconds`를 크게 설정하고 의도적으로 실패하는 이미지를 배포해서 K8s의 롤백 동작을 직접 관찰한다.

---

## Q3. HPA 메트릭 설계 — CPU 70%가 항상 올바른 기준인가?

LEARN.md의 HPA는 CPU 70%를 기준으로 스케일링한다.
그러나 CPU 사용률이 낮아도 응답 속도가 느린 상황(DB 병목, 네트워크 지연)에서는 CPU 기반 스케일링이 무의미하다.

조사할 것:
- Custom Metrics API와 External Metrics API의 차이는 무엇인가?
- Prometheus + KEDA(Kubernetes Event-Driven Autoscaler)로 HTTP 요청 수 기반 스케일링을 어떻게 구현하는가?
- HPA와 VPA(Vertical Pod Autoscaler)를 함께 사용할 때의 충돌 문제는 무엇인가?
- `requests.cpu`를 정확히 설정하지 않으면 HPA의 `averageUtilization` 계산이 왜 깨지는가?

검증 방법: `kubectl top pods`로 실제 CPU 사용률을 확인하고, HPA의 `TARGETS` 컬럼 값이 어떻게 계산되는지 수식으로 도출한다.

---

## Q4. Serverless Cold Start — 수백ms 지연이 실제 문제인가?

AWS Lambda의 Cold Start는 Node.js 기준 200~800ms, Java(JVM) 기준 1~5초가 걸릴 수 있다.
그런데 모든 서비스에서 이것이 문제인가? 대응책이 실제로 효과가 있는가?

조사할 것:
- Provisioned Concurrency와 일반 Lambda의 비용 차이를 계산하라. 어느 시점에 EC2가 더 저렴해지는가?
- Lambda SnapStart(Java)는 어떤 원리로 Cold Start를 줄이는가? 모든 JVM 기반 앱에 적용 가능한가?
- Cold Start가 문제되는 유스케이스(동기 API)와 문제되지 않는 유스케이스(비동기 이벤트 처리)를 구분하라
- Lambda의 실행 환경이 "재사용"되는 시간은 얼마나 되는가? — 워밍 전략의 근거가 되는 데이터

검증 방법: AWS X-Ray를 사용해서 실제 Lambda 호출의 Init Duration을 측정하고, 10분 간격 Ping으로 워밍 효과를 비교한다.

---

## Q5. 컨테이너 오케스트레이션의 서비스 디스커버리

LEARN.md에서 K8s Service는 `api-server-svc`라는 DNS 이름을 제공한다고 설명했다.
이 DNS 기반 서비스 디스커버리는 어떻게 동작하며, 실패 시 어떻게 되는가?

조사할 것:
- CoreDNS는 K8s에서 어떤 역할을 하는가? CoreDNS가 다운되면 클러스터 전체에 어떤 영향이 생기는가?
- `ClusterIP: None`인 Headless Service는 일반 Service와 무엇이 다르며, StatefulSet과 함께 쓰는 이유는?
- Consul이나 Eureka 같은 별도 서비스 레지스트리가 K8s 내에서도 필요한 경우는 언제인가?
- `ndots:5` DNS 설정이 K8s 파드의 외부 DNS 쿼리 성능에 미치는 영향과 튜닝 방법은?

검증 방법: `kubectl exec`로 파드 내에서 `nslookup api-server-svc.production.svc.cluster.local`을 실행해서 DNS 응답을 직접 확인하고, CoreDNS 파드의 로그로 쿼리 흐름을 추적한다.

---

## Q6. 하이브리드 아키텍처 — K8s와 Serverless를 함께 쓰는 설계

실제 프로덕션 시스템은 K8s만 쓰거나 Serverless만 쓰지 않는다.
API 서버는 K8s에서 상시 실행하고, 이미지 처리나 알림 발송은 Lambda로 처리하는 패턴이 흔하다.

조사할 것:
- K8s 파드에서 AWS Lambda를 트리거하는 방법은 무엇인가? (SDK 직접 호출 vs EventBridge vs SQS)
- KEDA를 사용해서 SQS 메시지 수에 따라 K8s 워크로드를 스케일링하는 패턴을 조사하라
- K8s 워크로드와 Lambda 함수가 같은 VPC 내에서 통신할 때 네트워크 설정(VPC, 서브넷, 보안 그룹)에서 주의할 점은?
- AWS App Runner, Google Cloud Run, Azure Container Apps는 K8s와 Serverless의 중간 어디쯤 위치하는가? 트레이드오프는?

검증 방법: K8s Job에서 SQS에 메시지를 발행하고, Lambda가 트리거되어 처리하는 간단한 파이프라인을 구현해서 지연 시간과 오류 처리를 측정한다.

---

## 📌 탐구 기록 방법

각 질문을 탐구한 후 다음 형식으로 기록한다:

```
## Q{번호} 탐구 결과
- 조사 날짜: YYYY-MM-DD
- 핵심 발견: (3줄 이내)
- 예상과 달랐던 점:
- 추가 질문:
- 참고 자료:
```

탐구는 문서를 읽는 것으로 끝내지 않는다. 직접 실행하고 측정한 결과가 있어야 진짜 학습이다.
