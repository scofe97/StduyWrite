---
title: "trivy 참조 시트"
tags: ["devops", "command", "image", "trivy", "security"]
status: draft
source:
  - "trivy v0.76.2 trivy --help 와 trivy image·filesystem·config·sbom --help 원문 (OrbStack Ubuntu 26.04.1 VM, aarch64 실측)"
  - "https://github.com/aquasecurity/trivy/releases/tag/v0.76.2"
  - "https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/others.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/db.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/filtering.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/advanced/air-gap.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/target/container_image.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/scanner/secret.md"
  - "https://github.com/aquasecurity/trivy/blob/v0.76.2/pkg/fanal/secret/builtin-allow-rules.go"
related:
  - ../README.md
  - ../../../../08_cloud/book/cks-study-guide/06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md
  - ../../../../08_cloud/book/cks-study-guide/06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md
  - ../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md
updated: "2026-11-23"
---

# trivy 참조 시트

---

> 이미지·디렉터리·설정 파일·SBOM 의 취약점과 설정 오류를 찾는 `trivy` 를, 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `trivy` 는 대상 안의 패키지 목록을 내려받은 취약점 DB 와 로컬에서 맞대어 알려진 취약점을 찾는 스캐너입니다.

`trivy` 는 Aqua Security 가 공개한 단일 바이너리라 GitHub 릴리스에서 받아 씁니다. 스캔 대상은 이미지(`image`)·디렉터리(`fs`)·설정 파일(`config`)·SBOM(`sbom`) 등입니다. DB 가 캐시에 있으면 스캔에 네트워크가 필요 없습니다.[^db-local] 왜 스캔하는지와 심각도의 뜻은 [믿을 수 있는 이미지만 들이기](../../../../08_cloud/book/cks-study-guide/06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md) 가 설명하므로 여기서는 되풀이하지 않습니다.

실측 환경은 OrbStack Ubuntu 26.04.1 VM(aarch64)의 `trivy` 0.76.2 이고, 이미지는 같은 VM 의 Docker Engine 29.1.3 에 있습니다. DB 는 `trivy version` 이 찍은 2026-11-23 07:04 UTC 판이라 이 시트의 건수와 CVE 목록은 그날의 값입니다. 가장 새 버전도 0.76.2(2026-11-05 릴리스)입니다.[^latest]



## 핵심 문법

> `trivy` 뒤에 대상 종류(`image`·`fs`·`config`·`sbom`)를 놓고, 플래그로 스캐너·거름 조건·보고서 형식을 정합니다.

```bash
# 호출 형태
# trivy --help 와 하위 명령 --help 의 Usage 줄
trivy [global flags] command [flags] target
trivy image [flags] IMAGE_NAME
trivy filesystem [flags] PATH
trivy config [flags] DIR
trivy sbom [flags] SBOM_PATH

# 이미지의 취약점을 본다 (이미지 취약점 표 읽기)
trivy image 이미지

# 심각도나 고칠 수 있는 것만 남긴다 (급한 취약점만 추리기)
trivy image --severity HIGH,CRITICAL 이미지
trivy image --ignore-unfixed 이미지

# 취약점이 있으면 종료 코드로 실패시킨다 (CI 에서 빌드 실패시키기)
trivy image --exit-code 1 이미지

# 보고서를 파일로 받는다 (결과를 JSON 으로 받아 세기)
trivy image --format json --output 파일 이미지

# 이미지를 tar 파일로 받아 스캔한다 (tar 파일 스캔하기)
trivy image --input tar파일

# 이미지가 아닌 것을 스캔한다 (Dockerfile·YAML·디렉터리 스캔하기)
trivy config 폴더
trivy fs 폴더

# SBOM 을 만들고 스캔한다 (SBOM 만들고 스캔하기)
trivy image --format cyclonedx --output 파일 이미지
trivy sbom 파일

# DB 를 갱신하지 않고 스캔한다 (폐쇄망에서 DB 갱신 없이 스캔하기)
trivy image --skip-db-update 이미지
```

### 옵션을 정하는 세 방법

```bash
# 같은 옵션을 정하는 방법. 위가 아래를 이긴다
# 명령줄 플래그    --severity HIGH
# 환경 변수        TRIVY_SEVERITY=HIGH  (TRIVY_ 를 붙이고 대문자로 쓰고 - 는 _ 로 바꾼다)
# 설정 파일        trivy.yaml
```

세 방법의 우선순위와 환경 변수 이름 규칙은 공식 문서에 있습니다.[^config-order]



## 종료 코드

> 취약점을 찾아도 기본은 0 이고, `--exit-code` 를 줘야 취약점이 종료 코드로 드러납니다.[^exit]

```bash
# 0  스캔이 끝났다. 취약점을 찾았어도 기본은 0 이다
# N  --exit-code N 을 줬고 취약점을 찾았다
# 1  스캔이 깨졌다. 이미지를 찾지 못했을 때 1 을 받았다
# 위 코드는 「CI 에서 빌드 실패시키기」 에서 실행해 받은 값이다
# --exit-on-eol 은 EOL 운영체제를 만났을 때의 종료 코드를 정하며 이 시트에서 실행하지 않았다
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다. 「주의사항과 동작 원리」 의 예는 각자 필요한 상태를 만들고 지웁니다.

### 실습 준비

> 아래 블록을 차례로 붙여 넣으면 `trivy` 와 취약점 DB, 스캔할 이미지 넷이 준비됩니다. 모두 Ubuntu aarch64 VM 에서 root 로 실행했고 Docker Engine 이 있어야 합니다.

```bash
# 작업 폴더를 만들고 공식 릴리스에서 ARM64 묶음과 체크섬 파일을 받는다
mkdir -p /root/sheet-trivy && cd /root/sheet-trivy
V=0.76.2
B=https://github.com/aquasecurity/trivy/releases/download/v$V
curl -sSLO $B/trivy_${V}_Linux-ARM64.tar.gz
curl -sSLO $B/trivy_${V}_checksums.txt

