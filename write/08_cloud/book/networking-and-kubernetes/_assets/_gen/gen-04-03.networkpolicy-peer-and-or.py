# 04-03.networkpolicy-peer-and-or — 대시 하나의 위치
# 본문 요구: "대시 하나의 위치가 AND 를 OR 로 바꾼다" — 실무 사고 1순위
# 타입 스펙: type-dp-security-matrix.md 의 2 행 대조. 차이가 문법 한 글자라
#           YAML 을 그대로 보여 주는 것이 어떤 도식보다 정확하다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 584
d = D(W, H, "NetworkPolicy peer · ONE DASH",
      "대시 하나의 위치가 AND 를 OR 로 바꾼다",
      "같은 셀렉터 둘이라도 한 항목에 있으면 교집합, 별개 항목으로 갈리면 합집합이다.",
      lead="한 항목에 있으면 교집합, 별개 항목으로 갈리면 합집합")

Y0, RH, GAP = 208, 124, 16
YX, YW = 44, 470
MX, MW = 534, 422

def row(r, tag, yaml_lines, meaning, sub, c, focal=False):
    y = Y0 + 24 + r * (RH + GAP)
    d.o.append(f'<rect x="{YX}" y="{y}" width="{YW}" height="{RH}" rx="6" fill="{PAPER2}" '
               f'stroke="{c}" stroke-width="1.2"/>')
    d.t(YX + 20, y + 30, tag, 12, c, KR, "start", 600)
    for i, ln in enumerate(yaml_lines):
        hot = ln.lstrip().startswith("-")
        d.t(YX + 24, y + 62 + i * 24, ln, 12, c if hot else MUTED, MONO, "start", 600 if hot else 400)
    d.o.append(f'<rect x="{MX}" y="{y}" width="{MW}" height="{RH}" rx="6" '
               f'fill="{c}{"12" if focal else "0A"}" stroke="{c}" stroke-width="{1.6 if focal else 1.2}"/>')
    d.t(MX + MW // 2, y + 62, meaning, 17, c, KR, "middle", 600)
    d.t(MX + MW // 2, y + 96, sub, 12, MUTED, KR)

ddx.band(d, 104, 520, "같은 셀렉터 · 대시 위치가 범위를 가름")
d.t(YX + YW // 2, Y0, "쓴 대로의 YAML", 12, SOFT, KR, "middle", 600)
d.t(MX + MW // 2, Y0, "그래서 누가 통과하나", 12, SOFT, KR, "middle", 600)

row(0, "AND — 대시 하나", ["- namespaceSelector: {...}", "  podSelector: {...}"],
    "교집합 — 좁게", "두 조건 모두 만족 시 통과 · 의도한 최소 권한", OK)
row(1, "OR — 대시 둘", ["- namespaceSelector: {...}", "- podSelector: {...}"],
    "합집합 — 넓게", "한 조건 충족 시 통과 · 실무 사고 1순위", BAD, focal=True)

d.legend(536, [("교집합 — 의도한 범위", OK), ("합집합 — 넓어진 범위", BAD)])
d.save("04-03.networkpolicy-peer-and-or.svg")
print("ok networkpolicy-peer-and-or")
