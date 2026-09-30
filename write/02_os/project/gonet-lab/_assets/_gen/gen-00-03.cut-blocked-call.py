# 00-03.cut-blocked-call — 막힌 호출을 어떻게 끊나
# 본문 요구(00-03 §5): ctx 를 받는 호출은 취소로 풀리고, 받지 않는 Accept·Read 는 AfterFunc 로 자원을 닫아 풀며,
#           닫아서 깨울 방법이 없는 stdin 은 읽기를 goroutine 으로 빼고 기다리지 않는 구조로 바꾼다 — 조건에 따른 판단 논리다.
# 타입 스펙: type-flowchart — 질문 두 칸(ctx 를 받나 / 닫을 자원이 있나)과 세 결론. focal 은 AfterFunc 로 닫는 길.
# 사실 출처: go doc context.AfterFunc, net.Listener.Close ("Any blocked Accept operations will be unblocked"),
#           gonet-lab client.go 수정(2026-09-27).
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, KR, MONO
from ddk import node, harrow, varrow

W, H = 960, 500
C1, C2, C3 = 24, 236, 520
R1, R2, R3, NH = 124, 244, 364, 64
d = D(W, H, "FLOWCHART · 00-03 CUT BLOCKED CALL", "막힌 호출을 어떻게 끊나",
      "종료 신호로 ctx 가 취소됐을 때, 막힌 호출이 ctx 를 받으면 그 취소로 풀린다. ctx 를 받지 않지만 닫을 자원이 있으면 "
      "AfterFunc 에서 그 자원을 Close 해 Accept 나 Read 를 에러로 풀어 준다. 닫아서 깨울 방법이 없는 stdin 읽기는 별도 "
      "goroutine 으로 빼고 메인이 그것을 기다리지 않게 구조를 바꾼다.",
      lead="질문 두 칸을 차례로 거쳐 세 가지 끊는 방법 중 하나로 갑니다.")
node(d, C1, R1, 172, NH, "종료 신호", "ctx 취소")
node(d, C2, R1, 220, NH, "호출이 ctx 를 받나", None, None, False, 13)
node(d, C2, R2, 220, NH, "닫을 자원이 있나", None, None, False, 13)
node(d, C3, R1, 416, NH, "ctx 취소로 풀림", "DialContext 같은 호출", OK)
node(d, C3, R2, 416, NH, "AfterFunc 에서 Close", "Accept · Read 가 에러로 풀림", ACC, True)
node(d, C3, R3, 416, NH, "읽기를 goroutine 으로 빼기", "stdin · 메인은 기다리지 않음", WARN)
harrow(d, C1 + 178, C2 - 6, R1 + NH / 2)
harrow(d, C2 + 226, C3 - 6, R1 + NH / 2, label="예")
harrow(d, C2 + 226, C3 - 6, R2 + NH / 2, label="예")
varrow(d, C2 + 110, R1 + NH + 4, R2 - 4, label="아니오")
d.arrow([(C2 + 110, R2 + NH + 4), (C2 + 110, R3 + NH / 2), (C3 - 6, R3 + NH / 2)], SOFT, "soft", 1.3)
d.t(C2 + 118, R2 + NH + 40, "아니오", 12, MUTED, KR, "start")
d.legend(448, [("ctx 로 풀림", OK), ("자원을 닫아 풀기", ACC), ("구조를 바꾸기", WARN)])
d.save("00-03.cut-blocked-call.svg")
print("ok cut")
