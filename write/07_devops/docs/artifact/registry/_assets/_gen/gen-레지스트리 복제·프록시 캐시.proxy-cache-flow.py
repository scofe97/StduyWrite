# -*- coding: utf-8 -*-
# 타입 스펙: type-sequence
"""Harbor Proxy Cache 의 캐시 히트·미스·업스트림 단절·push 거부 동작 시퀀스."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO


def has_kr(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class ProxySeq(Seq):
    def lanes(s, names, y0=104, lane_w=204):
        s.LX = {}
        centers = [160, 480, 800]
        for x, (nm, sub) in zip(centers, names):
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR if has_kr(nm) else MONO, "middle", 600)
            s.t(x, y0 + 38, sub, 13, MUTED, KR if has_kr(sub) else MONO)
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 12 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) // 2
        s.t(mx, y - 9, label, 13, c, KR if has_kr(label) else MONO, "middle", 600)
        if sub:
            s.t(mx, y + 16, sub, 13, MUTED, KR if has_kr(sub) else MONO, "middle")

    def group(s, y, h, tag, cond, c=RULE):
        s.o.append(
            f'<rect x="36" y="{y}" width="888" height="{h}" rx="4" '
            f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9"/>'
        )
        tw = len(tag) * 9 + 20
        s.o.append(f'<rect x="36" y="{y}" width="{tw}" height="18" rx="2" fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
        s.t(36 + tw // 2, y + 13, tag, 10, c, MONO, "middle", 600)
        s.t(44 + tw, y + 14, cond, 13, MUTED, KR, "start")


W, H = 960, 756

d = ProxySeq(
    W,
    H,
    "DEVOPS · HARBOR · PROXY CACHE FLOW",
    "Harbor Proxy Cache 의 pull 판정과 push 차단 순서",
    "캐시 미스 때는 업스트림에서 이미지를 내려받아 저장하고, 캐시 히트 때는 HEAD 요청으로 변경 여부만 확인해 rate limit 소모를 피하며, 업스트림 단절 시에는 캐시본을 반환한다",
    lead="HEAD 확인은 Docker Hub pull 횟수를 소모하지 않으며, 직접 push 는 차단됩니다",
)

d.lanes(
    [
        ("클라이언트", "docker / containerd"),
        ("Harbor Proxy Cache", "프록시 프로젝트"),
        ("업스트림 레지스트리", "Docker Hub · ECR"),
    ],
    y0=104,
    lane_w=204,
)

C, HPR, UP = "클라이언트", "Harbor Proxy Cache", "업스트림 레지스트리"

d.group(164, 152, "CASE 1", "캐시 미스 — 첫 pull 요청", INFO)
d.group(328, 152, "CASE 2", "캐시 히트 — 변경 없을 때", ACC)
d.group(492, 108, "CASE 3", "업스트림 단절 (unreachable)", WARN)
d.group(612, 88, "CASE 4", "Proxy Cache 직접 push 시도", BAD)

d.rails(700)

# CASE 1
d.msg(C, HPR, "pull proxy-proj/app:1.0", 204, INFO, "info")
d.msg(HPR, UP, "GET manifest + layers", 232, INFO, "info")
d.msg(UP, HPR, "200 이미지 저장", 264, OK, "ok", dash="5 4")
d.msg(HPR, C, "캐시 후 이미지 반환", 296, OK, "ok", dash="5 4")

# CASE 2
d.msg(C, HPR, "pull proxy-proj/app:1.0", 368, MUTED, "ar")
d.msg(HPR, UP, "HEAD manifest 확인", 396, ACC, "acc", sub="Docker Hub pull 미소모")
d.msg(UP, HPR, "동일 digest 확인", 436, OK, "ok", dash="5 4")
d.msg(HPR, C, "로컬 캐시 즉시 반환", 464, OK, "ok", dash="5 4")

# CASE 3
d.msg(C, HPR, "pull proxy-proj/app:1.0", 532, MUTED, "ar")
d.msg(HPR, UP, "HEAD 연결 실패", 556, WARN, "warn", dash="5 4")
d.msg(HPR, C, "기존 캐시 이미지 반환", 584, OK, "ok", dash="5 4")

# CASE 4
d.msg(C, HPR, "push proxy-proj/app:1.0", 652, BAD, "bad")
d.msg(HPR, C, "거부 (읽기 전용 프로젝트)", 680, BAD, "bad", dash="5 4")

d.legend(
    H - 44,
    [
        ("최초 pull", INFO),
        ("HEAD 확인", ACC),
        ("캐시 반환", OK),
        ("업스트림 단절", WARN),
        ("push 거부", BAD),
    ],
)

out = pathlib.Path(__file__).resolve().parent.parent / "레지스트리 복제·프록시 캐시.proxy-cache-flow.svg"
d.save(str(out))
print("ok gen-proxy-cache-flow")