# 체크섬을 맞춘 뒤 풀어서 설치한다
#   sha256sum -c   체크섬 파일의 값과 받은 파일을 맞대 본다
#   --ignore-missing   체크섬 파일에 있어도 받지 않은 파일은 건너뛴다
sha256sum -c --ignore-missing trivy_${V}_checksums.txt
tar -xzf trivy_${V}_Linux-ARM64.tar.gz trivy
install -m 0755 trivy /usr/local/bin/trivy
trivy --version
```

```bash
# 결과
trivy_0.76.2_Linux-ARM64.tar.gz: OK
Version: 0.76.2
```

```bash
# 이 시트의 모든 실행에 쓰는 환경 변수를 파일에 두고 읽어 들인다
cat > env.sh <<'EOF'
export TRIVY_CACHE_DIR=/root/sheet-trivy/cache
export TRIVY_SKIP_VERSION_CHECK=true
export TRIVY_DISABLE_TELEMETRY=true
EOF
source env.sh
```

`TRIVY_CACHE_DIR` 로 캐시를 작업 폴더 안에 두면 정리가 폴더 하나를 지우는 것으로 끝납니다. 버전을 고정하고 체크섬을 맞춰 받는 이유는 「침해된 0.69.4 릴리스」 에, 나머지 두 변수는 「버전 확인 요청이 나감」 에 있습니다.

```bash
# 스캔 전에 취약점 DB 만 먼저 받아 캐시 폴더에 둔다
#   --download-db-only   DB 를 내려받기만 하고 스캔하지 않는다
#   --no-progress        진행 막대를 숨긴다
trivy image --download-db-only --no-progress

# 설치한 trivy 와 받아 둔 DB 의 날짜를 본다
trivy version
```

```bash
# 결과
2026-11-23T21:21:07+09:00	INFO	[vulndb] Need to update DB
2026-11-23T21:21:07+09:00	INFO	[vulndb] Downloading vulnerability DB...
2026-11-23T21:21:07+09:00	INFO	[vulndb] Downloading artifact...	repo="mirror.gcr.io/aquasec/trivy-db:2"
2026-11-23T21:21:14+09:00	INFO	[vulndb] Artifact successfully downloaded	repo="mirror.gcr.io/aquasec/trivy-db:2"
Version: 0.76.2
Vulnerability DB:
  Version: 2
  UpdatedAt: 2026-11-23 07:04:04.632673631 +0000 UTC
  NextUpdate: 2026-11-24 07:04:04.63267311 +0000 UTC
  DownloadedAt: 2026-11-23 12:21:14.645528506 +0000 UTC
```

```bash
# 스캔할 이미지를 받아 sheet-trivy/ 이름으로 태그한다
#   pull -q   받는 진행 상황을 숨긴다
docker pull -q mirror.gcr.io/library/alpine:3.19 > /dev/null
docker pull -q mirror.gcr.io/library/alpine:3.23 > /dev/null
docker pull -q mirror.gcr.io/traefik/whoami:v1.10.1 > /dev/null
docker pull -q mirror.gcr.io/library/debian:12-slim > /dev/null
docker tag mirror.gcr.io/library/alpine:3.19 sheet-trivy/alpine:3.19
docker tag mirror.gcr.io/library/alpine:3.23 sheet-trivy/alpine:3.23
docker tag mirror.gcr.io/traefik/whoami:v1.10.1 sheet-trivy/whoami:1.10.1
docker tag mirror.gcr.io/library/debian:12-slim sheet-trivy/debian:12-slim

# 운영체제 패키지와 Go 바이너리가 함께 든 이미지를 하나 만든다
mkdir -p app
cat > app/Dockerfile <<'EOF'
FROM sheet-trivy/alpine:3.19
COPY --from=sheet-trivy/whoami:1.10.1 /whoami /usr/local/bin/whoami
EOF
#   build -q   빌드 로그를 숨긴다
docker build -q -t sheet-trivy/app:1 app 2>/dev/null > /dev/null

# 만든 이미지의 이름과 ID 를 본다
docker images --format '{{.Repository}}:{{.Tag}}  {{.ID}}  {{.Size}}' | grep '^sheet-trivy/' | sort
```

```bash
# 결과
sheet-trivy/alpine:3.19  6baf43584bcb  12.8MB
sheet-trivy/alpine:3.23  469c9ea410b9  14.6MB
sheet-trivy/app:1  b7c88ce9c164  19.8MB
sheet-trivy/debian:12-slim  734a72b3d614  138MB
sheet-trivy/whoami:1.10.1  6956a30c7d33  10.7MB
```

### 이미지 취약점 표 읽기

> `trivy image` 에 이미지 이름을 주면 요약 표와 취약점 표를 차례로 출력합니다.

```bash
# 이미지 하나를 스캔한다
#   -q   로그와 진행 막대를 숨기고 보고서만 남긴다
trivy image -q sheet-trivy/alpine:3.19
```

```bash
# 결과
# 앞 22줄만 싣는다 (전체 59줄)
# 줄은 113자에서 잘랐다
Report Summary

┌─────────────────────────────────────────┬────────┬─────────────────┬─────────┐
│                 Target                  │  Type  │ Vulnerabilities │ Secrets │
├─────────────────────────────────────────┼────────┼─────────────────┼─────────┤
│ sheet-trivy/alpine:3.19 (alpine 3.19.9) │ alpine │       10        │    -    │
└─────────────────────────────────────────┴────────┴─────────────────┴─────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)


sheet-trivy/alpine:3.19 (alpine 3.19.9)
=======================================
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)

┌───────────────┬────────────────┬──────────┬────────┬──────────────────────┬──────────────────────┬─────────────
│    Library    │ Vulnerability  │ Severity │ Status │  Installed Version   │    Fixed Version     │
├───────────────┼────────────────┼──────────┼────────┼──────────────────────┼──────────────────────┼─────────────
│ busybox       │ CVE-2024-58251 │ MEDIUM   │ fixed  │ 1.36.1-r20           │ 1.36.1-r21           │ In netstat i
│               │                │          │        │                      │                      │ of networ...
│               │                │          │        │                      │                      │ https://avd.
```

```bash
# 취약점 표의 열
# Library            취약한 패키지의 이름
# Vulnerability      취약점 ID(CVE 번호)
# Severity           심각도
# Status             이 배포판에서 고쳐졌는지. fixed 는 패치가 나왔다는 뜻이다
# Installed Version  이미지에 든 패키지의 버전
# Fixed Version      취약점이 고쳐진 버전
# Title              한 줄 설명. 위 출력은 줄을 잘라 보이지 않는다
```

같은 CVE 가 `busybox`·`busybox-binsh`·`ssl_client` 처럼 패키지마다 한 줄씩 나옵니다. 그래서 표의 줄 수는 CVE 수가 아니라 패키지와 CVE 의 짝 수입니다. `Status` 의 `affected` 는 영향은 받지만 패치가 아직 없다는 뜻입니다.[^status]

```bash
# 가장 새 태그를 스캔한다
trivy image -q sheet-trivy/alpine:3.23
```

```bash
# 결과
# 줄은 113자에서 잘랐다
Report Summary

