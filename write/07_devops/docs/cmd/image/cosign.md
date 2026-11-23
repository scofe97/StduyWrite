---
title: "cosign 참조 시트"
tags: ["devops", "command", "image", "cosign", "signature", "supply-chain"]
status: draft
source:
  - "cosign v3.1.4 `cosign --help` 와 하위 명령 `--help` 원문 (OrbStack Ubuntu 26.04.1 VM 실측)"
  - "https://github.com/sigstore/cosign/releases/tag/v3.1.4"
  - "https://github.com/sigstore/cosign/blob/v3.1.4/CHANGELOG.md"
  - "https://github.com/sigstore/cosign/blob/v3.1.4/cmd/cosign/cli/options/sign.go"
  - "https://github.com/sigstore/cosign/blob/v3.1.4/cmd/cosign/cli/signcommon/common.go"
  - "https://github.com/sigstore/cosign/blob/v3.1.4/cmd/cosign/errors/exit_codes.go"
  - "https://github.com/sigstore/cosign/blob/v3.1.4/cmd/cosign/cli/sign/privacy/privacy.go"
  - "https://docs.sigstore.dev/cosign/signing/signing_with_containers/"
  - "https://docs.sigstore.dev/cosign/verifying/verify/"
related:
  - "../README.md"
  - "../../../../08_cloud/book/cks-study-guide/06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md"
  - "../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md"
  - "./crane.md"
  - "./trivy.md"
updated: "2026-11-23"
---

# cosign 참조 시트

---

> 컨테이너 이미지와 일반 파일에 서명하고, 받는 쪽이 공개 키로 확인하고, 서명이 실패하는 경우를 가려내는 `cosign` 명령을 공개 로그에 아무것도 올리지 않고 돌려 본 예제로 모았습니다.

## 개요

> `cosign` 은 이미지 digest 에 서명을 만들어 같은 저장소에 함께 두고, 받는 쪽이 공개 키로 그 서명을 확인하게 하는 CLI 입니다.

서명은 이미지 안이 아니라 이미지를 가리키는 별도 객체로 저장소에 놓입니다. 서명 방식은 둘입니다. 키 쌍으로 서명하는 방식(`--key`)과, 로그인(OIDC)으로 인증한 뒤 일회용 키로 서명하는 키 없는 방식(keyless)입니다. 왜 서명을 검증하는지는 CKS 정독 노트가 설명하므로 이 시트는 명령만 다룹니다.

```bash
# 서명하는 쪽과 받는 쪽이 같은 저장소를 통해 만나는 길
# 서명하는 쪽  cosign sign --key cosign.key  →  저장소(이미지 digest 를 가리키는 서명 객체)
# 받는 쪽      cosign verify --key cosign.pub ←  같은 저장소에서 서명을 읽어 확인
```

이 시트는 키 쌍 방식만 실행했습니다. 키 없는 방식은 공개 Sigstore 로그에 기록이 남아 실행하지 않았습니다.

서명이 된 명령은 모두 로그에 올리지 않는 서명 설정을 준 채로 돌렸습니다. 그 근거는 「서명했더니 이미지 이름이 공개 로그에 남는 일」 에 있습니다.

이 시트의 출력은 OrbStack Ubuntu 26.04.1 LTS VM(aarch64)에서 실측했습니다. 실측 버전은 `cosign` `v3.1.4` 이며, 2026-11-23 기준 GitHub 릴리스의 가장 새 버전도 `v3.1.4` 입니다.[^env]



## 핵심 문법

> `cosign` 은 하위 명령으로 서명·검증·증명서 대상을 고르고, 서명은 `--key` 로 키를, `--signing-config` 로 서명 서비스 설정을 정하며, 이미지는 `이름@sha256:…` 로 가리킵니다.

```bash
# 호출 형태
cosign [command]
cosign sign [flags]

# 서명에 쓸 키 쌍과 서명 서비스 설정을 만든다 (서명에 쓸 키 쌍 만들기, 이미지에 서명하기)
cosign generate-key-pair
cosign signing-config create --out FILE

# 이미지 digest 에 서명한다 (이미지에 서명하기)
cosign sign --key cosign.key --signing-config FILE REPO@sha256:DIGEST

# 서명이 놓인 자리를 본다 (서명이 놓인 자리 보기)
cosign tree REPO@sha256:DIGEST

# 공개 키로 서명을 확인한다 (받는 쪽에서 서명 확인하기, 검증이 실패하는 세 경우)
cosign verify --key cosign.pub --insecure-ignore-tlog REPO@sha256:DIGEST

# 이미지가 아닌 파일에 서명하고 확인한다 (파일에 서명하고 확인하기)
cosign sign-blob --key cosign.key --signing-config FILE --bundle BUNDLE FILE
cosign verify-blob --key cosign.pub --insecure-ignore-tlog --bundle BUNDLE FILE

# 이미지에 증명서를 붙이고 확인한다 (이미지에 증명서 붙이기)
cosign attest --key cosign.key --signing-config FILE --predicate FILE --type TYPE REPO@sha256:DIGEST
cosign verify-attestation --key cosign.pub --insecure-ignore-tlog --type TYPE REPO@sha256:DIGEST
```

