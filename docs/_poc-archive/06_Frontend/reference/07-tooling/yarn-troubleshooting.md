# Yarn YN0018: 체크섬 불일치 에러 분석 및 해결 가이드

## 개요

```
YN0018: │ @types/react@npm:18.2.56: The remote archive doesn't match the expected checksum
```

Yarn Berry(v2+)에서 `yarn install` 실행 시 발생하는 체크섬 검증 실패 에러입니다.

---

## 에러 발생 원인

### 1. 체크섬이란?

체크섬(Checksum)은 패키지의 무결성을 검증하기 위한 해시값입니다. Yarn은 `yarn.lock` 파일에 각 패키지의 체크섬을 저장하고, 설치 시 다운로드된 패키지와 비교하여 변조나 손상을 감지합니다.

### 2. 주요 발생 원인

| 원인 | 설명 |
|------|------|
| **Yarn 버전 불일치** | 로컬과 CI/CD 환경의 Yarn 버전이 다를 경우 체크섬 계산 방식이 달라질 수 있음 |
| **줄 끝 문자(Line Ending) 변환** | Git이 CRLF/LF를 자동 변환하여 zip 파일이 손상됨 (Windows ↔ Unix) |
| **레지스트리 캐시 불일치** | npm 미러(Harbor 등)에 캐시된 패키지가 원본과 다름 |
| **Corepack 사용 여부** | Corepack으로 설치한 Yarn과 직접 설치한 Yarn의 체크섬 계산 차이 |
| **네트워크 문제** | 다운로드 중 패키지가 불완전하게 저장됨 |
| **yarn.lock 동기화 문제** | 로컬에서 패키지가 업데이트되었지만 yarn.lock이 커밋되지 않음 |

### 3. 왜 보안상 중요한가?

> "While this is not a major concern as most npm modules are downloaded through a TLS/SSL encrypted connection, it still has its cases. You might be downloading from your company's local npm registry, or you might for some reason be forced to use a pure HTTP, unencrypted connection."

체크섬 검증은 **공급망 공격(Supply Chain Attack)** 방지를 위한 보안 메커니즘입니다.

---

## 해결 방법

### 방법 1: checksumBehavior 설정 (권장)

`.yarnrc.yml` 파일에 체크섬 동작 방식을 설정합니다.

```yaml
# .yarnrc.yml
checksumBehavior: "update"
```

**옵션 설명**:

| 옵션 | 동작 | 사용 시나리오 |
|------|------|--------------|
| `throw` | 체크섬 불일치 시 에러 발생 (기본값) | 엄격한 보안이 필요한 프로덕션 |
| `update` | yarn.lock의 체크섬을 새 값으로 갱신 | 개발 환경, 체크섬 갱신 필요 시 |
| `ignore` | 체크섬 검증 건너뜀 | 임시 회피용 (비권장) |
| `reset` | 캐시 삭제 후 새로 다운로드 | 캐시 손상 의심 시 |

### 방법 2: 환경 변수로 일회성 해결

설정 파일을 영구 변경하지 않고 한 번만 적용:

```bash
# Linux/Mac
YARN_CHECKSUM_BEHAVIOR=update yarn install

# Windows PowerShell
$env:YARN_CHECKSUM_BEHAVIOR="update"; yarn install

# Windows CMD
set YARN_CHECKSUM_BEHAVIOR=update && yarn install
```

### 방법 3: 캐시 초기화 및 재설치

```bash
# Yarn 캐시 전체 삭제
yarn cache clean --all

# yarn.lock 삭제 후 재생성
rm yarn.lock
yarn install

# 변경사항 커밋
git add yarn.lock
git commit -m "fix: Regenerate yarn.lock with updated checksums"
```

### 방법 4: .gitattributes 설정 (Windows 환경)

Git의 줄 끝 문자 자동 변환으로 인한 문제 해결:

```gitattributes
# .gitattributes
*.zip binary
*.tgz binary
*.tar.gz binary
.yarn/cache/* binary
```

### 방법 5: 특정 패키지만 재설치

문제가 되는 패키지만 제거 후 재설치:

```bash
# 예: @types/react 패키지
yarn remove @types/react
yarn add -D @types/react@18.2.56
```

---

## CI/CD 환경별 해결 방법

### Jenkins/GitLab CI

**Dockerfile 수정**:
```dockerfile
# 방법 1: 환경 변수 사용
ENV YARN_CHECKSUM_BEHAVIOR=update
RUN yarn install

# 방법 2: 캐시 정리 후 설치
RUN yarn cache clean && yarn install
```

**Jenkinsfile 수정**:
```groovy
stage('Install') {
    environment {
        YARN_CHECKSUM_BEHAVIOR = 'update'
    }
    steps {
        sh 'yarn install'
    }
}
```

### GitHub Actions

```yaml
- name: Install dependencies
  run: yarn install
  env:
    YARN_CHECKSUM_BEHAVIOR: update
```

---

## 예방 조치

### 1. Yarn 버전 고정

```yaml
# .yarnrc.yml
yarnPath: .yarn/releases/yarn-4.1.0.cjs
```

### 2. Corepack 사용 통일

```json
// package.json
{
  "packageManager": "yarn@4.1.0"
}
```

```bash
# 모든 환경에서 동일하게 사용
corepack enable
corepack prepare yarn@4.1.0 --activate
```

### 3. yarn.lock 커밋 필수

```bash
# .gitignore에 yarn.lock이 없는지 확인
git add yarn.lock
git commit -m "chore: Update yarn.lock"
```

### 4. CI 캐시 주기적 갱신

캐시가 오래되면 체크섬 불일치가 발생할 수 있으므로 주기적으로 캐시를 무효화합니다.

---

## 관련 에러 코드

| 에러 코드 | 설명 |
|----------|------|
| YN0018 | 체크섬 불일치 |
| YN0060 | Peer dependency 버전 불일치 (경고) |
| YN0086 | Peer dependency 요구사항 미충족 (경고) |

---

## 참고 자료

- [Yarn 공식 문서 - Settings (.yarnrc.yml)](https://yarnpkg.com/configuration/yarnrc)
- [GitHub Issue #5795 - YN0018 in Windows](https://github.com/yarnpkg/berry/issues/5795)
- [GitHub Issue #6598 - checksumBehavior with --immutable](https://github.com/yarnpkg/berry/issues/6598)
- [GitHub Issue #1142 - YN0018 in GitHub Actions](https://github.com/yarnpkg/berry/issues/1142)

---

## 요약

| 상황 | 권장 해결법 |
|------|------------|
| 일회성 해결 | `YARN_CHECKSUM_BEHAVIOR=update yarn install` |
| 영구 설정 | `.yarnrc.yml`에 `checksumBehavior: "update"` 추가 |
| Windows CI 문제 | `.gitattributes`에 바이너리 파일 설정 |
| Harbor 레지스트리 문제 | 캐시 클린 후 재설치 |

---

*문서 작성일: 2025-12-30*
