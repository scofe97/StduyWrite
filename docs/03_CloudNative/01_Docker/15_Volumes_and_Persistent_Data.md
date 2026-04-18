# 15장: Volumes and Persistent Data

## 📌 핵심 요약

> Docker는 **비영속 데이터**를 위해 컨테이너 수명과 연결된 **로컬 스토리지 레이어**를, **영속 데이터**를 위해 컨테이너와 독립적인 수명 주기를 가진 **Volume**을 제공한다. Volume은 Docker의 **1급 객체(first-class object)**로, 컨테이너 삭제 후에도 데이터가 유지되며 다른 컨테이너에 마운트할 수 있다.

---

## 🎯 학습 목표

- [ ] 영속 데이터(Persistent)와 비영속 데이터(Non-persistent) 구분
- [ ] Stateful 앱과 Stateless 앱의 차이 이해
- [ ] 컨테이너의 로컬 스토리지 레이어(ephemeral storage) 동작 파악
- [ ] Docker Volume 생성, 검사, 삭제 명령어 숙달
- [ ] Volume을 컨테이너에 마운트하는 방법 습득
- [ ] 클러스터 노드 간 공유 스토리지 구성 이해

---

## 📖 본문 정리

### 1. 데이터 유형과 애플리케이션 분류

#### 💬 비유로 이해하기
> Volume은 **외장 하드**와 같다. 노트북(컨테이너)을 교체해도 외장 하드의 데이터는 그대로 남아있다. 반면 노트북 내장 SSD(로컬 스토리지)의 임시 파일은 노트북을 버리면 함께 사라진다.

#### 데이터 유형

| 유형 | 설명 | 예시 | Docker 솔루션 |
|------|------|------|---------------|
| **Persistent** | 보관해야 하는 중요한 데이터 | 고객 기록, 금융 데이터, 감사 로그 | Volume |
| **Non-persistent** | 보관 불필요한 임시 데이터 | 스크래치 파일, 세션 캐시 | 로컬 스토리지 |

#### 애플리케이션 분류

| 유형 | 설명 | 데이터 관리 |
|------|------|-------------|
| **Stateful** | 영속 데이터를 생성/관리하는 앱 | Volume 필요 |
| **Stateless** | 영속 데이터를 생성하지 않는 앱 | 로컬 스토리지로 충분 |

---

### 2. Volume 없는 컨테이너 (Ephemeral Storage)

#### 로컬 스토리지 레이어 구조

```
┌─────────────────────────────────────────────────────────────────┐
│               컨테이너 스토리지 구조 (Volume 없음)                 │
└─────────────────────────────────────────────────────────────────┘

  Container A                    Container B
  ┌─────────────────────┐        ┌─────────────────────┐
  │ Writable Layer      │        │ Writable Layer      │
  │ (로컬 스토리지)      │        │ (로컬 스토리지)      │
  │ • 임시 파일          │        │ • 임시 파일          │
  │ • 컨테이너 삭제 시   │        │ • 컨테이너 삭제 시   │
  │   함께 삭제됨!       │        │   함께 삭제됨!       │
  └──────────┬──────────┘        └──────────┬──────────┘
             │                              │
             │         공유 (Read-Only)      │
             ▼                              ▼
  ┌──────────────────────────────────────────────────────┐
  │                    Image Layer 3                      │
  │                    (Read-Only)                        │
  ├──────────────────────────────────────────────────────┤
  │                    Image Layer 2                      │
  │                    (Read-Only)                        │
  ├──────────────────────────────────────────────────────┤
  │                    Image Layer 1                      │
  │                    (Read-Only)                        │
  └──────────────────────────────────────────────────────┘
```

#### 로컬 스토리지 위치

| 플랫폼 | 경로 |
|--------|------|
| **Linux** | `/var/lib/docker/<storage-driver>/...` |
| **Windows** | `C:\ProgramData\Docker\windowsfilter\...` |

#### 로컬 스토리지의 별칭들
- Thin writable layer
- Ephemeral storage
- Read-write storage
- Graphdriver storage

