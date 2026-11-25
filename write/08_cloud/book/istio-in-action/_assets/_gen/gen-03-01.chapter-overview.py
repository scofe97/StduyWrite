# 03-01 학습 목표 뒤 줄기 그림(개념도) — 요청 한 건이 Envoy 를 지나는 길(가운데)과 그 길을 정하는 설정 두 갈래(정적 파일 vs xDS·ADS) 및 Istio 부양을 한 장에 잇는다.
# 값 근거: 03-01 본문 §1~§7 — downstream → Listener(:15001) → Route → Cluster → upstream(§2),
#          정적 YAML · xDS(LDS/RDS/CDS/EDS/SDS/ADS)(§5), Admin API(:15000)(§6), istiod·텔레메트리(§7).
# 공식 근거: Envoy v3 xDS/ADS, Istio 1.5+ istiod (03-01 본문 각주).
# 타입 스펙: type-architecture — 구성요소를 존으로 묶고 직각 화살표(d.arrow)로 잇는 노드 그래프.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 984, 688


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 03-01 OVERVIEW",
      "Envoy가 요청을 넘기고 Istio가 그 Envoy에 설정을 댄다",
      "3장의 줄기 그림. 가운데 데이터 플레인의 Envoy 코어에서 요청이 downstream → Listener → Route → Cluster → upstream 으로 흐른다. "
      "위쪽에서는 정적 설정 파일과 동적 xDS(ADS) 두 길이 설정을 댄다. Istio의 istiod는 Kubernetes API를 읽어 xDS로 설정·디스커버리·인증서를 대 주고, "
      "텔레메트리 연동 설정으로 Envoy 메트릭과 스팬이 Prometheus·Jaeger로 흐르게 한다. 아래쪽에는 앱 잔여 책임(§3), Admin API(:15000, §6), 관측 백엔드(§7)가 이어진다.",
      lead="화살표는 관계, 칩은 해당 절입니다. 가운데가 요청의 길, 위쪽이 설정과 부양의 길입니다.")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.12)" stroke-width="0.9"/>')
    lw = len(label) * 12 + 20
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="20" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 18, label, 13, SOFT, KR, "middle", 600)


def node(x, y, w, h, title, sub, c, sec, focal=False, sub2=None):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "1e", 1.4)
    else:
        d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, ACC if focal else c, 11)
    d.t(x + w / 2, y + 38, title, 14, ACC if focal else c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 76, sub2, 13, MUTED, kr(sub2), "middle")


# 존 (배경 → 존 → 화살표 → 노드)
zone(24, 100, 936, 176, "설정 공급과 부양 (컨트롤 플레인 · 정적 파일)")
zone(204, 316, 540, 176, "요청의 길 (데이터 플레인 · Envoy 프로세스 밖 L7)")

# 위 존 노드 좌표
K8 = (40, 144, 192, 92)      # Kubernetes API
IS = (284, 136, 212, 108)    # istiod (focal)
XDS = (548, 144, 184, 92)    # xDS / ADS
ST = (776, 144, 168, 92)     # 정적 설정 파일

# 가운데 존 노드 좌표
DN = (24, 384, 132, 76)      # downstream
LS = (224, 384, 140, 76)     # Listener
RT = (400, 384, 152, 76)     # Route
CL = (584, 384, 144, 76)     # Cluster
UP = (812, 384, 148, 76)     # upstream

# 아래 노드 좌표 (각자 연관 노드 바로 아래)
AP = (24, 536, 224, 68)      # 앱 잔여 책임 (downstream 아래)
AD = (292, 536, 224, 68)     # Admin API (Listener/Route 아래)
TL = (568, 536, 220, 68)     # 관측 백엔드 (Cluster 아래)

def cx(r): return r[0] + r[2] / 2
def cy(r): return r[1] + r[3] / 2

