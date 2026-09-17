# 2026-09-14 B(업그레이드 2분 뒤) 문항 · 원인 분석 — 사건.
# 논지는 "두 번의 소실이 성격이 다르다"이다. 워커 1 의 라우팅 표 한 장을 세 시점으로 옮겨 그린다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓인다. 같은 표를 t1·t2·t3 컷으로 세워 무엇이 걷혔는지 대조한다.
#           type-flowchart 는 개념 노트의 empty-selector-chain 이 이미 맡아 논지가 겹쳐 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 520
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 B",
      "두 번의 소실은 성격이 다릅니다",
      "워커 1 의 라우팅 표를 세 시점으로 놓았다. 업그레이드 중인 컨트롤 플레인 노드가 내려가면 그 노드로 가는 줄 하나가 빠지고 "
      "나머지는 그대로다. 라벨이 사라져 반사기와의 세션이 끊기면 그 세션으로 배운 줄이 한꺼번에 걷혀 자기 Pod 대역만 남는다.",
      lead="경로는 세션에 딸려 있어, 배워 온 세션이 죽으면 그 세션으로 알게 된 줄이 전부 사라집니다")

COLS = [
    (48, "t1 · 평소", "세션 정상", MUTED,
     [("10.244.1.0/24 → 로컬", OK), ("10.244.2.0/24 → 워커 2", OK),
      ("10.244.3.0/24 → 워커 3", OK), ("10.244.9.0/24 → 컨트롤 플레인 1", OK)]),
    (352, "t2 · 첫 노드 업그레이드", "그 노드만 내려감", MUTED,
     [("10.244.1.0/24 → 로컬", OK), ("10.244.2.0/24 → 워커 2", OK),
      ("10.244.3.0/24 → 워커 3", OK), ("10.244.9.0/24 → 컨트롤 플레인 1", BAD)]),
    (656, "t3 · 라벨 제거 2초 뒤", "반사기 세션 소멸", ACC,
     [("10.244.1.0/24 → 로컬", OK), ("10.244.2.0/24 → 워커 2", BAD),
      ("10.244.3.0/24 → 워커 3", BAD), ("10.244.9.0/24 → 컨트롤 플레인 1", BAD)]),
]

CW, HY, HH, RY, RH, STRIDE = 296, 104, 60, 180, 40, 48
for x, title, sub, c, rows in COLS:
    if c is ACC:
        d.tone(x, HY, CW, HH, ACC, 6)
    else:
        d.box(x, HY, CW, HH, PAPER2, RULE, 0.9, 6)
    d.t(x + 16, HY + 26, title, 13, c if c is ACC else INK, KR, "start", 600)
    d.t(x + 16, HY + 46, sub, 12, MUTED, KR, "start")
    for i, (txt, rc) in enumerate(rows):
        y = RY + i * STRIDE
        d.box(x, y, CW, RH, PAPER, RULE if rc is OK else f"{BAD}55", 0.9, 4)
        d.t(x + 16, y + 25, txt, 12, INK if rc is OK else BAD, MONO, "start")

d.t(48, 400, "걷힌 줄은 다른 노드의 Pod 대역", 12, MUTED, KR, "start")
d.t(48, 422, "남은 줄은 자기 노드 안에서 끝나는 통신", 12, MUTED, KR, "start")

d.legend(456, [("표에 남은 줄", OK), ("걷힌 줄", BAD), ("이 문항이 겨눈 시점", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-14.two-route-losses.svg"))
print("ok")
