# 04-02.fib-tree — 가장 긴 접두사가 이기는 경로 트리, 그리고 없는 Pod 주소가 닿는 블랙홀
# 본문 요구: "커널은 이 규칙을 비트 단위 최적화 트리인 FIB 로 컴파일해 보관합니다 … Longest Prefix Match … 막 사라져 calixxx
#           인터페이스가 없는 IP 는 윗단의 /26 블랙홀 규칙에 걸려 즉시 폐기됩니다" (2026-11-08 Mermaid 트리를 대체)
#           블랙홀은 /26 블록 경로 자체이고 /32 Pod 경로가 그 아래에 붙는다 (Calico CalicoNodeStatus 문서)
# 타입 스펙: type-tree — 왼쪽 → 오른쪽 트리. 열은 접두사 길이(기본 경로 → /8 → /16 → /26 → /32 · 블랙홀)이고 노드는 주소 대역이다.
#           focal 은 블랙홀. 연결선은 직각 버스 하나이고 노드 높이 52, 모든 좌표는 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 464
NH = 52
COLS = [(24, 156), (220, 156), (416, 156), (612, 156), (808, 168)]

d = D(W, H, "TREE · LONGEST PREFIX MATCH",
      "가장 긴 접두사가 이기고, 없는 주소는 /26 블랙홀이 받습니다",
      "기본 경로에서 시작해 상위 8비트가 10 이면 10.0.0.0/8, 상위 16비트가 10.244 이면 Pod 대역 10.244.0.0/16 으로 내려간다. "
      "그 아래 /26 블록 셋은 워커1, 워커2, 이 노드로 갈린다. 이 노드의 블록 10.244.242.64/26 자체가 blackhole 경로이고 그 아래에 "
      "10.244.242.66/32 같은 Pod 별 경로가 calixxx 로 붙는다. calixxx 가 없는 주소는 더 긴 /32 가 없어 /26 blackhole 에서 폐기된다. "
      "10.0.0.0/8 과 10.244.0.0/16 은 분기점을 보이려는 설명용 노드이고 실제 Calico 경로가 아니다. "
      "10.244.242.66 은 Calico 예시 클러스터의 CoreDNS Pod 주소이며 다른 도식의 주소와는 다른 클러스터 예시다.",
      lead="목적지에 맞는 규칙 중 접두사가 가장 긴 것이 고른다")


def node(col, y, title, sub, c=None):
    x, w = COLS[col]
    if c:
        d.tone(x, y, w, NH, c, 6, "1F" if c == ACC else "14", 1.6 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 22, ddx.fit(title, 13, w - 16, title), 13, c or INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 40, ddx.fit(sub, 12, w - 16, sub), 12, MUTED, KR, "middle")


def bus(col_a, ya, col_b, ys):
    # 부모 오른쪽 → 세로 버스 → 자식 왼쪽
    xa = COLS[col_a][0] + COLS[col_a][1]
    xb = COLS[col_b][0]
    xm = xa + 20
    d.line(xa, ya, xm, ya, SOFT, 1.2)
    d.line(xm, min(ys + [ya]), xm, max(ys + [ya]), SOFT, 1.2)
    for y in ys:
        d.arrow([(xm, y), (xb - 4, y)], SOFT, "soft", 1.2)


# 열 머리
for c, name in enumerate(["기본 경로", "상위 8비트", "상위 16비트", "/26 블록", "/32 Pod 경로"]):
    d.t(COLS[c][0], 104, name, 12, MUTED, KR, "start", 600)

ROOT, EXT, P8 = 268, 332, 204
P16, OTH = 204, 332
B1, B2, B3 = 128, 200, 280
L1 = 280

c = lambda y: y + NH // 2
bus(0, c(ROOT), 1, [c(P8), c(EXT)])
bus(1, c(P8), 2, [c(P16), c(OTH)])
bus(2, c(P16), 3, [c(B1), c(B2), c(B3)])
bus(3, c(B3), 4, [c(L1)])

node(0, ROOT, "0.0.0.0/0", "default 게이트웨이")
node(1, P8, "10.0.0.0/8", "상위 8비트 = 10")
node(1, EXT, "그 밖의 목적지", "외부망 · ens5", INFO)
node(2, P16, "10.244.0.0/16", "Pod 대역", OK)
node(2, OTH, "그 밖의 10.x", "호스트 자기 대역", INFO)
node(3, B1, "10.244.175.0/26", "워커1 노드 IP 로", INFO)
node(3, B2, "10.244.49.64/26", "워커2 노드 IP 로", INFO)
node(3, B3, "10.244.242.64/26", "blackhole 경로", ACC)
node(4, L1, "10.244.242.66/32", "cali… Pod 별 경로", OK)

d.legend(424, [("다른 곳으로 나감", INFO), ("이 노드의 Pod 경로", OK), ("블랙홀 안전망", ACC)])
d.save("04-02.fib-tree.svg")
print("ok fib-tree")
