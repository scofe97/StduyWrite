---
title: Kubernetes in Action 오답 노트
tags: [kubernetes, mistakes, review]
status: in_progress
updated: 2026-07-27
---

# Kubernetes in Action 오답 노트

## 2026-07-27 — namespace를 "격리 울타리"로 봄 (정의형 인출 실패)

- **자기 답**: 07-01 회차 1에서 namespace의 정의를 "자원과 권한을 분리하기 위한 쿠버네티스의 울타리"라 답했습니다. 동기를 물었을 때도 가시성 오염과 권한 경계만 나오고 *이름 충돌*이 두 번 연속 빠졌습니다. `kubectl get pods`가 보는 대상은 "현재 컨텍스트의 namespace"로 맞혔으나 `-n`·`-A`·`set-context` 세 명령을 인출하지 못했습니다. Terminating 진단은 conditions까지 갔으나 원인을 *finalizer*로 명명하지 못했습니다.
- **정답**: namespace의 1순위 축은 **이름의 스코프**입니다 — API 오브젝트를 겹치지 않는 그룹으로 조직하는 논리 장치이고, 그래서 팀 A와 팀 B가 둘 다 `kiada-ssl`이라는 Pod를 가질 수 있습니다(§1). 권한의 스코프는 그 위에 얹힌 **두 번째** 성질이고, 경계를 집행하는 것은 namespace가 아니라 **RBAC**입니다. 원문 §4는 "namespace는 이름과 권한을 나눌 뿐, 런타임과 네트워크는 나누지 못한다"고 명시합니다 — 같은 노드면 같은 OS 커널을 공유하고 네트워크는 기본 개방입니다. Terminating의 범인은 **finalizer**이며 `NamespaceFinalizersRemaining` condition이 지목합니다.
- **원인 추정**: 뿌리는 **"리눅스 네임스페이스의 격리 이미지가 쿠버네티스 namespace로 전이된 것"** 입니다. 원문 §진입이 두 개념의 혼동을 먼저 경고하는데, 격리 프레임을 쓰면 "울타리"가 먼저 나오고 이름 스코프가 뒤로 밀립니다. 다만 *적용* 문항에서는 "권한을 namespace별로 분리"를 스스로 도출했으므로 개념 자체는 있습니다 — **정의 형태의 인출 경로만 안 뚫린 상태**입니다(시나리오형 4점 / 정의형 2점). 명령 3종과 finalizer는 이해가 아니라 노출 부족입니다.
- **참고 챕터**: 07-01 §1(이름 충돌과 권한 경계)·§3(기본 namespace 전환)·§4(격리의 실체)·§5(finalizer). 원문 §빈칸 채우기가 `--all-namespaces`·`set-context`·`-o yaml`·`finalizers`를 그대로 묻습니다. "**namespace는 이름의 스코프가 1순위, 권한은 2순위, 런타임·네트워크는 아예 아님**" 한 줄.
- **재방문 트리거**: 2026-07-30 회차 2에서 (1) namespace를 문서 안 보고 한 문장으로 정의하고 리눅스 네임스페이스와의 차이를 덧붙이기, (2) §빈칸 채우기 4칸을 먼저 채우기, (3) "Terminating에 멈췄다"에 원인 한 단어로 답하기.

## 2026-07-27 — ClusterIP를 "정류장"으로 봄 + NodePort/LoadBalancer 타입이 노드 간 전달을 정한다고 봄

