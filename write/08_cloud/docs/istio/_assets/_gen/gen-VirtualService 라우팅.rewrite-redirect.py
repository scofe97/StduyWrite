# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""rewrite 와 redirect 의 요청 경로 비교 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460

d = D(
    W, H,
    "VIRTUALSERVICE · REWRITE VS REDIRECT",
    "rewrite 는 프록시 안에서, redirect 는 클라이언트를 거쳐 경로를 바꾼다",
    "rewrite 는 요청을 한 번만 보내고 프록시가 경로를 바꿔 백엔드에 전달하며, redirect 는 301 응답으로 클라이언트가 새 주소로 다시 요청한다",
    lead="클라이언트가 바뀐 주소를 보는지가 둘을 가른다"
)


def zone(x, y, w, h, label, c=RULE):
    d.o.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
        f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>'
    )
    lw = len(label) * 11 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 17, label, 12, SOFT, KR, "middle")


def node(x, y, w, title, sub, c=None):
    if c:
        d.tone(x, y, w, 68, c, 6, "14", 1.2)
    else:
        d.box(x, y, w, 68, PAPER, INFO, 1.0, 6)
    d.t(x + w // 2, y + 28, title, 12, c or INK, KR, "middle", 600)
    d.t(x + w // 2, y + 50, sub, 11, MUTED, KR, "middle")


# 상단: rewrite
zone(32, 96, 896, 140, "rewrite: 요청은 한 번, 경로는 프록시가 바꾼다", OK)
node(64, 136, 140, "클라이언트", "주소는 그대로", None)
node(400, 136, 150, "Envoy 프록시", "rewrite.uri", OK)
node(764, 136, 140, "백엔드", "바뀐 경로를 받음", None)
d.arrow([(204, 170), (400, 170)], INFO, "info", 1.2)
d.t(302, 160, "GET /ratings/1", 11, INFO, MONO, "middle")
d.arrow([(550, 170), (764, 170)], OK, "ok", 1.5)
d.t(657, 160, "GET /v1/bookRatings/1", 11, OK, MONO, "middle")

# 하단: redirect
zone(32, 256, 896, 190, "redirect: 301 을 받은 클라이언트가 다시 요청한다", ACC)
node(64, 296, 140, "클라이언트", "요청을 두 번 보냄", None)
node(400, 296, 150, "Envoy 프록시", "redirect", ACC)
node(764, 296, 140, "foo.example.com", "새 주소", None)
d.arrow([(204, 318), (400, 318)], INFO, "info", 1.2)
d.t(302, 308, "GET example.com/foo/bar", 11, INFO, MONO, "middle")
d.arrow([(400, 348), (204, 348)], ACC, "acc", 1.4)
d.t(302, 366, "301 foo.example.com/bar", 11, ACC, MONO, "middle")
d.arrow([(134, 364), (134, 414), (834, 414), (834, 364)], INFO, "info", 1.2)
d.t(484, 404, "GET foo.example.com/bar", 11, INFO, MONO, "middle")

d.save(pathlib.Path(__file__).parent.parent / "VirtualService 라우팅.rewrite-redirect.svg")
print("생성 완료: VirtualService 라우팅.rewrite-redirect.svg")
