# Ch09: 정리 정책과 스토리지 관리 — 심화 탐구

## Q1: Cleanup Task와 Compact Blob Store Task를 분리한 설계 이유는?

두 단계로 나눈 가장 큰 이유는 복구 가능성(recoverability)을 확보하기 위해서다. soft delete 상태에서는 Blob Store의 `.bytes` 파일이 물리적으로 남아 있으므로, 실수로 잘못된 Cleanup Policy를 적용했을 때 DB 메타데이터만 복원하면 아티팩트를 되살릴 수 있다. hard delete 후에는 복구가 불가능하니, soft delete라는 "안전 구간"을 둔 것이다.

또 다른 이유는 성능 분리다. Cleanup Task는 DB 쿼리 위주의 작업이고, Compact Task는 파일시스템 I/O 위주의 작업이다. 이 둘을 분리해서 서로 다른 시간대에 실행하면 Nexus 서비스에 미치는 영향을 줄일 수 있다. Compact는 대량의 파일을 삭제하면서 디스크 I/O를 점유하므로, 빌드가 활발한 업무 시간에 실행하면 아티팩트 다운로드 성능이 저하될 수 있기 때문이다.

이런 2단계 삭제 패턴은 Nexus만의 독특한 설계가 아니라, 데이터베이스의 MVCC(Multi-Version Concurrency Control)나 파일시스템의 unlink/fsck 관계와 유사한 개념이다. PostgreSQL의 VACUUM이 dead tuple을 정리하는 것과 본질적으로 같은 문제를 풀고 있는 셈이다. 즉시 삭제보다는 "삭제 마크 → 나중에 정리"가 동시성과 안전성 측면에서 유리한 것이다.

---

## Q2: S3 Blob Store로 전환 시 기존 데이터 마이그레이션 방법은?

Nexus는 Blob Store 간 직접 마이그레이션 기능을 제공하지 않는다. 공식 권장 방식은 다음과 같다.

1. 새 S3 Blob Store를 생성
2. 기존 리포지토리의 Blob Store를 새것으로 변경 (Nexus 3.x에서는 리포지토리 재생성 필요)
3. 이전 아티팩트는 기존 File Blob Store에 남고, 새 아티팩트만 S3에 저장됨
4. 시간이 지나면서 기존 아티팩트가 Cleanup으로 정리되거나, 수동으로 re-upload

"라이브 마이그레이션"이 안 되는 셈이라 불편하지만, 현실적인 우회책이 있다. Nexus를 일시 중지하고, File Blob Store의 content를 `aws s3 sync`로 S3에 복사한 뒤, S3 Blob Store를 같은 경로 구조로 생성하는 방법이다.

```bash
# 예시 (Nexus 중지 상태에서)
aws s3 sync /opt/sonatype-work/nexus3/blobs/docker-blobs/content/ \
  s3://company-nexus/docker-blobs/content/ \
  --storage-class STANDARD
```

다만 이건 공식 지원 절차가 아니므로, 반드시 사전 백업 후 테스트 환경에서 먼저 검증해야 한다. Blob Store 내부의 `.properties` 파일과 `.bytes` 파일의 관계가 정확히 유지되어야 하기 때문이다. `.properties`에 기록된 `size`, `sha1` 등의 값이 `.bytes`와 불일치하면 Nexus가 해당 blob을 corrupt로 판단할 수 있다. 소규모 Blob Store(100GB 이하)에서는 리포지토리를 재생성하고 아티팩트를 다시 upload하는 것이 더 안전한 선택인 경우가 많다.

---

## Q3: Docker 이미지 정리 시 manifest와 layer의 관계는?

Docker 이미지 삭제의 복잡성은 manifest와 layer의 다대다 관계에서 비롯된다. 하나의 manifest(이미지 태그)는 여러 layer를 참조하고, 하나의 layer는 여러 manifest에서 참조될 수 있다.

특정 태그를 삭제하면 해당 manifest는 제거되지만, 참조하던 layer가 다른 manifest에서도 사용 중이라면 layer는 삭제되지 않는다. Nexus의 Cleanup Task는 이 참조 관계를 추적해서 "어떤 manifest에서도 참조하지 않는 orphan layer"만 soft delete 대상으로 분류한다.

실무적으로 주의할 점은, manifest list(멀티 아키텍처 이미지)를 삭제할 때다. manifest list → platform manifest → layer라는 3단 참조 구조이므로, manifest list만 삭제하면 하위 platform manifest가 orphan이 되고, 이것들이 정리되어야 비로소 layer도 orphan이 된다. 한 번의 Cleanup 실행으로 전체 체인이 정리되지 않을 수 있어, Cleanup을 2~3회 연속 실행해야 완전히 정리되는 경우도 있다.

