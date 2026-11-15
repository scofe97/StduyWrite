# 타입 스펙: type-architecture
# 01-02 kubelet 과 crictl 의 CRI 호출 경로
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460

d = D(W, H, "KUBERNETES · CRI · 01-02",
      "kubelet 과 crictl 의 CRI 호출 경로",
      "kubelet 과 crictl 이 CRI gRPC 소켓을 통해 containerd 와 runc 로 이어지는 계층 구조",
      lead="CRI 클라이언트 계층에서 OCI 저수준 런타임과 리눅스 커널 격리까지의 흐름")


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


# ── 상단 구역: CRI 클라이언트 ──────────────────────────────────────────
ZONE1_Y = 88
ZONE1_H = 84
zone(20, ZONE1_Y, 920, ZONE1_H, "CRI 클라이언트 계층", INFO)

# 노드 1: kubelet (x: 100, w: 320)
N1_X, N1_W = 100, 320
d.tone(N1_X, ZONE1_Y + 20, N1_W, 54, INFO, 6, "12", 1.2)
d.t(N1_X + N1_W // 2, ZONE1_Y + 41, "kubelet 데몬", 13, INFO, KR, "middle", 600)
d.t(N1_X + N1_W // 2, ZONE1_Y + 61, "Pod 수명주기 감시 및 상태 조정", 13, MUTED, KR, "middle")

# 노드 2: crictl (x: 540, w: 320)
N2_X, N2_W = 540, 320
d.tone(N2_X, ZONE1_Y + 20, N2_W, 54, WARN, 6, "12", 1.2)
d.t(N2_X + N2_W // 2, ZONE1_Y + 41, "crictl CLI", 13, WARN, KR, "middle", 600)
d.t(N2_X + N2_W // 2, ZONE1_Y + 61, "노드 디버깅 전용 진단 도구", 13, MUTED, KR, "middle")


# ── 중단 소켓 바 ─────────────────────────────────────────────────────
SOCK_Y = 196
d.chip(W // 2, SOCK_Y, "gRPC /run/containerd/containerd.sock", ACC, 12, pad=10)

# 화살표 1: kubelet -> socket (직교 꺾임)
d.arrow([(N1_X + N1_W // 2, ZONE1_Y + 74), (N1_X + N1_W // 2, SOCK_Y), (W // 2 - 145, SOCK_Y)], INFO, "info", 1.2)

# 화살표 2: crictl -> socket (직교 꺾임)
d.arrow([(N2_X + N2_W // 2, ZONE1_Y + 74), (N2_X + N2_W // 2, SOCK_Y), (W // 2 + 145, SOCK_Y)], WARN, "warn", 1.2)


# ── 중단 구역: 고수준 런타임 ───────────────────────────────────────────
ZONE2_Y = 224
ZONE2_H = 76
zone(20, ZONE2_Y, 920, ZONE2_H, "고수준 CRI 런타임 계층", ACC)

# 노드 3: containerd CRI 플러그인
N3_X, N3_W = 200, 560
d.tone(N3_X, ZONE2_Y + 18, N3_W, 48, ACC, 6, "14", 1.3)
d.t(N3_X + N3_W // 2, ZONE2_Y + 38, "containerd CRI 플러그인 (k8s.io 네임스페이스)", 13, ACC, KR, "middle", 600)
d.t(N3_X + N3_W // 2, ZONE2_Y + 56, "CRI 런타임 서비스 · 이미지 서비스 구현", 13, MUTED, KR, "middle")

# 소켓 -> containerd 화살표 (수직선)
d.arrow([(W // 2, SOCK_Y + 12), (W // 2, ZONE2_Y + 16)], ACC, "acc", 1.4)


# ── 하단 구역: 저수준 OCI 런타임 및 커널 ───────────────────────────────
ZONE3_Y = 320
ZONE3_H = 74
zone(20, ZONE3_Y, 920, ZONE3_H, "저수준 OCI 런타임 및 커널 격리 계층", OK)

# 노드 4: runc
N4_X, N4_W = 100, 320
d.tone(N4_X, ZONE3_Y + 18, N4_W, 46, OK, 6, "12", 1.2)
d.t(N4_X + N4_W // 2, ZONE3_Y + 38, "runc (OCI 런타임)", 13, OK, KR, "middle", 600)
d.t(N4_X + N4_W // 2, ZONE3_Y + 54, "OCI 명세 기반 컨테이너 생성", 13, MUTED, KR, "middle")

# 노드 5: 리눅스 커널 격리
N5_X, N5_W = 540, 320
d.tone(N5_X, ZONE3_Y + 18, N5_W, 46, OK, 6, "12", 1.2)
d.t(N5_X + N5_W // 2, ZONE3_Y + 38, "리눅스 커널 격리", 13, OK, KR, "middle", 600)
d.t(N5_X + N5_W // 2, ZONE3_Y + 54, "cgroup v2 슬라이스 · 네임스페이스 격리", 13, MUTED, KR, "middle")

# containerd -> runc 화살표 (직교 꺾임)
d.arrow([(N1_X + N1_W // 2, ZONE2_Y + 66), (N1_X + N1_W // 2, ZONE3_Y + 16)], OK, "ok", 1.2)

# runc -> 커널 화살표 (수평선)
d.arrow([(N4_X + N4_W, ZONE3_Y + 41), (N5_X - 2, ZONE3_Y + 41)], OK, "ok", 1.2)
alabel((N4_X + N4_W + N5_X) // 2, ZONE3_Y + 32, "프로세스 생성", OK)

# 범례
LEG_Y = 412
d.legend(LEG_Y, [("CRI 클라이언트", INFO), ("진단 도구", WARN), ("CRI 런타임", ACC), ("OCI 및 커널", OK)])

d.save("01-02-cri-path.svg")