┌─────────────────────────────────────────┬────────┬─────────────────┬─────────┐
│                 Target                  │  Type  │ Vulnerabilities │ Secrets │
├─────────────────────────────────────────┼────────┼─────────────────┼─────────┤
│ sheet-trivy/alpine:3.23 (alpine 3.23.8) │ alpine │        1        │    -    │
└─────────────────────────────────────────┴────────┴─────────────────┴─────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)


sheet-trivy/alpine:3.23 (alpine 3.23.8)
=======================================
Total: 1 (UNKNOWN: 0, LOW: 0, MEDIUM: 1, HIGH: 0, CRITICAL: 0)

┌─────────┬───────────────┬──────────┬────────┬───────────────────┬───────────────┬──────────────────────────────
│ Library │ Vulnerability │ Severity │ Status │ Installed Version │ Fixed Version │                           Tit
├─────────┼───────────────┼──────────┼────────┼───────────────────┼───────────────┼──────────────────────────────
│ zlib    │ CVE-2026-4738 │ MEDIUM   │ fixed  │ 1.3.2-r1          │ 1.4-r0        │ Improper Restriction of Opera
│         │               │          │        │                   │               │ Memory Buffe ......
│         │               │          │        │                   │               │ https://avd.aquasec.com/nvd/c
└─────────┴───────────────┴──────────┴────────┴───────────────────┴───────────────┴──────────────────────────────
```

### 급한 취약점만 추리기

> `--severity` 로 심각도를, `--ignore-unfixed` 로 아직 고칠 수 없는 것을, `--pkg-types` 로 패키지 종류를 걸러 건수를 줄입니다.

```bash
# 심각도로 거른다
#   --severity   표에 보일 심각도를 쉼표로 고른다
trivy image -q --severity HIGH,CRITICAL sheet-trivy/alpine:3.19 | grep -E '^Total'

# 취약점 건수가 많은 Debian 이미지에서 고칠 수 없는 것을 뺀다
#   --ignore-unfixed   고친 버전이 나오지 않은 취약점은 보이지 않는다
trivy image -q sheet-trivy/debian:12-slim | grep -E '^Total'
trivy image -q --ignore-unfixed sheet-trivy/debian:12-slim | grep -E '^Total|debian'

# 패키지 종류로 거른다
#   --pkg-types   os 는 운영체제 패키지, library 는 언어 의존성과 바이너리다
trivy image -q --pkg-types os sheet-trivy/app:1 | grep -E '^Total|^[a-z]'
trivy image -q --pkg-types library sheet-trivy/app:1 | grep -E '^Total|^[a-z]'
```

```bash
# 결과
Total: 2 (HIGH: 2, CRITICAL: 0)
Total: 244 (UNKNOWN: 17, LOW: 89, MEDIUM: 100, HIGH: 37, CRITICAL: 1)
│ sheet-trivy/debian:12-slim (debian 12.15) │ debian │        0        │    -    │
sheet-trivy/app:1 (alpine 3.19.9)
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
usr/local/bin/whoami (gobinary)
Total: 91 (UNKNOWN: 0, LOW: 4, MEDIUM: 56, HIGH: 29, CRITICAL: 2)
```

Debian 이미지는 244건이 전부 고친 버전이 없어서 `--ignore-unfixed` 를 주면 0건이 됩니다. 고칠 수 없는 것을 빼면 건수는 줄지만 그 취약점이 없어진 것은 아닙니다.[^unfixed]

`--pkg-types` 는 `os` 와 `library` 둘만 받습니다.[^pkg-types] 운영체제 패키지 10건과 Go 바이너리 91건이 한 이미지에서 따로 잡힙니다.

### CI 에서 빌드 실패시키기

> `--exit-code` 를 주면 취약점을 찾았을 때 그 코드로 끝나서 파이프라인이 실패합니다.

```bash
# 취약점이 있어도 기본은 0 으로 끝난다
trivy image -q sheet-trivy/alpine:3.19 > /dev/null; echo "기본: $?"

# 취약점이 있으면 지정한 코드로 끝나게 한다
#   --exit-code   취약점을 찾았을 때 돌려줄 종료 코드다
trivy image -q --exit-code 1 sheet-trivy/alpine:3.19 > /dev/null; echo "--exit-code 1: $?"
trivy image -q --exit-code 1 --severity CRITICAL sheet-trivy/alpine:3.19 > /dev/null; echo "CRITICAL 만: $?"

# 스캔이 깨져서 실패하는 경우도 1 이라 취약점과 구분되지 않는다
trivy image -q --exit-code 1 sheet-trivy/nosuch:1 > /dev/null 2>&1; echo "없는 이미지, --exit-code 1: $?"

# 취약점에는 1 이 아닌 코드를 준다
trivy image -q --exit-code 10 sheet-trivy/alpine:3.19 > /dev/null; echo "취약점, --exit-code 10: $?"
trivy image -q --exit-code 10 sheet-trivy/nosuch:1 > /dev/null 2>&1; echo "없는 이미지, --exit-code 10: $?"
```

```bash
# 결과
기본: 0
--exit-code 1: 1
CRITICAL 만: 0
없는 이미지, --exit-code 1: 1
취약점, --exit-code 10: 10
없는 이미지, --exit-code 10: 1
```

`--severity CRITICAL` 로 좁히면 이 이미지에는 CRITICAL 이 없어서 0 으로 끝납니다. 심각도 기준은 `--severity` 와 `--exit-code` 를 함께 줘서 정합니다.[^exit-sev]

이미지를 찾지 못한 스캔 실패도 1 로 끝나므로, `--exit-code 1` 에서는 취약점 때문인지 스캔이 깨진 것인지 가려지지 않습니다. 취약점에 1 이 아닌 코드를 주면 둘이 갈립니다.

### 결과를 JSON 으로 받아 세기

> `--format json` 과 `--output` 으로 보고서를 파일에 쓰고 `jq` 로 심각도별 건수를 셉니다.

```bash
# 결과를 JSON 파일로 받는다
#   --format   보고서 형식을 table·json·cyclonedx 같은 것으로 정한다
#   --output   표준 출력 대신 파일에 쓴다
trivy image -q \
  --format json \
  --output alpine319.json \
  sheet-trivy/alpine:3.19