이 문제를 확인하려면 Cleanup 후 Blob Store 크기가 예상만큼 줄지 않을 때 다시 Cleanup을 실행해보는 것이다. 두 번째 실행에서 추가 삭제 대상이 발견된다면 다단 참조 정리가 진행 중인 것이다. Docker 이미지가 많은 환경에서는 Cleanup을 일주일에 2~3회 실행하는 것이 실무적인 권장 사항이다.

---

## Q4: Cleanup Policy Preview에서 보이는 것과 실제 삭제되는 것의 차이는?

Preview는 "현 시점에서 정책 기준에 부합하는 컴포넌트 목록"을 보여주는 스냅샷이다. 실제 Cleanup Task가 실행되는 시점에는 상황이 달라질 수 있다.

Preview에서 보였지만 삭제되지 않는 경우로는, Preview 후 누군가 해당 아티팩트를 다운로드해서 "Last Downloaded" 기준에서 벗어나는 케이스가 대표적이다. CI 파이프라인이 야간에 빌드를 돌리면서 아티팩트를 pull하면, 새벽 2시의 Cleanup 시점에서는 "방금 다운로드됨" 상태가 되어 정리 대상에서 빠질 수 있다.

반대로 Preview에 없었지만 삭제되는 경우는, Preview와 실제 실행 사이에 시간이 지나면서 새로운 아티팩트가 기준을 충족하게 된 때다. 예를 들어 Preview 시점에 29일이었던 아티팩트가 Cleanup 실행 시점에 31일이 되면 "Component Age > 30일" 기준에 새로 걸리게 된다.

Preview의 결과 건수에도 제한이 있을 수 있다. 대량의 컴포넌트가 대상일 때 UI에서 전부 보여주지 않는 경우가 있으므로, Preview 결과가 적다고 안심하지 말고 정책 기준 자체를 꼼꼼히 검토하는 습관이 필요하다. 특히 Release Type 필터를 빠뜨려서 RELEASE까지 정리 대상에 포함되는 실수가 가장 위험하니, Preview에서 RELEASE 아티팩트가 하나라도 보이면 즉시 정책을 수정해야 한다.

---

## Q5: RELEASE 아티팩트를 절대 삭제하면 안 되는 경우는?

금융(PCI-DSS), 의료(HIPAA), 정부(FedRAMP) 등 규제 환경에서는 프로덕션에 배포된 소프트웨어의 빌드 아티팩트를 일정 기간(보통 5~7년) 보존해야 한다. 감사 시 "2023년 3월에 배포된 버전 2.1.0의 바이너리를 제출하라"는 요구가 올 수 있는데, 이때 해당 아티팩트가 없으면 규제 위반이 된다.

이런 환경에서는 `maven-releases` 리포지토리에 Cleanup Policy를 절대 연결하지 않고, 전용 Blob Store에 저장해서 물리적으로도 분리한다. 추가로 Blob Store를 S3에 두고 Object Lock(WORM — Write Once Read Many)을 활성화하면, Nexus 관리자도 삭제할 수 없는 규제 준수 아카이브가 만들어진다.

```bash
# S3 Object Lock 설정 (버킷 생성 시)
aws s3api create-bucket \
  --bucket company-nexus-archive \
  --object-lock-enabled-for-bucket \
  --region ap-northeast-2

# 기본 보존 기간 설정 (7년)
aws s3api put-object-lock-configuration \
  --bucket company-nexus-archive \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "COMPLIANCE",
        "Years": 7
      }
    }
  }'
```

다만 모든 RELEASE를 영구 보존하면 스토리지 비용이 끝없이 증가하므로, "프로덕션에 배포된 버전"과 "배포되지 않은 RELEASE"를 구분하는 태깅 전략이 필요하다. Nexus Pro의 태그 기능이나 별도의 메타데이터 DB로 배포 이력을 관리하는 방식이 실무에서 쓰인다.

---

## Q6: Blob Store 분리 전략은 어떻게 설계하는가?

Blob Store 분리의 축은 크게 두 가지다. **포맷별**(Maven, Docker, npm)과 **환경별**(개발, 스테이징, 프로덕션)이 그것이다.

포맷별 분리는 스토리지 특성이 다를 때 유용하다. Docker 이미지는 대용량이라 빠른 SSD가 필요하고, Maven SNAPSHOT은 빈번하게 쓰고 지우므로 쓰기 내구성이 중요하며, RELEASE 아카이브는 접근 빈도가 낮으므로 저비용 스토리지(HDD 또는 S3 IA)가 적합하다.

