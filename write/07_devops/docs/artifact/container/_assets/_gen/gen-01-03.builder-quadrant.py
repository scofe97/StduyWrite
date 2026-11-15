# 타입 스펙: type-quadrant
# 01-03.builder-quadrant — 데몬 유무와 rootless 지원 사분면
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 520

d = D(W, H, "CONTAINER · 01-03 QUADRANT",
      "데몬 의존성과 rootless 지원 사분면",
      "데몬 유무와 rootless 지원 여부에 따른 빌더 배치와 Dockerfile 필요 구분",
      lead="x축 데몬 의존성과 y축 rootless 지원에 따른 6종 빌더 위치")

# 사분면 중심 및 축 설정
CX, CY = 480, 275
X_MIN, X_MAX = 80, 890
Y_MIN, Y_MAX = 100, 440

# 배경 톤 (Focal 사분면 강조: 우상단 rootless + daemonless)
d.box(CX + 10, Y_MIN, X_MAX - CX - 10, CY - Y_MIN - 10, fill=PAPER2, stroke=RULE, sw=0.8, r=8)
d.t(CX + 24, Y_MIN + 22, "표준 rootless 빌더 영역", 12, ACC, KR, "start", 600)

# 축 라인 (중심에서 사방으로 뻗는 직교 화살표)
d.arrow([(CX, CY), (X_MAX, CY)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (X_MIN, CY)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (CX, Y_MIN)], MUTED, "ar", 1.2)
d.arrow([(CX, CY), (CX, Y_MAX)], MUTED, "ar", 1.2)

# 축 단부 라벨 (Jobs-minimal 9px MONO uppercase)
d.t(X_MAX + 12, CY + 4, "DAEMONLESS", 9, INK, MONO, "start")
d.t(X_MIN - 12, CY + 4, "DAEMON", 9, INK, MONO, "end")
d.t(CX, Y_MIN - 14, "ROOTLESS", 9, INK, MONO, "middle")
d.t(CX, Y_MAX + 22, "ROOT REQUIRED", 9, INK, MONO, "middle")

# 1. Docker (좌하단: Daemon + Privileged)
DK_X, DK_Y = 250, 360
d.o.append(f'<circle cx="{DK_X}" cy="{DK_Y}" r="7" fill="{INFO}" stroke="{INK}" stroke-width="1.2"/>')
d.t(DK_X, DK_Y - 16, "Docker (docker build)", 13, INK, KR, "middle", 600)
d.t(DK_X, DK_Y + 22, "호스트 데몬 의존 · Dockerfile 기반", 11, MUTED, KR, "middle")

# 2. Kaniko (우하단: Daemonless + Privileged/root in container)
KN_X, KN_Y = 700, 360
d.o.append(f'<circle cx="{KN_X}" cy="{KN_Y}" r="7" fill="{WARN}" stroke="{INK}" stroke-width="1.2"/>')
d.t(KN_X, KN_Y - 16, "Kaniko", 13, WARN, KR, "middle", 600)
d.t(KN_X, KN_Y + 22, "컨테이너 내 root 필수 · 2025 보관", 11, MUTED, KR, "middle")

# 3. BuildKit (좌상단: Daemon(buildkitd) + Rootless)
BK_X, BK_Y = 300, 160
d.o.append(f'<circle cx="{BK_X}" cy="{BK_Y}" r="8" fill="{ACC}" stroke="{INK}" stroke-width="1.4"/>')
d.t(BK_X, BK_Y - 18, "BuildKit", 14, ACC, KR, "middle", 600)
d.t(BK_X, BK_Y + 22, "buildkitd 데몬 · rootless 모드", 11, MUTED, KR, "middle")

# 4. Buildah (우상단: Daemonless + Rootless)
BA_X, BA_Y = 700, 160
d.o.append(f'<circle cx="{BA_X}" cy="{BA_Y}" r="7" fill="{OK}" stroke="{INK}" stroke-width="1.2"/>')
d.t(BA_X, BA_Y - 18, "Buildah", 13, OK, KR, "middle", 600)
d.t(BA_X, BA_Y + 22, "fork-exec · user namespace", 11, MUTED, KR, "middle")

# 5. Jib (우상단: Daemonless + Rootless, Dockerfile 불필요 -> 사각형 마커)
JIB_X, JIB_Y = 590, 225
d.o.append(f'<rect x="{JIB_X - 6}" y="{JIB_Y - 6}" width="12" height="12" rx="2" fill="{OK}" stroke="{INK}" stroke-width="1.2"/>')
d.t(JIB_X, JIB_Y - 16, "Jib", 13, INK, KR, "middle", 600)
d.t(JIB_X, JIB_Y + 22, "JVM 플러그인 · 비특권", 11, MUTED, KR, "middle")

# 6. Buildpacks (우상단: Daemonless + Rootless, Dockerfile 불필요 -> 사각형 마커)
BP_X, BP_Y = 760, 225
d.o.append(f'<rect x="{BP_X - 6}" y="{BP_Y - 6}" width="12" height="12" rx="2" fill="{OK}" stroke="{INK}" stroke-width="1.2"/>')
d.t(BP_X, BP_Y - 16, "Buildpacks (pack · kpack)", 12, INK, KR, "middle", 600)
d.t(BP_X, BP_Y + 22, "kpack 기준 · pack 은 Docker 데몬", 11, MUTED, KR, "middle")

# 범례
LEG_Y = 476
d.legend(LEG_Y, [
    ("rootless · 데몬 사용", ACC),
    ("rootless · 데몬 없음", OK),
    ("root · 데몬 사용", INFO),
    ("보관 (신규 제외)", WARN),
])
d.t(X_MIN - 40, Y_MAX, "● Dockerfile 기반   ■ Dockerfile 불필요", 11, MUTED, KR, "start")

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.builder-quadrant.svg")
d.save(out_path)
print("ok gen-01-03.builder-quadrant")
