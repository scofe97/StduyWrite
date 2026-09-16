# 02-03.triage-ladder — 관문과 명령을 세로로 짝지운다
# 본문 요구: 관문마다 무엇을 치고 어디를 읽는가 — 물음 넷과 명령 넷이 짝
# 타입 스펙: type-process.md — 관문마다 "무엇을 확인하나 / 그때 치는 명령"이라는 같은 슬롯이
#           반복되고, 도구가 슬롯의 일부다. 스펙이 "도구가 중요하면 process"라 지정한다.
#           2026-08-28 렌더 확인 후 swimlane 에서 재분류.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
# 2026-08-28 명령 갱신 — 관문 3 의 `netstat -lp` 를 `ss -ltnp` 로. net-tools 는 지금 배포판에
#           기본으로 없고 본문 §4 도 ss 로 옮겼다. 읽을 자리 이름도 ss 의 열 이름을 따른다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 624   # 범례 구분선 아래 56px — 계약 §검증 '범례 아래 여유 30px'
d = D(W, H, "TRIAGE LADDER · ASK THEN RUN",
      "수사 사다리 — 관문마다 무엇을 치고 어디를 읽는가",
      "위에서부터 하나씩 묻고, 처음 막히는 관문이 곧 원인의 층이다. 아래 줄이 그 관문에서 실제로 치는 명령이다.",
      lead="처음 막히는 관문이 원인의 층이다 · 아래 줄이 거기서 치는 명령")

BW, BH, GAP = 200, 100, 24
CX = [64 + BW // 2 + i * (BW + GAP) for i in range(4)]
ddx.band(d, 104, 552, "계층 순서대로 묻기 · 원인이 있는 층에서 처음 걸림")
ddx.lane_pair(d, CX, 276, 452, BW, BH,
              "관문 — 위에서부터", "치는 명령",          # 아래 링 라벨이 첫 세로 화살표(x=164)에 닿지 않는 길이
              [("이름이 풀리는가", "안 풀리면 DNS 문제", "여기서 멈춤"),
               ("호스트에 닿는가", "안 닿으면 경로 문제", "Service 는 예외"),
               ("포트가 열렸는가", "안 열렸으면 바인딩 문제", "프로세스 확인"),
               ("대화가 되는가", "안 되면 L7 문제", "앱 로직으로")],
              [("dig <도메인>", "status · ANSWER SECTION", "NXDOMAIN 이면 없음"),
               ("ping -c 3 <주소>", "손실률과 왕복 시간", "Service 면 건너뜀"),
               ("ss -ltnp", "Local Address:Port 열", "와일드카드인지 루프백인지"),
               ("curl -v <URL>", "핸드셰이크와 응답 헤더", "어느 단계에서 멈추나")],
              ["", "", "", ""])
# 링크 라벨 — lane_pair 는 위 레인 바로 밑(y=top+bh/2+22)에 찍어 아래 링 윗테두리와 겹친다.
# 두 링 사이 통로의 한가운데로 옮겨 찍는다: 위 링 바닥 = 276+50+12, 아래 링 윗변 = 452-50-26.
MID_Y = ((276 + BH // 2 + 12) + (452 - BH // 2 - 26)) // 2 + 4
for cx, lab in zip(CX, ["조회", "확인", "점검", "대화"]):
    d.t(cx + 12, MID_Y, lab, 12, ACC, KR, "start")
d.legend(568, [("관문", INFO), ("치는 명령", ACC)])
d.save("02-03.triage-ladder.svg")
print("ok triage-ladder")
