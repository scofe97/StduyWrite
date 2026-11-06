---
title: "Helm 배포 동작 — checksum-config·resource-policy keep·reset-then-reuse-values"
tags: [helm, kubernetes, checksum, resource-policy, upgrade, reuse-values]
status: draft
source:
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/howto/charts_tips_and_tricks.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_upgrade.md
  - https://github.com/helm/helm/releases/tag/v3.14.0
  - https://raw.githubusercontent.com/helm/helm/v3.14.0/pkg/action/upgrade.go
updated: 2026-11-06
---

# Helm 배포 동작 — checksum-config·resource-policy keep·reset-then-reuse-values

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

세 가지를 모았습니다. 설정이 바뀌면 파드를 다시 띄우는 `checksum/config` annotation, 리소스를 남기는 `helm.sh/resource-policy: keep`, `helm upgrade` 가 이전 values 를 다루는 방식입니다.

checksum 예제 출력은 Helm v4.1.4 에서 `helm template` 으로 직접 돌린 결과입니다. `resource-policy: keep` 은 클러스터가 필요해 공식 문서 문장으로만 확인했습니다. upgrade 의 values 처리는 Helm v3.14.0 소스까지 열어 확인했습니다. 한계는 문서 끝에 적었습니다.

## 1. checksum-config 로 설정 변경 시 롤링

> 파드 템플릿 annotation 에 ConfigMap 렌더 결과의 해시를 넣으면, 설정이 바뀔 때만 Deployment 가 롤링됩니다. 공식 문서가 권하는 방식입니다.

### 설정만 바꾸면 파드가 그대로인 문제

ConfigMap 을 환경 변수나 파일로 마운트한 Deployment 는 ConfigMap 내용이 바뀌어도 파드를 다시 만들지 않습니다. Deployment 의 파드 템플릿이 그대로이기 때문입니다. `helm upgrade` 는 성공했다고 하는데 파드는 옛 설정으로 돌고 있는 상태가 됩니다. 환경 변수로 주입한 값은 파드가 새로 뜨기 전에는 바뀌지 않습니다.

### 동작 원리

파드 템플릿 안의 annotation 값이 바뀌면 파드 템플릿이 바뀐 것이어서 Deployment 가 롤링 업데이트를 합니다. 그래서 설정 파일의 렌더 결과를 해시로 바꿔 annotation 에 넣어 둡니다. 설정이 바뀌면 해시가 바뀌고, 그것이 롤링의 방아쇠가 됩니다. 공식 문서는 이렇게 설명합니다.

> "The `sha256sum` function can be used to ensure a deployment's annotation section is updated if another file changes:"

`include` 는 다른 템플릿 파일의 렌더 결과를 문자열로 가져오고, `sha256sum` 은 그 문자열의 해시를 계산합니다.

> "The `sha256sum` function receives a string, and computes it's SHA256 digest."

### 최소 예제

```yaml
# templates/deployment.yaml (일부)
spec:
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```

`$.Template.BasePath` 는 `templates/` 디렉터리 경로입니다. ConfigMap 의 데이터를 바꾸는 입력만 다르게 해서 렌더하면 해시가 이렇게 움직입니다(실측).

```bash
helm template demo ./demo -s templates/deployment.yaml
#   checksum/config: 2ecf44049fac886a4749e7beaa7ff9dc9ade82370132e1c86ee0d5efcba40d2a

helm template demo ./demo -s templates/deployment.yaml --set replicaCount=7
#   checksum/config: 2ecf44049fac886a4749e7beaa7ff9dc9ade82370132e1c86ee0d5efcba40d2a   (그대로)

# config/app.properties 내용을 log.level=debug 로 고친 뒤
helm template demo ./demo -s templates/deployment.yaml
#   checksum/config: ee92ebc38cd2335d658caec1ecf6f5afb1854bc6896252674b9171e932a50431   (바뀜)
```

replica 수나 이미지 태그처럼 ConfigMap 과 무관한 값을 바꿔도 해시는 같아서 불필요한 롤링은 생기지 않습니다. 반대로 values 로 ConfigMap 내용이 바뀌는 경우(`LOG_LEVEL` 을 `info` 에서 `debug` 로)에도 해시가 바뀝니다(실측).

