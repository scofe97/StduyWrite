# 04-03.networkpolicy-peer-and-or — 대시 하나의 위치
# 본문 요구: 「peer 넷과 AND·OR 함정」 — 대시 하나의 위치가 AND 를 OR 로 바꾼다. 아래 YAML 두 벌과 같은 값을 쓴다
#           (namespaceSelector team=store, podSelector app=frontend).
# 타입 스펙: type-dp-security-matrix.md 의 2 행 대조. 차이가 문법 한 글자라 YAML 을 그대로 보여 주는 것이 가장 정확하다.
#           2026-11-08 `{...}` 자리표시를 본문 YAML 의 실제 라벨로 바꿨다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 532
d = D(W, H, "NetworkPolicy peer · ONE DASH",
      "대시 하나의 위치가 AND 를 OR 로 바꾼다",
      "같은 셀렉터 둘이라도 한 항목에 있으면 team=store 네임스페이스 안의 app=frontend Pod 만 통과하는 교집합이고, "
      "별개 항목으로 갈리면 team=store 네임스페이스의 모든 Pod 와 정책 네임스페이스의 app=frontend Pod 가 통과하는 합집합이다.",
      lead="한 항목에 있으면 교집합, 별개 항목으로 갈리면 합집합")

Y0, RH, GAP = 156, 124, 16
YX, YW = 44, 470
MX, MW = 534, 422

def row(r, tag, yaml_lines, meaning, sub, c, focal=False):
    y = Y0 + 24 + r * (RH + GAP)
    d.o.append(f'<rect x="{YX}" y="{y}" width="{YW}" height="{RH}" rx="6" fill="{PAPER2}" '
               f'stroke="{c}" stroke-width="1.2"/>')
    d.t(YX + 20, y + 30, tag, 12, c, KR, "start", 600)
    for i, ln in enumerate(yaml_lines):
        hot = ln.lstrip().startswith("-")
        d.t(YX + 24, y + 62 + i * 24, ddx.fit(ln, 12, YW - 40, ln), 12, c if hot else MUTED, MONO, "start", 600 if hot else 400)
    d.o.append(f'<rect x="{MX}" y="{y}" width="{MW}" height="{RH}" rx="6" '
               f'fill="{c}{"12" if focal else "0A"}" stroke="{c}" stroke-width="{1.6 if focal else 1.2}"/>')
    d.t(MX + MW // 2, y + 62, meaning, 17, c, KR, "middle", 600)
    d.t(MX + MW // 2, y + 96, ddx.fit(sub, 12, MW - 24, sub), 12, MUTED, KR)

ddx.band(d, 104, 468, "같은 셀렉터 · 대시 위치가 범위를 가름")
d.t(YX + YW // 2, Y0, "쓴 대로의 YAML", 12, SOFT, KR, "middle", 600)
d.t(MX + MW // 2, Y0, "그래서 누가 통과하나", 12, SOFT, KR, "middle", 600)

row(0, "AND — 대시 하나", ["- namespaceSelector: team=store", "  podSelector: app=frontend"],
    "교집합 — 좁게", "team=store 안의 app=frontend 만 통과", OK)
row(1, "OR — 대시 둘", ["- namespaceSelector: team=store", "- podSelector: app=frontend"],
    "합집합 — 넓게", "team=store 의 모든 Pod 와 내 네임스페이스의 frontend", BAD, focal=True)

d.legend(484, [("교집합 — 의도한 범위", OK), ("합집합 — 넓어진 범위", BAD)])
d.save("04-03.networkpolicy-peer-and-or.svg")
print("ok networkpolicy-peer-and-or")
