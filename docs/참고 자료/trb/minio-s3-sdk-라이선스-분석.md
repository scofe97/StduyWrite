# MinIO → AWS S3 SDK 교체: 라이선스 분석 및 실무 판단

> 작성일: 2026-03-11
> 목적: TPS 프로젝트의 MinIO Java SDK → AWS S3 SDK 교체 작업에 대한 라이선스 사실 확인 및 교체 판단 근거 정리

---

## 1. 배경

TPS 프로젝트에서 MinIO 서버를 오브젝트 스토리지로 사용 중이다. 내부 문서에는 다음과 같은 교체 근거가 명시되어 있다.

> "MinIO 클라이언트(Java SDK)는 AGPL 라이선스를 사용합니다. AGPL은 네트워크를 통해 서비스를 제공하는 경우 소스 코드 공개 의무가 부과될 수 있어, 상용·내부 서비스에서 사용 시 라이선스 리스크가 있습니다."

이 문서는 위 근거의 사실 여부를 검증하고, 교체의 실질적 이유를 정리한다.

---

## 2. 라이선스 사실 확인

### 2.1 MinIO 생태계 라이선스 현황

| 대상 | GitHub 리포 | 라이선스 | 확인 방법 |
|------|------------|---------|----------|
| MinIO 서버 | `minio/minio` | **AGPL v3** | GitHub 리포 명시 |
| MinIO Client CLI (`mc`) | `minio/mc` | **AGPL v3** | GitHub 리포 명시 |
| MinIO Java SDK | `minio/minio-java` | **Apache 2.0** | GitHub API 확인 |
| MinIO Go SDK | `minio/minio-go` | Apache 2.0 | GitHub 리포 명시 |
| MinIO Python SDK | `minio/minio-py` | Apache 2.0 | GitHub 리포 명시 |
| AWS S3 SDK for Java v2 | `aws/aws-sdk-java-v2` | Apache 2.0 | GitHub 리포 명시 |

**핵심: MinIO Java SDK(`io.minio:minio`)는 AGPL이 아니라 Apache 2.0이다.**

### 2.2 내부 문서의 오류

문서에서 "MinIO 클라이언트(Java SDK)는 AGPL"이라고 적은 것은 사실과 다르다. 혼동의 원인은 MinIO의 2021년 공식 블로그 문구로 추정된다.

> "With RELEASE.2021-05-11 MinIO completed its transition to the GNU AGPL v3 license, meaning that the **server, client and gateway** are now licensed under GNU AGPL v3."

여기서 "client"는 **`mc` CLI 도구**를 의미하는 것이지, Java/Python/Go 등의 **SDK 라이브러리가 아니다.** SDK 리포지토리들은 모두 Apache 2.0을 유지하고 있으며, 이는 GitHub API를 통해 직접 확인했다.

### 2.3 AGPL v3 vs Apache 2.0 라이선스 비교

두 라이선스는 오픈소스지만 성격이 근본적으로 다르다. AGPL은 "사용자의 자유를 보장"하기 위해 소스 공개를 강제하는 카피레프트 라이선스이고, Apache 2.0은 "자유롭게 쓰되 출처만 밝혀라"는 허용적(permissive) 라이선스다.

| 항목 | AGPL v3 | Apache 2.0 |
|------|---------|------------|
| **분류** | 강한 카피레프트 (Copyleft) | 허용적 (Permissive) |
| **소스 공개 의무** | 있음 — 수정·배포·네트워크 서비스 제공 시 전체 소스 공개 필수 | 없음 — 소스 공개 의무 없이 상용 제품에 포함 가능 |
| **네트워크 조항 (Section 13)** | 있음 — 서버로 서비스를 제공하는 것만으로도 소스 공개 의무 발생 (GPL과의 핵심 차이) | 없음 |
| **파생저작물 전염** | 있음 — AGPL 코드를 linking하면 결합된 전체 프로그램이 AGPL 적용 | 없음 — 결합해도 내 코드의 라이선스는 유지 |
| **특허 허가** | 묵시적 허가 (명시 조항 없음) | 명시적 특허 허가 — 기여자가 관련 특허를 사용자에게 허가 |
| **상용 소프트웨어 포함** | 위험 — 소스 공개 의무 때문에 상용 제품에 직접 포함하기 어려움 | 안전 — 저작권 고지와 LICENSE 파일 포함만 하면 됨 |
| **수정 후 재배포** | 수정본 전체를 AGPL로 공개해야 함 | 수정본의 라이선스는 자유롭게 선택 가능 (변경 사항 표시만 필요) |
| **고지 의무** | 저작권 고지 + 라이선스 전문 포함 + 소스 접근 방법 안내 | 저작권 고지 + NOTICE 파일 포함 |

