# 06-01 §2 — 컨트롤러의 조정 루프와 그 한가운데의 API 서버.
# 원문 근거: 조정 루프는 "1. Reads the intended resource state from the API server ... Spec field
#            2. Observes the current state ... Status field, or by directly observing the cluster
#            3. Attempts to reconcile any difference ... As it modifies the state, it will store the
#            progress in the Status field" / watch 는 "create a persistent connection and ask the
#            server to push any updates to the resources through that connection".
#            원문 3단계 안에 "차이를 메우려 한다 · 조치한다 · 진행을 Status 에 적는다" 셋이 들어 있어
#            다섯 정거장으로 편다. 없는 단계를 지어내지 않는다.
# 타입 스펙: type-loop — 마지막 단계가 첫 단계로 돌아오고 한가운데가 상태를 쌓는 허브다.
#           축약: 스펙의 링 커넥터는 정거장 상자와 원의 교점을 구하라고 하지만, 여기서는 상자 반각
#                 atan(w/2 / R) 을 각도 여유로 써서 같은 원 위 호로 그린다(공식 산출, 눈대중 아님).
#           스펙의 스포크는 정거장→허브 기록 방향인데, watch 만 허브→정거장 방향이라 화살표를 뒤집는다.
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W, H = 880, 736
d = D(W, H, "LEARNING COREDNS · 06-01 §2",
      "조정 루프는 API 서버에 상태를 쌓는다",
      "컨트롤러는 의도된 상태를 읽고 현실을 관찰해 차이를 메우고, 그 진행을 다시 API 서버에 적는다. "
      "폴링 대신 watch 가 갱신을 밀어 주어 루프가 즉시 다시 돌기 시작한다.",
      "주황 정거장으로 API 서버가 변경을 밀어 줍니다")

CX, CY, R = 440, 376, 210
SW, SH = 168, 60
HW, HH = 200, 104
N = 5
stations = [
    ("Spec 읽기", "의도된 상태", "WATCH", True),
    ("현재 상태 관찰", "Status 또는 클러스터", None, False),
    ("차이 계산", "의도와 현실의 간격", None, False),
    ("조치", "파드를 만들고 지운다", None, False),
    ("Status 기록", "진행 상황을 남긴다", "STATUS", False),
]


def theta(k):
    return math.radians(-90 + k * (360 / N))


def center(k):
    a = theta(k)
    return (round((CX + R * math.cos(a)) / 4) * 4, round((CY + R * math.sin(a)) / 4) * 4)


def on_ring(deg):
    a = math.radians(deg)
    return (CX + R * math.cos(a), CY + R * math.sin(a))


def hub_edge(k):
    a = theta(k)
    c, s = math.cos(a), math.sin(a)
    t = min(HW / 2 / abs(c) if abs(c) > 1e-6 else 1e9, HH / 2 / abs(s) if abs(s) > 1e-6 else 1e9)
    return (CX + t * c, CY + t * s)


GAP = math.degrees(math.atan(SW / 2 / R)) + 3
for k in range(N):
    a1 = -90 + k * (360 / N) + GAP
    a2 = -90 + (k + 1) * (360 / N) - GAP
    x1, y1 = on_ring(a1)
    x2, y2 = on_ring(a2)
    d.path(f"M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}", MUTED, 1.4, m="ar")

# 스포크는 API 서버를 실제로 읽고 쓰는 두 정거장에만 둔다. 가운데 셋(관찰·계산·조치)은
# 클러스터를 직접 보거나 노드에서 움직이므로 허브에 선을 그으면 없는 접근을 그리게 된다.
# 경로는 직교 엘보로 낸다 — 방사형 직선은 그리기 규칙의 "비스듬한 연결선" 에 걸린다.
S0X, S0Y = center(0)
d.path(f"M {CX} {CY - HH / 2} L {CX} {S0Y + SH / 2 + 2}", ACC, 1.2, m="acc", dash="5 4")
d.chip(CX, (CY - HH / 2 + S0Y + SH / 2) / 2, "WATCH", ACC, 9)

S4X, S4Y = center(4)
ELB = CY + 32
d.path(f"M {S4X} {S4Y + SH / 2} L {S4X} {ELB} L {CX - HW / 2 - 2} {ELB}", SOFT, 1.2, m="soft", dash="5 4")
d.chip((S4X + CX - HW / 2) / 2, ELB - 18, "STATUS", SOFT, 9)

for k, (name, sub, spoke, focal) in enumerate(stations):
    cx, cy = center(k)
    if focal:
        d.tone(cx - SW / 2, cy - SH / 2, SW, SH, ACC, 6, "12", 1.4)
    else:
        d.box(cx - SW / 2, cy - SH / 2, SW, SH, PAPER2, RULE, 1.0)
    d.t(cx, cy - 4, name, 15, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 18, sub, 12, MUTED, KR)

d.box(CX - HW / 2, CY - HH / 2, HW, HH, PAPER, INFO, 1.2, 8)
d.t(CX, CY - 12, "API 서버", 16, INFO, KR, "middle", 600)
d.t(CX, CY + 10, "etcd 가 뒤를 받친다", 12, MUTED, KR)
d.t(CX, CY + 32, "Spec · Status", 12, MUTED, MONO)

d.t(20, 636, "폴링으로도 돌지만 간격을 줄이면 API 서버 부하가 늘고 늘리면 반응이 굼떠진다", 13, MUTED, KR, "start")
d.t(20, 660, "watch 는 지속 연결로 갱신을 밀어 주어 그 맞바꿈 자체를 없앤다", 13, MUTED, KR, "start")

d.legend(684, [("갱신이 밀려 들어오는 지점", ACC), ("상태가 쌓이는 허브", INFO)])
d.save("06-01.reconcile-loop.svg")
