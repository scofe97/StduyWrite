# 01-01 §3 라이브러리 하나를 고르면 나머지가 딸려 오는 구조.
# 본문: "Hystrix 를 쓰려면 Java 나 JVM 기반이어야 합니다. 서킷 브레이킹과 로드밸런싱은 대개 함께 가므로
#       Ribbon 도 필요하고, Ribbon 으로 로드밸런싱하려면 엔드포인트를 찾을 레지스트리가 있어야 하니
#       Eureka 까지 따라옵니다. 하나를 고르면 나머지가 딸려 오는 구조입니다."
# 팬인 배지가 이 그림의 요점이다 — 모든 서비스가 같은 런타임 전제 하나로 수렴한다.
# 타입 스펙: type-dependency — 무엇이 무엇에 기대는가. 랭크 행으로 놓고 팬인 배지를 단다.
#           JVM 런타임 전제가 다중 부모를 받는 수렴점이라 tree 가 아니라 이 타입이다.
#           축약: 저자의 서술에 되돌아가는 의존(cycle)은 없으므로 back-edge 를 그리지 않고,
#           accent 는 수렴점과 그 배지에 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 01-01 §3",
      "하나를 고르면 나머지가 딸려 온다",
      "서킷 브레이킹을 쓰려고 Hystrix 를 고르면 Ribbon 이 필요하고, Ribbon 은 Eureka 를 필요로 한다. "
      "그리고 셋 모두 같은 런타임 전제 하나로 수렴한다. 색이 붙은 노드가 그 수렴점이다.",
      "언어를 바꾸면 이 그림 전체를 그 언어에서 다시 그려야 합니다")

NW, NH = 160, 56
def node(x, y, name, sub, fanin, focal=False, ext=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif ext:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{INK}05" stroke="{INK}4D" stroke-width="1"/>')
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 24, name, 12, ACC if focal else INK, KR, "start", 600)
    d.t(x + 14, y + 42, sub, 9, MUTED, MONO, "start")
    bw = len(fanin) * 6 + 10
    d.o.append(f'<rect x="{x + NW - bw - 8}" y="{y + 8}" width="{bw}" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + NW - bw / 2 - 8, y + 19, fanin, 8, INK, MONO, "middle", 600)

R0, R1, R2, R3 = 124, 244, 364, 484
XS = [64, 300, 536]
for i, nm in enumerate(["서비스 A", "서비스 B", "서비스 C"]):
    node(XS[i], R0, nm, "우리 코드", "0 in", ext=True)

node(248, R1, "Hystrix", "서킷 브레이킹 · 벌크헤딩", "3 in")
node(248, R2, "Ribbon", "클라이언트 LB", "1 in")
node(248, R3, "Eureka", "레지스트리", "1 in")
node(632, R3, "JVM 런타임 전제", "Java 또는 JVM 기반", "3 in", focal=True)

# 서비스 셋 → Hystrix
for i in range(3):
    cx = XS[i] + NW / 2
    if i == 1:
        d.arrow([(cx, R0 + NH), (cx, R1 - 2)], MUTED, "ar", 1.3)
    else:
        d.path(f"M {cx} {R0 + NH} L {cx} {R1 - 26} L {395 if i == 0 else 395} {R1 - 26} L 395 {R1 - 2}", MUTED, 1.2, m="ar")
# 라이브러리 사슬
d.arrow([(328, R1 + NH), (328, R2 - 2)], MUTED, "ar", 1.3)
d.arrow([(328, R2 + NH), (328, R3 - 2)], MUTED, "ar", 1.3)
# 세 라이브러리 → 런타임 전제
for r in (R1, R2, R3):
    d.path(f"M {300 + NW} {r + NH / 2} L 700 {r + NH / 2} L 700 {R3 + NH / 2} L {760 - 2} {R3 + NH / 2}", ACC, 1.3, m="acc")

d.t(52, R1 + 24, "서킷 브레이킹이 필요해", 11, SOFT, KR, "start")
d.t(52, R2 + 24, "그러면 LB 도 있어야 하고", 11, SOFT, KR, "start")
d.t(52, R3 + 24, "그러면 레지스트리도", 11, SOFT, KR, "start")

d.t(28, 576, "언어를 추가하면 대응 패키지를 언어마다 찾아 검증해야 하고, 아예 못 찾는 조합도 생긴다", 11, SOFT, KR, "start")
d.legend(600, [("모두가 수렴하는 전제", ACC), ("우리가 쓰는 쪽", MUTED)])
d.save("01-01.library-coupling.svg")
