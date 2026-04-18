# Ch02: 설치와 배포 환경 — 심화 탐구

> LEARN.md의 개념을 더 깊이 파고드는 Q&A

---

## Q1: Docker volume을 bind mount 대신 named volume으로 써야 하는 경우는?

둘 다 데이터를 영속화하지만 관리 방식이 다르다.

**Named volume**은 Docker가 생명주기를 관리한다. `docker volume create`, `docker volume rm`으로 다루고, Docker Desktop에서도 일관되게 동작한다. 호스트 OS의 파일 권한 문제에서 비교적 자유롭다.

Linux이 아닌 macOS/Windows에서도 성능 이슈가 적은데, Docker가 내부적으로 VM 파일시스템을 사용하기 때문이다.

**Bind mount**는 호스트 경로를 직접 마운트하므로 백업 스크립트가 호스트에서 바로 접근할 수 있다. Nexus 데이터를 NFS나 특정 RAID 파티션에 저장하고 싶을 때 유용하다.

반면 UID/GID 충돌 문제가 빈번하게 발생한다. Nexus 이미지가 UID 200으로 실행되기 때문에 호스트 디렉토리도 200:200 소유여야 한다. `chown -R 200:200 /path/to/nexus-data`를 잊으면 Nexus가 시작 즉시 "Permission denied" 에러를 뱉으며 종료된다.

SELinux가 활성화된 RHEL/CentOS 환경에서는 bind mount에 `:Z` 플래그를 붙이지 않으면 SELinux가 접근을 차단한다. named volume은 Docker가 알아서 SELinux 컨텍스트를 설정하므로 이 문제에서 자유롭다.

결론적으로, 호스트 경로에 대한 특별한 요구사항이 없다면 named volume이 덜 골치 아프다. 백업이 필요하면 `docker run --rm -v nexus-data:/data -v $(pwd):/backup alpine tar czf /backup/nexus-backup.tar.gz /data` 같은 방식으로 named volume도 백업할 수 있다.

---

## Q2: JVM MaxDirectMemorySize를 힙과 별도로 설정하는 이유는?

JVM의 메모리는 크게 heap과 off-heap으로 나뉜다. `-Xmx`로 잡는 것은 heap이고, NIO에서 사용하는 DirectByteBuffer는 off-heap이다.

Nexus는 Blob Store에 접근할 때 NIO를 사용하는데, 이때 direct memory가 소비된다. 파일을 읽고 쓸 때 커널 공간과 유저 공간 사이의 복사를 줄이기 위해 direct buffer를 쓰는 것이다. 이 버퍼가 heap 밖에 할당되므로 `-Xmx`에는 포함되지 않는다.

`MaxDirectMemorySize`를 명시하지 않으면 JVM이 heap 크기와 동일하게 잡는다. heap이 2GB면 direct memory도 최대 2GB까지 쓸 수 있다는 뜻이다.

컨테이너 메모리 limit이 4GB라면 JVM heap(2GB) + direct memory(2GB) + JVM native overhead(수백 MB) = limit 초과로 OOM Kill이 발생한다.

이 OOM Kill은 JVM이 `OutOfMemoryError`를 던지기도 전에 커널이 프로세스를 죽이는 것이므로, 로그에 에러 메시지가 남지 않아 디버깅이 어렵다. `dmesg | grep -i oom`으로 커널 로그를 확인해야 비로소 원인을 알 수 있다.

그래서 heap과 direct memory의 합이 컨테이너 limit의 70~80% 이내가 되도록 설정하는 것이 안전하다. 나머지 20~30%는 JVM metaspace, thread stack, native code, JIT 컴파일러 캐시 등에 할당된다.

구체적 예시로, 컨테이너 limit이 8GB라면 `-Xmx4g -XX:MaxDirectMemorySize=2g`로 설정하여 합산 6GB, 나머지 2GB를 오버헤드용으로 확보하는 것이 권장된다.

---