> ⚠️ **중요**: 컨테이너는 **불변 객체(immutable object)**로 취급해야 한다. 라이브 컨테이너의 설정을 직접 변경하지 말고, 새 컨테이너를 만들어 교체하라!

---

### 3. Volume이 있는 컨테이너

#### Volume 사용의 세 가지 이유

| 이유 | 설명 |
|------|------|
| **독립적 수명 주기** | 컨테이너 삭제 시에도 Volume과 데이터 유지 |
| **외부 스토리지 연결** | 클라우드/전용 스토리지 시스템 통합 가능 |
| **데이터 공유** | 여러 호스트의 컨테이너가 동일 데이터 접근 |

#### Volume 마운트 구조

```
┌─────────────────────────────────────────────────────────────────┐
│               컨테이너 + Volume 구조                              │
└─────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                        Container                               │
  │  ┌─────────────────────────────────────────────────────────┐  │
  │  │               Container Filesystem                       │  │
  │  │                                                          │  │
  │  │    /app        → Writable Layer (임시)                   │  │
  │  │    /tmp        → Writable Layer (임시)                   │  │
  │  │    /data       → Volume (영속) ◄─────────────────┐       │  │
  │  │                                                  │       │  │
  │  └──────────────────────────────────────────────────┼───────┘  │
  └─────────────────────────────────────────────────────┼──────────┘
                                                        │
                                                        │ Mount
                                                        ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                       Docker Volume                            │
  │  ┌─────────────────────────────────────────────────────────┐  │
  │  │  Name: bizvol                                            │  │
  │  │  Driver: local                                           │  │
  │  │  Mountpoint: /var/lib/docker/volumes/bizvol/_data        │  │
  │  │                                                          │  │
  │  │  • 컨테이너 삭제 후에도 유지                               │  │
  │  │  • 다른 컨테이너에 마운트 가능                             │  │
  │  │  • 외부 스토리지로 백엔드 변경 가능                        │  │
  │  └─────────────────────────────────────────────────────────┘  │
  └───────────────────────────────────────────────────────────────┘
                                │
                                │ (Optional)
                                ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                   External Storage System                      │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
  │  │   AWS   │  │  Azure  │  │   NAS   │  │   SAN   │          │
  │  │   EBS   │  │  Disk   │  │         │  │         │          │
  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘          │
  └───────────────────────────────────────────────────────────────┘
```

---

### 4. Docker Volume 생성 및 관리

#### Volume 생성

```bash
# 기본 로컬 드라이버로 Volume 생성
$ docker volume create myvol
myvol

# 다른 드라이버 지정 (플러그인 설치 필요)
$ docker volume create -d <driver-name> myvol
```

#### Volume 목록 및 상세 정보

```bash
# Volume 목록 확인
$ docker volume ls
DRIVER              VOLUME NAME
local               myvol

# Volume 상세 정보
$ docker volume inspect myvol
[
    {
        "CreatedAt": "2024-05-15T12:23:14Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/myvol/_data",
        "Name": "myvol",
        "Options": null,
        "Scope": "local"
    }
]
```

**inspect 결과 필드 설명**:

| 필드 | 설명 |
|------|------|
| `Driver` | 사용 중인 드라이버 (local, 외부 드라이버 등) |
| `Scope` | 범위 (local = 단일 호스트만) |
| `Mountpoint` | Docker 호스트 파일시스템 내 실제 경로 |

#### Volume 삭제

```bash
# 특정 Volume 삭제
$ docker volume rm myvol

# 사용되지 않는 모든 Volume 삭제 (주의!)
$ docker volume prune --all
WARNING! This will remove all local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Volumes:
myvol
```

> ⚠️ **주의**: 컨테이너에서 사용 중인 Volume은 삭제할 수 없다!

---

### 5. Volume을 컨테이너에 마운트하기

#### 컨테이너 생성과 Volume 마운트

```bash
# Volume을 마운트하며 컨테이너 생성
$ docker run -it --name voltainer \
    --mount source=bizvol,target=/vol \
    alpine

# bizvol이 없으면 자동 생성됨!
```

**--mount 플래그 동작**:

