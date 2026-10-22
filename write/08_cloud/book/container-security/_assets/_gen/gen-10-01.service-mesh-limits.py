# 타입 스펙: type-architecture — 왼쪽 존에 사이드카가 주입된 파드 둘과 그 사이의 mTLS 경로(서비스 메시가 주는 것), 오른쪽 존에 사이드카 없는 파드와 침해된 파드의 직접 트래픽(못 주는 것)을 놓고 각 한계 밑에 보완 수단을 단다. focal 은 오른쪽 "못 주는 것" 존.
# 사실 출처: 노트 L249(사이드카 컨테이너 주입 · 파드를 드나드는 모든 트래픽이 프록시를 거침 · 사용자 공간), L251(상호 TLS), L245·L253(L5~L7 정책), L259~L262(두 가지 한계 · 보완 수단 둘), L268(CAP_NET_ADMIN 제거)
# Layout conventions: 존 y=96 h=272(왼쪽 x=24 w=448, 오른쪽 x=504 w=432), 파드 x=40·272 w=184 y=136~344, 노드 높이 56, 오른쪽 행 y=144·256 · 보완 칩 cy=224·336. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, KR, MONO

W, H = 960, 456


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 10-01 §6",
      "서비스 메시는 사이드카가 있는 파드의 서비스 경로만 지키고, 나머지는 보완 수단이 맡습니다",
      "왼쪽: 사이드카가 주입된 두 파드의 앱 컨테이너가 사이드카 프록시를 거쳐 상호 TLS 로 통신하고, 프록시는 L5~L7 정책을 강제한다. "
      "오른쪽: 사이드카가 없는 파드는 보호 범위 밖이고, 침해된 파드가 서비스 IP 를 거치지 않고 보내는 직접 트래픽은 기저 인프라를 지키지 못한다. "
      "각각 주입 확인 도구와 L3·L4 네트워크 정책이 보완한다.",
      lead="서비스 메시가 주는 보호와 닿지 않는 곳을 나란히 놓았습니다.")

ZY, ZH = 96, 272

# ── 존 ──
d.o.append(f'<rect x="24" y="{ZY}" width="448" height="{ZH}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="5 5"/>')
d.t(40, ZY + 24, "서비스 메시가 주는 것", 13, INK, KR, "start", 600)
d.o.append(f'<rect x="504" y="{ZY}" width="432" height="{ZH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(520, ZY + 24, "서비스 메시가 못 주는 것", 13, ACC, KR, "start", 600)


def node(x, y, w, h, t1, t2, c=None, dash=False):
    fit(t1, 14, w - 16)
    fit(t2, 13, w - 16)
    ds = ' stroke-dasharray="5 4"' if dash else ""
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"{ds}/>')
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + h / 2 - 4, t1, 14, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, t2, 13, MUTED, kr(t2), "middle")


# ── 왼쪽: 파드 둘 ──
for px, name in ((40, "파드 A"), (272, "파드 B")):
    d.o.append(f'<rect x="{px}" y="136" width="184" height="208" rx="8" fill="none" stroke="{RULE}" stroke-width="1"/>')
    d.t(px + 12, 158, name, 13, MUTED, KR, "start", 600)

# 화살표(노드보다 먼저)
d.arrow([(132, 236), (132, 260)], OK, "ok", 1.6)      # 앱 A → 사이드카 A
d.arrow([(364, 260), (364, 236)], OK, "ok", 1.6)      # 사이드카 B → 앱 B
d.arrow([(216, 292), (280, 292)], OK, "ok", 1.8)      # 사이드카 사이

for ax in (52, 284):
    node(ax, 176, 160, 56, "앱 컨테이너", "CAP_NET_ADMIN 제거")
    node(ax, 264, 160, 56, "사이드카 프록시", "L5~L7 · 사용자 공간", c=OK)
d.chip(248, 266, "mTLS", OK, 13)

# ── 오른쪽: 한계 둘과 보완 ──
d.arrow([(676, 172), (764, 172)], BAD, "bad", 1.6, "5 4")
d.arrow([(676, 284), (764, 284)], BAD, "bad", 1.6, "5 4")
d.t(720, 160, "프록시 없음", 13, BAD, KR, "middle", 600)
d.t(720, 272, "서비스 IP 우회", 13, BAD, KR, "middle", 600)

node(520, 144, 152, 56, "앱 컨테이너", "주입 안 된 파드")
node(768, 144, 152, 56, "보호 범위 밖", "주입된 파드만 보호", c=BAD, dash=True)
node(520, 256, 152, 56, "침해된 파드", "직접 트래픽")
node(768, 256, 152, 56, "기저 인프라", "서비스 수준 정책 밖", c=BAD, dash=True)
d.chip(844, 224, "보완: 주입 확인 도구", OK, 13)
d.chip(844, 336, "보완: L3·L4 정책", OK, 13)

d.legend(408, [("서비스 메시가 막는 경로 · 보완 수단", OK), ("보호가 닿지 않는 곳", BAD), ("못 주는 것 영역", ACC)])
d.save(str(ASSETS / "10-01.service-mesh-limits.svg"))
print("ok 10-01 service-mesh-limits")
