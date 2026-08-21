# 02-02.conntrack-return-path — 지나는 자리와 conntrack 이 쥔 값을 세로로 짝지운다
# 본문 요구: "응답은 규칙을 다시 안 본다 — conntrack 항목이 목적지를 되돌린다"
# 타입 스펙: type-swimlane.md 레인 둘. 위는 응답 패킷의 자리, 아래는 그때 conntrack 이 쥔 값.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "CONNTRACK · THE RETURN PATH",
      "응답은 규칙을 다시 안 본다 — conntrack 항목이 목적지를 되돌린다",
      "위는 응답 패킷이 지나는 자리, 아래는 그때 conntrack 항목이 쥐고 있는 값이다. 확률은 재평가되지 않는다.",
      lead="위는 응답이 지나는 자리 · 아래는 conntrack 이 쥔 값 · 확률은 재평가되지 않는다")

BW, BH, GAP = 200, 100, 24
CX = [64 + BW // 2 + i * (BW + GAP) for i in range(4)]
ddx.band(d, 104, 568, "첫 패킷만 규칙을 보고, 나머지는 항목 하나를 따라간다")
ddx.lane_pair(d, CX, 276, 452, BW, BH,
              "응답 패킷이 지나는 자리", "conntrack 항목이 쥐고 있는 값 — kind 실측",
              [("Pod 가 응답", "src 10.244.1.66:8080", "dst 10.244.1.11:43346"),
               ("conntrack 조회", "역방향 기대 튜플과 대조", "KUBE-SVC 는 평가 안 됨"),
               ("자동 역-DNAT", "출발지를 되돌린다", "src → 10.96.192.224:8080"),
               ("클라이언트 소켓", "보낸 주소에서 온 응답", "연결이 성립한다")],
              [("원방향 튜플", "src=10.244.1.11:43346", "dst=10.96.192.224:8080"),
               ("역방향 기대 튜플", "src=10.244.1.66:8080", "dst=10.244.1.11:43346"),
               ("되돌릴 값", "원방향의 dst 를 복원", "10.96.192.224:8080"),
               ("확률은 재평가 없음", "첫 패킷만 규칙을 본다", "연결 수명 동안 고정")],
              ["기록됨", "일치", "복원", "그래서"])
d.t(36, 540, "클라이언트는 자기가 보낸 주소에서 응답이 온 것으로 본다 — 그래야 소켓이 그 응답을 받아들인다",
     12, MUTED, KR, "start")
d.legend(584, [("응답이 지나는 자리", INFO), ("conntrack 이 쥔 값", ACC)])
d.save("02-02.conntrack-return-path.svg")
print("ok conntrack-return-path")