### 흔한 함정

- 해시는 `include` 한 파일의 렌더 결과만 봅니다. 파드가 읽는 ConfigMap·Secret 이 둘이면 각각 annotation 을 만들거나, 두 파일의 결과를 이어서 해시해야 합니다.
- 라이브러리 차트에서는 이 방식이 안 됩니다. 문서가 직접 적어 둔 제약입니다.

> "NOTE: If you're adding this to a library chart you won't be able to access your file in `$.Template.BasePath`."

- 파일 경로가 틀리면(`/configmap.yaml` 오타) 템플릿 렌더 에러가 나므로 조용히 해시가 비는 사고는 아닙니다. 대신 ConfigMap 파일 이름을 바꿀 때 이 annotation 도 같이 고쳐야 합니다.
- ConfigMap 을 volume 으로 마운트하면 파일은 갱신될 수 있어도 앱이 다시 읽어야 반영됩니다. 이 동작은 열어 본 Helm 문서의 범위 밖이어서 확인하지 못했습니다.

### 공식 문서 근거

- `checksum/config` 예제와 라이브러리 차트 제약 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/howto/charts_tips_and_tricks.md
- `sha256sum` 정의 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md



## 2. resource-policy keep 으로 리소스 보존

> `helm.sh/resource-policy: keep` annotation 이 붙은 리소스는 uninstall·upgrade·rollback 으로 삭제될 상황에서도 남습니다. 대신 Helm 이 더는 관리하지 않는 고아가 됩니다.

### 차트를 지우면 데이터까지 지워지는 문제

릴리스를 uninstall 하면 Helm 은 그 릴리스가 만든 리소스를 모두 지웁니다. PersistentVolumeClaim 이나 Secret 처럼 지우면 되돌릴 수 없는 리소스까지 함께입니다. upgrade 에서도 새 차트가 어떤 리소스를 더는 만들지 않으면 그 리소스가 삭제됩니다. 지켜야 하는 리소스에는 삭제 방지 표지가 필요합니다.

### 동작 원리

리소스 metadata 에 이 annotation 을 달면 Helm 이 삭제를 건너뜁니다. 공식 문서의 설명입니다.

> "The annotation `helm.sh/resource-policy: keep` instructs Helm to skip deleting this resource when a helm operation (such as `helm uninstall`, `helm upgrade` or `helm rollback`) would result in its deletion."

삭제를 건너뛴 리소스는 릴리스에서 떨어져 나갑니다. 문서는 이 부작용도 같이 적습니다.

> "However, this resource becomes orphaned. Helm will no longer manage it in any way."

### 최소 예제

```yaml
# templates/pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-data
  annotations:
    helm.sh/resource-policy: keep
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
```

`helm template` 으로 렌더하면 annotation 이 그대로 매니페스트에 나옵니다(실측). 실제 삭제를 건너뛰는지는 클러스터에서 uninstall 을 해 봐야 알 수 있고, 이 문서에서는 돌려 보지 않았습니다.

### 남은 리소스의 주인 문제

uninstall 뒤에도 PVC 가 남아 있으면 그 리소스는 어느 릴리스에도 속하지 않습니다. 새로 같은 이름으로 설치하면 이미 있는 리소스와 이름이 겹칩니다. 문서가 이 경우 하나를 짚어 줍니다.

> "This can lead to problems if using `helm install --replace` on a release that has already been uninstalled, but has kept resources."

정리하면 `keep` 은 삭제를 막는 대신 정리 책임을 사람에게 넘깁니다. 남은 리소스는 `kubectl delete` 로 직접 지우거나, 다시 설치할 때의 이름 충돌을 감안해 계획해 둡니다.

### 흔한 함정

