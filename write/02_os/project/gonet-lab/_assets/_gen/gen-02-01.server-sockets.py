# 02-01.server-sockets — 클라이언트 A·B·C 를 받는 두 서버
# 본문 요구(02-01 §3 「TCP 가 연결마다 소켓을 두는 이유」「UDP 서버의 소켓은 하나」「떠났다는 신호가 없어 타이머로 지웁니다」):
#           TCP 서버는 listener 하나에 클라이언트마다 연결 소켓(FD 1)과 goroutine 을 두고,
#           UDP 서버는 소켓 하나로 모두 받아 ReadFrom 이 주소를 돌려주며, 떠난 클라이언트는 앱 map 에서 타이머로 지운다.
# 타입 스펙: type-flowchart — 좌우 두 패널. 대각선 금지라 UDP 쪽은 세로 버스로 모은다. focal 은 UDP 소켓 하나.
# 사실 출처: 02-01 Phase 1 문답(질문 3, 3-1, 3-2), 01-01 §3 연결당 FD.
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, RULE, MONO, KR
from ddk import node, harrow

W, H = 960, 452
ROWS = [164, 244, 324]
NH = 56

d = D(W, H, "FLOWCHART · 02-01 SERVER SOCKETS", "클라이언트 A·B·C 를 받는 두 서버",
      "TCP 서버는 listener 하나와 클라이언트마다 연결 소켓 하나, goroutine 하나를 둔다. UDP 서버는 소켓 하나로 셋을 모두 받고 "
      "ReadFrom 이 데이터와 함께 보낸 쪽 주소를 돌려준다. 떠났다는 신호가 없으므로 앱이 주소별 마지막 시각을 적어 두고 "
      "오래 조용한 항목을 타이머로 지운다.",
      lead="왼쪽은 상대마다 자원이 생기고, 오른쪽은 소켓 하나에 앱 상태만 남습니다.")

# 왼쪽 TCP
d.t(24, 104, "TCP 서버", 13, SOFT, KR, "start", 600)
node(d, 200, 116, 240, 32, "listener · FD 1", None, None, False, 12)
for y, n in zip(ROWS, "ABC"):
    node(d, 24, y, 100, NH, f"클라이언트 {n}")
    harrow(d, 130, 194, y + NH / 2)
    node(d, 200, y, 240, NH, f"연결 소켓 {n}", "FD 1 · goroutine 1", ACC)

d.line(478, 100, 478, 388, RULE, 1.0, "3 6")

# 오른쪽 UDP
d.t(500, 104, "UDP 서버", 13, SOFT, KR, "start", 600)
BUS = 616
for y, n in zip(ROWS, "ABC"):
    node(d, 500, y, 100, NH, f"클라이언트 {n}")
    d.line(600, y + NH / 2, BUS, y + NH / 2, SOFT, 1.3)
d.line(BUS, ROWS[0] + NH / 2, BUS, ROWS[2] + NH / 2, SOFT, 1.3)
mid = ROWS[1] + NH / 2
harrow(d, BUS, 644, mid)
node(d, 650, ROWS[1], 124, NH, "UDP 소켓", "FD 1", OK, True)
d.t(712, ROWS[1] - 10, "데이터 + 주소", 12, MUTED, KR, "middle")
harrow(d, 780, 800, mid)
MX, MW = 806, 136
d.box(MX, ROWS[0], MW, ROWS[2] + NH - ROWS[0])
d.t(MX + MW / 2, ROWS[0] + 24, "앱 map", 13, INK, KR, "middle", 600)
d.t(MX + MW / 2, ROWS[0] + 42, "주소 → 마지막 시각", 11, MUTED, KR, "middle")
for k, (n, t, c) in enumerate((("A", "12:00:03", INK), ("B", "12:00:05", INK), ("C", "11:58:40", BAD))):
    yy = ROWS[0] + 90 + k * 40
    d.t(MX + 16, yy, n, 13, c, MONO, "start", 600)
    d.t(MX + MW - 14, yy, t, 12, c, MONO, "end")
d.t(MX + MW / 2, ROWS[2] + NH - 12, "C: 타이머로 삭제", 12, BAD, KR, "middle", 600)

d.legend(404, [("상대마다 생기는 자원", ACC), ("모두가 함께 쓰는 소켓", OK), ("앱이 지우는 항목", BAD)])
d.save("02-01.server-sockets.svg")
print("ok server-sockets")
