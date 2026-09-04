# a0-01 §5 오퍼레이터가 이름으로 갈라 보는 것.
# 본문(부록 A.4.2): "it is important for the name of the IstioOperator resource to match the
#       name of the installation we want to update. If the names don't match, the operator will
#       assume that the intent is to have a second control plane—which also has its uses for
#       multi-tenancy, canary upgrades, and so on."
# 타입 스펙: type-state — 설치 하나의 상태 전이가 논점이다. 시작점 · 상태 · 종료점을 두고
#           전이마다 조건 라벨을 단다.
#           축약: 같은 자극(리소스 적용)이 이름에 따라 두 상태로 갈리는 것이 이 도식의 전부라
#           되돌아오는 전이는 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 540
d = D(W, H, "ISTIO IN ACTION · A0-01 §5",
      "같은 YAML 이 이름 하나로 갱신이 되기도 새 설치가 되기도 한다",
      "오퍼레이터는 IstioOperator 리소스의 이벤트를 지켜보다가 설치를 그 정의에 맞춘다. 이때 "
      "metadata.name 이 갱신 대상을 정한다. 색이 붙은 상태가 이름이 맞았을 때 가는 자리다.",
      "이름이 다르면 컨트롤 플레인이 하나 더 서는데 저자는 그것도 쓸모가 있다고 적습니다")

SW, SH = 232, 68
def state(x, y, label, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, y + 28, label, 13, ACC if focal else (c or INK), KR, "middle", 600)
    d.t(x + SW / 2, y + 50, sub, 11, MUTED, MONO)

def lab(x, y, txt, c=MUTED):
    lw = sum(11 if '가' <= ch <= '힣' else 7 for ch in txt) + 16
    d.o.append(f'<rect x="{x - lw / 2}" y="{y - 13}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(x, y, txt, 11, c, KR, "middle", 600)

MID, TOP, BOT = 216, 132, 320
d.o.append(f'<circle cx="16" cy="{MID + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(24, MID + SH / 2), (46, MID + SH / 2)], MUTED, "ar", 1.4)

state(48, MID, "설치가 하나 서 있다", "name: control-plane")
state(440, TOP, "그 설치가 갱신된다", "accessLogEncoding: JSON", focal=True)
state(440, BOT, "둘째 컨트롤 플레인이 선다", "name: control-plane-2", INFO)

# 한 줄기가 나와 이름 판정으로 갈린다
FORK = 340
d.path(f"M 280 {MID + SH / 2} L {FORK} {MID + SH / 2}", MUTED, 1.3)
d.path(f"M {FORK} {TOP + SH / 2} L {FORK} {BOT + SH / 2}", MUTED, 1.3)
d.arrow([(FORK, TOP + SH / 2), (438, TOP + SH / 2)], ACC, "acc", 1.5)
d.arrow([(FORK, BOT + SH / 2), (438, BOT + SH / 2)], INFO, "info", 1.4)
lab(FORK + 28, TOP + SH / 2 - 18, "이름이 같다", ACC)
lab(FORK + 32, BOT + SH / 2 - 18, "이름이 다르다", INFO)

d.o.append(f'<circle cx="700" cy="{TOP + SH / 2}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="700" cy="{TOP + SH / 2}" r="5" fill="{INK}"/>')
d.arrow([(672, TOP + SH / 2), (688, TOP + SH / 2)], MUTED, "ar", 1.3)

d.t(740, TOP + SH / 2 - 6, "쓸모가 있는 갈래다", 11, INFO, KR, "start", 600)
d.t(740, TOP + SH / 2 + 16, "멀티테넌시 · 카나리 업그레이드", 11, MUTED, KR, "start")
d.path(f"M 736 {TOP + SH / 2 + 26} L 736 {BOT + SH / 2} L 676 {BOT + SH / 2}", INFO, 1.2, m="info", dash="4 3")

d.t(28, 424, "4 절에서는 이름이 겹치면 앞의 것을 지웠고 여기서는 겹쳐야 갱신된다 — 이름이 설치의 식별자라서 그렇다", 11, SOFT, KR, "start")
d.t(28, 448, "설치는 istioctl operator init 한 줄이고 그다음부터는 같은 YAML 을 kubectl apply 로 올린다", 11, MUTED, MONO, "start")
d.legend(472, [("이름이 맞았을 때 가는 자리", ACC), ("이름이 어긋났을 때 서는 것", INFO)])
d.save("a0-01.operator-name.svg")