- `keep` 이 막는 것은 삭제입니다. 이 annotation 을 단 리소스를 upgrade 가 어떻게 갱신하는지는 열어 본 페이지에 없어 확인하지 못했습니다.
- 지우려던 리소스가 안 지워졌을 때 원인이 이 annotation 일 수 있습니다. 릴리스가 이미 사라졌다면 Helm 으로는 찾을 수 없으니 `kubectl get <종류> <이름> -o yaml` 로 annotation 을 직접 봅니다.
- 테스트 환경에서는 `keep` 이 정리를 방해하므로 values 로 켜고 끄는 스위치를 두는 편이 편합니다.

### 공식 문서 근거

- `helm.sh/resource-policy: keep` 정의와 고아 부작용 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/howto/charts_tips_and_tricks.md



## 3. upgrade 의 values 처리 방식 비교

> `helm upgrade` 가 이전 릴리스의 values 를 어떻게 다룰지는 `--reuse-values`·`--reset-values`·`--reset-then-reuse-values` 가 갈라 줍니다. 세 번째는 Helm 3.14 에서 추가됐습니다.

### 새 차트 버전의 기본값이 안 먹는 문제

`helm upgrade` 에 `-f` 없이 `--set image.tag=2.0` 만 주면 어떤 values 로 렌더될까요? 플래그를 하나도 안 준 경우는 두 갈래입니다. `-f`·`--set` 이 하나도 없으면 지난 릴리스의 값을 그대로 복사합니다. 하나라도 있으면 지난 값 없이 차트 기본값에 새 값만 얹어 계산하므로, `--set` 한 줄이 지난번 `-f` 값을 지웁니다. 이를 막으려고 `--reuse-values` 를 쓰면 지난 값은 남지만, 새 차트 버전이 추가한 기본값은 들어오지 않습니다. 두 문제 사이에서 쓰는 것이 세 번째 옵션입니다.

### 세 옵션의 의미

공식 `helm upgrade` 문서가 각 플래그를 이렇게 설명합니다.

> `--reuse-values`: "when upgrading, reuse the last release's values and merge in any overrides from the command line via --set and -f."

> `--reset-values`: "when upgrading, reset the values to the ones built into the chart"

> `--reset-then-reuse-values`: "when upgrading, reset the values to the ones built into the chart, apply the last release's values and merge in any overrides from the command line via --set and -f."

| 옵션 | 값이 쌓이는 순서(낮은 쪽부터) |
|---|---|
| 플래그 없음, `-f`·`--set` 도 없음 | 지난 릴리스의 값을 그대로 복사(소스) |
| 플래그 없음, `-f`·`--set` 있음 | 차트 기본값, 그다음 명령행(지난 값은 쓰지 않음, 소스) |
| `--reuse-values` | 지난 릴리스의 값, 그다음 명령행 |
| `--reset-values` | 차트 기본값, 그다음 명령행 (`--reuse-values` 가 있어도 이쪽이 이김) |
| `--reset-then-reuse-values` | 차트 기본값, 지난 릴리스의 값, 그다음 명령행 |

문서는 우선순위 규칙도 적습니다. `--reset-values` 가 있으면 `--reuse-values` 는 무시됩니다. `--reset-then-reuse-values` 는 둘 중 하나라도 같이 지정되면 무시됩니다. 여러 `-f`·`--set` 중에서는 오른쪽 값이 이깁니다.

### 최소 예제

```bash
# 지난 배포에서 준 값을 유지하되 차트의 새 기본값도 받고 싶을 때
helm upgrade myapp ./chart --reset-then-reuse-values --set image.tag=2.0

# 항상 같은 values 파일로 전부 선언해서 올릴 때
helm upgrade myapp ./chart -f base.yaml -f prod.yaml --set image.tag=2.0
```

Helm 3.14 버전의 변경 기록에 이 플래그가 추가된 줄이 있습니다.

> "feat(helm): add --reset-then-reuse-values flag to 'helm upgrade'"

### Helm 소스로 확인한 분기

`helm upgrade` 의 values 결정은 Helm v3.14.0 `pkg/action/upgrade.go` 의 `reuseValues` 함수가 합니다. 함수 앞 주석은 이 함수가 하는 일을 한 줄로 말합니다.

> "reuseValues copies values from the current release to a new release if the"

함수는 위에서 아래로 네 갈래를 차례로 검사합니다(파일 531~570줄 부근).