| 상황 | 동작 |
|------|------|
| Volume이 이미 존재 | 기존 Volume 사용 |
| Volume이 존재하지 않음 | **자동 생성** 후 마운트 |

#### 실습: Volume 데이터 영속성 테스트

```bash
# 1단계: 컨테이너 생성 및 Volume 마운트
$ docker run -it --name voltainer \
    --mount source=bizvol,target=/vol \
    alpine

# 2단계: Volume에 데이터 쓰기
$ docker exec -it voltainer sh
# echo "I promise to write a book review on Amazon" > /vol/file1
# cat /vol/file1
I promise to write a book review on Amazon
# exit

# 3단계: 컨테이너 삭제
$ docker rm voltainer -f
voltainer

# 4단계: Volume 확인 (여전히 존재!)
$ docker volume ls
DRIVER              VOLUME NAME
local               bizvol

# 5단계: 호스트에서 직접 데이터 확인 (비권장, 교육용)
$ cat /var/lib/docker/volumes/bizvol/_data/file1
I promise to write a book review on Amazon

# 6단계: 새 컨테이너에 기존 Volume 마운트
$ docker run -it --name newctr \
    --mount source=bizvol,target=/vol \
    alpine sh

# cat /vol/file1
I promise to write a book review on Amazon
```

```
┌─────────────────────────────────────────────────────────────────┐
│                  Volume 영속성 테스트 흐름                        │
└─────────────────────────────────────────────────────────────────┘

  Step 1-2: 컨테이너 생성 + 데이터 쓰기
  ┌─────────────────┐
  │   voltainer     │
  │                 │──── /vol ────►┌─────────────┐
  │   "Hello!"      │               │   bizvol    │
  └─────────────────┘               │  file1: ... │
                                    └─────────────┘
            │
            │ Step 3: 컨테이너 삭제
            ▼
  ┌─────────────────┐
  │   ❌ 삭제됨     │               ┌─────────────┐
  │                 │               │   bizvol    │ ← 여전히 존재!
  └─────────────────┘               │  file1: ... │
                                    └─────────────┘
            │
            │ Step 6: 새 컨테이너에 마운트
            ▼
  ┌─────────────────┐
  │     newctr      │
  │                 │──── /vol ────►┌─────────────┐
  │   데이터 접근!   │               │   bizvol    │
  └─────────────────┘               │  file1: ... │
                                    └─────────────┘
```

#### Dockerfile에서 Volume 정의

```dockerfile
# Dockerfile
FROM alpine
VOLUME /data    # 마운트 포인트만 지정 (호스트 경로는 배포 시 지정)
```

> 💡 **참고**: Dockerfile에서는 호스트 디렉토리를 지정할 수 없다. 호스트 OS마다 경로가 다르기 때문!

---

### 6. 클러스터 노드 간 공유 스토리지

#### 외부 스토리지 시스템 연동

```
┌─────────────────────────────────────────────────────────────────┐
│              클러스터 노드 간 Volume 공유                         │
└─────────────────────────────────────────────────────────────────┘

  Docker Host 1                      Docker Host 2
  ┌─────────────────┐                ┌─────────────────┐
  │    Container    │                │    Container    │
  │      ctr1       │                │      ctr2       │
  │        │        │                │        │        │
  │   ┌────┴────┐   │                │   ┌────┴────┐   │
  │   │ Volume  │   │                │   │ Volume  │   │
  │   │ Driver  │   │                │   │ Driver  │   │
  │   └────┬────┘   │                │   └────┬────┘   │
  └────────┼────────┘                └────────┼────────┘
           │                                  │
           │      External Storage Driver     │
           │      (Plugin)                    │
           └──────────────┬───────────────────┘
                          │
                          ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                    External Storage System                     │
  │  ┌──────────────────────────────────────────────────────────┐ │
  │  │              Shared Volume (LUN / NFS Share)              │ │
  │  │                                                           │ │
  │  │   • 두 호스트의 컨테이너가 동일 데이터 접근               │ │
  │  │   • SAN, NAS, 클라우드 스토리지 등                        │ │
  │  └──────────────────────────────────────────────────────────┘ │
  └───────────────────────────────────────────────────────────────┘
```

