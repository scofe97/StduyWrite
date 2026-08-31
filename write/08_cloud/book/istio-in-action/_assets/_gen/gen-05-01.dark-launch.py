# 05-01 §2 헤더 하나로 갈리는 경로 — VirtualService 의 판단 순서.
# 본문: "첫 규칙의 매칭이 되면 v2, 안 되면 두 번째 규칙인 v1. 색이 붙은 가지가 새 버전으로 가는 유일한 길."
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 타원(시작·끝) · 마름모(판단) · 사각형(행동). 예=오른쪽, 아니오=아래.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 468
d = D(W, H, "ISTIO IN ACTION · 05-01 §2",
      "헤더 하나로 갈리는 경로",
      "catalog 로 가는 요청을 VirtualService 가 순서대로 판단한다. x-istio-cohort 헤더가 정확히 internal 이면 subset version-v2 로, 아니면 두 번째 규칙인 version-v1 로 간다.",
      "게이트웨이에서도, gateways: mesh 로 webapp 의 사이드카에서도 같은 판단입니다")

CX = 240
# 시작 타원
d.o.append(f'<rect x="{CX - 100}" y="104" width="200" height="40" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, 129, "catalog 로 가는 요청", 12, INK, KR, "middle", 600)
d.path(f"M {CX} 144 V 174", MUTED, 1.4, m="ar")
# 판단 마름모
dy, hw, hh = 236, 150, 60
d.o.append(f'<polygon points="{CX},{dy - hh} {CX + hw},{dy} {CX},{dy + hh} {CX - hw},{dy}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, dy - 6, "x-istio-cohort", 12, INK, MONO, "middle", 600)
d.t(CX, dy + 14, "exact: internal ?", 12, INK, MONO)
# 예 → 오른쪽 (초점 가지)
d.path(f"M {CX + hw} {dy} H 548", ACC, 1.6, m="acc")
d.t((CX + hw + 548) / 2, dy - 10, "예 — 첫 규칙 매칭", 12, ACC, KR)
d.o.append(f'<rect x="552" y="{dy - 28}" width="240" height="56" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(672, dy - 6, "subset: version-v2", 12, ACC, MONO, "middle", 600)
d.t(672, dy + 14, "새 버전 — 헤더를 넣은 사람만", 12, ACC, KR)
# 아니오 → 아래
d.path(f"M {CX} {dy + hh} V 340", MUTED, 1.4, m="ar")
d.t(CX + 12, 322, "아니오 — 두 번째 규칙", 12, MUTED, KR, "start")
d.box(CX - 120, 344, 240, 56, PAPER2, RULE, 1.0, 6)
d.t(CX, 366, "subset: version-v1", 12, INK, MONO, "middle", 600)
d.t(CX, 386, "검증된 버전 — 나머지 전부", 12, MUTED, KR)
# 판단의 근거 — DestinationRule 이 라벨을 subset 으로 이름 붙인다
d.t(672, 344, "subset 은 DestinationRule 이", 12, SOFT, KR)
d.t(672, 362, "version: v1 / v2 라벨에 붙인 이름", 12, SOFT, KR)
d.legend(412, [("새 버전으로 가는 유일한 길", ACC)])
d.save("05-01.dark-launch.svg")
