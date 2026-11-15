# 타입 스펙: type-architecture
# 01-01 DooD 와 DinD 의 소켓 경로 및 권한 모델
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 440

d = D(W, H, "DEVOPS · CONTAINER · 01-01",
      "DooD 와 DinD 의 소켓 제어 경로 및 권한 구조",
      "호스트 소켓 마운트(DooD)를 통한 호스트 root 장악 경로와 내부 데몬(DinD)의 --privileged 요구 구조",
      lead="DooD 호스트 데몬 공유(상단) vs DinD 내부 데몬 기동 및 커널 노출(하단)")


def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 8 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 15, label, 11, SOFT, KR, "middle")


def alabel(x, y, txt, c=MUTED):
    w = len(txt) * 7.0 + 8
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x, y + 1, txt, 11, c, MONO if not any("가" <= ch <= "힣" for ch in txt) else KR, "middle", 600)


# ── 상단 구역: DooD (Docker-out-of-Docker) ─────────────────────────
ZONE1_Y = 88
ZONE_H = 136
zone(20, ZONE1_Y, 920, ZONE_H, "DooD: 호스트 Docker 소켓 공유 경로", ACC)

# 노드 1: 빌드 컨테이너
N1_X, N_Y1 = 36, ZONE1_Y + 28
N_W1, N_H = 200, 88
d.box(N1_X, N_Y1, N_W1, N_H, PAPER, RULE, 1.0, 6)
d.t(N1_X + N_W1 // 2, N_Y1 + 24, "빌드 컨테이너 (Agent)", 13, INK, KR, "middle", 600)
d.t(N1_X + N_W1 // 2, N_Y1 + 46, "docker build CLI 실행", 12, MUTED, MONO, "middle")
d.chip(N1_X + N_W1 // 2, N_Y1 + 68, "docker.sock 마운트", MUTED, 11)

# 화살표 1 -> 2 (X: 236 -> 340, 간격 104px, 중심 288)
N2_X = 340
N_W2 = 240
d.arrow([(N1_X + N_W1 + 2, N_Y1 + N_H // 2), (N2_X - 2, N_Y1 + N_H // 2)], ACC, "acc", 1.4)
alabel(288, N_Y1 + N_H // 2 - 8, "소켓 전달", ACC)

# 노드 2: 호스트 Docker 데몬
d.tone(N2_X, N_Y1, N_W2, N_H, ACC, 6, "14", 1.3)
d.t(N2_X + N_W2 // 2, N_Y1 + 24, "호스트 dockerd (root)", 13, ACC, KR, "middle", 600)
d.t(N2_X + N_W2 // 2, N_Y1 + 46, "호스트 root 권한 상주", 12, INK, KR, "middle")
d.chip(N2_X + N_W2 // 2, N_Y1 + 68, "호스트 root 실행", BAD, 11)

# 화살표 2 -> 3 (X: 580 -> 684, 간격 104px, 중심 632)
N3_X = 684
N_W3 = 240
d.arrow([(N2_X + N_W2 + 2, N_Y1 + N_H // 2), (N3_X - 2, N_Y1 + N_H // 2)], BAD, "bad", 1.4)
alabel(632, N_Y1 + N_H // 2 - 8, "루트 마운트", BAD)

# 노드 3: 호스트 파일시스템 및 장악
d.tone(N3_X, N_Y1, N_W3, N_H, BAD, 6, "14", 1.3)
d.t(N3_X + N_W3 // 2, N_Y1 + 24, "호스트 파일시스템 (/)", 13, BAD, KR, "middle", 600)
d.t(N3_X + N_W3 // 2, N_Y1 + 46, "chroot /host sh 탈취", 12, INK, MONO, "middle")
d.chip(N3_X + N_W3 // 2, N_Y1 + 68, "호스트 탈출 위험", BAD, 11)


# ── 하단 구역: DinD (Docker-in-Docker) ─────────────────────────
ZONE2_Y = 240
zone(20, ZONE2_Y, 920, ZONE_H, "DinD: 컨테이너 내부 데몬 실행 경로", WARN)

# 노드 4: 빌드 컨테이너 (--privileged)
N_Y2 = ZONE2_Y + 28
d.tone(N1_X, N_Y2, N_W1, N_H, WARN, 6, "12", 1.2)
d.t(N1_X + N_W1 // 2, N_Y2 + 24, "빌드 컨테이너 (Agent)", 13, WARN, KR, "middle", 600)
d.t(N1_X + N_W1 // 2, N_Y2 + 46, "docker:dind 이미지 구동", 12, INK, MONO, "middle")
d.chip(N1_X + N_W1 // 2, N_Y2 + 68, "--privileged", WARN, 11)

# 화살표 4 -> 5
d.arrow([(N1_X + N_W1 + 2, N_Y2 + N_H // 2), (N2_X - 2, N_Y2 + N_H // 2)], INFO, "info", 1.4)
alabel(288, N_Y2 + N_H // 2 - 8, "내부 기동", INFO)

# 노드 5: 내부 dockerd
d.tone(N2_X, N_Y2, N_W2, N_H, INFO, 6, "12", 1.2)
d.t(N2_X + N_W2 // 2, N_Y2 + 24, "내부 dockerd (격리)", 13, INFO, KR, "middle", 600)
d.t(N2_X + N_W2 // 2, N_Y2 + 46, "컨테이너 내 데몬 실행", 12, INK, KR, "middle")
d.chip(N2_X + N_W2 // 2, N_Y2 + 68, "독립 OverlayFS 캐시", MUTED, 11)

# 화살표 5 -> 6
d.arrow([(N2_X + N_W2 + 2, N_Y2 + N_H // 2), (N3_X - 2, N_Y2 + N_H // 2)], WARN, "warn", 1.4)
alabel(632, N_Y2 + N_H // 2 - 8, "장치 직접 접근", WARN)

# 노드 6: 호스트 커널 공격 표면
d.tone(N3_X, N_Y2, N_W3, N_H, WARN, 6, "12", 1.2)
d.t(N3_X + N_W3 // 2, N_Y2 + 24, "호스트 커널 및 장치", 13, WARN, KR, "middle", 600)
d.t(N3_X + N_W3 // 2, N_Y2 + 46, "모든 /dev 접근, 장치 제한 해제", 12, INK, KR, "middle")
d.chip(N3_X + N_W3 // 2, N_Y2 + 68, "컨테이너 탈출 표면", WARN, 11)


# 범례
LEG_Y = ZONE2_Y + ZONE_H + 24
d.legend(LEG_Y, [
    ("호스트 데몬 제어 (focal)", ACC),
    ("호스트 장악 및 탈출 위험", BAD),
    ("특권 요구 및 커널 노출", WARN),
    ("컨테이너 내부 실행", INFO),
])

d.save("01-01.socket-path.svg")
print("ok gen-01-01.socket-path")
