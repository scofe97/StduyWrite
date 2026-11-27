# -*- coding: utf-8 -*-
# 타입 스펙: type-sequence
"""istiod와 Envoy 사이의 xDS ACK/NACK 시퀀스 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO


def has_kr(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class KrSeq(Seq):
    """한글 라벨·서브라벨에 KR 스택을 쓰고, 메시지·상태 칩을 다룬다."""

    def lanes(s, names, y0=104, lane_w=200):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR if has_kr(nm) else MONO, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, KR if has_kr(sub) else MONO)
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, KR if has_kr(label) else MONO, "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, KR if has_kr(sub) else MONO, "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        size = 12
        w = sum(size if "가" <= ch <= "힣" else size * 0.62 for ch in str(txt)) + 18
        s.o.append(
            f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
            f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>'
        )
        s.t(x, y + 4, txt, size, c, KR if has_kr(txt) else MONO)


W, H = 880, 536

d = KrSeq(
    W,
    H,
    "XDS · ACK AND NACK SEQUENCE",
    "검증 통과 시 새 버전을 ACK 하고, 실패 시 이전 버전과 오류를 NACK 한다",
    "istiod 가 DiscoveryResponse(version_info=v2, nonce=n2) 를 보내면 Envoy 는 유효 시 v2 ACK 를, 무효 시 v1 과 error_detail 로 NACK 을 보내고 v1 설정을 유지한다",
    lead="response_nonce 로 응답을 짝짓고 NACK 뒤에도 스트림과 v1 설정을 유지한다",
)

lx = d.lanes([("istiod", "컨트롤 플레인"), ("Envoy", "데이터 플레인")], y0=104, lane_w=200)
d.rails(472)

# 1. 컨트롤 플레인 설정 푸시
d.msg(
    "istiod",
    "Envoy",
    "DiscoveryResponse(version_info=v2, nonce=n2)",
    192,
    c=INFO,
    mk="info",
    sub="새 설정 푸시",
)

# 2. ALT 분기 프레임 (ACK vs NACK)
fx, fy, fw, fh = 76, 232, 728, 232
d.o.append(
    f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="4" '
    f'fill="rgba(245,245,243,0.04)" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.o.append(
    f'<rect x="{fx}" y="{fy}" width="40" height="16" rx="2" '
    f'fill="{PAPER}" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.t(fx + 20, fy + 12, "ALT", 8, MUTED, MONO, "middle")

# 분기 1: 검증 통과 → ACK
d.t(140, 264, "[검증 통과]", 12, MUTED, KR, "start")
d.msg(
    "Envoy",
    "istiod",
    "DiscoveryRequest(version_info=v2, response_nonce=n2)",
    296,
    c=ACC,
    mk="acc",
    sub="ACK · 적용 의도 전달 (v2)",
)

# 분기 구분선
d.line(fx + 8, 336, fx + fw - 8, 336, "rgba(245,245,243,0.20)", 1.0, "4 3")

# 분기 2: 검증 실패 → NACK + v1 유지
d.t(140, 360, "[검증 실패]", 12, MUTED, KR, "start")
d.msg(
    "Envoy",
    "istiod",
    "DiscoveryRequest(version_info=v1, response_nonce=n2, error_detail)",
    396,
    c=BAD,
    mk="bad",
    dash="5 4",
    sub="NACK · 오류 보고, 스트림 유지",
)
d.state("Envoy", "설정 v1 유지", 440, OK)

d.legend(
    488,
    [
        ("설정 전달", INFO),
        ("ACK(정상)", ACC),
        ("NACK(거부)", BAD),
        ("기존 설정 유지", OK),
    ],
)

out = pathlib.Path(__file__).parent.parent / "xDS 동기화 프로토콜.ack-nack.svg"
d.save(out)
print(f"생성 완료: {out.name}")
