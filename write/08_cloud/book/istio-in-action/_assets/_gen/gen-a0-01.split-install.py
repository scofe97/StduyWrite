# a0-01 §4 두 번째 리소스에서 프로파일과 이름을 고르는 판단.
# 본문(부록 A.3): 두 번째에 demo 를 쓰면 "it will re-install all the previously applied resources,
#       such as the roles and role bindings, custom resource definitions, and configuration,
#       thus interfering with the previous installation". 그래서 empty 를 쓴다.
#       이름은 "must be different from the previous installation. Otherwise, it would override
#       the installation and remove the control-plane components."
# 타입 스펙: type-flowchart — 판단 둘과 그 결과가 논점이다. 시작·끝은 타원, 단계는 사각,
#           판단은 마름모, 예는 오른쪽 아니오는 아래, 모든 갈래에 라벨.
#           축약: accent 는 저자가 권하는 갈래 하나에만 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 752
d = D(W, H, "ISTIO IN ACTION · A0-01 §4",
      "두 번째 리소스에서 갈리는 판단 둘",
      "컨트롤 플레인을 깐 뒤 게이트웨이를 따로 더할 때 프로파일과 이름을 각각 골라야 한다. "
      "둘 중 하나만 어긋나도 앞의 설치가 망가진다. 색이 붙은 갈래가 저자가 적은 절차다.",
      "둘 다 지켰을 때만 앞의 설치가 그대로 남습니다")

CA, CB = 268, 736

def oval(x, y, w, h, label, sub=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 22)
    c = ACC if focal else INK
    if sub:
        d.t(x + w / 2, y + h / 2 - 2, label, 13, c, KR, "middle", 600)
        d.t(x + w / 2, y + h / 2 + 18, sub, 11, MUTED, MONO)
    else:
        d.t(x + w / 2, y + h / 2 + 5, label, 13, c, KR, "middle", 600)

def step(x, y, w, h, label, sub, c=None):
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, label, 13, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 11, MUTED, KR, "middle")

def diamond(cx, cy, l1, l2):
    d.o.append(f'<polygon points="{cx},{cy - 56} {cx + 168},{cy} {cx},{cy + 56} {cx - 168},{cy}" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy - 4, l1, 12, INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, INK, KR, "middle", 600)

oval(CA - 168, 112, 336, 60, "컨트롤 플레인은 이미 깔려 있다", "profile: demo · name: control-plane")
diamond(CA, 268, "두 번째의 프로파일이", "empty 인가")
step(CB - 164, 236, 328, 64, "앞의 리소스가 다시 깔린다", "롤 · CRD · 설정이 재설치된다", BAD)
diamond(CA, 452, "두 번째의 이름이", "앞과 다른가")
step(CB - 164, 420, 328, 64, "앞의 설치를 덮어쓴다", "컨트롤 플레인 컴포넌트가 사라진다", BAD)
oval(CA - 168, 596, 336, 60, "게이트웨이만 따로 선다", "profile: empty · name: ingress-gateway", focal=True)

d.arrow([(CA, 172), (CA, 208)], MUTED, "ar", 1.4)
d.arrow([(CA + 168, 268), (CB - 166, 268)], BAD, "bad", 1.4)
d.arrow([(CA, 324), (CA, 392)], MUTED, "ar", 1.4)
d.arrow([(CA + 168, 452), (CB - 166, 452)], BAD, "bad", 1.4)
d.arrow([(CA, 508), (CA, 592)], ACC, "acc", 1.5)

d.t((CA + CB) / 2, 254, "아니오", 12, BAD, KR, "middle", 600)
d.t((CA + CB) / 2, 438, "아니오", 12, BAD, KR, "middle", 600)
d.t(CA + 20, 360, "예", 12, MUTED, KR, "start", 600)
d.t(CA + 20, 556, "예", 12, ACC, KR, "start", 600)

d.t(28, 688, "저자가 이 절차를 권하는 이유 — 컨트롤 플레인과 게이트웨이의 생명주기를 나누면 업그레이드가 서로에게 보이지 않는다", 11, SOFT, KR, "start")
d.legend(710, [("저자가 적은 절차", ACC), ("앞의 설치가 망가지는 갈래", BAD)])
d.save("a0-01.split-install.svg")
