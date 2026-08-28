# 04-01 §API 오브젝트 모델 — 사용자는 오브젝트만 조작한다
# 본문: 사용자는 서버를 직접 만지지 않고 오브젝트(spec)만 쓴다. API Server 가 모든 요청의
#   유일한 관문이고 etcd 가 유일한 진실의 원천이며, 컨트롤러는 spec 을 읽고 status 를 쓰는
#   감시 루프다. kubelet 은 자기 노드에 배정된 Pod 를 컨테이너로 실행한다.
# 타입 스펙: type-architecture.md — 층이 셋(사용자 · 컨트롤 플레인 · 워커 노드)이라 경계 링을 세로로 쌓는다.
#           코리도어를 74px 이상 확보한 뒤 칩을 넣는다 — 처음 배치에서 30px 통로에 칩을
#           넣어 상자를 덮었다(chip error).
#           점선 경계가 사용자 · 컨트롤 플레인 · 워커 노드 세 영역을 표시하고 그 안에 컴포넌트를 둔다 —
#           정본의 "Dashed boundary rectangles mark regions" 에 위에서 아래로 흐르는 주 경로다.
#           코럴 초점은 선언하는 쪽 하나다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 826
d = D(W, H, "KUBERNETES IN ACTION · 04-01",
      "사용자는 오브젝트만 쓰고, 컨트롤 플레인이 실제를 맞춘다",
      "사용자는 서버를 직접 만지지 않고 spec 을 쓴다. 컨트롤러가 감시 루프로 실제 상태를 그 "
      "선언에 맞추고, kubelet 이 배정된 Pod 를 컨테이너로 실행한다.",
      lead="명령이 아니라 원하는 상태의 선언이다 — 그래서 같은 매니페스트를 몇 번 넣어도 같다")

USER = (200, 220)
CP = (60, 292, 880, 210)
API, ETCD, CTRL = (260, 400), (640, 350), (640, 452)
WK = (60, 542, 880, 180)
N1, N2 = (300, 642), (700, 642)

ddx.band(d, 104, 770, "API Server 가 유일한 관문이고 etcd 가 유일한 진실의 원천이다")

def box(cx, cy, w, h, t, s, c):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(t, 13, w - 18, t), 13, c,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 14, ddx.fit(s, 10, w - 14, t), 10, SOFT, KR)

def zone(rect, label, c):
    x, y, w, h = rect
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x, y, label, 11, c, off=16)

box(*USER, 240, 76, "사용자 · kubectl", "서버가 아니라 오브젝트를 만진다", ACC)

zone(CP, "Control Plane — 원하는 상태에 실제를 맞춘다", INFO)
box(*API, 300, 108, "API Server", "모든 요청의 유일한 관문 · 인증·검증", INFO)
box(*ETCD, 280, 76, "etcd", "모든 오브젝트가 저장되는 곳", INFO)
box(*CTRL, 280, 76, "Scheduler · Controller Manager", "spec 을 읽고 status 를 쓴다", INFO)

zone(WK, "Worker Nodes — 실제로 컨테이너가 도는 곳", OK)
box(N1[0], N1[1], 320, 100, "kubelet · worker 1", "배정된 Pod 를 컨테이너로 실행한다", OK)
box(N2[0], N2[1], 320, 100, "kubelet · worker 2", "스케일하면 여기에도 분산된다", OK)

d.path(f"M {USER[0]} {USER[1]+38+6} L {USER[0]} {API[1]-54-10}", ACC, 1.8, m="acc")
d.chip(USER[0], 320, "spec 을 쓴다", ACC, 11)
d.path(f"M {API[0]+150+6} {ETCD[1]} L {ETCD[0]-140-10} {ETCD[1]}", MUTED, 1.5, m="ar")
d.chip(453, ETCD[1], "저장", MUTED, 11)
d.path(f"M {API[0]+150+6} {CTRL[1]} L {CTRL[0]-140-10} {CTRL[1]}", MUTED, 1.5, m="ar")
d.chip(453, CTRL[1], "감시한다", MUTED, 11)

d.path(f"M {API[0]} {CP[1]+CP[3]+6} L {API[0]} {N1[1]-50-10}", OK, 1.6, m="ok")
d.chip(400, 570, "배정된 Pod 를 감지한다", OK, 11)
d.path(f"M {N1[0]+160+6} {N1[1]} L {N2[0]-160-10} {N2[1]}", MUTED, 1.4, dash="6 5")
d.chip(500, N1[1], "분산된다", MUTED, 11)

# WK 존이 542~722 를 쓴다 — 산문은 그 아래로. 식으로 적지 말고 값을 확인해 적는다.
d.t(36, 748, "컨트롤러는 spec(원함)을 읽고 실제와의 간극을 확인해 작업한 뒤 status(실제)를 쓴다 "
                  "— 그 루프가 계속 돈다.", 12, MUTED, KR, "start")
d.legend(786, [("선언하는 쪽", ACC), ("컨트롤 플레인", INFO), ("워커 노드", OK)])
d.save("04-01-api-object-model.svg")
print("ok api-object-model")
