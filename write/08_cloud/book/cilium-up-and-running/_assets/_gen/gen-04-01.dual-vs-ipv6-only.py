# 타입 스펙: type-architecture — 듀얼 스택(IPv4+IPv6 직접)과 IPv6 전용(IPv4 끔 · 외부 IPv4 접근은 DNS64·NAT64 경유)의 주소·트래픽 구조 비교.
# 사실 출처: 추출본 ch04.txt 줄 860-868 · 949-969 · 1003-1050 · 1083-1208 · 1248-1253 (RFC 6146 NAT64, RFC 6147 DNS64).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 524
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §6", "듀얼 스택과 IPv6 전용의 주소·외부 통신 경로",
      "듀얼 스택은 IPv4·IPv6 를 함께 두고, IPv6 전용은 IPv4 를 끈 대신 외부 IPv4 에 닿을 때 DNS64 와 NAT64 가 필요합니다",
      "kind 실습 값 · Service PreferDualStack 대 SingleStack")


def zone(x, y, w, h, title, col):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}08" stroke="{col}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, title, 12, col, KR, "start", 600)


# Zone 1: 듀얼 스택 (위)
Z1Y, Z1H = 98, 152
zone(24, Z1Y, 872, Z1H, "듀얼 스택 · ipFamily: dual · ipv6.enabled=true", INFO)

b1 = [
    (44, 184, "Node PodCIDRs", "10.244.1.0/24", "fd00:10:244:1::/64", INFO),
    (272, 200, "Pod · pod-worker", "10.244.1.117", "fd00:10:244:1::8204", INFO),
    (516, 208, "Service · PreferDualStack", "10.96.181.159", "fd00:10:96::d4d5", INFO),
    (764, 112, "직접 통신", "curl -4 → 200", "curl -6 → 200", OK),
]
BY1 = Z1Y + 36
for x, w, t, l1, l2, c in b1:
    d.box(x, BY1, w, 92, PAPER, c, 1.1, 6)
    d.t(x + w / 2, BY1 + 22, t, 12 if any("가" <= ch <= "힣" for ch in t) else 11, c, KR if any("가" <= ch <= "힣" for ch in t) else MONO, "middle", 600)
    d.t(x + w / 2, BY1 + 48, l1, 11, INK, MONO, "middle")
    d.t(x + w / 2, BY1 + 70, l2, 11, INK, MONO, "middle")

for x0, x1, col, mk in [(228, 270, INFO, "info"), (472, 514, INFO, "info"), (724, 762, OK, "ok")]:
    d.arrow([(x0, BY1 + 46), (x1, BY1 + 46)], col, mk, 1.5)

# 화살표 의미: 대역 배정(주소 출처)과 호출 방향(트래픽)을 가른다
for (lx, l1, l2) in [(249, "대역", "배정"), (493, "curl", "요청"), (743, "응답", "확인")]:
    d.t(lx, BY1 + 24, l1, 11, MUTED, KR if l1 != "curl" else MONO, "middle")
    d.t(lx, BY1 + 37, l2, 11, MUTED, KR, "middle")

# Zone 2: IPv6 전용 (아래)
Z2Y, Z2H = 266, 188
zone(24, Z2Y, 872, Z2H, "IPv6 전용 · ipFamily: ipv6 · ipv4.enabled=false", OK)

BY2A = Z2Y + 32
b2_top = [
    (44, 184, "Node PodCIDR", "2001:db8:10:1::/64", OK),
    (272, 200, "Pod · pod-worker", "2001:db8:10:1::4d69", OK),
    (516, 208, "Service · SingleStack", "2001:db8:10:96::6f43", OK),
    (764, 112, "내부 통신", "curl -6 → 200", OK),
]
for x, w, t, l1, c in b2_top:
    d.box(x, BY2A, w, 62, PAPER, c, 1.1, 6)
    d.t(x + w / 2, BY2A + 22, t, 12 if any("가" <= ch <= "힣" for ch in t) else 11, c, KR if any("가" <= ch <= "힣" for ch in t) else MONO, "middle", 600)
    d.t(x + w / 2, BY2A + 44, l1, 11, INK, MONO, "middle")

for x0, x1 in [(228, 270), (472, 514), (724, 762)]:
    d.arrow([(x0, BY2A + 31), (x1, BY2A + 31)], OK, "ok", 1.5)
for (lx, l1, l2) in [(249, "대역", "배정"), (493, "curl", "요청"), (743, "응답", "확인")]:
    d.t(lx, BY2A + 8, l1, 11, MUTED, KR if l1 != "curl" else MONO, "middle")
    d.t(lx, BY2A + 20, l2, 11, MUTED, KR, "middle")

# 외부 IPv4 전용 의존 경로 (DNS64 · NAT64)
BY2B = Z2Y + 114
# Pod 아래에서 출발하는 직각 경로
d.arrow([(372, BY2A + 62), (372, BY2B + 28), (514, BY2B + 28)], ACC, "acc", 1.5)
d.t(442, BY2B + 18, "IPv4 외부 질의", 12, ACC, KR, "middle", 600)

d.tone(516, BY2B, 208, 56, ACC, r=6, op="14", sw=1.4)
d.t(516 + 104, BY2B + 22, "DNS64 · NAT64", 12, ACC, MONO, "middle", 600)
d.t(516 + 104, BY2B + 42, "A→AAAA 합성 · IPv6→IPv4", 12, INK, KR, "middle")

d.arrow([(724, BY2B + 28), (762, BY2B + 28)], WARN, "warn", 1.5)
d.tone(764, BY2B, 112, 56, WARN, r=6, op="12", sw=1.1)
d.t(764 + 56, BY2B + 22, "외부 IPv4", 13, WARN, KR, "middle", 600)
d.t(764 + 56, BY2B + 42, "레지스트리 등", 12, MUTED, KR, "middle")

d.legend(H - 52, [("듀얼 스택", INFO), ("IPv6 전용", OK), ("전환 장치(핵심)", ACC), ("외부 IPv4 전용", WARN)])
d.save("04-01.dual-vs-ipv6-only.svg")
