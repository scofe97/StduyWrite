# Chapter 3: Getting Docker

---

## 📌 핵심 요약
> Docker를 설치하는 방법은 **Docker Desktop**, **Multipass**, **Linux 직접 설치** 세 가지가 있다. **Docker Desktop**이 가장 권장되는 방법으로, 완전한 Docker 환경과 UI, 플러그인, Kubernetes 클러스터까지 제공한다. Mac에서 Docker는 **경량 Linux VM** 내부에서 실행되며, 이것이 Mac에서 Linux 컨테이너만 지원되는 이유다.

---

## 🎯 학습 목표
이 챕터를 읽고 나면:
- [ ] Docker 설치의 세 가지 방법을 알고 상황에 맞게 선택할 수 있다
- [ ] Docker Desktop의 장점과 라이선스 정책을 이해할 수 있다
- [ ] Windows와 Mac에서 Docker Desktop을 설치할 수 있다
- [ ] Mac에서 Docker가 Linux VM 내부에서 실행됨을 이해할 수 있다
- [ ] Multipass와 Linux 직접 설치 방법을 알고 있다

---

## 📖 본문 정리

### 1. Docker 설치 방법 비교

```
┌─────────────────────────────────────────────────────────┐
│              Docker 설치 방법 3가지                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │            🥇 Docker Desktop                │      │
│   │           (가장 권장되는 방법)               │      │
│   │                                             │      │
│   │  ✅ 완전한 기능     ✅ UI 제공              │      │
│   │  ✅ 플러그인 마켓   ✅ Kubernetes 포함      │      │
│   │  ✅ scout/debug/init 지원                   │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │            🥈 Multipass                     │      │
│   │        (Docker Desktop 사용 불가 시)         │      │
│   │                                             │      │
│   │  ✅ 클라우드 스타일 VM   ✅ 다중 노드 가능   │      │
│   │  ⚠️ scout/debug/init 미지원                 │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │            🥉 Linux 직접 설치               │      │
│   │        (서버 환경, 프로덕션용)               │      │
│   │                                             │      │
│   │  ✅ 경량 설치        ✅ 서버 최적화          │      │
│   │  ⚠️ scout/debug/init 미지원                 │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

| 방법 | 장점 | 단점 | 권장 상황 |
|------|------|------|----------|
| **Docker Desktop** | 완전한 기능, UI, 플러그인 | 유료 라이선스 (대기업) | 개발 환경 (권장) |
| **Multipass** | 간편한 VM, 다중 노드 | 일부 기능 미지원 | Desktop 불가 시 |
| **Linux 직접 설치** | 경량, 서버 최적화 | UI 없음, 기능 제한 | 프로덕션 서버 |

---

### 2. Docker Desktop

#### 2.1 Docker Desktop이란?

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Desktop 구성                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │              Docker Desktop                  │      │
│   │  ┌─────────────────────────────────────┐    │      │
│   │  │                                     │    │      │
│   │  │  🐳 Docker Engine                   │    │      │
│   │  │  🎨 Slick UI                        │    │      │
│   │  │  🔌 Extensions Marketplace          │    │      │
│   │  │  📦 Docker Compose                  │    │      │
│   │  │  ☸️  Kubernetes Cluster             │    │      │
│   │  │  🔧 Latest Plugins & Features       │    │      │
│   │  │     • docker scout                  │    │      │
│   │  │     • docker debug                  │    │      │
│   │  │     • docker init                   │    │      │
│   │  │                                     │    │      │
│   │  └─────────────────────────────────────┘    │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**핵심 기능:**
- **Docker Engine**: 컨테이너 실행 엔진
- **UI**: 직관적인 데스크톱 인터페이스
- **Extensions**: 마켓플레이스에서 기능 확장
- **Docker Compose**: 멀티 컨테이너 정의
- **Kubernetes**: 로컬 K8s 클러스터

---

#### 2.2 라이선스 정책

```
┌─────────────────────────────────────────────────────────┐
│               Docker Desktop 라이선스                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ✅ 무료 사용 가능:                                    │
│   ┌─────────────────────────────────────────────┐      │
│   │  • 개인 사용 (Personal use)                 │      │
│   │  • 교육 목적 (Education)                    │      │
│   │  • 소규모 기업                              │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   💰 유료 라이선스 필요:                                │
│   ┌─────────────────────────────────────────────┐      │
│   │  업무용 AND (다음 중 하나 해당 시):          │      │
│   │                                             │      │
│   │  • 직원 250명 이상                          │      │
│   │        OR                                   │      │
│   │  • 연 매출 $10M 이상                        │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

