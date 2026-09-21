# 05-01.stateful-identity — 이름은 남고 주소는 바뀐다
# 본문 요구: StatefulSet 이 주는 것은 재생성을 넘어 살아남는 *이름*이고, 그 이름이 어떤 주소로
#           풀리는지는 이름을 맡은 Service 의 종류가 정한다. headless(clusterIP: None) 이면
#           Pod 별 이름은 그 Pod IP 로, 서비스 이름은 대상 Pod IP 집합으로 풀린다.
#           일반 ClusterIP Service 의 이름은 Service 의 ClusterIP 하나로 풀린다.
#           근거: K8s DNS for Services and Pods — "Unlike normal Services, this resolves to the
#           set of IPs of all of the Pods selected by the Service."
# 타입 스펙: type-tree.md — 한 뿌리(이름)에서 조회 대상이 갈리고 각각 다른 답을 주는 구조가
#           이 절의 결론이라 갈래를 형태로 둔다. 05-01 의 다른 두 장(process · dp-security-matrix)과
#           겹치지 않는다.
# 좌표: 3단 x=118/400/772. 갈래는 y=228 / y=396 로 벌린다(stride 168).
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 596
d = D(W, H, "STATEFULSET · THE NAME STAYS, THE IP MAY NOT",
      "이름은 재생성을 넘어 남고 주소는 그때그때 풀린다",
      "StatefulSet 이 고정하는 것은 Pod 의 이름이고 IP 가 아니다. 그 이름이 무엇으로 풀리는지는 "
      "이름을 맡은 Service 가 headless 인지에 따라 갈린다.",
      lead="고정되는 것은 이름 · 주소는 조회 시점에 정해진다")
ddx.band(d, 104, 468, "무엇을 조회하느냐로 답이 갈린다")

def box(cx, cy, w, h, t1, t2, t3, c=None, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 18, ddx.fit(t1, 13, w - 18, t1), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(t2, 12, w - 16, t2), 12, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':·.-… ' for ch in t2) else KR)
    if t3: d.t(cx, cy + 26, ddx.fit(t3, 12, w - 14, t3), 12, SOFT, KR)

# 1단 — 뿌리: 고정되는 것
box(118, 312, 180, 108, "StatefulSet", "postgres · replicas 2", "고정 = 이름 postgres-0")
# 2단 — 이름을 맡는 자리
box(400, 312, 224, 108, "headless Service", "clusterIP: None", "spec.serviceName · 필수", focal=True)
d.path("M 212 312 L 284 312", MUTED, 1.5, m="ar")
d.t(248, 296, "이름 위임", 12, MUTED, KR)

# 3단 — 조회 대상별 답
box(772, 228, 384, 92, "Pod 별 이름", "postgres-0.postgres.default.svc…", "→ 그 Pod 의 현재 IP", OK)
box(772, 396, 384, 92, "서비스 이름", "postgres.default.svc.cluster.local", "→ 대상 Pod IP 집합", INFO)
d.path("M 516 288 L 552 288 L 552 228 L 576 228", OK, 1.5, m="ok")
d.path("M 516 336 L 552 336 L 552 396 L 576 396", INFO, 1.5, m="info")

# 대조 — 일반 ClusterIP 였다면
d.box(32, 484, 936, 64, PAPER, RULE, 0.9, 8)
d.t(52, 508, "일반 ClusterIP Service 였다면 · 이름은 Service 의 ClusterIP 하나로만 풀린다", 12, MUTED, KR, "start", 600)
d.t(52, 532, "Pod 별 레코드가 서지 않아 멤버를 지목할 수 없다", 12, SOFT, KR, "start")
d.legend(568, [("멤버를 지목", OK), ("전체 대상 집합", INFO), ("이름을 맡는 자리 · 필수", ACC)])
d.save("05-01.stateful-identity.svg"); print("ok stateful-identity")
