# a0-04 §6 도구가 그 아래에서 무엇을 부르나.
# 본문(부록 D.2.1 끝): "you will usually use the endpoints indirectly through other tools such
#       as Kiali, istioctl, and so on. For example, the istioctl proxy-status command uses the
#       /debug/syncz endpoint". D.2.2: ControlZ 는 9876, 가장 흔한 쓰임은 로깅 스코프 변경.
# 타입 스펙: type-dependency — 도구가 어느 엔드포인트에 기대는지가 논점이다. 랭크 행으로 놓고
#           팬인 배지를 단다.
#           축약: 저자가 예로 든 대응 하나만 실선으로 확정하고 나머지는 점선으로 둔다 —
#           원문이 Kiali 의 구체적 엔드포인트를 적지 않기 때문이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 616
d = D(W, H, "ISTIO IN ACTION · A0-04 §6",
      "평소에는 도구가 대신 친다",
      "운영자는 디버그 엔드포인트를 직접 치지 않고 Kiali 나 istioctl 을 통해 간접적으로 쓴다. "
      "색이 붙은 선이 저자가 예로 든 대응이고, 나머지는 원문이 구체적으로 적지 않아 점선으로 둔다.",
      "이 부록의 쓸모는 평소가 아니라 도구가 답을 못 줄 때 나옵니다")

NW, NH = 240, 64
def node(x, y, name, sub, fanin=None, focal=False, c=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 28, name, 12, ACC if focal else (c or INK), MONO, "start", 600)
    d.t(x + 16, y + 48, sub, 11, MUTED, KR, "start")
    if fanin:
        bw = len(fanin) * 7 + 12
        d.o.append(f'<rect x="{x + NW - bw - 10}" y="{y + 10}" width="{bw}" height="16" rx="2" fill="{INK}14"/>')
        d.t(x + NW - bw / 2 - 10, y + 22, fanin, 10, INK, MONO, "middle", 600)

TOP, BOT = 140, 340
node(40, TOP, "istioctl proxy-status", "동기화 여부를 본다", "0 in")
node(360, TOP, "Kiali", "메시를 그림으로 본다", "0 in")
# 이름이 길어 팬인 배지를 파고들었다. 이름을 줄이고 나머지를 부제로 내린다.
node(680, TOP, "istioctl dashboard", "controlz 로 9876 을 연다", "0 in")

node(40, BOT, "/debug/syncz", "nonce 두 개를 비교한다", "1 in", focal=True)
node(360, BOT, "그 밖의 debug 엔드포인트", "원문이 짝을 적지 않는다", None, c=INFO)
node(680, BOT, "ControlZ", "로깅 스코프 · 메모리 · 시그널", "1 in", c=INFO)

d.arrow([(160, TOP + NH), (160, BOT - 2)], ACC, "acc", 1.5)
d.t(176, BOT - 24, "저자가 든 예", 11, ACC, KR, "start", 600)
d.path(f"M 480 {TOP + NH} L 480 {BOT - 2}", MUTED, 1.2, m="ar", dash="4 3")
d.arrow([(800, TOP + NH), (800, BOT - 2)], INFO, "info", 1.4)

CY = 460
d.box(40, CY, 880, 68, PAPER2, RULE, 1.0, 6)
d.t(60, CY + 26, "ControlZ 가 담는 여덟", 11, ACC, KR, "start", 600)
d.t(60, CY + 50, "로깅 스코프 · 메모리 사용량 · 환경변수 · 프로세스 정보 · 명령줄 인자 · 버전 · 메트릭 · 시그널(SIGUSR1)", 11, INK, KR, "start")

d.t(28, 556, "가장 흔한 쓰임은 Pilot 을 디버깅할 때 로깅 스코프를 바꾸는 것이다", 11, SOFT, KR, "start")
d.legend(576, [("저자가 예로 든 대응", ACC), ("원문이 짝을 적지 않는 자리", INFO)])
d.save("a0-04.tool-mapping.svg")
