# Ch05. REST API와 웹 연동 - 심화 탐구

---

## Q1. continuationToken vs offset/limit — 어떤 상황에서 어떤 방식이 유리할까?

offset/limit은 "10페이지로 건너뛰기"가 가능하다는 장점이 있다. 사용자가 페이지 번호를 클릭하는 UI에 자연스럽게 맞아떨어지기 때문이다. 하지만 offset이 커질수록 DB는 그만큼의 행을 스캔하고 버려야 하므로, 수십만 건에서는 성능이 급격히 나빠진다.

continuationToken은 마지막 조회 위치를 토큰에 인코딩하므로, 데이터가 아무리 많아도 조회 성능이 일정하다. 대신 "5페이지로 점프"가 불가능하고, 순방향 순회만 된다. Nexus처럼 컴포넌트가 수십만 개에 달할 수 있는 시스템에서는 토큰 방식이 합리적인 선택이다.

결론적으로, 전체 목록을 순회하거나 무한 스크롤 UI라면 토큰 방식이 낫고, 페이지 번호 기반 네비게이션이 필수라면 offset/limit이 필요하다. 둘 다 제공하는 API(예: GitHub)도 있는데, Nexus는 토큰만 지원하므로 UI 설계 시 "더 보기" 버튼이나 무한 스크롤 패턴을 채택해야 한다. 만약 페이지 번호 UI가 반드시 필요하다면, 클라이언트 측에서 전체 결과를 한 번 순회하면서 각 페이지의 시작 토큰을 캐싱해두는 방법도 있긴 한데, 데이터가 변경되면 캐시가 무효화되므로 실용성은 제한적이다.

---

## Q2. API Token과 Basic Auth — 각각 언제 쓰는 게 적절할까?

Basic Auth는 설정이 단순해서 로컬 개발이나 일회성 스크립트에 적합하다. 하지만 비밀번호를 직접 전달하므로, 비밀번호 로테이션 시 모든 사용처를 업데이트해야 하는 번거로움이 따른다.

API Token(Nexus Pro)은 비밀번호와 독립적인 인증 수단이라서 CI/CD 파이프라인에 안성맞춤이다. 토큰을 폐기해도 사용자 비밀번호는 영향받지 않고, 토큰별로 폐기가 가능하니 유출 시 대응이 빠르다. 하나의 서비스 계정에서 여러 토큰을 발급받아 Jenkins용, GitHub Actions용, ArgoCD용으로 분리하면, 특정 시스템이 해킹되었을 때 해당 토큰만 폐기할 수 있어 피해 범위를 최소화할 수 있다.

OSS 환경이라면 서비스 전용 계정을 만들어 비밀번호를 CI 시크릿에 넣는 방식으로 대체하되, 계정 비밀번호 변경 시 CI 설정도 함께 바꿔야 한다는 운영 부담은 감수해야 한다. 이 부담을 줄이려면 Vault나 AWS Secrets Manager 같은 시크릿 관리 도구를 도입해서, 비밀번호를 한 곳에서 변경하면 모든 CI 파이프라인에 자동 반영되게 만드는 것이 실무적인 해결책이다.

---

## Q3. 1GB 이상 대용량 파일을 REST API로 올릴 수 있을까?

Nexus REST API 자체에 하드코딩된 파일 크기 제한은 없지만, 실질적으로 여러 제약이 작동한다. 첫째, JVM 힙 메모리 — 멀티파트 파싱 과정에서 메모리를 소비하므로 힙이 부족하면 OOM이 발생할 수 있다. 둘째, 리버스 프록시 설정 — Nginx의 `client_max_body_size` 기본값이 1MB라서 이를 늘리지 않으면 413 에러가 난다. 셋째, 타임아웃 — 대용량 전송은 시간이 걸리므로 프록시와 클라이언트 양쪽의 타임아웃을 조정해야 한다.

실제로 1GB 파일을 올려야 한다면 다음 설정을 확인해야 한다.

```nginx
# Nginx
client_max_body_size 2G;
proxy_read_timeout 600;
proxy_send_timeout 600;
proxy_request_buffering off;  # 스트리밍 전달, 메모리 절약
```

