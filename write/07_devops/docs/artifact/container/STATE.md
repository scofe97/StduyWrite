---
topic: container-image
scope: durable
level: 기본
last_verified: null
blocked_count: null
next_lesson: "03-01 Phase 1~3 완료, Phase 4 6문항 자답 대기 중 — 완료 후 03-02"
updated: 2026-11-24
---

# container-image 학습 상태

## 미션 — 왜 이걸 배우는가
컨테이너 이미지의 내부 구조(index·manifest·config·layer)와 digest 사슬을 이해한다. 머신·store·레지스트리가 달라도 같은 이미지인지 스스로 가리는 것이 목표다.



## 현재 난이도 레벨
기본 — 미평가. Phase 4 자답 전까지 조정하지 않는다.



## 막힌 지점
### 2026-11-23 `03-01` Phase 1
- Q1 대상: `03-01` §1~§2 (이름·태그 vs digest, 네 조각 digest 사슬)
- Q1 첫 예측: "음 같은 이미지 태그로 받았는데 1바이트라도 달라지는걸 알려면 저 4개 구성요소에 대해서 모두 해시로 관리한다?, // 내용 변경은 보통 layer가 가장 많이 발생할건데 나머지 3개도 바뀔수 있지않아? // 해결방식이 맞는지는 모르겠음"
- Q1 판정: `몰랐던 사실` — 네 조각을 각자 따로 해시 관리하는 그림으로 생각함.
- Q1 근거: 태그 이동 가능성, `index → manifest → config·layer` 순서와 연쇄 변경을 몰랐음.
- Q1 도움: `도움받은 응답` (첫 막힘 전제 1단계 → 자식 digest 내포 도출; 둘째 막힘 4단 설명).
- Q1 방식·효과: 고정 파일명 대조(`도움됨`), 4단 설명·`manifest` 중계 정정(`도움됨`).
- Q2 대상: `03-01` §3 (`--platform` 선택과 `docker save` 실패 조건)
- Q2 첫 예측: "애플 실리콘 전용 이미지를 다운받은다음 저장하려는데 데몬에서 매니페스트를 만들수없다(diagest를 찾을수없다?)고 나온다. // save할때 linux/amd64에 대해서는 찾았을거고 다른 플랫폼에서 에러가 난건가? (플랫폼 지정없이 하면 모든 플랫폼을 저장하려하는가?) -> 플랫폼을 지정하거나 완전히 배제해서 해야하는구나 (배제하는편이 용량을 덜먹을거고)"
- Q2 판정: `잘못 알던 인과` — 생략 시 모든 플랫폼을 받거나 저장한다고 봄.
- Q2 근거: 생략 시 daemon 플랫폼(`arm64`) 1개만 고르며, 둘 다 빼면 `arm64` 가 서버로 감.
- Q2 도움: `도움받은 응답` (9개 중 1개만 pull 전제 + 맥 arm64 반례 → 기본값·호환성 도출).
- Q2 방식·효과: 플랫폼 9개 중 1개 저장 전제(`도움됨`), 반례(`도움됨`). Phase 2 점검: OS vs daemon 플랫폼.
- Q3 대상: `03-01` §1·§4 (`containerd store` vs `classic store` 이미지 ID 차이)
- Q3 첫 예측:
  - "containerd store가 이전 방식이라는데 어떻게 다른거지?, classic docker는 /var/lib/docker로 직접 저장 (나중에 직접 확인해보겠다)"
  - "이 저장소라는 곳이 어디를 ID로 삼냐고?, 뭔진 모르겠지만 index아닐까 최상위 계층을 ID로 삼아야하잖아"
- Q3 판정: `몰랐던 사실` — 최상위(`index`) 직관은 `containerd` 1행과 맞으나 3갈래 이유를 몰랐음.
- Q3 근거: `containerd` 는 가져온 최상위(`index` 또는 `manifest`), `classic` 은 `config` digest.
- Q3 도움: `도움받은 응답` (태그 vs `manifest` digest 경로 설명 요청·제공, 3행 좁힘 질문).
- Q3 방식·효과: 태그 vs `manifest` digest 경로 설명(`도움됨`), 1행 오기(`config`→`index`) 정정(`도움됨`).
- 보강 후보: §2 index·§4 store 별 이미지 ID — 태그 pull(index 경유)과 manifest digest pull 경로 차이.
- Q4 대상: `03-01` §4 (`mediaType`·재압축 시 `manifest` vs `config` digest, 같은 이미지 판정 기준)
- Q4 첫 예측:
  - "앞에서 배웠듯이 인덱스에서 한 글자라도 수정되면 이미지 ID가 변경된다고 했죠? 매니페스트 안에서 mediaType 문자열이 Docker에서 OCI로 바뀌든 레이어가 다른 GZIP 수준으로 압축되든 변경이 일어나 무조건 이미지 ID가 바뀔 겁니다."
  - "같은 파일 시스템이라는 거는 정확히 무슨 말인지 모르겠네요. 실행 설정이라 함은 config 파일을 비교하면 되겠죠? 아 config 파일이 아니라 config 레이어를 비교하면 되겠죠? 나머지는 어떤 곳을 비교해야 할지 잘 모르겠네요."
