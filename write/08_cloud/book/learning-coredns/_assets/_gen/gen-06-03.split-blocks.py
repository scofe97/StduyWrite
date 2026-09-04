# 06-03 §6 — 클러스터 존을 서버 블록 앞으로 옮기면 질의가 어느 체인을 지나는지가 갈린다.
# 원문 근거: "By moving the CLUSTER_DOMAIN and REVERSE_CIDRS to the beginning of the server block,
#            we are telling CoreDNS that it should route queries for those zones only through this
#            set of plug-ins, which does not include the cache plug-in. Queries for other zones will
#            go through the second stanza, and so will be cached." /
#            대가: "For each zone listed at the front of the server block, CoreDNS will create an
#            independent plug-in chain. This means that the Kubernetes caches will be duplicated
#            within the CoreDNS instance, increasing the memory consumption."
# 타입 스펙: type-flowchart — 조건 하나로 갈리는 라우팅이고 분기마다 라벨을 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, INFO, KR, MONO

W, H = 880, 700
d = D(W, H, "LEARNING COREDNS · 06-03 §6",
      "질의가 어느 블록으로 가는가",
      "클러스터 존을 서버 블록 앞으로 옮기면 그 존의 질의만 캐시 없는 체인을 지난다. "
      "나머지는 두 번째 블록으로 가서 상류 TTL 대로 캐시된다.",
      "주황 대가가 이 분리의 값입니다")

LX, RX = 216, 664
BW, BH = 336, 64


def step(cx, y, title, sub, c=INK):
    d.box(cx - BW / 2, y, BW, BH, PAPER2, RULE, 1.0)
    d.t(cx, y + 26, title, 15, c, KR, "middle", 600)
    d.t(cx, y + 48, sub, 12, MUTED, KR)


def oval(cx, y, w, h, txt, c):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + h / 2 + 5, txt, 15, c, KR, "middle", 600)


oval(440, 104, 300, 48, "질의가 들어온다", MUTED)

DW, DH = 320, 84
DY = 188
d.path(f"M 440 152 L 440 {DY - 2}", MUTED, 1.4, m="ar")
d.o.append(f'<path d="M 440 {DY} L {440 + DW / 2} {DY + DH / 2} L 440 {DY + DH} L {440 - DW / 2} {DY + DH / 2} Z" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(440, DY + 38, "블록 앞에 적어 둔", 14, ACC, KR, "middle", 600)
d.t(440, DY + 58, "클러스터 존인가", 14, ACC, KR, "middle", 600)

d.path(f"M {440 - DW / 2} {DY + DH / 2} L {LX} {DY + DH / 2} L {LX} 316", MUTED, 1.4, m="ar")
d.t(LX + 12, DY + 30, "그렇다", 13, MUTED, KR, "start")
d.path(f"M {440 + DW / 2} {DY + DH / 2} L {RX} {DY + DH / 2} L {RX} 316", MUTED, 1.4, m="ar")
d.t(RX - 12, DY + 30, "아니다", 13, MUTED, KR, "end")

step(LX, 318, "첫 블록", "kubernetes · ready · loadbalance")
step(RX, 318, "둘째 블록", "forward · cache")
d.path(f"M {LX} 382 L {LX} 408", MUTED, 1.4, m="ar")
d.path(f"M {RX} 382 L {RX} 408", MUTED, 1.4, m="ar")
step(LX, 410, "cache 가 없다", "메모리의 자원에서 즉석 생성")
step(RX, 410, "cache 가 있다", "상류 TTL 대로 · 30초 상한 없음")
d.path(f"M {LX} 474 L {LX} 500", MUTED, 1.4, m="ar")
d.path(f"M {RX} 474 L {RX} 500", MUTED, 1.4, m="ar")
oval(LX, 502, 336, 48, "중복 저장이 사라진다", OK)
oval(RX, 502, 336, 48, "네트워크 왕복을 아낀다", INFO)

d.tone(20, 574, 840, 56, ACC, 6, "0E", 1.4)
d.t(440, 598, "대가 — 앞에 나열한 존마다 독립 플러그인 체인이 생겨 쿠버네티스 캐시가 중복된다", 13, ACC, KR)
d.t(440, 618, "작은 클러스터면 무시할 만하고, 큰 클러스터면 재 보고 정해야 한다", 12, MUTED, KR)

d.legend(644, [("이 분리가 치르는 값", ACC), ("클러스터 질의가 얻는 것", OK), ("바깥 질의가 얻는 것", INFO)])
d.save("06-03.split-blocks.svg")
