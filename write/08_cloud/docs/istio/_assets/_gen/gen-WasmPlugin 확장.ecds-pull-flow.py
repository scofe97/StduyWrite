# -*- coding: utf-8 -*-
# 타입 스펙: type-sequence
"""WasmPlugin ECDS 설정 전달, istio-agent 모듈 pull·캐시, Envoy AUTHN 로드 흐름 시퀀스.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO


def has_kr(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class WasmSeq(Seq):
    """4개 레인을 4px 격자로 고정하고 한글·영문 폰트 스택을 갈라 쓴다."""

    def lanes(s, names, y0=104, lane_w=176):
        s.LX = {}
        centers = [112, 352, 592, 832]
        for x, (nm, sub) in zip(centers, names):
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR if has_kr(nm) else MONO, "middle", 600)
            s.t(x, y0 + 38, sub, 13, MUTED, KR if has_kr(sub) else MONO)
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, label_x=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 12 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = label_x if label_x is not None else (x1 + x2) // 2
        s.t(mx, y - 10, label, 13, c, KR if has_kr(label) else MONO, "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 13, MUTED, KR if has_kr(sub) else MONO, "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        size = 13
        w = round(sum(size if "가" <= ch <= "힣" else size * 0.62 for ch in str(txt)) + 20)
        w = (w + 3) // 4 * 4
        s.o.append(
            f'<rect x="{x - w // 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
            f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>'
        )
        s.t(x, y + 4, txt, size, c, KR if has_kr(txt) else MONO)


W, H = 960, 632

d = WasmSeq(
    W,
    H,
    "ISTIO · WASMPLUGIN ECDS FLOW",
    "istiod 가 ECDS 로 내리고 istio-agent 가 받아 캐시한다",
    "istiod 가 WasmPlugin 을 ECDS 설정으로 보내면 istio-agent 가 OCI 레지스트리에서 모듈을 pull 해 로컬 캐시에 둔 뒤 경로를 치환해 Envoy AUTHN 자리에 싣고, 실패 시에는 failStrategy 에 따라 allow 또는 deny RBAC 대체 필터를 싣는다",
    lead="원격 url 을 로컬 경로로 바꾼 뒤 Envoy HTTP 필터 체인의 AUTHN 자리에 로드한다",
)

d.lanes(
    [
        ("istiod", "컨트롤 플레인"),
        ("istio-agent", "xDS 프록시·캐시"),
        ("OCI 레지스트리", "모듈 저장소"),
        ("Envoy", "데이터 플레인"),
    ],
    y0=104,
    lane_w=176,
)
d.rails(564)

# 1. ECDS 설정 푸시
d.msg(
    "istiod",
    "istio-agent",
    "ECDS 설정 푸시",
    192,
    c=INFO,
    mk="info",
    sub="phase: AUTHN · oci://",
)

# 2. OCI 모듈 pull 및 캐시 적재
d.msg(
    "istio-agent",
    "OCI 레지스트리",
    "Wasm 모듈 pull",
    244,
    c=INFO,
    mk="info",
    sub="imagePullPolicy · sha256",
)
d.msg(
    "OCI 레지스트리",
    "istio-agent",
    ".wasm 바이너리 반환",
    296,
    c=MUTED,
    mk="ar",
    dash="5 4",
    sub="로컬 캐시 적재",
)

# 3. ALT 분기 프레임 (성공 vs fetch/검증 실패)
fx, fy, fw, fh = 64, 332, 864, 224
d.o.append(
    f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="4" '
    f'fill="rgba(245,245,243,0.04)" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.o.append(
    f'<rect x="{fx}" y="{fy}" width="40" height="16" rx="2" '
    f'fill="{PAPER}" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.t(fx + 20, fy + 12, "ALT", 8, MUTED, MONO, "middle")

# 분기 1: pull·검증 성공
d.t(128, 356, "[pull·검증 성공]", 13, MUTED, KR, "start")
d.msg(
    "istio-agent",
    "Envoy",
    "ECDS 전달 (file://)",
    384,
    c=ACC,
    mk="acc",
    sub="로컬 경로 치환",
    label_x=712,
)
d.state("Envoy", "AUTHN 자리 로드", 420, OK)

# 분기 구분선
d.line(fx + 8, 440, fx + fw - 8, 440, "rgba(245,245,243,0.20)", 1.0, "4 3")

# 분기 2: pull·검증 실패
d.t(128, 460, "[pull·검증 실패]", 13, MUTED, KR, "start")
d.msg(
    "istio-agent",
    "Envoy",
    "ECDS 전달 (RBAC 대체)",
    492,
    c=BAD,
    mk="bad",
    dash="5 4",
    sub="FAIL_OPEN 만 allow",
    label_x=712,
)
d.state("Envoy", "allow·deny 필터", 528, WARN)

d.legend(
    580,
    [
        ("설정·요청", INFO),
        ("ECDS 전달", ACC),
        ("필터 로드", OK),
        ("실패 시 대체 전달", BAD),
        ("대체 필터", WARN),
    ],
)

out = pathlib.Path(__file__).parent.parent / "WasmPlugin 확장.ecds-pull-flow.svg"
d.save(out)
print(f"생성 완료: {out.name}")
