# 타입 스펙: type-process — 설치 도구 선택에서 사전 점검·에이전트 교체·CNI 이전·지표 수집까지 다섯 단계를 행동 레인과 도구·값 레인 두 줄로 놓은 수명주기 지도. 초점은 사전 점검 한 단계.
# 사실 출처: 추출본 cil16.txt 줄 21-166(설치 도구), 190-222(preflight), 226-254(트래픽 안정성), 258-313(CNI 이전), 317-352(지표 포트) / docs.cilium.io v1.20 operations/upgrade·installation/k8s-install-migration·observability/metrics
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 404
LABEL_W, LP = 96, 12
X0, SLOT, NODE_W, NODE_H = 116, 156, 128, 64
CHIP_Y, LAB_Y = 104, 136
LANE_Y = [152, 248]
LANE_H = 88

d = D(W, H, "CILIUM UP AND RUNNING · 16-01", "운영 수명주기 다섯 단계와 쓰는 도구",
      "설치 도구를 고르고 올리기 전에 점검하며 이전과 지표까지 이어집니다",
      "행동 한 줄과 그 단계의 도구·값 한 줄")

steps = [("1", "설치"), ("2", "점검"), ("3", "교체"), ("4", "이전"), ("5", "관측")]
FOCAL = 1
nodes_a = [("도구 고르기", "Helm 위에 GitOps"), ("사전 점검", "이미지 미리 받기"),
           ("에이전트 교체", "노드마다 재시작"), ("노드 단위 이전", "CNI 를 하나씩"),
           ("지표 수집", "구성 요소별 포트")]
nodes_b = [("helm install", "Argo CD · Flux"), ("preflight.enabled", "READY 수 일치"),
           ("helm upgrade -f", "한 마이너씩"), ("CiliumNodeConfig", "tunnelPort 8473"),
           ("9962 · 9963 · 9965", "cilium_ · envoy_")]

def nx(j): return X0 + j * SLOT
def cx(j): return nx(j) + NODE_W // 2

# 레인 라벨과 띠
for k, (nm, sub) in enumerate([("행동", "무엇을 하나"), ("도구·값", "무엇으로 하나")]):
    y = LANE_Y[k]
    d.box(LP, y, LABEL_W, LANE_H, PAPER2, RULE, 0.9, r=6)
    d.t(LP + LABEL_W / 2, y + 40, nm, 13, INK, KR, "middle", 600)
    d.t(LP + LABEL_W / 2, y + 62, sub, 12, MUTED, KR)

# 단계 머리: 번호 칩과 이름
for j, (num, lab) in enumerate(steps):
    focal = j == FOCAL
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{cx(j) - 12}" y="{CHIP_Y - 10}" width="24" height="20" rx="10" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx(j), CHIP_Y + 4, num, 12, c, MONO, "middle", 600)
    d.t(cx(j), LAB_Y, lab, 12, c, KR, "middle", 600)

# 같은 열의 행동과 도구·값을 잇는 점선
for j in range(5):
    d.line(cx(j), LANE_Y[0] + 12 + NODE_H, cx(j), LANE_Y[1] + 12, SOFT, 0.9, "3 5")

# 행동 레인 화살표 (단계 사이)
ya = LANE_Y[0] + 12 + NODE_H // 2
for j in range(4):
    focal = j in (FOCAL - 1, FOCAL)
    d.arrow([(nx(j) + NODE_W + 2, ya), (nx(j + 1) - 3, ya)], ACC if focal else MUTED, "acc" if focal else "ar", 1.5 if focal else 1.4)

# 행동 레인 노드
for j, (t1, t2) in enumerate(nodes_a):
    y = LANE_Y[0] + 12
    if j == FOCAL:
        d.tone(nx(j), y, NODE_W, NODE_H, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(nx(j), y, NODE_W, NODE_H, PAPER2, RULE, 0.9, r=6)
    d.t(cx(j), y + 28, t1, 13, INK, KR, "middle", 600)
    d.t(cx(j), y + 49, t2, 12, MUTED, KR)

# 도구·값 레인 노드
for j, (t1, t2) in enumerate(nodes_b):
    y = LANE_Y[1] + 12
    d.box(nx(j), y, NODE_W, NODE_H, PAPER, RULE, 0.9, r=6)
    d.t(cx(j), y + 28, t1, 11, INK, MONO, "middle", 600)
    d.t(cx(j), y + 49, t2, 11, MUTED, MONO if t2[0].isascii() else KR)

d.legend(LANE_Y[1] + LANE_H + 28, [("점검 단계", ACC), ("단계 사이", MUTED), ("그 단계의 도구·값", SOFT)])
d.save("16-01.chapter-overview.svg")
