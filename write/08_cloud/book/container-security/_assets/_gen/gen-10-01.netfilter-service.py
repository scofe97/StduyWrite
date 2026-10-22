# 타입 스펙: type-data-flow — 위쪽 kube-proxy 가 체인 규칙을 쓰고 아래쪽 흐름이 다섯 단계(Service 이름 · KUBE-SERVICES · KUBE-SVC · KUBE-SEP · 파드)를 지난다. 맨 아래 띠에 패킷의 목적지 주소가 단계마다 어떻게 되는지 싣고, DNAT 에서만 값이 바뀜을 focal 로 건다.
# 사실 출처: 노트 L144(kube-proxy 가 iptables 규칙으로 부하 분산 · DNS · 규칙 다시 쓰임), L146~L163(iptables -t nat -L 출력: Service IP 10.100.132.10 · KUBE-SERVICES · KUBE-SVC-SV7AMNAGZFKZEMQ4 · KUBE-SEP-XZGVVMRRSKK6PWWN · KUBE-SEP-PUXUHBP3DTPPX72C · probability 0.5 · DNAT · 파드 IP 10.32.0.3 / 10.32.0.4 · nginx 복제본 두 개)
# Layout conventions: 단계 슬롯 폭 104·128·208·208·152 + 간격 40(x=24·168·336·584·832), 주 행 y=248 h=56, SEP 두 노드 y=204·284 h=64, kube-proxy y=96 h=56 · 버스 y=176, 값 띠 y=420. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 1000, 516


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "DATA-FLOW · 10-01 §4",
      "Service IP 로 향한 패킷은 세 체인을 지나며 목적지가 파드 IP 로 바뀝니다",
      "my-nginx 의 Service IP 10.100.132.10 으로 향한 패킷이 커널의 KUBE-SERVICES, KUBE-SVC-SV7AMNAGZFKZEMQ4 체인을 거쳐 "
      "확률 0.5 로 두 KUBE-SEP 체인 중 하나로 갈라지고, DNAT 가 목적지를 파드 IP 10.32.0.3 또는 10.32.0.4 로 바꾼다. "
      "kube-proxy 는 이 규칙들을 쓴다.",
      lead="iptables -t nat -L 로 보이는 체인 세 개를 따라가며 패킷의 목적지 주소가 어디서 바뀌는지 봅니다.")

# 단계 슬롯
XS = [24, 168, 336, 584, 832]
WS = [104, 128, 208, 208, 152]
CX = [x + w // 2 for x, w in zip(XS, WS)]
MY, MH = 248, 56          # 주 행
MCY = MY + MH // 2        # 276


def node(i, y, h, t1, t2, c=None, focal=False, mono1=True, dash=False):
    x, w = XS[i], WS[i]
    fit(t1, 12 if mono1 else 14, w - 16)
    fit(t2, 13, w - 16)
    ds = ' stroke-dasharray="5 4"' if dash else ""
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"{ds}/>')
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + h / 2 - 4, t1, 12 if mono1 else 14, c or INK, MONO if mono1 else KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, t2, 13, MUTED, KR if any("가" <= c <= "힣" for c in t2) else MONO, "middle")


# ── 화살표(노드보다 먼저) ──
# kube-proxy → 세 체인: 규칙 작성(버스)
BUS = 176
d.line(CX[2], 152, CX[2], BUS, WARN, 1.4, "5 4")  # 버스까지는 선만
d.line(CX[1], BUS, CX[3], BUS, WARN, 1.4, "5 4")
d.arrow([(CX[1], BUS), (CX[1], MY - 4)], WARN, "warn", 1.4, "5 4")
d.arrow([(CX[2], BUS), (CX[2], MY - 4)], WARN, "warn", 1.4, "5 4")
d.arrow([(CX[3], BUS), (CX[3], 200)], WARN, "warn", 1.4, "5 4")