## Q3: K8s에서 Nexus Pod이 재시작될 때 데이터 유실을 방지하려면?

핵심은 **PersistentVolumeClaim(PVC)**이다. StatefulSet의 `volumeClaimTemplates`로 PVC를 선언하면, Pod이 삭제되고 재생성되어도 같은 PVC에 다시 연결된다.

Deployment + PVC 조합도 가능하지만, StatefulSet이 "동일한 Pod 이름 + 동일한 PVC 바인딩"을 보장하므로 상태를 유지하는 애플리케이션에 더 적합하다.

하지만 PVC만으로 충분할까? 아니다. Nexus가 쓰기 도중 Pod이 강제 종료되면 H2 DB가 손상될 수 있다. 이를 완화하려면 두 가지를 해야 한다.

첫째, `terminationGracePeriodSeconds`를 충분히 설정한다(기본 30초 → 120초 이상). Nexus가 진행 중인 작업을 마무리하고 DB를 정상 종료할 시간을 주는 것이다.

둘째, preStop hook으로 Nexus의 graceful shutdown을 트리거한다. preStop에서 `/lifecycle/phase?phase=KERNEL_STOPPED`를 호출하거나, 단순히 `sleep 30`으로 SIGTERM 처리 시간을 확보하는 방법이 있다.

StorageClass의 `reclaimPolicy`도 반드시 확인해야 한다. `Delete` 정책이면 PVC 삭제 시 PV도 함께 삭제된다. 실수로 StatefulSet을 삭제하면 데이터가 영구 소실될 수 있다.

프로덕션에서는 `Retain` 정책을 사용하여 PV가 자동 삭제되지 않도록 보호하거나, VolumeSnapshot으로 주기적 스냅샷을 생성해두는 것이 안전하다.

---

## Q4: Reverse proxy 없이 Nexus를 직접 노출하면 생기는 문제는?

세 가지 관점에서 문제가 된다.

**보안**: Nexus 자체의 TLS 설정은 Java keystore 기반이라 인증서 갱신이 번거롭다. Let's Encrypt + certbot 자동 갱신을 쓰려면 nginx 같은 proxy가 사이에 있어야 한다.

또한 rate limiting, IP allowlist 같은 방어 기능이 Nexus에는 없다. 누군가 대량의 요청을 보내면 서버가 과부하에 빠질 수 있는데, nginx라면 `limit_req_zone`으로 간단히 방어할 수 있다.

**Docker Registry 라우팅**: Nexus에서 Docker hosted/proxy 리포지토리는 각각 별도 포트를 사용한다. proxy 없이는 개발자가 포트 번호를 외워야 하고, 리포지토리가 추가될 때마다 포트가 늘어난다.

Reverse proxy가 있으면 서브도메인이나 경로 기반으로 라우팅할 수 있어서 클라이언트가 알아야 할 엔드포인트가 단순해진다. 방화벽 관리 측면에서도 443 포트 하나만 열면 되니 보안팀과의 협의가 수월해진다.

**운영**: 앞단에 proxy가 있으면 access log를 별도로 남기고, 무중단 인증서 교체가 가능하며, A/B 라우팅으로 blue-green 업그레이드도 할 수 있다. Traefik을 사용하면 Docker 레이블 기반 자동 설정, Let's Encrypt 자동 갱신까지 가능해서 운영 부담이 더 줄어든다.

---

## Q5: start_period 120s의 근거 — Nexus 시작 과정에서 무슨 일이 일어나는가?

Nexus는 단순한 웹 앱이 아니라 **OSGi 기반 모듈 시스템**이다. 시작 시 다음 단계를 거친다:

1. **JVM bootstrap** (5-10s): 클래스 로딩, GC 초기화
2. **Karaf/OSGi 컨테이너 시작** (10-20s): 번들 스캔 및 의존성 해결
3. **번들 초기화** (20-40s): 수십 개의 OSGi 번들이 순차적으로 activate
4. **DB 초기화** (10-20s): H2 스키마 검증, 마이그레이션 적용, 인덱스 로드
5. **Blob Store 검증** (5-10s): Blob Store 접근 가능성 확인
6. **리포지토리 로드** (10-30s): 모든 리포지토리 구성 로드 및 헬스체크

