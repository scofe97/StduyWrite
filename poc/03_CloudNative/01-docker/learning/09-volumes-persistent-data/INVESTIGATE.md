# Ch09. Volumes & Persistent Data - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Volume Driver 플러그인은 어떻게 동작하며, 어떤 것들이 있는가?

### 왜 이 질문이 중요한가
기본 `local` 드라이버는 단일 호스트에만 유효하다. 프로덕션 환경에서 멀티 호스트 클러스터를 운영하려면 외부 스토리지 시스템과 통합할 수 있는 Volume Driver가 필요하다.

### 답변
**Volume Driver 아키텍처**:

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Volume Plugins                   │
└─────────────────────────────────────────────────────────┘

  Docker Engine
  ┌───────────────────────────────────────────────────────┐
  │  docker volume create -d <driver> myvolume            │
  └────────────────────────┬──────────────────────────────┘
                           │
                           ▼
  ┌───────────────────────────────────────────────────────┐
  │               Volume Plugin API                        │
  │  • Create()    • Mount()      • Unmount()             │
  │  • Remove()    • List()       • Path()                │
  └────────────────────────┬──────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │   AWS EBS    │ │   Azure Disk │ │   NFS/CIFS   │
  │   Plugin     │ │   Plugin     │ │   Plugin     │
  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
         │                │                │
         ▼                ▼                ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  AWS EBS     │ │  Azure Disk  │ │  NFS Server  │
  │  Volume      │ │  Volume      │ │  Share       │
  └──────────────┘ └──────────────┘ └──────────────┘
```

**주요 Volume 플러그인**:

**1. 클라우드 스토리지**:
```bash
# AWS EBS
$ docker plugin install rexray/ebs \
  EBS_REGION=us-east-1

$ docker volume create -d rexray/ebs \
  --opt size=20 \
  --opt volumetype=gp3 \
  myvolume

# Azure Disk
$ docker plugin install rexray/azure \
  AZURE_STORAGE_ACCOUNT=mystorageacct

$ docker volume create -d rexray/azure \
  --opt size=100 \
  myvolume
```

**2. 네트워크 파일 시스템**:
```bash
# NFS
$ docker volume create -d local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/exports/data \
  nfs-volume

# CIFS/SMB (Windows 공유)
$ docker volume create -d local \
  --opt type=cifs \
  --opt o=username=user,password=pass \
  --opt device=//192.168.1.100/share \
  cifs-volume
```

**3. 분산 스토리지**:
```bash
# GlusterFS
$ docker plugin install trajano/glusterfs-volume-plugin

$ docker volume create -d glusterfs \
  --opt glusterserver=192.168.1.100 \
  --opt glustervolume=gv0 \
  gluster-vol

# Ceph RBD
$ docker volume create -d rexray/rbd \
  --opt size=50 \
  ceph-volume
```

**4. 전용 스토리지**:
```bash
# NetApp
$ docker plugin install netapp/trident

# Pure Storage
$ docker plugin install pure/docker-plugin

# HPE 3PAR
$ docker plugin install hpe/3par
```

**Volume 플러그인 API 흐름**:
```
1. docker volume create -d nfs myvolume
   → Plugin.Create(name="myvolume", opts={...})
   → Plugin: NFS 서버에 디렉토리 생성

2. docker run --mount source=myvolume,target=/data myapp
   → Plugin.Mount(id="myvolume")
   → Plugin: NFS 공유를 호스트의 /mnt/volumes/myvolume에 마운트
   → Docker: 컨테이너에 bind mount

3. 컨테이너 종료
   → Plugin.Unmount(id="myvolume")
   → Plugin: NFS 마운트 해제

4. docker volume rm myvolume
   → Plugin.Remove(name="myvolume")
   → Plugin: NFS 서버에서 디렉토리 삭제
```

**플러그인 설치 및 관리**:
```bash
# 플러그인 검색
$ docker plugin ls

# 플러그인 설치
$ docker plugin install <plugin-name>

# 플러그인 설정 확인
$ docker plugin inspect <plugin-name>

