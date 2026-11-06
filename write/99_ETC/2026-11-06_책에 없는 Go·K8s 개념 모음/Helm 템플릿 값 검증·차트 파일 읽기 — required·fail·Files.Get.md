---
title: "Helm 템플릿 값 검증·차트 파일 읽기 — required·fail·Files.Get"
tags: [helm, kubernetes, template, required, fail, dict, files]
status: draft
source:
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/howto/charts_tips_and_tricks.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/named_templates.md
  - https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/accessing_files.md
updated: 2026-11-06
---

# Helm 템플릿 값 검증·차트 파일 읽기 — required·fail·Files.Get

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

렌더 단계에서 잘못된 값을 막는 `required`·`fail` 을 먼저 봅니다. 이어서 named template 에 값을 여러 개 넘기는 `dict` 와, 차트 안 파일을 ConfigMap 으로 옮기는 `.Files` 를 다룹니다.

예제 출력은 Helm v4.1.4 에서 `helm template` 으로 직접 돌린 결과입니다. 공식 문서 문장은 영어 원문 그대로 인용하고, 문서가 말하지 않는 동작은 실측이라고 표시합니다.

## 1. required·fail 로 렌더 단계 값 검증

> 값이 비었거나 조합이 틀렸을 때 클러스터에 가기 전, 렌더 단계에서 에러로 멈추게 하는 두 함수입니다. 빈 값 하나는 `required`, 여러 값의 조합이나 열거형 검사는 `fail` 이 맞습니다.

### 검증이 없을 때 생기는 문제

values 에 `database.host` 를 비워 둔 채 배포하면 템플릿은 빈 문자열을 그대로 YAML 에 끼워 넣습니다. 렌더는 성공하고, 파드가 뜬 뒤에야 접속 실패로 드러납니다. 값 오타(`mode: ha` 대신 `mode: HA` 같은 대소문자 실수)도 마찬가지로 조용히 통과합니다. 문제가 배포 이후에 터질수록 원인과 변경 사이의 거리가 멀어져 찾기 어렵습니다.

### 동작 원리

`required` 는 값이 비어 있으면 렌더를 중단하고, 개발자가 준 메시지를 에러로 돌려줍니다. 공식 문서는 이렇게 말합니다.

> "The `required` function gives developers the ability to declare a value entry as required for template rendering."

`fail` 은 조건과 상관없이 에러를 냅니다. 그래서 `if` 와 함께 쓰는 것이 전제입니다.

> "Unconditionally returns an empty `string` and an `error` with the specified text."

둘 다 템플릿을 렌더하는 시점에 실행됩니다. 그래서 `helm install`·`helm upgrade`·`helm template` 어디서든 매니페스트가 만들어지기 전에 막힙니다. 에러 메시지에는 템플릿 파일과 줄 번호가 붙습니다.

### 최소 예제

```yaml
# values.yaml
database:
  enabled: false
  host: ""
mode: standard
```

```yaml
# templates/validate.yaml
{{- if .Values.database.enabled }}
{{- $_ := required "database.host is required when database.enabled=true" .Values.database.host }}
{{- end }}
{{- if not (has .Values.mode (list "standard" "ha")) }}
{{- fail (printf "mode must be standard or ha, got %q" .Values.mode) }}
{{- end }}
```

`$_ :=` 로 결과를 버리는 것은 `required` 의 반환값을 출력에 찍지 않으려는 관용입니다. 두 조건을 어기면 렌더가 이렇게 멈춥니다.

```bash
helm template demo ./demo --set database.enabled=true
Error: execution error at (demo/templates/validate.yaml:2:10): database.host is required when database.enabled=true

helm template demo ./demo --set mode=weird
Error: execution error at (demo/templates/validate.yaml:5:4): mode must be standard or ha, got "weird"
```

종료 코드는 1 이어서(실측) CI 단계가 그대로 실패합니다.

### 흔한 함정

- `helm lint` 는 이 검증을 잡아 주지 않습니다. 같은 차트에서 `mode=weird` 로 `helm lint` 를 돌리면 `level=INFO msg="funcMap fail"` 한 줄만 찍힙니다. 결과는 `0 chart(s) failed` 에 종료 코드 0 이었습니다. `--strict` 를 붙여도 같았습니다(실측, Helm v4.1.4). 값 검증은 `helm template` 을 돌려야 확인됩니다.
- `required` 의 "비었다"는 빈 문자열·`nil` 같은 빈 값을 가리킵니다. `0` 이나 `false` 를 의미 있는 값으로 쓰는 키에는 `required` 대신 `hasKey` 와 `fail` 을 조합하는 쪽이 안전합니다.
- 메시지에 값 이름과 기대 형식을 같이 적지 않으면 에러만 보고 어느 키를 고칠지 모릅니다. 위 예제의 `got "weird"` 처럼 받은 값을 함께 찍는 편이 낫습니다.
- 타입·범위 같은 구조 검증은 `values.schema.json` 이 맡습니다. `required`·`fail` 은 값 사이의 조건처럼 스키마로 쓰기 어려운 검사에 둡니다.