# 최상위 키와 이미지 정보를 본다
jq -c 'keys' alpine319.json
jq -c '{ArtifactName, ArtifactType, OS: .Metadata.OS}' alpine319.json

# 심각도별 건수를 센다
jq -r '.Results[].Vulnerabilities | group_by(.Severity)[] | "\(.[0].Severity) \(length)"' alpine319.json

# 취약점 ID, 심각도, 패키지, 설치 버전, 고친 버전을 탭으로 뽑는다
jq -r '.Results[].Vulnerabilities[] | [.VulnerabilityID, .Severity, .PkgName, .InstalledVersion, .FixedVersion] | @tsv' alpine319.json | head -4
```

```bash
# 결과
["ArtifactID","ArtifactName","ArtifactType","CreatedAt","Metadata","ReportID","Results","SchemaVersion","Trivy"]
{"ArtifactName":"sheet-trivy/alpine:3.19","ArtifactType":"container_image","OS":{"Family":"alpine","Name":"3.19.9","EOSL":true}}
HIGH 2
LOW 3
MEDIUM 5
CVE-2024-58251	MEDIUM	busybox	1.36.1-r20	1.36.1-r21
CVE-2025-46394	LOW	busybox	1.36.1-r20	1.36.1-r21
CVE-2024-58251	MEDIUM	busybox-binsh	1.36.1-r20	1.36.1-r21
CVE-2025-46394	LOW	busybox-binsh	1.36.1-r20	1.36.1-r21
```

`OS.EOSL` 이 `true` 이면 이 배포판 버전은 지원이 끝났다는 표시입니다. 이런 이미지는 보안 업데이트가 없어서 탐지가 충분하지 않을 수 있다고 공식 문서가 적습니다.[^eol]

### tar 파일 스캔하기

> `--input` 으로 `docker save` 가 만든 tar 파일을 스캔하면 데몬과 레지스트리 없이 반입 전 검사를 할 수 있습니다.

```bash
# 이미지를 tar 로 내보내고 그 파일을 스캔한다
#   --input   이미지 이름 대신 tar 파일 경로를 받는다
docker save -o alpine319.tar sheet-trivy/alpine:3.19
ls -l alpine319.tar

# 데몬 주소를 없는 소켓으로 바꿔도 tar 스캔은 된다
DOCKER_HOST=unix:///nonexistent trivy image -q --input alpine319.tar | grep -E '^Total|alpine319'
```

```bash
# 결과
-rw------- 1 root root 3465216 Nov 23 21:21 alpine319.tar
│ alpine319.tar (alpine 3.19.9) │ alpine │       10        │    -    │
alpine319.tar (alpine 3.19.9)
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
```

tar 안에는 이미지 이름이 대상으로 잡히지 않아 요약 표의 대상 이름이 파일 이름으로 나옵니다. 폐쇄망 반입 절차는 [이미지 구조와 digest](../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) 와 [docker 참조 시트](../../../../08_cloud/docs/cmd/container/docker.md) 가 맡습니다.

### Dockerfile·YAML·디렉터리 스캔하기

> `trivy config` 는 설정 파일의 잘못된 설정을, `trivy fs` 는 디렉터리의 의존성 취약점과 시크릿을 찾습니다.

```bash
# 설정 오류를 찾을 예제 Dockerfile 과 Pod YAML 을 만든다
mkdir -p cfg
cat > cfg/Dockerfile <<'EOF'
FROM alpine:3.19
RUN apk add curl
EOF
cat > cfg/pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: demo
spec:
  containers:
    - name: demo
      image: alpine:3.19
      securityContext:
        privileged: true
EOF

# 폴더의 설정 파일을 검사한다
#   --table-mode summary   요약 표만 보인다 (--help 가 실험 기능이라 표시해 바뀔 수 있다)
trivy config -q --table-mode summary cfg

# HIGH 이상만 거르고 지적 제목만 뽑는다
trivy config -q --severity HIGH,CRITICAL cfg | grep -E '^(DS|KSV)-'
```

```bash
# 결과
Report Summary

┌────────────┬────────────┬───────────────────┐
│   Target   │    Type    │ Misconfigurations │
├────────────┼────────────┼───────────────────┤
│ Dockerfile │ dockerfile │         3         │
├────────────┼────────────┼───────────────────┤
│ pod.yaml   │ kubernetes │        17         │
└────────────┴────────────┴───────────────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)

DS-0002 (HIGH): Specify at least 1 USER command in Dockerfile with non-root user as argument
DS-0025 (HIGH): '--no-cache' is missed: apk add curl
KSV-0014 (HIGH): Container 'demo' of Pod 'demo' should set 'securityContext.readOnlyRootFilesystem' to true
KSV-0017 (HIGH): Container 'demo' of Pod 'demo' should set 'securityContext.privileged' to false
KSV-0118 (HIGH): pod demo in default namespace is using the default security context, which allows root privileges
```

Dockerfile 에서 3건, Pod YAML 에서 17건이 나왔고 `--severity HIGH,CRITICAL` 로 거른 지적 제목이 5건입니다. 설정 검사는 이미지 이름이 아니라 폴더를 받습니다.

```bash
# 의존성 파일과 시크릿이 든 예제 폴더를 만든다
mkdir -p proj
echo 'flask==0.12' > proj/requirements.txt
echo 'secret="dummyvalue12345"' > proj/app.conf
cat > proj/creds.txt <<'EOF'
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

# 폴더를 스캔한다. 기본 스캐너는 vuln 과 secret 이다
#   fs   이미지가 아니라 디렉터리를 대상으로 한다
trivy fs -q proj | grep -E '^Total|^[a-z]'

# 시크릿만 스캔한다. 기본 규칙에 걸린 건수를 센다
#   --scanners   켤 스캐너를 쉼표로 고른다
echo "기본 규칙: $(trivy fs -q --scanners secret proj | grep -c '^Total')건"