# 플러그인 비활성화/제거
$ docker plugin disable <plugin-name>
$ docker plugin rm <plugin-name>
```

### 실무 적용
AWS에서는 EBS 플러그인으로 컨테이너가 다른 EC2 인스턴스로 이동해도 볼륨이 자동으로 따라간다. Kubernetes에서는 CSI (Container Storage Interface) 드라이버가 이 역할을 하며, 더 표준화되어 있다. 프로덕션에서는 클라우드 제공자의 관리형 스토리지 서비스를 권장한다.

---

## Q2. Bind Mount와 Volume의 성능 차이는 얼마나 나며, 각각 언제 사용해야 하는가?

### 왜 이 질문이 중요한가
개발 중에는 Bind Mount로 소스 코드를 마운트하지만, 프로덕션에서는 Volume을 사용한다. 두 방식의 성능 차이와 트레이드오프를 이해해야 올바른 선택을 할 수 있다.

### 답변
**Bind Mount vs Volume 아키텍처**:

```
┌─────────────────────────────────────────────────────────┐
│                    Bind Mount                            │
└─────────────────────────────────────────────────────────┘

  Host Filesystem                Container
  ┌──────────────────┐          ┌──────────────────┐
  │ /home/user/code/ │◄─────────┤ /app/src         │
  │   ├─ app.js      │  직접     │   ├─ app.js      │
  │   ├─ config.yml  │  바인드   │   ├─ config.yml  │
  │   └─ package.json│          │   └─ package.json│
  └──────────────────┘          └──────────────────┘

  • 호스트 파일시스템 직접 참조
  • 호스트의 권한, 메타데이터 그대로 사용
  • 플랫폼 의존적 (Windows/Mac에서 성능 이슈)

┌─────────────────────────────────────────────────────────┐
│                       Volume                             │
└─────────────────────────────────────────────────────────┘

  Docker Managed Area              Container
  ┌──────────────────────────┐    ┌──────────────────┐
  │ /var/lib/docker/volumes/ │    │ /data            │
  │   myvolume/              │◄───┤   ├─ file1.db    │
  │     _data/               │ 마운트│   └─ file2.log   │
  │       ├─ file1.db        │    └──────────────────┘
  │       └─ file2.log       │
  └──────────────────────────┘

  • Docker가 관리하는 전용 영역
  • 플랫폼 독립적
  • 백업, 마이그레이션 용이
```

**성능 비교 (벤치마크)**:

| 작업 | Bind Mount (Linux) | Volume (Linux) | Bind Mount (Mac) | 차이 |
|------|-------------------|---------------|-----------------|------|
| 순차 읽기 | 3.2 GB/s | 3.1 GB/s | 250 MB/s | Mac에서 -92% |
| 순차 쓰기 | 2.8 GB/s | 2.7 GB/s | 180 MB/s | Mac에서 -94% |
| 랜덤 읽기 | 1.5 GB/s | 1.4 GB/s | 80 MB/s | Mac에서 -95% |
| 작은 파일 생성 | 15k/s | 14k/s | 1.2k/s | Mac에서 -92% |
| 메타데이터 연산 | 20k/s | 19k/s | 800/s | Mac에서 -96% |

**Windows/Mac에서 느린 이유**:
```
┌─────────────────────────────────────────────────────────┐
│        macOS/Windows Bind Mount 경로                     │
└─────────────────────────────────────────────────────────┘

  macOS                      VM (HyperKit/WSL2)      Container
  ┌──────────────┐          ┌──────────────┐        ┌────────┐
  │ /Users/...   │─────────►│ /host_mnt/   │───────►│ /app   │
  │   app.js     │  VirtioFS│   app.js     │ mount  │ app.js │
  └──────────────┘          └──────────────┘        └────────┘
       ▲                          │
       │    osxfs/grpcfuse       │
       └──────────────────────────┘

  • 2번의 파일시스템 경계 통과 (macOS → VM → Container)
  • 네트워크 프로토콜 (9p, VirtioFS)로 파일 동기화
  • 메타데이터 연산마다 왕복 필요
```

**사용 시나리오별 권장**:

**개발 환경 (Bind Mount)**:
```yaml
# docker-compose.dev.yaml
services:
  web:
    volumes:
      - ./src:/app/src:delegated  # delegated 플래그로 성능 개선
      - ./config:/app/config:ro   # 읽기 전용
      - /app/node_modules         # 익명 볼륨으로 제외
```

**프로덕션 환경 (Volume)**:
```yaml
# docker-compose.prod.yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data
  cache:
    volumes:
      - cache-data:/data

volumes:
  db-data:
    driver: rexray/ebs
    driver_opts:
      size: 100
      volumetype: gp3
  cache-data:
    driver: local
```

**성능 최적화 팁**:

**1. Mac/Windows에서 Bind Mount 최적화**:
```yaml
# Delegated 모드 (약간의 일관성 희생, 성능 향상)
volumes:
  - ./src:/app/src:delegated

# Cached 모드 (읽기 최적화)
volumes:
  - ./src:/app/src:cached

