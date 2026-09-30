# 01-01.chapter-overview — 조용한 연결이 서버를 멈추기까지
# 본문 요구(01-01 학습 목표 지도 문단): 조용한 연결 하나가 새 손님의 시간 초과까지 번지는 한 줄의 사슬과 각 고리의 절.
# 타입 스펙: type-flowchart — 여섯 단계를 가로로 잇는 흐름. focal 은 끊을 수 있는 맨 앞 고리(Read).
# 사실 출처: 본문 §1~§4, gonet-lab server.go.
from dd import D, INK, MUTED, SOFT, ACC, WARN, BAD, KR
from ddk import node, harrow

W, H = 960, 320
X, NW, NH, STEP, Y = 24, 132, 76, 154, 128
steps = [("Read 에서 기다림", "조용한 연결", ACC, True, "§4 끊는 곳"),
         ("FD 가 쌓임", "연결마다 하나", WARN, False, "§2 한도"),
         ("EMFILE", "accept4 실패", WARN, False, "§3"),
         ("wg.Wait 에 멈춤", "로그 없음", WARN, False, "§3"),
         ("대기열이 참", "꺼낼 goroutine 없음", WARN, False, "§3"),
         ("새 손님 시간 초과", "SYN 버림", BAD, False, "§3")]
d = D(W, H, "FLOWCHART · 01-01 OVERVIEW", "조용한 연결이 서버를 멈추기까지",
      "조용한 연결의 핸들러가 Read 에서 기다리면 FD 가 연결마다 쌓이고, 한도에 닿으면 accept4 가 EMFILE 로 실패한다. "
      "Accept 루프는 에러 분기의 wg.Wait 에 멈춰 로그도 남기지 않고, 꺼낼 goroutine 이 없어 accept 대기열이 차며, "
      "그 뒤 새 손님의 SYN 은 버려져 시간 초과로 끝난다. 끊을 수 있는 고리는 맨 앞의 Read 다.",
      lead="왼쪽 끝이 원인, 오른쪽 끝이 밖에서 보이는 증상입니다.")
for i, (t, s, c, f, sec) in enumerate(steps):
    x = X + i * STEP
    node(d, x, Y, NW, NH, t, s, c, f, 13)
    if i < 5:
        harrow(d, x + NW + 3, x + STEP - 3, Y + NH / 2)
    d.chip(x + NW / 2, Y + NH + 30, sec, ACC if f else MUTED, 12)
d.legend(268, [("끊을 수 있는 곳", ACC), ("번져 가는 고리", WARN), ("밖에서 보이는 증상", BAD)])
d.save("01-01.chapter-overview.svg")
print("ok 01-01 overview")