### 옵션과 서명 설정

```bash
# cosign 하위 명령의 --help 에서 찾은 옵션. --signing-config 와 --predicate 는 서명 쪽, --insecure-ignore-tlog 는 검증 쪽, 나머지는 양쪽에서 쓴다
# --key                    개인 키 파일·KMS 주소·Kubernetes Secret 경로. verify 에서는 공개 키 경로
# --signing-config         서명 서비스(공개 로그·인증 기관·시각 서버) 주소를 담은 설정 파일 경로
# --insecure-ignore-tlog   투명성 로그 확인을 건너뛴다. 로그에 올리지 않은 서명을 확인할 때 쓴다
# --bundle                 sign-blob 은 검증에 필요한 자료를 이 파일에 쓰고, verify-blob 은 이 파일을 읽는다
# --predicate, --type      attest 에서 증명서 내용 파일과 그 종류(예: spdxjson 또는 URI)
```



## 종료 코드

> 성공하면 0 이고, 이 시트에서는 서명이 없으면 10, 없는 태그면 11, 다른 키의 서명과 파일 변조는 1 이 나왔으며, 12·13 은 소스에만 있고 받지 못했습니다.[^exit]

```bash
# 0   성공
# 1   그 밖의 오류. 다른 키의 서명, 파일 변조, 로그 확인 실패에서 받았다
# 10  서명이 없는 이미지를 검증했다 (ImageWithoutSignature)
# 11  없는 태그를 검증했다 (NonExistentTag). 존재하지 않는 태그에 verify 를 돌려 받았다
#     (오류 문장은 Error: image tag not found: GET …/manifests/nosuchtag: MANIFEST_UNKNOWN …)
# 12  맞는 서명이 없다 (NoMatchingSignature). 소스의 상수이며 받지 못했다. 다른 키의 서명은 12 가 아니라 1 이었다
# 13  서명에 인증서가 없다 (NoCertificateFoundOnSignature). 소스의 상수이며 받지 못했다
# 10 과 1 은 「검증이 실패하는 세 경우」 와 「파일에 서명하고 확인하기」 의 예제에 있다
```



## 유스케이스

> 아래 예제는 앞 소절에서 만든 저장소·키·변수를 이어 쓰므로 같은 root 셸에서 위에서 아래로 차례로 실행합니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 cosign 설치, 로컬 저장소(5102 포트), 서명할 이미지와 그 digest 변수가 생기며, 실행 환경은 root 셸입니다.

```bash
# 작업 폴더를 만든다. 키 쌍과 예제 파일이 여기에 생긴다
mkdir -p /root/sheet-cosign && cd /root/sheet-cosign

# 공식 릴리스에서 Linux arm64 바이너리와 체크섬 파일을 받아 맞춘 뒤 설치한다 (x86_64 면 amd64 로 바꾼다)
B=https://github.com/sigstore/cosign/releases/download/v3.1.4
curl -fsSL -o cosign $B/cosign-linux-arm64
curl -fsSL -o cosign_checksums.txt $B/cosign_checksums.txt
grep ' cosign-linux-arm64$' cosign_checksums.txt | sed 's/cosign-linux-arm64/cosign/' | sha256sum -c -    # cosign: OK
install -m 0755 cosign /usr/local/bin/cosign
cosign version 2>&1 | grep -E 'GitVersion|Platform'
```

```bash
GitVersion:    v3.1.4
Platform:      linux/arm64
```

```bash
# Docker Hub 속도 제한을 피하려고 미러에서 registry:2 를 받아 작업용 태그를 붙이고 5102 포트에 띄운다
docker pull -q mirror.gcr.io/library/registry:2    # mirror.gcr.io/library/registry:2
docker tag mirror.gcr.io/library/registry:2 sheet-cosign/registry:2
docker run -d --name sheet-cosign-reg -p 127.0.0.1:5102:5000 sheet-cosign/registry:2 > /dev/null
sleep 2
curl -s localhost:5102/v2/    # {}

# 서명할 이미지를 저장소에 복사하고 digest 를 변수에 담는다. crane 설치는 crane 시트의 「실습 준비」 를 따른다 (줄은 100자에서 잘랐다)
R=localhost:5102/sheet-cosign/app
crane copy mirror.gcr.io/library/alpine:3.20 $R:1.0 2>&1 | tail -n 1    # 2026/11/23 21:31:23 localhost:5102/sheet-cosign/app:1.0: digest: sha256:d9e853e87e55526f6b2917df91a2
D=$(crane digest $R:1.0)
echo $D    # sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
```

### 서명에 쓸 키 쌍 만들기

> `generate-key-pair` 가 개인 키와 공개 키 파일을 만들고, 개인 키 비밀번호는 환경 변수로 줄 수 있습니다.

```bash
# 비밀번호를 환경 변수로 주고 키 쌍을 만든다 (예제용 가짜 값이다)
export COSIGN_PASSWORD=example-pass
cosign generate-key-pair
```

```bash
Private key written to cosign.key
Public key written to cosign.pub
```

```bash
# 생긴 파일 둘과 개인 키의 첫 줄, 공개 키 전문을 본다. 개인 키 본문은 열지 않는다
ls cosign.*
head -n 1 cosign.key
cat cosign.pub
```

