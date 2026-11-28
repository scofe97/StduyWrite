# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""Harbor Replication (Push / Pull) 과 Proxy Cache 의 통신 방향·트리거·역할 비교."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 608

d = D(
    W,
    H,
    "DEVOPS · HARBOR · REPLICATION & PROXY CACHE",
    "Harbor Replication (Push·Pull) 과 Proxy Cache 의 구조 비교",
    "Push 복제는 로컬 이벤트를 원격으로 밀어내고, Pull 복제는 로컬 jobservice 가 원격에서 당겨 오며, Proxy Cache 는 클라이언트 pull 시점에 온디맨드로 캐시한다",
    lead="연결을 누가 여는지와 아티팩트가 어느 방향으로 흐르는지로 세 방식이 갈립니다",
)


def zone(x, y, w, h, label, c=RULE):
    d.o.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>'
    )
    lw = sum(13 if "가" <= ch <= "힣" else 7.8 for ch in label) + 24
    d.o.append(f'<rect x="{x + 16}" y="{y + 7}" width="{lw:.0f}" height="20" rx="3" fill="{PAPER}"/>')
    d.t(x + 16 + lw / 2, y + 21, label, 13, SOFT, KR, "middle")


def alabel(x, y, txt, c=MUTED):
    fam = MONO if not any("가" <= ch <= "힣" for ch in txt) else KR
    w = sum(12 if "가" <= ch <= "힣" else 7.5 for ch in txt) + 12
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x, y + 2, txt, 13, c, fam, "middle", 600)


# 가로 배치: N1(36..240, w=204), gap1(240..356, mid=298), N2(356..588, w=232), gap2(588..704, mid=646), N3(704..924, w=220)
N1_X, N1_W = 36, 204
N2_X, N2_W = 356, 232
N3_X, N3_W = 704, 220
GAP1_M = 298
GAP2_M = 646
N_H = 88

# ── Zone 1: Push-based Replication ─────────────────────────────────────────
Z1_Y, Z_H = 88, 140
zone(20, Z1_Y, 920, Z_H, "1. Push Replication (로컬 → 원격)", INFO)
N_Y1 = Z1_Y + 36

