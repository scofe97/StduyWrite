# 타입 스펙: type-flowchart
# 01-03.builder-selection-flow — 환경·보안·언어·Dockerfile 에 따른 빌더 선택 결정 트리
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 960, 520

d = D(W, H, "CONTAINER · 01-03 FLOWCHART",
      "환경과 제약에 따른 빌더 선택 결정 흐름",
      "실행 환경, 보안 정책, 대상 언어, Dockerfile 준비 여부에 따른 6종 빌더 선택 경로",
      lead="질문 분기(Pod 실행 여부 → 특권 허용 → JVM 여부 → Dockerfile 유무)와 최종 선택 도구")

CX = 240
BOX_X = 520
BOX_W = 410
BOX_H = 50

# ── 분기 1: Pod 환경인가? ──
Y1 = 118
d.o.append(f'<path d="M {CX} {Y1 - 22} L {CX + 95} {Y1} L {CX} {Y1 + 22} L {CX - 95} {Y1} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y1 + 4, "실행 환경이 Pod 인가?", 12, INK, KR, "middle")

# 분기 1 아니오 -> Docker
d.arrow([(CX + 95, Y1), (BOX_X - 2, Y1)], MUTED, "ar", 1.2)
d.t((CX + 95 + BOX_X) // 2, Y1 - 7, "아니오 (VM)", 11, MUTED, KR, "middle")
d.tone(BOX_X, Y1 - BOX_H // 2, BOX_W, BOX_H, INFO, 6, "12", 1.2)
d.t(BOX_X + 16, Y1 - 6, "Docker (docker build)", 13, INFO, KR, "start", 600)
d.t(BOX_X + 16, Y1 + 14, "VM 호스트 데몬 직접 활용 · Dockerfile 기반", 11, MUTED, KR, "start")

# 분기 1 예 -> 아래로
d.arrow([(CX, Y1 + 22), (CX, 190 - 22)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y1 + 22 + 190 - 22) // 2 + 4, "예", 11, MUTED, KR, "start")

# ── 분기 2: 특권 허용? ──
Y2 = 190
d.o.append(f'<path d="M {CX} {Y2 - 22} L {CX + 95} {Y2} L {CX} {Y2 + 22} L {CX - 95} {Y2} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y2 + 4, "특권(privileged) 허용?", 12, INK, KR, "middle")

# 분기 2 예 -> BuildKit 데몬 / DinD
d.arrow([(CX + 95, Y2), (BOX_X - 2, Y2)], MUTED, "ar", 1.2)
d.t((CX + 95 + BOX_X) // 2, Y2 - 7, "예", 11, MUTED, KR, "middle")
d.tone(BOX_X, Y2 - BOX_H // 2, BOX_W, BOX_H, WARN, 6, "12", 1.2)
d.t(BOX_X + 16, Y2 - 6, "BuildKit 데몬 또는 Docker DinD", 13, WARN, KR, "start", 600)
d.t(BOX_X + 16, Y2 + 14, "호스트 소켓 마운트 또는 특권 컨테이너 전제", 11, MUTED, KR, "start")

# 분기 2 아니오 -> 아래로
d.arrow([(CX, Y2 + 22), (CX, 262 - 22)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y2 + 22 + 262 - 22) // 2 + 4, "아니오", 11, MUTED, KR, "start")

# ── 분기 3: JVM 애플리케이션인가? ──
Y3 = 262
d.o.append(f'<path d="M {CX} {Y3 - 22} L {CX + 95} {Y3} L {CX} {Y3 + 22} L {CX - 95} {Y3} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y3 + 4, "JVM 애플리케이션인가?", 12, INK, KR, "middle")

# 분기 3 예 -> Jib
d.arrow([(CX + 95, Y3), (BOX_X - 2, Y3)], MUTED, "ar", 1.2)
d.t((CX + 95 + BOX_X) // 2, Y3 - 7, "예", 11, MUTED, KR, "middle")
d.tone(BOX_X, Y3 - BOX_H // 2, BOX_W, BOX_H, OK, 6, "12", 1.2)
d.t(BOX_X + 16, Y3 - 6, "Jib (Maven · Gradle 플러그인)", 13, OK, KR, "start", 600)
d.t(BOX_X + 16, Y3 + 14, "Dockerfile 불필요 · Restricted Pod 에서도 동작", 11, MUTED, KR, "start")

# 분기 3 아니오 -> 아래로
d.arrow([(CX, Y3 + 22), (CX, 334 - 22)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y3 + 22 + 334 - 22) // 2 + 4, "아니오", 11, MUTED, KR, "start")

# ── 분기 4: Dockerfile 준비 여부 ──
Y4 = 334
d.o.append(f'<path d="M {CX} {Y4 - 22} L {CX + 95} {Y4} L {CX} {Y4 + 22} L {CX - 95} {Y4} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y4 + 4, "Dockerfile 있는가?", 12, INK, KR, "middle")

# 분기 4 예 -> BuildKit rootless / Buildah (Focal)
d.arrow([(CX + 95, Y4), (BOX_X - 2, Y4)], ACC, "acc", 1.4)
d.t((CX + 95 + BOX_X) // 2, Y4 - 7, "예", 11, ACC, KR, "middle", 600)
d.tone(BOX_X, Y4 - BOX_H // 2, BOX_W, BOX_H, ACC, 6, "16", 1.4)
d.t(BOX_X + 16, Y4 - 6, "BuildKit rootless 또는 Buildah", 13, ACC, KR, "start", 600)
d.t(BOX_X + 16, Y4 + 14, "빌드 전용 네임스페이스 · 보안 프로필 완화 필요", 11, MUTED, KR, "start")

# 분기 4 아니오 -> 직교 꺾임 화살표로 Buildpacks 박스로 이동
Y5 = 406
d.arrow([(CX, Y4 + 22), (CX, Y5), (BOX_X - 2, Y5)], MUTED, "ar", 1.2)
d.t(CX + 14, Y4 + 32, "아니오", 11, MUTED, KR, "start")
d.tone(BOX_X, Y5 - BOX_H // 2, BOX_W, BOX_H, INFO, 6, "12", 1.2)
d.t(BOX_X + 16, Y5 - 6, "Buildpacks (pack · kpack)", 13, INFO, KR, "start", 600)
d.t(BOX_X + 16, Y5 + 14, "소스 감지 · Pod 에서는 kpack (Restricted 조건)", 11, MUTED, KR, "start")

# 범례
LEG_Y = 472
d.legend(LEG_Y, [
    ("privileged 없음 · 완화 필요", ACC),
    ("언어 특화 (Jib)", OK),
    ("데몬·다언어 감지", INFO),
    ("특권 격리 완화", WARN),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.builder-selection-flow.svg")
d.save(out_path)
print("ok gen-01-03.builder-selection-flow")
