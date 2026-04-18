# Contents 구현 리뷰

## What - 무엇을 구현했는가

`contents_server.go` (190줄)에 ContentsService의 3개 RPC를 구현했다. 저장소 내 파일과 디렉토리를 탐색하는 읽기 전용 기능이며, 4개 서비스 중 가장 작은 규모다. 쓰기 작업(파일 생성·수정·삭제)은 포함하지 않는다.

| RPC | 역할 | 주요 파라미터 |
|-----|------|--------------|
| GetTree | 디렉토리 트리 조회 | ref, path, recursive |
| GetContents | 파일/디렉토리 내용 조회 | path, ref |
| GetReadme | README 파일 자동 탐지 | ref |

---

## How - 어떻게 구현했는가

### 변환 없는 직접 반환 구조

ContentsService는 BranchService와 달리 중간 공통 타입을 거치지 않는다. 클라이언트 계층이 proto 메시지를 직접 반환하는 구조로, 서버 코드가 간결하다. 이것이 190줄이라는 최소 규모의 이유다.

```
Provider API 응답
    ↓ client 계층
proto 메시지 직접 반환 (변환 함수 없음)
```

### GetTree - Provider별 구현

세 Provider는 트리 조회 방식이 상이하다.

| Provider | API | 특이사항 |
|----------|-----|---------|
| GitHub | `Git.GetTree()` | truncated 플래그 반환. 트리가 너무 크면 `truncated=true` |
| GitLab | `Repositories.ListTree()` | 페이지네이션으로 전체 수집. 잘림 없음 |
| Bitbucket | `Repositories.ListFiles()` + `getTreeRecursive()` | 재귀 헬퍼로 전체 트리 구성 |

GitHub의 `truncated` 정보는 `GetTreeResponse.truncated` 필드로 그대로 전달되어, 클라이언트가 결과가 불완전할 수 있음을 인식할 수 있다.

### GetContents - type switching 패턴

GetContents는 응답 타입(파일/디렉토리)에 따라 반환 구조가 달라진다. Go 코드에서 type switch를 사용하여 분기한다.

```go
switch content := result.(type) {
case *client.FileContent:
    // content 필드 채워서 반환
case *client.DirContent:
    // entries 필드 채워서 반환
}
```

Provider별 차이도 이 계층에서 흡수된다.

- **GitHub**: `Repositories.GetContents()` — 파일/디렉토리 모두 처리. 디렉토리면 entries 배열 반환
- **GitLab**: `RepositoryFiles.GetFile()` — 파일 내용을 Base64로 반환
- **Bitbucket**: `Repositories.GetFileBlob()` — raw 내용 반환 후 **서버에서 Base64 인코딩 수행**

Bitbucket은 raw 바이트를 반환하므로 GitHub/GitLab과 달리 서버에서 직접 Base64 인코딩을 수행한다는 점이 핵심 차이다.

### GetReadme - 탐지 우선순위

README 파일명 탐지는 Provider마다 다르게 처리된다.

- **GitHub**: `Repositories.GetReadme()` API가 서버 측에서 자동 탐지하므로 별도 로직 불필요
- **GitLab / Bitbucket**: 클라이언트가 다음 순서로 순차적으로 시도

```
README.md → README.rst → README.txt → README → readme.md
```

모든 시도가 실패하면 `codes.NotFound`를 반환한다. 다른 두 메서드가 에러 시 `codes.Internal`만 반환하는 것과 달리, GetReadme는 `codes.NotFound`를 명시적으로 사용한다. 파일이 없는 상황은 비정상이 아니라 정상적인 부재 상태이기 때문이다.

---

## Why - 왜 이렇게 구현했는가

### 읽기 전용으로 범위를 제한한 이유

파일 쓰기(CreateFile, UpdateFile, DeleteFile)를 포함하면 웹 에디터 기능 구현이 가능하다. 그러나 현재 단계에서는 코드 탐색이 주된 요구사항이다. 쓰기 기능은 Provider별 충돌 처리, 커밋 메시지 생성, 브랜치 선택 등 복잡성이 훨씬 높아지므로 별도 Phase에서 다룬다.

### proto 직접 반환 구조를 선택한 이유

BranchService는 Provider별 차이(ahead/behind 계산 방식 등)를 흡수하기 위해 2단계 변환을 사용한다. ContentsService는 파일 내용·트리 항목처럼 구조가 단순하고 Provider 간 차이가 Base64 인코딩 여부 정도에 그치므로, client 계층에서 바로 proto 메시지를 반환해도 복잡성이 충분히 관리된다. 불필요한 중간 타입을 추가하면 오히려 코드량만 늘어난다.

### GetReadme에서 NotFound를 별도 처리한 이유

README가 없는 것은 저장소 설정 문제가 아니라 단순히 해당 파일이 없는 상태다. `codes.Internal`로 반환하면 클라이언트가 서버 오류로 오해하고 에러 처리를 잘못 구현할 수 있다. `codes.NotFound`를 명시적으로 반환하면 클라이언트가 "README 없음"을 정상 상태로 처리할 수 있다.

---

## 참고 패턴

| 패턴 | 적용 위치 | 설명 |
|------|-----------|------|
| proto 직접 반환 | `contents_server.go` 전체 | 중간 변환 타입 없이 client → proto 직접 |
| type switching | `GetContents` | 파일/디렉토리 타입에 따른 응답 구조 분기 |
| 탐지 우선순위 목록 | `GetReadme` GitLab/Bitbucket | README.md 우선, 다양한 확장자 순차 시도 |
| 의미있는 에러 코드 | `GetReadme` | NotFound와 Internal 명시적 구분 |
| Base64 서버 인코딩 | `GetContents` Bitbucket | raw 응답을 서버에서 직접 인코딩 |

---

## 개선 가능 사항

1. **파일 쓰기 API**: CreateFile, UpdateFile, DeleteFile을 추가하면 웹 에디터 기능 구현이 가능하다.
2. **디렉토리 shallow content**: GetContents가 디렉토리를 반환할 때 entries의 content가 비어 있는데, 옵션으로 shallow content를 포함할 수 있으면 파일 트리에서 미리보기가 가능하다.
3. **파일 크기 제한**: 대용량 바이너리 파일 요청 시 OOM 방지를 위한 크기 제한 검증이 필요하다.
4. **캐싱**: 동일 ref의 동일 path 요청은 Git SHA 기반 불변성을 활용하여 캐싱하면 성능을 개선할 수 있다.
