# 02-01.netns-isolation — 네임스페이스마다 따로 두는 것과 전역 한 벌에 표식으로 가르는 것
# 본문 요구: "인터페이스 목록·loopback·라우팅·netfilter 훅은 struct net 안에 따로,
#            소켓 해시와 ARP 이웃 테이블은 전역 한 벌에 소속 표식" + "세 네임스페이스가 모두 8080"
# 타입 스펙: type-nested — 노드 링 안에 네임스페이스 링 셋, 그 아래 전역 표 하나가 셋을 가로지른다.
#           열이 네임스페이스, 행이 자료구조다. 윗단은 열마다 상자가 따로라 '한 벌씩'이 자리로 보이고,
#           아랫단은 한 상자가 세 열을 가로질러 '함께 쓰는 한 벌'이 자리로 보인다.
# 2026-09-21 손으로 쓴 SVG(생성기 없음)와 본문 mermaid 를 이 한 장으로 합쳤다. 둘 다 '소켓 해시가
#            struct net 마다 따로'라고 그렸으나 커널 소스는 전역 tcp_hashinfo 하나에 bind 버킷마다
#            ib_net 을 달고 inet_bind_bucket_match() 가 net_eq() 로 가른다. ARP 도 전역 arp_tbl 하나이고
#            struct neighbour 에는 net 필드 없이 dev 만 있다 — 장치가 한 네임스페이스에 속해 갈린다.
#            그래서 두 줄을 아랫단으로 내리고, 가르는 단서를 줄마다 다르게 적었다(표식 · 장치).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 612
d = D(W, H, "NETNS · struct net",
      "네트워크 네임스페이스 격리 — struct net 안에 따로, 전역 표는 소속으로 가른다",
      "열은 네임스페이스 셋, 행은 자료구조다. 인터페이스·라우팅·netfilter 는 네임스페이스마다 struct net 안에 한 벌씩 있고, "
      "소켓 해시와 ARP 이웃 테이블은 커널 전체가 한 벌을 쓴다. 소켓 항목은 소속 네임스페이스 표식으로, ARP 항목은 매달린 장치로 가른다. "
      "세 네임스페이스가 같은 8080, 두 Pod 가 같은 10.244.1.1 과 eth0 을 가져도 소속이 달라 부딪치지 않는다.",
      lead="같은 8080 · 같은 10.244.1.1 이어도 소속이 다르면 부딪치지 않는다")

GX = 48                                   # 행 이름 칸
COLX, CW = [192, 456, 720], 240           # stride 264 · 링 사이 24
CX = [x + CW // 2 for x in COLX]
# 링 폭이 240 이라 테두리 위 이름표(ring_label 마스크)는 shape-overlap 으로 잡힌다 — 이름을 링 안쪽 머리에 쓴다
RING_Y, RING_H = 152, 200                 # 152~352
ROW_TOP, ROW_H = [192, 244, 296], 40      # stride 52
G_Y, G_H = 392, 132                       # 전역 한 벌 392~524
SOCK_Y, ARP_Y, ENT_H = 420, 472, 40

ddx.band(d, 104, 540, "한 리눅스 노드 · 커널 하나")

# 윗단 — 네임스페이스마다 따로
d.t(GX, RING_Y + 24, "struct net 안", 11, SOFT, KR, "start", 600)
for y, lab in zip(ROW_TOP, ["인터페이스", "라우팅", "netfilter"]):
    d.t(GX, y + ROW_H // 2 + 4, lab, 12, MUTED, KR if lab != "netfilter" else MONO, "start")

NS = [("root netns",  ["eth0 10.0.0.10 · lo",  "default via 10.0.0.1",   "kube-proxy 규칙"]),
      ("pod-a netns", ["eth0 10.244.1.5 · lo", "default via 10.244.1.1", "비어 있음"]),
      ("pod-b netns", ["eth0 10.244.1.6 · lo", "default via 10.244.1.1", "비어 있음"])]
for x, cx, (name, cells) in zip(COLX, CX, NS):
    d.o.append(f'<rect x="{x}" y="{RING_Y}" width="{CW}" height="{RING_H}" rx="8" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    d.t(x + 16, RING_Y + 24, name, 12, INFO, MONO, "start", 600)
    for y, c in zip(ROW_TOP, cells):
        d.box(x + 16, y, CW - 32, ROW_H, PAPER2, RULE, 1.0, 6)
        mono = all(ord(ch) < 128 or ch == '·' for ch in c)
        d.t(cx, y + ROW_H // 2 + 4, ddx.fit(c, 12, CW - 48, c), 12, INK if mono else MUTED,
            MONO if mono else KR)

# 아랫단 — 전역 한 벌 · 항목마다 표식
d.t(GX, G_Y + 16, "커널 전역 한 벌", 11, SOFT, KR, "start", 600)
for y, lab, how in [(SOCK_Y, "소켓 해시", "표식으로 가름"), (ARP_Y, "ARP 이웃", "장치로 가름")]:
    d.t(GX, y + ENT_H // 2 - 2, lab, 12, MUTED, KR, "start")
    d.t(GX, y + ENT_H // 2 + 14, how, 11, SOFT, KR, "start")
d.box(COLX[0], G_Y, COLX[-1] + CW - COLX[0], G_H, PAPER2, MUTED, 1.1, 8)

EX, EW = COLX[0] + 12, COLX[-1] + CW - COLX[0] - 24
d.o.append(f'<rect x="{EX}" y="{SOCK_Y}" width="{EW}" height="{ENT_H}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.box(EX, ARP_Y, EW, ENT_H, PAPER, RULE, 1.0, 6)
for cx, tag, gw in zip(CX, ["root", "pod-a", "pod-b"], ["10.0.0.1", "10.244.1.1", "10.244.1.1"]):
    d.t(cx, SOCK_Y + ENT_H // 2 + 4, ddx.fit(f"net={tag} · :8080", 12, CW - 24), 12, ACC, MONO)
    d.t(cx, ARP_Y + ENT_H // 2 + 4, ddx.fit(f"{gw} · eth0", 12, CW - 24), 12, INK, MONO)

# 표식이 가리키는 소속 — 링 아래에서 해당 항목까지 세로로
for cx in CX:
    d.line(cx, RING_Y + RING_H + 4, cx, SOCK_Y - 4, ACC, 1.2, "3 4")
d.t(CX[0] + 10, RING_Y + RING_H + 28, "소속 표식", 11, ACC, KR, "start")

d.legend(556, [("struct net 안 · 네임스페이스마다", INFO), ("커널 전역 한 벌", MUTED),
               ("bind 가 표식으로 가르는 자리", ACC)])
d.save("02-01.netns-isolation.svg")
print("ok 02-01.netns-isolation")
