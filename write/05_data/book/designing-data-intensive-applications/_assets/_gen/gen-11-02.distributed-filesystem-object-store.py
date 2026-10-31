# 11-02 §4 — 분산 파일시스템과 오브젝트 스토어의 아키텍처 비교
# 사실 출처: 11-02 본문 §1 L33(블록 크기), §4(L70~L83 비교표), §5 L92(S3 호환 저장소). 원서 Ch.11 p.8(4 MB blocks), p.10~11(co-location, 분리, 비원자 rename, prefix).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 900
BANNER_Y = 104
BANNER_H = 36

# 패널 영역
PANEL_Y = 156
PANEL_H = 310

BOTTOM_Y = 480
BOTTOM_H = 34

LEG_Y = 530
H = LEG_Y + 52

d = D(W, H, "11-02 · §4 DFS VS OBJECT STORE", "DFS와 오브젝트 스토어 아키텍처 비교",
      "계산-저장 co-location 모델과 계산-저장 분리 모델의 구조적 대조",
      "co-location 로컬리티 · 계산-저장 분리 · 독립 스케일링 · 원자적 연산과 디렉토리 체계")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "아키텍처 대조: 계산-저장 결합형(HDFS) 대 초고속 네트워크 기반 계산-저장 분리형(S3)", 12, INK, KR, "middle", 600)

PW = 414
GAP = 24
X_LEFT = 24
X_RIGHT = 462

# 1. 좌측: DFS (co-location 모델)
d.box(X_LEFT, PANEL_Y, PW, PANEL_H, PAPER2, RULE, 0.9)
d.chip(X_LEFT + 70, PANEL_Y + 22, "DFS 모델", INFO, 12)
d.t(X_LEFT + 150, PANEL_Y + 26, "계산-저장 결합 (co-location)", 13, INK, KR, "start", 600)

# 노드 2개 (결합형 머신)
for n_idx in range(2):
    ny = PANEL_Y + 44 + n_idx * 78
    d.box(X_LEFT + 16, ny, PW - 32, 70, PAPER, INFO, 0.6)
    d.t(X_LEFT + 28, ny + 18, f"클러스터 서버 {n_idx+1}", 11, SOFT, KR, "start")

    # 상단 연산 태스크
    d.box(X_LEFT + 120, ny + 8, 120, 22, PAPER2, INFO, 0.7)
    d.t(X_LEFT + 180, ny + 23, "배치 연산 태스크", 11, INK, KR, "middle")

    # 화살표: 로컬 버스
    d.arrow([(X_LEFT + 248, ny + 19), (X_LEFT + 268, ny + 19)], OK, "ok", 1.2)

    # 하단 로컬 디스크 DataNode
    d.box(X_LEFT + 276, ny + 8, 110, 22, PAPER2, INFO, 0.7)
    d.t(X_LEFT + 331, ny + 23, "DataNode 블록", 11, INK, KR, "middle")

    d.t(X_LEFT + 28, ny + 46, "로컬 I/O: 네트워크 전송 없는 로컬 디스크 읽기", 11, MUTED, KR, "start")

# 하단 DFS 특징 목록
d.box(X_LEFT + 16, PANEL_Y + 208, PW - 32, 90, PAPER, RULE, 0.6)
d.t(X_LEFT + 28, PANEL_Y + 228, "원자적 rename: 메타데이터 변경만으로 원자적 완료", 12, INK, KR, "start")
d.t(X_LEFT + 28, PANEL_Y + 250, "디렉토리 계층: POSIX 호환 계층 구조 네임스페이스", 12, INK, KR, "start")
d.t(X_LEFT + 28, PANEL_Y + 272, "확장성 한계: 스토리지와 연산 자원의 동시 증설 제약", 12, MUTED, KR, "start")


# 2. 우측: 오브젝트 스토어 (계산-저장 분리 모델, focal)
d.box(X_RIGHT, PANEL_Y, PW, PANEL_H, PAPER2, ACC, 1.3)
d.chip(X_RIGHT + 80, PANEL_Y + 22, "오브젝트 스토어", ACC, 12)
d.t(X_RIGHT + 160, PANEL_Y + 26, "계산-저장 물리 분리 (Decoupled)", 13, INK, KR, "start", 600)

# 상단 컴퓨팅 풀
d.box(X_RIGHT + 16, PANEL_Y + 44, PW - 32, 38, PAPER, OK, 0.8)
d.chip(X_RIGHT + 80, PANEL_Y + 63, "컴퓨팅 풀", OK, 11)
d.t(X_RIGHT + 140, PANEL_Y + 67, "Spark / Trino 독립 확장", 12, INK, KR, "start")

# 중앙 네트워크 패브릭
d.tone(X_RIGHT + 16, PANEL_Y + 90, PW - 32, 28, WARN, 4, "18", 1.0)
d.t(X_RIGHT + PW / 2, PANEL_Y + 108, "고속 데이터센터 네트워크 패브릭 (25Gbps+)", 11, WARN, KR, "middle", 600)

# 하단 스토리지 풀
d.box(X_RIGHT + 16, PANEL_Y + 126, PW - 32, 38, PAPER, ACC, 0.8)
d.chip(X_RIGHT + 80, PANEL_Y + 145, "스토리지 풀", ACC, 11)
d.t(X_RIGHT + 140, PANEL_Y + 149, "S3 오브젝트 독립 확장", 12, INK, KR, "start")

# 하단 오브젝트 스토어 특징 목록
d.box(X_RIGHT + 16, PANEL_Y + 172, PW - 32, 126, PAPER, RULE, 0.6)
d.t(X_RIGHT + 28, PANEL_Y + 194, "비원자 rename: 새 키 복사 후 기존 객체 삭제 2단계", 12, INK, KR, "start")
d.t(X_RIGHT + 28, PANEL_Y + 216, "평면 네임스페이스: 디렉토리 부재 · 접두사 URL 체계", 12, INK, KR, "start")
d.t(X_RIGHT + 28, PANEL_Y + 238, "독립적 탄력 스케일: 연산 노드와 스토리지 개별 증설", 12, ACC, KR, "start", 600)
d.t(X_RIGHT + 28, PANEL_Y + 260, "S3 API: MinIO · R2 · B2 가 호환", 12, INK, KR, "start")
d.t(X_RIGHT + 28, PANEL_Y + 282, "블록 크기: 4MB (JuiceFS · S3 내부)", 12, MUTED, KR, "start")

# 하단 블록 크기 및 스펙 대조 바
d.tone(24, BOTTOM_Y, W - 48, BOTTOM_H, SOFT, 4, "12", 0.9)
d.t(W / 2, BOTTOM_Y + 22, "핵심 수치 대조: HDFS 기본 블록 128MB 대 S3 내부 블록 4MB · co-location 대 물리 분리", 12, INK, KR, "middle")

d.legend(LEG_Y, [
    ("계산-저장 분리 (focal)", ACC),
    ("DFS co-location", INFO),
    ("독립 컴퓨팅 풀", OK),
    ("고속 네트워크 패브릭", WARN),
])

d.save("11-02.distributed-filesystem-object-store.svg")
