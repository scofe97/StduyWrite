---
title: OverlayFS 와 idmapped mount — Netflix 사례
tags: [linux, overlayfs, user-namespace, idmap, mount, kubernetes, containerd, case-study]
status: final
source:
  - 플레이빌더 카이 강의 Ch-05 OverlayFS lowerdir Mount
  - https://netflixtechblog.com/mount-mayhem-at-netflix-scaling-containers-on-modern-cpus-f3b09b68beac
  - https://github.com/containerd/containerd/pull/12092
  - https://man7.org/linux/man-pages/man2/mount_setattr.2.html
  - https://docs.kernel.org/filesystems/overlayfs.html
  - https://docs.kernel.org/filesystems/idmappings.html
  - https://containerd.io/docs/2.1/user-namespaces/readme/
related:
  - ../../book/learning-modern-linux/05-01.모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다.md
  - ../../book/learning-modern-linux/06-02.컨테이너의 새로움은 재료가 아니라 조합에 있다.md
  - ./01-02.mount propagation.md
  - ../../../08_cloud/book/container-security/04-02.나머지 namespace와 호스트에서 본 컨테이너.md
  - ../../../08_cloud/book/container-security/06-01.컨테이너 이미지 해부 — 두 부분과 층과 식별자.md
updated: 2026-11-16
---
# OverlayFS 와 idmapped mount — Netflix 사례
---
> Netflix 는 컨테이너마다 사용자 ID 구간을 나누려고 idmapped mount(마운트 단위로 파일 소유자 ID 를 바꿔 보이게 하는 커널 기능)를 썼다. 레이어 50개 컨테이너 100개를 동시에 띄우자 마운트 연산 20,200회가 커널의 전역 마운트 락에 몰려 노드가 30초 넘게 멈췄고 부모 디렉터리를 한 번만 idmap 하는 containerd 수정으로 풀었다.[^netflix]

## 학습 목표와 범위

> 보안 격리 한 겹이 마운트 호출 수와 락 경합을 거쳐 노드 정체로 번지는 인과를 따라가고 수정이 호출 수를 어떻게 떼어 놓는지 설명한다. 하드웨어 일반론과 containerd 내부 구현은 다루지 않는다.

1. user namespace 만으로 부족해서 idmapped mount 가 필요해지는 이유와, 그 대신 치르는 비용을 설명한다.
2. 레이어 50개 컨테이너 100개의 마운트 연산 수를 `100 × 2 × (1 + 50 + 50)` 으로 직접 계산한다.
3. 전역 마운트 락에서 스핀이 길어지는 과정과, 같은 부하에서 CPU 구조마다 결과가 갈린 이유를 설명한다.
4. 수정이 호출 수를 레이어 수와 무관하게 만드는 원리를 설명하고 이 문서가 확인하지 못한 주장을 구분한다.

원글 본문을 직접 열지 못해 2차 요약으로 읽은 항목에는 "2차 요약" 이라고 적었다.



## 1. 증상과 장애 환경

> 장애는 이미지 레이어가 50개 이상인 컨테이너를 r5.metal 에서 약 100개 동시에 띄울 때 나타났다. 동시 기동 수가 약 20개 이하면 모든 플랫폼이 비슷하게 동작했다.[^netflix]

마운트 테이블을 읽는 데 30초 넘게 걸렸다. 단순한 헬스 체크가 30초 만에 타임아웃됐다. systemd 와 containerd 도 마운트 이벤트를 처리하느라 멈췄고 kubelet 은 containerd 와 통신하다 타임아웃을 냈다.[^netflix] 겉으로는 컨테이너 기동 지연이지만 호스트 OS 자체가 느려진 장애다.

노드가 NotReady 로 바뀌었는지, PLEG(kubelet 이 컨테이너 상태를 점검하는 모듈)가 응답을 못 했는지는 원글에 없다. 이 문서의 이전 판이 적은 "5단계로 번진 나비 효과" 중 그 두 단계는 추정이라 지웠다.



## 2. ID 매핑과 idmapped mount

> user namespace 는 컨테이너의 root 를 호스트의 일반 UID 로 바꾼다. 그런데 이미지 레이어 파일의 소유자를 그 UID 로 보이게 하려면 파일을 chown 하거나 마운트마다 매핑해야 하고 Netflix 는 뒤쪽을 택했다.