#### 2.3 플랫폼별 컨테이너 지원

```
┌─────────────────────────────────────────────────────────┐
│           Docker Desktop 플랫폼별 컨테이너 지원          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Windows Pro/Enterprise:                               │
│   ┌─────────────────────────────────────────────┐      │
│   │  ✅ Windows Containers                      │      │
│   │  ✅ Linux Containers (via WSL 2)            │      │
│   │                                             │      │
│   │  💡 우클릭 → "Switch to Windows containers" │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   Windows Home / Mac / Linux:                           │
│   ┌─────────────────────────────────────────────┐      │
│   │  ❌ Windows Containers                      │      │
│   │  ✅ Linux Containers Only                   │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   📊 현실: 거의 모든 컨테이너 = Linux 컨테이너           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 3. Windows에서 Docker Desktop 설치

#### 3.1 사전 요구사항

```
┌─────────────────────────────────────────────────────────┐
│              Windows 사전 요구사항                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   필수 조건:                                            │
│   ┌─────────────────────────────────────────────┐      │
│   │  ✓ Windows 10/11 64-bit                     │      │
│   │  ✓ Hardware Virtualization (BIOS에서 활성화) │      │
│   │  ✓ WSL 2 (Windows Subsystem for Linux 2)    │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   ⚠️ 주의: BIOS 설정 변경 시 매우 신중하게!              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 3.2 설치 및 확인

```bash
# 설치 후 버전 확인
$ docker version

Server: Docker Desktop 4.42.0 (192140)
 Engine:
  Version:          28.1.1
  API version:      1.49 (minimum version 1.24)
  Go version:       go1.23.8
  OS/Arch:          linux/amd64    # ← Linux 컨테이너 모드!
```

**설치 단계:**
1. "install Docker Desktop on Windows" 검색
2. 다운로드 페이지에서 설치 파일 다운로드
3. 설치 시 **WSL 2 backend 활성화** 선택
4. 설치 완료 후 시작 메뉴에서 Docker Desktop 시작
5. 작업 표시줄의 🐳 아이콘으로 시작 상태 확인

---

### 4. Mac에서 Docker Desktop 설치

#### 4.1 Mac 아키텍처 이해

```
┌─────────────────────────────────────────────────────────┐
│            Docker Desktop on Mac 아키텍처               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │               macOS                          │      │
│   │  ┌─────────────────────────────────────┐    │      │
│   │  │         Docker CLI (Client)         │    │      │
│   │  │         darwin/arm64 또는            │    │      │
│   │  │         darwin/amd64                │    │      │
│   │  └────────────────┬────────────────────┘    │      │
│   │                   │ API                     │      │
│   │                   ▼                         │      │
│   │  ┌─────────────────────────────────────┐    │      │
│   │  │    Lightweight Linux VM             │    │ ←핵심│
│   │  │  ┌─────────────────────────────┐   │    │      │
│   │  │  │     Docker Engine           │   │    │      │
│   │  │  │     linux/arm64 또는         │   │    │      │
│   │  │  │     linux/amd64             │   │    │      │
│   │  │  │                             │   │    │      │
│   │  │  │   🐳 🐳 🐳 Containers       │   │    │      │
│   │  │  └─────────────────────────────┘   │    │      │
│   │  └─────────────────────────────────────┘    │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   💡 사용자는 VM 존재를 인식하지 못함 (Seamless)         │
│   💡 이것이 Mac에서 Linux 컨테이너만 지원되는 이유!       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> 💬 **비유**: Mac에서 Docker는 마치 번역기처럼 작동한다. 사용자는 한국어(Mac 명령)로 말하고, 숨겨진 번역기(Linux VM)가 영어(Linux 명령)로 변환하여 실행한다.

---

#### 4.2 설치 및 확인

```bash
# 설치 후 버전 확인
$ docker version

Client:
 Version:           28.1.1
 API version:       1.49
 OS/Arch:           darwin/arm64    # ← 네이티브 Mac 클라이언트

Server: Docker Desktop 4.42.0 (192140)
 Engine:
  Version:          28.1.1
  API version:      1.49 (minimum version 1.24)
  OS/Arch:          linux/arm64     # ← Linux VM 내부 실행!
 containerd:
  Version:          1.7.21
 runc:
  Version:          1.2.5
 docker-init:
  Version:          0.19.0
