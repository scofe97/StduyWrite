# 타입 스펙: type-flowchart — Pod 패킷이 eBPF 프로그램에서 커널 통과·Envoy·DNS 프록시 세 갈래로 갈라지는 판단 흐름.
# 고른 이유: 본문 §5 「eBPF 와 Envoy 의 분업」이 「L7 검사가 필요한 트래픽만 골라 Envoy 로 넘기고 나머지는 커널에 남는다」는 분기 논리이고,
#            갈림 조건(L7 규칙 유무·DNS 질의)이 논지라 조건에 따라 갈라지는 flowchart 가 맞다. 스펙의 판단 마름모 대신 갈래 화살표 라벨로 조건을 적었다.
# 사실 출처: 《Cilium: Up and Running》 Ch.2 「Cilium at a Glance」의 트래픽 설명 문단과 「The Envoy Proxy」「The DNS Proxy」.
# 값 근거: tc · tcx 후크(본문 §3 「에이전트의 다섯 가지 핵심 책임」), TPROXY·xDS 유닉스 소켓(본문 §5 「eBPF 와 Envoy 의 분업」 끝 문단), HTTP 경로·gRPC·TLS 종단(본문 §5 같은 소절 첫 문단),
#          UDP/TCP 53(본문 §5 「DNS 프록시와 FQDN 보안 정책」), cilium_ipcache_v2(같은 소절 순서 4), 에이전트에 내장된 DNS 프록시(같은 소절 둘째 문단).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "CILIUM UP AND RUNNING · 02-01 §5", "Pod 패킷이 eBPF 에서 세 갈래로 갈라지는 길",
      "eBPF 프로그램이 패킷을 판정해 L3·L4 는 커널에서 끝내고, L7 규칙이 걸린 패킷은 Envoy 로, DNS 질의는 에이전트 안의 DNS 프록시로 넘기는 분기",
      lead="화살표 옆 글자는 갈래를 고르는 조건이고, Envoy 를 거친 패킷은 eBPF 경로로 돌아와 나갑니다.")


def block(x, y, w, h, c, title, lines, focal=False):
    d.tone(x, y, w, h, c, r=6, op="18" if focal else "14", sw=1.4 if focal else 1.1)
    d.t(x + 14, y + 24, title, 14, c, KR, "start", 600)
    for i, (txt, mono) in enumerate(lines):
        d.t(x + 14, y + 46 + 18 * i, txt, 12, INK if mono else MUTED, MONO if mono else KR, "start")


block(28, 108, 224, 64, MUTED, "Pod", [("패킷을 보냄", False)])
block(330, 108, 260, 64, ACC, "eBPF 프로그램", [("tc · tcx 후크에서 패킷 판정", False)], focal=True)
d.arrow([(252, 140), (330, 140)], MUTED, "ar", 1.4)

# 갈림
d.line(460, 172, 460, 200, MUTED, 1.4)
d.arrow([(460, 200), (160, 200), (160, 244)], OK, "ok", 1.4)
d.arrow([(460, 200), (460, 244)], WARN, "warn", 1.4)
d.arrow([(460, 200), (760, 200), (760, 244)], INFO, "info", 1.4)
d.t(172, 228, "L7·FQDN 규칙 없음", 12, OK, KR, "start", 600)
d.t(472, 228, "L7 규칙 있음", 12, WARN, KR, "start", 600)
d.t(772, 216, "FQDN 규칙이 걸린", 12, INFO, KR, "start", 600)
d.t(772, 232, "DNS 질의", 12, INFO, KR, "start", 600)

block(28, 244, 264, 78, OK, "커널 데이터패스", [("L3 · L4 판정으로 전달 또는 차단", False), ("프록시를 거치지 않음", False)])
block(328, 244, 264, 78, WARN, "cilium-envoy", [("HTTP 경로 · gRPC · TLS 종단", False), ("TPROXY 로 수신", False)])
block(628, 244, 264, 78, INFO, "DNS 프록시 · 에이전트 안", [("UDP/TCP 53 질의를 가로챔", False), ("CoreDNS 중계 · 신원 기록", False)])

d.arrow([(460, 322), (460, 360)], WARN, "warn", 1.4)
d.t(472, 346, "처리를 마친 패킷", 12, MUTED, KR, "start")
block(328, 360, 264, 56, OK, "커널 eBPF 경로", [("목적지로 전달", False)])

d.legend(440, [("판정하는 곳", ACC), ("커널 안에서 끝", OK), ("Envoy (L7)", WARN), ("DNS 프록시", INFO)])
d.save("02-01.l7-dns-redirect.svg")