컨테이너 안에서 UID 0(root)으로 도는 프로세스가 탈출했을 때, 호스트에서도 UID 0 이면 호스트 전체가 위험하다. user namespace 는 컨테이너 내부 UID 0 을 호스트의 높은 UID 로 대응시켜 이 위험을 낮춘다. 강의의 예시에서는 컨테이너마다 65,536개 구간을 따로 준다.

| 컨테이너 | 내부 UID | 호스트 UID 범위 |
|---|---|---|
| A | 0 | 100000 ~ 165535 |
| B | 0 | 165536 ~ 231071 |

이 구간 안에서 A 가 탈출해도 호스트의 일반 사용자 권한이고 B 의 파일은 소유자 구간이 달라 건드릴 수 없다. 이전에는 컨테이너가 호스트와 같은 UID 풀(예시에서는 UID 1000)을 공유해 한 컨테이너가 뚫리면 다른 컨테이너의 파일까지 닿았다. 2차 요약에 따르면 Netflix 는 이 무렵 virtual kubelet + Docker 에서 kubelet + containerd 로 옮겼다.

### chown 과 idmapped mount

문제는 이미지 레이어 파일이 root(UID 0) 소유로 저장되어 있다는 점이다. 컨테이너가 자기 UID 0 으로 읽으려면 그 파일이 호스트의 100000번 소유로 보여야 한다. 방법은 둘이다.

- 파일을 재귀 chown 한다. 커널 문서는 소유권을 전역적이고 영구적으로 바꾸므로 "grave implications" 가 있다고 쓴다. containerd 도 이 경로를 `slow_chown` 이라 부르며 명시적으로 동의해야 쓰게 한다.[^cd]
- 마운트마다 ID 를 매핑한다. 커널 문서는 이를 같은 dentry 집합을 마운트마다 다른 소유권으로 노출하는 기능이라고 설명한다.[^idmap] `mount_setattr(2)` 의 `MOUNT_ATTR_IDMAP` 이 매핑을 마운트에 붙이고 파일시스템의 소유권은 그대로 남는다.[^man]

OverlayFS 가 idmapped 마운트를 지원하는 것은 Linux 5.19 부터다.[^man] 매핑이 마운트 단위라서 lowerdir 레이어마다 따로 마운트를 만들어 매핑해야 한다. 이 구조가 다음 절의 호출 수를 만든다.



## 3. 마운트 호출이 쌓이는 과정

> 레이어 50개 컨테이너 하나가 101회, containerd 가 이를 두 번 수행해 202회, 100개를 동시에 띄우면 20,200회다. 호출 수는 레이어 수와 컨테이너 수의 곱으로 자란다.

레이어 50개 이미지는 OverlayFS 의 읽기 전용 층(lowerdir)이 50개라서 컨테이너 하나를 띄울 때마다 마운트 연산이 쌓인다. OverlayFS 는 lowerdir 여러 개와 쓰기 가능한 층 하나(upperdir)를 겹쳐 하나의 디렉터리로 보이게 한다. 작업용 디렉터리 workdir 은 upperdir 와 같은 파일시스템에 있어야 한다. 겹쳐 보이는 결과가 컨테이너의 `/` 가 되며 커널 문서는 이를 merged directory 라고 부른다.[^ovl] 이미지 레이어가 어떻게 따로 저장되는지는 [컨테이너 이미지 해부](../../../08_cloud/book/container-security/06-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%9D%B4%EB%AF%B8%EC%A7%80%20%ED%95%B4%EB%B6%80%20%E2%80%94%20%EB%91%90%20%EB%B6%80%EB%B6%84%EA%B3%BC%20%EC%B8%B5%EA%B3%BC%20%EC%8B%9D%EB%B3%84%EC%9E%90.md)에 정리했다.

![컨테이너 하나가 뜰 때 쌓이는 마운트 호출 — 기존은 101회에서 202회, 20,200회로 늘고, 변경 후는 레이어 수와 무관하다](./_assets/OverlayFS%20%EC%99%80%20idmapped%20mount%20%E2%80%94%20Netflix%20%EC%82%AC%EB%A1%80.mount-calls.svg)