- **자기 답**: 11-02 재검증에서 세 번 연속 같은 지점에 걸렸습니다. (1) 목적지/출발지 변환을 물었는데 경로("PC → LB → 노드 → 파드")만 답하고 *어느 필드가 바뀌는지*를 안 나눴습니다. (2) 목적지가 "노드 → **클러스터**(ClusterIP)"로 바뀐다고 세 번 답했습니다 — 07-20 오답 노트의 "Cluster는 ClusterIP로 치환한다"와 같은 문장. (3) "NodePort 볼 때는 다른 노드로 전송을 못 해준 것 같은데 로드밸런서는 되나?"라고 물어 *타입*이 노드 간 전달을 정한다고 봤습니다. (4) 노드 3대(A:3/B:1/C:0)인데 로드밸런서 분배를 2대로 계산해 `50/3, 50`이라 답했습니다. (5) healthCheckNodePort를 켜면 "(a)처럼 균등하게" 된다고 답해 Local의 두 대가를 하나로 뭉쳤습니다.
- **정답**: **ClusterIP는 경로상의 정류장이 아니라 규칙표의 색인**입니다. 어느 인터페이스에도 안 붙은 가상 IP라 무언가를 경유시킬 실체가 없습니다. `ClusterIP:80`과 `노드IP:30080`은 같은 파드 목록을 가리키는 **두 입구**이고, node port로 들어온 패킷의 목적지는 `172.18.0.4:30080` → `10.244.2.9:8080`으로 **곧바로** 바뀝니다. 문서 §1의 "30080 → 80 → 8080" 표기는 매핑 관계이지 경유 경로가 아닙니다. **결정은 두 번** 내려집니다 — ① 로드밸런서가 *노드*를 고름(헬스체크+균등 분배, 파드는 안 봄) ② 도착한 노드 커널이 *파드*를 고름(후보 범위 = externalTrafficPolicy). 그래서 **다른 노드로 넘길 수 있는지는 정책이 정하고 타입이 정하지 않습니다** — Cluster면 NodePort도 넘기고, Local이면 LoadBalancer도 못 넘김. A:3/B:1/C:0에 100요청이면 Local은 노드 **셋 모두**에 33씩 → 파드당 11·11·11·33(3배 어긋남) + C의 33 유실. healthCheckNodePort를 켜면 C가 빠져 50씩 → 16.7·16.7·16.7·50 — **유실만 사라지고 3배 어긋남은 남습니다**. 불균등은 "LB는 노드 단위로 나누는데 노드마다 파드 수가 다르다"에서 나오므로 노드별 파드 수를 맞춰야(DaemonSet·topologySpreadConstraints) 줄어듭니다.
- **원인 추정**: 뿌리가 **"가상 IP를 실체 있는 경유지로 상상한 것"** 하나입니다. ClusterIP를 정류장으로 보면 목적지가 그리로 바뀐다고 답하게 되고, 07-20의 SNAT/DNAT 혼동도 여기서 재발했습니다. (3)의 타입 혼동은 다른 결 — 로드밸런서가 *노드를 고르는* 1단과 커널이 *파드를 고르는* 2단을 한 층으로 뭉쳐, 1단 장치(LB)의 유무로 2단 능력(노드 간 전달)을 설명하려 한 것입니다. (5)는 "장치가 있으면 문제가 다 풀린다"는 기대 — 대가가 둘이고 장치가 하나만 푼다는 비대칭을 안 세웠습니다.
- **참고 챕터**: 11-02 §3. 이번 세션에서 문서를 보강했습니다 — SVG 3장(`11-02-dnat-snat-two-fields`, `11-02-lb-picks-node-policy-picks-pod`, `11-02-external-traffic-policy` 3열 개정) + §1에 "ClusterIP는 색인" 교정 단락 + §3에 선언/집행 분리·2단 결정·SNAT 생략 기전·장치의 효과 범위. "**Cluster=NAT 2번(목적지→파드IP, 출발지→노드IP) / Local=NAT 1번(목적지만) + 대가 둘: 유실은 healthCheckNodePort로 막고 불균등은 못 막는다**" 한 줄.
- **재방문 트리거**: 다음 복습에서 (1) 문서 안 보고 목적지·출발지 두 줄을 채우고 각 변환의 주체와 "Local에서 사라지는 줄"을 적기, (2) 노드별 파드 수를 임의로 주고 Local·Local+healthCheck 두 경우의 파드당 요청 수를 계산해 *3배 비율이 안 바뀌는 것* 확인, (3) "ClusterIP는 정류장인가 색인인가"에 한 문장으로 답하기.

