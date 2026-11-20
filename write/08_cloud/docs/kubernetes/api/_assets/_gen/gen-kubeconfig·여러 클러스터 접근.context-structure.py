# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""kubeconfig·여러 클러스터 접근 §1 도식 — 컨텍스트가 클러스터와 사용자를 연결하는 구조.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
스킨은 writing-method Diagram Design 스타일 계약의 다크 토큰을 쓴다.
"""
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460

d = D(W, H, "KUBECONFIG · CONTEXTS -> CLUSTERS & USERS",
      "컨텍스트가 클러스터와 사용자를 연결하는 구조",
      "contexts 블록이 cluster 와 user 를 이름으로 묶고 current-context 가 활성 대상을 가리킴",
      lead="한 클러스터에 여러 사용자가 매핑되며 인증서 방향이 서로 나뉨")

def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 9 + 20
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 17, label, 13, SOFT, KR, "middle")

def alabel(x, y, txt, c=MUTED):
    w = len(txt) * 8.0 + 12
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x, y + 2, txt, 13, c, MONO if not any("가" <= ch <= "힣" for ch in txt) else KR, "middle", 600)

# ── 상단 구역: contexts 및 current-context ─────────────────────────
ZONE1_Y = 88
ZONE1_H = 116
zone(20, ZONE1_Y, 920, ZONE1_H, "contexts: 클러스터와 사용자 결합 포인터", ACC)

# 포인터: current-context
d.chip(110, ZONE1_Y + 50, "current-context", ACC, 11)
d.arrow([(170, ZONE1_Y + 50), (218, ZONE1_Y + 50)], ACC, "acc", 1.4)

# 컨텍스트 1: dev-admin (활성)
CTX1_X, CTX_Y = 220, ZONE1_Y + 20
CTX_W, CTX_H = 320, 76
d.tone(CTX1_X, CTX_Y, CTX_W, CTX_H, ACC, 6, "14", 1.3)
d.t(CTX1_X + CTX_W // 2, CTX_Y + 22, "dev-admin (현재 활성 컨텍스트)", 13, ACC, KR, "middle", 600)
d.t(CTX1_X + CTX_W // 2, CTX_Y + 44, "cluster: dev-cluster  |  user: admin", 11, INK, MONO, "middle")
d.t(CTX1_X + CTX_W // 2, CTX_Y + 64, "namespace: default", 11, MUTED, MONO, "middle")

# 컨텍스트 2: dev-dev (비활성)
CTX2_X = 580
d.box(CTX2_X, CTX_Y, CTX_W, CTX_H, PAPER, RULE, 1.0, 6)
d.t(CTX2_X + CTX_W // 2, CTX_Y + 22, "dev-developer (대기 컨텍스트)", 13, INK, KR, "middle", 600)
d.t(CTX2_X + CTX_W // 2, CTX_Y + 44, "cluster: dev-cluster  |  user: developer", 11, MUTED, MONO, "middle")
d.t(CTX2_X + CTX_W // 2, CTX_Y + 64, "namespace: frontend", 11, MUTED, MONO, "middle")

# ── 하단 좌측 구역: clusters (서버 검증) ─────────────────────────
ZONE2_Y = 244
ZONE2_H = 144
zone(20, ZONE2_Y, 440, ZONE2_H, "clusters", INFO)

CLU_X, CLU_Y = 40, ZONE2_Y + 28
CLU_W, CLU_H = 400, 96
d.tone(CLU_X, CLU_Y, CLU_W, CLU_H, INFO, 6, "12", 1.2)
d.t(CLU_X + CLU_W // 2, CLU_Y + 24, "dev-cluster", 14, INFO, MONO, "middle", 600)
d.t(CLU_X + CLU_W // 2, CLU_Y + 46, "server: https://192.0.2.10:6443", 11, INK, MONO, "middle")
d.t(CLU_X + CLU_W // 2, CLU_Y + 66, "certificate-authority-data: <CA PEM>", 11, MUTED, MONO, "middle")
d.chip(CLU_X + CLU_W // 2, CLU_Y + 86, "서버 검증 (CA 신뢰)", INFO, 13)

# ── 하단 우측 구역: users (클라이언트 인증) ─────────────────────────
zone(500, ZONE2_Y, 440, ZONE2_H, "users", OK)

# 사용자 1: admin
USR1_X, USR_Y = 520, ZONE2_Y + 28
USR_W, USR_H = 190, 96
d.tone(USR1_X, USR_Y, USR_W, USR_H, OK, 6, "12", 1.2)
d.t(USR1_X + USR_W // 2, USR_Y + 22, "admin (관리자)", 13, OK, KR, "middle", 600)
d.t(USR1_X + USR_W // 2, USR_Y + 44, "client-cert-data", 11, INK, MONO, "middle")
d.t(USR1_X + USR_W // 2, USR_Y + 62, "client-key-data", 11, MUTED, MONO, "middle")
d.chip(USR1_X + USR_W // 2, USR_Y + 84, "클라이언트 인증", OK, 13)

# 사용자 2: developer
USR2_X = 730
d.box(USR2_X, USR_Y, USR_W, USR_H, PAPER, RULE, 1.0, 6)
d.t(USR2_X + USR_W // 2, USR_Y + 22, "developer (개발자)", 13, INK, KR, "middle", 600)
d.t(USR2_X + USR_W // 2, USR_Y + 44, "token", 11, INK, MONO, "middle")
d.t(USR2_X + USR_W // 2, USR_Y + 62, "(또는 exec 플러그인)", 11, MUTED, KR, "middle")
d.chip(USR2_X + USR_W // 2, USR_Y + 84, "클라이언트 인증", MUTED, 13)

# ── 연결선 (직교 L자 / U자 경로) ─────────────────────────
# CTX1 하단 좌측 포트(x=300) -> dev-cluster 상단 포트(x=240)
d.arrow([(300, CTX_Y + CTX_H), (300, 230), (240, 230), (240, CLU_Y - 2)], INFO, "info", 1.4)
alabel(270, 218, "cluster 참조", INFO)

# CTX1 하단 우측 포트(x=460) -> admin 상단 포트(x=615)
d.arrow([(460, CTX_Y + CTX_H), (460, 230), (615, 230), (615, USR_Y - 2)], OK, "ok", 1.4)
alabel(538, 218, "user 참조", OK)

# CTX2 하단 좌측 포트(x=660) -> dev-cluster 상단 포트(x=360)
d.arrow([(660, CTX_Y + CTX_H), (660, 238), (360, 238), (360, CLU_Y - 2)], MUTED, "ar", 1.2, dash="4 3")

# CTX2 하단 우측 포트(x=825) -> developer 상단 포트(x=825)
d.arrow([(825, CTX_Y + CTX_H), (825, USR_Y - 2)], MUTED, "ar", 1.2, dash="4 3")

# 범례
d.legend(412, [
    ("활성 연결", ACC),
    ("대기 참조", MUTED),
    ("서버 검증 (CA)", INFO),
    ("클라이언트 인증", OK),
])

out_path = pathlib.Path(__file__).resolve().parents[1] / "kubeconfig·여러 클러스터 접근.context-structure.svg"
d.save(str(out_path))
print(f"wrote {out_path.name}")
