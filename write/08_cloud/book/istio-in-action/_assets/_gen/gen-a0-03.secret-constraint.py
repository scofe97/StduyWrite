# a0-03 §4 제약에서 부품이 나오는 순서.
# 본문(부록 C.2.2): "workloads must not possess secrets ... Otherwise, the system can easily be
#       exploited by a malicious user who gets access to those secrets. As a consequence of the
#       restriction, workloads lack a means of authentication and cannot initiate secure
#       communication with the Workload API. To resolve this situation, SPIFFE defines the
#       Workload Endpoint specification."
# 타입 스펙: type-flowchart — 제약에서 결론이 따라 나오는 유도가 논점이다. 시작·끝은 타원,
#           단계는 사각, 판단은 마름모, 예는 오른쪽 아니오는 아래, 모든 갈래에 라벨.
#           축약: accent 는 규격이 실제로 고른 갈래 하나에만 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 756
d = D(W, H, "ISTIO IN ACTION · A0-03 §4",
      "비밀을 뺐더니 부품이 하나 더 필요해졌다",
      "워크로드에 비밀을 주면 그것을 얻은 공격자가 시스템을 악용한다. 그래서 뺐더니 이번에는 "
      "인증할 수단이 없어진다. 색이 붙은 갈래가 규격이 그 공백을 메운 방법이다.",
      "제약 하나가 규격의 나머지 구조를 거의 다 결정합니다")

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
        d.t(x + w / 2, y + h / 2 + 18, sub, 11, MUTED, KR, "middle")
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

oval(CA - 168, 112, 336, 60, "워크로드에 신원을 줘야 한다", "SVID 를 받아야 한다")
diamond(CA, 268, "워크로드가 비밀을", "직접 들고 있나")
step(CB - 164, 236, 328, 64, "비밀을 얻으면 악용된다", "규격이 이것을 금한다", BAD)
diamond(CA, 452, "그러면 스스로", "인증할 수 있나")
step(CB - 164, 420, 328, 64, "안전한 통신을 못 연다", "받으러 갈 수가 없다", BAD)
oval(CA - 168, 592, 336, 60, "엔드포인트가 대신한다", "곁에서 증명하고 받아 온다", focal=True)

d.arrow([(CA, 172), (CA, 208)], MUTED, "ar", 1.4)
d.arrow([(CA + 168, 268), (CB - 166, 268)], BAD, "bad", 1.4)
d.arrow([(CA, 324), (CA, 392)], MUTED, "ar", 1.4)
d.arrow([(CA + 168, 452), (CB - 166, 452)], BAD, "bad", 1.4)
d.arrow([(CA, 508), (CA, 588)], ACC, "acc", 1.5)

d.t((CA + CB) / 2, 254, "예", 12, BAD, KR, "middle", 600)
d.t((CA + CB) / 2, 438, "아니오", 12, BAD, KR, "middle", 600)
d.t(CA + 20, 360, "아니오", 12, MUTED, KR, "start", 600)
d.t(CA + 20, 552, "그래서", 12, ACC, KR, "start", 600)

d.t(28, 680, "엔드포인트가 하는 일 둘 — 워크로드 증명(커널 인트로스펙션 · 오케스트레이터 질의)과 Workload API 노출", 11, SOFT, KR, "start")
d.legend(700, [("규격이 고른 해법", ACC), ("막다른 갈래", BAD)])
d.save("a0-03.secret-constraint.svg")
