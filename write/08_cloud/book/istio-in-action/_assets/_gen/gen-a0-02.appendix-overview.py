# a0-02 전체 지도 — 파드와 VM 두 길이 같은 사이드카 부품 넷에 설정을 내리는 모양.
# 값 근거(본문 a0-02):
#   - §1: 사이드카 부품 넷 — istio-agent(기동·부트스트랩), 로컬 DNS 프록시, Envoy, istio-init(리디렉션).
#   - §2·§3: 파드 명세 주입 — 수동(istioctl kube-inject)과 자동(MutatingWebhookConfiguration → istiod 저장 전).
#   - §4: 파드 트래픽 돌리기 — istio-init(NET_ADMIN·NET_RAW) 또는 Istio CNI(노드 데몬셋).
#   - §5·§6: VM 설정 파일 — istioctl x workload entry configure 가 파일 다섯 생성, cluster.env 가 식별자 전달.
#   - §7: 장애 추적 — 파일 직접 수정 후 프록시 재시작 반복.
# 타입 스펙: type-architecture — 두 경로(파드·VM)가 공통 목표(사이드카 부품 넷)로 합류하는 구조.
#           좌표는 열 셋(출발·가공/적용·합류)과 행 stride 로 4의 배수 정렬.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, RULE, KR, MONO

W, H = 960, 704

d = D(W, H, "ISTIO IN ACTION · A0-02 OVERVIEW",
      "프록시는 설정을 어떻게 받는가 — 파드와 VM 의 두 길",
      "파드 길과 VM 길은 출발 환경이 다르지만 결국 같은 사이드카 부품 넷에 설정과 신원과 트래픽 경로를 넘긴다. "
      "위쪽 파드 길은 수동·자동 명세 주입과 istio-init 또는 CNI 로 트래픽을 돌리고, 아래쪽 VM 길은 다섯 파일과 "
      "cluster.env 를 거쳐 장애 시 직접 수정 고리로 이어진다.",
      lead="화살표 위 글자는 관계, 칩은 해당 절 번호, 왼쪽에서 오른쪽으로 읽습니다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, w, h, title, lines, c, sec, focal=False):
    d.tone(x, y, w, h, c, 6, "1e" if focal else "14", 1.4 if focal else 1.2)
    d.chip(x + 26, y + 16, sec, c, 11)
    d.t(x + w / 2 + 10, y + 24, title, 14, c, kr(title), "middle", 600)
    for i, s in enumerate(lines):
        d.t(x + w / 2, y + 48 + i * 18, s, 13, MUTED, kr(s), "middle")


# 구역 헤더
d.t(24, 108, "파드 경로 (쿠버네티스)", 13, INFO, KR, "start", 600)
d.line(24, 116, 636, 116, RULE, 0.8)
d.t(24, 412, "VM 경로 (클러스터 밖)", 13, INFO, KR, "start", 600)
d.line(24, 420, 636, 420, RULE, 0.8)
d.t(696, 108, "공통 목표", 13, ACC, KR, "start", 600)
d.line(696, 116, 936, 116, RULE, 0.8)

# 파드 경로 (§2, §3, §4)
node(24, 136, 224, 88, "수동 주입", ["istioctl kube-inject", "Git · CD 통제"], INFO, "§2")
node(24, 248, 224, 88, "자동 주입", ["istio-injection=enabled", "웹훅 · 저장 전 주입"], INFO, "§3")
node(388, 192, 248, 96, "트래픽 돌리기", ["istio-init (NET_ADMIN)", "또는 Istio CNI (데몬셋)"], INFO, "§4")

# 파드 주입 -> 리디렉션 -> 사이드카
d.arrow([(248, 180), (316, 180), (316, 224), (386, 224)], INFO, "info", 1.4)
d.t(316, 170, "명세 추가", 13, MUTED, KR, "middle")
d.arrow([(248, 292), (316, 292), (316, 256), (386, 256)], INFO, "info", 1.4)
d.t(316, 312, "같은 파드 정의", 13, MUTED, KR, "middle")

# VM 경로 (§5, §6, §7)
node(24, 440, 224, 92, "다섯 파일 생성", ["istioctl x workload", "entry configure"], INFO, "§5")
node(388, 440, 248, 92, "cluster.env 해석", ["meshID · cluster · network", "DNS_CAPTURE · SPIFFE"], INFO, "§6")
node(388, 568, 248, 68, "장애 추적 반복", ["직접 수정 · 프록시 재시작"], OK, "§7")

d.arrow([(248, 486), (386, 486)], INFO, "info", 1.4)
d.t(316, 474, "다섯 중 하나", 13, MUTED, KR, "middle")
d.arrow([(512, 532), (512, 566)], OK, "ok", 1.3)

# 공통 목표: 사이드카 부품 넷 (§1)
SX, SY, SW, SH = 696, 220, 240, 252
d.tone(SX, SY, SW, SH, ACC, 8, "1e", 1.5)
d.chip(SX + 28, SY + 20, "§1", ACC, 11)
d.t(SX + SW / 2 + 12, SY + 28, "사이드카 부품 넷", 15, ACC, KR, "middle", 700)
d.t(SX + SW / 2, SY + 52, "Envoy 가 못 하는 일을 분담", 13, MUTED, KR, "middle")
parts = [
    ("트래픽 리디렉션", "파드는 istio-init"),
    ("istio-agent", "Envoy 기동 · 신원 · 설정"),
    ("Envoy 프록시", "트래픽 처리"),
    ("로컬 DNS 프록시", "이름 해석 (기본 꺼짐)"),
]
for i, (nm, sub) in enumerate(parts):
    py = SY + 72 + i * 42
    d.box(SX + 16, py, SW - 32, 36, "#161B22", RULE, 0.9, 4)
    d.t(SX + 26, py + 15, nm, 12, INK, kr(nm), "start", 600)
    d.t(SX + 26, py + 30, sub, 12, MUTED, kr(sub), "start")

# 두 길이 사이드카에 합류
d.arrow([(636, 240), (652, 240), (652, 310), (694, 310)], ACC, "acc", 1.5)
d.t(666, 228, "리디렉션", 13, ACC, KR, "middle", 600)
d.arrow([(636, 486), (676, 486), (676, 352), (694, 352)], ACC, "acc", 1.5)
d.t(666, 506, "설정 전달", 13, ACC, KR, "middle", 600)

d.legend(660, [("사이드카 부품 넷", ACC), ("경로별 단계", INFO), ("장애 때 도는 반복", OK)])
d.save("a0-02.appendix-overview.svg")
print("ok overview")
