# 타입 스펙: type-process — 기존 CNI 클러스터에서 노드 한 대를 Cilium 으로 옮기는 일곱 단계. 위 레인은 운영자의 명령, 아래 레인은 노드와 Cilium 에서 일어나는 일이다. 초점은 에이전트 재시작으로 CNI 설정이 쓰이는 단계 하나.
# 값 근거: 16-01 본문 §4, docs.cilium.io/en/v1.20/installation/k8s-install-migration/ (cordon·drain·label·delete pod·reboot·validate·uncordon, 05-cilium.conflist, CiliumNodeConfig, 10.245.0.0/16)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 992, 412
LABEL_W, LP = 68, 12
X0, SLOT, NODE_W, NODE_H = 92, 129, 110, 68
CHIP_Y, LAB_Y = 104, 136
LANE_Y = [152, 252]
LANE_H = 92

d = D(W, H, "CILIUM UP AND RUNNING · 16-01 §4", "노드 한 대를 옮기는 일곱 단계",
      "라벨을 붙인 노드만 Cilium 이 CNI 를 맡고 나머지는 기존 CNI 로 남습니다",
      "컨트롤 플레인 외 노드 한 대마다 1~7 을 반복합니다")

steps = [("1", "차단"), ("2", "비움"), ("3", "표시"), ("4", "재시작"), ("5", "재부팅"), ("6", "검증"), ("7", "재개")]
FOCAL = 3

def nx(j): return X0 + j * SLOT
def cx(j): return nx(j) + NODE_W // 2

for k, (nm, sub) in enumerate([("운영자", "kubectl"), ("노드", "Cilium")]):
    y = LANE_Y[k]
    d.box(LP, y, LABEL_W, LANE_H, PAPER2, RULE, 0.9, r=6)
    d.t(LP + LABEL_W / 2, y + 40, nm, 13, INK, KR, "middle", 600)
    d.t(LP + LABEL_W / 2, y + 62, sub, 11, MUTED, MONO)

for j, (num, lab) in enumerate(steps):
    c = ACC if j == FOCAL else MUTED
    d.o.append(f'<rect x="{cx(j) - 12}" y="{CHIP_Y - 10}" width="24" height="20" rx="10" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx(j), CHIP_Y + 4, num, 12, c, MONO, "middle", 600)
    d.t(cx(j), LAB_Y, lab, 13, c, KR, "middle", 600)

# (레인, 단계, 제목, 부제, 도구)
nodes = [
    (0, 0, "cordon", "스케줄 차단", None),
    (0, 1, "drain", "Pod 비우기", None),
    (0, 2, "label", "CiliumNodeConfig", INFO),
    (1, 3, "에이전트 재시작", "05-cilium.conflist", "focal"),
    (1, 4, "노드 재부팅", "Pod 재기동", None),
    (0, 5, "cilium status", "10.245.0.0/16", OK),
    (0, 6, "uncordon", "스케줄 재개", None),
]
def ny(k): return LANE_Y[k] + 12
def mid(k): return ny(k) + NODE_H // 2

# 연결선: 모두 직각, 먼저 그려 노드 아래에 깐다
d.arrow([(nx(0) + NODE_W + 2, mid(0)), (nx(1) - 3, mid(0))], MUTED, "ar", 1.4)
d.arrow([(nx(1) + NODE_W + 2, mid(0)), (nx(2) - 3, mid(0))], MUTED, "ar", 1.4)
d.arrow([(nx(2) + NODE_W + 2, mid(0)), (cx(3), mid(0)), (cx(3), ny(1) - 3)], ACC, "acc", 1.6)
d.arrow([(nx(3) + NODE_W + 2, mid(1)), (nx(4) - 3, mid(1))], ACC, "acc", 1.6)
d.arrow([(nx(4) + NODE_W + 2, mid(1)), (cx(5), mid(1)), (cx(5), ny(0) + NODE_H + 3)], OK, "ok", 1.4)
d.arrow([(nx(5) + NODE_W + 2, mid(0)), (nx(6) - 3, mid(0))], OK, "ok", 1.4)

for k, j, t1, t2, tone in nodes:
    y = ny(k)
    if tone == "focal":
        d.tone(nx(j), y, NODE_W, NODE_H, ACC, r=6, op="14", sw=1.4)
    elif tone in (INFO, OK):
        d.tone(nx(j), y, NODE_W, NODE_H, tone, r=6, op="10", sw=1.0)
    else:
        d.box(nx(j), y, NODE_W, NODE_H, PAPER2, RULE, 0.9, r=6)
    mono1 = t1.isascii()
    mono2 = t2.isascii()
    d.t(cx(j), y + 28, t1, 11 if mono1 else 13, ACC if tone == "focal" else INK, MONO if mono1 else KR, "middle", 600)
    d.t(cx(j), y + 50, t2, 10 if (mono2 and len(t2) >= 16) else (11 if mono2 else 13), MUTED, MONO if mono2 else KR)

d.legend(LANE_Y[1] + LANE_H + 28, [("CNI 대상 지정", INFO), ("CNI 설정 기록", ACC), ("검증 · 재개", OK), ("준비 단계", MUTED)])
d.save("16-01.node-migration-process.svg")