## 2026-07-24 — 이름 해석(DNS)과 주소 변환(DNAT)을 한 덩어리로 봄

- **2026-07-27 보강 완료**: `_todo-11-01-보강.md`의 세 항목을 모두 처리했습니다 — 항목 2·3(네 컴포넌트 시각화, 두 단계 주소 변환 시각화)은 `11-01-service-component-responsibilities.svg`·`11-01-dns-dnat-two-stage.svg`로 이미 반영돼 있었고, 항목 1(CoreDNS 정체)은 §5에 단락을 추가했습니다 — CoreDNS는 API 오브젝트가 아니라 `kube-system`의 Deployment 애드온이고 앞단 `kube-dns` Service의 ClusterIP가 파드 `nameserver`에 들어가므로 DNS 질의도 Service 트래픽과 같은 DNAT 경로를 지납니다 + 두 갈래 위임(클러스터 도메인은 자기가 답, 외부는 업스트림 forward). TODO 파일은 삭제했습니다. 개념 자체의 재검증은 다음 복습 몫입니다.
- **자기 답**: 11-01 복습에서 세 지점이 같은 뿌리로 막혔습니다. (1) `quiz`가 ClusterIP로 풀리는 과정에서 `/etc/resolv.conf`를 **누가** 채우는지 몰라 kube-proxy를 DNS 자리에 놓았습니다. (2) 네 컴포넌트 역할 분리(§3)에서 스케줄러만 정확했고, CNI가 `resolv.conf`를 채운다고 잘못 답했으며 kube-proxy는 "흐리게만 안다"고 했습니다. (3) 요청 한 번이 파드에 닿는 전 구간에서 "Service 오브젝트가 패킷을 받아 넘긴다", "라운드로빈으로 분산"이라 답했고 **주소가 두 번 바뀐다는 걸 못 떠올렸습니다.**
- **정답**: `quiz` → 파드IP까지 주소가 **두 번** 바뀝니다. **① 이름 해석(DNS)**: `quiz`를 CoreDNS가 ClusterIP(`10.96.136.190`)로 풀어줌 — `/etc/resolv.conf`는 **kubelet**이 파드 생성 시 씀(search 접미사 + ndots:5로 짧은 이름 판정). **② 주소 변환(DNAT)**: ClusterIP는 어느 인터페이스에도 안 붙은 **가상 IP**라, **보내는 쪽 노드 커널**이 목적지를 실제 파드IP(`10.244.2.9`)로 바꿔치기함. Service는 패킷을 받는 실체가 아님 — 받는 주체가 없고, kube-proxy가 심어둔 규칙을 근거로 커널이 변환. 파드 선택은 라운드로빈이 아니라 iptables random 모듈의 **확률적 선택**(실측 13/10/7). 네 컴포넌트: **스케줄러=노드 배정 / CNI=파드IP 발급(넷 중 IP를 유일하게 *만드는* 것) / EndpointSlice 컨트롤러=ready 파드IP를 명단에 옮겨 적기 / kube-proxy=명단으로 커널에 DNAT 규칙 심는 컨트롤러(패킷을 직접 나르지 않음)**.
- **원인 추정**: "이름→IP"와 "IP→IP"를 한 덩어리로 뭉뚱그려, 두 변환의 주체(CoreDNS vs 노드 커널)와 위치(DNS 단계 vs DNAT 단계)를 구분하지 못했습니다. kube-proxy를 DNS 자리에 놓은 것, Service가 패킷을 받아 넘긴다고 본 것이 전부 이 하나에서 나왔습니다. 2026-07-20 오답 노트의 공통 뿌리 "자동으로 채워지는 것의 내부 기전"과 같은 결입니다. A-1(expose selector)만 통과한 건 그게 라벨 매칭 문제라 이 축과 무관했기 때문입니다.
- **참고 챕터**: 11-01 §5(cluster DNS·NAT가 끼는 곳)·§3(네 컴포넌트 역할 분리). 깊은 기전은 `04-05.DNS와 CoreDNS`·`01-02.K8s 패킷 여정`. "이름→ClusterIP는 CoreDNS(DNS), ClusterIP→파드IP는 노드 커널(DNAT), 주소가 두 번 바뀐다" 한 줄. (보강 TODO는 `_todo-11-01-보강.md`)
- **재방문 트리거**: 다음 복습에서 (1) `quiz → ClusterIP → 파드IP` 두 화살표를 그리고 각 화살표의 주체(CoreDNS / 노드 커널)를 손으로 적기, (2) 네 컴포넌트를 "노드 배정·IP 발급·명단·길"로 나눠 문서 안 보고 나열.

