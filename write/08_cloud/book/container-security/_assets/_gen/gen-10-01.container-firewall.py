# 타입 스펙: type-architecture — 최종 사용자 · 상품 검색 컨테이너 · 상품 DB 로 이어지는 허용 경로와, 검색 컨테이너에서 결제 게이트웨이로 가는 차단 경로를 한 장에 놓아 "통신할 이유 없음이 곧 규칙" 임을 보인다. focal 은 방화벽 존 안의 검색 컨테이너.
# 사실 출처: 노트 L40~L46(작은 구성 요소의 정상 동작 정의 · 전자상거래 예 · 네트워크 정책 · 규칙 밖 연결 시도 보고)
# Layout conventions: 존 x=336 y=100 w=288 h=200(방화벽), 노드 높이 72(주 행 y=164), 차단 행 y=340 h=64, 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W, H = 960, 496


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 10-01 §1",
      "상품 검색 컨테이너가 말할 상대는 둘뿐이고, 나머지는 이유 없음이 곧 규칙입니다",
      "최종 사용자의 검색 요청이 상품 검색 컨테이너로 들어가고, 검색 컨테이너는 상품 데이터베이스를 조회한다. "
      "검색 컨테이너에서 결제 게이트웨이로 향하는 경로는 컨테이너 방화벽이 차단하고, 규칙 밖 연결 시도는 보고된다.",
      lead="컨테이너 방화벽은 승인된 목적지로만 트래픽이 흐르게 제한합니다.")

# 방화벽 존 — 검색 컨테이너를 드나드는 트래픽을 감싼다
ZX, ZY, ZW, ZH = 336, 100, 288, 200
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="5 5"/>')
d.t(ZX + 16, ZY + 26, "컨테이너 방화벽", 13, INK, KR, "start", 600)
d.t(ZX + 16, ZY + 44, "네트워크 정책", 13, MUTED, KR, "start")

NH, NY = 72, 164
CY = NY + NH // 2

# 화살표(노드보다 먼저)
d.arrow([(232, CY), (364, CY)], OK, "ok", 1.6)
d.arrow([(592, CY), (724, CY)], OK, "ok", 1.6)
d.t(298, CY - 12, "검색 요청", 13, MUTED, KR, "middle", 600)
d.t(658, CY - 12, "조회", 13, MUTED, KR, "middle", 600)
d.arrow([(480, NY + NH + 4), (480, 336)], BAD, "bad", 1.8, "5 4")
d.arrow([(504, 316), (816, 316), (816, 340)], WARN, "warn", 1.4, "5 4")
d.t(496, 284, "통신할 이유 없음", 13, BAD, KR, "start", 600)

# 노드
def node(x, y, w, h, t1, t2, c=None, focal=False, dash=False):
    fit(t1, 14, w - 16)
    fit(t2, 13, w - 16)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
    elif c:
        ds = ' stroke-dasharray="5 4"' if dash else ""
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"{ds}/>')
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + h / 2 - 4, t1, 14, ACC if focal else (c or INK), KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, t2, 13, MUTED, KR, "middle")


node(56, NY, 176, NH, "최종 사용자", "검색 요청 발신")
node(368, NY, 224, NH, "상품 검색 컨테이너", "마이크로서비스 하나", focal=True)
node(728, NY, 176, NH, "상품 데이터베이스", "조회 대상")
node(368, 340, 224, 64, "결제 게이트웨이", "통신 이유 없음", c=BAD, dash=True)
node(728, 340, 176, 64, "연결 시도 보고", "조사 근거로 남음", c=WARN)

d.chip(480, 316, "차단", BAD, 13)

d.legend(448, [("허용 경로", OK), ("차단 경로", BAD), ("보고", WARN), ("정상 동작을 정의한 단위", ACC)])
d.save(str(ASSETS / "10-01.container-firewall.svg"))
print("ok 10-01 container-firewall")