위 줄이 기존 방식이다. 레이어마다 idmapped bind mount 를 하나씩 만든다. 그 50개를 lowerdir 로 삼아 overlay 를 한 번 마운트한다. 이어서 임시 마운트 50개를 해제한다. 원글은 이 합계를 `100 × 2 × (1 + 50 + 50) = 20,200` 으로 계산한다. 레이어마다 `open_tree()`, `mount_setattr()`, `move_mount()` 가 불리므로 시스템 콜 수는 이보다 더 크다.[^netflix]

"두 번 수행" 은 containerd 가 이 과정을 컨테이너당 두 번 돈다는 뜻이다. 2차 요약은 한 번은 이미지의 사용자 정보를 읽으려는 것이고 한 번은 실제 루트 파일시스템을 만드는 것이라고 설명한다.



## 4. 전역 마운트 락 병목

> 마운트 테이블은 시스템 전역 자원이라 락 하나로 보호된다. 20,200회의 갱신이 몰리면 테이블을 읽는 쪽이 락이 풀리길 스핀하며 기다리고 헬스 체크까지 같이 멈춘다.

원글이 짚은 병목은 커널 VFS 의 전역 마운트 락이다. CPU 의 핫패스는 `path_init()` 안의 스핀 루프였다. 이 루프는 시퀀스 락을 기다렸고 실행 명령은 대부분 `pause` 였다.[^netflix] 시퀀스 락은 값이 바뀌는 동안 읽기를 재시도하게 하는 락이다.

CPU 가 어디서 멈추는지 분류하는 Top-down 분석(TMA)으로 보면 파이프라인 슬롯의 95.5% 가 경합 접근으로 막혀 있었다. 그중 57% 는 false sharing 이었다.

스핀은 락이 짧게 잡힐 때 싸다. 스레드를 재우고 깨우는 문맥 교환 비용이 락을 쥐는 시간보다 크면 기다리는 편이 낫기 때문이다. 마운트 갱신은 원래 짧은 작업이라 커널이 이렇게 설계했다. 그런데 20,200회의 갱신이 연달아 락을 쥐면 읽는 쪽은 짧은 갱신 하나를 기다리는 것이 아니라 갱신 행렬이 끝나기를 기다린다. 이 풀이는 시퀀스 락의 일반 동작에서 이은 것이고 원글은 이렇게 설명하지 않았다.

그래서 마운트와 무관한 경로도 같이 느려진다. 경로 탐색이 이 락을 거치기 때문이다. 헬스 체크, containerd 통신, systemd 의 마운트 이벤트 처리가 모두 같은 자리에서 기다렸다.



## 5. CPU 구조별 차이

> 같은 부하에서 r5.metal 은 약 100개 부근에서 실패하기 시작했고 단일 소켓인 m7i 와 m7a 는 더 버텼다. 소켓 수, 하이퍼스레딩, 캐시 구조가 락 경합을 증폭하는 정도를 갈랐다.

| 인스턴스 | 구조 | 원글의 관찰 |
|---|---|---|
| r5.metal | Intel 5세대, 2소켓·다중 NUMA, 48코어 96 vCPU[^aws] | 동시 기동 약 100개 부근에서 실패 |
| m7i.metal-24xl | Intel 7세대, 1소켓·1 NUMA | 지연 감소, 성공률 증가. 하이퍼스레딩을 끄면 20~30% 추가 개선 |
| m7a.24xlarge | AMD 7세대, 1소켓·1 NUMA, 칩렛 | 확장성이 가장 일관되고 실패율이 가장 낮음 |

2소켓 인스턴스(48xl)가 1소켓(24xl)보다 실패가 빨랐다는 대조도 원글에 있다. 코어 수는 원글이 적지 않아 AWS 사양 표에서 가져왔다.

### NUMA

NUMA(Non-Uniform Memory Access)는 소켓마다 로컬 메모리가 따로 있어 다른 소켓의 메모리에 닿으려면 인터커넥트를 지나야 하는 구조다. 락 변수는 한 소켓의 메모리에 있으므로 다른 소켓의 코어가 그것을 확인할 때마다 소켓 간 원자 연산 일관성 비용이 든다. 스핀 대기가 많을수록 이 비용이 누적된다.

