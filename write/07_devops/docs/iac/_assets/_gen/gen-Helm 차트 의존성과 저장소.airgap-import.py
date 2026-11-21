# 타입 스펙: type-architecture
# 3절 폐쇄망 환경 차트와 이미지 반입 경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 468

d = D(W, H, "HELM · AIRGAP IMPORT",
      "폐쇄망 환경 차트 및 컨테이너 이미지 반입 경로",
      "외부망에서 tgz 차트와 이미지 목록을 추출해 망 분리 경계를 넘어 사내 레지스트리에 적재하고 설치하는 아키텍처",
      lead="외부망 아카이브 추출(좌) → 망 분리 경계 통과 → 사내 레지스트리 적재 및 클러스터 설치(우)")

# ── 존 정의 (좌: 외부망 / 우: 폐쇄망) ──────────────────────────────────
ZONE_Y = 94
ZONE_H = 304
ZONE_W = 410

# 외부망 존 (x: 24 ~ 434)
d.o.append(f'<rect x="24" y="{ZONE_Y}" width="{ZONE_W}" height="{ZONE_H}" rx="8" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>')
d.o.append(f'<rect x="40" y="{ZONE_Y + 4}" width="156" height="16" rx="2" fill="{PAPER}"/>')
d.t(118, ZONE_Y + 16, "외부망 (인터넷 가능 환경)", 11, SOFT, KR, "middle")

# 폐쇄망 존 (x: 526 ~ 936)
d.o.append(f'<rect x="526" y="{ZONE_Y}" width="{ZONE_W}" height="{ZONE_H}" rx="8" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>')
d.o.append(f'<rect x="542" y="{ZONE_Y + 4}" width="156" height="16" rx="2" fill="{PAPER}"/>')
d.t(620, ZONE_Y + 16, "폐쇄망 (사내 격리 환경)", 11, SOFT, KR, "middle")

# 망 분리 경계선 (x: 480, 통로 x: 434 ~ 526)
d.line(480, ZONE_Y, 480, ZONE_Y + ZONE_H, SOFT, 1.0, "4 4")
d.o.append(f'<rect x="444" y="234" width="72" height="20" rx="4" fill="{PAPER}" stroke="{SOFT}" stroke-width="0.8"/>')
d.t(480, 248, "망 분리 경계", 11, SOFT, KR, "middle")


