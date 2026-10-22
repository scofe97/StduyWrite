# 타입 스펙: type-sequence — Follow Stream 이 복원한 방향별 바이트 흐름
# 사실 출처: 노트 L259~L270 (follow,tcp,ascii,2 출력), L272 (해석 산문)
# 02-04 §8 — 화살표 하나가 방향 하나의 바이트 덩어리이고 라벨은 출력에 찍힌 숫자 그대로다. Seq/Ack/Win 이 없다는 것이 논지라
# focal 은 가장 큰 덩어리(응답 본문 6162)가 아니라 "TCP 제어 정보가 없다" 는 한 줄이다.
import sys; sys.path.insert(0, ".")
from dd import ACC, MUTED, SOFT, INFO
from _tls_lab import SeqKR, kr, text_w

W, H = 880, 420
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-04 §8",
          "Follow Stream 이 되돌린 바이트",
          "follow,tcp,ascii,2 출력의 세 덩어리. Node 0 이 78바이트를 보내고 Node 1 이 156바이트와 6162바이트로 답한다. 출력에는 Seq·Ack·Win 이 없고 방향별 바이트 수만 남는다.",
          "TCP 헤더 값 대신 방향마다 바이트 수가 남습니다")
d.lanes([("Node 0", "[::1]:61012"), ("Node 1", "[::1]:18080")], y0=104, lane_w=210)
d.rails(344)
d.msg("Node 0", "Node 1", "78바이트", 204, INFO, "info", sub="GET / HTTP/1.1 · Host: localhost:18080")
d.msg("Node 1", "Node 0", "156바이트", 264, MUTED, "ar", sub="HTTP/1.0 200 OK · Content-Length: 6162")
d.msg("Node 1", "Node 0", "6162바이트", 324, MUTED, "ar", sub="<!DOCTYPE HTML> 부터 본문")
# focal — 사라진 것
x = (d.LX["Node 0"] + d.LX["Node 1"]) / 2
w = text_w("Seq · Ack · Win 없음", 13) + 28
d.tone(x - w / 2, 150, w, 28, ACC, 6, "1f", 1.4)
d.t(x, 169, "Seq · Ack · Win 없음", 13, ACC, kr("한"), "middle", 600)
d.legend(372, [("클라이언트가 보낸 바이트", INFO), ("서버가 보낸 바이트", MUTED), ("걷어낸 TCP 제어 정보", ACC)])
d.save("02-04.follow-stream-bytes.svg")