```bash
cosign.key
cosign.pub
-----BEGIN ENCRYPTED SIGSTORE PRIVATE KEY-----
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEHdY8iVGyp6RKYJMgy7GoevK06XCq
s1TNP76LgmBPGGNmcdSjknzwxrEoWSHXedbuSGX7ZtJCh4lhe5ExT/6D2Q==
-----END PUBLIC KEY-----
```

`cosign.key` 는 서명하는 쪽만 가지고 `cosign.pub` 은 받는 쪽에 나눠 줍니다.

### 이미지에 서명하기

> 공개 로그를 쓰지 않는 서명 설정 파일을 만들고, 이미지를 `이름@sha256:…` 로 가리켜 `--key` 로 서명합니다.

```bash
# 서비스 주소를 하나도 넣지 않은 서명 설정을 만든다. 공개 로그 주소가 없는 설정이다
cosign signing-config create --out signing-config.json
cat signing-config.json    # {"mediaType":"application/vnd.dev.sigstore.signingconfig.v0.2+json", "rekorTlogConfig":{}, "tsaConfig":{}}
```

```bash
# 키로 서명한다. 서명 설정을 --signing-config 로 주고, 이미지는 digest 로 가리킨다
#   --key             서명할 개인 키 파일
#   --signing-config  위에서 만든 서명 설정 파일
#   --yes             확인 질문을 건너뛴다
#   -a                서명에 key=value 꼬리표를 붙인다. 검증 출력의 optional 칸에 나온다
cosign sign \
  --key cosign.key \
  --signing-config signing-config.json \
  --yes \
  -a env=lab \
  $R@$D
```

```bash
Signing artifact...
Pushing signature to: localhost:5102/sheet-cosign/app
```

이 설정에는 공개 로그 주소가 없어서 서명이 로그로 나가지 않고 저장소에만 올라갑니다.[^tlog]

### 서명이 놓인 자리 보기

> `tree` 로 이미지에 붙은 서명을 보고, `crane` 으로 저장소에 생긴 태그와 서명 객체의 모양을 확인합니다.

```bash
# 이미지에 붙은 서명·증명서를 본다
cosign tree $R@$D
```

```bash
📦 Supply Chain Security Related artifacts for an image: localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
└── 🔗 https://sigstore.dev/cosign/sign/v1 artifacts via OCI referrer: localhost:5102/sheet-cosign/app@sha256:576e72cf0131adfe62c3b6e6aef9230b940adc90423da51f5723cb90c3b4f1f3
   └── 🍒 sha256:d3fcd7e6aefe8b205f2655ee86cdbda0115964da0d172b31ce1e8a86846a9317
```

```bash
# 저장소의 태그를 본다. 서명은 digest 로 이름 붙은 태그 하나로만 보인다
crane ls $R
T=sha256-${D#sha256:}
crane manifest $R:$T | jq .
```

```bash
1.0
sha256-d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "size": 1012,
      "digest": "sha256:576e72cf0131adfe62c3b6e6aef9230b940adc90423da51f5723cb90c3b4f1f3",
      "annotations": {
        "dev.sigstore.bundle.content": "dsse-envelope",
        "dev.sigstore.bundle.predicateType": "https://sigstore.dev/cosign/sign/v1",
        "org.opencontainers.image.created": "2026-11-23T12:31:24Z"
      },
      "artifactType": "application/vnd.dev.sigstore.bundle.v0.3+json"
    }
  ]
}
```

```bash
# 서명 객체(manifest)의 종류와 가리키는 이미지를 본다
SD=$(crane manifest $R:$T | jq -r '.manifests[0].digest')
crane manifest $R@$SD | jq '{artifactType, subject: .subject.digest, layers: [.layers[].mediaType]}'
```

```bash
{
  "artifactType": "application/vnd.dev.sigstore.bundle.v0.3+json",
  "subject": "sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc",
  "layers": [
    "application/vnd.dev.sigstore.bundle.v0.3+json"
  ]
}
```

이 실습 저장소는 이미지를 가리키는 객체를 되돌려 주는 기능(referrers API)에 404 로 답합니다. 서명은 그 대신 `sha256-` 로 시작하는 태그 아래 목록으로 보입니다.[^referrers]

```bash
# triangulate 는 v3 에서 deprecated 이고 옛 .sig 태그 이름을 찍는다. 위 태그 목록에는 그 이름이 없다 (줄은 120자에서 잘랐다)
cosign triangulate $R@$D
```

```bash
Command "triangulate" is deprecated, triangulate will be removed in v4.0.0 (see https://github.com/sigstore/cosign/issue
localhost:5102/sheet-cosign/app:sha256-d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc.sig
```

### 받는 쪽에서 서명 확인하기

> 받는 쪽은 `cosign verify --key cosign.pub` 으로 서명을 확인하고, 로그에 올리지 않은 서명이라 `--insecure-ignore-tlog` 가 필요합니다.