합산하면 60-130초다. Blob Store가 S3라면 네트워크 지연으로 더 걸릴 수 있고, 리포지토리가 수백 개인 대규모 인스턴스는 3분을 넘기기도 한다.

120초는 일반적인 환경에서의 안전 마진이며, 대규모에서는 180-240초로 늘리는 것도 고려해야 한다.

`start_period`와 `interval`, `retries`의 관계도 이해해야 한다. Docker의 healthcheck는 `start_period` 동안은 실패해도 컨테이너를 unhealthy로 판정하지 않는다.

K8s에서는 이 개념이 `startupProbe`, `livenessProbe`, `readinessProbe`로 분리되어 있어 더 세밀한 제어가 가능하다.

---

## Q6: Docker 환경에서 Nexus 업그레이드 전략 — blue-green vs rolling?

**Blue-green**이 안전하다. 새 버전 컨테이너를 다른 포트에 **새 volume으로** 띄우고, 기존 데이터를 복사한 뒤 확인하고, proxy를 전환하는 방식이다.

여기서 절대 해서는 안 되는 것: **같은 Blob Store를 두 Nexus 인스턴스가 동시에 마운트하는 것**. Nexus OSS는 단일 노드만 지원하므로, 동일 데이터를 두 프로세스가 접근하면 파일 락 충돌, DB 손상이 발생한다.

blue-green을 하려면 데이터를 복사해서 별도 volume을 만들어야 하며, 전환 시점에 짧은 downtime은 감수해야 한다.

구체적 절차는 이렇다: (1) Nexus 중지 → (2) 데이터 볼륨 스냅샷/복사 → (3) 새 버전 컨테이너를 복사본 볼륨으로 시작 → (4) 상태 확인 → (5) Reverse Proxy 전환 → (6) 문제 없으면 구버전 제거.

Rolling update는 K8s에서 replicas=1인 StatefulSet의 `updateStrategy: RollingUpdate`로 구현되지만, 결국 구 Pod 종료 → 신 Pod 시작이므로 1-2분의 downtime은 피할 수 없다.

DB 마이그레이션이 포함된 메이저 업그레이드(예: OrientDB → H2)에서는 반드시 전체 백업 후 진행해야 하고, 롤백 시 이전 백업 + 이전 이미지 조합으로 복원해야 한다.

---

## 심화: Nexus를 HA(고가용성)로 구성하려면 어떤 아키텍처가 필요한가?

Nexus OSS는 HA를 지원하지 않는다. **Nexus Pro(유료)**에서만 active-passive HA가 가능하다.

Active 노드가 요청을 처리하고, Passive 노드는 대기한다. 두 노드는 **공유 Blob Store**(NFS 또는 S3)와 **공유 DB**(외부 PostgreSQL)를 사용한다.

Active 노드가 다운되면 로드밸런서가 Passive로 전환한다. 이 전환에 걸리는 시간은 로드밸런서의 헬스체크 간격 + Nexus 시작 시간으로, 보통 2-5분 정도 소요된다.

OSS에서 HA 비슷한 효과를 내려면? proxy 리포지토리를 여러 Nexus 인스턴스에 중복 구성하면 외부 의존성 다운로드는 한쪽이 죽어도 가능하다.

hosted 아티팩트는 양쪽에 동시 배포(dual publish)하는 방법도 있지만 일관성 보장이 어렵고 CI 파이프라인이 복잡해진다.

가장 현실적인 OSS 전략은 Nexus 장애 시 CI가 로컬 캐시(`~/.m2/repository`, `node_modules`)로 버틸 수 있도록 설계하고, 자동 백업 + 빠른 복구 스크립트를 준비해두는 것이다.
