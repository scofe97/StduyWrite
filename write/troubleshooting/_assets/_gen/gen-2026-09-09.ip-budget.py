# 2026-09-09 D 문항 — 문서의 최대치와 실제 상한이 다른 이유.
# 논지는 나눗셈 하나다. 노드당 소비하는 것은 Pod 수가 아니라 할당받는 IP 블록이고,
# 110 개에 256 개를 주므로 /16 은 595 대가 아니라 256 대에서 끝난다.
# 타입 스펙: type-bar — 두 계산의 결과를 길이로 비교한다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 800, 462
BX, BW = 168, 520
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-09 D",
      "문서의 110 과 실제로 쓰이는 256",
      "노드가 소비하는 것은 Pod 수가 아니라 할당받는 IP 블록이다. "
      "GKE 는 Pod 110 개를 담으려고 /24 즉 256 개를 준다. "
      "그래서 /16 에 붙일 수 있는 노드는 595 대가 아니라 256 대에서 끝난다.",
      lead="여유를 두는 이유는 죽은 Pod 의 주소를 바로 재사용하지 않기 때문입니다")

# 두 계산 비교
rows = [("문서의 최대치로 계산", "65,536 ÷ 110", 595, INFO),
        ("실제 소비량으로 계산", "65,536 ÷ 256", 256, ACC)]
for i,(label, calc, val, c) in enumerate(rows):
    y = 118 + i*86
    d.t(BX-16, y+20, label, 12, MUTED, KR, "end")
    d.t(BX-16, y+40, calc, 12, SOFT, MONO, "end")
    w = BW * val / 595
    if c is ACC: d.tone(BX, y, w, 42, ACC, 5)
    else: d.box(BX, y, w, 42, PAPER2, RULE, 0.9, 5)
    d.t(BX+w+14, y+26, f"노드 {val} 대", 13, c, KR, "start", 600)

# 실제 멈춘 지점
d.line(BX + BW*256/595, 104, BX + BW*256/595, 292, BAD, 1.2, "4 3")
d.t(BX + BW*256/595, 306, "여기서 멈췄습니다", 12, BAD, KR)

# 나눗셈 해부
d.box(28, 330, 744, 66, PAPER2, RULE, 0.9, 6)
for cx, top, bot in ((92, "65,536", "/16 총 주소"), (232, "256", "노드당 /24"), (372, "256", "붙일 수 있는 노드")):
    d.t(cx, 356, top, 14, INK, MONO, "middle", 600)
    d.t(cx, 378, bot, 12, SOFT, KR)
d.t(162, 356, "÷", 14, MUTED, MONO); d.t(302, 356, "=", 14, MUTED, MONO)

d.legend(H-50, [("실제 상한", ACC), ("문서만 보고 기대한 값", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-09.ip-budget.svg"))
print("ok")