# 화살표 (노드보다 먼저 — 전부 d.arrow 직각 좌표)
# 1) 위 존 가로 흐름: K8 -> istiod -> xDS/ADS
d.arrow([(K8[0] + K8[2], cy(K8)), (IS[0] - 2, cy(IS))], ACC, "acc", 1.3)
d.t((K8[0] + K8[2] + IS[0]) / 2, cy(K8) - 10, "의도", 13, MUTED, KR)
d.arrow([(IS[0] + IS[2], cy(IS)), (XDS[0] - 2, cy(XDS))], ACC, "acc", 1.4)
d.t((IS[0] + IS[2] + XDS[0]) / 2, cy(IS) - 10, "직렬화", 13, MUTED, KR)

# 2) 설정 내려감: xDS/ADS -> Route/Cluster, 정적 파일 -> Cluster
# 설정은 Listener·Route·Cluster 한 요소가 아니라 Envoy 프로세스 전체에 닿으므로 화살표 끝을 요청의 길 존 테두리(y=316)에 둔다.
d.arrow([(cx(XDS), XDS[1] + XDS[3]), (cx(XDS), 314)], OK, "ok", 1.4)
d.t(cx(XDS) - 12, 290, "xDS·ADS 동적 설정", 13, OK, KR, "end", 600)
d.arrow([(cx(ST), ST[1] + ST[3]), (cx(ST), 300), (700, 300), (700, 314)], MUTED, "ar", 1.2)
d.t(cx(ST) - 12, 290, "몇 대뿐이면 정적 파일", 13, MUTED, KR, "end")

# 3) 가운데 요청 경로: downstream -> Listener -> Route -> Cluster -> upstream
for a, b in ((DN, LS), (LS, RT), (RT, CL), (CL, UP)):
    d.arrow([(a[0] + a[2], cy(a)), (b[0] - 2, cy(b))], INFO, "info", 1.5)
d.t((DN[0] + DN[2] + LS[0]) / 2, cy(DN) - 10, "호출", 13, INFO, KR)
d.t((CL[0] + CL[2] + UP[0]) / 2, cy(CL) - 10, "전달", 13, INFO, KR)

# 4) 아래 연결: 각자 바로 위 노드에서 수직/ㄱ자 하강 (교차 없음)
d.arrow([(cx(DN), DN[1] + DN[3]), (cx(DN), AP[1] - 2)], INFO, "info", 1.2)
d.t(cx(DN) + 12, 514, "직접 처리", 13, INFO, KR, "start")

# 관측 출력도 개별 노드가 아니라 요청의 길 존(Envoy 전체)에서 나온다.
d.arrow([(cx(AD), 492), (cx(AD), AD[1] - 2)], OK, "ok", 1.3)
d.t(cx(AD) + 12, 516, "카운터 노출", 13, OK, KR, "start")

d.arrow([(cx(TL), 492), (cx(TL), TL[1] - 2)], MUTED, "ar", 1.2)
d.t(cx(TL) + 12, 516, "메트릭·스팬", 13, MUTED, KR, "start")

# 노드 배치
node(*K8, "Kubernetes API", "VirtualService · 레지스트리", MUTED, "§7")
node(*IS, "istiod", "설정 · 디스커버리 · 인증서", ACC, "§7", focal=True, sub2="텔레메트리 연동 설정")
node(*XDS, "xDS · ADS", "LDS·RDS·CDS·EDS·SDS", OK, "§5")
node(*ST, "정적 설정 파일", "JSON · YAML", MUTED, "§5·6")

node(*DN, "downstream", "호출 앱 · curl", INFO, "§1·2")
node(*LS, "Listener", "입구 · 포트", INFO, "§2")
node(*RT, "Route", "규칙 · 타임아웃 · 재시도", INFO, "§2·3")
node(*CL, "Cluster", "디스커버리 · LB · 이상치", INFO, "§2·3")
node(*UP, "upstream", "대상 서비스", INFO, "§2")

node(*AP, "앱 잔여 책임", "재시도 정책 · B3 전파", INFO, "§3")
node(*AD, "Admin API (:15000)", "/stats · /config_dump", OK, "§6")
node(*TL, "관측 백엔드", "Prometheus · Jaeger", MUTED, "§7")

d.chip(722, 332, "§4", MUTED, 11)
d.legend(H - 40, [("요청 경로 · 프록시", INFO), ("설정·관측 대응", OK), ("Istio 부양 중심", ACC), ("대안 · 외부 백엔드", MUTED)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01 chapter-overview")