```bash
# 확인 결과(JSON)는 표준출력이라 파일로 받고, 화면에는 확인한 항목만 남긴다
#   --key                   확인에 쓸 공개 키 파일
#   --insecure-ignore-tlog  투명성 로그 확인을 건너뛴다
cosign verify --key cosign.pub --insecure-ignore-tlog $R@$D > verify.json
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.

Verification for localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
```

```bash
# 파일로 받은 JSON 을 읽는다
jq . verify.json
```

```bash
[
  {
    "critical": {
      "identity": {
        "docker-reference": "localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc"
      },
      "image": {
        "docker-manifest-digest": "sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc"
      },
      "type": "https://sigstore.dev/cosign/sign/v1"
    },
    "optional": {
      "env": "lab"
    }
  }
]
```

```bash
# critical.identity.docker-reference  확인한 이미지 이름
# critical.image.docker-manifest-digest  서명이 묶인 이미지 digest
# critical.type                       서명 종류
# optional                            서명할 때 -a 로 붙인 꼬리표
```

```bash
# 같은 확인을 --insecure-ignore-tlog 없이 하면 로그에 기록이 없어 실패한다 (줄은 120자에서 잘랐다)
cosign verify --key cosign.pub $R@$D; echo $?
```

```bash
Error: no matching attestations: failed to verify log inclusion: not enough verified log entries from transparency log: 
error during command execution: no matching attestations: failed to verify log inclusion: not enough verified log entrie
1
```

### 검증이 실패하는 세 경우

> 서명이 없는 이미지, 다른 키로 서명한 이미지, 서명 뒤 같은 태그에 다른 이미지를 올린 경우는 오류 문장과 종료 코드로 가를 수 있습니다.

```bash
# 첫째, 서명하지 않은 이미지를 확인한다 (줄은 100자에서 잘랐다)
crane copy mirror.gcr.io/library/busybox:1.36 $R:unsigned 2>&1 | tail -n 1    # 2026/11/23 21:31:33 localhost:5102/sheet-cosign/app:unsigned: digest: sha256:73aaf090f3d85aa34ee1998
U=$(crane digest $R:unsigned)
cosign verify --key cosign.pub --insecure-ignore-tlog $R@$U; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.
Error: no signatures found
error during command execution: no signatures found
10
```

```bash
# 둘째, 다른 키로 서명한 이미지를 cosign.pub 으로 확인한다 (줄은 140자에서 잘랐다)
mkdir other && (cd other && cosign generate-key-pair > /dev/null 2>&1)
cosign sign \
  --key other/cosign.key \
  --signing-config signing-config.json \
  --yes \
  $R@$U
cosign verify --key cosign.pub --insecure-ignore-tlog $R@$U; echo $?
```

```bash
Signing artifact...
Pushing signature to: localhost:5102/sheet-cosign/app
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.
Error: no matching attestations: failed to verify signature: could not verify envelope: accepted signatures do not match threshold, Found: 0
error during command execution: no matching attestations: failed to verify signature: could not verify envelope: accepted signatures do not 
1
```

```bash
# 셋째, 서명한 태그에 다른 이미지를 올리고 태그로 확인한다 (줄은 100자에서 잘랐다)
crane copy mirror.gcr.io/library/alpine:3.19 $R:1.0 2>&1 | tail -n 1    # 2026/11/23 21:31:42 localhost:5102/sheet-cosign/app:1.0: digest: sha256:6baf43584bcb78f2e5847d1de515
cosign verify --key cosign.pub --insecure-ignore-tlog $R:1.0; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.
Error: no signatures found
error during command execution: no signatures found
10
```

```bash
# 원래 digest 로는 여전히 통과한다. 태그를 되돌려 둔다 (줄은 100자에서 잘랐다)
cosign verify --key cosign.pub --insecure-ignore-tlog $R@$D > /dev/null; echo $?
crane tag $R@$D 1.0
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.

Verification for localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
0
2026/11/23 21:31:42 localhost:5102/sheet-cosign/app:1.0: digest: sha256:d9e853e87e55526f6b2917df91a2
```

서명이 없는 경우와 서명 뒤 내용이 바뀐 경우는 같은 오류와 10 이 나옵니다. 서명은 digest 에 묶이므로 바뀐 이미지는 서명이 없는 이미지와 같기 때문입니다. 다른 키로 서명한 경우는 서명 객체는 있어서 다른 오류와 1 이 나옵니다.

### 파일에 서명하고 확인하기

> `sign-blob` 은 이미지가 아닌 파일에 서명하고 검증 자료를 묶음(bundle) 파일에 써 주며, `verify-blob` 이 그 묶음으로 확인합니다.

```bash
# 배포 파일 대신 쓸 작은 파일에 서명한다. 로그에 올리지 않는 서명 설정을 같이 준다
#   --bundle   검증에 필요한 자료를 이 파일에 쓴다
echo "release 1.0" > release.txt
cosign sign-blob \
  --key cosign.key \
  --signing-config signing-config.json \
  --bundle release.bundle \
  --yes \
  release.txt
```

```bash
Using payload from: release.txt
Signing artifact...
Wrote bundle to file release.bundle
```

```bash
# 묶음 파일의 최상위 키와, 검증 자료에 로그 기록(tlogEntries)이 없는 것을 본다
jq -c keys release.bundle
jq -c '.verificationMaterial | keys' release.bundle
```