#### 공유 스토리지 구성 요구사항

| 요구사항 | 설명 |
|----------|------|
| **전용 스토리지 시스템** | SAN, NAS, 클라우드 스토리지 |
| **Volume Driver/Plugin** | 외부 시스템과 Docker 연결 |
| **애플리케이션 설계** | 동시 쓰기로 인한 데이터 손상 방지 |

---

### 7. 데이터 손상(Corruption) 주의사항

#### 💬 비유로 이해하기
> 두 사람이 **동시에 같은 문서를 편집**하는 것과 같다. A가 수정을 로컬에 저장했다가 나중에 업로드하는 사이에 B가 같은 부분을 수정하면, 한 쪽의 변경사항이 사라진다.

```
┌─────────────────────────────────────────────────────────────────┐
│                  공유 Volume 데이터 손상 시나리오                  │
└─────────────────────────────────────────────────────────────────┘

  시간 →

  T1: ctr1이 데이터 업데이트 (로컬 캐시에 저장)
  ┌─────────┐                              ┌─────────┐
  │  ctr1   │  value = "A" (캐시)          │  ctr2   │
  └─────────┘                              └─────────┘
                     │
                     ▼ (아직 커밋 안 됨)
              ┌─────────────┐
              │Shared Volume│  value = "원본"
              └─────────────┘

  T2: ctr2가 같은 데이터 업데이트 (즉시 커밋)
  ┌─────────┐                              ┌─────────┐
  │  ctr1   │  value = "A" (캐시)          │  ctr2   │
  └─────────┘                              └─────────┘
                                                  │
                                                  ▼ (즉시 커밋)
              ┌─────────────┐
              │Shared Volume│  value = "B" ← ctr2 변경 적용
              └─────────────┘

  T3: ctr1이 캐시를 플러시 (덮어쓰기!)
  ┌─────────┐                              ┌─────────┐
  │  ctr1   │                              │  ctr2   │
  └─────────┘                              └─────────┘
       │
       ▼ (캐시 플러시)
              ┌─────────────┐
              │Shared Volume│  value = "A" ← ctr2 변경 손실!
              └─────────────┘

  결과: ctr2의 변경사항("B")이 손실됨
        두 앱 모두 자신의 변경이 적용됐다고 착각
```

**해결 방안**:
- 애플리케이션 레벨에서 **동시성 제어** 구현
- **분산 락(Distributed Lock)** 사용
- **쓰기 작업 조율** 로직 설계

---

### 8. 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `docker volume create <name>` | Volume 생성 (기본: local 드라이버) |
| `docker volume create -d <driver>` | 특정 드라이버로 Volume 생성 |
| `docker volume ls` | 모든 Volume 목록 |
| `docker volume inspect <name>` | Volume 상세 정보 (Mountpoint 등) |
| `docker volume rm <name>` | 특정 Volume 삭제 (사용 중이면 실패) |
| `docker volume prune --all` | 미사용 모든 Volume 삭제 (주의!) |
| `--mount source=<vol>,target=<path>` | 컨테이너에 Volume 마운트 |

---

## 🔍 심화 학습

### Volume Driver 비교

| 드라이버 유형 | 범위 | 특징 |
|---------------|------|------|
| **local** (기본) | 단일 호스트 | 추가 설정 불필요, Docker 기본 제공 |
| **Third-party** | 멀티 호스트 | 외부 스토리지 연동, 플러그인 설치 필요 |

### Bind Mount vs Volume

| 특성 | Bind Mount | Volume |
|------|------------|--------|
| **관리** | 호스트 파일시스템 직접 참조 | Docker가 관리 |
| **이식성** | 호스트 경로 의존 (낮음) | 높음 |
| **백업** | 수동 | docker volume 명령어로 관리 |
| **성능** | 호스트와 동일 | 호스트와 유사 |
| **권장 용도** | 개발 환경 (코드 공유) | 프로덕션 데이터 영속화 |

