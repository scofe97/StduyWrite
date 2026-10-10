# 타입 스펙: type-timeline — 한 번의 A 질의로 생긴 FQDN 캐시 항목이 질의·등록·응답 전달·연결 허용·TTL 만료·정리를 거치는 순서. 눈금은 순서이며 시간 비례가 아니다.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 695-745(응답을 FQDN 캐시와 IP 캐시에 반영한 뒤 Pod 에 응답, 그 뒤 연결) / docs.cilium.io v1.20 cmdref/cilium-agent(--tofqdns-proxy-response-max-delay 기본 100ms · --tofqdns-min-ttl · --tofqdns-max-deferred-connection-deletes 기본 10000) · cilium v1.20.2 pkg/fqdn/namemanager/gc.go(TTL 이 지나도 연결이 살아 있으면 IP 유지)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 344
d = D(W, H, "CILIUM UP AND RUNNING · 13-02 §3", "FQDN 캐시 항목의 수명",
      "질의로 생긴 항목은 응답 TTL 동안 허용 근거가 되고, 만료 뒤에도 연결이 살아 있으면 IP 가 유지됩니다",
      "눈금은 순서이며 시간 비례가 아닙니다")

Y_BASE = 200
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

events = [
    (100, "시작", True, "A 질의", "cilium.io.", INFO, False),
    (260, "응답 전달 전", False, "IP 등록", "보류 최대 100ms", ACC, True),
    (420, "등록 뒤", True, "응답 전달", "Pod 가 IP 로 연결", INFO, False),
    (580, "TTL 안", False, "연결 허용", "identity 일치", OK, False),
    (720, "TTL 만료", True, "항목 만료", "연결 중이면 IP 유지", WARN, False),
    (840, "연결 종료 뒤", False, "정리", "캐시에서 삭제", MUTED, False),
]

for x, time_str, is_above, title, sub, color, focal in events:
    r = 6 if focal else 4
    fill_col = color if focal else PAPER
    d.o.append(f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{fill_col}" stroke="{color}" stroke-width="1.4"/>')

    date_y = Y_BASE - 14 if is_above else Y_BASE + 22
    d.t(x, date_y, time_str, 12, color if focal else MUTED, KR, "middle", 600)

    if is_above:
        text_y = Y_BASE - 56
        d.line(x, Y_BASE - 22, x, text_y + 18, RULE, sw=0.8, dash="2 2")
    else:
        text_y = Y_BASE + 56
        d.line(x, Y_BASE + 28, x, text_y - 14, RULE, sw=0.8, dash="2 2")

    if focal:
        bw, bh = max(120, sum(6.8 if ord(c) < 128 else 11.5 for c in sub) + 20), 44
        by = text_y - 14
        d.tone(x - bw / 2, by, bw, bh, color, r=4, op="18", sw=1.2)
        d.t(x, by + 18, title, 12, color, KR, "middle", 600)
        d.t(x, by + 34, sub, 12, INK, KR, "middle")
    else:
        d.t(x, text_y, title, 12, color if is_above else INK, KR, "middle", 600)
        d.t(x, text_y + 16, sub, 12, MUTED, KR, "middle")

d.save("13-02.fqdn-cache-lifetime.svg")