# Consistent 모드 (기본값, 완벽한 일관성)
volumes:
  - ./src:/app/src:consistent
```

**2. 익명 볼륨으로 제외**:
```dockerfile
# node_modules를 Bind Mount에서 제외
VOLUME /app/node_modules
```

```yaml
services:
  web:
    volumes:
      - ./:/app
      - /app/node_modules  # 호스트 것 대신 컨테이너 것 사용
```

**3. tmpfs 마운트 (메모리 기반, 초고속)**:
```yaml
services:
  app:
    tmpfs:
      - /tmp
      - /app/cache:size=100M,mode=1777
```

**4. Volume 대신 COPY (이미지에 포함)**:
```dockerfile
# 프로덕션: 소스를 이미지에 포함 (가장 빠름)
COPY . /app
```

### 실무 적용
로컬 개발에서는 Bind Mount로 핫 리로드를 활용하되, `node_modules`나 `.git` 같은 대용량 디렉토리는 제외한다. macOS/Windows에서는 delegated 모드를 사용하여 성능을 개선한다. 프로덕션에서는 Volume이나 COPY를 사용하여 플랫폼 독립성과 성능을 보장한다.

---

## Q3. tmpfs 마운트는 언제 사용하며, 어떤 이점이 있는가?

### 왜 이 질문이 중요한가
tmpfs는 메모리 기반 파일시스템으로 디스크 I/O를 완전히 우회한다. 임시 데이터를 다룰 때 극적인 성능 향상을 제공하지만, 메모리 소비와 데이터 휘발성을 이해해야 한다.

### 답변
**tmpfs의 특징**:

```
┌─────────────────────────────────────────────────────────┐
│              Volume vs tmpfs 비교                        │
└─────────────────────────────────────────────────────────┘

  일반 Volume (디스크 기반)
  Container                   Host Disk
  ┌──────────────┐           ┌──────────────┐
  │ /data        │◄──────────┤ /var/lib/... │
  │  write()     │           │  SSD/HDD     │
  └──────┬───────┘           └──────────────┘
         │
         ├─ 페이지 캐시
         ├─ I/O 스케줄러
         ├─ 디스크 큐
         └─ 물리적 쓰기 (느림)

  tmpfs (메모리 기반)
  Container                   Host RAM
  ┌──────────────┐           ┌──────────────┐
  │ /tmp         │◄──────────┤ Memory Pages │
  │  write()     │           │  (매우 빠름) │
  └──────────────┘           └──────────────┘
         │
         └─ 메모리 직접 쓰기 (초고속)

  • 디스크 I/O 없음
  • 컨테이너 재시작 시 데이터 삭제
  • 메모리 부족 시 스왑 가능 (성능 저하)
```

**성능 비교**:

| 작업 | SSD Volume | tmpfs | 속도 향상 |
|------|-----------|-------|----------|
| 순차 쓰기 | 500 MB/s | 3000 MB/s | 6배 |
| 랜덤 쓰기 | 200 MB/s | 2800 MB/s | 14배 |
| 작은 파일 생성 | 5k/s | 50k/s | 10배 |
| fsync() | 10ms | 0.001ms | 1만배 |

**사용 시나리오**:

**1. 테스트 데이터베이스**:
```yaml
services:
  test-db:
    image: postgres:15
    tmpfs:
      - /var/lib/postgresql/data  # 테스트 DB를 메모리에
    environment:
      - POSTGRES_PASSWORD=test
```
- 테스트가 10배 이상 빠름
- 테스트 후 데이터 자동 삭제 (정리 불필요)

**2. 빌드 캐시**:
```yaml
services:
  builder:
    tmpfs:
      - /tmp
      - /root/.cache  # npm, pip, cargo 캐시
```

**3. 세션 스토어 (임시)**:
```yaml
services:
  app:
    tmpfs:
      - /app/sessions:size=500M,mode=1700
```

**4. 로그 버퍼**:
```yaml
services:
  app:
    tmpfs:
      - /var/log:size=100M
    # 주기적으로 외부 로그 수집기로 전송
```

**tmpfs 옵션**:
```yaml
services:
  app:
    tmpfs:
      - /tmp:size=1G,mode=1777,uid=1000,gid=1000,noexec,nosuid