### 공식 문서 근거

- `required` 정의와 예제 `{{ required "A valid foo is required!" .Values.foo }}` — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/howto/charts_tips_and_tricks.md , https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md
- `fail` 정의 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md



## 2. dict 로 named template 값 전달

> named template 은 인자를 하나만 받습니다. 값이 여러 개 필요하면 `dict` 로 묶어 넘기고, 최상위 객체가 필요하면 `"root" $` 를 함께 넣습니다.

### 인자가 하나뿐일 때 생기는 문제

`define` 으로 만든 헬퍼는 `include`·`template` 호출에서 넘긴 값 하나만 받습니다. 라벨 헬퍼에 이름과 티어를 따로 넘기고 싶어도 자리가 하나라서 막힙니다. 또 점(`.`) 대신 새 값을 넘기면 헬퍼 안에서 `.Values`·`.Release` 가 사라집니다. 공식 문서가 이 범위 규칙을 직접 설명합니다.

> "When a named template (created with `define`) is rendered, it will receive the scope passed in by the `template` call."

### 동작 원리

넘긴 값이 곧 헬퍼 안의 `.` 입니다. 문서는 `.Values` 처럼 원하는 범위를 아무거나 넘길 수 있다고 하면서, 헬퍼 안에서 `$` 가 가리키는 것도 넘긴 값이라고 말합니다.

> "In the context of the named template, `$` will refer to the scope you passed in and not some global scope."

`dict` 는 키와 값 쌍으로 맵을 만드는 함수입니다.

> "Creating dictionaries is done by calling the `dict` function and passing it a list of pairs."

그러므로 `dict` 로 만든 맵을 넘기면 헬퍼 안에서 `.name`, `.tier` 처럼 키로 값을 꺼냅니다. `.Values` 를 쓰려면 `"root" $` 로 최상위 범위를 같이 넣어야 합니다. 문서가 `dict` 로 여러 값을 넘기는 방식을 명시한 문장은 확인하지 못했고, 위 두 문장에서 도출한 사용법을 실측으로 확인했습니다.

### 최소 예제

```yaml
# templates/_helpers.tpl
{{- define "demo.labels" -}}
app: {{ .name }}
tier: {{ .tier | default "backend" }}
{{- end -}}

{{- define "demo.fullimage" -}}
{{ .root.Values.image.repository }}:{{ .root.Values.image.tag }}@{{ .name }}
{{- end -}}
```

```yaml
# templates/configmap.yaml (일부)
metadata:
  labels:
    {{- include "demo.labels" (dict "name" "demo" "tier" "web") | nindent 4 }}
```

렌더 결과는 `app: demo`, `tier: web` 입니다. `"root" $` 를 넣은 호출은 이렇게 풀립니다.

```bash
{{ include "demo.fullimage" (dict "root" $ "name" "web") | quote }}
=> "nginx:1.27@web"
```

### 흔한 함정

- `dict` 만 넘기고 `root` 를 빼면 헬퍼 안 `.Values` 가 `nil` 이 되어 렌더가 실패합니다(실측). 에러는 `nil pointer evaluating interface {}.image` 로 나옵니다.
- 헬퍼 안에서 `with` 나 `range` 로 범위가 바뀌면 `$` 도 헬퍼가 받은 맵을 가리킵니다. 최상위 객체는 항상 `root` 키로 꺼내는 규칙을 두면 헷갈리지 않습니다.
- `template` 대신 `include` 를 씁니다. `include` 는 결과를 문자열로 돌려줘서 `nindent` 같은 파이프에 이을 수 있기 때문입니다.

> "It is considered preferable to use `include` over `template`"

### 공식 문서 근거

- 범위 전달 규칙과 `$` 의 의미 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/named_templates.md
- `dict` 정의 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/function_list.md



## 3. .Files 로 차트 파일 읽기

> 차트 안의 설정 파일을 `.Files.Get`·`.Files.Glob` 으로 읽어 ConfigMap 에 넣습니다. `templates/` 아래 파일과 `.helmignore` 대상은 읽을 수 없고, 읽으려 하면 에러 없이 빈 문자열이 나옵니다.

