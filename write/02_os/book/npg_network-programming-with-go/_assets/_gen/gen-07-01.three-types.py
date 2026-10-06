# 타입 스펙: type-swimlane
# 07-01 세 가지 소켓 타입의 메시지 경계 비교
# 사실 출처: NPG Ch.7 Listing 7-4 (12B pingpingping), Listing 7-9 (4B ping x 3), Listing 7-11·7-12 (2B pi 수신 + ng 폐기)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 880, 500
d = D(W, H, "NPG CH.7 — THREE SOCKET TYPES",
      "소켓 타입별 메시지 경계",
      "소켓 타입과 버퍼 크기에 따른 수신 경계 비교",
      "동일한 ping 3회 전송 시 수신 경계와 잔여 폐기")

# Lane 1: unix 스트림 (Listing 7-4)
y1 = 104
d.box(24, y1, 156, 96)
d.t(36, y1 + 22, "TYPE 1", 9, SOFT, MONO, "start")
d.t(36, y1 + 44, "unix", 13, INK, MONO, "start", 600)
d.t(36, y1 + 66, "net.Conn / Read", 10, MUTED, MONO, "start")

d.box(192, y1, 484, 96)
d.tone(208, y1 + 16, 280, 28, INFO, op="20")
d.t(348, y1 + 34, '"ping" + "ping" + "ping"', 11, INFO, MONO, "middle", 600)
d.arrow([(348, y1 + 44), (348, y1 + 58)], c=INFO, m="info")
d.t(348, y1 + 78, 'Read(1024) → "pingpingping"', 11, INK, MONO, "middle", 600)

d.box(688, y1, 168, 96)
d.t(700, y1 + 38, "경계 없음", 12, INFO, KR, "start", 600)
d.t(700, y1 + 62, "12B 일괄 수신", 11, MUTED, KR, "start")

# Lane 2: unixgram 데이터그램 (Listing 7-9)
y2 = 216
d.box(24, y2, 156, 100)
d.t(36, y2 + 22, "TYPE 2", 9, SOFT, MONO, "start")
d.t(36, y2 + 44, "unixgram", 13, INK, MONO, "start", 600)
d.t(36, y2 + 66, "net.PacketConn", 10, MUTED, MONO, "start")

d.box(192, y2, 484, 100)
# 송신 데이터그램 3개
d.tone(208, y2 + 16, 88, 24, OK, op="20")
d.t(252, y2 + 32, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(304, y2 + 16, 88, 24, OK, op="20")
d.t(348, y2 + 32, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(400, y2 + 16, 88, 24, OK, op="20")
d.t(444, y2 + 32, '"ping"', 11, OK, MONO, "middle", 600)

# 세 블록 각각에서 읽기 결과로 하향 화살표
d.arrow([(252, y2 + 40), (252, y2 + 58)], c=OK, m="ok")
d.arrow([(348, y2 + 40), (348, y2 + 58)], c=OK, m="ok")
d.arrow([(444, y2 + 40), (444, y2 + 58)], c=OK, m="ok")

# 수신 결과 3개 (세 번 따로 읽음)
d.tone(208, y2 + 58, 88, 24, OK, op="20")
d.t(252, y2 + 74, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(304, y2 + 58, 88, 24, OK, op="20")
d.t(348, y2 + 74, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(400, y2 + 58, 88, 24, OK, op="20")
d.t(444, y2 + 74, '"ping"', 11, OK, MONO, "middle", 600)
d.t(508, y2 + 74, 'ReadFrom(1024) 3회', 11, OK, KR, "start", 600)

d.box(688, y2, 168, 100)
d.t(700, y2 + 40, "경계 보존", 12, OK, KR, "start", 600)
d.t(700, y2 + 64, "메시지 분리 수신", 11, MUTED, KR, "start")

# Lane 3: unixpacket 시퀀스 패킷 (Listing 7-11, 7-12)
y3 = 332
d.box(24, y3, 156, 100)
d.t(36, y3 + 24, "TYPE 3", 9, SOFT, MONO, "start")
d.t(36, y3 + 48, "unixpacket", 13, INK, MONO, "start", 600)
d.t(36, y3 + 72, "net.Conn / Read", 10, MUTED, MONO, "start")

d.box(192, y3, 484, 100)
# 윗줄: unixgram 처럼 "ping" 블록 셋 (경계 보존)
d.tone(208, y3 + 16, 88, 24, OK, op="20")
d.t(252, y3 + 32, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(304, y3 + 16, 88, 24, OK, op="20")
d.t(348, y3 + 32, '"ping"', 11, OK, MONO, "middle", 600)
d.tone(400, y3 + 16, 88, 24, OK, op="20")
d.t(444, y3 + 32, '"ping"', 11, OK, MONO, "middle", 600)
d.t(508, y3 + 32, 'Read(1024) 3회', 11, OK, KR, "start", 600)

# 아랫줄: Read(2) 로 한 블록이 "pi"(읽음)와 "ng"(버려짐)로 갈리는 모습
d.tone(208, y3 + 58, 42, 24, OK, op="20")
d.t(229, y3 + 74, '"pi"', 11, OK, MONO, "middle", 600)
d.tone(254, y3 + 58, 42, 24, BAD, op="20")
d.t(275, y3 + 74, '"ng"', 11, BAD, MONO, "middle", 600)
d.t(316, y3 + 74, 'Read(2) → msg[:2] ("ng" 폐기)', 11, BAD, KR, "start")

d.box(688, y3, 168, 100)
d.t(700, y3 + 40, "잔여 폐기", 12, BAD, KR, "start", 600)
d.t(700, y3 + 64, "버퍼 초과분 유실", 11, MUTED, KR, "start")

# 범례
d.legend(452, [("경계 보존", OK), ("스트림 결합", INFO), ("잔여 폐기", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07-01.three-types.svg"))
d.save(out)
print(f"saved: {out}")