**실무적 의미:**
- AGPL 라이브러리를 `build.gradle`에 의존성으로 추가하면, 이론적으로 내 애플리케이션 전체가 AGPL 적용 대상이 된다. 네트워크를 통해 서비스하는 순간 소스 공개 의무가 발생한다.
- Apache 2.0 라이브러리는 `build.gradle`에 추가해도 내 코드에 아무런 의무가 전파되지 않는다. 저작권 고지만 유지하면 된다.
- 따라서 MinIO Java SDK가 Apache 2.0이라는 사실은, SDK를 의존성으로 사용해도 TPS 소스 코드 공개 의무가 전혀 없다는 것을 의미한다.

### 2.4 AGPL 의무가 발생하는 경우와 아닌 경우

AGPL v3의 소스 공개 의무는 Section 13에 정의되어 있다.

**의무가 발생하는 경우:**
- AGPL 코드를 **수정**하여 네트워크 서비스로 제공할 때
- AGPL 라이브러리를 **linking**(의존성으로 포함)하여 하나의 프로그램으로 결합할 때

**의무가 발생하지 않는 경우:**
- AGPL 서버를 **수정 없이** 내부 인프라로 사용할 때
- AGPL 서버와 **HTTP 네트워크 통신**만 할 때 (API 호출은 파생저작물이 아님)
- **Apache 2.0 SDK**를 사용하여 AGPL 서버에 접속할 때

TPS 프로젝트의 상황:
- MinIO 서버: 수정 없이 내부 스토리지로 사용 → AGPL 의무 없음
- MinIO Java SDK: Apache 2.0 → AGPL 의무 자체가 해당 없음
- 애플리케이션 → MinIO 서버: HTTP 통신 → 파생저작물 아님

**따라서 현재 구성에서 소스 코드 공개 의무는 없다.**

### 2.5 "AGPL 서버를 설치하면 파일을 공개해야 하나?"

흔한 오해가 있다. "AGPL 소프트웨어를 쓰면 뭔가 공개해야 하는 거 아닌가?" MinIO 서버(AGPL)를 K8s에 설치해서 파일 저장소로 쓰는 상황을 정리한다.

**AGPL이 말하는 "공개"의 대상은 소프트웨어 소스 코드이지, 저장된 데이터가 아니다.**

```
AGPL이 공개를 요구하는 것:
  → MinIO "서버 프로그램"의 소스 코드 (수정했을 때만)

AGPL과 전혀 무관한 것:
  → MinIO에 저장한 사용자 파일 (문서, 이미지, 동영상 등)
  → TPS 애플리케이션의 소스 코드 (MinIO와 HTTP로 통신할 뿐)
  → TPS의 비즈니스 데이터
```

**의무 발생 조건을 단계별로 확인하면:**

```
1단계: MinIO 서버 소스 코드를 수정했는가?
  └─ NO → 공개 의무 없음. 끝.
  └─ YES → 2단계로

2단계: 수정한 MinIO를 제3자에게 네트워크로 서비스하는가?
  └─ NO (내부 인프라로만 사용) → 공개 의무 없음. 끝.
  └─ YES → 수정된 MinIO 서버 소스 코드를 공개해야 함
```

TPS는 1단계에서 이미 "NO"다. 공식 Docker 이미지(`quay.io/minio/minio:RELEASE.2024-04-18T19-09-19Z`)를 수정 없이 헬름 차트로 배포하고 있기 때문이다. 따라서 어떤 공개 의무도 발생하지 않는다.

AGPL은 소프트웨어 라이선스다. MySQL에 저장한 고객 데이터를 공개할 의무가 없는 것처럼, MinIO에 저장한 파일을 공개할 의무도 없다.

---

## 3. 그럼에도 S3 SDK 교체가 합리적인 경우

라이선스 리스크는 없지만, 다음 상황에서는 교체가 합리적이다.

### 3.1 교체가 합리적인 경우

| 근거 | 설명 |
|------|------|
| **S3 마이그레이션 가능성** | 향후 AWS S3나 다른 S3 호환 스토리지로 전환할 계획이 있다면, 미리 표준 SDK를 사용하는 것이 유리하다 |
| **벤더 독립성** | MinIO SDK에 종속되지 않으면 Ceph, GCS 등 다른 S3 호환 스토리지로 교체가 쉽다 |
| **SDK 유지보수 불안** | 2026-02 MinIO 서버 리포에 "THIS REPOSITORY IS NO LONGER MAINTAINED" 선언. SDK 리포도 영향받을 수 있다 |
| **법무/감사 간소화** | AGPL 서버 벤더의 SDK라는 점이 컴플라이언스 심사에서 불필요한 질문을 유발할 수 있다 |