# 문서의 예제 규칙을 trivy-secret.yaml 로 두면 app.conf 가 걸린다
cat > proj/trivy-secret.yaml <<'EOF'
rules:
  - id: rule1
    category: general
    title: Generic Rule
    severity: HIGH
    regex: (?i)(?P<key>(secret))(=|:).{0,5}['"](?P<secret>[0-9a-zA-Z\-_=]{8,64})['"]
EOF
trivy fs -q --scanners secret --secret-config proj/trivy-secret.yaml proj | grep -E '^Total|^[a-z]|^HIGH'
```

```bash
# 결과
requirements.txt (pip)
Total: 4 (UNKNOWN: 0, LOW: 1, MEDIUM: 0, HIGH: 3, CRITICAL: 0)
기본 규칙: 0건
app.conf (secrets)
Total: 1 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 1, CRITICAL: 0)
HIGH: general (rule1)
```

AWS 문서가 예로 쓰는 키(`creds.txt`)는 기본 규칙에 걸리지 않습니다. 내용에 `example` 이 들어 있으면 시크릿으로 보지 않는 내장 허용 규칙이 있기 때문입니다.[^allow-example] `app.conf` 의 값은 이 시트가 지어낸 더미이고, 걸린 것은 공식 문서의 예제 규칙 `rule1` 입니다.[^secret-rule]

### SBOM 만들고 스캔하기

> `--format cyclonedx` 나 `spdx-json` 으로 SBOM 을 만들고 `trivy sbom` 으로 이미지 없이 스캔합니다.

```bash
# 이미지의 SBOM 을 CycloneDX 와 SPDX 로 만든다
trivy image -q --format cyclonedx --output alpine319.cdx.json sheet-trivy/alpine:3.19
trivy image -q --format spdx-json --output alpine319.spdx.json sheet-trivy/alpine:3.19

# 형식과 패키지 수를 본다
jq -c '{bomFormat, specVersion, components: (.components | length)}' alpine319.cdx.json
jq -c '{spdxVersion, packages: (.packages | length)}' alpine319.spdx.json

# SBOM 파일을 이미지 없이 스캔한다
trivy sbom -q alpine319.cdx.json | grep -E '^Total|alpine319'
trivy sbom -q alpine319.spdx.json | grep -E '^Total'
```

```bash
# 결과
{"bomFormat":"CycloneDX","specVersion":"1.7","components":16}
{"spdxVersion":"SPDX-2.3","packages":17}
│ alpine319.cdx.json (alpine 3.19.9) │ alpine │       10        │
alpine319.cdx.json (alpine 3.19.9)
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
```

SBOM 에서 읽은 패키지로 스캔한 건수가 이미지를 직접 스캔한 10건과 같습니다.[^sbom]

### 폐쇄망에서 DB 갱신 없이 스캔하기

> DB 파일을 미리 받아 옮겨 두고 `--skip-db-update` 를 주면 갱신을 시도하지 않고 스캔합니다.

```bash
# 받아 둔 DB 가 어떤 파일인지 본다
ls -l cache/db

# 캐시 폴더를 옮기는 것을 mv 로 흉내 낸다
mkdir -p cache-airgap
mv cache/db cache-airgap/db

# 네트워크가 없는 네임스페이스에서 갱신 없이 스캔한다
#   unshare -n         네트워크 인터페이스가 없는 새 네임스페이스에서 명령을 실행한다
#   --cache-dir        이 실행에만 캐시 폴더를 바꾼다
#   --skip-db-update   취약점 DB 를 갱신하지 않는다
#   --skip-java-db-update   Java DB 를 갱신하지 않는다
#   --skip-check-update     검사 규칙 묶음을 갱신하지 않는다
#   --offline-scan     의존성을 알아내려는 API 요청을 보내지 않는다
unshare -n trivy image -q \
  --cache-dir cache-airgap \
  --skip-db-update \
  --skip-java-db-update \
  --skip-check-update \
  --offline-scan \
  sheet-trivy/alpine:3.19 | grep -E '^Total'

# DB 를 제자리로 돌린다
mv cache-airgap/db cache/db
```

```bash
# 결과
total 1771352
-rw-r--r-- 1 root root        152 Nov 23 21:21 metadata.json
-rw-r--r-- 1 root root 1813860352 Nov 23 16:12 trivy.db
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
```

`unshare -n` 안에서도 로컬 Docker 의 이미지를 찾았고, 그 안에서 DB 를 받으려는 시도는 「DB 내려받기 실패」 에서 실패합니다. 갱신을 끄는 세 옵션과 `--offline-scan` 의 쓰임은 공식 문서에 있습니다.[^airgap]

### 알고 넘어갈 취약점 적어 두기

> 프로젝트 폴더의 `.trivyignore` 에 취약점 ID 를 적으면 다음 스캔부터 표에서 빠집니다.

```bash
# 넘어갈 취약점을 .trivyignore 에 적는다
cat > .trivyignore <<'EOF'
# musl 은 이미지를 다시 빌드할 때 고친다
CVE-2026-40200
CVE-2026-6042 exp:2026-12-31
EOF

# 적은 뒤 건수를 본다
trivy image -q sheet-trivy/alpine:3.19 | grep -E '^Total'

# 무시된 것을 따로 보인다
#   --show-suppressed   무시된 취약점을 별도 표로 보인다 (--help 가 실험 기능이라 표시해 바뀔 수 있다)
trivy image -q --show-suppressed sheet-trivy/alpine:3.19 | tail -12

# 다른 폴더에서 돌리면 .trivyignore 를 읽지 못한다
(cd cfg && trivy image -q sheet-trivy/alpine:3.19 | grep -E '^Total')
```

```bash
# 결과
Total: 6 (UNKNOWN: 0, LOW: 3, MEDIUM: 3, HIGH: 0, CRITICAL: 0)
=====================================
┌────────────┬────────────────┬──────────┬─────────┬───────────┬──────────────┐
│  Library   │ Vulnerability  │ Severity │ Status  │ Statement │    Source    │
├────────────┼────────────────┼──────────┼─────────┼───────────┼──────────────┤
│ musl       │ CVE-2026-40200 │ HIGH     │ ignored │ N/A       │ .trivyignore │
│            ├────────────────┼──────────┤         │           │              │
│            │ CVE-2026-6042  │ MEDIUM   │         │           │              │
├────────────┼────────────────┼──────────┤         │           │              │
│ musl-utils │ CVE-2026-40200 │ HIGH     │         │           │              │
│            ├────────────────┼──────────┤         │           │              │
│            │ CVE-2026-6042  │ MEDIUM   │         │           │              │
└────────────┴────────────────┴──────────┴─────────┴───────────┴──────────────┘
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
```

10건에서 6건으로 줄었습니다. 날짜(`exp:`)를 붙이면 그날까지만 넘어가는 항목이 됩니다.[^ignorefile]

`.trivyignore` 는 `trivy` 를 실행한 폴더에서 읽으므로 다른 폴더에서 돌리면 적용되지 않습니다. 파일 위치는 `--ignorefile` 로 바꿉니다.

### 실습 정리

> 만든 이미지 태그와 작업 폴더를 지웁니다. 설치한 `trivy` 바이너리는 남깁니다.

```bash
# 이미지 태그와 만든 이미지를 지운다
docker rmi \
  sheet-trivy/app:1 \
  sheet-trivy/alpine:3.19 \
  sheet-trivy/alpine:3.23 \
  sheet-trivy/whoami:1.10.1 \
  sheet-trivy/debian:12-slim > /dev/null