```bash
# curl 타임아웃 조정
curl --max-time 600 --connect-timeout 30 -u admin:admin123 \
  -X POST "http://localhost:8081/service/rest/v1/components?repository=raw-hosted" \
  -F "raw.directory=/large-files" \
  -F "raw.asset1=@./big-archive.tar.gz" \
  -F "raw.asset1.filename=big-archive.tar.gz"
```

대안으로는 직접 PUT 방식이 있다. Raw 리포지토리는 `PUT /repository/{repo-name}/{path}` 경로로 파일을 직접 스트리밍할 수 있어서, 멀티파트 오버헤드를 피할 수 있다. Docker 이미지처럼 레이어 단위로 분할된 포맷은 자체 프로토콜을 쓰니 REST API 크기 제한과는 무관하다.

---

## Q4. CORS 설정 없이 다른 도메인에서 Nexus API를 호출하는 방법이 있을까?

가장 흔한 방법은 백엔드 프록시를 두는 것이다. 프론트엔드가 자기 서버의 `/api/nexus/*` 경로로 요청하면, 서버가 Nexus에 대신 요청하고 결과를 돌려준다. 브라우저 입장에서는 같은 출처이므로 CORS 문제가 발생하지 않는다. 이 방식의 추가 장점은 Nexus 인증 정보를 서버 쪽에서만 관리할 수 있다는 것이다. 프론트엔드 코드에 Basic Auth 정보를 넣지 않아도 되니 보안 측면에서도 우수하다.

두 번째로 Nginx 등의 리버스 프록시에서 `Access-Control-Allow-Origin` 헤더를 주입하는 방식이 있다. Nexus 앞에 프록시를 배치하는 건 TLS 종료나 로드밸런싱 때문에 이미 흔한 구성이므로, CORS 헤더 추가는 큰 부담이 아니다. 다만 preflight 요청(OPTIONS)에 대한 처리를 빠뜨리는 경우가 많으니, `if ($request_method = OPTIONS) { return 204; }` 블록을 반드시 포함해야 한다.

세 번째로 같은 도메인에서 웹 앱을 서빙하면 아예 CORS가 발생하지 않는다. Nexus의 기본 포트에 커스텀 페이지를 올리기는 어렵지만, 프록시에서 `/app/*`은 정적 파일로, `/service/*`은 Nexus로 라우팅하면 동일 출처를 만들 수 있다. 프로덕션 배포에서는 이 방식이 CORS 헤더를 관리하는 것보다 깔끔한 경우가 많다.

---

## Q5. Search API는 내부적으로 어떻게 인덱싱하고 있을까?

Nexus는 컴포넌트 메타데이터를 내부 데이터베이스(OrientDB 또는 H2)에 저장하면서 인덱스를 구축한다. 업로드 시점에 메타데이터(groupId, artifactId, version, 태그 등)가 인덱싱되고, 검색 시 이 인덱스를 조회한다.

`keyword` 파라미터는 여러 필드를 대상으로 부분 매칭을 수행하지만, 전문 검색 엔진(Elasticsearch 같은)이 아니므로 퍼지 매칭이나 형태소 분석은 지원하지 않는다. `group`, `name`, `version` 같은 정확한 필드 지정 검색이 훨씬 빠르고 정확하다. 실무에서 "spring"을 keyword로 검색하면 수천 개가 나올 수 있지만, `group=org.springframework&name=spring-core`로 검색하면 원하는 결과만 정확히 나온다.

Rebuild Index 태스크를 돌리면 인덱스를 재구축할 수 있는데, 디스크의 블롭과 DB 메타데이터가 불일치할 때(수동 파일 삭제 후 등) 필요하다. 대규모 리포지토리에서는 리빌드에 상당한 시간이 걸리니 운영 시간을 피해 실행해야 한다. Nexus 업그레이드 후에도 인덱스 호환성 문제가 생길 수 있으므로, 업그레이드 절차에 Rebuild Index를 포함시키는 팀도 있다.

---

## Q6. REST API로 리포지토리 자체를 생성하거나 설정을 변경할 수 있을까?

가능하다. `/service/rest/v1/repositories/{format}/{type}` 엔드포인트로 리포지토리 CRUD를 수행할 수 있다. 예를 들어 Maven hosted 리포지토리를 만들려면 `POST /service/rest/v1/repositories/maven/hosted`에 JSON 설정을 보내면 된다.

