# -*- coding: utf-8 -*-
# 타입 스펙: type-sequence
"""Pod A 에서 Pod B 로 가는 East-West 트래픽의 iptables 가로채기·Envoy 2-hop 시퀀스 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO


def has_hangul(s):
    return any("가" <= ch <= "힣" for ch in str(s))


class KrSeq(Seq):
    """한글 라벨은 KR 13px 폰트, ASCII/식별자는 MONO 11px 폰트로 내보낸다."""

    def lanes(self, names, y0=104, lane_w=136):
        self.LX = {}
        # W=1000 에서 x=100..900 (간격 160px, 폭 136px, 좌우 여백 32px — 모두 4의 배수)
        x0 = 32 + lane_w // 2
        step = 160
        for i, (nm, sub) in enumerate(names):
            x = x0 + step * i
            self.LX[nm] = x
            self.box(x - lane_w // 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            sz = 13 if has_hangul(nm) else 12
            self.t(x, y0 + 20, nm, sz, INK, KR if has_hangul(nm) else MONO, "middle", 600)
            self.t(x, y0 + 38, sub, 11, MUTED, KR if has_hangul(sub) else MONO)
        self.lane_top = y0 + 48
        return self.LX

    def msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        lsz = 13 if has_hangul(label) else 11
        self.t(mx, y - 9, label, lsz, c, KR if has_hangul(label) else MONO, "middle", 600)
        if sub:
            ssz = 13 if has_hangul(sub) else 11
            self.t(mx, y + 17, sub, ssz, MUTED, KR if has_hangul(sub) else MONO)

    def state(self, a, txt, y, c):
        x = self.LX[a]
        is_kr = has_hangul(txt)
        fam = KR if is_kr else MONO
        sz = 13 if is_kr else 11
        w = int(sum(sz if "가" <= ch <= "힣" else sz * 0.62 for ch in str(txt)) + 16)
        w += (4 - w % 4) % 4
        self.o.append(
            f'<rect x="{x - w // 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
            f'fill="{PAPER}" stroke="{c}" stroke-width="1.1"/>'
        )
        self.t(x, y + 4, txt, sz, c, fam)


W, H = 1000, 520

d = KrSeq(
    W, H,
    "EAST-WEST · IPTABLES & SIDECAR 2-HOP",
    "Pod A 에서 Pod B 로 가는 트래픽 가로채기와 사이드카 2-hop 흐름",
    "Pod A 앱의 아웃바운드가 OUTPUT·ISTIO_OUTPUT 을 거쳐 Envoy A(15001)로 들어가고, "
    "UID 1337 RETURN 으로 빠져나와 Pod B 의 PREROUTING·ISTIO_INBOUND 를 거쳐 "
    "Envoy B(15006)와 127.0.0.6 RETURN 을 지나 Pod B 앱에 닿는 순서",
    lead="앱은 서비스 DNS 와 포트만 호출하고, 커널 iptables 규칙이 양쪽 Envoy(15001·15006)로 경로를 돌립니다",
)

lanes = [
    ("Pod A 앱", "UID != 1337"),
    ("A iptables", "nat OUTPUT"),
    ("Envoy A", "UID 1337 · :15001"),
    ("B iptables", "nat PREROUTING"),
    ("Envoy B", "UID 1337 · :15006"),
    ("Pod B 앱", ":8080"),
]
d.lanes(lanes, y0=104, lane_w=136)
d.rails(444)

# 요청 처리 중 Envoy A·B 활성 막대
d.box(d.LX["Envoy A"] - 4, 240, 8, 56, PAPER2, ACC, 0.9, 2)
d.box(d.LX["Envoy B"] - 4, 344, 8, 56, PAPER2, OK, 0.9, 2)

# 1. App A -> A iptables
d.msg("Pod A 앱", "A iptables", "TCP :8080", 192, INFO, "info", sub="ISTIO_OUTPUT")

# 2. A iptables -> Envoy A:15001
d.msg("A iptables", "Envoy A", "REDIRECT :15001", 244, INFO, "info", sub="ISTIO_REDIRECT")

# 3. Envoy A -> B iptables (mTLS; UID 1337 RETURN 으로 15001 재진입 방지)
d.msg("Envoy A", "B iptables", "mTLS → Pod B:8080", 296, ACC, "acc", sub="UID 1337 RETURN")

# 4. B iptables -> Envoy B:15006
d.msg("B iptables", "Envoy B", "REDIRECT :15006", 348, INFO, "info", sub="ISTIO_IN_REDIRECT")

# 5. Envoy B -> Pod B app (127.0.0.6 바인드 RETURN)
d.msg("Envoy B", "Pod B 앱", "127.0.0.6 → :8080", 400, OK, "ok", sub="127.0.0.6 RETURN")

# 예외 규칙 칩
d.state("A iptables", "1337 제외", 296, OK)
d.state("B iptables", "15090·15021 제외", 400, MUTED)

d.legend(468, [
    ("iptables 가로채기", INFO),
    ("mTLS · 프록시 전송", ACC),
    ("예외(RETURN) · 앱 전달", OK),
])

out = pathlib.Path(__file__).parent.parent / "사이드카 트래픽 가로채기·iptables 체인.east-west-flow.svg"
d.save(out)
print(f"생성 완료: {out.name}")
