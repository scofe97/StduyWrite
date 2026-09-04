# 01-02.tcp-12packets — 요청 하나에 오가는 12패킷, 실선 둘만 내용을 나른다
# 본문 요구(01-02 §3 도입): "위 그림이 연결 하나의 전체 일생"이고 "실선 둘만 실제 내용을 나른다.
#           나머지 열은 연결을 세우고 확인하고 닫는 데 쓰인다. 이 비율이 §4의 결론"이다.
#           본문이 비율을 결론으로 못 박으므로 시퀀스만으로 끝내지 않고 아래에 12칸을 네 몫으로
#           가른 띠를 붙였다 — 열둘 중 둘이라는 비율이 눈에 들어와야 한다.
#           내용 둘만 굵게 쓰고 나머지 열은 보통 굵기로 둔 것도 같은 이유다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 왼쪽 번호가 패킷 순번이다.
#           아래 구성 띠는 시간 축이 아니라 같은 열둘을 몫으로 다시 센 것이라 레일 밖에 둔다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import Seq, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 860
Y0, STRIDE = 214, 44
BAR_X, BAR_W, BAR_Y, TOTAL = 200, 662, 754, 12

d = Seq(W, H, "SEQUENCE · 01-02 TCP LIFECYCLE",
        "요청 하나에 오가는 12패킷 — 실선 둘만 내용을 나른다",
        "curl 요청 한 번에 오가는 TCP 패킷 12개의 전체 일생. 수립 3개, 확인 3개, 종료 4개는 연결을 "
        "세우고 확인하고 닫는 데 쓰이고, 실제 내용을 나르는 것은 HTTP GET과 HTTP 200 두 개뿐이다.",
        lead="열둘 중 둘만 내용입니다 — 나머지 열이 신뢰성의 값입니다.")

C, S = "클라이언트", "서버"
LX = d.lanes([(C, "curl"), (S, "localhost:8080")], lane_w=200)
d.rails(728)
MID = (LX[C] + LX[S]) / 2

# (방향, 라벨, 부제, 색, 마커, 굵기, 점선, 라벨 굵기)
PKTS = [(1, "SYN",              "클라 ISN 을 고른다",          WARN, "warn", 1.3, None,  400),
        (0, "SYN-ACK",          "서버도 자기 ISN",             WARN, "warn", 1.3, None,  400),
        (1, "ACK",              "여기서 연결이 선다",           WARN, "warn", 1.3, None,  400),
        (0, "ACK",              "수립 직후 한 번 더",           INFO, "info", 1.3, "4 4", 400),
        (1, "HTTP GET  (78B)",  "실제 내용 — 1~78 바이트",      OK,   "ok",   2.2, None,  600),
        (0, "ACK 79",           "78 까지 받았다",              INFO, "info", 1.3, "4 4", 400),
        (0, "HTTP 200  (121B)", "실제 내용 — 서버는 자기 번호로", OK,  "ok",   2.2, None,  600),
        (1, "ACK 122",          None,                        INFO, "info", 1.3, "4 4", 400),
        (1, "FIN-ACK",          "닫기 시작",                   BAD,  "bad",  1.3, None,  400),
        (0, "ACK",              None,                        BAD,  "bad",  1.3, None,  400),
        (0, "FIN-ACK",          None,                        BAD,  "bad",  1.3, None,  400),
        (1, "ACK",              "연결 소멸",                   BAD,  "bad",  1.3, None,  400)]

for i, (fwd, label, sub, c, mk, sw, dash, weight) in enumerate(PKTS):
    y = Y0 + STRIDE * i
    if fwd:
        d.path(f"M {LX[C]+10} {y} L {LX[S]-12} {y}", c, sw, m=mk, dash=dash)
    else:
        d.path(f"M {LX[S]-10} {y} L {LX[C]+12} {y}", c, sw, m=mk, dash=dash)
    d.t(LX[C] - 24, y + 4, str(i + 1), 11, SOFT, MONO, "end")
    d.t(MID, y - 8, label, 11, c, MONO, "middle", weight)
    if sub:
        d.t(MID, y + 13, sub, 11, MUTED)

# 같은 열둘을 몫으로 다시 센다 — 시간이 아니라 비율이다
d.line(12, 746, W - 48, 746, RULE, 0.8)
d.t(12, BAR_Y + 12, "12패킷의 구성", 11, INK, KR, "start", 600)
x = BAR_X
for count, name, c in ((3, "수립 3", WARN), (3, "확인 3", INFO),
                       (4, "종료 4", BAD), (2, "데이터 2", OK)):
    w = BAR_W * count / TOTAL
    d.tone(x, BAR_Y, w, 26, c, 4, "33", 1.2)
    d.t(x + w / 2, BAR_Y + 17, name, 11, c)
    x += w
d.t(W - 54, BAR_Y + 17, "내용은 2/12", 11, OK, KR, "end", 600)

d.legend(816, [("실제 내용", OK), ("연결 수립", WARN), ("확인 응답", INFO), ("연결 종료", BAD)])
d.save("01-02.tcp-12packets.svg")
print("ok tcp-12packets")