- `ResetValues`: 지난 `Config` 를 완전히 무시하고 새 값만 돌려줍니다. 소스 주석은 "we completely ignore current.Config" 입니다.
- `ReuseValues`: 지난 차트와 지난 `Config` 로 지난 값을 다시 만듭니다(`chartutil.CoalesceValues`). 새 값 위에 지난 `Config` 를 합친 뒤 `chart.Values = oldVals` 로 차트 값을 덮습니다(552줄). 새 차트의 기본값이 들어올 자리가 없어집니다.
- `ResetThenReuseValues`: 새 차트의 값은 그대로 두고 지난 `Config` 만 새 값과 합칩니다. 소스 주석은 "we use the new chart's values, but we copy the old config's values over the new config's values" 입니다.
- 플래그 없음: `len(newVals) == 0 && len(current.Config) > 0` 이면 지난 `Config` 를 그대로 씁니다(566~568줄). 아니면 새 값만 돌려줍니다.

```go
if len(newVals) == 0 && len(current.Config) > 0 {
    newVals = current.Config
}
return newVals, nil
```

이 소스 절은 줄 번호와 코드를 v3.14.0 태그 파일에서 직접 열어 확인했습니다. 4.x 소스도 같은지는 확인하지 못했습니다.

### 흔한 함정

- `--reuse-values` 로 올린 차트가 새 버전에서 values 키를 추가하면 템플릿이 그 키를 읽을 때 `nil` 이 될 수 있습니다. 소스가 이유를 보여 줍니다. 아래 소스 절의 `chart.Values = oldVals` 가 새 차트의 기본값을 지난 차트 기준 값으로 덮어씁니다. 실제 클러스터에서 재현하지는 못했습니다.
- `--reset-then-reuse-values` 는 3.14 이전 클라이언트에는 없는 플래그입니다. CI 이미지에 깔린 Helm 버전을 먼저 확인합니다.
- 어느 옵션이든 `-f` 로 모든 값을 선언하는 쪽이 재현성이 좋습니다. 옵션 이름을 외우지 않아도 되고, 깃에 남은 파일이 곧 배포 상태이기 때문입니다.
- 세 옵션이 실제로 어떤 값을 만드는지는 `helm get values <릴리스>` 로 올린 뒤 확인합니다. 이 명령은 문서 근거가 아니라 일반 사용법이어서 이 문서에서는 돌려 보지 않았습니다.

### 공식 문서 근거

- 세 플래그 설명과 우선순위 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/helm/helm_upgrade.md
- `--reset-then-reuse-values` 추가 시점 — https://github.com/helm/helm/releases/tag/v3.14.0
- `reuseValues` 의 네 갈래와 `chart.Values = oldVals` — https://raw.githubusercontent.com/helm/helm/v3.14.0/pkg/action/upgrade.go



## 확인하지 못한 것

- `resource-policy: keep` 이 uninstall·upgrade 에서 실제로 리소스를 남기는지는 클러스터에서 돌려 보지 않았습니다. 문서 문장만 근거입니다.
- 삭제를 건너뛴 뒤 같은 이름으로 재설치할 때 나는 정확한 에러 메시지는 열어 본 문서에 없었습니다.
- `--reuse-values` 가 새 차트 기본값을 못 받는 동작은 v3.14.0 소스로 확인했지만 클러스터에서 재현하지는 않았습니다. 4.x 소스에서 같은 분기인지도 확인하지 못했습니다.
- `helm upgrade` 문서 페이지는 Helm 4.3.1 기준으로 표시됐고, 3.x 문서에서 같은 문장인지는 확인하지 못했습니다. 실측 환경은 Helm v4.1.4 입니다.
- 3.14 릴리스 노트에는 이 플래그가 변경 기록 한 줄로만 나오고 주요 변경 항목에는 없었습니다.



## 관련 문서

- [Helm 기초](../../08_cloud/docs/helm/01-01.Helm 기초.md) — values 우선순위와 `--reuse-values` 비권장 언급
- [Helm 고급](../../08_cloud/docs/helm/01-02.Helm 고급.md)
