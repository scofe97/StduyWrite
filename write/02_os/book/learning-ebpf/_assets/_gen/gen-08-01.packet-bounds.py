# 타입 스펙: type-nested — 바깥 data~data_end 버퍼 안에 이더넷 헤더·IP 헤더·L4 상자가 바이트 폭 비례(20px/바이트)로 놓이고, 헤더 안에 필드가 들어간다. 아래 눈금자에 data·data+14·data+34·data_end 와 경계 검사 둘을 건다.
# 사실 출처: 예제 저장소 lizrice/learning-ebpf chapter8/packet.h (HEAD 91ded4a) 21~43행(lookup_protocol: sizeof(struct ethhdr) 14, sizeof(struct iphdr) 20, ETH_P_IP 0x0800, iph->protocol),
#   ETH_HLEN 14(packet.h 10행), 이더넷 h_dest 6·h_source 6·h_proto 2 바이트(0~5·6~11·12~13), IPv4 헤더 protocol 은 헤더 안 9번째 바이트라 패킷 오프셋 14+9=23,
#   추출본 ebpf8.txt 248~296행(lookup_protocol 과 설명).
# Layout conventions: X(b)=56+20b, 헤더 상자 y=140~240, 필드 행 y=176~224, 눈금자 y=336, 괄호 y=392·448. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 576
d = D(W, H, "LEARNING EBPF · 08-01 §2", "헤더를 하나 읽을 때마다 data_end 를 넘지 않는지 먼저 증명한다",
      "패킷 버퍼는 data 에서 data_end 까지다. 이더넷 헤더는 0~13 바이트로 h_proto 가 12~13 에 있고 값은 0x0800 이다. IP 헤더는 14~33 바이트로 protocol 이 오프셋 23 에 있고 값은 1 이다. data+14 가 data_end 이하여야 이더넷 헤더를, data+34 가 data_end 이하여야 IP 헤더를 읽을 수 있다.",
      "읽기 전에 경계 안임을 보여야 verifier 가 통과시킵니다")

def X(b): return 56 + 20 * b

# 바깥 버퍼
d.o.append(f'<rect x="24" y="104" width="952" height="152" rx="8" fill="{INK}06" stroke="{SOFT}" stroke-width="1.2"/>')
d.t(40, 124, "data ~ data_end", 11, SOFT, MONO, "start", 600)

# 헤더 상자
HY, HHT = 140, 100
d.tone(X(0), HY, X(14) - X(0), HHT, INFO, 6, "12", 1.2)
d.tone(X(14), HY, X(34) - X(14), HHT, INFO, 6, "12", 1.2)
d.tone(X(34), HY, 200, HHT, MUTED, 6, "12", 1.2)
d.t(X(0) + 12, HY + 20, "struct ethhdr", 12, INFO, MONO, "start", 600)
d.t(X(14) - 12, HY + 20, "0~13", 11, MUTED, MONO, "end")
d.t(X(14) + 12, HY + 20, "struct iphdr", 12, INFO, MONO, "start", 600)
d.t(X(34) - 12, HY + 20, "14~33", 11, MUTED, MONO, "end")
d.t(X(34) + 12, HY + 20, "L4", 12, MUTED, MONO, "start", 600)
d.t(X(34) + 188, HY + 20, "34~", 11, MUTED, MONO, "end")

# 필드
FY, FH = 176, 48
def field(x0, x1, name, c, sub=None, hot=False):
    w = x1 - x0
    if hot:
        d.tone(x0, FY, w, FH, ACC, 4, "1F", 1.4)
    else:
        d.box(x0, FY, w, FH, PAPER2, RULE, 0.9, 4)
    if name:
        d.t(x0 + w / 2, FY + 22, name, 12, c, MONO, "middle", 600)
    if sub:
        d.t(x0 + w / 2, FY + 38, sub, 11, MUTED, MONO)

field(X(0) + 4, X(6) - 4, "h_dest", INK, "0~5")
field(X(6) + 4, X(12) - 4, "h_source", INK, "6~11")
field(X(12) + 4, X(14) - 4, None, ACC, None, hot=True)
field(X(14) + 4, X(23) - 4, "…", MUTED)
field(X(23), X(24), None, ACC, None, hot=True)
field(X(24) + 4, X(34) - 4, "…", MUTED)
d.box(X(34) + 4, FY, 192, FH, PAPER2, RULE, 0.9, 4)
d.t(X(34) + 100, FY + 28, "1 ICMP · 6 TCP · 17 UDP", 11, MUTED, MONO)

# 필드 설명 칩
d.line(X(13), FY + FH, X(13), 276, ACC, 1.2)
d.chip(X(13), 292, "h_proto 12~13 = 0x0800", ACC, 11)
d.line(X(23) + 10, FY + FH, X(23) + 10, 276, ACC, 1.2)
d.chip(X(23) + 10 + 56, 292, "protocol 23 = 1", ACC, 11)

# 눈금자
RY = 348
d.line(X(0), RY, X(34) + 200, RY, SOFT, 1.2)
for b, lab, anc in ((0, "data", "start"), (14, "data+14", "middle"), (34, "data+34", "middle")):
    d.line(X(b), RY - 6, X(b), RY + 6, SOFT, 1.2)
    d.t(X(b), RY + 24, lab, 12, INK, MONO, anc, 600)
d.line(X(34) + 200, RY - 6, X(34) + 200, RY + 6, SOFT, 1.2)
d.t(X(34) + 200, RY + 24, "data_end", 12, INK, MONO, "end", 600)

# 경계 검사 둘
def bracket(x0, x1, y, label, expr, c):
    d.line(x0, y - 6, x0, y + 6, c, 1.4)
    d.line(x1, y - 6, x1, y + 6, c, 1.4)
    d.line(x0, y, x1, y, c, 1.4)
    d.chip((x0 + x1) / 2, y, label, c, 11)
    d.t((x0 + x1) / 2, y + 28, expr, 12, c, MONO, "middle", 600)

bracket(X(0), X(14), 400, "검사 1", "data+14 ≤ data_end", OK)
bracket(X(0), X(34), 456, "검사 2", "data+34 ≤ data_end", OK)

d.legend(H - 56, [("검사 통과 조건", OK), ("읽는 필드", ACC), ("헤더", INFO)])
d.save("08-01.packet-bounds.svg")
