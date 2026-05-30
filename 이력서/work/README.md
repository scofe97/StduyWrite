# work/ — 깃 이력 기반 작업 마스터 인벤토리

이 폴더는 깃 이력을 저장소별·도메인별 작업 단위로 묶어 "무엇을·왜·어떻게 했는가"로 정리한 자료입니다. 커밋 단건 나열은 두지 않습니다 — 필요하면 아래 "갱신 방법"의 `git log` 명령으로 직접 조회하면 됩니다. 상위 `RESUME.md` 와 `경력기술서.md` 는 이 정리본에서 항목을 추려 씁니다.

## 파일

먼저 [about-trombone.md](about-trombone.md) 는 트럼본 프로젝트 자체가 무엇인지(제품 소개 + 내 담당 영역)를 정리한 문서입니다 — 면접에서 "트럼본이 뭐고 내가 뭘 했는지" 설명용. 아래 표의 나머지는 저장소별 깃 이력 작업 정리입니다.

| 파일 | 저장소 | 본인 커밋 | 기간 |
|------|--------|-----------|------|
| [tps-app.md](tps-app.md) | GitLab `TRB305/*` (트럼본 본체: react-app·workflow-api·common-api·scheduler 등) | 2,276건 | 2024-03 ~ 2026-04 |
| [ppp-engine.md](ppp-engine.md) | GitLab `PPP/operator-api·executor·message-lib` (Jenkins 실행 엔진) | 463건 | 2026-04 ~ 2026-05 |
| [tps-manifest.md](tps-manifest.md) | `tps_manifest` (GitOps·인프라) | 80건 | 2024-05 ~ 2026-05 |

> 본인 식별자(이력 추적 시 모두 합산): `bh.sim@okestro.com`, `심보현 <사용자이메일@..com>`(설정 오류), `bh.sim@oksetro.com`(오타), `scofe`.

### 저장소 관계 (중요)

같은 트럼본 본체 코드가 두 곳에 있습니다. **Bitbucket `okestrolab/tps`(과거) → GitLab `TRB305`(현재 활성)** 로 마이그레이션됐고, 해시 1,895건이 공유됩니다. GitLab 이 2026-04 까지로 더 최신이고 신규 작업을 포함하므로 `tps-app.md` 는 **GitLab TRB305 기준**으로 작성했습니다. Bitbucket 은 GitLab 에 흡수된 과거 이력이라 별도 보관하지 않습니다.

TRB305 의 react-app/workflow-api/common-api/scheduler 는 모노레포에서 분리된 멀티 repo라 **공유 히스토리를 가집니다**(같은 커밋이 여러 repo에 복제됨). 그래서 모듈별로 따로 세지 않고 **해시 기준 합집합(2,276건)** 으로 집계했습니다.

## 갱신 방법

새 커밋을 반영하려면 각 저장소에서 아래를 실행해 도메인 표를 갱신합니다.

```bash
# 공통 함수: 한 repo의 내 커밋을 해시 기준 1줄로 추출
mine() { rtk proxy git -C "$1" log --all --no-merges \
  --author='bh.sim@okestro.com' --author='사용자이메일@..com' \
  --author='bh.sim@oksetro.com' --author='scofe' \
  --pretty=tformat:'%ad|%h|%s' --date=short 2>/dev/null \
  | sort -u | awk -F'|' '!seen[$2]++'; }

# tps-app (TRB305 — 공유 히스토리라 모듈 합쳐 해시 dedup)
cd ~/okestro/tps-gitlab2
for m in react-app workflow-api common-api scheduler pms-api pipeline-api; do mine "$m"; done \
  | sort | awk -F'|' '!seen[$2]++'

# ppp-engine
for m in operator executor message-lib; do echo "## $m"; mine "$m"; done

# tps-manifest
mine ~/okestro/tps_manifest
```

## 집계 함정 (다음에 또 헷갈리지 않도록)

깃 이력 집계 중 같은 질문에 50건과 2,000건이 번갈아 나오는 문제를 겪었습니다. 원인은 셋입니다.

1. **`--author='A|B'` perl-regexp 는 과대 카운트.** 정렬·중복제거 전 단계에서 잘못 매칭됩니다. 대신 `--author` 플래그를 식별자마다 따로 주면 git 이 OR 로 처리합니다.
2. **`--author=bh.sim@okestro`(`.com` 누락)는 부분매칭으로 오작동**해 50건만 잡힙니다. 전체 이메일을 정확히 적어야 합니다.
3. **`--all` 을 빼면 `origin/develop`(3.0.5 브랜치 tip)에는 50건만** 남아 있습니다. 3.0.4 이력은 다른 브랜치에 있어 `--all` 이 필수입니다.
4. **`rtk` 토큰 절감 프록시가 `git log` 출력을 샘플링**해 50줄로 잘라냅니다. 전수가 필요하면 `rtk proxy git log ...` 로 우회합니다.
5. **GitLab TRB305 멀티 repo는 공유 히스토리.** react-app/workflow-api/common-api/scheduler 가 각각 ~2,000건씩 나오지만 같은 커밋이 복제된 것입니다. 모듈별 합산이 아니라 **해시 dedup 합집합**(2,276건)이 정답입니다.

정답 명령은 위 "갱신 방법"의 형태입니다. `--all --no-merges` + 정확한 이메일 + `rtk proxy` + `sort -u` + `awk '!seen[$2]++'`(해시 dedup).

## 범위 밖

- **Redpanda Playground**(개인 GCP)는 사이드 프로젝트로 RESUME.md 에 별도 기재됩니다.
- **qa** (`github.com/scofe97/ApiTest`, 10건)는 개인 GitHub 의 API 테스트 자동화로, 사용자 판단에 따라 인벤토리에서 제외했습니다.
- Bitbucket `okestrolab/tps`(과거 본체)는 GitLab TRB305 에 흡수돼 별도 보관하지 않습니다.