환경별 분리는 접근 제어와 결합할 때 의미가 있다. 개발용 Blob Store는 자유롭게 정리하되, 프로덕션용은 보존 정책을 엄격히 적용하는 식이다.

실무적인 Blob Store 설계 예시를 규모별로 정리하면 이렇다.

```
소규모 (5-10명, 100GB 이하):
  default → 모든 리포지토리

중규모 (10-50명, 500GB 이하):
  default      → Maven, npm, 기타
  docker-blobs → Docker 전용

대규모 (50명 이상, 1TB 이상):
  maven-blobs    → Maven (SSD)
  docker-blobs   → Docker (대용량 SSD)
  npm-blobs      → npm (SSD)
  archive-blobs  → 장기 보존 RELEASE (S3/HDD)
  proxy-cache    → proxy 캐시 (저비용 디스크, 공격적 정리)
```

소규모 팀이라면 `default`와 `docker-blobs` 두 개로 충분한 경우가 많고, 팀이 커지고 아티팩트가 늘어나면서 점진적으로 분리해가는 게 현실적인 접근이다. 처음부터 과도하게 분리하면 관리 오버헤드만 늘어난다. 분리를 고려할 시점의 신호는 "특정 포맷의 아티팩트가 전체 디스크의 60% 이상을 차지할 때"다.

---

## Q7: Cleanup 실행 중 Nexus 성능에 미치는 영향은?

Cleanup Task 자체는 DB 쿼리가 주된 작업이므로, CPU와 메모리에 부하를 준다. 대규모 리포지토리(컴포넌트 10만 개 이상)에서는 Cleanup이 30분~1시간 걸릴 수 있으며, 이 시간 동안 검색 API 응답이 느려질 수 있다.

Compact Task는 파일시스템 I/O가 주된 작업이다. 수만 개의 파일을 삭제하면서 디스크 I/O를 점유하므로, 같은 디스크에서 아티팩트를 서빙하는 성능이 저하된다. SSD 환경에서는 영향이 적지만 HDD 환경에서는 체감될 수 있다.

성능 영향을 최소화하는 전략은 세 가지다. 첫째, 업무 시간 외(새벽 2-5시)에 실행한다. 둘째, Blob Store를 분리해서 Compact를 분산 실행한다. default는 2시, docker-blobs는 3시, proxy-cache는 4시처럼. 셋째, Nexus의 JVM 힙 메모리가 충분한지 확인한다. Cleanup 중 DB 쿼리가 대량의 결과를 처리하므로, 4GB 이상의 힙을 할당하는 것이 권장된다.

---

## 심화 질문

> 디스크 90% 사용 시 긴급 대응 절차는?

첫째, 가장 빠른 효과를 내는 건 docker-proxy 캐시 삭제다. proxy 리포지토리의 "Invalidate cache" 후 Compact를 실행하면 캐시된 외부 이미지가 즉시 회수된다. 내부 아티팩트를 건드리지 않으므로 영향 범위가 작다.

```bash
# proxy 캐시 무효화 (REST API)
curl -u admin:admin123 -X POST \
  "http://localhost:8081/service/rest/v1/repositories/docker-proxy/invalidate-cache"

# Compact 즉시 실행
curl -u admin:admin123 -X POST \
  "http://localhost:8081/service/rest/v1/tasks/run" \
  -H "Content-Type: application/json" \
  -d '{"id": "compact-docker-blobs-task-id"}'
```

둘째, SNAPSHOT과 untagged Docker 이미지를 대상으로 "Component Age > 7일" 같은 공격적인 Cleanup Policy를 임시 적용하고 Cleanup + Compact를 수동 실행한다. 정상화 후에는 원래 정책으로 되돌린다. 정상 정책으로 복원하는 것을 잊지 않도록 캘린더 리마인더를 걸어두는 게 좋다.

셋째, 위 조치로도 부족하면 임시 디스크를 마운트해서 Blob Store 경로를 변경하거나, 새 Blob Store를 추가 디스크에 생성해서 일부 리포지토리를 이동한다.

이 모든 과정에서 절대 하지 말아야 할 것은 Blob Store 디렉토리에서 파일을 직접 삭제(`rm`)하는 것이다. Nexus DB와 Blob Store 간 정합성이 깨지면 복구가 극도로 어려워진다. 반드시 Nexus API나 Task를 통해 삭제해야 한다. 긴급 상황에서 이 원칙을 무시하고 싶은 유혹이 생기지만, 정합성 깨진 Nexus를 복구하는 데 드는 시간이 디스크 정리보다 몇 배는 더 걸린다.
