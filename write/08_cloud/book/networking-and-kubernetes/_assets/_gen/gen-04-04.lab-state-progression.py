# 04-04.lab-state-progression — 실습이 클러스터를 어느 상태로 밀고 가는가
# 본문 요구: 실습 문서에 도식이 한 장도 없어 묶음이 서로 무관한 명령 더미로 읽힌다.
#           묶음은 클러스터 상태를 한 칸씩 옮기는 전이이고, 지금 어디까지 왔는지가 보여야 한다.
# 타입 스펙: type-state.md — 주체 하나(클러스터)의 상태 전이. 전이 라벨은 event [guard] 꼴,
#           coral 은 독자가 주목할 상태 하나에만 — 여기서는 실습이 실제로 도달한 마지막 상태.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 700
d = D(W, H, "ch4 LAB · CLUSTER STATE",
      "실습이 클러스터를 어느 상태로 밀고 가는가",
      "묶음마다 클러스터가 한 칸씩 옮겨 가고, 오른쪽에 그 자리에서 실제로 본 값을 적는다.",
      lead="묶음은 명령 더미가 아니라 상태를 옮기는 전이다")

BX, BW, BH = 24, 430, 60
OX, OW = 500, 476
CXX = BX + BW / 2
CYS = [152, 246, 340, 434, 528]

STATES = [
    ("CNI 가 없다", "노드 NotReady · CoreDNS Pending", True,
     "/etc/cni/net.d 비어 있음", "노드 셋 다 NotReady · 묶음 1"),
    ("CNI 가 붙었다", "노드 Ready · podCIDR 를 받는다", True,
     "10.244.0.0/24 · 10.244.2.0/24 · 10.244.1.0/24", "05-cilium.conflist 하나 · 묶음 2"),
    ("서비스가 규칙이 됐다", "SVC 체인 하나 + SEP 체인 셋", True,
     "확률 0.33333333349 → 0.5 → 없음", "세 노드 모두 default/web 11줄 · 묶음 3"),
    ("명단에서 빠진다", "들어오는 길만 끊긴다", True,
     "낙하 8초 · 복귀 1~4초", "SEP 체인이 아예 안 생긴다 · 묶음 4"),
    ("선택되어 잠긴다", "허용한 것만 들어온다", True,
     "들어오는 쪽 000 5s · 나가는 쪽 bad address", "정책은 합쳐진다 · 묶음 5"),
]
EVENTS = [
    "helm install cilium  [ipam.mode=kubernetes]",
    "create deployment web --replicas=3  /  expose",
    "rm /tmp/ready  [readinessProbe 실패]",
    "apply NetworkPolicy  [라벨에 걸린다]",
]

d.o.append(f'<circle cx="{CXX}" cy="96" r="6" fill="{INK}"/>')
d.path(f"M {CXX} 104 L {CXX} {CYS[0]-BH/2-4}", SOFT, 1.4, m="soft")

for i, (title, sub, done, o1, o2) in enumerate(STATES):
    cy = CYS[i]
    focal = (i == 4)
    col = ACC if focal else (INFO if done else SOFT)
    y = cy - BH / 2
    if focal:
        d.tone(BX, y, BW, BH, ACC, 8, "10", 1.4)
    elif done:
        d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    else:
        d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{BH}" rx="8" fill="none" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(BX + 18, cy - 4, ddx.fit(title, 13, BW - 36, f"st {title}"), 13, col, KR, "start", 600)
    d.t(BX + 18, cy + 17, ddx.fit(sub, 11, BW - 36, f"sub {sub}"), 11, MUTED, KR, "start")

    oc = INK if done else SOFT
    d.line(OX, y, OX, y + BH, RULE, 0.8)
    lat = all(ord(c) < 128 for c in o1)
    d.t(OX + 18, cy - 4, ddx.fit(o1, 11, OW - 36, f"obs {o1}"), 11 if not lat else 11, oc,
        MONO if lat else KR, "start")
    d.t(OX + 18, cy + 17, ddx.fit(o2, 11, OW - 36, f"obs2 {o2}"), 11, MUTED, KR, "start")

    if i < len(EVENTS):
        y1, y2 = cy + BH / 2, CYS[i + 1] - BH / 2 - 4
        c = SOFT if i >= 3 else MUTED
        d.path(f"M {CXX} {y1} L {CXX} {y2}", c, 1.4, m="soft" if c == SOFT else "ar",
               dash="4 4" if i >= 3 else None)
        d.t(CXX + 14, (y1 + y2) / 2 + 4,
            ddx.fit(EVENTS[i], 11, W - 48 - (CXX + 14), f"ev {i}"), 11, c, MONO, "start")

d.path(f"M {CXX} {CYS[-1]+BH/2} L {CXX} 572", SOFT, 1.4, dash="4 4")
d.o.append(f'<circle cx="{CXX}" cy="580" r="8" fill="none" stroke="{SOFT}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{CXX}" cy="580" r="5" fill="{SOFT}"/>')
d.t(CXX + 20, 584, "묶음 6~8 — 이름 · L7 · 노드 밖 (모두 완료)", 11, SOFT, KR, "start")

d.t(24, 616, "네 번째 전이는 되돌릴 수 있다 — touch /tmp/ready 를 다시 하면 세 번째 상태로 돌아온다.",
    12, MUTED, KR, "start")
d.t(24, 636, "readiness 도 정책도 들어오는 길만 건드린다. 어느 상태에서도 Pod 가 밖으로 나가는 길은 열려 있다.",
    12, MUTED, KR, "start")
d.legend(654, [("실행해서 값을 본 상태", INFO), ("지금 도달한 자리", ACC), ("아직 실행 전", SOFT)])
d.save("04-04.lab-state-progression.svg")
print("ok lab-state-progression")
