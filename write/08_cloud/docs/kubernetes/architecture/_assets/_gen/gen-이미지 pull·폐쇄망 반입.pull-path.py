# 타입 스펙: type-architecture
# 이미지 pull·폐쇄망 반입 이미지 pull 경로 — kubelet 에서 레지스트리까지
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 396

d = D(W, H, "KUBERNETES · IMAGE PULL",
      "이미지 pull 경로",
      "kubelet 이 CRI PullImage 로 containerd 를 부르고, containerd 가 레지스트리에 매니페스트 요청·토큰 받고 재시도·레이어 받기를 차례로 보내는 경로",
      lead="자격은 Pod 의 Secret 과 노드 설정, 두 곳에서 올 수 있습니다")


def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 11 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="16" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 16, label, 13, MUTED, KR, "middle")


# ── 상단 행: kubelet → containerd → 레지스트리 ─────────────────────────
ROW_Y, NODE_H, NODE_W = 100, 64, 220
KX, CX, RX = 40, 370, 700

for x, name, sub, c in (
    (KX, "kubelet", "imagePullPolicy 판정", INFO),
    (CX, "containerd", "CRI 이미지 서비스", INFO),
    (RX, "레지스트리", "/v2/ API · 예: Harbor", OK),
):
    d.tone(x, ROW_Y, NODE_W, NODE_H, c, 6, "12", 1.2)
    d.t(x + NODE_W // 2, ROW_Y + 26, name, 14, c, KR, "middle", 600)
    d.t(x + NODE_W // 2, ROW_Y + 48, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

AY = ROW_Y + 32
d.arrow([(KX + NODE_W + 2, AY), (CX - 2, AY)], INFO, "info", 1.3)
d.arrow([(CX + NODE_W + 2, AY), (RX - 2, AY)], OK, "ok", 1.3)
d.chip((KX + NODE_W + CX) // 2, AY - 14, "PullImage", INFO, 11)
d.chip((CX + NODE_W + RX) // 2, AY - 14, "HTTPS", OK, 11)
d.t((KX + NODE_W + CX) // 2, AY + 24, "Secret 자격을", 11, MUTED, KR)
d.t((KX + NODE_W + CX) // 2, AY + 40, "실어 보냄", 11, MUTED, KR)
d.t((CX + NODE_W + RX) // 2, AY + 24, "Secret 자격,", 11, MUTED, KR)
d.t((CX + NODE_W + RX) // 2, AY + 40, "없으면 노드 설정", 11, MUTED, KR)

# ── 하단 구역: containerd 가 보내는 요청 순서 ─────────────────────────
ZY, ZH = 204, 120
zone(20, ZY, 920, ZH, "containerd 가 레지스트리에 보내는 요청 순서", RULE)
d.arrow([(CX + NODE_W // 2, ROW_Y + NODE_H), (CX + NODE_W // 2, ZY - 2)], INFO, "info", 1.3)

BY, BH, BW = ZY + 32, 68, 268
steps = [
    (40, "1. 매니페스트 요청", "GET manifests/<tag> → 401", False),
    (348, "2. 토큰 받고 재시도", "200 · 태그 → digest", True),
    (656, "3. 레이어 받기", "GET blobs/<digest> · 같은 토큰", False),
]
for x, name, sub, focal in steps:
    if focal:
        d.tone(x, BY, BW, BH, ACC, 6, "14", 1.4)
        d.t(x + BW // 2, BY + 28, name, 14, ACC, KR, "middle", 600)
    else:
        d.box(x, BY, BW, BH, PAPER, RULE, 1.0)
        d.t(x + BW // 2, BY + 28, name, 14, INK, KR, "middle", 600)
    d.t(x + BW // 2, BY + 50, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")

for x in (40, 348):
    d.arrow([(x + BW + 2, BY + BH // 2), (x + BW + 40 - 2, BY + BH // 2)], MUTED, "ar", 1.3)

d.legend(356, [("노드 안 구성요소", INFO), ("레지스트리", OK), ("자격을 처음 내는 단계", ACC)])
d.save("이미지 pull·폐쇄망 반입.pull-path.svg")
