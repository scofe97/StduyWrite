# 타입 스펙: type-swimlane — Pod 하나가 뜨고 통신하기까지를 가로 5단계, 일을 맡는 주체를 세로 3줄(사람·클러스터·노드)로 놓은 개요.
# 고른 이유: 이 장의 줄기가 「노드가 하는 일과 클러스터가 하는 일이 어디서 갈리고 어디서 만나는가」라서, 주체별 줄 위에
#            단계가 이어지는 스윔레인이 가장 가깝다. 스펙에 단계 열 공식이 없어 좌표는 4 의 배수 stride(열 176, 카드 폭 144)로 잡았다.
# 사실 출처: 《Cilium: Up and Running》 Ch.2 Figure 2-1~2-5 와 본문 §1~§6 (절 순서는 흐름 단계 순서와 같다).
# 값 근거: 단계 1 = 본문 §2 「새 노드 합류와 PodCIDR 배분 흐름」 3~5 (CiliumNode · spec.ipam.podCIDRs, 값 10.1.1.0/24 는 원서 Figure 2-4 의 예 값).
#          단계 2 = 본문 §3 「에이전트의 다섯 가지 핵심 책임」 (05-cilium.conflist · /opt/cni/bin/cilium-cni · /sys/fs/bpf · tc / 6.6+ tcx).
#          단계 3 = 본문 §4 「Pod 생성 시의 배선 시퀀스」 (ADD · cilium.sock REST · EndpointCreate · cilium_lxc).
#          단계 4 = 본문 §5 「eBPF 와 Envoy 의 분업」·「DNS 프록시와 FQDN 보안 정책」 (cilium-envoy DaemonSet · UDP/TCP 53 · cilium_ipcache_v2).
#          단계 5 = 본문 §6 「Hubble 관측 파이프라인」 (cilium_events · gRPC :4244 · Relay 컨테이너 :4245 · Service :80 · hubble observe · cilium status).
# 칸마다 §N 칩은 그 카드를 다루는 절이다. 3·4 단계 위쪽 빈 칸은 본문 §2 「오퍼레이터가 멈추면 무엇이 중단되는가」(데이터패스는 노드 커널에서 자율 동작)에서 왔다.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 656


def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "CILIUM UP AND RUNNING · 02-01 OVERVIEW", "Pod 하나가 뜨고 통신하기까지 누가 무엇을 하는가",
      "가로는 노드 합류에서 관측까지 다섯 단계이고 세로는 일을 맡는 주체 세 줄이다. 클러스터에 하나 도는 오퍼레이터는 노드가 합류할 때 CiliumNode 로 PodCIDR 를 넘기고, "
      "그 뒤 Pod 생성과 통신은 노드마다 도는 에이전트와 CNI 플러그인과 프록시가 노드 안에서 끝낸다. 관측은 노드의 Hubble 서버에서 클러스터의 Relay 를 거쳐 사람의 CLI 와 UI 로 올라간다.",
      lead="가로는 단계 1~5, 세로는 일을 맡는 주체이고, 칩은 그 카드를 다루는 절입니다.")

X0, STRIDE, CW = 124, 176, 144
COLS = [X0 + STRIDE * i for i in range(5)]


def card(col, y, h, c, title, lines, sec, soft=False):
    x = COLS[col]
    if soft:
        d.box(x, y, CW, h, PAPER, SOFT, sw=1.0, r=5)
    else:
        d.tone(x, y, CW, h, c, r=5, op="14", sw=1.1)
    d.t(x + 10, y + 19, title, 12, c, KR, "start", 600)
    d.chip(x + CW - 16, y + 13, sec, c, size=9)
    for i, (txt, mono) in enumerate(lines):
        m = mono and fam(txt) == MONO
        d.t(x + 10, y + 36 + 14 * i, txt, 10 if m else 11, INK if mono else MUTED, MONO if m else KR, "start")


# 단계 머리
for i, lab in enumerate(("1 노드 합류", "2 에이전트 기동", "3 Pod 생성", "4 Pod 통신", "5 관측")):
    d.chip(COLS[i] + CW / 2, 118, lab, INK, size=11)

# 줄 바탕과 이름
LANES = ((136, 76, "사람이", "보는 길", None), (236, 100, "클러스터에", "하나만", "Deployment"), (360, 226, "노드마다", "하나씩", None))
for y0, h, a, b, m in LANES:
    d.box(24, y0, 88, h, PAPER2, RULE, sw=0.9, r=6)
    d.box(116, y0, 868, h, PAPER2, RULE, sw=0.9, r=6)
    cy = y0 + h / 2
    d.t(68, cy - (6 if m else 2), a, 12, INK, KR, "middle", 600)
    d.t(68, cy + (12 if m else 16), b, 12, INK, KR, "middle", 600)
    if m:
        d.t(68, cy + 30, m, 9, MUTED, MONO, "middle")

