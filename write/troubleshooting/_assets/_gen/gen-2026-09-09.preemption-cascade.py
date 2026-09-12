# 2026-09-09 B 문항 — 우선순위 도입이 만든 선점 연쇄.
# 논지는 "설정을 빠뜨린 쪽이 오히려 높아졌다"와 "부활한 Pod 가 동료를 민다"이다.
# 왼쪽이 클래스 도입 전, 오른쪽이 후. 아래가 연쇄 고리.
# 타입 스펙: type-flowchart — 상태 변화와 그로 인한 연쇄 분기.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 800, 520
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-09 B",
      "설정을 빠뜨린 쪽이 더 높아졌습니다",
      "우선순위 클래스를 도입해도 이미 떠 있던 Pod 에는 소급되지 않는다. "
      "그래서 기존 운영은 0 에 남고, 설정을 빠뜨린 신규는 globalDefault 가 채워 medium 을 받는다. "
      "자원이 부족하면 높은 쪽이 낮은 쪽을 밀어내고, 부활한 Pod 가 또 동료를 민다.",
      lead="globalDefault 는 이미 떠 있는 Pod 에 소급되지 않습니다")

# 상단 — 두 무리의 우선순위
BY, BW, BH = 108, 340, 92
d.box(28, BY, BW, BH, PAPER2, RULE, 0.9, 6)
d.t(46, BY+26, "기존 운영 인스턴스", 13, INK, KR, "start", 600)
d.t(46, BY+48, "클래스 생기기 전에 생성", 12, SOFT, KR, "start")
d.t(46, BY+72, "priorityClassName 없음  →  우선순위 0", 12, BAD, MONO, "start")

d.tone(432, BY, BW, BH, ACC, 6)
d.t(450, BY+26, "새로 배포한 한 벌", 13, ACC, KR, "start", 600)
d.t(450, BY+48, "매니페스트에 설정을 빠뜨림", 12, SOFT, KR, "start")
d.t(450, BY+72, "globalDefault 가 채움  →  medium", 12, ACC, MONO, "start")

d.t(400, BY-14, "같은 자원 풀", 12, MUTED, KR)

# 연쇄
CY = 238
d.t(28, CY, "자원이 부족하면 높은 쪽이 낮은 쪽을 밀어냅니다", 13, INK, KR, "start", 600)
STEPS = [
    ("medium 이 자리를 못 찾음", INFO),
    ("0 짜리 운영 Pod 를 선점", BAD),
    ("컨트롤러가 다시 만듦 — 이제 medium", WARN),
    ("또 다른 0 을 선점", BAD),
]
sx, sw, sh = 28, 172, 46
for i,(t,c) in enumerate(STEPS):
    x = sx + i*(sw+16)
    d.box(x, CY+20, sw, sh, PAPER2, RULE, 0.9, 5)
    d.t(x+sw/2, CY+40, t.split(" — ")[0], 12, c, KR)
    if " — " in t: d.t(x+sw/2, CY+58, t.split(" — ")[1], 12, SOFT, KR)
    if i < 3: d.arrow([(x+sw, CY+43),(x+sw+12, CY+43)], MUTED, "ar", 1.2)
# 되돌아가는 고리
d.path(f"M {sx+3*(sw+16)+sw/2} {CY+66} L {sx+3*(sw+16)+sw/2} {CY+86} L {sx+sw/2} {CY+86} L {sx+sw/2} {CY+70}", BAD, 1.3, "bad", "4 3")
d.t(400, CY+102, "자원 총량은 그대로라 계속 돕니다", 12, BAD, KR)

# 결과
RY = 380
d.box(28, RY, 744, 62, PAPER2, RULE, 0.9, 6)
d.t(46, RY+24, "상태를 들고 있는 서비스라 종료 중인 인스턴스에는 쓸 수 없습니다", 13, INK, KR, "start", 600)
d.t(46, RY+46, "쓸 수 있는 인스턴스가 남지 않아 30분간 쓰기가 멈췄습니다 · PodDisruptionBudget 은 선점을 막지 못합니다", 12, SOFT, KR, "start")

d.legend(H-42, [("설정을 빠뜨렸는데 더 높아진 쪽", ACC), ("밀려나는 쪽", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-09.preemption-cascade.svg"))
print("ok")
