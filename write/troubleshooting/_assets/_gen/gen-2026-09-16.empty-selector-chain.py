# 개념 노트 「노드 간 경로를 누가 퍼뜨리는가」 · 셀렉터가 빈 집합이 될 때.
# 논지는 "라벨 하나가 사라지면 경로 배포까지 조용히 걷힌다"이고, 왼쪽이 사건, 오른쪽이 그때 읽히는 값이다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 단계, 오른쪽에 그 단계에서 관측되는 값.
#           type-sequence 는 주체가 주고받는 메시지가 아니라 한 줄기 연쇄라 기각.
#           focal 은 2 단계 하나 — 에러가 아니라 빈 집합이라는 것이 이 노트의 논지다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560
d = D(W, H, "TROUBLESHOOTING CONCEPT · EMPTY SELECTOR",
      "라벨 하나가 사라진 뒤의 다섯 걸음",
      "업그레이드가 컨트롤 플레인 노드에서 옛 라벨을 지우면 그 라벨로 반사기를 고르던 셀렉터가 빈 집합이 된다. "
      "오브젝트는 그대로 남고 로그도 조용한데 BGP 세션이 사라지고, 그 세션으로 배웠던 다른 노드의 Pod 대역 경로가 함께 걷힌다.",
      lead="셀렉터가 아무도 못 고르는 것은 에러가 아니라 빈 집합이라 로그에 남지 않습니다")

STEPS = [
    ("kubeadm upgrade apply · 1.24", "컨트롤 플레인 노드에서 옛 라벨 제거", INFO,
     "kubectl get nodes -l node-role…/master", "결과 0 개"),
    ("BGPPeer 셀렉터 · 빈 집합", "peerSelector 가 고른 노드 0", ACC,
     "calicoctl get bgppeer -o yaml", "리소스는 그대로"),
    ("BGP 세션 종료", "반사기와 맺고 있던 피어 소멸", BAD,
     "calicoctl node status", "피어 목록 없음"),
    ("경로 철회", "다른 노드 Pod 대역이 라우팅 표에서 빠짐", BAD,
     "ip route | grep bird", "다른 노드 대역 없음"),
    ("노드를 넘는 Pod 통신 단절", "같은 노드 안은 그대로", BAD,
     "이름 해석 · 메트릭 · 웹훅", "한 뿌리에서 갈라진 증상"),
]

X, BW, BH, STRIDE, Y0 = 48, 380, 56, 76, 112
OX, OW = 496, 376

for i, (title, sub, c, cmd, out) in enumerate(STEPS):
    y = Y0 + i * STRIDE
    if i:                                     # 단계 사이 세로 화살표
        d.arrow([(X + BW // 2, y - STRIDE + BH), (X + BW // 2, y)], MUTED, "ar", 1.4)
    if c is ACC:
        d.tone(X, y, BW, BH, ACC, 6)
    else:
        d.box(X, y, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(X + 20, y + 24, title, 13, c, KR, "start", 600)
    d.t(X + 20, y + 44, sub, 12, MUTED, KR, "start")

    d.line(X + BW, y + BH // 2, OX, y + BH // 2, RULE, 0.8, "4,3")
    d.box(OX, y, OW, BH, PAPER, RULE, 0.9, 6)
    d.t(OX + 20, y + 24, cmd, 12, INK, MONO if i < 4 else KR, "start")
    d.t(OX + 20, y + 44, out, 12, MUTED, KR, "start")

d.legend(504, [("업그레이드가 바꾼 것", INFO), ("아무도 못 고른 집합", ACC), ("걷힌 것", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-16.empty-selector-chain.svg"))
print("ok")