- Q4 판정: `몰랐던 사실` — 바이트 변경 시 digest 변화는 알았으나, `config` 가 `diff_ids`(압축 전 tar sha256)로 파일시스템을 대표하는 점과 비교 트레이드오프를 몰랐음.
- Q4 근거: 첫 예측에서 파일시스템 동등성 비교 대상을 몰랐고, `diff_ids` 전제 제공 뒤에도 재압축 시 `config` 가 바뀔 것으로 추측함(`gzip` 무손실 복원 → `diff_ids` 불변 연결 후 도출).
- Q4 도움: `도움받은 응답` (첫 막힘 `diff_ids` 전제 + `gzip` 무손실 복원 짚기 → `config digest` 도출; 둘째 막힘 4단 설명 → 자기 말 한 줄 설명 통과).
- Q4 방식·효과: `diff_ids` 전제(`도움됨`), `gzip -1`/`-9` 무손실 복원 대조(`도움됨`), `diff_ids` 단독 비교 시 실행 설정 누락 짚기(`도움됨`), 4단 설명(`도움됨`).
- Phase 1 완료: Q1~Q4 통과. Q3·Q4 같은 뿌리(조각별 digest 범위) 짚고 Phase 2 대조 진입.
- Phase 3 희망: 학습자가 옆 창에서 간단한 이미지 구조·digest 사슬 실습을 희망함.

### 2026-11-23 `03-01` Phase 2
- 판정 표·원문 대조 이견 없음.
- 핵심 질문 3곳 통과: `## 3`(OS vs daemon 플랫폼 짚음), `## 4`, `## 2`.

### 2026-11-24 `03-01` Phase 3
- 옆 창(`lab-03-01`) 3단계 완료: `v1`/`v2` 빌드·재압축, `busybox:1.35` save 실패·ID 분기.
- 마무리 확인: `classic store` 가 `config` digest 를 ID 로 쓰는 이유를 보충 정리함.



## 미해결 질문
(아직 없음)



## 다음 레슨 후보 + 고른 이유
- `03-01` Phase 1~4 완료 후 `03-02` — 내부 구조와 digest 를 잡아야 통신·반입이 이어진다.



## 지금 다루지 않는 것
- 멀티 플랫폼 이미지 빌드(`02-03` 예정) — 로드맵 제외 · 다시 볼 조건: index 를 직접 만들어야 할 때
- 이미지 서명·SBOM 검증(attestation 내용 읽기) — 미션과 무관 · 다시 볼 조건: 공급망 보안 검증이 필요할 때



## 볼 자료 (셋 이내)
- [OCI Image Spec v1.1.0](https://github.com/opencontainers/image-spec/tree/v1.1.0) — 1차 · 지금: index·manifest·config·descriptor 정본
- [Docker Docs — containerd image store](https://docs.docker.com/engine/storage/containerd/) — 1차 · 지금: containerd store 와 classic store 차이
- `03-01.이미지 구조와 digest.md` · `03-02.레지스트리 통신과 오프라인 반입.md` — 2차(직접 측정 포함) · 지금: 학습 대상 노트



## 물어볼 곳
- [opencontainers/image-spec Issues](https://github.com/opencontainers/image-spec/issues)



## 코칭 기록 (선택)
- 2026-11-23 · 조언 · overdue_reviews · 연체 12편(최장 77일)/대기 19개 · 학습자 답(그대로 감)
- 2026-11-23 · 같은 범위 · 03-01.이미지 구조와 digest
- 2026-11-23 · 조언 · unverified_states · 미검증 토픽 9개 · 학습자 답(답 없음)
- 2026-11-24 · 같은 범위 · 03-01.이미지 구조와 digest
