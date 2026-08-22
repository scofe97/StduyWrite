# 06-01 §2 — phase 는 되돌아가지 않는다, 그리고 죽음에는 두 경우가 있다
# 본문: "한번 Running 에 도달한 Pod 가 Pending 으로 되돌아가는 일은 실무에서 관찰되지 않는다"
#       + "여기서 두 경우를 구분해야 합니다 — 같은 Pod 안의 컨테이너가 죽은 경우 / Pod 자체가 사라진 경우"
# 타입 스펙: 본문이 "두 경우를 구분"이라 못 박으므로 계약의 "윗줄과 아랫줄이 같은 모양으로
#           이어진다 → 비교 행렬" 을 따른다. 옛 판은 이 대비를 문단 세 줄로 적어 두었는데,
#           계약이 금지하는 형태다(라벨은 라벨로 쓴다 · 이유는 본문 산문이 맡는다).
#           위의 한 줄 사슬은 되돌아가지 않는다는 사실만 지고, 판정 축은 행렬의 phase 열이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 660
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "phase 는 되돌아가지 않는다 — 죽음에는 두 경우가 있다",
      "컨테이너 재시작은 컨테이너 수준의 사건이라 phase 를 바꾸지 않는다. Pod 자체가 사라지면 "
      "그 Pod 를 되살리는 것이 아니라 Deployment 가 새 Pod 를 만들어 Pending 부터 다시 시작한다.",
      lead="쿠버네티스는 Pod 를 고쳐 쓰지 않고 새로 만들어 교체한다")

CY, BW, BH = 200, 200, 76
PEND, RUN, END = 200, 500, 800

ddx.band(d, 104, 604, "복구는 phase 를 되돌리는 것이 아니라 새 Pod 를 만드는 것이다")

ddx.node(d, PEND, CY, "Pending", "아직 준비 중", BW, BH)
ddx.node(d, RUN, CY, "Running", "최소 하나 실행 중", BW, BH)
ddx.node(d, END, CY, "Succeeded · Failed", "종료된 Pod", BW, BH)
ddx.hop(d, PEND, RUN, CY, half=BW // 2)
ddx.hop(d, RUN, END, CY, half=BW // 2)

# 일어나지 않는 전이 — 아래로 돌려 긋고 ✕ 를 얹는다
BACK = CY + BH // 2 + 28
d.path(f"M {RUN} {CY+BH//2+6} L {RUN} {BACK} L {PEND} {BACK} L {PEND} {CY+BH//2+10}",
       BAD, 1.4, m="bad", dash="6 5")
XM = (PEND + RUN) // 2
for dx, dy in ((-1, -1), (-1, 1)):
    d.o.append(f'<line x1="{XM-11*dx}" y1="{BACK-9*dy}" x2="{XM+11*dx}" y2="{BACK+9*dy}" '
               f'stroke="{BAD}" stroke-width="2.4"/>')
d.t(XM, BACK + 30, "실무에서 되돌아가지 않는다", 11, BAD, KR)

ddx.matrix(
    d, x0=32, hdr_y=350, row_h=88, gap=12, focal_col=3,
    cols=[(215, "무엇이 죽었나"), (235, "누가 대응하나"),
          (225, "Pod 오브젝트는"), (225, "phase 는")],
    rows=[
        ([("컨테이너가 죽음", "같은 Pod 안에서"), ("kubelet 이 재시작", "그 자리에 다시 띄운다"),
          ("그대로 살아 있다", "오브젝트는 바뀌지 않는다"), ("Running 유지", "restarts 만 올라간다")], INFO),
        ([("Pod 가 사라짐", "노드 장애·삭제"), ("Deployment 가 만든다", "그 Pod 의 복구는 없다"),
          ("새 오브젝트로 교체", "고쳐 쓰지 않는다"), ("Pending 부터 다시", "새 Pod 의 phase")], WARN),
    ])

d.t(36, 586, "실측에서 restarts=4 인 Pod 의 phase 는 여전히 Running 이었다 — 재시작 횟수는 "
             "컨테이너 상태이지 phase 가 아니다", 12, MUTED, KR, "start")
d.legend(620, [("컨테이너 수준의 사건", INFO), ("Pod 교체", WARN), ("일어나지 않는 전이", BAD)])
d.save("06-01-phase-lifecycle-rules.svg")
print("ok phase-lifecycle-rules")
