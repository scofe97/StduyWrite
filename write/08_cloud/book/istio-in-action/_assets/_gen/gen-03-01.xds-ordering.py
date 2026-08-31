# 03-01 §5 xDS 순서 경쟁 — RDS 와 CDS 가 따로 도착할 때와 ADS 로 묶일 때.
# 본문: "Envoy가 RDS로 새 라우트를 받았는데 그 라우트가 가리키는 cluster foo 는 아직 CDS로 오지 않았다.
# CDS가 갱신될 때까지 라우팅 오류. ADS는 모든 변경을 스트림 하나에 순서대로 싣는다. Istio는 ADS를 쓴다."
# 타입 스펙: type-sequence — 주체 둘(xDS 서버 · Envoy) 사이의 시간순 메시지. alt 프레임 하나에 두 구간.
#           coral 은 두 번째 구간의 마지막 상태 하나(Istio의 선택).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = Seq(W, H, "ISTIO IN ACTION · 03-01 §5",
        "RDS와 CDS가 따로 올 때와 ADS로 묶일 때",
        "위 구간: RDS 가 cluster foo 를 가리키는 라우트를 먼저 보내고 CDS 가 뒤늦게 foo 를 보내 그 사이 라우팅 오류가 난다. "
        "아래 구간: ADS 스트림 하나가 CDS 를 먼저, RDS 를 뒤에 실어 오류 구간이 없다.",
        "xDS는 최종 일관성 위에 있어 개별 스트림은 순서를 보장하지 않는다. Istio가 ADS를 고른 이유")

LX = d.lanes([("xDS 서버", "istiod · gRPC stream"), ("Envoy", "service proxy")], y0=104, lane_w=210)
XS, XE = LX["xDS 서버"], LX["Envoy"]
d.rails(500)

def push(label, y, c=MUTED, mk="ar"):
    d.path(f"M {XS + 10} {y} L {XE - 12} {y}", c, 1.5, m=mk)
    d.t((XS + XE) / 2, y - 8, label, 12, c, KR)

def state(txt, y, c, w):
    d.o.append(f'<rect x="{XE - w / 2}" y="{y - 12}" width="{w}" height="24" rx="5" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(XE, y + 4, txt, 12, c, KR)

# alt 프레임 — 레일 바깥 60px 안쪽
FX, FY, FH = XS - 68, 172, 316
FW = (XE + 104) - FX          # 오른쪽 변이 상태 상자(XE ± 92)보다 바깥에 오게
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="rgba(245,245,245,0.04)" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="40" height="16" rx="2" fill="{PAPER}" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.t(FX + 20, FY + 12, "ALT", 8, MUTED, MONO)
d.t(XS + 20, FY + 34, "[RDS · CDS 스트림이 따로]", 12, SOFT, KR, "start")   # 가드는 왼쪽 레일 오른쪽에

push("RDS: route → cluster foo", 236)
state("foo 없음 → 라우팅 오류", 272, WARN, 184)
push("CDS: cluster foo", 308)
state("수렴", 340, INFO, 72)

DIV = 364
d.line(FX + 8, DIV, FX + FW - 8, DIV, "rgba(245,245,245,0.20)", 1.0, "4 3")
d.t(XS + 20, DIV + 22, "[ADS 스트림 하나]", 12, SOFT, KR, "start")

push("ADS: CDS(cluster foo)", 412)
push("ADS: RDS(route → foo)", 448)
state("오류 구간 없이 수렴", 480, ACC, 168)

d.legend(516, [("오류 구간", WARN), ("수렴", INFO), ("Istio의 선택", ACC)])
d.save("03-01.xds-ordering.svg")
print("h 필요:", 516 + 22 + 16, " 실제:", H)
