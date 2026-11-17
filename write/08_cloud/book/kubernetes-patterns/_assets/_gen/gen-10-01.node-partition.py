# 10-01 노드 분단 — 같은 Pod 를 세 장면으로 본다
# 본문: replicas 1 인 ReplicaSet 에서 노드가 클러스터와 끊기면, 컨트롤 플레인은 Pod 가 죽었는지
#   연결만 끊겼는지 구분하지 못한다. taint 와 tolerationSeconds 300초가 지나 축출하면 분단된 Pod 가
#   살아 있는 채로 새 Pod 가 뜨므로 잠시 둘이 된다. 같은 지점에서 StatefulSet 은 옛 Pod 의 종료를
#   확인할 때까지 새 Pod 를 만들지 않아 0 이 된다.
# 타입 스펙: type-process — 같은 두 노드가 시간 순 세 장면으로 바뀌는 단계 흐름이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 548
PX = (24, 336, 648)             # 장면 패널 x
PW, PH = 288, 296
PY = 104

d = D(W, H, "KUBERNETES PATTERNS · 10-01",
      "분단되면 ReplicaSet 은 잠시 둘이 됩니다",
      "같은 Pod 를 세 장면으로 봅니다. 처음에는 Node A 에서 Pod 하나가 돕니다. Node A 가 끊기면 NotReady 가 되고 unreachable taint 가 붙지만 "
      "Pod 는 계속 돕니다. tolerationSeconds 300초가 지나 축출하면 ReplicaSet 은 Node B 에 새 Pod 를 만들어 둘이 되고, StatefulSet 은 옛 Pod 종료를 확인할 때까지 기다립니다.",
      lead="replicas: 1 이라도 새 Pod 는 옛 Pod 의 종료를 확인하기 전에 뜰 수 있습니다")

def pod(x, y, name, c, dashed=False, w=104):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="32" rx="5" fill="{c}18" stroke="{c}" stroke-width="1.2"'
               + (' stroke-dasharray="4 3"' if dashed else '') + '/>')
    d.t(x + w // 2, y + 21, name, 13, c, MONO, "middle", 600)

def node(px, y, name, status, c, h=112):
    d.box(px + 24, y, PW - 48, h, PAPER2, c, 1.1, 6)
    d.t(px + 36, y + 22, name, 13, INK, MONO, "start", 600)
    d.t(px + PW - 36, y + 22, status, 12, c, KR, "end")

SCENES = [
    ("1  정상", "t = 0", OK),
    ("2  분단", "t0 + 50초", WARN),
    ("3  축출", "t0 + 350초", BAD),
]
for i, (h1, h2, c) in enumerate(SCENES):
    x = PX[i]
    d.box(x, PY, PW, PH, PAPER, RULE, 0.9, 8)
    d.t(x + 16, PY + 28, h1, 14, c, KR, "start", 600)
    d.t(x + PW - 16, PY + 28, h2, 12, MUTED, KR, "end")

NA_Y, NB_Y = PY + 48, PY + 176
# 장면 1
node(PX[0], NA_Y, "Node A", "Ready", OK);    pod(PX[0] + 36, NA_Y + 44, "pod-x", OK)
node(PX[0], NB_Y, "Node B", "Ready", OK)
# 장면 2
node(PX[1], NA_Y, "Node A", "NotReady", WARN); pod(PX[1] + 36, NA_Y + 44, "pod-x", WARN)
d.t(PX[1] + 152, NA_Y + 62, "계속 도는 중", 12, MUTED, KR, "start")
d.t(PX[1] + 36, NA_Y + 100, "unreachable taint", 12, WARN, MONO, "start")
node(PX[1], NB_Y, "Node B", "Ready", OK)
d.t(PX[1] + PW // 2, NB_Y + 66, "아직 새 Pod 없음", 12, MUTED, KR)
# 장면 3
node(PX[2], NA_Y, "Node A", "NotReady", WARN); pod(PX[2] + 36, NA_Y + 44, "pod-x", BAD)
d.t(PX[2] + 152, NA_Y + 62, "살아 있을 수 있음", 12, BAD, KR, "start")
node(PX[2], NB_Y, "Node B", "Ready", OK)
d.o.append(f'<rect x="{PX[2]+36}" y="{NB_Y+44}" width="104" height="32" rx="5" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(PX[2] + 88, NB_Y + 65, "pod-y", 13, ACC, MONO, "middle", 600)
d.t(PX[2] + 152, NB_Y + 62, "새 Pod", 12, ACC, KR, "start")

# 장면 사이 화살표
for i in (0, 1):
    xa, xb = PX[i] + PW + 4, PX[i + 1] - 4
    my = PY + PH // 2
    d.path(f"M {xa} {my} L {xb} {my}", MUTED, 1.5, m="ar")

# 아래: 선택에 따른 결과
RY = PY + PH + 28
d.t(PX[1] - 24, RY + 4, "장면 3 에서 컨트롤러별 결과", 12, SOFT, KR, "start")
d.tone(PX[1] - 24, RY + 20, 296, 80, WARN, 6, "12", 1.1)
d.t(PX[1] + 124, RY + 48, "ReplicaSet", 14, WARN, MONO, "middle", 600)
d.t(PX[1] + 124, RY + 72, "새 Pod 즉시 생성 · 둘", 13, INK, KR)
d.tone(PX[2], RY + 20, 288, 80, INFO, 6, "12", 1.1)
d.t(PX[2] + 144, RY + 48, "StatefulSet", 14, INFO, MONO, "middle", 600)
d.t(PX[2] + 144, RY + 72, "옛 Pod 종료 확인까지 대기 · 0", 13, INK, KR)
d.t(PX[0], RY + 52, "같은 장애 · 두 선택", 13, INK, KR, "start", 600)
d.t(PX[0], RY + 72, "at-least-one 대 at-most-one", 12, MUTED, MONO, "start")

d.save("10-01.node-partition.svg")
print("ok node-partition")
