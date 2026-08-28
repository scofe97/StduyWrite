# 13-02 §4 — 무엇을 건드리는가로 가른 여섯
# 짝 도식(filter-kinds-and-mirror-trap)이 '흐름 구조' 축을 맡으므로, 이쪽은 '무엇을 고치는가'
# 축만 본다. 두 도식이 같은 그림이 되지 않게 축을 확실히 갈라 둔다.
# 타입 스펙: type-nested.md — 두 상자가 필터를 나눠 담는다 — 포함 관계가 곧 분류다. 오가는 것을 고치는 쪽과 흐름 자체를
#           바꾸는 쪽이 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 600, "KUBERNETES IN ACTION · 13-02",
      "고치는 필터와 흐름을 바꾸는 필터",
      "여섯을 평면으로 나열하면 성격 차이가 안 보인다. 넷은 오가는 것을 고칠 뿐 흐름은 그대로 두고, "
      "둘은 흐름 자체를 바꾼다.",
      "rules.filters 에 넣는 여섯 가지")

def group(x0, w, label, items, c, focal):
    ddx.band(d, 100, 452, label, x=x0, w=w)
    for i, (nm, s) in enumerate(items):
        cy = 190 + i * 84
        bx = x0 + 28
        if focal:
            d.o.append(f'<rect x="{bx}" y="{cy-32}" width="{w-56}" height="64" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
        else:
            d.box(bx, cy - 32, w - 56, 64, PAPER2, c, 1.1, 6); tc = c
        d.t(bx + 20, cy - 6, nm, 12, tc, MONO, "start", 600)
        d.t(bx + 20, cy + 16, s, 11, MUTED, KR, "start")

group(24, 620, "오가는 것을 고친다 — 흐름은 하나 그대로", [
    ("RequestHeaderModifier", "요청 헤더를 add · set · remove"),
    ("ResponseHeaderModifier", "응답 헤더를 같은 방식으로"),
    ("URLRewrite", "백엔드가 기대하는 경로로 바꿔 보낸다"),
], INFO, False)
group(668, 488, "흐름 자체를 바꾼다", [
    ("RequestMirror", "복사본을 다른 백엔드에도 보낸다"),
    ("RequestRedirect", "백엔드에 안 가고 직접 응답한다"),
], ACC, True)
d.t(912, 400, "ExtensionRef 는 또 다른 축이다 —", 11, SOFT, KR)
d.t(912, 420, "설정을 HTTPRoute 밖에 두는 위임", 11, SOFT, KR)

d.t(24, 500, "ExtensionRef 와 RequestMirror 가 나머지와 결이 다른데 다른 축에서 다르다. "
             "ExtensionRef 는 설정을 어디 두는가가, RequestMirror 는 트래픽 흐름 구조가 다르다.",
     11, MUTED, KR, "start")
d.legend(536, [("고치는 필터", INFO), ("흐름을 바꾸는 필터", ACC)])
d.save("13-02-httproute-filters.svg")
print("ok")
