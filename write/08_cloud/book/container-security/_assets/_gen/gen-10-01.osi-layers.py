# 타입 스펙: type-layers — 위에서 아래로 L7 · L4 · L3 · L2 · L1 다섯 층. 오른쪽 열에 보안 수단이 걸치는 층 범위를 막대로 놓아, 서비스 메시(L5~L7)와 네트워크 정책(L3·L4)이 서로 겹치지 않음을 보인다. focal 은 두 수단 사이의 "겹치지 않음" 경계.
# 사실 출처: 노트 L22(네트워크 정책 L3·L4 netfilter · 서비스 메시 L5~L7 사이드카), L54(API 방화벽 · WAF L7), L66~L72(계층 표), L76·L89(L1·L2 는 컨테이너에서 가상), L173(netfilter 는 커널 · 호스트 수준), L249(프록시 규칙은 사용자 공간)
# Layout conventions: 층 x=48 w=496 h=56 stride 72(y=220·292·364·436), L7 만 y=100, L7 과 L4 사이 L6·L5 틈 y=156~220. 오른쪽 막대 열 A x=584 w=176, 열 B x=776 w=152. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 960, 572


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "LAYERS · 10-01 §2",
      "서비스 메시는 L5~L7, 네트워크 정책은 L3·L4 에서 막아 서로 겹치지 않습니다",
      "위에서 아래로 L7 애플리케이션, L4 전송, L3 네트워크, L2 데이터 링크, L1 물리. 서비스 메시는 L5~L7 의 사이드카 프록시, "
      "네트워크 정책은 L3 와 L4 의 netfilter 규칙에서 동작하고, API 방화벽과 WAF 는 L7 에서 동작한다.",
      lead="계층마다 오가는 것과 주소가 다르고, 보안 수단은 그 계층에 걸립니다.")

LX, LW, LH = 48, 496, 56
ROWS = [
    (100, "L7", "애플리케이션", "웹 요청 · REST API", "URL · DNS", INFO),
    (220, "L4", "전송", "TCP · UDP 패킷", "포트 번호", INFO),
    (292, "L3", "네트워크", "IP 패킷", "IP 주소", INFO),
    (364, "L2", "데이터 링크", "이더넷 프레임", "MAC 주소 · ARP", SOFT),
    (436, "L1", "물리", "인터페이스", "가상일 수 있음", SOFT),
]
for y, tag, name, flow, addr, c in ROWS:
    fit(flow, 13, 200)
    d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.0"/>')
    d.t(LX + 16, y + 22, tag, 10, SOFT, MONO, "start")
    d.t(LX + 16, y + 44, name, 15, INK, KR, "start", 600)
    d.t(LX + LW - 16, y + 24, flow, 13, INK, kr(flow), "end", 600)
    d.t(LX + LW - 16, y + 44, addr, 13, MUTED, kr(addr), "end")

# L7 과 L4 사이 — 표에서 생략된 두 층
d.line(LX + 16, 188, LX + LW / 2 - 112, 188, RULE, 0.8, "3 5")
d.line(LX + LW / 2 + 112, 188, LX + LW - 16, 188, RULE, 0.8, "3 5")
d.chip(LX + LW / 2, 188, "L6 · L5 는 표에서 생략", SOFT, 13)

# 오른쪽 막대 — 보안 수단이 걸치는 층 범위
def bar(x, y0, y1, w, t1, t2, c, mono1=False):
    fit(t1, 13, w - 16)
    fit(t2, 13, w - 16)
    d.o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{y1 - y0}" rx="6" fill="{c}1A" stroke="{c}" stroke-width="1.2"/>')
    mid = (y0 + y1) / 2
    d.t(x + w / 2, mid - 2, t1, 13, INK, MONO if mono1 else KR, "middle", 600)
    d.t(x + w / 2, mid + 18, t2, 13, MUTED, kr(t2), "middle")


bar(584, 100, 204, 176, "서비스 메시", "L5~L7 · 사용자 공간", OK)
bar(584, 220, 348, 176, "네트워크 정책", "L3 · L4", OK)
bar(776, 100, 156, 152, "API 방화벽 · WAF", "L7", MUTED, mono1=False)
bar(776, 220, 348, 152, "netfilter 규칙", "커널 · 호스트 수준", MUTED)
bar(584, 364, 492, 344, "컨테이너에서는 가상", "소프트웨어 브리지 · 가상 이더넷", SOFT)

# focal — 두 수단 사이 경계
d.line(584, 212, 928, 212, ACC, 1.4, "6 5")
d.chip(852, 184, "겹치지 않음", ACC, 13)

d.legend(524, [("계층", INFO), ("가상 계층", SOFT), ("사이드카 · 정책 수단", OK), ("전통 방화벽 · 커널 규칙", MUTED), ("겹치지 않는 경계", ACC)])
d.save(str(ASSETS / "10-01.osi-layers.svg"))
print("ok 10-01 osi-layers")