### 추가 학습 주제
- tmpfs 마운트 (메모리 기반 임시 스토리지)
- Volume 백업 및 복원 전략
- 스토리지 드라이버(overlay2, devicemapper 등)
- CSI (Container Storage Interface)

---

## 💡 실무 적용 포인트

### 면접 대비 Q&A

**Q1: Docker에서 Persistent Data와 Non-persistent Data를 어떻게 다르게 처리하는가?**

> A: Non-persistent 데이터는 컨테이너의 **writable layer(로컬 스토리지)**에 저장되며, 컨테이너 삭제 시 함께 삭제됩니다. Persistent 데이터는 **Volume**에 저장하며, Volume은 컨테이너와 독립적인 수명 주기를 가져 컨테이너 삭제 후에도 데이터가 유지됩니다.

**Q2: Volume이 컨테이너와 독립적이라는 것은 무슨 의미인가?**

> A: Volume은 Docker의 **1급 객체(first-class object)**로, `docker volume` 하위 명령어로 독립적으로 생성, 검사, 삭제할 수 있습니다. 컨테이너를 삭제해도 Volume은 남아있고, 같은 Volume을 다른 컨테이너에 마운트하여 데이터를 재사용할 수 있습니다.

**Q3: 왜 컨테이너를 불변 객체(immutable object)로 취급해야 하는가?**

> A: 라이브 컨테이너의 설정을 직접 수정하면 **재현 가능성**이 떨어지고 **버전 관리**가 어려워집니다. 설정 변경이 필요하면 새 이미지로 새 컨테이너를 만들어 기존 것을 교체하는 방식이 권장됩니다. 데이터베이스 앱이 데이터를 변경하는 것은 허용되지만, 사용자나 도구가 컨테이너 구성을 변경하는 것은 피해야 합니다.

**Q4: 클러스터 환경에서 공유 Volume 사용 시 주의할 점은?**

> A: 여러 컨테이너가 동시에 같은 Volume에 쓰기를 수행하면 **데이터 손상(corruption)**이 발생할 수 있습니다. 한 앱이 캐시에 변경사항을 보관하는 동안 다른 앱이 같은 데이터를 수정하면 나중에 커밋되는 쪽이 이전 변경을 덮어쓸 수 있습니다. 이를 방지하려면 애플리케이션 레벨에서 **동시성 제어**나 **분산 락**을 구현해야 합니다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Persistent vs Non-persistent 데이터 구분
- [ ] Stateful vs Stateless 애플리케이션 이해
- [ ] 컨테이너의 writable layer와 Volume의 차이
- [ ] Volume이 1급 객체인 이유

### Volume 관리
- [ ] `docker volume create`: Volume 생성
- [ ] `docker volume ls`: Volume 목록
- [ ] `docker volume inspect`: 상세 정보 (Mountpoint 확인)
- [ ] `docker volume rm`: 특정 Volume 삭제
- [ ] `docker volume prune --all`: 미사용 Volume 일괄 삭제 (주의)

### 컨테이너와 Volume 연결
- [ ] `--mount source=<vol>,target=<path>`: Volume 마운트
- [ ] Volume 미존재 시 자동 생성 동작 이해
- [ ] 컨테이너 삭제 후 Volume 존속 확인
- [ ] 기존 Volume을 새 컨테이너에 마운트

### 고급 개념
- [ ] 외부 스토리지 시스템 연동 구조 이해
- [ ] Volume Driver/Plugin 역할
- [ ] 공유 스토리지의 데이터 손상 위험
- [ ] Dockerfile VOLUME 명령어 제약사항

### 운영 원칙
- [ ] 컨테이너는 불변 객체로 취급
- [ ] 프로덕션에서 호스트 파일시스템 직접 접근 지양
- [ ] 공유 Volume 사용 시 동시성 제어 설계

---

## 🔗 참고 자료

- [Docker Volumes 공식 문서](https://docs.docker.com/storage/volumes/)
- [Manage data in Docker](https://docs.docker.com/storage/)
- [Storage drivers](https://docs.docker.com/storage/storagedriver/)
- [Volume plugins](https://docs.docker.com/engine/extend/plugins_volume/)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 15