YH, YC = 146, 250
YA, YB, YD = 374, 446, 518

# 사람이 보는 길
card(1, YH, 56, MUTED, "Cilium CLI", [("cilium status", True), ("API 서버로 상태 조회", False)], "§6", soft=True)
card(4, YH, 56, MUTED, "Hubble CLI · UI", [("hubble observe", True), ("전체 노드 흐름 조회", False)], "§6", soft=True)

# 클러스터에 하나
card(0, YC, 72, INFO, "cilium-operator", [("CiliumNode 생성", False), ("podCIDRs 10.1.1.0/24", True), ("활성 인스턴스는 하나", False)], "§2")
card(4, YC, 72, INFO, "Hubble Relay", [("피어 연결 · 스트림 병합", False), ("Service :80 → :4245", True), ("클러스터에 하나", False)], "§6")
d.o.append(f'<rect x="{COLS[2]}" y="{YC}" width="{COLS[3] + CW - COLS[2]}" height="72" rx="5" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t((COLS[2] + COLS[3] + CW) / 2, YC + 31, "3·4 단계는 노드 안에서 끝남", 12, MUTED, KR, "middle", 600)
d.t((COLS[2] + COLS[3] + CW) / 2, YC + 51, "오퍼레이터를 거치지 않음", 11, MUTED, KR, "middle")

# 노드마다
card(0, YA, 56, ACC, "cilium-agent", [("CiliumNode 를 감시", False), ("10.1.1.0/24 수신", True)], "§2")
card(1, YA, 56, OK, "cilium-agent", [("CNI 플러그인 설치", False), ("05-cilium.conflist", True)], "§3")
card(1, YB, 56, OK, "cilium-agent", [("eBPF 적재 · 맵 고정", False), ("/sys/fs/bpf", True)], "§3")
card(2, YA, 56, OK, "cilium-cni", [("런타임이 ADD 로 실행", False), ("cilium.sock REST", True)], "§4")
card(2, YB, 56, OK, "cilium-agent", [("EndpointCreate 처리", False), ("cilium_lxc 등록", True)], "§4")
card(3, YA, 56, OK, "eBPF 프로그램", [("후크에서 패킷을 판정", False), ("tc · 6.6+ tcx", True)], "§5")
card(3, YB, 56, OK, "cilium-envoy", [("L7 규칙이 걸린 패킷", False), ("DaemonSet", True)], "§5")
card(3, YD, 56, OK, "DNS 프록시", [("UDP/TCP 53 질의", False), ("cilium_ipcache_v2", True)], "§5")
card(4, YA, 56, OK, "Hubble Server", [("이벤트에 정보 보강", False), ("cilium_events", True)], "§6")

cx = [c + CW / 2 for c in COLS]
# 1 오퍼레이터 → 에이전트: 두 층을 잇는 한 줄
d.arrow([(cx[0], YC + 72), (cx[0], YA)], ACC, "acc", 1.6)
d.t(cx[0] + 12, 352, "CiliumNode", 10, ACC, MONO, "start")
# 단계 안·사이 이음
d.arrow([(COLS[0] + CW, YA + 28), (COLS[1], YA + 28)], OK, "ok", 1.3)
d.arrow([(cx[1], YA + 56), (cx[1], YB)], OK, "ok", 1.3)
d.arrow([(COLS[1] + CW, YA + 28), (COLS[2], YA + 28)], SOFT, "soft", 1.3, "3 3")
d.arrow([(cx[2], YA + 56), (cx[2], YB)], OK, "ok", 1.3)
d.arrow([(COLS[2] + CW, YB + 28), (COLS[2] + CW + 16, YB + 28), (COLS[2] + CW + 16, YA + 28), (COLS[3], YA + 28)], OK, "ok", 1.3)
d.arrow([(cx[3], YA + 56), (cx[3], YB)], OK, "ok", 1.3)
d.arrow([(COLS[3] + CW, YA + 42), (COLS[3] + CW + 16, YA + 42), (COLS[3] + CW + 16, YD + 28), (COLS[3] + CW, YD + 28)], OK, "ok", 1.3)
d.arrow([(COLS[3] + CW, YA + 28), (COLS[4], YA + 28)], OK, "ok", 1.3)
# 5 관측: 노드 → 클러스터 → 사람
d.arrow([(cx[4], YA), (cx[4], YC + 72)], INFO, "info", 1.4)
d.t(cx[4] + 12, 352, "gRPC :4244", 10, INFO, MONO, "start")
d.arrow([(cx[4], YC), (cx[4], YH + 56)], INFO, "info", 1.4)
d.t(cx[4] + 12, 228, "흐름 제공", 11, INFO, KR, "start")

d.legend(606, [("클러스터에 하나", INFO), ("노드마다", OK), ("두 층을 잇는 한 줄", ACC), ("사람이 보는 길", MUTED)])
d.save("02-01.chapter-overview.svg")