## 2026-07-20 — externalTrafficPolicy Local: SNAT 정체 + "노드는 균등, 파드는 불균등"

- **자기 답**: 11-02 Phase 4 Q2에서 "Cluster는 ClusterIP로 치환한다"고 답해 *목적지(DNAT)와 출발지(SNAT)를 혼동*했습니다. Q5(Local의 두 번째 대가 = 불균등 분산 + healthCheckNodePort)는 "그게 있나?"로 막혀 설명이 필요했습니다.
- **정답**: 노드가 받은 요청을 다른 노드 파드로 넘길 때 두 NAT이 겹칩니다. **DNAT**(목적지 `노드IP:30080`→`파드IP:8080`)는 두 정책 다 함. **SNAT/masquerade**(출발지 `클라이언트IP`→`받은 노드IP`)는 **Cluster만** 함 — 응답이 반드시 받은 노드로 되돌아오게(비대칭 경로 방지) 출발지를 위조하는 대가로 파드가 보는 Client IP가 노드 IP가 됨. **Local은 SNAT을 안 해** 원본 IP 보존, 대신 "로컬 파드로만 라우팅"이라 파드 없는 노드는 타임아웃. 불균등: LB는 **노드 단위**로 균등 분배하는데 노드마다 파드 수가 달라(A:3, B:1) 파드당 부하가 어긋남(A 파드 11% vs B 파드 33%). 타임아웃 우회는 **healthCheckNodePort**(로컬 파드 있으면 200, 없으면 503) + LB 헬스체크로 파드 없는 노드를 분배에서 제외.
- **원인 추정**: (1) NAT을 "IP를 바꾸는 것" 하나로 뭉뚱그려 목적지/출발지 방향 구분을 안 세움. (2) Local의 대가를 "타임아웃" 하나만 알고 "불균등 분산"은 노드/파드 분배 단위가 다르다는 데서 나온다는 걸 못 떠올림. 오늘 3세션 공통 약점 "자동으로 채워지는 것의 내부 기전"과 같은 결(kube-proxy가 심는 SNAT 규칙).
- **참고 챕터**: 11-02 §3(externalTrafficPolicy). 뿌리는 `02_os/networking/01-02.K8s 패킷 여정` §1.2(POSTROUTING=SNAT)·§2(kube-proxy). "Cluster=SNAT함(Client IP=노드 IP), Local=SNAT안함(원본 보존)+로컬 파드만+healthCheckNodePort로 죽은 노드 제외" 한 줄.
- **재방문 트리거**: 다음 복습에서 (1) 한 요청이 다른 노드 파드로 갈 때 DNAT·SNAT이 각각 무엇을 바꾸는지 화살표로 그리기, (2) Local에서 노드별 파드 수를 임의로 주고 파드당 트래픽 비율을 계산.

## 2026-07-20 — DNS 짧은 이름 resolve: /etc/resolv.conf의 search와 ndots

