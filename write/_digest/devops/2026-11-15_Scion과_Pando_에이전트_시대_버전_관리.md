> 출처: Gemini · 2026-11-15 · AI 에이전트 시대의 버전 관리 아키텍처 심층 분석 리포트 (영상 「Git은 이러라고 만든 게 아님 Scion & Pando」 자막 분석) · 분야: devops-keywords, data-keywords · 미검증

## 요점

한 줄: 에이전트가 임시 컨테이너에서 저장소를 반복해 받는 워크로드에 Git 이 맞지 않아, 두 회사가 모노레포를 유지한 채 새 버전 관리 시스템(Scion·Pando)으로 옮긴 사례입니다.

- 문제: Git 은 2005년 오프라인 분산 협업용으로 설계됐습니다. 지금은 수많은 에이전트가 임시 컨테이너에서 매번 저장소를 받고 지우는 워크로드로 바뀌었습니다.
- Anthropic 규모: 하루 머지가 5월 약 2,500건에서 9월 30,000건 이상으로 늘었고, CI 체크아웃은 하루 2,500만 회입니다.
- OpenAI 증상(원문): Codex 병렬 작업이 늘며 push·pull 지연과 병합 실패가 잦아졌고 저장소 신뢰도가 90% 아래로 떨어졌다고 합니다.
- 원문이 꼽은 Git 의 약점 셋: 전체 데이터 복제, 클라이언트 연산(blame·diff·커밋), 저장소 단위로 직렬화된 ref 갱신입니다.
- 다이어트 기법의 한계: shallow 는 이력을 잃고, sparse checkout 은 객체를 여전히 다 받습니다. partial clone 은 거대 모노레포에서 뼈대가 크고 조회마다 왕복이 생깁니다.
- 공통점: 두 회사 모두 저장소를 쪼개지 않고 모노레포와 trunk-based 개발을 유지했습니다.
- Scion: 상시 온라인을 전제로 필요한 경로만 단계별로 조회합니다. 콘텐츠 주소 저장과 다층 캐시를 쓰고, blame·diff·커밋을 서버가 처리합니다.
- Scion 성과: 이전 git 미러 인프라보다 CPU·메모리가 약 200분의 1이고, 코드 다운로드가 수 분에서 수 초로 줄었다고 합니다.
- Pando: git CLI 와 프로토콜은 그대로 둡니다. push 된 packfile 을 저장해 두었다가 그대로 내주고, 브랜치마다 따로 버전을 조율합니다.
- Pando 성과와 대가: push 시간이 약 5분의 1로 줄었습니다. 대신 여러 브랜치를 한 시점으로 보는 전역 일관성을 포기하고 저장 공간을 더 씁니다.
- 일반 조직용 권고(원문): 에이전트마다 `git worktree` 로 작업 공간을 나누고, `main` 한 줄기와 커밋 SHA 기반 승격을 씁니다. CI 는 `cancel-in-progress` 와 경로 필터로 줄입니다.
- 리뷰 방식(원문): 한 줄씩 읽기보다 변경 의도를 먼저 검증하고, 세부 회귀는 머지 후 자동 테스트에 맡기라고 권합니다.
- 찾을 키워드: `packfile-uri`, `Mononoke`, `EdenFS`, `causal consistency`, `merge queue` 입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| 에이전트 워크로드 | 임시 클라우드 컨테이너의 에이전트가 작업마다 빈 환경에서 저장소를 받고 지우는 사용 패턴 | |
| Git 객체 모델 (blob·tree·commit) | 내용 해시로 불변 객체를 저장하고, 바뀐 파일의 상위 tree 만 새로 만드는 Merkle 구조 | [코드 버전 관리와 빌드](../../07_devops/book/fdsd_fundamentals-devops/04-01.How to Version Build and Test Your Code.md) (일부: 커밋 워크플로만, 내부 객체 구조 없음) |
| Merkle tree | 자식 해시를 모아 부모 해시를 만들어 바뀐 부분만 새로 계산하는 트리 | [system-design 06-02](../../03_architecture/book/system-design/06-02.벡터 시계·가십·임시 위탁·머클 트리가 충돌과 장애를 다루고 쓰기와 읽기는 SSTable 을 지난다.md) |
| Packfile | Git 이 객체를 델타 압축해 한 상자로 묶어 주고받는 전송 단위 | |
| shallow·sparse·partial clone | 이력(세로축)·폴더(가로축)·blob 을 줄여 받는 Git 다이어트 기법 셋 | [bmf 06-03](../../03_architecture/book/bmf_building-micro-frontends/06-03.모노레포 — 한 저장소가 주는 것과 받는 값.md) (일부: sparse-checkout만, shallow·partial 없음) |
| 모노레포·trunk-based | 한 저장소와 `main` 한 줄기에 짧은 브랜치를 빠르게 합치는 개발 방식 | [bmf 06-03](../../03_architecture/book/bmf_building-micro-frontends/06-03.모노레포 — 한 저장소가 주는 것과 받는 값.md), [cicd-patterns 05-01](../../07_devops/book/cicd_cicd-patterns/05-01.Exploring Structural CICD Design Patterns.md) |
| Scion | Anthropic 이 git 을 걷어내고 만든 서버 중심 사내 VCS | |
| 콘텐츠 주소 저장소·다층 캐시 | 내용 해시를 키로 불변 저장해 로컬 → 리전 → 서버 캐시가 대부분 요청을 받는 구조 | |
| 서버 사이드 연산 | blame·diff·커밋 생성을 서버가 맡아 로컬 저장소 없이 API 로 묻는 방식 | |
| Pando | OpenAI 가 git 클라이언트는 그대로 두고 서버·저장 계층만 새로 만든 git 백엔드 | |
| 브랜치별 버전 관리 | 저장소 전체 순서 대신 브랜치마다 따로 조율해 서로 다른 브랜치 push 를 병렬로 받는 방식 | |
| Sapling·Mononoke | Meta 의 대규모 모노레포 VCS 와 그 서버 구성 요소 | |
| 복제 지연·파티셔닝 | 미러 서버 동기화 지연과, 잠금 단위를 쪼개 경합을 줄이는 분산 시스템 원리 | [DDIA 06-03](../../05_data/book/designing-data-intensive-applications/06-03.복제 지연 문제와 일관성 보장.md), [07-01](../../05_data/book/designing-data-intensive-applications/07-01.샤딩 개요와 키 범위 샤딩.md) |
| `git worktree` | `.git` 객체 저장소는 공유하고 작업 디렉터리와 브랜치를 에이전트마다 따로 주는 기능 | [claude-code 05-04](../../10_AI/docs/claude-code/05-04.Session Management·Git Worktrees·Agent Teams·Remote Control.md) |
| CI 동시성 취소·경로 필터 | 같은 PR 의 이전 CI 실행을 취소하고 바뀐 경로의 테스트만 돌리는 설정 | [CI/CD 설정](../../07_devops/book/fdsd_fundamentals-devops/05-01.How to Set Up CI CD.md) (일부: GitHub Actions paths 필터만, 동시성 취소 없음) |