d.box(N1_X, N_Y1, N1_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N1_X + N1_W // 2, N_Y1 + 24, "CI / 개발자", 13, INK, KR, "middle", 600)
d.t(N1_X + N1_W // 2, N_Y1 + 46, "docker push / retag", 12, MUTED, MONO, "middle")
d.chip(N1_X + N1_W // 2, N_Y1 + 68, "로컬 변경 발생", MUTED, 13)

d.arrow([(N1_X + N1_W + 2, N_Y1 + 44), (N2_X - 2, N_Y1 + 44)], INFO, "info", 1.4)
alabel(GAP1_M, N_Y1 + 30, "push", INFO)

d.tone(N2_X, N_Y1, N2_W, N_H, INFO, 6, "14", 1.3)
d.t(N2_X + N2_W // 2, N_Y1 + 24, "로컬 Harbor (원본)", 13, INFO, KR, "middle", 600)
d.t(N2_X + N2_W // 2, N_Y1 + 46, "Event / Cron / Manual", 12, INK, MONO, "middle")
d.chip(N2_X + N2_W // 2, N_Y1 + 68, "jobservice 송신", INFO, 13)

d.arrow([(N2_X + N2_W + 2, N_Y1 + 44), (N3_X - 2, N_Y1 + 44)], INFO, "info", 1.4)
alabel(GAP2_M, N_Y1 + 30, "송신 연결", INFO)

d.box(N3_X, N_Y1, N3_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N3_X + N3_W // 2, N_Y1 + 24, "원격 레지스트리 (대상)", 13, INK, KR, "middle", 600)
d.t(N3_X + N3_W // 2, N_Y1 + 46, "DR Harbor · ECR · ACR", 12, MUTED, MONO, "middle")
d.chip(N3_X + N3_W // 2, N_Y1 + 68, "쓰기 권한 필요", WARN, 13)


# ── Zone 2: Pull-based Replication ─────────────────────────────────────────
Z2_Y = 240
zone(20, Z2_Y, 920, Z_H, "2. Pull Replication (원격 → 로컬)", OK)
N_Y2 = Z2_Y + 36

d.box(N1_X, N_Y2, N1_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N1_X + N1_W // 2, N_Y2 + 24, "원격 레지스트리 (원본)", 13, INK, KR, "middle", 600)
d.t(N1_X + N1_W // 2, N_Y2 + 46, "Docker Hub · 메인 Harbor", 12, MUTED, MONO, "middle")
d.chip(N1_X + N1_W // 2, N_Y2 + 68, "읽기 권한만 필요", OK, 13)

d.arrow([(N2_X - 2, N_Y2 + 30), (N1_X + N1_W + 2, N_Y2 + 30)], MUTED, "ar", 1.2, dash="5 4")
alabel(GAP1_M, N_Y2 + 16, "pull 질의", MUTED)
d.arrow([(N1_X + N1_W + 2, N_Y2 + 60), (N2_X - 2, N_Y2 + 60)], OK, "ok", 1.4)
alabel(GAP1_M, N_Y2 + 78, "수신 저장", OK)

d.tone(N2_X, N_Y2, N2_W, N_H, OK, 6, "14", 1.3)
d.t(N2_X + N2_W // 2, N_Y2 + 24, "로컬 Harbor (대상)", 13, OK, KR, "middle", 600)
d.t(N2_X + N2_W // 2, N_Y2 + 46, "Scheduled / Manual", 12, INK, MONO, "middle")
d.chip(N2_X + N2_W // 2, N_Y2 + 68, "Event 트리거 불가", WARN, 13)

d.arrow([(N2_X + N2_W + 2, N_Y2 + 44), (N3_X - 2, N_Y2 + 44)], OK, "ok", 1.4)
alabel(GAP2_M, N_Y2 + 30, "로컬 pull", OK)

d.box(N3_X, N_Y2, N3_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N3_X + N3_W // 2, N_Y2 + 24, "내부 K8s 클러스터", 13, INK, KR, "middle", 600)
d.t(N3_X + N3_W // 2, N_Y2 + 46, "사내망 이미지 소비", 13, MUTED, KR, "middle")
d.chip(N3_X + N3_W // 2, N_Y2 + 68, "사전 배치 완료", OK, 13)


# ── Zone 3: Proxy Cache (Pull-Through) ─────────────────────────────────────
Z3_Y = 392
zone(20, Z3_Y, 920, Z_H, "3. Proxy Cache (pull 온디맨드)", ACC)
N_Y3 = Z3_Y + 36

d.box(N1_X, N_Y3, N1_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N1_X + N1_W // 2, N_Y3 + 24, "K8s 노드 / 클라이언트", 13, INK, KR, "middle", 600)
d.t(N1_X + N1_W // 2, N_Y3 + 46, "harbor/proxy-proj/img", 12, MUTED, MONO, "middle")
d.chip(N1_X + N1_W // 2, N_Y3 + 68, "직접 push 불가", BAD, 13)

d.arrow([(N1_X + N1_W + 2, N_Y3 + 44), (N2_X - 2, N_Y3 + 44)], ACC, "acc", 1.4)
alabel(GAP1_M, N_Y3 + 30, "pull 요청", ACC)

d.tone(N2_X, N_Y3, N2_W, N_H, ACC, 6, "14", 1.3)
d.t(N2_X + N2_W // 2, N_Y3 + 24, "Harbor Proxy Cache", 13, ACC, KR, "middle", 600)
d.t(N2_X + N2_W // 2, N_Y3 + 46, "미스 pull · 히트 HEAD", 13, INK, KR, "middle")
d.chip(N2_X + N2_W // 2, N_Y3 + 68, "기본 7일 보존 정책", ACC, 13)

d.arrow([(N2_X + N2_W + 2, N_Y3 + 30), (N3_X - 2, N_Y3 + 30)], ACC, "acc", 1.2, dash="5 4")
alabel(GAP2_M, N_Y3 + 16, "HEAD / GET", ACC)
d.arrow([(N3_X - 2, N_Y3 + 60), (N2_X + N2_W + 2, N_Y3 + 60)], OK, "ok", 1.4)
alabel(GAP2_M, N_Y3 + 78, "미스 시 전송", OK)

d.box(N3_X, N_Y3, N3_W, N_H, PAPER, RULE, 1.0, 6)
d.t(N3_X + N3_W // 2, N_Y3 + 24, "업스트림 레지스트리", 13, INK, KR, "middle", 600)
d.t(N3_X + N3_W // 2, N_Y3 + 46, "Docker Hub · ECR · GHCR", 12, MUTED, MONO, "middle")
d.chip(N3_X + N3_W // 2, N_Y3 + 68, "HEAD 무과금", OK, 13)

d.legend(
    H - 56,
    [
        ("Push 복제", INFO),
        ("Pull 복제", OK),
        ("Proxy Cache", ACC),
        ("제약·주의", WARN),
        ("차단·불가", BAD),
    ],
)

out = pathlib.Path(__file__).resolve().parent.parent / "레지스트리 복제·프록시 캐시.replication-modes.svg"
d.save(str(out))
print("ok gen-replication-modes")
