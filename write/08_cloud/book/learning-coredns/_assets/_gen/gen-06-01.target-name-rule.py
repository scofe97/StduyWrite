# 06-01 §6 — SRV 대상과 ADDITIONAL 의 A 에 쓰이는 엔드포인트 이름을 CoreDNS 가 고르는 순서.
# 소스 근거: plugin/kubernetes/kubernetes.go 의 endpointHostname — Hostname 이 있으면 그것,
#            endpointNameMode && TargetRefName 이면 파드 이름, 아니면 IPv4 는 '.' 를 '-' 로, IPv6 는 ':' 를 '-' 로(끝이 '-' 면 '0').
#            README 의 endpoint_pod_names 설명(대상 파드가 없거나 63자를 넘으면 대시 형태).
# 값 근거: 원서 Example 6-5 의 10-5-104-3, Example 6-7 의 myhost.
# 타입 스펙: type-flowchart — 위에서부터 조건을 하나씩 걸러 이름이 하나로 정해지는 분기가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, WARN, KR, MONO

W, H = 880, 530
d = D(W, H, "LEARNING COREDNS · 06-01 §6",
      "엔드포인트 이름은 위에서부터 걸러 정한다",
      "엔드포인트에 hostname 이 있으면 그 값을 쓴다. 없으면 endpoint_pod_names 를 켰을 때 파드 이름을, "
      "끄면 IP 를 대시로 이은 이름을 쓴다. 원서 예의 10-5-104-3 이 마지막 칸이다.",
      "주황 칸이 원서 예제가 받은 이름입니다")

LX, LW = 40, 300
RX, RW = 480, 380


def box(x, y, w, h, main, sub, focal=False, mono=False, q=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, WARN if q else RULE, 1.0, 6)
    d.t(x + 16, y + 26, main, 14, ACC if focal else INK, MONO if mono else KR, "start", 600)
    if sub:
        d.t(x + 16, y + 48, sub, 12, MUTED, KR, "start")


box(LX, 110, LW, 60, "엔드포인트 하나", "원서 Example 6-5 · IP 10.5.104.3")
box(LX, 210, LW, 60, "hostname 이 있나", "파드의 hostname · subdomain 이 맞을 때", q=True)
box(LX, 310, LW, 60, "endpoint_pod_names 를 켰나", "kubernetes 플러그인 옵션", q=True)
box(LX, 410, LW, 60, "10-5-104-3", "IP 를 대시로 · 기본값", focal=True, mono=True)

box(RX, 210, RW, 60, "myhost", "hostname 값 그대로 · Example 6-7", mono=True)
box(RX, 310, RW, 60, "파드 이름", "대상 파드가 없거나 63자를 넘으면 대시 형태")

for y0, y1 in ((170, 210), (270, 310), (370, 410)):
    d.path(f"M {LX + LW / 2} {y0 + 2} L {LX + LW / 2} {y1 - 3}", MUTED, 1.3, m="ar")
for y0, lab in ((270, "아니요"), (370, "아니요")):
    d.t(LX + LW / 2 + 10, y0 + 24, lab, 12, MUTED, KR, "start")
for y in (240, 340):
    d.path(f"M {LX + LW + 2} {y} L {RX - 3} {y}", MUTED, 1.3, m="ar")
    d.t((LX + LW + RX) / 2, y - 8, "예", 12, MUTED, KR)

d.t(RX, 446, "IPv6 · ':' 를 '-' 로 · 끝이 '-' 면 0 을 붙임", 12, MUTED, KR, "start")

d.legend(490, [("원서 예제가 받은 이름", ACC), ("조건", WARN)])
d.save("06-01.target-name-rule.svg")
