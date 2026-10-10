# 타입 스펙: type-deployment — EKS 노드의 ENI 가 보조 IP 를 들고 있고 Pod 가 그 주소를 VPC 안에서 직접 쓰는 배치.
# 사실 출처: 추출본 cil4.txt 줄 657-667 · 751-757 · 775-790, docs.cilium.io/en/stable/network/concepts/ipam/eni/ (status.eni.enis).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 492
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §5", "ENI 보조 IP 에서 Pod 주소까지",
      "Pod 는 ENI 가 들고 있는 VPC 주소를 NAT 없이 그대로 씁니다",
      "EKS · eu-west-1 · echoserver Pod")

# zone: VPC
ZX, ZY, ZW, ZH = 24, 100, 872, 324
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}05" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 4"/>')
d.o.append(f'<rect x="{ZX + 12}" y="{ZY - 8}" width="150" height="16" fill="{PAPER}"/>')
d.t(ZX + 20, ZY + 4, "AWS VPC · eu-west-1", 9, SOFT, MONO, "start")

# node
NX, NY, NW, NH = 48, 132, 824, 224
d.box(NX, NY, NW, NH, PAPER2, RULE, 1.0, 6)
d.o.append(f'<rect x="{NX + 12}" y="{NY + 12}" width="32" height="16" rx="2" fill="{PAPER}" stroke="{MUTED}" stroke-width="0.8"/>')
d.t(NX + 28, NY + 24, "VM", 9, MUTED, MONO, "middle")
d.t(NX + 54, NY + 25, "EC2 ip-192-168-132-54", 11, INK, MONO, "start", 600)

# ENI chip (focal)
EX, EY, EW, EH = 72, 196, 236, 64
d.tone(EX, EY, EW, EH, ACC, r=4, op="14", sw=1.4)
d.t(EX + EW / 2, EY + 24, "ENI", 9, ACC, MONO, "middle")
d.t(EX + EW / 2, EY + 46, "eni-02f39382678db84b5", 11, ACC, MONO, "middle", 600)
d.t(EX + EW / 2, EY + EH + 20, "보조 IP 9개", 12, MUTED, KR, "middle")

# secondary IP chips
IX, IW, IH = 396, 184, 36
ips = ["192.168.156.61", "192.168.142.65", "192.168.131.53"]
ys = [160, 224, 288]
PX, PW = 660, 188
for ip, y in zip(ips, ys):
    d.box(IX, y, IW, IH, PAPER, INFO, 1.0, 4)
    d.t(IX + IW / 2, y + 23, ip, 11, INK, MONO, "middle")
    d.box(PX, y, PW, IH, PAPER, OK, 1.0, 4)
    d.t(PX + PW / 2, y + 23, "echoserver", 12, OK, MONO, "middle", 600)
    cy = y + IH / 2
    d.arrow([(IX + IW, cy), (PX, cy)], OK, "ok", 1.5)
d.t((IX + IW + PX) / 2, ys[0] + IH / 2 - 8, "Pod IP", 12, MUTED, KR, "middle")

# ENI -> IP chips (bus)
bx = 348
d.line(EX + EW, EY + EH / 2, bx, EY + EH / 2, INFO, 1.5)
d.line(bx, ys[0] + IH / 2, bx, ys[2] + IH / 2, INFO, 1.5)
for y in ys:
    d.arrow([(bx, y + IH / 2), (IX, y + IH / 2)], INFO, "info", 1.5)
d.t(bx - 12, EY + EH / 2 - 10, "/32", 11, MUTED, MONO, "end")

# limit strip
d.box(48, 372, 824, 36, PAPER2, RULE, 0.9, 6)
d.t(60, 395, "노드 IP 상한", 12, MUTED, KR, "start")
d.t(172, 395, "ENI 수 × ENI 당 IP 수 (PD 끔)", 12, INK, KR, "start", 600)

d.legend(440, [("ENI", ACC), ("보조 IP", INFO), ("Pod", OK)])
d.save("04-01.eni-deployment.svg")
