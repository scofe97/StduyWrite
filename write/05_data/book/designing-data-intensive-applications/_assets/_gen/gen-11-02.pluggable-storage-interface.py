# 11-02 §5 — 플러그어블 스토리지 인터페이스 계층 구조
# 사실 출처: 11-02 본문 §5(L88~L107; L103 VFS·open/read/write·Spark/Trino/Flink, L107 shared-disk=NAS·SAN), 원서 Ch.11 p.9(S3 API 플러그어블, FUSE/NFS, shared-nothing vs NAS/SAN), p.10(get/put, 불변 객체).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 900
BANNER_Y = 104
BANNER_H = 36

# 계층 1: 애플리케이션
L1_Y = 156
L1_H = 68

# 계층 2: 플러그어블 인터페이스 (focal)
L2_Y = 248
L2_H = 88

# 계층 3: 구현체 풀
L3_Y = 360
L3_H = 80

# 하단 아키텍처 대조 배너
ARCH_Y = 458
ARCH_H = 34

LEG_Y = 508
H = LEG_Y + 52

d = D(W, H, "11-02 · §5 PLUGGABLE STORAGE INTERFACE", "플러그어블 스토리지 인터페이스 계층",
      "VFS 유추에 기반한 표준 스토리지 프로토콜과 다중 저장소 분리 구조",
      "배치 프레임워크 계층 · S3 API 사실상 표준 · POSIX 호환 FUSE · 분산 스토리지 구현체")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "VFS 유추: Linux VFS가 로컬 파일시스템을 추상화하듯, 표준 인터페이스가 분산 구현체 은닉", 12, INK, KR, "middle", 600)

# 계층 1: 배치 프레임워크 및 쿼리 엔진 (INFO)
d.box(24, L1_Y, W - 48, L1_H, PAPER2, RULE, 0.9)
d.chip(110, L1_Y + 20, "배치 프레임워크 계층", INFO, 12)
d.t(210, L1_Y + 24, "저장소 구현 독립적 데이터 처리 엔진", 12, INK, KR, "start", 600)

fw_list = [
    ("Apache Spark", 40),
    ("Trino", 255),
    ("Apache Flink", 470),
    ("Hadoop MapReduce", 685),
]
for name, fx in fw_list:
    d.box(fx, L1_Y + 36, 175, 22, PAPER, INFO, 0.7)
    d.t(fx + 87, L1_Y + 51, name, 12, INK, MONO, "middle")

# 계층 2: 플러그어블 스토리지 인터페이스 (focal ACC)
# 좌측: S3 API (원서 p.10: get/put, 객체는 불변)
S3_W = 414
d.box(24, L2_Y, S3_W, L2_H, PAPER2, ACC, 1.3)
d.chip(106, L2_Y + 22, "S3 호환 API", ACC, 12)
d.t(180, L2_Y + 26, "오브젝트 스토어 표준 프로토콜", 13, INK, KR, "start", 600)
d.t(38, L2_Y + 52, "get · put 기반 불변 객체 인터페이스", 12, INK, KR, "start")
d.t(38, L2_Y + 72, "MinIO부터 Cloudflare R2까지 단일 클라이언트 접근", 12, MUTED, KR, "start")

# 우측: POSIX / VFS 인터페이스 (OK)
VFS_X = 462
VFS_W = 414
d.box(VFS_X, L2_Y, VFS_W, L2_H, PAPER2, OK, 1.1)
d.chip(VFS_X + 110, L2_Y + 22, "POSIX 계층", OK, 12)
d.t(VFS_X + 190, L2_Y + 26, "파일시스템 시스템 콜 호환", 13, INK, KR, "start", 600)
d.t(VFS_X + 24, L2_Y + 52, "FUSE(s3fs) 마운트 및 NFS 프로토콜 추상화", 12, INK, KR, "start")
d.t(VFS_X + 24, L2_Y + 72, "open() · read() · write()", 12, MUTED, MONO, "start")

# 계층 1 -> 계층 2 연결 화살표
d.arrow([(230, L1_Y + L1_H), (230, L2_Y - 4)], ACC, "acc", 1.4)
d.arrow([(670, L1_Y + L1_H), (670, L2_Y - 4)], OK, "ok", 1.4)

# 계층 3: 스토리지 구현체 풀
# 좌측: S3 호환 구현체들 (WARN)
d.box(24, L3_Y, S3_W, L3_H, PAPER2, WARN, 0.9)
d.chip(106, L3_Y + 20, "오브젝트 스토어 풀", WARN, 12)
d.t(190, L3_Y + 24, "S3 API 호환 구현체", 12, INK, KR, "start", 600)

s3_impls = [
    ("AWS S3", 36, 88),
    ("MinIO", 132, 84),
    ("Cloudflare R2", 224, 102),
    ("Ceph / B2", 334, 92),
]
for name, ix, iw in s3_impls:
    d.box(ix, L3_Y + 36, iw, 24, PAPER, WARN, 0.6)
    d.t(ix + iw / 2, L3_Y + 52, name, 12, INK, MONO, "middle")

# 우측: DFS 구현체들 (OK)
d.box(VFS_X, L3_Y, VFS_W, L3_H, PAPER2, OK, 0.9)
d.chip(VFS_X + 96, L3_Y + 20, "분산 파일시스템", OK, 12)
d.t(VFS_X + 176, L3_Y + 24, "분산 파일시스템 구현체", 12, INK, KR, "start", 600)

dfs_impls = [
    ("Apache HDFS", VFS_X + 12, 98),
    ("JuiceFS", VFS_X + 118, 86),
    ("Amazon EFS", VFS_X + 212, 96),
    ("Archil", VFS_X + 316, 86),
]
for name, ix, iw in dfs_impls:
    d.box(ix, L3_Y + 36, iw, 24, PAPER, OK, 0.6)
    d.t(ix + iw / 2, L3_Y + 52, name, 12, INK, MONO, "middle")

# 계층 2 -> 계층 3 연결 화살표
d.arrow([(230, L2_Y + L2_H), (230, L3_Y - 4)], WARN, "warn", 1.4)
d.arrow([(670, L2_Y + L2_H), (670, L3_Y - 4)], OK, "ok", 1.4)

# 하단 아키텍처 대조 배너
d.tone(24, ARCH_Y, W - 48, ARCH_H, SOFT, 4, "12", 0.9)
d.t(W / 2, ARCH_Y + 22, "클러스터 구조 대조: shared-nothing(HDFS 로컬 디스크 풀) 대 shared-disk(NAS · SAN)", 12, INK, KR, "middle")

d.legend(LEG_Y, [
    ("표준 인터페이스 (focal)", ACC),
    ("배치 프레임워크", INFO),
    ("오브젝트 스토어 풀", WARN),
    ("분산 파일시스템", OK),
])

d.save("11-02.pluggable-storage-interface.svg")
