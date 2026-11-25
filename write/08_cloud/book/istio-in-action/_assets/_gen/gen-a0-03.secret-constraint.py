# a0-03 §4 제약에서 부품이 나오는 순서.
# 값 근거(본문 a0-03 §4, 원문 부록 C.2.2·C.2.3):
#   - 제약: 워크로드는 신원 비밀 소유 불가(탈취 시 악용) → 스스로 인증 불가 · Workload API 와 안전 통신 불가.
#   - 해법: Workload Endpoint 가 대신 워크로드 증명 + CSR 생성·제출 → Workload API 가 SAN URI 든 SVID 발급.
# 타입 스펙: type-flowchart — 제약에서 결론이 따라 나오는 유도가 논점이다. 시작·끝은 타원,
#           단계는 사각, 판단은 마름모, 예는 오른쪽 아니오는 아래, 모든 갈래에 라벨.
#           축약: accent 는 규격이 고른 해법에, bad 는 금지된 갈래에, info 는 인증 공백 단계에 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 744
d = D(W, H, "ISTIO IN ACTION · A0-03 §4",
      "비밀을 뺐더니 부품이 하나 더 필요해졌다",
      "워크로드에 비밀을 주면 그것을 얻은 공격자가 시스템을 악용한다. 그래서 뺐더니 이번에는 "
      "인증할 수단이 없어진다. 색이 붙은 해법이 규격이 그 공백을 메운 방법이다.",
      "제약 하나가 규격의 나머지 구조를 거의 다 결정합니다")

CA, CB = 268, 736


def oval(x, y, w, h, label, sub=None, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 24, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 24)
    c = ACC if focal else INK
    if sub:
        d.t(x + w / 2, y + h / 2 - 4, label, 14, c, KR, "middle", 600)
        d.t(x + w / 2, y + h / 2 + 18, sub, 13, MUTED, KR, "middle")
    else:
        d.t(x + w / 2, y + h / 2 + 5, label, 14, c, KR, "middle", 600)


def step(x, y, w, h, label, sub, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.2)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, label, 14, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + 50, sub, 13, MUTED, KR, "middle")


def diamond(cx, cy, l1, l2):
    d.o.append(f'<polygon points="{cx},{cy - 56} {cx + 172},{cy} {cx},{cy + 56} {cx - 172},{cy}" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy - 4, l1, 13, INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 13, INK, KR, "middle", 600)


oval(CA - 172, 112, 344, 64, "워크로드에 신원을 줘야 한다", "SVID 를 받아야 한다")
diamond(CA, 272, "워크로드가 신원 비밀을", "직접 들고 있나")
step(CB - 172, 236, 344, 72, "비밀 탈취 시 시스템 악용", "규격이 이것을 금한다", BAD)

step(CA - 172, 384, 344, 72, "자기를 인증할 수단이 없다", "Workload API 와 안전 통신 불가", INFO)
step(CB - 172, 384, 344, 72, "신원 없이 API 호출 시도", "신원 받으러 못 가는 막다른 길", BAD)

oval(CA - 172, 528, 344, 72, "Workload Endpoint 가 대신한다", "워크로드 증명 → CSR → SAN URI SVID", focal=True)

d.arrow([(CA, 176), (CA, 214)], MUTED, "ar", 1.4)
d.arrow([(CA + 172, 272), (CB - 174, 272)], BAD, "bad", 1.4)
d.arrow([(CA, 328), (CA, 382)], INFO, "info", 1.4)
d.arrow([(CA + 172, 420), (CB - 174, 420)], BAD, "bad", 1.4)
d.arrow([(CA, 456), (CA, 526)], ACC, "acc", 1.5)

d.t((CA + CB) / 2, 258, "예", 13, BAD, KR, "middle", 600)
d.t(CA + 16, 360, "아니오", 13, INFO, KR, "start", 600)
d.t((CA + CB) / 2, 406, "직접 통신 시도", 13, BAD, KR, "middle", 600)
d.t(CA + 16, 496, "공백 메움", 13, ACC, KR, "start", 600)

d.t(28, 636, "발급 세 걸음: 1. 워크로드 증명 · CSR 생성 → 2. Workload API 에 제출 → 3. SAN URI 든 SVID 응답", 13, SOFT, KR, "start")
d.legend(664, [("규격이 고른 해법", ACC), ("인증 공백 상태", INFO), ("금지 · 막다른 갈래", BAD)])
d.save("a0-03.secret-constraint.svg")
print("ok secret-constraint")