### 하이퍼스레딩

하이퍼스레딩은 물리 코어 하나를 논리 CPU 둘로 보이게 하는 기능이다. 두 논리 CPU 는 실행 유닛과 캐시를 나눠 쓰므로 한쪽이 스핀으로 자원을 쥐면 다른 쪽 락 획득도 늦어진다. 원글에서 m7i 의 하이퍼스레딩을 끄자 기동 지연이 20~30% 줄었다.

### 캐시 구조

LLC 는 코어들이 마지막으로 공유하는 캐시(Last Level Cache)다. 원글은 두 구조를 비교한다. Intel 메시에서는 중앙의 요청 큐가 병목이 될 수 있다. AMD 칩렛은 코어 묶음인 CCX 와 Infinity Fabric 으로 경합이 여러 도메인에 나뉜다. 2차 요약은 m7i 와 m7a 사이에 약 20% 성능 차이가 났다고 전한다. 이전 판은 "R5 는 단일 LLC, M7i·M7a 는 CCX 분산형" 이라고 적었으나 m7i 는 Intel 이라 CCX 구조를 갖지 않는다.

원글의 임시 대응은 영향받는 워크로드를 더 잘 확장되는 CPU 구조로 보내는 것이었다. 호출 수 자체를 줄이는 것이 근본 해결이다.



## 6. 부모 디렉터리 한 번 idmap

> 레이어마다 idmap 하는 대신 레이어들의 공통 부모 디렉터리를 한 번 재귀적으로 idmap 하면 컨테이너당 마운트 연산이 레이어 수 n 에 비례하는 O(n) 에서 O(1) 로 줄어든다.

수정은 containerd PR #12092 "Only idmap once per overlayfs, not per layer" 다. 작성자는 컨테이너 100개, 레이어 50개에서 `100 * 50 (5000)` 번의 bind mount 가 `100` 번으로 줄어든다고 적었다. containerd 와 shim 이 모두 이 일을 하므로 실제로는 두 배라고 덧붙였다. 2025년 8월 17일 main 에 병합됐고 2.0 과 2.1 로 백포트 PR 이 올라갔다.[^pr]

원글은 다른 방법도 소개한다. `fsconfig()` 의 lowerdir+ 로 idmap 된 lowerdir 을 fd 로 넘기는 방식인데 최신 커널이 필요해 택하지 않았다. 부모 디렉터리 방식은 더 많은 사용자에게 도움이 된다는 이유로 골랐다.[^netflix]

원글은 수정 뒤 수치를 싣지 않는다. 플레임그래프에서 마운트 작업이 보라색으로 강조해야 보일 만큼 사라졌다고 정성적으로만 말한다. 이전 판의 "약 600번, 33배 감소" 는 `100 × 2 × 3` 으로 짠 추정이라 지웠다.

### 커널 6.3 에 대한 판정

이전 판은 이 수정을 "Linux 6.3 에서 도입된 recursive bind mount" 라고 썼다. 1차 자료는 이를 뒷받침하지 않는다.

- `mount_setattr(2)` 는 `AT_RECURSIVE` 와 `MOUNT_ATTR_IDMAP` 의 조합에 6.3 이라는 단서를 달지 않는다. 6.3 은 tmpfs 의 idmap 지원 시작 버전으로만 나온다.[^man]
- containerd PR 은 6.3 을 언급하지 않고 작성자의 테스트 커널은 6.5 기반이었다.[^pr]
- "6.3 에서 재귀 바인드를 도입했다" 는 문장은 Cloud Native Now 기사 필자의 서술이다.[^cnn]
- containerd 문서는 Kubernetes 1.27 이상에서 6.3 이상의 커널을 요구한다. 파드 볼륨의 모든 파일시스템이 idmap 을 지원해야 한다는 이유다.[^cd] tmpfs 가 6.3 부터라는 사실과 이으면 6.3 요구는 재귀 마운트보다 tmpfs 쪽에서 왔을 가능성이 크다. 이것은 두 문서를 이은 추론이다.



## 7. 한계와 적용 전 점검

> 원글은 한 회사의 한 하드웨어 조합 사례다. 호출 수는 계산으로 바로 확인되지만 정체가 시작되는 동시 기동 수는 CPU 구조에 따라 달라서 자기 환경에서 재야 한다.

