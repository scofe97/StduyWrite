# 13-03 §3 — 다른 층 이야기다
# "네임스페이스가 달라도 통신은 되잖아"라는 반문이 출발점이라, 같은 두 네임스페이스를 두 층으로
# 겹쳐 놓고 한 층은 뚫려 있고 한 층은 막혀 있음을 보인다. 막힌 자리가 focal.
# 타입 스펙: type-layers.md — 네트워크 층과 오브젝트 층을 위아래로 놓고 대조한다 — 파드끼리는 통하는데 오브젝트 참조는
#           막힌다는 것이 두 층을 나눈 이유다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 656, "KUBERNETES IN ACTION · 13-03",
      "통신은 되는데 참조는 막힌다",
      "트래픽이 안 흐르는 이유는 네트워크가 막혀서가 아니라 참조 권한이 없어서다. "
      "두 사실이 층이 달라 서로를 설명해 주지 않는다.",
      "kiada 네임스페이스와 service-namespace 사이")

def layer(y0, label, left, right, arrow_c, verdict, verdict_c, focal, why):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1132)
    cy = y0 + 112
    for x0, (t, s) in ((110, left), (700, right)):
        d.box(x0, cy - 66, 370, 132, PAPER, RULE, 0.9, 8)
        d.t(x0 + 185, cy - 42, s, 11, SOFT, KR)
        if focal and x0 == 700:
            d.o.append(f'<rect x="{x0+95}" y="{cy-24}" width="180" height="62" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x0 + 185, cy + 2, t, 12, ACC, KR, "middle", 600)
        else:
            ddx.node(d, x0 + 185, cy + 6, t, "", 180, 62, OK if not focal else INFO)
    if focal:
        d.path(f"M 484 {cy+6} L 640 {cy+6}", BAD, 1.5, m="bad", dash="6 5")
        d.line(562, cy - 14, 562, cy + 26, BAD, 2.0)
    else:
        d.path(f"M 484 {cy+6} L 690 {cy+6}", OK, 1.5, m="ok")
    d.t(587, cy + 52, verdict, 11, verdict_c, KR)
    d.t(587, y0 + 190, why, 11, SOFT, KR)

layer(100, "네트워크 층 — 파드 사이", ("파드 A", "kiada"), ("파드 B", "service-namespace"),
      OK, "그냥 된다", OK, False, "11-01 의 flat 네트워크 — FQDN 으로 부르면 닿는다")
layer(340, "오브젝트 층 — 선언 사이", ("HTTPRoute", "kiada"), ("Service", "service-namespace"),
      BAD, "기본은 막힌다", BAD, True, "backendRefs 에 적어도 ResolvedRefs 가 RefNotPermitted 로 False")

d.t(24, 582, "안 막으면 아무 네임스페이스에서 남의 팀 내부 전용 서비스를 backendRefs 에 적어 외부로 노출할 수 있다 — "
             "그리고 소유자는 그 사실을 모른다.", 11, MUTED, KR, "start")
d.legend(608, [("뚫려 있다", OK), ("막혀 있다", BAD), ("허가가 필요한 쪽", ACC)])
d.save("13-03-network-vs-reference-layers.svg")
print("ok")