```

**Client vs Server OS/Arch:**

| 컴포넌트 | OS/Arch | 설명 |
|----------|---------|------|
| **Client** | darwin/arm64 (또는 amd64) | Mac 네이티브 앱 |
| **Server** | linux/arm64 (또는 amd64) | Linux VM 내부 실행 |

---

### 5. Multipass로 Docker 설치

#### 5.1 Multipass란?

```
┌─────────────────────────────────────────────────────────┐
│                      Multipass                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   목적: 클라우드 스타일 Linux VM을 로컬에 생성           │
│                                                         │
│   특징:                                                  │
│   ┌─────────────────────────────────────────────┐      │
│   │  ✅ 무료                                     │      │
│   │  ✅ 설치/사용 매우 간편                       │      │
│   │  ✅ Linux, Mac, Windows 지원                 │      │
│   │  ✅ 다중 노드 Docker 클러스터 구성 가능       │      │
│   │  ⚠️ scout/debug/init 미지원                  │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   URL: https://multipass.run/install                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 5.2 핵심 명령어

```bash
# 1. Docker 이미지로 VM 생성
$ multipass launch docker --name node1
# → Docker 사전 설치된 Ubuntu VM 생성 (1-2분 소요)

# 2. VM 목록 확인
$ multipass ls
Name    State      IPv4             Image
node1   Running    192.168.64.37    Ubuntu 24.04 LTS
                   172.17.0.1
                   172.18.0.1

# 3. VM 접속
$ multipass shell node1

# 4. Docker 확인 (VM 내부에서)
$ docker --version
Docker version 26.1.0, build 9714adc

$ docker info
Client: Docker Engine - Community
 Version:    27.3.1
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
  compose: Docker Compose (Docker Inc.)

# 5. VM에서 나가기
$ exit

# 6. VM 삭제
$ multipass delete node1
$ multipass purge
```

**명령어 정리:**

| 명령어 | 설명 |
|--------|------|
| `multipass launch docker --name <이름>` | Docker 포함 VM 생성 |
| `multipass ls` | VM 목록 조회 |
| `multipass shell <이름>` | VM 접속 |
| `multipass delete <이름>` | VM 삭제 (휴지통) |
| `multipass purge` | 완전 삭제 |

---

### 6. Linux에서 Docker 직접 설치

#### 6.1 Ubuntu에서 Snap 설치

```bash
# 1. Docker 설치 (snap 사용)
$ sudo snap install docker
docker 27.2.0 from Canonical✓ installed

# 2. 버전 확인
$ sudo docker --version
Docker version 27.2.0, build 3ab4256

# 3. 상세 정보 확인
$ sudo docker info
Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 27.2.0
```

#### 6.2 sudo 없이 Docker 사용

```bash
# 1. docker 그룹 생성
$ sudo groupadd docker

# 2. 현재 사용자를 docker 그룹에 추가
$ sudo usermod -aG docker $(whoami)

# 3. Docker 서비스 재시작
$ sudo service docker start

# 4. 이후 sudo 없이 사용 가능
$ docker --version
```

---

### 7. 설치 방법 비교 요약

```
┌─────────────────────────────────────────────────────────┐
│                  설치 방법 비교 요약                     │
├───────────────┬─────────────┬─────────────┬─────────────┤
│     기능      │Docker Desktop│  Multipass  │Linux 직접   │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ UI            │     ✅      │     ❌      │     ❌      │
│ docker scout  │     ✅      │     ❌      │     ❌      │
│ docker debug  │     ✅      │     ❌      │     ❌      │
│ docker init   │     ✅      │     ❌      │     ❌      │
│ Kubernetes    │     ✅      │  수동 설치   │  수동 설치   │
│ Extensions    │     ✅      │     ❌      │     ❌      │
│ 다중 노드     │     ❌      │     ✅      │     ✅      │
│ 프로덕션 적합 │     ❌      │     ⚠️      │     ✅      │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ 권장 상황     │  개발 환경   │Desktop 불가시│ 서버/프로덕션│
└───────────────┴─────────────┴─────────────┴─────────────┘
```

---

## 🔍 심화 학습

### 공식 설치 문서

