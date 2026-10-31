# 11-01 §5 — 단일 머신 Unix 구성요소(파일시스템·스케줄러·프로세스)와 분산 배치 시스템(스토리지·오케스트레이터·프레임워크)의 1:1 대응.
# 사실 출처: 11-01 본문 §5(L102~L110), DDIA 2판 Ch 11 p.7~9 ("Batch Processing in Distributed Systems"). 칸 라벨은 본문 및 원서 대목.
# 타입 스펙: type-layers
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
LY = 156
LH = 72
GAP_L = 12
BOT_Y = LY + 3 * LH + 2 * GAP_L + 16
BOT_H = 40
LEG = BOT_Y + BOT_H + 20
H = LEG + 52

d = D(W, H, "11-01 · §5 DISTRIBUTED OS ANALOGY", "단일 머신 Unix와 분산 배치 처리 시스템 대응",
      "단일 머신의 파일시스템, 커널 스케줄러, 파이프 프로세스가 분산 배치의 스토리지, 잡 오케스트레이터, 처리 프레임워크로 대응되는 구조를 층별로 조망한다.",
      "운영체제 유추 · 파일시스템 vs 분산 스토리지 · 커널 vs 오케스트레이터 · 프로세스 vs 분산 엔진 · 컴퓨트-스토리지 분리")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "분산 운영체제 유추: 분산 배치 프레임워크는 단일 머신 OS의 스토리지·스케줄러·프로세스 역할을 대규모로 확장한 것", 12, INK, KR, "middle", 600)

layers = [
    ("실행 계층",
     "파이프로 연결된 프로세스", "stdin · stdout 데이터 파이프 (cat | awk | sort)", INFO,
     "분산 처리 프레임워크", "선구자 MapReduce → DAG 기반 Spark · Flink", OK),
    ("제어 계층",
     "커널 프로세스 스케줄러", "CPU 자원 할당 · 프로세스 실행 시점 관리", INFO,
     "잡 오케스트레이터", "Hadoop Oozie · Azkaban → Airflow · Dagster", OK),
    ("저장 계층",
     "로컬 파일시스템 (VFS)", "블록 디바이스 드라이버 · ext4 · XFS", INFO,
     "분산 파일시스템 · 오브젝트 스토리지", "초기 HDFS → 클라우드 S3 · GCS · Azure Blob", OK),
]

for idx, (layer_name, u_title, u_desc, u_c, d_title, d_desc, d_c) in enumerate(layers):
    y = LY + idx * (LH + GAP_L)

    # 좌측: 단일 머신 Unix 상자
    d.box(28, y, 368, LH, PAPER2, u_c, 1.0)
    d.t(44, y + 26, u_title, 13, INK, KR, "start", 600)
    d.t(44, y + 50, u_desc, 11, MUTED, KR, "start")

    # 중앙: 계층 태그 및 양방향 대응 표시
    d.chip(440, y + 26, layer_name, MUTED, 11, 4)
    d.arrow([(412, y + 46), (468, y + 46)], MUTED, "ar", 1.2)
    d.arrow([(468, y + 46), (412, y + 46)], MUTED, "ar", 1.2)

    # 우측: 분산 배치 시스템 상자
    d.box(484, y, 368, LH, PAPER2, d_c, 1.0)
    d.t(500, y + 26, d_title, 13, INK, KR, "start", 600)
    d.t(500, y + 50, d_desc, 11, MUTED, KR, "start")

# 하단 아키텍처 진화 배너
d.tone(28, BOT_Y, W - 56, BOT_H, ACC, 4, "14", 1.0)
d.t(W / 2, BOT_Y + 24, "핵심 진화: HDFS 데이터 지역성(컴퓨트·스토리지 동거) → 오브젝트 스토리지 컴퓨트·스토리지 분리(독립 확장 및 비용 최적화)", 11.5, INK, KR, "middle", 600)

d.legend(LEG, [
    ("단일 머신 Unix 요소", INFO),
    ("분산 배치 시스템 대응", OK),
    ("스토리지 분리 진화", ACC),
])

d.save("11-01.distributed-os-analogy.svg")