# 패킷 경로
d.arrow([(128, MCY), (164, MCY)], MUTED, "ar", 1.6)
d.t(148, MCY - 12, "DNS", 13, MUTED, MONO, "middle", 600)
d.arrow([(296, MCY), (332, MCY)], MUTED, "ar", 1.6)
d.path(f"M 544 {MCY} L 564 {MCY} L 564 236 L 580 236", MUTED, 1.6, "ar")
d.path(f"M 564 {MCY} L 564 316 L 580 316", MUTED, 1.6, "ar")
d.arrow([(792, 236), (828, 236)], ACC, "acc", 1.8)
d.arrow([(792, 316), (828, 316)], ACC, "acc", 1.8)

# ── 노드 ──
node(0, MY, MH, "my-nginx", "서비스 이름", mono1=True)
node(1, MY, MH, "KUBE-SERVICES", "목적지 일치", c=INFO)
node(2, MY, MH, "KUBE-SVC-SV7AMNAGZFKZEMQ4", "확률 분기", c=INFO)
node(3, 204, 64, "KUBE-SEP-XZGVVMRRSKK6PWWN", "probability 0.5", c=INFO)
node(3, 284, 64, "KUBE-SEP-PUXUHBP3DTPPX72C", "나머지", c=INFO)

# 파드 두 개
x4, w4 = XS[4], WS[4]
d.o.append(f'<rect x="{x4}" y="216" width="{w4}" height="120" rx="6" fill="{OK}12" stroke="{OK}" stroke-width="1.2"/>')
d.t(x4 + w4 / 2, 244, "nginx 파드 2개", 14, OK, KR, "middle", 600)
d.t(x4 + w4 / 2, 284, "10.32.0.3", 13, INK, MONO, "middle", 600)
d.t(x4 + w4 / 2, 308, "10.32.0.4", 13, INK, MONO, "middle", 600)

# kube-proxy (사용자 공간)
d.o.append(f'<rect x="{XS[2]}" y="96" width="{WS[2]}" height="56" rx="6" fill="{WARN}12" stroke="{WARN}" stroke-width="1.2"/>')
d.t(CX[2], 120, "kube-proxy", 13, WARN, MONO, "middle", 600)
d.t(CX[2], 140, "iptables 규칙 작성", 13, MUTED, KR, "middle")
d.t(564, 128, "파드 집합이 바뀌면 재작성", 13, MUTED, KR, "start")

# ── 패킷의 목적지 주소 띠 ──
RY = 420
d.t(156, 380, "패킷의 목적지 주소", 13, MUTED, KR, "middle", 600)
for i, y1 in ((0, MY + MH), (1, MY + MH), (2, MY + MH)):
    d.line(CX[i], y1 + 4, CX[i], RY - 12, RULE, 0.8, "3 5")
d.line(CX[3], 348 + 4, CX[3], RY - 12, RULE, 0.8, "3 5")
d.line(CX[4], 336 + 4, CX[4], RY - 12, RULE, 0.8, "3 5")

IP = "10.100.132.10"
d.chip(CX[0], RY, IP, INFO, 12)
d.chip(CX[1], RY, IP, INFO, 12)
d.chip(CX[2], RY, IP, INFO, 12)
d.chip(CX[3], RY, "DNAT", ACC, 12)
d.chip(CX[4], RY, "10.32.0.3 | 10.32.0.4", OK, 12)


def edge(i, j, c, mk):
    # 칩 오른쪽 끝에서 다음 칩 왼쪽 끝까지(4의 배수로 맞춤)
    def half(t, sz=12):
        return (len(t) * sz * 0.62 + 14) / 2
    labels = [IP, IP, IP, "DNAT", "10.32.0.3 | 10.32.0.4"]
    x1 = int((CX[i] + half(labels[i]) + 6) // 4 * 4)
    x2 = int((CX[j] - half(labels[j]) - 6) // 4 * 4)
    d.arrow([(x1, RY), (x2, RY)], c, mk, 1.4)


edge(0, 1, MUTED, "ar")
edge(1, 2, MUTED, "ar")
edge(2, 3, MUTED, "ar")
edge(3, 4, ACC, "acc")

d.legend(468, [("체인", INFO), ("규칙 작성", WARN), ("목적지가 바뀌는 지점", ACC), ("파드", OK)])
d.save(str(ASSETS / "10-01.netfilter-service.svg"))
print("ok 10-01 netfilter-service")
