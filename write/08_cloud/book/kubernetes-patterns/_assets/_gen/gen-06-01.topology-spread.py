# 06-01 topology spread — maxSkew 가 새 Pod 의 zone 을 정하고, 롤링 업데이트에서는 새 Pod 가 자리를 못 찾는다
# 본문: 장면 1 은 zone-a 에 app=bar Pod 2개, zone-b 에 1개가 있을 때 새 Pod 의 배치(maxSkew 1, DoNotSchedule).
#   장면 2 는 노드 둘 · replica 2 · required anti-affinity 에서 maxSurge 로 만든 surge Pod 가 Pending 에 머무는 경우.
# 타입 스펙: type-process — 새 Pod 가 후보 위치로 가며 허용·거부로 갈리는 단계 흐름을 전·후 두 장면으로 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W = 900
d = D(W, 706, "KUBERNETES PATTERNS · 06-01",
      "maxSkew 는 zone 을 고르고, required anti-affinity 는 롤링을 막습니다",
      "장면 1 에서 zone-a 에 app bar Pod 2개, zone-b 에 1개가 있을 때 새 Pod 를 zone-a 에 놓으면 3 대 1 로 skew 2 가 되어 maxSkew 1 을 넘으므로 DoNotSchedule 이 거부하고, "
      "zone-b 에 놓으면 2 대 2 로 통과합니다. 장면 2 에서는 노드 둘, replica 2, required anti-affinity 환경의 롤링 업데이트에서 surge Pod 가 놓일 노드가 없어 Pending 이 됩니다.",
      lead="장면 1 은 topology spread 가 zone 을 고르는 규칙, 장면 2 는 그 대안이 필요해지는 required anti-affinity 의 함정")

def chip(x, y, txt, c, w=84, dash=False):
    ds = ' stroke-dasharray="4 3"' if dash else ""
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"{ds}/>')
    d.t(x + w // 2, y + 19, txt, 11, c, MONO)

# ── 장면 1 ───────────────────────────────────────────────────────────────
d.t(24, 112, "장면 1 — topologyKey topology.kubernetes.io/zone · maxSkew 1 · DoNotSchedule", 12, SOFT, KR, "start", 600)
ZX, ZW, ZH = 300, 576, 88
ZA, ZB = 128, 232
d.tone(ZX, ZA, ZW, ZH, BAD, 6, "0c", 1.0)
d.t(ZX + 16, ZA + 28, "zone-a", 14, BAD, MONO, "start", 600)
chip(ZX + 16, ZA + 44, "app: bar", INFO); chip(ZX + 108, ZA + 44, "app: bar", INFO)
d.t(ZX + 300, ZA + 28, "새 Pod 를 놓으면 3 대 1", 13, INK, KR, "start", 600)
d.t(ZX + 300, ZA + 50, "skew 2 > maxSkew 1", 12, BAD, MONO, "start")
d.t(ZX + 300, ZA + 72, "DoNotSchedule 이 거부", 12, MUTED, KR, "start")
d.tone(ZX, ZB, ZW, ZH, OK, 6, "0c", 1.0)
d.t(ZX + 16, ZB + 28, "zone-b", 14, OK, MONO, "start", 600)
chip(ZX + 16, ZB + 44, "app: bar", INFO); chip(ZX + 108, ZB + 44, "새 Pod", ACC, dash=True)
d.t(ZX + 300, ZB + 28, "새 Pod 를 놓으면 2 대 2", 13, INK, KR, "start", 600)
d.t(ZX + 300, ZB + 50, "skew 0 ≤ maxSkew 1", 12, OK, MONO, "start")
d.t(ZX + 300, ZB + 72, "필터 통과", 12, MUTED, KR, "start")
d.tone(24, 190, 176, 60, ACC, 6, "16", 1.4)
d.t(112, 214, "새 Pod", 14, ACC, KR, "middle", 600)
d.t(112, 236, "app: bar", 12, INK, MONO)
d.arrow([(202, 204), (250, 204), (250, 172), (296, 172)], BAD, "bad", 1.4, "5 4")
d.arrow([(202, 236), (250, 236), (250, 276), (296, 276)], OK, "ok", 1.4)

# ── 장면 2 ───────────────────────────────────────────────────────────────
SEP = 348
d.line(24, SEP, W - 24, SEP, RULE, 0.8)
d.t(24, SEP + 32, "장면 2 — 노드 2 · replica 2 · required anti-affinity 에서 롤링 업데이트(maxSurge 1)", 12, SOFT, KR, "start", 600)
NY, NH = 470, 84
for i, n in enumerate(("node-1", "node-2")):
    x = 24 + i * 272
    d.box(x, NY, 232, NH, PAPER2, RULE, 0.9, 6)
    d.t(x + 16, NY + 28, n, 13, INK, MONO, "start", 600)
    chip(x + 16, NY + 42, "app: bar", INFO)
    d.t(x + 116, NY + 61, "기존 Pod", 12, MUTED, KR, "start")
d.tone(640, NY, 236, NH, BAD, 6, "12", 1.2)
d.t(658, NY + 26, "surge Pod", 13, INK, KR, "start", 600)
d.t(658, NY + 50, "Pending", 15, BAD, MONO, "start", 600)
d.t(658, NY + 72, "maxSurge 1 로 추가됨", 12, MUTED, KR, "start")
d.arrow([(638, NY + 42), (536, NY + 42)], BAD, "bad", 1.4, "5 4")
d.arrow([(758, NY - 2), (758, NY - 36), (140, NY - 36), (140, NY - 4)], BAD, "bad", 1.4, "5 4")
d.t(450, NY - 46, "required anti-affinity · 같은 app: bar Pod 가 있는 노드", 12, BAD, KR, "middle")

FY = NY + NH + 28
d.tone(24, FY, 852, 48, OK, 6, "10", 1.0)
d.t(40, FY + 29, "풀리는 설정", 12, OK, KR, "start", 600)
d.t(150, FY + 29, "maxSurge: 0 · maxUnavailable: 1", 13, INK, MONO, "start", 600)
d.t(450, FY + 29, "옛 Pod 가 먼저 내려가고 그 자리에 새 Pod 가 놓임", 12, MUTED, KR, "start")

d.legend(FY + 76, [("허용", OK), ("거부·Pending", BAD), ("새 Pod", ACC), ("기존 Pod", INFO)])
d.save("06-01.topology-spread.svg")
print("ok topology-spread")