- **자기 답**: 11-01 Phase 4 Q5(짧은 이름 `http://kiada`가 어떻게 완전한 이름으로 확장돼 resolve되나 + ndots:5 역할)에서 파일 경로(`/etc/resolv.conf`)만 근접하고 "왜 생기고 어떻게 하는지 모름"으로 막혔습니다.
- **정답**: kubelet이 파드 생성 시 `/etc/resolv.conf`를 자동으로 써넣습니다. `search default.svc.cluster.local svc.cluster.local cluster.local` 줄이 짧은 이름 뒤에 접미사를 차례로 붙여 매칭될 때까지 시도(→ `kiada.default.svc.cluster.local` 매칭). `options ndots:5`는 점이 5개 미만인 이름을 상대 이름으로 보고 search 접미사를 붙이게 함(k8s 최장 FQDN이 점 5개라 그 미만은 짧은 이름 취급). CoreDNS가 A 레코드로 ClusterIP를 반환.
- **원인 추정**: resolv.conf가 "자동으로 채워지는 것"이라는 것만 알고, search/ndots라는 확장 메커니즘 내부를 안 열어봤습니다. Q2(expose selector)와 함께 "자동으로 채워지는 것의 내부 동작"에서 공통으로 막힌 패턴.
- **참고 챕터**: 11-01 §5(cluster DNS). 실습 C-2에서 `http://kiada:8080`이 실제로 resolve된 것을 관찰. "search가 접미사 붙이고, ndots:5가 짧은 이름인지 판정" 한 줄.
- **재방문 트리거**: 다음 복습에서 파드 안 `cat /etc/resolv.conf`로 search·ndots를 직접 확인하고, `kiada`가 어느 접미사로 확장되는지 손으로 추적.

## 2026-07-20 — kubectl expose의 selector 함정: 파드 라벨을 전부 가져간다

- **2026-07-24 재검증**: 힌트 없이 자답 통과. SELECTOR `app=quiz,rel=stable`과 canary 0%(등록조차 안 됨)를 모두 인출했습니다. **해결**로 봅니다.
- **자기 답**: 11-01 Phase 4 Q2(`kubectl expose pod quiz`로 만든 Service의 selector 값 + canary 배포 시 문제)에서 selector가 `app=quiz` 하나일 거라 예측했고, canary 개념은 미학습이라 문제를 못 떠올렸습니다.
- **정답**: `kubectl expose pod`는 그 파드의 라벨을 *전부* selector로 복사합니다. 파드가 `app=quiz,rel=stable`이면 selector도 `app=quiz,rel=stable` 둘 다가 됩니다(실습 출력에서 `SELECTOR app=quiz,rel=stable` 확인). 나중에 canary(`app=quiz,rel=canary`)를 배포하면 `rel`이 stable이 아니라 selector에 안 맞아 **canary가 Service에 아예 등록조차 안 됩니다**(트래픽 0%). `kubectl set selector service quiz app=quiz`로 좁혀야 canary도 포함됩니다.
- **원인 추정**: "app=quiz 하나여야 한다"는 *목표 상태*는 직관했으나, expose가 그렇게 안 해주고 라벨을 전부 가져간다는 *실제 동작*을 몰랐습니다. Service 방식 자체는 멀쩡하고 expose의 selector 복사가 canary 시나리오와 어긋나는 것.
- **참고 챕터**: 11-01 §3(kubectl expose)·§4(set selector). "expose는 파드 라벨을 전부 selector로 가져가니, canary를 받으려면 app=quiz로 좁혀라" 한 줄. (canary = 신버전을 일부 트래픽에만 흘려 검증하는 배포. k8s 기본은 파드 개수 비율로 대략 조절, 정밀 %는 L7 필요.)
- **재방문 트리거**: 다음 복습에서 `kubectl expose pod`가 만든 selector를 예측하고 `kubectl get svc -o wide`로 실제 SELECTOR와 대조. canary 파드가 왜 트래픽을 못 받는지 설명.

