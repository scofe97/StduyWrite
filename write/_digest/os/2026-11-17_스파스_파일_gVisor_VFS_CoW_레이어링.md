> 출처: 외부 AI 대화 · 2026-11-17 · gvx 류 샌드박스 아래의 VFS·블록 스토리지·CoW 이론과 학습 자료 · 분야: os-keywords · 미검증

## 요점

한 줄: gvx 류 샌드박스는 스파스 파일·홀펀칭, 유저스페이스 VFS, CoW 레이어링 세 이론 위에서 돌아가며, 자료는 OSTEP 영속성 파트 → 커널 문서 → gVisor·gvx 코드 순으로 읽으라는 추천입니다.

- 블록 할당: 파일시스템은 데이터를 고정 크기 블록으로 관리하고 inode 와 extent tree 로 논리 오프셋을 물리 블록에 잇습니다. 쓰지 않은 구간에 블록을 할당하지 않는 것이 스파스 파일이고, 이미 할당된 구간을 `fallocate` 의 `PUNCH_HOLE` 로 풀어 공간을 돌려주는 것이 홀펀칭입니다. `ext4lite` 의 용량 축소가 이 원리입니다.
- 유저스페이스 커널: gVisor 의 Sentry 가 `open`·`mount`·`write` 같은 시스템 콜을 사용자 공간에서 받아 처리합니다. 자체 VFS 와 inode·dentry 캐시를 두므로 호스트 커널 권한 없이 `.ext4` 파일 하나를 블록 디바이스처럼 읽고, `xattr` 와 화이트아웃도 다룹니다.
- CoW 레이어링: 읽기 전용 베이스 위에 변경분만 쓰는 층을 겹겹이 쌓습니다. 디렉터리 단위(overlayfs)와 블록·익스텐트 단위(reflink 계열) 두 갈래가 있고, 후자는 포인터만 복제해서 큰 환경도 빨리 복제합니다.
- 읽는 순서: OSTEP 영속성 파트와 `man 2 fallocate` 로 시스템 콜 동작을 잡고, 로컬에서 직접 마운트해 블록 사용량을 눈으로 본 뒤, gVisor VFS 문서와 gvx 의 `ext4lite` 코드를 읽습니다.
- 찾을 키워드: `fallocate`, `FALLOC_FL_PUNCH_HOLE`, `FICLONERANGE`, `cp --reflink=auto`, `virtio-fs`, `EROFS`, `lowerdir`·`upperdir`.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| 스파스 파일 | 쓰지 않은 구간에 물리 블록을 할당하지 않고 메타데이터에만 빈 구간으로 적는 파일 | |
| 홀펀칭 (`PUNCH_HOLE`) | 이미 할당된 블록 범위를 `fallocate` 로 풀어 구멍으로 바꾸는 호출 | |
| inode·extent tree | 논리 오프셋과 물리 블록 사이 매핑을 담는 구조 | [Systems Performance 08-02](../../02_os/book/systems-performance/08-02.파일 시스템 — 아키텍처·캐시·파일시스템 유형.md) (일부: ext4 의 extent 기반 소개만, extent tree 구조 없음) |
| 유저스페이스 커널 (Sentry) | 시스템 콜을 사용자 공간 런타임이 가로채 처리하는 구조 | [container-security 08-01 §4](../../08_cloud/book/container-security/08-01.컨테이너 격리 강화 — 샌드박싱의 세 갈래.md) |
| 유저스페이스 VFS | Sentry 안에 둔 독자 VFS 계층과 inode·dentry 캐시 | |
| `xattr`·화이트아웃 | 확장 속성, 그리고 오버레이에서 삭제를 표시하는 문자 디바이스 | [LML 05-01](../../02_os/book/learning-modern-linux/05-01.모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다.md) (일부: 화이트아웃만, `xattr` 없음) |
| CoW 레이어링·overlayfs | 읽기 전용 하위 층 위에 쓰기 가능한 상위 층을 겹쳐 변경분만 기록 | [LML 05-01](../../02_os/book/learning-modern-linux/05-01.모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다.md), [OverlayFS 와 idmapped mount](../../02_os/docs/kernel/OverlayFS%20와%20idmapped%20mount%20—%20Netflix%20사례.md) (일부: lowerdir·upperdir 와 마운트 비용만, 화이트아웃 없음) |
| reflink (`FICLONERANGE`) | 파일 복사 때 데이터 블록을 복제하지 않고 같은 블록을 공유 | [LML 05-01](../../02_os/book/learning-modern-linux/05-01.모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다.md) |
| LFS·CoW 파일시스템 | 모든 쓰기를 순차 로그로 바꾸는 파일시스템 설계 | [OSTEP README](../../02_os/book/ostep_operating-systems-three-easy-pieces/README.md) (일부: 43장 계획 표만, 정독 노트 없음) |
| Git worktree | 같은 저장소에 작업 트리를 여러 개 두는 기능 | [claude-code 05-04](../../10_AI/docs/claude-code/05-04.Session Management·Git Worktrees·Agent Teams·Remote Control.md) (일부: `claude --worktree` 사용법만, 내부 구조 없음) |
| `ext4lite` | gvx 의 단일 `.ext4` 파일용 유저스페이스 ext4 구현 | |
| `virtio-fs`·EROFS | 호스트 디렉터리 공유 파일시스템과 읽기 전용 압축 이미지 파일시스템 | |
| lazy pulling | 컨테이너 이미지를 통째로 풀지 않고 필요한 부분만 가져오는 방식 | |



