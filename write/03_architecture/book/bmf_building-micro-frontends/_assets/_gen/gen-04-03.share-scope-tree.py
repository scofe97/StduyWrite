# 04-03 §1 — shareScope 로 갈린 공유 자원. 저자가 개발자 도구에서 찍어 보인 출력 그대로다.
# window.__FEDERATION__.__SHARE__ 아래 조각 이름 · 스코프 · 라이브러리:버전 순으로 내려간다.
# 타입 스펙: type-tree — 뿌리 하나에서 갈라지는 단일 부모 계층. 되돌아오는 간선이 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1200
ROOT_W, NW, NH = 340, 250, 56
ROOT_Y, T1_Y, T2_Y = 104, 212, 320
T1 = [("HomeMFE", "React 17 을 쓰는 조각", 320), ("UserPaymentsMFE", "React 18 을 쓰는 조각", 880)]
T2 = [   # (부모 중심 x 대비 오프셋, 스코프, 내용, focal)
    (320 - 150, "default", "react-router-dom 6.21.3", False),
    (320 + 150, "react17", "react 17.0.2 · react-dom 17.0.2", True),
    (880, "default", "react 18.2.0 · react-dom 18.2.0", False),
]
LEGEND_Y = T2_Y + NH + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-03 §1",
      "shareScope 가 버전을 갈라 놓는다",
      "같은 페이지에서 React 17 과 18 이 부딪히지 않는 이유는 스코프가 다르기 때문이다. 색이 붙은 가지가 홈 조각이 따로 판 스코프다.",
      "window.__FEDERATION__.__SHARE__ 에서 이 트리를 그대로 볼 수 있습니다")

d.line(600, ROOT_Y + NH, 600, ROOT_Y + NH + 26, MUTED, 1.0)
d.line(T1[0][2], ROOT_Y + NH + 26, T1[1][2], ROOT_Y + NH + 26, MUTED, 1.0)
for _, _, cx in T1:
    d.line(cx, ROOT_Y + NH + 26, cx, T1_Y, MUTED, 1.0)
d.line(T2[0][0], T1_Y + NH + 26, T2[1][0], T1_Y + NH + 26, MUTED, 1.0)
d.line(T1[0][2], T1_Y + NH, T1[0][2], T1_Y + NH + 26, MUTED, 1.0)
for cx, *_ in T2[:2]:
    d.line(cx, T1_Y + NH + 26, cx, T2_Y, MUTED, 1.0)
d.line(T1[1][2], T1_Y + NH, T1[1][2], T2_Y, MUTED, 1.0)

d.box(600 - ROOT_W / 2, ROOT_Y, ROOT_W, NH, PAPER2, RULE, 1.0, 6)
d.t(600, ROOT_Y + 24, "__FEDERATION__.__SHARE__", 12.5, INK, MONO, "middle", 600)
d.t(600, ROOT_Y + 42, "브라우저에서 바로 들여다볼 수 있는 공유 자원", 9.5, MUTED, KR)

for name, sub, cx in T1:
    d.box(cx - NW / 2, T1_Y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(cx, T1_Y + 24, name, 12, INK, MONO, "middle", 600)
    d.t(cx, T1_Y + 42, sub, 9.5, MUTED, KR)

for cx, scope, body, focal in T2:
    if focal:
        d.tone(cx - NW / 2, T2_Y, NW, NH, ACC, 6, "14", 1.3)
        d.t(cx, T2_Y + 24, scope, 12, ACC, MONO, "middle", 600)
        d.t(cx, T2_Y + 42, body, 9.5, ACC, MONO)
    else:
        d.box(cx - NW / 2, T2_Y, NW, NH, f"{INK}08", MUTED, 0.8, 6)
        d.t(cx, T2_Y + 24, scope, 12, INK, MONO, "middle", 600)
        d.t(cx, T2_Y + 42, body, 9.5, MUTED, MONO)

d.legend(LEGEND_Y, [("홈 조각이 따로 판 스코프", ACC)])
d.save("04-03.share-scope-tree.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
