# 01-01 §아키텍처 — 모든 통신은 API Server 를 거친다
# 본문·옛 도식: 컨트롤 플레인은 상태를 통제하고 워커 노드는 실제로 실행한다.
#   "컴포넌트끼리 직접 연결되지 않습니다." API Server 만이 통신 허브다.
#   배포 흐름 넷: ① 매니페스트 제출 → etcd 저장 ② Controller 가 부족분 Pod 생성
#   ③ Scheduler 가 노드 배정 ④ Kubelet 이 컨테이너 실행.
# 타입 스펙: 04-01 은 spec·status 축을 지므로 이 장은 다른 것을 진다 — 허브 앤 스포크다.
#           '직접 연결되지 않는다' 가 요점이므로 컴포넌트끼리 잇지 않는 것 자체를 보이고,
#           그 사실을 ✕ 로 못 박는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 700
d = D(W, H, "KUBERNETES IN ACTION · 01-01",
      "모든 통신이 API Server 한 곳을 거친다",
      "컨트롤 플레인은 상태를 통제하고 워커 노드는 실제로 실행한다. 컴포넌트끼리는 서로 "
      "직접 연결되지 않고 언제나 API Server 를 통한다.",
      lead="개발자·운영자도 예외가 아니다 — kubectl 은 API Server 로만 말한다")

HUB = (500, 356)
SPOKES = [(160, 240, "etcd", "오브젝트를 영속한다"),
          (840, 240, "Controllers", "부족분을 조정한다"),
          (160, 472, "Scheduler", "노드를 정한다"),
          (840, 472, "Kubelet", "컨테이너를 실행한다")]
KCTL = (500, 200)
BW, BH = 260, 76

ddx.band(d, 104, 644, "컴포넌트끼리 잇는 선이 하나도 없다 — 그것이 이 그림의 요점이다")

d.o.append(f'<rect x="{HUB[0]-160}" y="{HUB[1]-52}" width="320" height="104" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HUB[0], HUB[1] - 12, "API Server", 16, ACC, MONO, "middle", 600)
d.t(HUB[0], HUB[1] + 14, "유일한 통신 허브 · RESTful", 11, SOFT, KR)

def box(cx, cy, t, s, c):
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, t, 13, c, MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 14, s, 10, SOFT, KR)

box(*KCTL, "kubectl — 개발자·운영자", "오브젝트를 만든다", INFO)
for cx, cy, t, s in SPOKES:
    box(cx, cy, t, s, OK if cy > 356 else INFO)

d.path(f"M {KCTL[0]} {KCTL[1]+BH//2+6} L {HUB[0]} {HUB[1]-52-10}", INFO, 1.6, m="info")
# 마지막 구간은 허브 변으로 들어가야 화살촉이 상자를 가리킨다. 세로로 끝내면 촉이
# 상자 옆을 스치고 만다. 꺾는 열은 320 / 680 — 그래야 모든 구간의 방향이 한쪽으로 간다.
for cx, cy, _, _ in SPOKES:
    if cx < 500:
        d.path(f"M {cx+BW//2+6} {cy} L 320 {cy} L 320 {HUB[1]} L {HUB[0]-160-4} {HUB[1]}",
               MUTED, 1.5, m="ar")
    else:
        d.path(f"M {cx-BW//2-6} {cy} L 680 {cy} L 680 {HUB[1]} L {HUB[0]+160+4} {HUB[1]}",
               MUTED, 1.5, m="ar")

# 직접 연결이 없다는 사실 — 있을 법한 선 하나를 그어 지운다
d.path(f"M {SPOKES[0][0]} {SPOKES[0][1]+BH//2+6} L {SPOKES[2][0]} {SPOKES[2][1]-BH//2-6}",
       BAD, 1.4, dash="6 5")
XY = (160, 356)
for dx, dy in ((-1, -1), (-1, 1)):
    d.o.append(f'<line x1="{XY[0]-12*dx}" y1="{XY[1]-12*dy}" x2="{XY[0]+12*dx}" y2="{XY[1]+12*dy}" '
               f'stroke="{BAD}" stroke-width="2.4"/>')
# 라벨을 ✕ 옆에 두면 스포크 화살촉과 부딪힌다 — 아래로 내려 가운데 정렬한다
d.t(160, 404, "컴포넌트끼리 직접 잇지 않는다", 11, BAD, KR)

d.t(36, 556, "① 매니페스트 제출 → etcd 저장   ② Controller 가 부족분 Pod 생성   "
             "③ Scheduler 가 노드 배정   ④ Kubelet 이 컨테이너 실행", 11, SOFT, KR, "start")
d.t(36, 584, "네 단계가 모두 API Server 를 거쳐 간다 — 그래서 허브가 하나뿐이어도 전체가 돈다.",
     12, MUTED, KR, "start")
d.legend(660, [("컨트롤 플레인 쪽", INFO), ("실행하는 쪽", OK), ("유일한 허브", ACC),
               ("존재하지 않는 연결", BAD)])
d.save("01-01-control-plane-architecture.svg")
print("ok control-plane-architecture")
