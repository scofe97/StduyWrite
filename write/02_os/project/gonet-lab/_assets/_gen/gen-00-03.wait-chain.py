# 00-03.wait-chain — 막힌 Read 를 바깥에서 닫아 기다림의 사슬을 푸는 순서
# 본문 요구(00-03 §4): "위쪽 두 줄이 멈춰 있는 상태이고, 종료 신호가 오면 오른쪽 goroutine 이 연결을 닫습니다.
#           그러면 막혀 있던 Read 가 에러로 돌아오고, io.Copy → defer → wg.Done() → wg.Wait() → return 이 차례로 풀립니다."
#           — goroutine 여럿 사이의 시간순 호출이 논지다.
# 타입 스펙: type-sequence — 레인 넷(메인·핸들러·AfterFunc·커널), 시간은 위→아래. 되돌아오는 에러는 점선.
#           focal 은 사슬을 끊는 conn.Close() 한 줄이다.
# 사실 출처: Go 명세·io.Copy·context.AfterFunc 문서, gonet-lab 실험 4·5 (2026-09-27).
# Seq 의 msg·selfmsg·state 는 라벨을 MONO 로 고정하므로 한글 라벨용으로 폰트만 갈라 쓰는 서브클래스를 둔다(계약 §프리미티브).
from dd import INK, MUTED, SOFT, RULE, ACC, OK, WARN, KR, MONO
from ddk import SeqKR

W, H = 960, 700
d = SeqKR(W, H, "SEQUENCE · 00-03 WAIT CHAIN",
          "막힌 Read 를 바깥에서 닫아야 사슬이 풀립니다",
          "종료 신호 전에는 핸들러 goroutine 이 연결의 Read 에서, 메인 goroutine 이 Accept 에서 기다린다. 신호로 "
          "context 가 취소되면 AfterFunc goroutine 이 listener 를 닫고, Accept 에러로 풀린 메인은 wg.Wait 에서 다시 멈춘다. "
          "AfterFunc 가 연결까지 닫으면 Read 에러, io.Copy 반환, defer 의 wg.Done, wg.Wait 반환, main 의 return 이 차례로 풀린다.",
          lead="가로선 위가 종료 신호 전, 아래가 신호 뒤에 사슬이 생기고 풀리는 순서입니다.")
d.lanes([("메인 goroutine", "main"), ("핸들러 goroutine", "go func"),
         ("AfterFunc goroutine", "ctx 취소 뒤"), ("커널 · 연결", "listener · conn")], y0=100, lane_w=180)
d.rails(652)

d.msg("메인 goroutine", "커널 · 연결", "Accept", 188, MUTED, "ar", sub="다음 손님을 기다림")
d.msg("핸들러 goroutine", "커널 · 연결", "Read", 244, WARN, "warn", sub="src 가 끝나기를 기다림")

d.line(24, 292, W - 48, 292, RULE, 1.0, "6 4")
d.t(W - 48, 284, "종료 신호 · ctx 취소", 12, SOFT, KR, "end")

d.msg("AfterFunc goroutine", "커널 · 연결", "ln.Close()", 332, MUTED, "ar")
d.msg("커널 · 연결", "메인 goroutine", "Accept 에러 · ErrClosed", 380, MUTED, "ar", dash="5 4")
d.selfmsg("메인 goroutine", "wg.Wait()", 424, WARN, sub="Done 을 기다림")
d.msg("AfterFunc goroutine", "커널 · 연결", "conn.Close()", 472, ACC, "acc")
d.msg("커널 · 연결", "핸들러 goroutine", "Read 에러 · ErrClosed", 520, MUTED, "ar", dash="5 4")
d.selfmsg("핸들러 goroutine", "io.Copy 반환", 560, OK, sub="defer 실행")
d.msg("핸들러 goroutine", "메인 goroutine", "wg.Done()", 604, OK, "ok")
d.selfmsg("메인 goroutine", "Wait 반환 · return", 640, OK)

d.legend(660, [("멈춘 대기", WARN), ("사슬을 끊는 호출", ACC), ("풀려나는 순서", OK)])
d.save("00-03.wait-chain.svg")
print("ok wait-chain")
