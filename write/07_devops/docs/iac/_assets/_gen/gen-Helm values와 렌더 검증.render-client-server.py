# 타입 스펙: type-architecture
# 4절 렌더링 결과 사전 검증 — 클라이언트 vs 서버 렌더
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 452

d = D(W, H, "HELM · CLIENT VS SERVER RENDER",
      "사전 렌더링 검증의 클라이언트·서버 모드와 검증 범위",
      "클라이언트 렌더와 서버 렌더의 API 서버 통신 여부 및 검증 가능 범위",
      lead="클라이언트 렌더는 로컬 완결 · 서버 모드만 API 서버와 통신해 lookup 및 리소스 종류 검증")

def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 8 + 18
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 15, label, 11, SOFT, KR, "middle")

# ── 존 1: 로컬 환경 (Helm CLI) ──────────────────────────────────
ZONE1_X, ZONE_Y, ZONE1_W, ZONE_H = 24, 96, 424, 216
zone(ZONE1_X, ZONE_Y, ZONE1_W, ZONE_H, "로컬 환경 (Helm CLI)", RULE)

# 노드 1: 클라이언트 모드
N1_X, N1_Y, N1_W, N1_H = 40, 126, 392, 74
d.box(N1_X, N1_Y, N1_W, N1_H, PAPER, RULE, 1.0, 6)
d.t(N1_X + 16, N1_Y + 24, "클라이언트 렌더 (helm template / --dry-run=client)", 13, INK, KR, "start", 600)
d.t(N1_X + 16, N1_Y + 44, "내장 Go 템플릿 엔진 실행 · API 서버 미접속", 11, MUTED, KR, "start")
d.t(N1_X + 16, N1_Y + 62, "lookup: \"false\" (빈 값) · .Capabilities: 내장 v1.35.0", 11, WARN, MONO, "start")

# 노드 2: 서버 모드
N2_X, N2_Y, N2_W, N2_H = 40, 222, 392, 74
d.box(N2_X, N2_Y, N2_W, N2_H, PAPER, ACC, 1.2, 6)
d.t(N2_X + 16, N2_Y + 24, "서버 렌더 (helm template / install --dry-run=server)", 13, ACC, KR, "start", 600)
d.t(N2_X + 16, N2_Y + 44, "클러스터 접속 허용 · lookup 및 리소스 종류 질의", 11, MUTED, KR, "start")
d.t(N2_X + 16, N2_Y + 62, "lookup: \"true\" (실제 ConfigMap 조회 반영)", 11, OK, MONO, "start")


# ── 존 2: Kubernetes 클러스터 ────────────────────────────────────
ZONE2_X, ZONE2_W = 512, 424
zone(ZONE2_X, ZONE_Y, ZONE2_W, ZONE_H, "Kubernetes 클러스터 (kube-apiserver)", INFO)

# 노드 3: kube-apiserver 및 etcd
N3_X, N3_Y, N3_W, N3_H = 528, 126, 392, 170
d.tone(N3_X, N3_Y, N3_W, N3_H, INFO, 6, "14", 1.2)
d.t(N3_X + 16, N3_Y + 24, "kube-apiserver", 13, INFO, KR, "start", 600)
d.t(N3_X + 16, N3_Y + 46, "클러스터 등록 리소스 종류(kind) 및 API 버전 확인", 11, MUTED, KR, "start")

CHIP_CX = N3_X + N3_W // 2  # 724
CHIP_W = 340

def inner_chip(cy, txt, col):
    d.o.append(f'<rect x="{CHIP_CX - CHIP_W // 2}" y="{cy - 10}" width="{CHIP_W}" height="20" rx="4" fill="{PAPER}" stroke="{col}" stroke-width="0.8"/>')
    d.t(CHIP_CX, cy + 4, txt, 11, col, KR, "middle")

inner_chip(N3_Y + 74, "ConfigMap hl-valr-existing-cm 실재", OK)
inner_chip(N3_Y + 104, "policy/v1beta1 PodDisruptionBudget 미지원", BAD)
inner_chip(N3_Y + 134, "리소스 내부 상세 필드 유효성 미검증", WARN)


# ── 화살표 (서버 모드 <-> kube-apiserver) ────────────────────────
# 화살표 Y좌표를 텍스트와 겹치지 않게 노드 하단 쪽으로 분리
AY1 = N2_Y + 38
d.arrow([(N2_X + N2_W + 2, AY1), (N3_X - 2, AY1)], ACC, "acc", 1.4)
d.t((N2_X + N2_W + N3_X) // 2, AY1 - 7, "1. 질의", 11, ACC, KR, "middle", 600)

AY2 = N2_Y + 64
d.arrow([(N3_X - 2, AY2), (N2_X + N2_W + 2, AY2)], OK, "ok", 1.4)
d.t((N2_X + N2_W + N3_X) // 2, AY2 - 7, "2. 응답", 11, OK, KR, "middle", 600)


# ── 하단 검증 범위 요약 카드 ────────────────────────────────────
SUMM_Y = 328
SUMM_H = 48
SUMM_W = 448

d.tone(ZONE1_X, SUMM_Y, SUMM_W, SUMM_H, OK, 6, "14", 1.2)
d.t(ZONE1_X + 16, SUMM_Y + 19, "서버 모드가 잡는 것", 12, OK, KR, "start", 600)
d.t(ZONE1_X + 16, SUMM_Y + 36, "클러스터 미지원 kind 및 폐기 API 버전 (policy/v1beta1 PDB 차단)", 11, INK, KR, "start")

d.tone(ZONE1_X + SUMM_W + 16, SUMM_Y, SUMM_W, SUMM_H, WARN, 6, "14", 1.2)
d.t(ZONE1_X + SUMM_W + 32, SUMM_Y + 19, "서버 모드가 놓치는 것", 12, WARN, KR, "start", 600)
d.t(ZONE1_X + SUMM_W + 32, SUMM_Y + 36, "필드 오타 및 값 범위 오류 (port: 99999, protcol, spec.bogus 통과)", 11, INK, KR, "start")


# ── 범례 ────────────────────────────────────────────────────────
LEG_Y = 404
d.legend(LEG_Y, [
    ("검증 성공 (차단)", OK),
    ("검증 누락 (통과)", WARN),
    ("서버 통신 질의", ACC),
    ("클러스터 미지원", BAD),
    ("클러스터 리소스", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm values와 렌더 검증.render-client-server.svg")
d.save(out_path)
print("ok gen-Helm values와 렌더 검증.render-client-server")
