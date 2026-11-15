# 타입 스펙: type-data-flow
# 01-02 네 도구의 소켓과 네임스페이스 관측 범위
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460

d = D(W, H, "KUBERNETES · RUNTIME · 01-02",
      "네 도구의 소켓과 네임스페이스 관측 범위",
      "crictl, ctr, nerdctl, docker 가 연결하는 소켓 경로와 네임스페이스 격리 차이",
      lead="containerd k8s.io 네임스페이스와 독립 Docker 데몬이 가르는 관측 대상")


def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 9 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="16" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 16, label, 13, SOFT, KR, "middle")


def alabel(x, y, txt, c=MUTED):
    w = len(txt) * 7.5 + 8
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="16" rx="2" fill="{PAPER}"/>')
    d.t(x, y + 2, txt, 13, c, MONO if not any("가" <= ch <= "힣" for ch in txt) else KR, "middle", 600)


# ── 좌측: 4대 CLI 진단 도구 ──────────────────────────────────────────
CLI_X = 36
CLI_W = 220
CLI_H = 68

# crictl (y: 88..156)
d.tone(CLI_X, 88, CLI_W, CLI_H, OK, 6, "12", 1.2)
d.t(CLI_X + CLI_W // 2, 108, "crictl", 13, OK, MONO, "middle", 600)
d.t(CLI_X + CLI_W // 2, 125, "CRI 전용 디버깅 CLI", 13, MUTED, KR, "middle")
d.chip(CLI_X + CLI_W // 2, 142, "k8s.io 자동 조회", OK, 11)

# ctr (y: 164..232)
d.tone(CLI_X, 164, CLI_W, CLI_H, INFO, 6, "12", 1.2)
d.t(CLI_X + CLI_W // 2, 184, "ctr", 13, INFO, MONO, "middle", 600)
d.t(CLI_X + CLI_W // 2, 201, "containerd 자체 저수준 CLI", 13, MUTED, KR, "middle")
d.chip(CLI_X + CLI_W // 2, 218, "-n k8s.io 지정 필수", WARN, 11)

# nerdctl (y: 240..308)
d.tone(CLI_X, 240, CLI_W, CLI_H, INFO, 6, "12", 1.2)
d.t(CLI_X + CLI_W // 2, 260, "nerdctl", 13, INFO, MONO, "middle", 600)
d.t(CLI_X + CLI_W // 2, 277, "Docker 호환 containerd CLI", 13, MUTED, KR, "middle")
d.chip(CLI_X + CLI_W // 2, 294, "-n k8s.io 지정 필수", WARN, 11)

# docker (y: 316..384)
d.tone(CLI_X, 316, CLI_W, CLI_H, BAD, 6, "12", 1.2)
d.t(CLI_X + CLI_W // 2, 336, "docker", 13, BAD, MONO, "middle", 600)
d.t(CLI_X + CLI_W // 2, 353, "Docker Engine 전용 CLI", 13, MUTED, KR, "middle")
d.chip(CLI_X + CLI_W // 2, 370, "k8s 컨테이너 관측 불가", BAD, 11)


# ── 우측 상단: containerd 데몬 구역 ──────────────────────────────────
ZONE_C_X = 380
ZONE_C_Y = 88
ZONE_C_W = 540
ZONE_C_H = 212
zone(ZONE_C_X, ZONE_C_Y, ZONE_C_W, ZONE_C_H, "containerd 데몬 (/run/containerd/containerd.sock)", ACC)

# containerd 내부: k8s.io 네임스페이스
d.tone(ZONE_C_X + 24, ZONE_C_Y + 28, 492, 80, OK, 6, "14", 1.3)
d.t(ZONE_C_X + 270, ZONE_C_Y + 54, "네임스페이스: k8s.io (쿠버네티스 워크로드)", 13, OK, KR, "middle", 600)
d.t(ZONE_C_X + 270, ZONE_C_Y + 74, "kubelet 이 생성한 Pod 샌드박스 및 애플리케이션 컨테이너 상주", 13, MUTED, KR, "middle")
d.chip(ZONE_C_X + 270, ZONE_C_Y + 94, "pause 인프라 컨테이너 · Pod 네트워크 공유", OK, 11)

# containerd 내부: default 네임스페이스
d.box(ZONE_C_X + 24, ZONE_C_Y + 120, 492, 72, PAPER, RULE, 1.0, 6)
d.t(ZONE_C_X + 270, ZONE_C_Y + 146, "네임스페이스: default (일반 컨테이너)", 13, SOFT, KR, "middle", 600)
d.t(ZONE_C_X + 270, ZONE_C_Y + 166, "ctr 또는 nerdctl 기본 실행 컨테이너 (쿠버네티스 외부)", 13, MUTED, KR, "middle")


# ── 우측 하단: 별개 Docker 데몬 구역 ─────────────────────────────────
ZONE_D_Y = 316
ZONE_D_H = 68
zone(ZONE_C_X, ZONE_D_Y, ZONE_C_W, ZONE_D_H, "독립 Docker Engine 데몬 (/var/run/docker.sock)", BAD)
d.tone(ZONE_C_X + 24, ZONE_D_Y + 24, 492, 36, BAD, 6, "12", 1.2)
d.t(ZONE_C_X + 270, ZONE_D_Y + 46, "dockerd 단독 컨테이너 공간 (kubelet 과 연결 없음)", 13, BAD, KR, "middle", 600)


# ── 연결 화살표 (모두 직교 꺾임 또는 수평선) ─────────────────────────
# crictl -> k8s.io (직접 수평 연결)
d.arrow([(CLI_X + CLI_W, 118), (ZONE_C_X + 22, 118)], OK, "ok", 1.4)
alabel(318, 110, "CRI gRPC", OK)

# ctr -> default (직교 꺾임)
d.arrow([(CLI_X + CLI_W, 198), (318, 198), (318, 156), (ZONE_C_X + 22, 156)], WARN, "warn", 1.2)

# nerdctl -> default (직교 꺾임)
d.arrow([(CLI_X + CLI_W, 274), (334, 274), (334, 168), (ZONE_C_X + 22, 168)], WARN, "warn", 1.2)

# docker -> dockerd (수평 연결)
d.arrow([(CLI_X + CLI_W, 350), (ZONE_C_X + 22, 350)], BAD, "bad", 1.4)
alabel(318, 342, "docker.sock", BAD)


# 범례
LEG_Y = 412
d.legend(LEG_Y, [("CRI 직접 조회", OK), ("런타임 데몬", ACC), ("호스트 CLI", INFO), ("옵션 필요", WARN), ("접근 불가", BAD)])

d.save("01-02-crictl-views.svg")