# 받을 때 쓴 원본 태그를 지운다
docker rmi \
  mirror.gcr.io/library/alpine:3.19 \
  mirror.gcr.io/library/alpine:3.23 \
  mirror.gcr.io/traefik/whoami:v1.10.1 \
  mirror.gcr.io/library/debian:12-slim > /dev/null

# 작업 폴더와 캐시를 지운다
cd /root
rm -rf /root/sheet-trivy
```



## 주의사항과 동작 원리

> 아래 예는 「실습 정리」 가 지운 상태를 다시 만들어 쓰고, 마지막 항목 뒤에 지웁니다.

```bash
# 정리에서 지운 상태를 다시 만든다
mkdir -p /root/sheet-trivy && cd /root/sheet-trivy
cat > env.sh <<'EOF'
export TRIVY_CACHE_DIR=/root/sheet-trivy/cache
export TRIVY_SKIP_VERSION_CHECK=true
export TRIVY_DISABLE_TELEMETRY=true
EOF
source env.sh
trivy image --download-db-only --no-progress 2> /dev/null
docker pull -q mirror.gcr.io/library/alpine:3.19 > /dev/null
docker tag mirror.gcr.io/library/alpine:3.19 sheet-trivy/alpine:3.19
```

### 취약점이 많은데 CI 가 통과함

> `--exit-code` 가 없으면 `trivy` 는 0 으로 끝나고, 파이프 뒤에 다른 명령이 있으면 `--exit-code` 를 줘도 그 명령의 코드가 남습니다.

```bash
# 취약점이 있어도 trivy 는 0 으로 끝난다
trivy image -q sheet-trivy/alpine:3.19 | grep -E '^Total'; echo "파이프 끝: $?"

# --exit-code 1 을 줘도 grep 뒤에서는 grep 의 코드가 남는다
trivy image -q --exit-code 1 sheet-trivy/alpine:3.19 | grep -E '^Total'; echo "파이프 끝: $?"

# pipefail 을 켜면 trivy 의 코드가 남는다
set -o pipefail
trivy image -q --exit-code 1 sheet-trivy/alpine:3.19 | grep -E '^Total'; echo "pipefail: $?"
set +o pipefail
```

```bash
# 결과
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
파이프 끝: 0
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
파이프 끝: 0
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
pipefail: 1
```

셸은 파이프의 마지막 명령의 코드를 돌려주므로 `grep` 이 0 으로 끝나면 `trivy` 의 1 이 가려집니다. `set -o pipefail` 을 켜면 `trivy` 의 코드가 남습니다. 기본값이 0 이라는 것은 공식 문서에 적혀 있습니다.[^exit]

### 어제와 오늘 결과가 다름

> 취약점 DB 는 계속 갱신되므로 같은 이미지도 날짜가 지나면 건수가 달라지고, 이 시트의 출력은 DB 날짜 2026-11-23 의 값입니다.

```bash
# 받아 둔 DB 의 갱신 날짜를 본다
jq . cache/db/metadata.json

# 같은 날짜의 DB 로 고정해 다시 스캔한다
#   --skip-db-update   DB 가 오래됐어도 내려받지 않는다
trivy image -q --skip-db-update sheet-trivy/alpine:3.19 | grep -E '^Total'
```

```bash
# 결과
{
  "Version": 2,
  "NextUpdate": "2026-11-24T07:04:04.63267311Z",
  "UpdatedAt": "2026-11-23T07:04:04.632673631Z",
  "DownloadedAt": "2026-11-23T12:21:44.379054944Z"
}
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
```

`UpdatedAt` 은 DB 를 만든 시각이고 `NextUpdate` 는 그 뒤에 새 DB 를 받을 수 있는 시각입니다. `--skip-db-update` 를 주면 DB 가 오래돼도 받지 않으므로 날짜를 고정해 재현할 때 씁니다.

### 로컬 이미지와 저장소 이미지 헷갈림

> `trivy` 는 로컬 Docker, containerd, Podman, 레지스트리 순으로 이미지를 찾으므로 같은 이름이면 로컬이 먼저입니다.[^image-src]

```bash
# 이름이 같을 때 어느 쪽을 스캔하는지 이미지 출처를 하나로 고정해 본다
#   --image-src   이미지를 찾을 곳을 우선순위대로 고른다
trivy image -q --image-src docker sheet-trivy/alpine:3.19 | grep -E '^Total'
trivy image -q --image-src remote sheet-trivy/alpine:3.19 2>&1
```

```bash
# 결과
# 줄은 140자에서 잘랐다
Total: 10 (UNKNOWN: 0, LOW: 3, MEDIUM: 5, HIGH: 2, CRITICAL: 0)
2026-11-23T21:21:53+09:00	FATAL	Fatal error	run error: image scan error: scan error: unable to initialize a scan service: unable to initiali
	* remote error: GET https://index.docker.io/v2/sheet-trivy/alpine/manifests/3.19: UNAUTHORIZED: authentication required; [map[Action:pull C
```

`--image-src` 는 찾을 곳과 순서를 정합니다. 로컬에만 있는 이름을 `remote` 로 고정하면 레지스트리 인증 오류가 납니다. 저장소의 이미지를 스캔하려면 `remote` 만 고르고 저장소에 있는 이름을 줍니다.

### DB 내려받기 실패

> 캐시가 비어 있는데 DB 를 받을 수 없으면 스캔이 시작되지 못하고, 이때 갱신을 끄면 첫 실행 오류가 납니다.

```bash
# 캐시가 비어 있고 네트워크가 없으면 DB 를 받지 못해 실패한다
mkdir -p cache-empty
unshare -n trivy image -q --cache-dir cache-empty sheet-trivy/alpine:3.19 2>&1 | head -3