```

| 옵션 | 설명 |
|------|------|
| `size` | 최대 크기 (기본: 호스트 메모리의 50%) |
| `mode` | 파일 권한 (8진수) |
| `uid`, `gid` | 소유자 |
| `noexec` | 실행 파일 차단 (보안) |
| `nosuid` | setuid 비트 무시 (보안) |

**Docker Run 예시**:
```bash
docker run --tmpfs /tmp:rw,noexec,nosuid,size=1G myapp
```

**주의사항**:

**1. 메모리 소비**:
```bash
# tmpfs에 1GB 데이터 쓰면 → 호스트 메모리 1GB 소비
# 메모리 부족 시 OOM Killer가 컨테이너 종료 가능
```

**2. 데이터 휘발성**:
```bash
# 컨테이너 재시작 → 모든 데이터 삭제
# 중요한 데이터는 절대 tmpfs에 저장 금지
```

**3. 스왑 위험**:
```bash
# 메모리 부족 시 tmpfs가 스왑으로 이동
# → 디스크보다 느려질 수 있음 (역효과)
# 스왑 비활성화 권장: --memory-swappiness=0
```

### 실무 적용
CI/CD 파이프라인에서 테스트 DB를 tmpfs로 실행하면 빌드 시간이 크게 단축된다. 고성능 캐시 서버(Redis, Memcached)는 이미 메모리 기반이므로 tmpfs 불필요하지만, 임시 파일을 많이 생성하는 앱(컴파일러, 이미지 처리 등)은 `/tmp`를 tmpfs로 마운트하여 성능을 개선한다.

---

## Q4. Volume 백업과 복원 전략은 무엇인가?

### 왜 이 질문이 중요한가
Volume에는 DB 데이터, 사용자 업로드 파일 등 중요한 데이터가 저장된다. 백업 전략이 없으면 하드웨어 장애나 실수로 데이터를 영구히 잃을 수 있다.

### 답변
**백업 방법 비교**:

**1. 컨테이너를 통한 백업 (간단)**:
```bash
# 백업
docker run --rm \
  -v myvolume:/source:ro \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/myvolume-backup-$(date +%Y%m%d).tar.gz -C /source .

# 복원
docker run --rm \
  -v myvolume:/target \
  -v $(pwd):/backup \
  alpine \
  tar xzf /backup/myvolume-backup-20240523.tar.gz -C /target
```

**2. 호스트에서 직접 백업 (빠름)**:
```bash
# Volume 위치 확인
VOL_PATH=$(docker volume inspect myvolume --format '{{.Mountpoint}}')
# /var/lib/docker/volumes/myvolume/_data

# 백업 (root 권한 필요)
sudo tar czf myvolume-backup.tar.gz -C $VOL_PATH .

# 복원
sudo tar xzf myvolume-backup.tar.gz -C $VOL_PATH
```

**3. 스냅샷 기반 백업 (클라우드)**:
```bash
# AWS EBS Volume
docker volume create -d rexray/ebs myvolume

# 스냅샷 생성
aws ec2 create-snapshot \
  --volume-id vol-1234567890abcdef0 \
  --description "myvolume backup $(date)"

# 스냅샷에서 복원
aws ec2 create-volume \
  --snapshot-id snap-1234567890abcdef0 \
  --availability-zone us-east-1a
```

**4. 복제를 통한 백업**:
```bash
# Volume 복제
docker run --rm \
  -v myvolume:/source:ro \
  -v myvolume-backup:/target \
  alpine \
  sh -c "cp -a /source/. /target/"
```

**자동 백업 시스템 (Docker Compose + Cron)**:

```yaml
# docker-compose.backup.yaml
services:
  backup:
    image: alpine
    volumes:
      - db-data:/data:ro
      - ./backups:/backups
    command: >
      sh -c "
        tar czf /backups/db-backup-$$(date +%Y%m%d-%H%M%S).tar.gz -C /data . &&
        find /backups -name 'db-backup-*.tar.gz' -mtime +7 -delete
      "
    restart: "no"

volumes:
  db-data:
    external: true
```

```bash
# Cron 작업 (매일 새벽 2시)
0 2 * * * cd /path/to/app && docker compose -f docker-compose.backup.yaml up
```

**증분 백업 (rsync)**:
```bash
# 첫 백업
docker run --rm \
  -v myvolume:/source:ro \
  -v backup-storage:/backup \
  alpine \
  rsync -av --delete /source/ /backup/full/

# 증분 백업 (변경된 파일만)
docker run --rm \
  -v myvolume:/source:ro \
  -v backup-storage:/backup \
  alpine \
  rsync -av --link-dest=/backup/full /source/ /backup/incremental-$(date +%Y%m%d)/
```

**데이터베이스 전용 백업**:

**PostgreSQL**:
```bash
# 논리적 백업 (SQL 덤프)
docker exec my-postgres pg_dump -U postgres dbname > backup.sql

