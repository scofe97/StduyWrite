# 05-01.stateful-identity — 이름이 어디서 갈라지는가
# 본문 요구: "`<Pod명>.<서비스명>.<네임스페이스>.svc.cluster.local` 이 개별 Pod 를, 서비스 이름이
#           서비스 주소를 돌려줍니다. Pod 별 레코드와 서비스 레코드가 공존하는 셈입니다 —
#           특정 멤버를 지목할지, 서비스 전체를 부를지를 클라이언트가 고를 수 있습니다."
#           그리고 "`spec.serviceName` 은 선택이 아니라 필수 필드"이고 그 서비스가
#           "headless(`clusterIP: None`) 여야" Pod 별 레코드가 생긴다는 것.
# 타입 스펙: type-tree.md — 한 뿌리에서 이름이 두 갈래로 갈리는 구조가 이 절의 결론이라
#           갈래를 형태로 둔다. 05-01 의 다른 두 장(process · dp-security-matrix)과 겹치지 않는다.
# 좌표: 3단 x=118/400/760. 갈래는 y=250(Pod 별)·y=410(서비스)로 벌린다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 1000, 572
d = D(W, H, "STATEFULSET · WHERE THE NAME FORKS",
      "이름은 headless Service 에서 두 갈래로 갈린다",
      "StatefulSet 이 준 ordinal 이 headless Service 를 지나면서 Pod 별 레코드와 서비스 레코드 "
      "두 갈래가 된다. 일반 ClusterIP 를 적으면 위 갈래가 아예 생기지 않는다.",
      lead="ordinal → headless Service → Pod 를 지목하는 이름과 서비스 전체를 부르는 이름")
ddx.band(d, 104, 504, "갈래가 둘이라 클라이언트가 고를 수 있다 — 지목할지, 전체를 부를지")

def box(cx, cy, w, h, t1, t2, t3, c=None, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 18, ddx.fit(t1, 13, w - 18, t1), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(t2, 11, w - 16, t2), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':·.- ' for ch in t2) else KR)
    if t3: d.t(cx, cy + 26, ddx.fit(t3, 11, w - 14, t3), 11, SOFT, KR)

# 1단 — 뿌리
box(118, 330, 180, 108, "StatefulSet", "postgres · replicas 2", "ordinal 0 · 1")
# 2단 — 이름을 만드는 자리
box(400, 330, 220, 108, "headless Service", "clusterIP: None", "spec.serviceName · 필수", focal=True)
d.path("M 212 330 L 286 330", MUTED, 1.5, m="ar")
d.t(249, 314, ddx.fit("이름을 맡긴다", 11, 74, "corridor"), 11, MUTED, KR)

# 3단 — 두 갈래
box(760, 240, 380, 96, "Pod 별 레코드", "postgres-0.postgres.default.svc…", "10.244.1.3 — 멤버를 지목한다", OK)
box(760, 420, 380, 96, "서비스 레코드", "postgres.default.svc.cluster.local", "10.105.214.153 — 전체를 부른다", INFO)
d.path("M 514 306 L 552 306 L 552 240 L 566 240", OK, 1.5, m="ok")
d.path("M 514 354 L 552 354 L 552 420 L 566 420", INFO, 1.5, m="info")

d.t(36, 484, "일반 ClusterIP 를 적으면 이름이 서비스 VIP 로만 풀려 위 갈래가 생기지 않는다 — "
             "Pod 별 정체성이 사라진다", 12, ACC, KR, "start")
d.legend(520, [("멤버를 지목하는 이름", OK), ("전체를 부르는 이름", INFO), ("없으면 위 갈래가 없다", ACC)])
d.save("05-01.stateful-identity.svg"); print("ok stateful-identity")