# 캐시가 비어 있을 때 갱신을 끄면 첫 실행 오류가 난다
trivy image -q --cache-dir cache-empty --skip-db-update sheet-trivy/alpine:3.19 2>&1

# 캐시 폴더의 크기를 본다
du -sh cache/*
```

```bash
# 결과
# 줄은 140자에서 잘랐다
2026-11-23T21:21:57+09:00	FATAL	Fatal error	run error: init error: DB error: failed to download vulnerability DB: OCI artifact error: failed
	* Get "https://mirror.gcr.io/v2/": dial tcp: lookup mirror.gcr.io on 0.250.250.200:53: dial udp 0.250.250.200:53: connect: network is unrea

2026-11-23T21:21:57+09:00	FATAL	Fatal error	run error: init error: DB error: database error: --skip-db-update cannot be specified on the fir
1.7G	cache/db
36K	cache/fanal
```

기본으로 받는 곳은 `mirror.gcr.io/aquasec` 이고, 일시적 오류(429·5xx)가 나면 `ghcr.io/aquasecurity` 로 넘어갑니다.[^db-repo] 받은 DB 는 캐시 폴더의 `db` 에 1.7G 로 풀립니다. 이전 스캔의 분석 결과(`fanal`)도 같은 폴더에 쌓입니다.[^cache]

### 스캔이 오래 걸림

> 기본으로 취약점과 시크릿 스캐너가 함께 켜져 있고, 시크릿 스캔이 느리면 `--scanners vuln` 으로 끕니다.

```bash
# 기본으로 켜진 스캐너를 로그에서 본다
trivy image --no-progress sheet-trivy/alpine:3.19 2>&1 | grep 'scanning is'

# 취약점만 켜면 secret 줄이 사라진다
#   --scanners vuln   취약점 스캐너만 켠다
trivy image --no-progress --scanners vuln sheet-trivy/alpine:3.19 2>&1 | grep 'scanning is'
```

```bash
# 결과
2026-11-23T21:21:57+09:00	INFO	[vuln] Vulnerability scanning is enabled
2026-11-23T21:21:57+09:00	INFO	[secret] Secret scanning is enabled
2026-11-23T21:21:57+09:00	INFO	[secret] If your scanning is slow, please try '--scanners vuln' to disable secret scanning
2026-11-23T21:21:57+09:00	INFO	[vuln] Vulnerability scanning is enabled
```

로그가 `--scanners vuln` 을 직접 권합니다. 공식 문서도 기본이 취약점과 시크릿이라고 적습니다.[^scanners] 이 VM 의 작은 이미지에서는 시간 차이를 재지 않았습니다.

### 침해된 0.69.4 릴리스

> 2026-03-19 에 침해된 자격 증명으로 악성 Trivy 0.69.4 릴리스가 배포된 일이 있어, 이 시트는 버전을 고정하고 체크섬을 맞춰 받습니다.

```bash
# 침해된 0.69.4 ARM64 묶음의 해시가 이 체크섬 파일에 있는지 센다
V=0.76.2
curl -sSLO https://github.com/aquasecurity/trivy/releases/download/v$V/trivy_${V}_checksums.txt
grep -c e401ae1e6d2442fa9a0c79dc0f3b0457ecfebf74a9c0a920159c49437f663aef trivy_${V}_checksums.txt
grep 'Linux-ARM64.tar.gz$' trivy_${V}_checksums.txt
```

```bash
# 결과
0
ab9d51f86e6a5fb936f605faff6b593ac51bc378fff4d3e8b9d58358b9c367c3  trivy_0.76.2_Linux-ARM64.tar.gz
```

공지가 밝힌 침해 대상은 0.69.4 바이너리와 이미지, Docker Hub 의 0.69.5·0.69.6 이미지, `trivy-action` 과 `setup-trivy` 의 태그입니다. 안전한 바이너리로는 0.69.2 와 0.69.3 을 듭니다.[^advisory]

이 시트가 쓰는 0.76.2 는 공지의 영향 범위 밖에 있는 이후 릴리스입니다. 침해된 0.69.4 ARM64 묶음의 해시는 위처럼 체크섬 파일에 없었습니다. 릴리스에 붙은 sigstore 서명 파일은 검증하지 않았습니다.

### 버전 확인 요청이 나감

> `trivy` 는 새 버전을 확인하고 사용 통계를 모을 때 `check.trivy.dev` 로 요청을 보내고, 끄려면 두 옵션을 모두 줘야 합니다.

```bash
# 버전 확인과 텔레메트리를 끄는 옵션을 도움말에서 찾는다
trivy image --help | grep -E 'skip-version-check|disable-telemetry'
```

```bash
# 결과
      --disable-telemetry           disable sending anonymous usage data to Aqua
      --skip-version-check          suppress notices about version updates and Trivy announcements
```

공식 문서는 버전 확인과 텔레메트리가 서로 독립된 기능이라 한쪽만 끄면 이 도메인 연결이 다 막히지 않는다고 적습니다.[^vercheck] 「실습 준비」 의 `env.sh` 가 두 환경 변수로 이 시트의 모든 실행에서 둘을 껐습니다.

### 이 절의 실습 정리

```bash
# 이 절에서 만든 것을 지운다
docker rmi sheet-trivy/alpine:3.19 mirror.gcr.io/library/alpine:3.19 > /dev/null
cd /root
rm -rf /root/sheet-trivy
```



## 관련 문서

> 이어서 볼 시트와 책 노트입니다.

- [crane 참조 시트](crane.md) — 레지스트리의 이미지를 읽고 옮기는 명령
- [믿을 수 있는 이미지만 들이기](../../../../08_cloud/book/cks-study-guide/06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md) — 스캔을 하는 이유와 심각도의 뜻
- [이미지 작게 만들고 미리 검사하기](../../../../08_cloud/book/cks-study-guide/06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md) — Dockerfile 과 매니페스트를 미리 검사하는 도구
- [이미지 구조와 digest](../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) — 이미지를 이루는 층과 digest 의 구조



## 참고 자료

> 검증 환경과 근거 자료, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04.1 LTS VM(aarch64), trivy 0.76.2, Docker Engine 29.1.3
- 가장 새 버전: trivy 0.76.2 (2026-11-05 릴리스, 2026-11-23 에 GitHub API 로 확인)
- [trivy 0.76.2 릴리스](https://github.com/aquasecurity/trivy/releases/tag/v0.76.2)
- [GHSA-69fq-xp46-6x23 공급망 침해 공지](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23)
- [trivy 0.76 공식 문서](https://github.com/aquasecurity/trivy/tree/v0.76.2/docs/guide)

[^db-local]: air-gap 문서는 필요한 외부 자원으로 취약점 DB 를 들고 DB 를 OCI 이미지로 받는다고 적습니다. 이 시트는 `unshare -n` 으로 네트워크를 끊은 채 캐시된 DB 로 스캔이 되는 것을 실행해 확인했습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/advanced/air-gap.md
[^latest]: 2026-11-23 에 `https://api.github.com/repos/aquasecurity/trivy/releases/latest` 가 `v0.76.2`, 게시일 2026-11-05 를 돌려줬습니다. 같은 릴리스에 `trivy_0.76.2_Linux-ARM64.tar.gz` 와 `trivy_0.76.2_checksums.txt` 가 있습니다. https://github.com/aquasecurity/trivy/releases/tag/v0.76.2
[^config-order]: 문서는 우선순위를 "CLI flags (overrides all other settings)", "Environment variables (overrides config file settings)", "Configuration file" 순으로 적고, 환경 변수 이름은 "Add `TRIVY_` prefix", "All uppercase letters", "Replace `-` with `_`" 로 만든다고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/index.md
[^exit]: others 문서에 "By default, `Trivy` exits with code 0 even when security issues are detected." 와 "Use the `--exit-code` option if you want to exit with a non-zero exit code." 가 있습니다. 이미지를 찾지 못했을 때 1 로 끝난 것은 이 시트의 실측입니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/others.md
[^exit-sev]: others 문서는 심각도를 좁히는 예로 "`trivy image --exit-code 0 --severity MEDIUM,HIGH ruby:2.4.0`" 와 "`trivy image --exit-code 1 --severity CRITICAL ruby:2.4.0`" 를 듭니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/others.md
[^status]: filtering 문서의 상태 목록에 "`affected`: this package is affected by this vulnerability on this platform, but there is no patch released yet" 와 "`fixed`: this vulnerability is fixed on this platform" 가 있습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/filtering.md
[^unfixed]: vulnerability 문서는 고친 버전이 아직 배포되지 않은 취약점을 숨기는 플래그로 `--ignore-unfixed` 를 설명하고, `--help` 는 "display only fixed vulnerabilities" 라고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/scanner/vulnerability.md
[^pkg-types]: `trivy image --help` 에 "`--pkg-types strings   list of package types (allowed values: os,library) (default [os,library])`" 가 있습니다.
[^eol]: others 문서에 "Sometimes you may surprisingly get 0 vulnerabilities in an old image" 와 "`--exit-on-eol` can fail scanning on EOL OS with a non-zero code." 가 있고, 같은 문서의 로그 예에 "The vulnerability detection may be insufficient because security updates are not provided" 가 있습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/others.md
[^allow-example]: 내장 허용 규칙 파일에 ID 가 "examples" 인 규칙이 있고, 그 Description 은 "Avoid example files and paths" 이며, 정규식은 `MustCompile("(?i)example")` 입니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/pkg/fanal/secret/builtin-allow-rules.go AWS IAM 사용자 가이드가 예로 쓰는 키 값 `AKIAIOSFODNN7EXAMPLE` 은 이 페이지에서 직접 확인했습니다. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
[^secret-rule]: secret 문서의 `trivy-secret.yaml` 예제에 `id: rule1`, `severity: HIGH` 와 이 시트가 쓴 정규식이 있고, `--secret-config` 로 파일 경로를 바꿀 수 있다고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/scanner/secret.md
[^sbom]: `trivy sbom --help` 가 "Scan SBOM for vulnerabilities and licenses" 라고 적고, sbom 문서는 "Trivy can generate SBOM in the [CycloneDX][cyclonedx] format." 라고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/supply-chain/sbom.md
[^airgap]: db 문서가 `--skip-db-update`·`--skip-java-db-update`·`--skip-check-update` 와 `--download-db-only` 를 설명하고, air-gap 문서는 Maven Central 로 가는 요청을 `--offline-scan` 으로 막는다고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/db.md https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/advanced/air-gap.md
[^ignorefile]: filtering 문서의 `.trivyignore` 예에 "Accept the risk until 2023-01-01" 주석과 `CVE-2019-14697 exp:2023-01-01` 줄이 있습니다. `trivy image --help` 는 `--ignorefile` 의 기본값을 `.trivyignore` 로 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/filtering.md
[^image-src]: container_image 문서에 "it will first look in the local Docker Engine, then Containerd, Podman, and finally container registry." 가 있고 `--image-src` 로 바꿀 수 있다고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/target/container_image.md
[^db-repo]: db 문서에 "Trivy will attempt to pull images from the following registries in the order specified." 와 "In case of transient errors (e.g. status 429 or 5xx), Trivy will fall back to alternative registries in the order specified." 가 있고 기본 위치 `mirror.gcr.io/aquasec`, `ghcr.io/aquasecurity` 가 있습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/db.md
[^cache]: cache 문서가 캐시 폴더에 담기는 것으로 스캔 캐시와 취약점 DB 를 들고, `--cache-dir` 로 위치를 바꾼다고 적습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/configuration/cache.md
[^scanners]: container_image 문서에 "By default, vulnerability and secret scanning are enabled, and you can configure that with `--scanners`." 가 있습니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/target/container_image.md
[^advisory]: 공지에 "On March 19, 2026, a threat actor used compromised credentials to publish a malicious Trivy v0.69.4 release" 가 있습니다. 「Update to Known-Safe Versions」 표의 Trivy binary 행에는 "v0.69.2, v0.69.3" 이 있습니다. 영향 목록에는 0.69.4 와 Docker Hub 의 0.69.5·0.69.6 이미지가 있고, 침해 지표(Indicators of Compromise) 목록의 실행 파일 SHA256 에 `trivy_0.69.4_Linux-ARM64.tar.gz` 의 값이 있습니다. https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23
[^vercheck]: air-gap 문서에 "Note that these are two independent features controlled by separate flags — using only one of them is not sufficient to prevent all connections to this domain." 가 있고, 같은 문서가 `trivy image --skip-version-check --disable-telemetry <image>` 를 예로 듭니다. https://github.com/aquasecurity/trivy/blob/v0.76.2/docs/guide/advanced/air-gap.md