# 복원
docker exec -i my-postgres psql -U postgres dbname < backup.sql

# 물리적 백업 (pg_basebackup)
docker exec my-postgres pg_basebackup -D /backup -F tar -z
```

**MySQL**:
```bash
# 백업
docker exec my-mysql mysqldump -u root -p dbname > backup.sql

# 복원
docker exec -i my-mysql mysql -u root -p dbname < backup.sql
```

**MongoDB**:
```bash
# 백업
docker exec my-mongo mongodump --archive=/backup/dump.gz --gzip

# 복원
docker exec my-mongo mongorestore --archive=/backup/dump.gz --gzip
```

**재해 복구 전략**:

**3-2-1 백업 규칙**:
- **3개의 복사본**: 원본 + 2개 백업
- **2가지 다른 미디어**: 로컬 디스크 + 클라우드
- **1개는 오프사이트**: 다른 지역/데이터센터

**예시**:
```
원본: Docker Volume (프로덕션 서버)
  ├─ 백업 1: 로컬 NAS (매일 자동)
  ├─ 백업 2: AWS S3 (매주 자동)
  └─ 백업 3: Glacier (매월, 장기 보관)
```

**백업 검증**:
```bash
# 백업 무결성 검증 (MD5 체크섬)
docker run --rm \
  -v myvolume:/data:ro \
  alpine \
  sh -c "find /data -type f -exec md5sum {} +" > checksums.txt

# 복원 후 검증
docker run --rm \
  -v myvolume-restored:/data:ro \
  -v $(pwd):/checksums \
  alpine \
  sh -c "cd /data && md5sum -c /checksums/checksums.txt"
```

### 실무 적용
프로덕션에서는 클라우드 제공자의 자동 스냅샷 기능을 활용한다 (AWS EBS, Azure Disk, GCP Persistent Disk). 정기적으로 복원 테스트를 수행하여 백업이 실제로 작동하는지 확인한다. 중요한 DB는 논리적 백업(dump)과 물리적 백업(snapshot)을 병행한다.

---

## Q5. 데이터 마이그레이션은 어떻게 수행하는가? (호스트 간, 클라우드 간)

### 왜 이 질문이 중요한가
서버를 교체하거나 클라우드를 이전할 때 Volume 데이터를 안전하게 옮겨야 한다. 다운타임을 최소화하면서 데이터 무결성을 보장하는 방법이 필요하다.

### 답변
**시나리오별 마이그레이션 전략**:

**1. 같은 호스트 내 Volume 복사**:
```bash
# Volume-to-Volume 복사
docker run --rm \
  -v old-volume:/source:ro \
  -v new-volume:/target \
  alpine \
  cp -av /source/. /target/

# 검증
docker run --rm \
  -v old-volume:/old:ro \
  -v new-volume:/new:ro \
  alpine \
  diff -r /old /new
```

**2. 다른 호스트로 마이그레이션**:

**방법 A: tar + SSH**:
```bash
# 호스트 A에서 백업 생성
docker run --rm \
  -v myvolume:/data:ro \
  alpine \
  tar czf - -C /data . | \
  ssh user@host-b "cat > /tmp/volume-backup.tar.gz"

# 호스트 B에서 복원
ssh user@host-b "docker run --rm \
  -v myvolume:/data \
  -v /tmp:/backup \
  alpine \
  tar xzf /backup/volume-backup.tar.gz -C /data"
```

**방법 B: rsync (증분 동기화)**:
```bash
# 호스트 A
VOL_A=$(docker volume inspect myvolume --format '{{.Mountpoint}}')

# 호스트 B로 rsync
sudo rsync -avz --progress \
  $VOL_A/ \
  user@host-b:/var/lib/docker/volumes/myvolume/_data/

# 서비스 중단 후 최종 동기화 (변경분만)
sudo rsync -avz --delete \
  $VOL_A/ \
  user@host-b:/var/lib/docker/volumes/myvolume/_data/
```

**방법 C: Docker Registry + Volume Plugin**:
```bash
# 호스트 A: 볼륨 데이터를 이미지로 변환
docker run --rm \
  -v myvolume:/data:ro \
  alpine \
  tar czf - -C /data . | \
  docker import - myvolume-image:latest

docker push myregistry.io/myvolume-image:latest

# 호스트 B: 이미지를 볼륨으로 복원
docker pull myregistry.io/myvolume-image:latest
docker create --name temp myregistry.io/myvolume-image:latest
docker export temp | \
  docker run --rm -i \
    -v myvolume:/data \
    alpine \
    tar xf - -C /data
