# 04-03.dns-search-path — 짧은 이름 하나가 다섯 번의 질의가 되는 구조
# 본문 요구: "일반 질의는 <service>.default.svc.cluster.local → svc.cluster.local →
#           cluster.local → 호스트 검색 경로 순으로 시도되므로, 짧은 이름 하나에 다섯 번의
#           요청이 나가 지연을 키울 수 있습니다" + 처방 둘(Autopath · ndots).
# 타입 스펙: type-data-flow.md — 1차에서 4차까지 시도가 한 줄로 이어지고 그 끝에 처방 둘
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 592   # 처방 상자가 496 에서 끝나므로 주석은 그 아래 28px
d = D(W, H, "CLUSTER DNS · SEARCH PATH COST",
      "짧은 이름 하나가 다섯 번의 질의가 된다",
      "검색 경로를 차례로 붙여 가며 시도하기 때문에 이름 하나에 요청이 여러 번 나간다.",
      lead="지연의 근원은 서버가 느린 것이 아니라 물어보는 횟수다")

BY, BH, BW, GAP = 160, 96, 200, 32
STEPS = [(["<service>.default", ".svc.cluster.local"]), (["svc.cluster.local"]),
         (["cluster.local"]), (["호스트 검색 경로"])]
for i, lines in enumerate(STEPS):
    x = 32 + i * (BW + GAP)
    d.box(x, BY, BW, BH, PAPER2, INFO, 1.1, 6)
    d.t(x + BW // 2, BY + 26, f"{i+1}차 시도", 11, SOFT, KR)
    for j, ln in enumerate(lines):
        mono = all(ord(c) < 128 for c in ln)
        d.t(x + BW // 2, BY + 56 + j * 22, ddx.fit(ln, 11, BW - 16, ln), 11,
            MUTED, MONO if mono else KR)
    if i < 3:
        a = x + BW
        d.path(f"M {a+6} {BY+BH//2} L {a+GAP-10} {BY+BH//2}", MUTED, 1.4, m="ar")

FY = BY + BH + 40
d.tone(32, FY, 896, 64, ACC, 6, "12", 1.4)
d.t(480, FY + 40, "짧은 이름 하나에 요청이 다섯 번 — 클러스터 DNS 지연의 근원", 13, ACC, KR)

PY, PW, PH = FY + 104, 448, 96
for x, title, lines, c in ((32, "CoreDNS Autopath", ["서버 측에서 검색 경로를 완성해", "CNAME 으로 답한다 · 질의 한 번", "대신 CoreDNS 메모리가 는다"], WARN),
                          (520, "ndots 조정", ["Pod 기본값 ndots:5 탓에", "외부 도메인도 검색 경로를 다 돈다", "FQDN 이나 dnsConfig 로 낮춘다"], WARN)):
    d.box(x, PY, PW, PH, PAPER2, c, 1.1, 6)
    d.t(x + PW // 2, PY + 28, title, 13, c, KR, "middle", 600)
    for i, ln in enumerate(lines):
        d.t(x + PW // 2, PY + 52 + i * 20, ddx.fit(ln, 11, PW - 24, ln), 11, MUTED, KR)

d.t(36, 524, "처방 둘 다 질의 횟수를 줄이는 쪽이다 — 하나는 서버가 대신 완성하고, 하나는 애초에 검색 경로를 덜 돌게 한다",
    12, MUTED, KR, "start")
d.legend(536, [("차례로 시도하는 이름", INFO), ("처방", WARN), ("그 결과", ACC)])
d.save("04-03.dns-search-path.svg")
print("ok dns-search-path")