## 자료와 실습

- 자료:
  - 『Operating Systems: Three Easy Pieces』 Persistence 파트: inode·블록 할당·저널링·LFS 와 CoW 기초를 다룹니다. 정독 노트는 [ostep](../../02_os/book/ostep_operating-systems-three-easy-pieces/README.md) 입니다(40~43장 노트는 아직 없음).
  - [ext4 커널 문서](https://docs.kernel.org/filesystems/ext4/): extent 구조를 보는 용도입니다.
  - [overlayfs 커널 문서](https://docs.kernel.org/filesystems/overlayfs.html): `lowerdir`·`upperdir` 와 화이트아웃 처리 원리입니다.
  - 『Linux System Programming』(Robert Love): `fallocate`·`ftruncate`·`mount`·`unshare` 명세와 엣지 케이스를 익히는 용도입니다. 정독 노트가 있는 책은 [tlpi](../../02_os/book/tlpi_the-linux-programming-interface/README.md) 입니다.
  - [google/gvisor](https://github.com/google/gvisor): 공식 Architecture Guide 와 `pkg/sentry/vfs/`, `pkg/sentry/fsimpl/` 에서 리눅스 파일시스템을 Go 로 다시 구현한 모습을 봅니다.
  - [gfire-sigs/gvx](https://github.com/gfire-sigs/gvx): 단일 `.ext4` 파일을 Go 로 파싱·마운트하는 `ext4lite` 와 마운트 체이닝 로직입니다. `io.ReaderAt`·`io.WriterAt` 로 블록 디바이스를 추상화한 부분을 봅니다.
  - [containerd/stargz-snapshotter](https://github.com/containerd/stargz-snapshotter), [firecracker](https://github.com/firecracker-microvm/firecracker): lazy pulling 과 마이크로VM 스냅샷 구현체입니다.
  - [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk): Git 의 worktree 를 CLI 로 자동화하는 Rust 프로젝트입니다.
- 실습:
  - 순서 2: `truncate -s 1G disk.img` 로 빈 파일을 만들고 `mkfs.ext4`·`mount -o loop`·overlayfs 를 손으로 마운트하고 체이닝합니다. 완료: `du -sh` 와 `ls -lh` 의 차이로 블록 사용량 변화를 확인합니다.



## 경고

- ⚠ Git worktree 를 CoW 로 본 주장: 「`worktrunk` 의 Git Worktree 는 파일·디렉터리 단위 CoW」 는 맞지 않습니다. [git-worktree 문서](https://git-scm.com/docs/git-worktree)는 `add` 가 경로에 작업 트리를 만들고 커밋을 체크아웃하는 기능으로 설명하며 CoW·reflink 는 나오지 않습니다. 확인됨. worktrunk 저장소 자체는 확인하지 않았습니다.
- ⚠ 홀펀칭이 블록을 「호스트 OS」 에 즉시 돌려준다는 주장: [fallocate(2)](https://man7.org/linux/man-pages/man2/fallocate.2.html) 는 `PUNCH_HOLE` 이 범위의 온전한 파일시스템 블록을 파일에서 떼고, 일부 블록은 0 으로 채운다고 적습니다. 블록은 그 파일이 놓인 파일시스템으로 돌아가므로 「호스트」 는 이미지 파일이 호스트 파일시스템 위에 있을 때만 맞습니다. 지원도 파일시스템마다 달라서 XFS·ext4·Btrfs·tmpfs 등이며 미지원이면 오류를 돌려줍니다. 확인됨.
- ⚠ Btrfs·ZFS 의 reflink 와 「수 밀리초」: OpenZFS 의 파일 복제(block cloning)는 [2.2.0 릴리스](https://github.com/openzfs/zfs/releases/tag/zfs-2.2.0)에 들어온 기능이고 스냅샷과는 다른 기능입니다. 확인됨. 「수십 GB 를 수 밀리초」 는 측정 근거가 없어서 과장 여부를 확인하지 못했습니다.
- ⚠ `FICLONERANGE`/reflink 를 「리눅스/유닉스 표준」 이라 한 주장: [ioctl_ficlonerange(2)](https://man7.org/linux/man-pages/man2/ioctl_ficlonerange.2.html) 에 따르면 Linux 4.5 에 들어온 ioctl 이고 원래 Btrfs 전용 `BTRFS_IOC_CLONE` 이었습니다. macOS APFS 는 다른 호출인 [`clonefile(2)`](https://keith.github.io/xcode-man-pages/clonefile.2.html) 을 씁니다. 표준 규격이 아니라 파일시스템 기능입니다. 확인됨.
- ⚠ ext4 커널 문서가 `fallocate`·`PUNCH_HOLE` 을 설명한다는 주장: [docs.kernel.org/filesystems/ext4/](https://docs.kernel.org/filesystems/ext4/) 목차 페이지에는 두 낱말이 없습니다. 하위 장은 전수로 보지 않아 미확인이고, 지원 사실은 위 fallocate(2) 가 근거입니다.
- ⚠ 《Linux System Programming》 이 `fallocate`·`mount`·`unshare` 를 다룬다는 주장: 목차를 확인하지 못했습니다. 미확인.
- ⚠ Firecracker 가 블록 디바이스 스냅샷을 체이닝한다는 주장: [Firecracker 스냅샷 문서](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md)가 다루는 것은 게스트 메모리 파일과 microVM 상태 파일이고, 블록 디바이스 체이닝으로 부팅한다는 문구는 찾지 못했습니다. diff 스냅샷은 developer preview 로 적혀 있습니다.
- ⚠ gVisor 가 `.ext4` 를 해석해 `xattr`·화이트아웃을 「완벽히」 처리한다는 주장: 이 기능은 gVisor 본가가 아니라 gvx 저장소의 `ext4lite` 에 있습니다. [google/gvisor](https://github.com/google/gvisor/tree/master/pkg/sentry/fsimpl) 의 `fsimpl` 에는 `erofs`·`overlay`·`gofer`·`tmpfs` 등이 있고 ext4 는 없습니다. gvx 쪽은 [README](https://github.com/gfire-sigs/gvx)가 `security.*`·`trusted.overlay.*` 확장 속성 지원을 적으며 `xattr.go` 도 있습니다. 구현은 확인됨, 「완벽히」 는 과장이며 완전성은 확인하지 못했습니다.
- ⚠ `ext4lite` 의 자동 용량 축소 원리: gvx 소스의 `storage_linux.go` 는 `FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE` 로 홀펀칭합니다. `storage_darwin.go` 는 `F_PUNCHHOLE`(16 KiB 정렬)을 씁니다. `trim.go` 는 flush 뒤 64 KiB 이상 연속 빈 구간을 즉시 풀어 줍니다. 확인됨. README 는 홀펀칭이 안 되는 파일시스템이면 밀집 할당으로 물러난다고 적습니다. 마운트를 해제할 때 끝 그룹을 압축한다는 말도 있습니다.
- ⚠ `virtio-fs` 와 EROFS 가 「가장 많이 조합」 된다는 주장: 조합 빈도의 근거가 없어 확인하지 못했습니다. 다만 gVisor 의 `fsimpl` 에 `erofs` 가 있는 것은 확인했습니다.
- ⚠ stargz-snapshotter·Firecracker 를 「업계 표준」 이라 한 주장: 확인하지 못했습니다.
