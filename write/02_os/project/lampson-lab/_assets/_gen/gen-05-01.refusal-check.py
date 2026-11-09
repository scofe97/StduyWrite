# 05-01 §2 — 거부 테스트 하나가 확인하는 세 가지와 어긋날 때 찍히는 실패 문구.
# 타입 스펙: type-process — 칸 셋이 같은 슬롯(확인할 것 · 통과 조건 · 어긋날 때의 문구)으로 반복되고
#           화살표가 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 372
d = D(W, H, "LAMPSON LAB · 05-01 §2",
      "거부 테스트 하나의 세 확인",
      "정상 경로가 먼저 성공하고, 막아야 할 요청이 거부되고, 로그에 그 사유가 남아야 PASS 다. 아래 줄은 어긋날 때 찍히는 실패 문구다.",
      "AC-06 의 예 — deployer 가 role-operator@crm 을 요청한다")

CW, CH, GAP, X0, Y = 248, 132, 40, 24, 100
cards = [
    ("1 양성 대조", "자기 인증서는 받는다",
     "precondition: deployer cannot get", "its own certificate"),
    ("2 거부", "role-operator@crm 은 발급 실패",
     "certificate issued", "(principals {...})"),
    ("3 거부 사유", "step-ca 로그에 기대한 문구",
     "refused, but step-ca did not log", "the expected reason"),
]
for i, (name, ok, f1, f2) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 60, "통과 조건", 11, SOFT, KR, "start")
    d.t(x + 16, Y + 84, ok, 12, MUTED, KR, "start")
    if i < 2:
        d.arrow([(x + CW + 4, Y + CH / 2), (x + CW + GAP - 4, Y + CH / 2)], MUTED, "ar", 1.4)
    # 어긋날 때 문구
    d.line(x + CW / 2, Y + CH, x + CW / 2, 268, RULE, 0.8, "3 4")
    d.t(x + 16, 292, "어긋나면", 11, SOFT, KR, "start")
    d.t(x + 16, 312, f1, 11, ACC if focal else MUTED, MONO, "start")
    d.t(x + 16, 330, f2, 11, ACC if focal else MUTED, MONO, "start")

d.t(24, 358, "첫 칸이 어긋나면 거기서 FAIL 로 멈춘다", 12, SOFT, KR, "start")
d.save("05-01.refusal-check.svg")
