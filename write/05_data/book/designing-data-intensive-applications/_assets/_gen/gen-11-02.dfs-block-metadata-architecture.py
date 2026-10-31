# 11-02 §1 — 분산 파일시스템의 메타데이터와 블록 배치 구조
# 사실 출처: 11-02 본문 §1(L29~L37), 원서 DDIA 2nd Edition Ch. 11 p.8 (900MB 파일, 128MB 7개 + 4MB 1개 블록, 블록 크기 비교, data nodes)·p.9 (NameNode 메타데이터)
# 원서는 파일 이름을 주지 않는다. DataNode 넷과 블록 배치는 "블록이 여러 머신에 퍼진다"(p.8)를 보이는 예시 배치다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 900
BANNER_Y = 104
BANNER_H = 34

# 파일 블록 영역
FILE_Y = 150
FILE_H = 68

# 컴포넌트 영역
COMP_Y = 230
COMP_H = 92

# DataNode 풀 영역
DN_Y = 362
DN_H = 78

LEG_Y = 462
H = LEG_Y + 52

d = D(W, H, "11-02 · §1 DFS ARCHITECTURE", "분산 파일시스템 메타데이터와 블록 배치 구조",
      "클라이언트가 NameNode에서 메타데이터를 조회하고 DataNode와 직접 통신하는 구조",
      "900MB 파일 블록 분할 · NameNode 메모리 메타데이터 · DataNode 직접 데이터 스트리밍")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "원서 900MB 파일 예시: 128MB 블록 7개와 4MB 부분 블록 1개 분할 배치", 12, INK, KR, "middle", 600)

# 1. 파일 블록 분할 박스
d.box(24, FILE_Y, W - 48, FILE_H, PAPER2, RULE, 0.9)
d.chip(96, FILE_Y + 20, "900MB 파일", INFO, 12)
d.t(196, FILE_Y + 24, "대용량 파일 블록 분할 (HDFS 기준)", 12, INK, KR, "start", 600)
d.t(W - 36, FILE_Y + 24, "ext4 4KB · JuiceFS 4MB · HDFS 128MB", 12, SOFT, MONO, "end")

# 블록 8개 가로 배열 (B0~B6: 128MB, B7: 4MB)
BX0 = 36
BW_FULL = 96
BW_LAST = 74
BGAP = 8
BY = FILE_Y + 36

for i in range(8):
    bw = BW_LAST if i == 7 else BW_FULL
    bx = BX0 + i * (BW_FULL + BGAP)
    is_partial = (i == 7)
    bc = MUTED if is_partial else INFO
    d.box(bx, BY, bw, 22, PAPER, bc, 0.8)
    label = f"B{i} (4MB)" if is_partial else f"B{i} (128MB)"
    d.t(bx + bw / 2, BY + 15, label, 12, bc, MONO, "middle")

# 2. Client와 NameNode
# Client
CL_X = 24
CL_W = 260
d.box(CL_X, COMP_Y, CL_W, COMP_H, PAPER2, ACC, 1.2)
d.chip(CL_X + 64, COMP_Y + 22, "CLIENT", ACC, 12)
d.t(CL_X + 136, COMP_Y + 26, "배치 워커 태스크", 13, INK, KR, "start", 600)
d.t(CL_X + 16, COMP_Y + 52, "MapReduce / Spark 워커", 12, INK, KR, "start")
d.t(CL_X + 16, COMP_Y + 72, "블록 메타데이터 조회 및 직접 읽기", 12, MUTED, KR, "start")

# NameNode
NN_X = 540
NN_W = 336
d.box(NN_X, COMP_Y, NN_W, COMP_H, PAPER2, INFO, 1.2)
d.chip(NN_X + 64, COMP_Y + 22, "NAMENODE", INFO, 12)
d.t(NN_X + 140, COMP_Y + 26, "메타데이터 서비스", 13, INK, KR, "start", 600)
d.t(NN_X + 16, COMP_Y + 52, "메모리 상주 파일 네임스페이스", 12, INK, KR, "start")
d.t(NN_X + 16, COMP_Y + 72, "블록-DataNode 위치 매핑 테이블 유지", 12, MUTED, KR, "start")

# Client <-> NameNode 인터랙션 화살표
# 1) Client -> NameNode: 블록 위치 질의
d.arrow([(CL_X + CL_W, COMP_Y + 34), (NN_X, COMP_Y + 34)], INFO, "info", 1.4)
d.t((CL_X + CL_W + NN_X) / 2, COMP_Y + 26, "1. 블록 위치 질의", 12, INFO, KR, "middle")

# 2) NameNode -> Client: 위치 매핑 응답
d.arrow([(NN_X, COMP_Y + 66), (CL_X + CL_W, COMP_Y + 66)], OK, "ok", 1.4)
d.t((CL_X + CL_W + NN_X) / 2, COMP_Y + 58, "2. DataNode 목록 응답", 12, OK, KR, "middle")

# 3. DataNode 풀 (하단 4개 노드)
DN_W = 200
DN_GAP = 16
DN_X0 = 24

dns = [
    ("DataNode 1", "B0, B1 저장", "로컬 OS 캐시 + 디스크"),
    ("DataNode 2", "B2, B3 저장", "로컬 OS 캐시 + 디스크"),
    ("DataNode 3", "B4, B5 저장", "로컬 OS 캐시 + 디스크"),
    ("DataNode 4", "B6, B7 저장", "로컬 OS 캐시 + 디스크"),
]

for idx, (title, blocks, desc) in enumerate(dns):
    dx = DN_X0 + idx * (DN_W + DN_GAP)
    d.box(dx, DN_Y, DN_W, DN_H, PAPER2, WARN, 0.9)
    d.chip(dx + 52, DN_Y + 20, f"NODE {idx+1}", WARN, 12)
    d.t(dx + 120, DN_Y + 24, title, 12, INK, KR, "start", 600)
    d.t(dx + 14, DN_Y + 48, blocks, 12, INK, KR, "start")
    d.t(dx + 14, DN_Y + 66, desc, 12, MUTED, KR, "start")

# Client -> DataNode 직접 데이터 스트리밍 화살표 (focal)
d.arrow([(CL_X + 60, COMP_Y + COMP_H), (CL_X + 60, DN_Y - 18), (DN_X0 + 100, DN_Y - 18), (DN_X0 + 100, DN_Y - 6)], ACC, "acc", 1.6)
d.t(CL_X + 175, DN_Y - 10, "3. 직접 데이터 I/O (네트워크 스트리밍)", 12, ACC, KR, "start", 600)

d.legend(LEG_Y, [
    ("직접 데이터 I/O (focal)", ACC),
    ("블록 분할·메타 질의", INFO),
    ("위치 응답", OK),
    ("DataNode 저장소", WARN),
])

d.save("11-02.dfs-block-metadata-architecture.svg")