### 3.2 교체가 불필요한 경우

| 조건 | 설명 |
|------|------|
| MinIO를 계속 사용할 것이 확정 | 벤더 독립성의 실익이 없다 |
| S3 전환 계획 없음 | 마이그레이션 대비가 불필요하다 |
| SDK가 안정적으로 동작 중 | MinIO SDK는 HTTP 래퍼라 서버가 유지되면 SDK 업데이트 필요성이 낮다 |
| 교체 비용이 큼 | 모든 모듈 서비스 코드 변경, 예외 처리 교체, 테스트 비용 발생 |

---

## 4. MinIO S3 API 호환성

MinIO 서버를 유지하면서 AWS S3 SDK로 클라이언트만 교체하는 패턴은 실무에서 흔히 사용된다. MinIO는 S3 프로토콜을 네이티브로 구현한 서버이기 때문이다.

### 4.1 S3 API란?

S3(Simple Storage Service) API는 AWS가 2006년에 만든 오브젝트 스토리지 HTTP 프로토콜이다. 파일을 버킷(bucket)이라는 논리적 컨테이너에 키(key)로 저장하고, HTTP 요청으로 업로드/다운로드/삭제한다. 이 프로토콜이 사실상 업계 표준이 되면서, MinIO/Ceph/GCS 등 다른 스토리지도 동일한 API를 구현하게 되었다.

```
[애플리케이션] --HTTP(S3 프로토콜)--> [S3 호환 서버]
                                      ├── AWS S3 (클라우드)
                                      ├── MinIO (온프레미스)
                                      ├── Ceph (분산 스토리지)
                                      └── GCS (Google, 호환 모드)
```

### 4.2 MinIO SDK vs AWS S3 SDK

두 SDK 모두 결국 S3 프로토콜로 HTTP 요청을 보내는 클라이언트 라이브러리다. 차이는 API 설계 방식에 있다.

**MinIO Java SDK (`io.minio:minio`)**
- MinIO에 최적화된 래퍼. 메서드명이 직관적이고 간결하다.
- `Args` 빌더 패턴 사용: `PutObjectArgs.builder().bucket(...).object(...).build()`
- MinIO 전용 기능(Admin API 등) 접근 가능

**AWS S3 SDK for Java v2 (`software.amazon.awssdk:s3`)**
- AWS 공식 SDK. S3뿐 아니라 모든 AWS 서비스를 동일한 패턴으로 제공한다.
- `Request` 빌더 패턴 사용: `PutObjectRequest.builder().bucket(...).key(...).build()`
- S3 호환 서버라면 `endpointOverride`로 주소만 바꿔서 동일 코드로 접속 가능

둘 다 내부적으로는 같은 S3 HTTP API를 호출하므로, MinIO 서버 입장에서는 어떤 SDK로 요청이 왔는지 구분할 수 없다.

### 4.3 TPS에서 사용하는 API 호환 여부

| MinIO SDK API | AWS S3 SDK API | 호환 |
|---------------|----------------|------|
| `makeBucket` | `createBucket` | O |
| `putObject` | `putObject` | O |
| `getObject` | `getObject` | O |
| `statObject` | `headObject` | O |
| `removeObject` | `deleteObject` | O |
| `copyObject` | `copyObject` | O |
| `listObjects` | `listObjectsV2Paginator` | O |
| `bucketExists` | `headBucket` | O |
| `getPresignedObjectUrl` | `S3Presigner` (별도 클래스) | 주의 |

### 4.2 S3 SDK 사용 시 필수 설정

```java
S3Client s3Client = S3Client.builder()
    .credentialsProvider(StaticCredentialsProvider.create(
        AwsBasicCredentials.create(accessKey, secretKey)))
    .endpointOverride(URI.create("http://minio-host:9000"))
    .region(Region.US_EAST_1)      // 형식 요건, MinIO에서는 실제 의미 없음
    .forcePathStyle(true)          // 필수: MinIO는 path-style URL 사용
    .build();
```

- `forcePathStyle(true)`: 없으면 버킷을 찾지 못함 (virtual-host-style이 기본값)
- `endpointOverride`: MinIO 서버 주소 명시 필수
- `region`: 값 자체는 무의미하지만 SDK가 내부적으로 요구함