## 2026-07-20 — 스냅샷 복원 시 dataSourceRef.apiGroup: 왜 스냅샷만 필수인가

- **자기 답**: Phase 4 Q4(PVC 소스 vs 스냅샷 소스에서 dataSourceRef가 딱 하나 달라지는 점)에서 "모르겠다"로 막혔습니다. 이어서 "core 그룹 API인 것과 아닌 것의 차이가 뭐냐"고 물었습니다 — API 그룹 구분 자체가 흐릿했습니다.
- **정답**: 스냅샷을 소스로 쓸 때만 `apiGroup: snapshot.storage.k8s.io`를 명시해야 합니다. PVC/PV는 **core 그룹**(`apiVersion: v1`, 그룹명이 빈 문자열 `""`)이라 `apiGroup`을 생략하면 core로 해석돼 찾아지지만, VolumeSnapshot은 **named 그룹**(`snapshot.storage.k8s.io/v1`)이라 생략하면 "core 그룹의 VolumeSnapshot"을 찾다 실패합니다. core 그룹은 Pod·Service·PVC·ConfigMap 등 초기 근본 오브젝트의 예약 공간(`/api/v1/...`)이고, 그 외는 전부 `apps/v1`·`snapshot.storage.k8s.io/v1`처럼 그룹명이 붙는 named 그룹(`/apis/<group>/...`)입니다.
- **원인 추정**: 오브젝트의 `apiVersion:` 접두어가 곧 API 그룹 소속이고, "생략 = core 그룹" 규칙이라 core에 없는 오브젝트는 그룹 명시가 필수라는 연결을 안 짚었습니다.
- **참고 챕터**: 10-03 §3(스냅샷에서 PV 복원). "apiGroup 생략 = core 그룹을 뒤져라, 스냅샷은 core에 없으니 그룹명 명시 필수" 한 줄.
- **재방문 트리거**: 다음 복습에서 (1) PVC 소스 복제 YAML과 스냅샷 소스 복원 YAML의 dataSourceRef를 나란히 쓰고 차이를 설명, (2) `kubectl api-resources` 출력에서 core(`v1`)와 named 그룹 오브젝트를 각각 두 개씩 골라내기.

## 2026-07-20 — ephemeral vs emptyDir: PV 기능 상속을 스스로 못 떠올림

- **자기 답**: Phase 4 Q5(emptyDir가 못 하는데 ephemeral은 되는 것 3가지+와 그 능력의 출처)에서 힌트 후에도 "모르겠다"로 막혔습니다. Phase 1에서도 4개 중 1개(data source)만 맞혔던 지점입니다.
- **정답**: ephemeral이 되는 것 — (1) 스냅샷·복원, (2) data source 초기화, (3) 고정 크기 제한(파드 초과 불가), (4) 리사이즈. 이 능력들은 전부 **ephemeral 볼륨으로 만들어지는 게 "정상 PV"이기 때문**에 나옵니다(실습에서 파드 생성 시 진짜 PVC·PV가 자동 생성돼 바인딩되는 것을 관찰). emptyDir는 노드 로컬 디렉터리라 이 PV 기능이 하나도 없습니다.
- **원인 추정**: 개별 사실(스냅샷·리사이즈)은 알지만, "ephemeral = 정상 PV → PV의 모든 기능을 물려받음"이라는 *상속(transfer)* 프레임을 못 세웠습니다. Q4(apiGroup)와 함께 "배운 것을 다른 맥락에 적용"에서 공통으로 막힌 패턴.
- **참고 챕터**: 10-03 §5. "ephemeral은 정상 PV라 스냅샷·data source·고정크기·리사이즈를 물려받고, emptyDir는 그냥 노드 디렉터리" 한 줄.
- **재방문 트리거**: 다음 복습에서 emptyDir와 ephemeral 각각 되는 것/안 되는 것을 표 없이 나열하고, "왜 ephemeral만 되나"를 한 문장(정상 PV)으로 답.