```bash
# Raw hosted 리포지토리 생성 예시
curl -u admin:admin123 -X POST \
  "http://localhost:8081/service/rest/v1/repositories/raw/hosted" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "team-raw-hosted",
    "online": true,
    "storage": {
      "blobStoreName": "default",
      "strictContentTypeValidation": false,
      "writePolicy": "ALLOW"
    }
  }'

# 리포지토리 삭제
curl -u admin:admin123 -X DELETE \
  "http://localhost:8081/service/rest/v1/repositories/team-raw-hosted"
```

다만 이 API는 관리자 권한(`nx-admin`)이 필요하고, 리포지토리 설정(스토리지, 정책, 프록시 URL 등)을 모두 JSON으로 명시해야 한다. UI에서 클릭 몇 번으로 할 일을 JSON으로 작성하는 건 번거롭지만, Infrastructure as Code 관점에서는 리포지토리 구성을 코드로 관리하고 Git에 커밋할 수 있다는 장점이 크다.

Blob store 관리, 보안 설정, 스케줄 태스크 등도 API로 제어할 수 있어서, 이론적으로는 Nexus UI를 한 번도 열지 않고 전체 인스턴스를 구성하는 것도 가능하다. Terraform의 Nexus 프로바이더가 이 API들을 래핑한 것이니 참고해볼 만하다.

---

## Q7. Nexus API 응답 캐싱 전략은 어떻게 세울까?

Nexus API 응답 자체에는 Cache-Control 헤더가 제한적으로 설정되어 있다. 검색 결과나 컴포넌트 목록은 실시간으로 변할 수 있으므로, Nexus가 적극적으로 캐시를 권장하지 않는 것이다.

하지만 클라이언트 측에서 합리적인 캐싱을 구현할 수 있다. 리포지토리 목록(`/repositories`)은 자주 변하지 않으므로 5~10분 TTL로 캐싱해도 무방하고, 에셋의 `downloadUrl`은 변하지 않으므로 오래 캐싱 가능하다. 반면 검색 결과는 새 아티팩트 업로드 시 바뀌므로, 짧은 TTL(30초~1분)이거나 캐싱하지 않는 편이 안전하다.

프론트엔드에서 React Query나 SWR 같은 라이브러리를 쓴다면, staleTime과 cacheTime을 엔드포인트별로 다르게 설정하는 것이 효과적이다. 리포지토리 목록은 `staleTime: 10 * 60 * 1000`, 검색 결과는 `staleTime: 0`으로 설정하면 불필요한 네트워크 요청을 줄이면서도 데이터 신선도를 유지할 수 있다.

---

## 심화 질문: Nexus Script API(Groovy)가 deprecated된 이유와 대안은?

Nexus 3 초기에는 Groovy 스크립트를 서버에 등록하고 실행하는 Script API가 존재했다. 리포지토리 생성, 사용자 관리 등 REST API로 불가능했던 관리 작업을 스크립트로 자동화할 수 있어서 널리 사용됐다.

그런데 이 기능은 서버 내부에서 임의의 Groovy 코드를 실행하는 셈이라 보안 위험이 컸다. 인증된 관리자만 등록할 수 있다고 해도, 스크립트가 내부 API를 무제한으로 호출할 수 있으므로 권한 경계가 모호했다. 스크립트 하나가 전체 데이터를 삭제하거나 설정을 변조할 수 있다는 뜻이니까. 또한 Nexus 업그레이드 시 내부 API가 변경되면 기존 스크립트가 깨지는 호환성 문제도 빈번했다.

Sonatype은 Nexus 3.21부터 Script API를 기본 비활성화하고(nexus.scripts.allowCreation=true로 명시 활성화 필요), 대신 REST API를 확장하는 방향으로 전환했다. 현재 리포지토리 CRUD, 보안 설정, 태스크 관리 등 대부분의 관리 기능이 REST API로 가능하므로, 스크립트가 필요한 경우는 거의 없다.

레거시 스크립트가 남아 있다면, 해당 로직을 REST API 호출로 마이그레이션하거나, Terraform Nexus Provider로 전환하는 것이 권장 방향이다. Terraform Provider는 `nexus_repository`, `nexus_security_user`, `nexus_blobstore` 같은 리소스를 선언적으로 관리할 수 있어서, 스크립트보다 유지보수가 훨씬 용이하다.