```bash
["mediaType","messageSignature","verificationMaterial"]
["publicKey"]
```

```bash
# 묶음으로 파일을 확인한다. 종료 코드는 마지막 줄이다
cosign verify-blob --key cosign.pub --insecure-ignore-tlog --bundle release.bundle release.txt; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the blob.
Verified OK
0
```

```bash
# 파일 내용을 바꾼 뒤 같은 묶음으로 확인하면 실패한다 (줄은 140자에서 잘랐다)
echo tampered >> release.txt
cosign verify-blob --key cosign.pub --insecure-ignore-tlog --bundle release.bundle release.txt; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the blob.
Error: failed to verify signature: could not verify message: invalid signature when validating ASN.1 encoded signature
error during command execution: failed to verify signature: could not verify message: invalid signature when validating ASN.1 encoded signat
1
```

```bash
# v3 의 sign-blob 은 --bundle 없이는 서명하지 않는다
echo "release 2.0" > other.txt
cosign sign-blob --key cosign.key --signing-config signing-config.json --yes other.txt; echo $?
```

```bash
Error: must specify --bundle with --new-bundle-format
error during command execution: must specify --bundle with --new-bundle-format
1
```

### 이미지에 증명서 붙이기

> `attest` 는 SBOM 이나 빌드 정보 같은 JSON 문서를 서명해 이미지에 붙이고, `verify-attestation` 이 서명을 확인한 뒤 문서를 돌려줍니다.

```bash
# 작은 JSON 을 만들어 서명해 붙인다
#   --predicate   서명해 붙일 문서 파일
#   --type        문서의 종류. URI 를 직접 줄 수 있다
echo '{"name":"app","packages":["musl","busybox"]}' > sbom.json
cosign attest \
  --key cosign.key \
  --signing-config signing-config.json \
  --yes \
  --predicate sbom.json \
  --type https://example.com/sbom/v1 \
  $R@$D
```

```bash
Using payload from: sbom.json
Signing artifact...
```

```bash
# 확인하고, 돌려받은 payload 를 풀어 문서 내용을 본다
cosign verify-attestation --key cosign.pub --insecure-ignore-tlog --type https://example.com/sbom/v1 $R@$D > att.json
jq -r .payload att.json | base64 -d | jq -c '{predicateType, predicate}'
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the attestation.

Verification for localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
{"predicateType":"https://example.com/sbom/v1","predicate":{"name":"app","packages":["musl","busybox"]}}
```

```bash
# 이제 이미지에는 서명과 증명서가 따로 붙어 있다
cosign tree $R@$D
```

```bash
📦 Supply Chain Security Related artifacts for an image: localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
└── 🔗 https://example.com/sbom/v1 artifacts via OCI referrer: localhost:5102/sheet-cosign/app@sha256:35916ba78dc48612b7a88b6699cc06b88f4d1f31d1dbed75a0c8dbdcee6bf019
   └── 🍒 sha256:571ef51f6838194103e4b4a25cfd10cf48747d8caae938b2994d03527020ca0c
└── 🔗 https://sigstore.dev/cosign/sign/v1 artifacts via OCI referrer: localhost:5102/sheet-cosign/app@sha256:576e72cf0131adfe62c3b6e6aef9230b940adc90423da51f5723cb90c3b4f1f3
   └── 🍒 sha256:d3fcd7e6aefe8b205f2655ee86cdbda0115964da0d172b31ce1e8a86846a9317
```

### 키 없는 서명의 꼴과 공개되는 것

> 키 없는 서명은 로그인(OIDC)으로 인증한 뒤 일회용 키로 서명하며, 인증한 계정의 정보가 공개 로그에 남을 수 있어 이 시트에서 실행하지 않았습니다.

```bash
# 실행하지 않았습니다. 아래는 공식 문서의 꼴이며 줄 앞의 # 을 떼고 치면 공개 로그에 기록이 올라갑니다
# 서명: --key 없이 이미지만 준다. OIDC 로그인으로 인증한다
# cosign sign IMAGE

# 확인: 누가 어떤 로그인 서비스로 서명했는지를 짚는다
# cosign verify IMAGE \
#   --certificate-identity=name@example.com \
#   --certificate-oidc-issuer=https://accounts.example.com
```

cosign 의 개인정보 안내는 서명에 쓴 정보가 "will be stored in public transparency logs and cannot be removed later" 라고 밝힙니다. 그 정보에 계정의 이메일 주소가 들 수 있다고 적습니다.[^privacy]

확인하는 쪽은 `--certificate-identity` 와 `--certificate-oidc-issuer` 를 줍니다. 그 꼴과 발급처별 주소는 공식 문서에 있습니다.[^keyless]

### 실습 정리

> 주의사항의 예가 위 저장소와 이미지를 이어 쓰므로 그 예까지 돌린 뒤에 실행합니다.