## 2026-07-14 — field selector와 fieldRef의 혼동: 같은 "field"인데 다른 메커니즘

- **자기 답**: Downward API의 `valueFrom.fieldRef.fieldPath`를 보고 "이게 07-03의 field selector 검색과 같은 것이냐"고 물었습니다 — 이름이 둘 다 field라 같은 개념으로 묶어 생각했습니다.
- **정답**: 완전히 다른 메커니즘입니다. **field selector**(07-03)는 클러스터 *바깥*에서 여러 오브젝트를 *필터링·조회*하는 검색(`kubectl get pods --field-selector spec.nodeName=X` → 조건 맞는 Pod 리스트)이고, **fieldRef**(08-03 Downward API)는 클러스터 *안*에서 한 Pod가 *자기 값 하나를 컨테이너에 주입*하는 참조(`valueFrom.fieldRef.fieldPath: spec.nodeName` → 그 값을 env/파일로)입니다. 방향이 정반대입니다 — 하나는 밖에서 안으로 걸러 보고, 하나는 안에서 자기 값을 꺼내 넣습니다.
- **원인 추정**: `spec.nodeName` 같은 필드 경로 문자열을 양쪽이 공유하는 것을 보고, "재료가 같으니 도구도 같다"고 묶었습니다. 재료(필드 경로)는 공유하지만 도구(검색 필터 vs 주입 참조)는 다릅니다.
- **참고 챕터**: 07-03 §1(field selector)·08-03 §5(fieldRef). "field selector = 밖에서 오브젝트 골라내는 검색, fieldRef = 안에서 자기 값 꺼내 넣는 주입" 한 줄로 정리함.
- **재방문 트리거**: 2026-07-16 복습에서 `spec.nodeName`을 field selector와 fieldRef 각각의 문법으로 쓰고, 두 결과(Pod 리스트 vs env 값 하나)가 어떻게 다른지 말로 설명.

## 2026-07-14 — Secret 주입: env vs 볼륨 트레이드오프를 스스로 못 떠올림

- **자기 답**: Phase 4 Q5(볼륨이 더 안전한데 env를 왜 안 없애나)에서 "모르겠다"로 막혔고, 힌트를 받은 뒤에야 "env가 코드상 편하고 Spring relaxed binding으로 자동 처리된다"에 도달했습니다.
- **정답**: env의 장점은 (1) 앱 코드가 단순(`getenv` 한 줄 vs 파일 열기·읽기·파싱), (2) 12-factor 관례로 프레임워크가 env를 기본 기대(Spring은 `SPRING_DATASOURCE_PASSWORD` env를 relaxed binding으로 자동 매핑)입니다. 판단 기준은 "비밀값이면 볼륨(유출 표면 회피), 비밀 아니면 env(편의)". 이는 Q3에서 본 "Downward API(POD_IP 등 공개 정보)는 env여도 되지만 Secret은 볼륨이 낫다"와 같은 판단 축입니다.
- **원인 추정**: env의 *위험*(Q3에서 답한 로그·자식 상속)은 알았지만, 그 반대편인 *편의*를 장점으로 뒤집어 세우지 못했습니다. 한 축(위험)만 보고 트레이드오프의 다른 축(편의)을 못 떠올린 것.
- **참고 챕터**: 08-03 §3(env 주입 경고)·Spring 관점(configtree). "편의는 env, 안전은 볼륨" 한 줄.
- **재방문 트리거**: 2026-07-16 복습에서 "DB 비밀번호"와 "로그 레벨"을 각각 어느 경로로 주입할지와 그 이유를 답. 두 값의 성격(비밀/공개)으로 갈리는 것을 설명.

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
