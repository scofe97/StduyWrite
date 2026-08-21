# 02-03.triage-ladder — 관문과 명령을 세로로 짝지운다
# 본문 요구: 관문마다 무엇을 치고 어디를 읽는가 — 물음 넷과 명령 넷이 짝
# 타입 스펙: type-swimlane.md 레인 둘. 가로는 사다리 순서(위에서부터 막히는 곳이 원인),
#           세로는 그 관문에서 실제로 치는 명령.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "TRIAGE LADDER · ASK THEN RUN",
      "수사 사다리 — 관문마다 무엇을 치고 어디를 읽는가",
      "위에서부터 하나씩 묻고, 처음 막히는 관문이 곧 원인의 층이다. 아래 줄이 그 관문에서 실제로 치는 명령이다.",
      lead="처음 막히는 관문이 원인의 층이다 · 아래 줄이 거기서 치는 명령")

BW, BH, GAP = 200, 100, 24
CX = [64 + BW // 2 + i * (BW + GAP) for i in range(4)]
ddx.band(d, 104, 568, "계층 순서대로 물으면 원인이 있는 층에서 처음 걸린다")
ddx.lane_pair(d, CX, 276, 452, BW, BH,
              "관문 — 위에서부터 묻는다", "실제로 치는 명령과 읽을 자리",
              [("이름이 풀리는가", "안 풀리면 DNS 문제", "여기서 멈춤"),
               ("호스트에 닿는가", "안 닿으면 경로 문제", "Service 는 예외"),
               ("포트가 열렸는가", "안 열렸으면 바인딩 문제", "프로세스 확인"),
               ("대화가 되는가", "안 되면 L7 문제", "앱 로직으로")],
              [("dig <도메인>", "status · ANSWER SECTION", "NXDOMAIN 이면 없음"),
               ("ping -c 3 <주소>", "손실률과 왕복 시간", "Service 면 건너뛴다"),
               ("netstat -lp", "Local Address 열", "와일드카드인지 루프백인지"),
               ("curl -v <URL>", "핸드셰이크와 응답 헤더", "어느 단계에서 멈추나")],
              ["조회", "확인", "점검", "대화"])
d.t(36, 540, "Service 주소는 ping 에 답하지 않는다 — 두 번째 관문만 예외로 두고 세 번째로 넘어간다",
     12, MUTED, KR, "start")
d.legend(584, [("관문", INFO), ("치는 명령", ACC)])
d.save("02-03.triage-ladder.svg")
print("ok triage-ladder")
