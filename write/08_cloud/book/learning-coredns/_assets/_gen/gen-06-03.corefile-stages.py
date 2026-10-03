# 06-03 §6 — 원서의 개선 Corefile 1단계와 2단계를 줄 단위로 맞대어, 무엇을 왜 뺐는지 보인다.
# 본문 근거: 이 노트 §6 의 두 Corefile 코드 블록과 「두 번째 단계」 산문. upstream 의 현재 오류는
#            plugin/kubernetes/setup.go(upstream 분기 없음, unknown property)와 1.7.0 릴리스 노트로 확인(2026-10-03).
#            둘째 블록의 prometheus 는 2단계에서 빠지는데 원서가 이유를 적지 않는다(코드 블록 대조).
# 타입 스펙: type-dp-security-matrix — 줄(행) × 단계(열) 격자에서 칸이 있음·뺌·추가 중 무엇인지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING COREDNS · 06-03 §6",
      "두 단계에 걸쳐 무엇을 뺐나",
      "1단계는 클러스터 존을 블록 앞으로 옮겨 캐시를 떼고, 2단계는 첫 블록에서 폐기된 레코드와 중복된 줄을 더 뺀다. "
      "upstream 은 원서 시점에 중복이었지만 지금은 남겨 두면 서버가 뜨지 않는다.",
      "주황 줄은 지금 CoreDNS 에서 오류가 납니다")

COLS = [(20, 300, "줄"), (330, 110, "1단계"), (450, 110, "2단계"), (570, 290, "왜")]
first = [
    ("errors", "있음", "있음", ""),
    ("health", "있음", "있음", "1.5.0 부터 전역"),
    ("kubernetes · pods insecure", "있음", "뺌", "파드 레코드 폐기"),
    ("kubernetes · upstream", "있음", "뺌", "1.4 부터 기본 · 지금은 오류"),
    ("kubernetes · fallthrough", "있음", "뺌", "CIDR 을 열거할 수 있으면"),
    ("ready", "없음", "추가", "API 캐시가 차면 준비"),
    ("prometheus :9153", "있음", "있음", ""),
    ("forward . UPSTREAM", "있음", "뺌", "CIDR 을 열거할 수 있으면"),
    ("loop · reload · loadbalance", "있음", "있음", ""),
]
second = [
    ("errors · forward · cache · loop", "있음", "있음", ""),
    ("prometheus :9153", "있음", "뺌", "원서 설명 없음"),
]
PITCH, RH = 34, 30


def colour(v):
    return {"뺌": BAD, "추가": OK}.get(v, MUTED)


def rows(items, y0):
    for i, (line, s1, s2, why) in enumerate(items):
        y = y0 + i * PITCH
        focal = "upstream" in line
        if focal:
            d.tone(16, y - 2, 848, RH + 4, ACC, 6, "14", 1.4)
        for x, w, _ in COLS:
            if not focal:
                d.box(x, y, w, RH, PAPER2, RULE, 0.8, 4)
        d.t(32, y + 20, line, 13, ACC if focal else INK, MONO, "start", 600)
        d.t(385, y + 20, s1, 12, colour(s1), KR)
        d.t(505, y + 20, s2, 12, colour(s2), KR, "middle", 600)
        if why:
            d.t(582, y + 20, why, 12, MUTED, KR, "start")


for x, w, head in COLS:
    d.t(x + 12, 112, head, 12, SOFT, KR, "start", 600)
d.t(20, 136, "첫 블록 · CLUSTER_DOMAIN REVERSE_CIDRS", 12, SOFT, MONO, "start", 600)
rows(first, 146)
y2 = 146 + len(first) * PITCH + 18
d.t(20, y2, "둘째 블록 · .", 12, SOFT, MONO, "start", 600)
rows(second, y2 + 10)

d.t(20, 580, "upstream 은 1.7.0 에서 제거 · 지금 파서는 unknown property 로 거부", 13, MUTED, KR, "start")

d.legend(596, [("지금 오류가 나는 줄", ACC), ("뺀 줄", BAD), ("더한 줄", OK)])
d.save("06-03.corefile-stages.svg")