```bash
# 컨테이너와 이미지, 주의사항에서 넣은 hosts 줄, 작업 폴더를 지운다
docker rm -fv sheet-cosign-reg sheet-cosign-reg2
docker rmi sheet-cosign/registry:2 mirror.gcr.io/library/registry:2 > /dev/null
sed -i '/registry.example.com/d' /etc/hosts
cd /root && rm -rf /root/sheet-cosign

# 남은 것이 없는지 센다. 앞 두 값은 개수, 마지막은 작업 폴더가 없을 때 나오는 1 이다
docker ps -a --format '{{.Names}}' | grep -c '^sheet-cosign'
docker images --format '{{.Repository}}' | grep -c 'sheet-cosign/'
test -e /root/sheet-cosign; echo $?
```



## 주의사항과 동작 원리

### 서명했더니 이미지 이름이 공개 로그에 남는 일

> v3 는 서명하면 공개 투명성 로그에 올리는 것이 기본이라서, 사내 이미지 이름이 로그에 남지 않게 하려면 로그 주소가 없는 서명 설정을 줘야 합니다.

```bash
# --help 의 예제에서 기본 서명이 로그에 올리는 것을 확인한다
cosign sign --help 2>&1 | grep -n -A1 'transparency log'
```

```bash
49:  # sign a container image and upload to the transparency log
50-  cosign sign --key cosign.key <IMAGE DIGEST>
--
52:  # sign a container image and skip uploading to the transparency log
53-  cosign sign --key cosign.key --tlog-upload=false <IMAGE DIGEST>
```

```bash
# 예제에 있는 --tlog-upload=false 만으로는 v3 에서 서명이 거부된다 (줄은 150자에서 잘랐다)
cosign sign --key cosign.key --tlog-upload=false --yes $R@$D; echo $?
```

```bash
Flag --tlog-upload has been deprecated, prefer using a --signing-config file with no transparency log services
Error: --tlog-upload=false is not supported with --signing-config or --use-signing-config. Provide a signing config with --signing-config without a tr
error during command execution: --tlog-upload=false is not supported with --signing-config or --use-signing-config. Provide a signing config with --si
1
```

로그에 올리지 않는 방법은 `--tlog-upload=false` 가 아니라 앞의 「이미지에 서명하기」 처럼 로그 주소가 빠진 서명 설정입니다. 이 시트에서 서명이 된 명령은 모두 그 설정으로 돌렸습니다.

올리는 명령(`sign`·`attest`·`sign-blob`)은 바깥 접속이 막힌 셸에서 돌려 로그 요청이 나가지 않게 했습니다. `--yes` 는 비공개 저장소 확인 질문까지 건너뜁니다.[^tlog]

### 태그로 서명했을 때 나오는 경고

> 이미지를 태그로 가리켜 서명하면 경고가 나오는데, 태그는 서명 뒤에도 다른 이미지로 옮겨질 수 있어서 digest 로 가리켜야 합니다.

```bash
# 태그로 서명한다. 서명은 되지만 경고가 먼저 나온다
cosign sign --key cosign.key --signing-config signing-config.json --yes $R:1.0 2>&1 | head -n 5
```

```bash
WARNING: Image reference localhost:5102/sheet-cosign/app:1.0 uses a tag, not a digest, to identify the image to sign.
    This can lead you to sign a different image than the intended one. Please use a
    digest (example.com/ubuntu@sha256:abc123...) rather than tag
    (example.com/ubuntu:latest) for the input to cosign. The ability to refer to
    images by tag will be removed in a future release.
```

경고는 "The ability to refer to images by tag will be removed in a future release." 라고 알립니다. 위 「검증이 실패하는 세 경우」 의 셋째가 이 위험을 보여 줍니다.

### 저장소를 옮기면 검증이 실패하는 일

> 서명은 이미지와 따로 놓인 객체라서 `crane copy` 로 이미지만 다른 저장소로 복사하면 서명이 따라가지 않으며, 이 환경에서는 `cosign save` 와 `load` 로 옮겼을 때 검증이 통과했습니다.

```bash
# 둘째 저장소를 5112 포트에 띄우고 crane 으로 이미지만 복사해 확인한다 (줄은 100자에서 잘랐다)
docker run -d --name sheet-cosign-reg2 -p 127.0.0.1:5112:5000 sheet-cosign/registry:2 > /dev/null
sleep 2
R2=localhost:5112/sheet-cosign/app
crane copy $R@$D $R2@$D 2>&1 | tail -n 1    # 2026/11/23 21:31:46 localhost:5112/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696
cosign verify --key cosign.pub --insecure-ignore-tlog $R2@$D; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.
Error: no signatures found
error during command execution: no signatures found
10
```

```bash
# cosign copy 도 서명을 옮기지 못했다. 명령이 deprecated 라고 알린다 (줄은 100자에서 잘랐다)
cosign copy $R@$D $R2:2.0 2>&1 | tail -n 2
cosign verify --key cosign.pub --insecure-ignore-tlog $R2@$D; echo $?
```

```bash
Copying localhost:5102/sheet-cosign/app@sha256:ba51d55642345137ba4ebf1a15623cbd26493c258e4215391f608
Copying localhost:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d4
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.
Error: no signatures found
error during command execution: no signatures found
10
```

```bash
# 디스크로 저장했다가 올리면 서명도 같이 옮겨진다
cosign save --dir savedir $R@$D
cosign load --dir savedir $R2:2.0
cosign verify --key cosign.pub --insecure-ignore-tlog $R2@$D > /dev/null; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.

Verification for localhost:5112/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
0
```