### 4.3 알려진 비호환 (TPS와 무관)

- `GetBucketAcl` / `PutBucketAcl`: MinIO는 Policy 기반 접근제어 사용
- `GetBucketWebsite` / `PutBucketWebsite`: 미지원
- 버킷 로깅 및 Analytics API: 미지원

---

## 5. 교체 작업 시 주의사항

교체를 진행한다면 다음을 주의해야 한다.

### 5.1 Presigned URL

workflow-api에서 이미지 미리보기를 위해 `getPresignedObjectUrl()`을 사용 중이다. S3 SDK에서는 `S3Presigner`라는 별도 클래스가 필요하다. S3FileClient에 이 기능이 포함되어 있는지 확인해야 한다.

### 5.2 예외 처리 전면 교체

MinIO SDK 예외(`ErrorResponseException`, `ServerException` 등)와 S3 SDK 예외(`S3Exception`, `NoSuchKeyException` 등)는 완전히 다른 클래스다. 기존 catch 블록을 모두 교체해야 한다.

### 5.3 scheduler 모듈의 독자적 연결

`MinioUploader.connetMinio()`가 런타임에 직접 MinioClient를 생성한다(Config 빈 미사용). S3FileClient로 교체 시 이 패턴을 어떻게 처리할지 결정이 필요하다.

### 5.4 pms-api 빈 충돌 가능성

pms-api가 별도 Config로 S3Client 빈을 등록하면 core-lib의 S3Client 빈과 충돌할 수 있다. `@Qualifier` 또는 `@ConditionalOnMissingBean` 전략이 필요하다.

### 5.5 ppln-logging-api 하드코딩 자격증명

MinioServiceImpl에 하드코딩된 access key/secret key가 존재한다(현재 주석 처리). 이번 정리 시 파일 삭제 대상에 포함해야 한다.

---

## 6. 결론

| 항목 | 결론 |
|------|------|
| MinIO Java SDK가 AGPL인가? | 아니다, **Apache 2.0**이다 |
| SDK 사용 시 소스 공개 의무가 있는가? | **없다** |
| 내부 문서의 교체 근거가 정확한가? | **아니다** (SDK 라이선스를 AGPL로 오인) |
| 교체 자체가 나쁜 결정인가? | 아니다, 벤더 독립성·SDK 유지보수 등 다른 근거는 유효하다 |
| MinIO 고정 + S3 전환 없는 상황에서는? | **교체 비용 대비 실익이 낮다** |

---

## 출처

### MinIO 라이선스

- [minio/minio-java GitHub 리포지토리](https://github.com/minio/minio-java) — SDK 라이선스 Apache 2.0 확인
- [minio-java/LICENSE 파일](https://github.com/minio/minio-java/blob/master/LICENSE) — Apache License 2.0 전문
- [minio/minio GitHub 리포지토리](https://github.com/minio/minio) — 서버 라이선스 AGPL v3 확인
- [MinIO 공식 블로그: From Open Source to Free and Open Source (2021)](https://www.min.io/blog/from-open-source-to-free-and-open-source-minio-is-now-fully-licensed-under-gnu-agplv3) — AGPL 전환 공지, "server, client and gateway" 문구 원문

### AGPL 법적 해석

- [GNU AGPL v3 라이선스 전문](https://www.gnu.org/licenses/agpl-3.0.en.html) — Section 13 네트워크 조항
- [FSF GPL FAQ: Derivative Works](https://www.gnu.org/licenses/gpl-faq.en.html) — 파생저작물 판단 기준
- [FSF: The Fundamentals of the AGPLv3 (2021)](https://www.fsf.org/bulletin/2021/fall/the-fundamentals-of-the-agplv3) — AGPL 의무 발생 조건 해설
- [FOSSA: AGPL License Guide](https://fossa.com/blog/open-source-software-licenses-101-agpl-license/) — AGPL linking 의무 실무 해설

### MinIO S3 호환성

- [MinIO S3 API Compatibility](https://min.io/product/s3-compatibility) — 공식 호환성 목록
- [AGPL and clients 토론 (minio/minio #21296)](https://github.com/minio/minio/discussions/21296) — 클라이언트 SDK 라이선스 관련 커뮤니티 토론

### MinIO 최근 동향 (2026)

- [How MinIO went from open source darling to cautionary tale (2026-02)](https://news.reading.sh/2026/02/14/how-minio-went-from-open-source-darling-to-cautionary-tale/) — 서버 리포 유지보수 중단 선언
- [MinIO Commercial License 페이지](https://www.min.io/commercial-license) — AIStor 상용 전환 안내