## 자료와 실습

- 자료:
  - [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects): Git 의 내부 객체 모델(Blob·Tree·Commit·Tag)과 Delta 압축 기반 Packfile 전송 프로토콜 명세입니다.
  - [git-worktree](https://git-scm.com/docs/git-worktree)·[git-sparse-checkout](https://git-scm.com/docs/git-sparse-checkout): 단일 저장소에서 여러 작업 트리를 운영하는 공식 명세입니다.
  - [Sapling SCM](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/): 가상 파일시스템(EdenFS)과 서버 중심 조회 아키텍처를 다룬 Meta 엔지니어링 글입니다.
  - [Redesigning source control](https://www.anthropic.com/engineering/redesigning-source-control): Claude Code 워크로드 대응을 위해 git 을 대체한 Scion 아키텍처 공식 글입니다.
  - [Scaling Git at OpenAI](https://openai.com/index/scaling-git-at-openai/): Git 프로토콜을 유지한 채 팩파일 무개봉 중계로 백엔드를 확장한 Pando 공식 글입니다.
  - [How we scaled Git at GitHub](https://github.blog/engineering/): Spokes 복제 시스템과 스토리지 샤딩을 다룬 GitHub 엔지니어링 블로그입니다.
  - 『Pro Git』 2판 10장(Git Internals): Merkle Tree 기반 불변 키-값 저장소 구조와 Packfile 네트워크 프로토콜입니다.
  - 『데이터 중심 애플리케이션 설계』: 리포트는 5장(복제)·6장(파티셔닝)·7장(트랜잭션)을 권합니다. 정독 노트 2판 기준으로 복제는 [06-01.복제 개요와 단일 리더](../../05_data/book/designing-data-intensive-applications/06-01.복제 개요와 단일 리더.md) 입니다. 파티셔닝은 [07-01.샤딩 개요와 키 범위 샤딩](../../05_data/book/designing-data-intensive-applications/07-01.샤딩 개요와 키 범위 샤딩.md) 입니다. 트랜잭션은 [08-01.ACID와 트랜잭션 개요](../../05_data/book/designing-data-intensive-applications/08-01.ACID와 트랜잭션 개요.md) 입니다.
  - 『Software Engineering at Google』 9장(코드 리뷰)·16장(버전 관리와 브랜치 관리): 모노레포와 트렁크 기반 개발의 이점을 다룹니다.
  - 코드: [benhoyt/pygit](https://github.com/benhoyt/pygit) 의 `pygit.py`(`hash_object` 등)에서 스냅샷 트리 생성 원리를 봅니다. [facebook/sapling](https://github.com/facebook/sapling) 의 `eden/scm/` 을 봅니다. [git/git](https://github.com/git/git) 의 `pack-objects.c` 와 `refs/files-backend.c` 도 봅니다.
- 실습:
  - Level 1: `git worktree` 로 다중 에이전트 작업 공간 격리를 실험합니다. 메인 저장소 외에 3개의 독립 디렉터리를 만들고 셸 스크립트로 파일 수정과 커밋을 동시에 돌립니다. 함정은 같은 브랜치를 둘 이상의 worktree 에서 체크아웃하려 할 때 에러가 나는 점입니다. 완료: `index.lock` 충돌 없이 150개 커밋이 기록되고 `git worktree remove` 로 정리됩니다.
  - Level 2: Packfile 무개봉 패스스루 경량 Git 스마트 HTTP 프록시를 만듭니다. Go 로 `/info/refs` 와 push·fetch 엔드포인트를 열고 `.pack` 스트림을 풀지 않은 채 저장하며 브랜치별 CAS 버전 번호를 갱신합니다. 함정은 동일 브랜치 동시 푸시 때 낙관적 락 충돌과 프로토콜 파싱 오류입니다. 완료: CPU 급증 없이 다중 브랜치 동시 푸시와 페치가 동작합니다.
  - Level 3: 온디맨드 가상 파일시스템(FUSE) 기반 온라인 전용 VCS 프로토타입을 만듭니다. FUSE 로 시스템 콜을 가로채고 로컬 캐시 → Redis → S3 순으로 불변 Blob 을 읽으며 변경 파일 목록만 서버로 보냅니다. 함정은 IDE 나 빌더의 전체 디렉터리 스캔으로 왕복 지연이 커져 메타데이터 프리페칭이 필요한 점입니다. 완료: 단일 파일 수정 시 네트워크 전송량이 수 KB 이내이고 캐시 적중률 99% 이상을 달성합니다.



## 경고

- ⚠ fetch 횟수: 원문은 "하루 fetch 2,500만 회" 라고 적습니다. Anthropic 글은 이를 CI 의 코드 체크아웃 수로 적습니다(확인됨, [Anthropic 글](https://www.anthropic.com/engineering/redesigning-source-control)).
- ⚠ 개발 인원: 원문은 "7명이 5개월간 Scion 개발" 이라고 적습니다. Anthropic 글은 7명이 Scion 과 코드 리뷰 도구 Antique 를 함께 만들었고 5개월에 이전했다고 적습니다(확인됨, 위 글).
- ⚠ 비교 대상: 200분의 1은 git 일반이 아니라 이전 git 미러 인프라와 비교한 수치입니다. 99% 캐시 적중은 계층마다의 수치입니다(확인됨, 위 글).
- ⚠ 전체 복사본: "서버를 포함해 어디에도 전체 복사본이 없다" 는 완전히 펼친(materialized) 사본이 없다는 뜻입니다. 데몬은 주기적으로 갱신한 스냅샷에서 시작합니다(확인됨, 위 글).
- ⚠ Sapling 관계: 원문은 facebook/sapling 을 Scion 의 "설계 참고 모델" 로 소개합니다. Anthropic 글은 Sapling 의 서버 Mononoke 를 선행 사례로 들 뿐이고 기반이라고 하지 않습니다(확인됨, 위 글).
- ⚠ Pando 세부: 브랜치별 조율(인과 일관성), packfile 불변 저장, `packfile-uri` 전달, push 중앙값 약 5배 개선은 검색 요약으로만 확인했습니다. OpenAI 원문은 403 으로 열지 못했습니다.
- ⚠ 확인하지 않은 주장: "엔지니어 1명 + Codex 로 10주", "신뢰도 90% 미만", "packfile 을 열지 않고 적재" 는 확인하지 않았습니다. "7개 계층 전부 교체 vs 하위 2개 계층 교체" 는 영상의 구분입니다.
- ⚠ GitHub 동향: "초당 7,200건 테스트" 와 Spokes 연결은 출처가 없고, 원문 링크는 GitHub 블로그 첫 화면뿐입니다.
- ⚠ 책 장 번호: 원문은 DDIA 5·6·7장(복제·파티셔닝·트랜잭션)을 듭니다. 노트로 정리한 2판에서는 6·7·8장입니다. 복제는 [DDIA 06-01](../../05_data/book/designing-data-intensive-applications/06-01.복제 개요와 단일 리더.md) 입니다. 트랜잭션은 [08-01](../../05_data/book/designing-data-intensive-applications/08-01.ACID와 트랜잭션 개요.md) 입니다.
- ⚠ 공개 여부: Scion 과 Pando 모두 사내 시스템이고 공개되지 않았습니다. Anthropic 은 Scion 이 일반적인 git 대체재가 아니라고 적었습니다.