`cosign copy` 는 이 버전에서 deprecated 이고 `--help` 가 대체 방법을 알려 줍니다. 이 환경에서는 `cosign copy` 뒤에도 서명이 따라가지 않았습니다.[^copy]

### 로컬 HTTP 저장소에서 거부되는 일

> cosign 은 저장소에 HTTPS 로 먼저 말을 걸어서, `localhost` 가 아닌 이름의 HTTP 저장소에는 `--allow-http-registry` 가 필요합니다.

```bash
# registry.example.com 은 실제 주소가 아니라서 VM 의 hosts 에 127.0.0.1 로 건다 (줄은 120자에서 잘랐다)
echo '127.0.0.1 registry.example.com' >> /etc/hosts
cosign verify --key cosign.pub --insecure-ignore-tlog registry.example.com:5102/sheet-cosign/app@$D 2>&1 | tail -n 2 | cut -c1-120
```

```bash
Error: Get "https://registry.example.com:5102/v2/": http: server gave HTTP response to HTTPS client
error during command execution: Get "https://registry.example.com:5102/v2/": http: server gave HTTP response to HTTPS cl
```

```bash
# HTTP 를 허용하고 다시 확인한다
cosign verify --key cosign.pub --insecure-ignore-tlog --allow-http-registry registry.example.com:5102/sheet-cosign/app@$D > /dev/null; echo $?
```

```bash
WARNING: Skipping tlog verification is an insecure practice that lacks transparency and auditability verification for the signature.

Verification for registry.example.com:5102/sheet-cosign/app@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key
0
```

위 예제의 `localhost:5102` 는 이 옵션 없이 통과했습니다. 옵션의 안내는 "Don't use this for anything but testing" 입니다.[^http]

### v3 에서 바뀐 서명 위치와 형식

> v3 는 서명을 묶음(bundle) 형식으로 만들어 이미지를 가리키는 객체로 올리는 것을 기본으로 바꿔서, `.sig` 태그를 찾거나 `--bundle` 없이 쓰던 v2 습관이 통하지 않습니다.

```bash
# 이 시트에서 받은 v3 의 변화
# 서명 위치  .sig 태그가 아니라 이미지를 가리키는 객체(artifactType 이 sigstore bundle). 「서명이 놓인 자리 보기」
# 서명 설정  --signing-config 로 서비스 주소를 준다. --tlog-upload=false 는 거부된다. 「서명했더니 …」
# sign-blob  --bundle 이 필수다. 「파일에 서명하고 확인하기」
# 확인       로그 기록이 없는 서명은 --insecure-ignore-tlog 가 필요하다. 「받는 쪽에서 서명 확인하기」
# 명령       copy 와 triangulate 는 deprecated 이고 --help 가 대신 쓸 명령(copy 는 save·load, triangulate 는 tree)을 알려 준다
```

CHANGELOG 의 v3.0.0 항목은 새 묶음 형식과 서명 설정이 "on by default" 라고 밝힙니다.[^v3] 이전 버전의 습관대로 서명하던 스크립트를 v3 로 올릴 때는 위 다섯 곳을 먼저 확인합니다.



## 관련 문서

> 이어서 볼 이미지 도구 시트와 서명·digest 배경 노트입니다.

- [DevOps 명령어 시트](../README.md) — 다른 명령 시트 목록
- [믿을 수 있는 이미지만 들이기 — 서명·digest·레지스트리 허용 목록·Trivy](../../../../08_cloud/book/cks-study-guide/06-02.%EB%AF%BF%EC%9D%84%20%EC%88%98%20%EC%9E%88%EB%8A%94%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A7%8C%20%EB%93%A4%EC%9D%B4%EA%B8%B0%20%E2%80%94%20%EC%84%9C%EB%AA%85%C2%B7digest%C2%B7%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%97%88%EC%9A%A9%20%EB%AA%A9%EB%A1%9D%C2%B7Trivy.md) — 왜 서명과 digest 를 검증하는지
- [이미지 구조와 digest](../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) — 서명이 묶이는 digest 의 구조
- [crane 참조 시트](./crane.md) — 서명이 놓인 태그와 객체를 `crane ls`·`crane manifest` 로 읽는 방법
- [trivy 참조 시트](./trivy.md) — 서명과 별개로 이미지의 취약점을 검사하는 방법



## 참고 자료