docker rm temp
```

**3. 클라우드 간 마이그레이션**:

**AWS → Azure 예시**:
```bash
# AWS EBS 스냅샷 생성
aws ec2 create-snapshot --volume-id vol-123

# 스냅샷을 S3로 내보내기
aws ec2 export-image --image-id ami-123 --s3-export-location ...

# Azure로 복사
azcopy copy \
  https://s3.amazonaws.com/bucket/snapshot.vhd \
  https://mystorageacct.blob.core.windows.net/container/

# Azure Disk 생성
az disk create --source https://.../snapshot.vhd
```

**4. 최소 다운타임 마이그레이션**:

**Phase 1: 초기 동기화 (서비스 실행 중)**:
```bash
# 호스트 A → B: 대부분의 데이터 복사
rsync -av --progress $VOL_A/ user@host-b:$VOL_B/
```

**Phase 2: 서비스 중단**:
```bash
# 호스트 A: 쓰기 작업 중지
docker stop myapp
```

**Phase 3: 최종 동기화 (변경분만)**:
```bash
# 델타 동기화 (빠름)
rsync -av --delete $VOL_A/ user@host-b:$VOL_B/
```

**Phase 4: 서비스 재개**:
```bash
# 호스트 B: 서비스 시작
docker start myapp
```

**다운타임**: 최종 동기화 시간만 (수초~수분)

**5. Zero-Downtime 마이그레이션 (복제 기반)**:

**PostgreSQL 예시**:
```yaml
# 호스트 A: Primary DB
# 호스트 B: Replica DB (Streaming Replication)

# 1. 호스트 B에서 Replica 구성
# 2. Replica가 Primary를 따라잡을 때까지 대기
# 3. Primary를 ReadOnly로 전환
# 4. Replica를 Primary로 승격
# 5. 애플리케이션을 호스트 B로 전환
```

**데이터 무결성 검증**:
```bash
# 체크섬 비교
docker run --rm -v myvolume:/data:ro alpine \
  sh -c "find /data -type f -exec md5sum {} +" | sort > checksums-a.txt

ssh user@host-b "docker run --rm -v myvolume:/data:ro alpine \
  sh -c 'find /data -type f -exec md5sum {} +' | sort" > checksums-b.txt

diff checksums-a.txt checksums-b.txt
```

### 실무 적용
대규모 마이그레이션은 rsync를 사용하여 초기 동기화를 수행하고, 서비스 중단 시간에 최종 델타만 동기화한다. 클라우드 간 이동은 클라우드 제공자의 마이그레이션 서비스(AWS DataSync, Azure Migrate)를 활용한다. 중요한 데이터는 마이그레이션 후 반드시 체크섬 검증을 수행한다.

---

## Q6. 스토리지 드라이버(overlay2, devicemapper 등)는 Volume과 어떻게 다른가?

### 왜 이 질문이 중요한가
스토리지 드라이버와 Volume은 모두 데이터를 저장하지만 목적과 동작 방식이 다르다. 혼동하면 성능이나 영속성 문제가 발생할 수 있다.

### 답변
**스토리지 드라이버 vs Volume**:

```
┌─────────────────────────────────────────────────────────┐
│               스토리지 드라이버 (overlay2)                │
│              이미지 레이어 + Writable Layer 관리          │
└─────────────────────────────────────────────────────────┘

  Image Layers (Read-Only)          Container
  ┌────────────────────────┐        ┌────────────────────┐
  │ Layer 3: app.js        │        │ Writable Layer     │
  ├────────────────────────┤        │ (로컬 스토리지)     │
  │ Layer 2: npm packages  │────┐   │ • /tmp/cache.db    │
  ├────────────────────────┤    │   │ • /var/log/app.log │
  │ Layer 1: OS files      │    │   └────────────────────┘
  └────────────────────────┘    │
                                │ overlay2로 통합
                                ▼
                         Unified Filesystem
                         (Copy-on-Write)

  용도: 이미지 레이어 저장, 컨테이너별 변경사항
  영속성: 컨테이너 삭제 시 데이터 삭제
  관리: Docker가 자동 관리
  성능: 읽기 빠름, 쓰기는 CoW 오버헤드 있음