동시 기동이 몰리는 때는 노드 부팅 직후나 일제 재배포다. 평소에는 마운트 폭주가 보이지 않으므로 일제 재시작 시나리오를 따로 시험해야 한다. 이 판단은 원글이 아니라 이 문서의 해석이다.

격리를 강하게 할수록 커널이 추적할 자원이 늘고 그 추적이 락 경합으로 모인다. user namespace 를 도입할 때는 기능 검증과 함께 이 비용을 같은 규모로 재는 것이 맞다.

아래는 도입 전에 확인할 네 가지다. 명령은 이 문서에서 직접 실행해 보지 않았다.

| 항목 | 확인 방법 |
|---|---|
| 커널 버전이 idmapped overlayfs 요건(5.19 이상, Kubernetes 1.27 이상은 6.3 이상)을 넘는가 | `uname -r` |
| 이미지 평균 레이어 수 | `docker history <image>` |
| 일제 기동 때 마운트 연산 수 | `perf trace -e open_tree,mount_setattr,move_mount` |
| 소켓·NUMA 구성 | `lscpu`, `numactl --hardware` |

레이어 수를 줄이는 이미지 최적화는 수정이 없는 containerd 에서도 쓸 수 있는 대응이다. 레이어 50개는 비정상이 아니라 흔한 수치다. Dockerfile 명령이 파일시스템 레이어나 이미지 설정의 변경을 낳으므로 의존성과 빌드 단계가 많은 이미지는 쉽게 수십 개가 된다.



## 참고 자료

[^netflix]: Netflix Technology Blog, "Mount Mayhem at Netflix: Scaling Containers on Modern CPUs". <https://netflixtechblog.com/mount-mayhem-at-netflix-scaling-containers-on-modern-cpus-f3b09b68beac>
[^pr]: containerd PR #12092, "Only idmap once per overlayfs, not per layer". <https://github.com/containerd/containerd/pull/12092>
[^man]: `mount_setattr(2)` — Linux manual page. <https://man7.org/linux/man-pages/man2/mount_setattr.2.html>
[^idmap]: Idmapped Mounts, The Linux Kernel documentation. <https://docs.kernel.org/filesystems/idmappings.html>
[^ovl]: Overlay Filesystem, The Linux Kernel documentation. <https://docs.kernel.org/filesystems/overlayfs.html>
[^cd]: containerd, "Kubernetes User Namespaces". <https://containerd.io/docs/2.1/user-namespaces/readme/>
[^cnn]: Cloud Native Now, "Netflix Found a Faster Way to Load Containers". <https://cloudnativenow.com/features/netflix-found-a-faster-way-to-load-containers/>
[^aws]: AWS, "Amazon EC2 memory optimized instance types" 사양 표. <https://docs.aws.amazon.com/ec2/latest/instancetypes/mo.html>

- [모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다](../../book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md#%EC%9C%A0%EB%8B%88%EC%98%A8-%EB%A7%88%EC%9A%B4%ED%8A%B8%EC%99%80-overlayfs) — CoW 와 OverlayFS 가 컨테이너 이미지 층의 토대가 되는 과정
- [mount propagation](./01-02.mount%20propagation.md) — bind mount 가 마운트 네임스페이스 사이로 전파되는 규칙
- [나머지 namespace와 호스트에서 본 컨테이너](../../../08_cloud/book/container-security/04-02.%EB%82%98%EB%A8%B8%EC%A7%80%20namespace%EC%99%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%EC%97%90%EC%84%9C%20%EB%B3%B8%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88.md) — `unshare` 로 user namespace 를 직접 만들어 보기
- [컨테이너의 새로움은 재료가 아니라 조합에 있다](../../book/learning-modern-linux/06-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%EC%83%88%EB%A1%9C%EC%9B%80%EC%9D%80%20%EC%9E%AC%EB%A3%8C%EA%B0%80%20%EC%95%84%EB%8B%88%EB%9D%BC%20%EC%A1%B0%ED%95%A9%EC%97%90%20%EC%9E%88%EB%8B%A4.md) — 시스템 콜, namespace·cgroup 전반