# ── 외부망 노드 ──────────────────────────────────────────────────────────
# 1. 공용 저장소 및 레지스트리
BOX1_X, BOX1_Y, BOX1_W, BOX1_H = 38, 130, 168, 120
d.tone(BOX1_X, BOX1_Y, BOX1_W, BOX1_H, INFO, 6, "12", 1.0)
d.t(BOX1_X + BOX1_W // 2, BOX1_Y + 22, "공용 원격 저장소", 13, INFO, KR, "middle", 600)
d.t(BOX1_X + BOX1_W // 2, BOX1_Y + 40, "인터넷 공개 레지스트리", 11, MUTED, KR, "middle")
d.line(BOX1_X + 12, BOX1_Y + 50, BOX1_X + BOX1_W - 12, BOX1_Y + 50, RULE, 0.6)
d.t(BOX1_X + BOX1_W // 2, BOX1_Y + 70, "podinfo-6.7.1.tgz", 11, INK, MONO, "middle")
d.t(BOX1_X + BOX1_W // 2, BOX1_Y + 90, "ghcr.io/stefanprodan", 11, MUTED, MONO, "middle")
d.t(BOX1_X + BOX1_W // 2, BOX1_Y + 108, "curlimages/curl:7.69.0", 10, MUTED, MONO, "middle")

# 2. 외부 작업 호스트
BOX2_X, BOX2_Y, BOX2_W, BOX2_H = 248, 130, 172, 252
d.box(BOX2_X, BOX2_Y, BOX2_W, BOX2_H, PAPER, RULE, 1.0)
d.t(BOX2_X + BOX2_W // 2, BOX2_Y + 22, "외부 작업 호스트", 13, INK, KR, "middle", 600)
d.t(BOX2_X + BOX2_W // 2, BOX2_Y + 40, "Helm · Docker CLI", 11, MUTED, MONO, "middle")

# 외부 호스트 내부 단계 카드
# 단계 1: 이미지 목록 추출
C1_Y = BOX2_Y + 52
d.box(BOX2_X + 10, C1_Y, 152, 56, PAPER2, RULE, 0.8)
d.t(BOX2_X + 86, C1_Y + 18, "1. 이미지 목록 추출", 11, INK, KR, "middle", 600)
d.t(BOX2_X + 86, C1_Y + 34, "helm template", 11, INFO, MONO, "middle", 600)
d.t(BOX2_X + 86, C1_Y + 48, "grep · sed · sort", 10, MUTED, MONO, "middle")

# 단계 2: 이미지 아카이브 묶기
C2_Y = BOX2_Y + 116
d.box(BOX2_X + 10, C2_Y, 152, 56, PAPER2, RULE, 0.8)
d.t(BOX2_X + 86, C2_Y + 18, "2. 이미지 아카이브", 11, INK, KR, "middle", 600)
d.t(BOX2_X + 86, C2_Y + 34, "docker save", 11, INFO, MONO, "middle", 600)
d.t(BOX2_X + 86, C2_Y + 48, "이미지 tar 아카이브", 11, SOFT, KR, "middle")

# 반입 준비 상태
C3_Y = BOX2_Y + 182
d.box(BOX2_X + 10, C3_Y, 152, 54, PAPER2, ACC, 0.8)
d.t(BOX2_X + 86, C3_Y + 20, "반입 패키지 준비", 11, ACC, KR, "middle", 600)
d.t(BOX2_X + 86, C3_Y + 40, "차트 tgz + 이미지 tar", 11, INK, KR, "middle")


# ── 화살표: 공용 저장소 -> 외부 작업 호스트 (다운로드) ────────────────────
d.arrow([(BOX1_X + BOX1_W + 2, BOX1_Y + 42), (BOX2_X - 4, BOX1_Y + 42)], INFO, "info", 1.2)
d.t((BOX1_X + BOX1_W + BOX2_X) // 2, BOX1_Y + 34, "다운로드", 11, INFO, KR, "middle")


# ── 화살표: 외부 호스트 -> 내부 호스트 (망 분리 반입) ───────────────────
# 라벨과 선이 겹치지 않도록 분할 렌더링
BOX3_X, BOX3_Y, BOX3_W, BOX3_H = 534, 130, 160, 252
d.line(BOX2_X + BOX2_W + 2, C3_Y + 27, 444, C3_Y + 27, ACC, 1.4)
d.arrow([(516, C3_Y + 27), (BOX3_X - 4, C3_Y + 27)], ACC, "acc", 1.4)
d.o.append(f'<rect x="444" y="{C3_Y + 16}" width="72" height="22" rx="3" fill="{PAPER}" stroke="{ACC}" stroke-width="0.8"/>')
d.t(480, C3_Y + 31, "3. 보안 반입", 11, ACC, KR, "middle", 600)


# ── 폐쇄망 노드 ──────────────────────────────────────────────────────────
# 3. 내부 작업 호스트
d.box(BOX3_X, BOX3_Y, BOX3_W, BOX3_H, PAPER, RULE, 1.0)
d.t(BOX3_X + BOX3_W // 2, BOX3_Y + 22, "내부 작업 호스트", 13, INK, KR, "middle", 600)
d.t(BOX3_X + BOX3_W // 2, BOX3_Y + 40, "폐쇄망 관리 환경", 11, MUTED, KR, "middle")

# 내부 호스트 단계 카드
I1_Y = BOX3_Y + 52
d.box(BOX3_X + 8, I1_Y, 144, 56, PAPER2, RULE, 0.8)
d.t(BOX3_X + 80, I1_Y + 18, "4. 사내 적재", 11, INK, KR, "middle", 600)
d.t(BOX3_X + 80, I1_Y + 34, "docker load", 11, INFO, MONO, "middle", 600)
d.t(BOX3_X + 80, I1_Y + 48, "사내 레지스트리에 등록", 11, SOFT, KR, "middle")

I2_Y = BOX3_Y + 116
d.box(BOX3_X + 8, I2_Y, 144, 58, PAPER2, RULE, 0.8)
d.t(BOX3_X + 80, I2_Y + 18, "5. 로컬 차트 배포", 11, INK, KR, "middle", 600)
d.t(BOX3_X + 80, I2_Y + 34, "helm install", 11, OK, MONO, "middle", 600)
d.t(BOX3_X + 80, I2_Y + 49, "./podinfo-6.7.1.tgz", 10, MUTED, MONO, "middle")

I3_Y = BOX3_Y + 182
d.box(BOX3_X + 8, I3_Y, 144, 54, PAPER2, RULE, 0.8)
d.t(BOX3_X + 80, I3_Y + 20, "배포 상태 검증", 11, INK, KR, "middle", 600)
d.t(BOX3_X + 80, I3_Y + 38, "helm list -n hl-dep", 10, MUTED, MONO, "middle")

# 4. 사내 프라이빗 레지스트리 (FOCAL!)
BOX4_X, BOX4_Y, BOX4_W, BOX4_H = 754, 130, 172, 98
d.tone(BOX4_X, BOX4_Y, BOX4_W, BOX4_H, ACC, 6, "16", 1.4)
d.t(BOX4_X + BOX4_W // 2, BOX4_Y + 22, "사내 레지스트리", 13, ACC, KR, "middle", 600)
d.t(BOX4_X + BOX4_W // 2, BOX4_Y + 40, "registry.example.com", 11, INK, MONO, "middle")
d.line(BOX4_X + 12, BOX4_Y + 50, BOX4_X + BOX4_W - 12, BOX4_Y + 50, ACC, 0.6)
d.t(BOX4_X + BOX4_W // 2, BOX4_Y + 68, "사내 전용 이미지 보관", 11, MUTED, KR, "middle")
d.t(BOX4_X + BOX4_W // 2, BOX4_Y + 86, "podinfo:6.7.1 이미지", 11, ACC, MONO, "middle")

# 5. 쿠버네티스 클러스터
BOX5_X, BOX5_Y, BOX5_W, BOX5_H = 754, 262, 172, 120
d.tone(BOX5_X, BOX5_Y, BOX5_W, BOX5_H, OK, 6, "12", 1.1)
d.t(BOX5_X + BOX5_W // 2, BOX5_Y + 22, "쿠버네티스 클러스터", 13, OK, KR, "middle", 600)
d.t(BOX5_X + BOX5_W // 2, BOX5_Y + 40, "hl-dep 네임스페이스", 11, MUTED, KR, "middle")
d.line(BOX5_X + 12, BOX5_Y + 50, BOX5_X + BOX5_W - 12, BOX5_Y + 50, RULE, 0.6)
d.t(BOX5_X + BOX5_W // 2, BOX5_Y + 68, "hl-dep-podinfo 릴리스", 11, INK, MONO, "middle")
d.t(BOX5_X + BOX5_W // 2, BOX5_Y + 88, "STATUS: deployed", 11, OK, MONO, "middle", 600)
d.t(BOX5_X + BOX5_W // 2, BOX5_Y + 106, "이미지 없으면 ImagePullBackOff", 11, MUTED, KR, "middle")


# ── 화살표: 내부 호스트 -> 사내 레지스트리 / 클러스터 ────────────────────
MID_GAP_X = (BOX3_X + BOX3_W + BOX4_X) // 2

# 내부 호스트 -> 사내 레지스트리 (도커 푸시)
d.arrow([(BOX3_X + BOX3_W + 2, I1_Y + 28), (BOX4_X - 4, I1_Y + 28)], INFO, "info", 1.2)
d.t(MID_GAP_X, I1_Y + 18, "등록", 11, INFO, KR, "middle")

# 내부 호스트 -> 클러스터 (helm install 매니페스트)
d.arrow([(BOX3_X + BOX3_W + 2, I2_Y + 28), (BOX5_X - 4, I2_Y + 28)], OK, "ok", 1.2)
d.t(MID_GAP_X, I2_Y + 18, "매니페스트", 11, OK, KR, "middle")

# 사내 레지스트리 -> 클러스터 (6. 이미지 풀 수직 화살표 - 34px 길이)
d.arrow([(BOX4_X + BOX4_W // 2, BOX4_Y + BOX4_H + 2), (BOX5_X + BOX5_W // 2, BOX5_Y - 4)], OK, "ok", 1.2)
d.o.append(f'<rect x="{BOX4_X + BOX4_W // 2 - 44}" y="240" width="88" height="16" rx="2" fill="{PAPER}"/>')
d.t(BOX4_X + BOX4_W // 2, 252, "6. 이미지 풀", 11, OK, KR, "middle")


# ── 범례 ──────────────────────────────────────────────────────────────
d.legend(420, [
    ("외부 환경", INFO),
    ("사내 레지스트리 (핵심)", ACC),
    ("정상 배포 (클러스터)", OK),
    ("망 분리 경계", SOFT)
])

d.save("Helm 차트 의존성과 저장소.airgap-import.svg")
print("ok Helm 차트 의존성과 저장소.airgap-import.svg")