┌─────────────────────────────────────────────────────────┐
│                      Volume                              │
│                    데이터 영속화                          │
└─────────────────────────────────────────────────────────┘

  Docker Volume                    Container
  ┌────────────────────────┐      ┌────────────────────┐
  │ /var/lib/docker/       │      │ /data ─────────────┼─┐
  │  volumes/myvolume/     │◄─────┤                    │ │
  │   _data/               │      │                    │ │
  │     • db.sqlite        │      └────────────────────┘ │
  │     • uploads/         │                             │
  │     • backups/         │                             │
  └────────────────────────┘                             │
                                                          │
  용도: 영속 데이터 저장 (DB, 파일 등)                    │
  영속성: 컨테이너 삭제 후에도 유지                        │
  관리: docker volume 명령어로 관리                       │
  성능: 직접 I/O, CoW 오버헤드 없음                       │
                                                          │
  ┌────────────────────────────────────────────────────────┘
  └─► 스토리지 드라이버와 무관하게 동작
```

**주요 스토리지 드라이버**:

| 드라이버 | 메커니즘 | 장점 | 단점 | 사용처 |
|----------|---------|------|------|--------|
| **overlay2** | Union FS | 빠름, 효율적 | - | 대부분 (권장) |
| **aufs** | Union FS | 오래된 안정화 | 커널 지원 제한 | 레거시 |
| **devicemapper** | Block 기반 | 안정적 | 느림, 복잡 | RHEL 7 |
| **btrfs** | CoW FS | 스냅샷 빠름 | 메타데이터 오버헤드 | Btrfs 파일시스템 |
| **zfs** | CoW FS | 강력한 기능 | 메모리 소비 큼 | ZFS 파일시스템 |
| **vfs** | 복사 기반 | 단순 | 매우 느림 | 테스트용 |

**overlay2 동작 원리**:
```bash
# 이미지 레이어 확인
$ docker image inspect nginx --format='{{.RootFS.Layers}}'
[
  sha256:abc123...,
  sha256:def456...,
  sha256:ghi789...
]

# overlay2 마운트 구조
$ mount | grep overlay
overlay on /var/lib/docker/overlay2/.../merged type overlay (
  lowerdir=/var/lib/docker/overlay2/l/ABC:/var/lib/docker/overlay2/l/DEF,
  upperdir=/var/lib/docker/overlay2/.../diff,
  workdir=/var/lib/docker/overlay2/.../work
)
```

**Copy-on-Write (CoW) 동작**:
```
┌─────────────────────────────────────────────────────────┐
│              CoW in Writable Layer                       │
└─────────────────────────────────────────────────────────┘

1. 읽기 작업:
   Container → Read /etc/nginx/nginx.conf
     → Lower Layer (Image)에서 직접 읽음 (빠름)

2. 쓰기 작업 (파일이 Image에 있음):
   Container → Write /etc/nginx/nginx.conf
     → Image Layer에서 Writable Layer로 복사 (CoW)
     → Writable Layer에서 수정
     → 오버헤드 발생 (느림)

3. 새 파일 생성:
   Container → Create /tmp/cache.db
     → Writable Layer에 직접 생성 (빠름)
```

**Volume을 사용해야 하는 이유**:
1. **CoW 오버헤드 회피**: Volume은 직접 I/O, 복사 비용 없음
2. **영속성**: 컨테이너 삭제 후에도 데이터 유지
3. **공유**: 여러 컨테이너가 동일 Volume 접근 가능
4. **백업 용이**: `docker volume` 명령어로 관리
5. **드라이버 독립성**: 스토리지 드라이버 변경 시에도 Volume 데이터 유지

**성능 비교**:
| 작업 | Writable Layer (overlay2) | Volume | 차이 |
|------|--------------------------|--------|------|
| 새 파일 생성 | 15k/s | 15k/s | 동일 |
| 기존 파일 수정 (작음) | 8k/s | 14k/s | -43% |
| 기존 파일 수정 (큼) | 200 MB/s | 500 MB/s | -60% |
| DB 쓰기 워크로드 | 느림 (CoW) | 빠름 | -50% |

### 실무 적용
스토리지 드라이버는 변경할 일이 거의 없다 (기본 overlay2 사용). 중요한 것은 DB 파일, 로그, 업로드 파일 등 영속 데이터는 반드시 Volume에 저장하고, Writable Layer는 임시 파일만 사용하는 것이다. Writable Layer에 대용량 데이터를 쓰면 성능 저하와 디스크 낭비가 발생한다.

---

## Q7. NFS 볼륨을 사용할 때 주의사항과 최적화 방법은?

### 왜 이 질문이 중요한가
NFS는 여러 호스트에서 동일한 데이터에 접근할 수 있는 간단한 방법이지만, 성능과 일관성 문제가 있다. 올바르게 설정하지 않으면 데이터 손상이나 심각한 성능 저하가 발생한다.

### 답변
**NFS Volume 구성**:

```yaml
# docker-compose.yaml
services:
  app:
    volumes:
      - nfs-data:/data

volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw,nfsvers=4.1
      device: ":/exports/data"
```

**NFS 버전 선택**:
| 버전 | 특징 | 성능 | 권장 |
|------|------|------|------|
| NFSv3 | 간단, 널리 지원 | 중간 | 레거시 |
| NFSv4.0 | 상태 기반, 보안 강화 | 중간 | 일반 |
| NFSv4.1 | pNFS 지원, 병렬 I/O | 높음 | **권장** |
| NFSv4.2 | 서버 사이드 복사, 희소 파일 | 최고 | 최신 |

**성능 최적화 옵션**:

```yaml
volumes:
  nfs-optimized:
    driver: local
    driver_opts:
      type: nfs
      o: >-
        addr=192.168.1.100,
        nfsvers=4.1,
        rw,
        async,
        noatime,
        nodiratime,
        rsize=1048576,
        wsize=1048576,
        hard,
        timeo=600,
        retrans=2,
        tcp
      device: ":/exports/data"
```

**옵션 설명**:
| 옵션 | 설명 | 권장 값 |
|------|------|---------|
| `async` | 비동기 쓰기 (빠름, 데이터 손실 위험) | 주의 |
| `sync` | 동기 쓰기 (느림, 안전) | DB용 |
| `noatime` | 접근 시간 미기록 (메타데이터 쓰기 감소) | 켜기 |
| `rsize` | 읽기 버퍼 크기 | 1048576 (1MB) |
| `wsize` | 쓰기 버퍼 크기 | 1048576 (1MB) |
| `hard` | 서버 장애 시 재시도 (무한 대기) | 일반적 |
| `soft` | 서버 장애 시 포기 (I/O 에러) | 비권장 |
| `timeo` | 타임아웃 (0.1초 단위) | 600 (60초) |
| `tcp` | UDP 대신 TCP 사용 | 권장 |

**주의사항**:

**1. 파일 락킹 문제**:
```bash
# NFS는 파일 락킹이 불완전할 수 있음
# SQLite 같은 파일 기반 DB는 NFS에서 손상 가능

# 해결책 1: 네트워크 DB 사용 (PostgreSQL, MySQL)
# 해결책 2: lockd 데몬 확인
systemctl status nfs-lock
```

**2. 캐시 일관성**:
```yaml
# 캐시를 비활성화하여 일관성 보장 (느림)
driver_opts:
  o: addr=...,noac,lookupcache=none

# 또는 짧은 캐시 TTL
driver_opts:
  o: addr=...,actimeo=1  # 1초 캐시
```

**3. UID/GID 매핑**:
```bash
# 호스트와 NFS 서버의 UID가 일치해야 함
# 불일치 시 권한 문제 발생

# NFS 서버: /etc/exports
/exports/data *(rw,sync,no_subtree_check,all_squash,anonuid=1000,anongid=1000)
```

**4. 네트워크 장애**:
```yaml
# soft 옵션 사용 시 데이터 손실 가능
# hard 옵션 사용 시 네트워크 장애 시 컨테이너 멈춤

# 해결: 타임아웃 + 재시도 제한
driver_opts:
  o: addr=...,hard,timeo=600,retrans=2,_netdev
```

**성능 벤치마크**:
| 워크로드 | 로컬 Volume | NFS (최적화) | NFS (기본) |
|----------|------------|-------------|-----------|
| 순차 읽기 | 3000 MB/s | 800 MB/s | 400 MB/s |
| 순차 쓰기 | 2500 MB/s | 600 MB/s | 200 MB/s |
| 메타데이터 연산 | 20k/s | 5k/s | 1k/s |
| DB 쓰기 | 10k TPS | 2k TPS | 500 TPS |

**대안: 분산 스토리지**:
- **GlusterFS**: 복제 + 분산, NFS보다 안정적
- **CephFS**: 확장성 높음, 복잡
- **Longhorn**: Kubernetes 전용, 간단

### 실무 적용
NFS는 읽기 위주 워크로드(정적 파일, 미디어)에 적합하다. 쓰기 집약적 DB나 로그는 로컬 Volume이나 클라우드 블록 스토리지를 사용한다. Kubernetes에서는 NFS Subdir External Provisioner나 EFS CSI Driver를 사용하여 동적 프로비저닝을 구성한다.