| 플랫폼 | URL |
|--------|-----|
| Docker Desktop (Windows) | [docs.docker.com/desktop/windows/install](https://docs.docker.com/desktop/windows/install/) |
| Docker Desktop (Mac) | [docs.docker.com/desktop/mac/install](https://docs.docker.com/desktop/mac/install/) |
| Docker Desktop (Linux) | [docs.docker.com/desktop/linux/install](https://docs.docker.com/desktop/linux/install/) |
| Multipass | [multipass.run/install](https://multipass.run/install) |
| Docker Engine (Linux) | [docs.docker.com/engine/install](https://docs.docker.com/engine/install/) |

### WSL 2 관련
- [WSL 2 설치 가이드](https://learn.microsoft.com/en-us/windows/wsl/install)

---

## 💡 실무 적용 포인트

### Quick Reference: 어떤 설치 방법을 선택할까?

```
┌─────────────────────────────────────────────────────────┐
│                    설치 방법 결정 트리                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   개발/학습 목적인가?                                    │
│        │                                                │
│   ┌────┴────┐                                          │
│   Yes       No (프로덕션)                               │
│   │          │                                          │
│   ▼          ▼                                          │
│   Docker     Linux 직접 설치                            │
│   Desktop    (snap, apt, yum)                          │
│   사용 가능?                                            │
│   │                                                     │
│   ┌────┴────┐                                          │
│   Yes       No                                          │
│   │          │                                          │
│   ▼          ▼                                          │
│   Docker     Multipass                                  │
│   Desktop    또는                                       │
│              Linux VM                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 면접 질문

**Q1: Mac에서 Docker 컨테이너는 어디서 실행되나요?**
```
A: Mac에서 Docker 컨테이너는 경량 Linux VM 내부에서 실행됩니다.

   Docker Desktop은 이 VM을 자동으로 관리하며, 사용자에게는
   투명하게(seamlessly) API를 노출합니다.

   `docker version` 출력을 보면:
   - Client: darwin/arm64 (Mac 네이티브)
   - Server: linux/arm64 (Linux VM 내부)

   이것이 Mac에서 Linux 컨테이너만 지원되는 이유입니다.
```

**Q2: Docker Desktop의 라이선스 정책은 어떻게 되나요?**
```
A: Docker Desktop은 다음 경우 무료입니다:
   - 개인 사용
   - 교육 목적
   - 소규모 기업

   유료 라이선스가 필요한 경우:
   - 업무용 사용 AND
   - (직원 250명 이상 OR 연 매출 $10M 이상)
```

**Q3: Docker Desktop이 제공하지만 다른 설치 방법에서는 없는 기능은?**
```
A: Docker Desktop 전용 기능:
   - docker scout (보안 취약점 분석)
   - docker debug (컨테이너 디버깅)
   - docker init (프로젝트 초기화)
   - GUI/UI
   - Extensions Marketplace
   - 내장 Kubernetes 클러스터

   Multipass나 Linux 직접 설치에서는 이 기능들이 제공되지 않습니다.
```

**Q4: Windows에서 Docker Desktop 설치 전 필수 요구사항은?**
```
A: 세 가지 필수 요구사항:
   1. Windows 10/11 64-bit
   2. Hardware Virtualization 활성화 (BIOS에서 설정)
   3. WSL 2 (Windows Subsystem for Linux 2) 설치

   BIOS 설정 변경 시 주의가 필요하며, WSL 2 backend를
   활성화해야 Linux 컨테이너를 실행할 수 있습니다.
```

---

## ✅ 체크리스트

### Docker Desktop
- [ ] Docker Desktop의 구성 요소(Engine, UI, Extensions, Compose, K8s)를 알고 있다
- [ ] 라이선스 정책(무료: 개인/교육, 유료: 대기업)을 이해한다
- [ ] Windows에서 사전 요구사항(64-bit, Virtualization, WSL 2)을 알고 있다
- [ ] Mac에서 Docker가 Linux VM 내부에서 실행됨을 이해한다
- [ ] `docker version`으로 Client/Server OS/Arch 차이를 확인할 수 있다

### Multipass
- [ ] Multipass의 목적(클라우드 스타일 VM)을 이해한다
- [ ] `multipass launch`, `ls`, `shell`, `delete`, `purge` 명령어를 알고 있다
- [ ] Docker Desktop 대비 제한 사항(scout/debug/init 미지원)을 알고 있다

### Linux 직접 설치
- [ ] `sudo snap install docker`로 설치할 수 있다
- [ ] docker 그룹에 사용자를 추가하여 sudo 없이 사용하는 방법을 안다
- [ ] 프로덕션 환경에서 직접 설치가 적합한 이유를 이해한다

### 설치 방법 선택
- [ ] 상황에 맞는 설치 방법을 선택할 수 있다
- [ ] 각 방법의 장단점을 비교할 수 있다

---

## 🔗 참고 자료

- 📘 [Docker Desktop 공식 문서](https://docs.docker.com/desktop/)
- 📘 [Docker Engine 설치 가이드](https://docs.docker.com/engine/install/)
- 📘 [Multipass 공식 사이트](https://multipass.run/)
- 📘 [WSL 2 설치 가이드](https://learn.microsoft.com/en-us/windows/wsl/install)
- 📘 [Docker Licensing FAQ](https://www.docker.com/pricing/faq/)
