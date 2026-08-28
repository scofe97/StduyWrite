# 01-02.tls-handshake — 비밀을 나르는 화살표는 열 개 중 하나뿐이다
# 본문 요구(01-02 §5): "메시지 열 개가 노출 상태에 따라 세 구간으로 갈린다"가 캡션이고, 본문은
#           "열 개 중 아홉을 주워도 봉인 하나를 못 열면 소용이 없다"로 맺는다. 그래서 이 그림의
#           단위는 메시지가 아니라 노출 상태다 — 배경 띠 셋이 평문·봉인·암호문 구간이고, 오른쪽
#           끝 칩이 메시지마다 그 상태를 다시 못 박는다.
#           ClientKeyExchange 만 선을 굵게(2.6) 한 것은 이 하나가 유일한 비밀이기 때문이고,
#           2단계 띠 높이가 46px 로 한 줄뿐인 것도 그 뜻이다. 내용 없는 선언(ServerHelloDone·
#           ChangeCipherSpec)은 점선으로 두어 나르는 것이 없다는 것을 선 모양으로 구분했다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 배경 띠는 시간 구간이 아니라
#           노출 상태 구간이라 레인을 가로질러 깔았다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1060, 756
Y0, STRIDE = 222, 48

d = Seq(W, H, "SEQUENCE · 01-02 TLS 1.2",
        "TLS 핸드셰이크 — 비밀을 나르는 화살표는 하나뿐",
        "TLS 1.2 핸드셰이크의 메시지 열 개가 노출 상태에 따라 세 구간으로 갈린다. 1구간 네 "
        "메시지는 전부 평문이고, 2구간의 ClientKeyExchange 하나만 공개키로 봉해져 비밀을 나르며, "
        "3구간부터 암호문이 된다. 그 하나를 열지 못하면 3구간은 통째로 읽히지 않는다.",
        lead="열 개 중 아홉을 주워도 봉인 하나를 못 열면 소용이 없습니다.")

C, S = "클라이언트", "서버"
LX = d.lanes([(C, "client"), (S, "server")], lane_w=200)
d.rails(686)
MID = (LX[C] + LX[S]) / 2
CHIP_X = LX[S] + 70        # 노출 상태 칩은 레인 오른쪽 바깥에 한 줄로 선다

for y0, h, label, c in ((198, 190, "1단계 — 전부 평문", INFO),
                        (390, 46, "2단계 — 봉인 하나", OK),
                        (438, 238, "3단계 — 암호문", ACC)):
    d.box(12, y0, W - 60, h, f"{c}0A", f"{c}33", 1, 8)
    d.t(24, y0 + 16, label, 10, c, KR, "start", 600)

# (방향, 이름, 부제, 색, 마커, 선 굵기, 라벨 굵기, 점선, 노출 상태)
MSGS = [(1, "ClientHello",       "cipher 목록 + 난수",              INFO, "info", 1.4, 400, None,  "평문"),
        (0, "ServerHello",       "cipher 하나를 고른다",             INFO, "info", 1.4, 400, None,  "평문"),
        (0, "Certificate",       "공개키가 담긴 여권",               INFO, "info", 1.4, 400, None,  "평문"),
        (0, "ServerHelloDone",   "보낼 것 다 보냈다 — 내용 없음",     SOFT, "soft", 1.4, 400, "5 5", "선언"),
        (1, "ClientKeyExchange", "premaster — 이 그림의 유일한 비밀", OK,   "ok",   2.6, 600, None,  "봉인"),
        (1, "ChangeCipherSpec",  "이제부터 암호화한다",              SOFT, "soft", 1.4, 400, "5 5", "선언"),
        (1, "Finished",          None,                            ACC,  "acc",  1.4, 400, None,  "암호문"),
        (0, "ChangeCipherSpec",  None,                            SOFT, "soft", 1.4, 400, "5 5", "선언"),
        (0, "Finished",          None,                            ACC,  "acc",  1.4, 400, None,  "암호문"),
        (1, "HTTP 요청 본문",     "아홉 개를 지나서야 내용이 나간다",   ACC,  "acc",  1.4, 400, None,  "암호문")]

for i, (fwd, name, sub, c, mk, sw, weight, dash, seal) in enumerate(MSGS):
    y = Y0 + STRIDE * i
    if fwd:
        d.path(f"M {LX[C]+10} {y} L {LX[S]-12} {y}", c, sw, m=mk, dash=dash)
    else:
        d.path(f"M {LX[S]-10} {y} L {LX[C]+12} {y}", c, sw, m=mk, dash=dash)
    d.t(LX[C] - 26, y + 4, str(i + 1), 10, SOFT, MONO, "end")
    d.t(MID, y - 8, name, 11, c, MONO, "middle", weight)
    if sub:
        d.t(MID, y + 13, sub, 9, MUTED)
    d.chip(CHIP_X, y, seal, c, 8)

d.t(W - 68, 440, "이 하나를 못 열면 아래는 통째로 못 읽는다", 10, BAD, KR, "end")
d.legend(712, [("평문 — 다 보인다", INFO), ("봉인 — 유일한 비밀", OK),
               ("암호문", ACC), ("선언 — 내용 없음", SOFT)])
d.save("01-02.tls-handshake.svg")
print("ok tls-handshake")