### 파일을 템플릿에 직접 쓸 때 생기는 문제

설정 파일 내용을 values 나 템플릿 본문에 복사해 두면 파일을 고칠 때마다 두 곳을 맞춰야 합니다. 실제 파일을 차트에 두고 렌더 시점에 끌어오면 원본 하나만 고치면 됩니다.

### 동작 원리

`.Files.Get` 은 경로의 파일 내용을 문자열로 돌려줍니다. 문서는 반복문 안에서 파일 이름과 내용을 나란히 찍는 예제를 보여 줍니다.

```yaml
data:
  {{- $files := .Files }}
  {{- range tuple "config1.toml" "config2.toml" "config3.toml" }}
  {{ . }}: |-
    {{ $files.Get . }}
  {{- end }}
```

`.Files.Glob` 은 패턴에 맞는 파일 묶음을 돌려주고, 그 결과에도 `Files` 의 메서드를 그대로 쓸 수 있습니다.

> "`.Glob` returns a `Files` type, so you may call any of the `Files` methods on the returned object."

`AsConfig` 는 묶음을 ConfigMap 의 `data` 항목으로 바꿔 줍니다. 파일 이름이 키가 되고 내용이 값이 됩니다. `AsSecrets` 는 같은 일을 Secret 용 base64 로 합니다.

> "For further organization, it is especially useful to use these methods in conjunction with the `Glob` method."

### 최소 예제

```markdown
demo/
  Chart.yaml
  config/
    app.properties      # log.level=info
    feature.properties  # feature.x=on
  files/
    secret.txt
  templates/
    configmap.yaml
  .helmignore           # files/
```

```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo-config
data:
  {{- (.Files.Glob "config/*").AsConfig | nindent 2 }}
```

```bash
helm template demo ./demo -s templates/configmap.yaml
data:
  app.properties: |
    log.level=info
  feature.properties: |
    feature.x=on
```

### 접근 제한과 빈 문자열 함정

문서는 읽을 수 없는 두 경우를 이렇게 적습니다.

> "Files in `templates/` cannot be accessed."

> "Files excluded using `.helmignore` cannot be accessed."

문서에는 읽으면 어떻게 되는지가 없습니다. 실측하면 에러가 아니라 빈 문자열입니다.

```bash
tpl: {{ .Files.Get "templates/role.yaml" | quote }}   => tpl: ""
ign: {{ .Files.Get "files/secret.txt" | quote }}      => ign: ""   (files/ 가 .helmignore 에 있음)
cfg: {{ .Files.Get "config/app.properties" | quote }} => cfg: "log.level=info\n"
```

파일 이름 오타나 `.helmignore` 때문에 ConfigMap 값이 조용히 비는 사고가 여기서 나옵니다. 꼭 있어야 하는 파일은 1절의 `required` 로 감쌉니다.

```yaml
{{ required "files/secret.txt must exist" (.Files.Get "files/secret.txt") }}
```

`.helmignore` 에 걸린 파일은 `helm package` 결과물에도 들어가지 않아, 로컬 렌더와 패키지 렌더의 결과가 갈릴 수 있습니다.

### 공식 문서 근거

- `.Files.Get`·`.Files.Glob`·`AsConfig`·`AsSecrets` 와 접근 제한 두 문장 — https://raw.githubusercontent.com/helm/helm-www/60d4db89421147aec9fc3fcef9e2d49e2729f50b/versioned_docs/version-3/chart_template_guide/accessing_files.md



## 확인하지 못한 것

- 문서에 `dict` 로 값을 여러 개 넘기는 방식을 직접 설명한 문장은 열어 본 페이지에 없었습니다. 2절의 사용법은 범위 전달 문장과 `dict` 정의에서 도출해 실측으로만 확인했습니다.
- `required` 가 어떤 값까지 "비었다"고 보는지(`0`·`false` 포함 여부)는 직접 돌려 확인하지 않았습니다. 함정의 해당 항목은 확인 전 주의 사항입니다.
- 접근 제한 파일을 읽을 때 빈 문자열이 나오는 동작은 Helm v4.1.4 실측이고, 다른 버전에서 같은지는 확인하지 못했습니다.
- `helm lint` 가 `fail` 을 통과시키는 동작도 v4.1.4 실측입니다. 공식 lint 페이지에는 종료 코드 설명이 없어 문서 근거는 없습니다.



## 관련 문서

- [Helm 고급](../../08_cloud/docs/helm/01-02.Helm 고급.md) — `values.schema.json`·`helm template` 워크플로우
- [Helm 기초](../../08_cloud/docs/helm/01-01.Helm 기초.md)
