# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""기본 동작과 두 해법의 시작·종료 순서 비교 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 560

d = D(
    W, H,
    "SIDECAR · START AND STOP ORDER",
    "기본은 동시에 시작하고, 두 해법은 순서를 정한다",
    "기본 동작은 앱이 프록시보다 먼저 요청을 보내 실패할 수 있고, holdApplicationUntilProxyStarts 는 시작만, 네이티브 사이드카는 시작과 종료 순서를 모두 맞춘다",
    lead="어디까지 순서를 보장하느냐가 세 가지를 가른다"
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


# 1. 기본
zone(32, 96, 896, 110, "기본: 컨테이너가 거의 동시에 시작한다", BAD)
node(64, 126, 200, "istio-proxy 시작", "아직 준비 안 됨", WARN)
node(380, 126, 200, "앱 시작", "바로 아웃바운드 요청", None)
node(696, 126, 200, "요청 실패", "CrashLoopBackOff 가능", BAD)
d.arrow([(264, 160), (380, 160)], INFO, "info", 1.2)
d.arrow([(580, 160), (696, 160)], BAD, "bad", 1.4)

# 2. hold
zone(32, 226, 896, 110, "holdApplicationUntilProxyStarts: 시작만 미룬다", ACC)
node(64, 256, 200, "istio-proxy 준비", "트래픽을 받을 수 있음", OK)
node(380, 256, 200, "앱 시작", "훅이 준비될 때까지 미룸", ACC)
node(696, 256, 200, "종료·Job·init", "순서 보장 없음", None)
d.arrow([(264, 290), (380, 290)], OK, "ok", 1.5)
d.arrow([(580, 290), (696, 290)], INFO, "info", 1.0)

# 3. 네이티브
zone(32, 356, 896, 180, "네이티브 사이드카: Kubernetes 가 시작과 종료를 맞춘다", OK)
node(64, 386, 190, "proxy 시작", "사이드카가 먼저", OK)
node(298, 386, 190, "앱 시작", "proxy 가 started 된 뒤", None)
node(532, 386, 190, "앱 종료", "주 컨테이너가 먼저", None)
node(766, 386, 130, "proxy 종료", "앱이 멈춘 뒤", OK)
d.arrow([(254, 420), (298, 420)], OK, "ok", 1.5)
d.arrow([(488, 420), (532, 420)], INFO, "info", 1.0)
d.arrow([(722, 420), (766, 420)], OK, "ok", 1.5)
d.t(480, 500, "init 컨테이너도 proxy 뒤에 돌고, Job 은 앱이 끝나면 파드가 끝난다", 12, SOFT, KR, "middle")

d.save(pathlib.Path(__file__).parent.parent / "사이드카 시동·종료 순서.startup-order.svg")
print("생성 완료: 사이드카 시동·종료 순서.startup-order.svg")
