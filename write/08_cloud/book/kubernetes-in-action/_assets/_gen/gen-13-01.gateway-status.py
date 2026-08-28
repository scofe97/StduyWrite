# 13-01 §5 — 누가 채우는지가 갈린다
# 캡션이 "채워 가는 순서"와 "attachedRoutes 만 Route 가 채운다"를 함께 요구한다. 그러니 단계
# 순서 위에 채우는 주체를 표시해야 하고, 주체가 다른 마지막 칸이 focal 이다.
# 타입 스펙: type-data-flow.md — status 의 칸이 순서대로 채워지는 파이프라인. 단계 머리가 그 칸을 *누가* 채우는지를 맡고,
#           마지막 한 칸만 다른 주체(Route 오브젝트)가 채운다는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 600, "KUBERNETES IN ACTION · 13-01",
      "마지막 한 칸만 다른 주체가 채운다",
      "apply 한 직후에는 spec 만 있고 status 는 비어 있다. 컨트롤러가 위에서부터 채워 나가지만, "
      "attachedRoutes 는 Route 오브젝트가 이 Gateway 를 참조해야 비로소 오른다.",
      "kubectl apply -f gateway.yaml 직후부터")

STEP = [("status 가 비어 있다", "spec 만 있다", "—", None),
        ("addresses", "닿을 수 있는 주소", "컨트롤러", None),
        ("conditions", "Accepted · Programmed", "컨트롤러", None),
        ("listeners", "supportedKinds · conditions", "컨트롤러", None),
        ("attachedRoutes", "붙은 Route 수", "Route 오브젝트", ACC)]
BW, GP = 216, 26
X0 = (1240 - (5 * BW + 4 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]
for cx, (t, s, who, c) in zip(CX, STEP):
    d.t(cx, 168, who, 10, ACC if c is ACC else SOFT, KR)
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="188" width="{BW}" height="88" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(cx - BW // 2, 188, BW, 88, PAPER2, RULE, 1.1, 6); tc = INK
    d.t(cx, 222, ddx.fit(t, 13, BW - 18, t), 13, tc, KR if any('가' <= ch <= '힣' for ch in t) else MONO,
        "middle", 600)
    d.t(cx, 248, ddx.fit(s, 11, BW - 16, s), 11, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 232 L {b-BW//2-9} 232", MUTED, 1.5, m="ar")

d.t(CX[4], 310, "컨트롤러가 채우지 못한다", 11, ACC, KR)
d.t(CX[4], 332, "Route 를 안 만들었으면 0 이다", 11, ACC, KR)
d.t(CX[4], 366, "그리고 접속하면 404 가 난다", 11, ACC, KR)

d.t(24, 440, "conditions 에서 먼저 볼 것은 Accepted(게이트웨이가 받아들였는가)와 "
             "Programmed(설정이 생성돼 접근 가능해질지)다. Ready 는 예약이고 Scheduled 는 deprecated 다.",
     11, MUTED, KR, "start")
d.t(24, 462, "listener 의 conditions 다섯 중 ResolvedRefs 가 12-02 의 아픈 곳을 덮는다 — "
             "TLS Secret 이름을 잘못 적으면 접속이 아니라 배포 시점 status 에 False 로 남는다.",
     11, MUTED, KR, "start")
d.legend(500, [("Route 가 채운다", ACC)])
d.save("13-01-gateway-status.svg")
print("ok")