> 검증 환경과 근거 자료, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04.1 LTS(aarch64) — 2026-11-23 실측
- 도구 버전: cosign v3.1.4(가장 새 버전도 v3.1.4), crane v0.22.1, registry:2
- [cosign v3.1.4 릴리스](https://github.com/sigstore/cosign/releases/tag/v3.1.4)
- [Sigstore: Signing Containers](https://docs.sigstore.dev/cosign/signing/signing_with_containers/)
- [Sigstore: Verifying Signatures](https://docs.sigstore.dev/cosign/verifying/verify/)

[^env]: `cosign version` 출력 `GitVersion: v3.1.4` 와 GitHub API `https://api.github.com/repos/sigstore/cosign/releases/latest` 의 `tag_name: v3.1.4` 를 2026-11-23 에 확인했습니다. 바이너리는 같은 릴리스의 `cosign-linux-arm64` 이고 `cosign_checksums.txt` 로 `sha256sum -c` 를 통과시켰습니다.
[^exit]: `cosign` `v3.1.4` `cmd/cosign/errors/exit_codes.go` 는 `ImageWithoutSignature = 10`, `NonExistentTag = 11`, `NoMatchingSignature = 12`, `NoCertificateFoundOnSignature = 13` 을 정의하고, `exit_code_lookup.go` 는 어느 경우에도 맞지 않으면 1 을 돌려줍니다. 받은 10(서명 없음)·1(다른 키, 파일 변조, 로그 기록 없음)은 이 시트 예제의 실측이고, 11(없는 태그)은 존재하지 않는 태그에 `cosign verify` 를 돌려 받았습니다. 12·13 은 받지 못했습니다.
[^tlog]: `cosign sign --help` 의 예제는 `# sign a container image and upload to the transparency log` 아래에 `cosign sign --key cosign.key <IMAGE DIGEST>` 를 둡니다. `v3.1.4` `cmd/cosign/cli/options/sign.go` 는 `--tlog-upload` 의 기본값을 `true` 로 두고 deprecated 로 표시하며, `cmd/cosign/cli/signcommon/common.go` 의 `ShouldUploadToTlog` 는 `if ko.SigningConfig != nil && len(ko.SigningConfig.RekorLogURLs()) == 0 { return false }` 로 서명 설정에 로그 주소가 없으면 올리지 않습니다. 같은 함수는 `SkipConfirmation`(`--yes`)이면 비공개 저장소 확인 없이 `true` 를 돌려줍니다. 이 시트의 서명은 `cosign signing-config create --out` 으로 만든 빈 설정으로 했고, 설정 내용은 `{"mediaType":"application/vnd.dev.sigstore.signingconfig.v0.2+json", "rekorTlogConfig":{}, "tsaConfig":{}}` 입니다. 서명 명령은 `HTTPS_PROXY` 를 닿지 않는 주소로 준 셸에서 돌려 바깥 요청이 나가면 실패하게 했습니다.
[^referrers]: `crane manifest` 로 읽은 `sha256-` 태그는 `application/vnd.oci.image.index.v1+json` 이고 서명 객체를 가리키는 목록입니다. 이 저장소(`registry:2`)에서 `curl -s -o /dev/null -w '%{http_code}\n' localhost:5102/v2/sheet-cosign/app/referrers/DIGEST` 가 404 를 돌려주는 것을 확인했으며, referrers API 지원 여부로 이 동작을 설명한 공식 문서는 찾아 대조하지 않았습니다.
[^privacy]: `cosign` `v3.1.4` `cmd/cosign/cli/sign/privacy/privacy.go` 의 안내문은 "This may include the email address associated with the account with which you authenticate your contractual Agreement." 와 "This information will be used for signing this artifact and will be stored in public transparency logs and cannot be removed later" 를 담습니다.
[^keyless]: Sigstore 공식 문서는 키 없는 서명의 꼴을 `cosign sign $IMAGE` 로, 확인을 `cosign verify <image URI> --certificate-identity=name@example.com --certificate-oidc-issuer=https://accounts.example.com` 으로 적고, "The oidc-issuer for Google is https://accounts.google.com, Microsoft is https://login.microsoftonline.com, GitHub is https://github.com/login/oauth, and GitLab is https://gitlab.com." 라고 밝힙니다.
[^copy]: `cosign copy --help` 가 낸 안내는 `"oras copy -r" will copy images and referring artifacts`, `"cosign save" to write to disk, followed by "cosign load" for a new registry`, `"cosign download" followed by "cosign attach" to just copy the bundle` 입니다. `cosign copy` 뒤 `cosign verify` 가 `no signatures found` 와 10 을 낸 것은 이 시트의 실측이며, `oras` 는 설치하지 않아 돌리지 못했습니다.
[^http]: `cosign sign --help` 의 `--allow-http-registry` 설명은 "whether to allow using HTTP protocol while connecting to registries. Don't use this for anything but testing" 입니다. `localhost:` 주소가 옵션 없이 통과한 것은 이 시트의 실측이며 그 이유를 밝힌 문서는 찾아 대조하지 않았습니다.
[^v3]: `cosign` `v3.1.4` `CHANGELOG.md` 의 v3.0.0 항목은 "with all of the new capabilities of recent releases **on by default**" 라고 쓰고 "Default to using the new protobuf format (#4318)", "Fetch service URLs from the TUF PGI signing config by default (#4428)" 를 변경으로 올리고, 소개문에서 "container signatures stored as an OCI Image 1.1 referring artifact" 를 새 기능으로 꼽습니다. 같은 파일 v3.0.5 항목은 "Deprecate cosign triangulate (#4676)" 와 "Deprecate cosign copy (#4681)" 를, v3.0.2 항목은 "the `--bundle` flag specifying an output file to write the Sigstore bundle (which contains all relevant verification material) has moved from optional to required in v3" 를 올립니다.
