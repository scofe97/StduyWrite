# 01-01.stuck-server — EMFILE 뒤 멈춘 gonet 서버의 모습
# 본문 요구(01-01 §3): 핸들러들은 Read 에, Accept 루프는 wg.Wait 에 멈추고, listener 는 열린 채라 커널이
#           handshake 를 끝내 대기열에 줄을 세우다 backlog 가 차면 SYN 을 버린다 — 주체 넷 사이의 시간순 사건.
# 타입 스펙: type-sequence — 레인 넷(새 손님·커널·Accept 루프·핸들러), 시간은 위→아래. 되돌아오는 값은 점선.
#           focal 은 멈춤의 중심인 wg.Wait.
# 사실 출처: gonet-lab server.go:35-65·73, accept(2) EMFILE, systems-performance 10-02 §4 대기열 표.
from dd import INK, MUTED, SOFT, RULE, ACC, WARN, BAD, KR, MONO
from ddk import SeqKR

W, H = 960, 640
C, K, L, Hd = "새 손님", "커널", "Accept 루프", "핸들러 ×N"
d = SeqKR(W, H, "SEQUENCE · 01-01 STUCK SERVER", "EMFILE 뒤 멈춘 gonet 서버",
          "핸들러 goroutine 들은 조용한 연결의 Read 에서 기다린다. FD 가 다 차 accept4 가 EMFILE 을 돌려주면 Accept 루프는 "
          "에러 분기의 wg.Wait 에서 멈춘다. listener 가 열려 있어 커널은 새 손님의 handshake 를 끝내 대기열에 세우지만 꺼내는 "
          "goroutine 이 없고, 대기열이 차면 그다음 SYN 을 버려 새 손님은 시간 초과로 끝난다.",
          lead="위에서 아래로, 서버가 멈추고 새 손님이 막히는 순서입니다.")
d.lanes([(C, "클라이언트"), (K, "listener · 대기열"), (L, "server.go:36"), (Hd, "handleEcho")], y0=96, lane_w=180)
d.rails(588)
d.msg(Hd, K, "Read", 184, WARN, "warn", sub="조용한 연결을 기다림")
d.msg(L, K, "accept4", 236)
d.msg(K, L, "-1 EMFILE", 276, BAD, "bad", dash="5 4", sub="FD 가 다 참")
d.selfmsg(L, "wg.Wait()", 328, ACC, sub="Done 이 오지 않음")
d.msg(C, K, "SYN", 380)
d.selfmsg(K, "handshake", 420, MUTED, sub="대기열에 줄")
d.msg(K, C, "연결된 듯 보이나 응답 없음", 470, MUTED, "ar", dash="5 4")
d.msg(C, K, "SYN (대기열이 찬 뒤)", 520, BAD, "bad")
d.selfmsg(K, "SYN 버림", 560, BAD, sub="재전송 뒤 시간 초과")
d.legend(600, [("멈춘 대기", WARN), ("멈춤의 중심", ACC), ("실패", BAD)])
d.save("01-01.stuck-server.svg")
print("ok stuck")
