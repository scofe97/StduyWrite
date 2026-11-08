# 타입 스펙: type-dp-security-matrix
# 사실 출처: 2026-11-08 실측 — 맥북에서 사용자 프로세스 sshd(OpenSSH 10.3p1) 세 개를 GatewayPorts no·yes·clientspecified 로 띄우고
#            같은 맥북의 ssh 로 -R <요청 주소>:<포트>:127.0.0.1:18099 를 걸어 lsof -iTCP -sTCP:LISTEN 으로 열린 주소를 읽었다.
#            lsof 의 * 는 주소족마다 한 줄이다: yes 는 IPv4 * 와 IPv6 * 두 줄, clientspecified + 0.0.0.0 은 IPv4 * 한 줄(RFC 4254 §7.1 "0.0.0.0" 은 IPv4 전용).
# 논지: 어느 조합이 어느 주소로 열리는가 — 서버의 GatewayPorts 와 클라이언트가 적은 수신 주소의 격자.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, RULE, INK, MUTED, SOFT, ACC, OK, WARN, KR, MONO

W, H = 984, 472
LX, CX0, CSTRIDE, CW = 24, 232, 240, 232
HY, HH = 108, 56
RY0, RSTRIDE, RH = 176, 76, 64

d = D(W, H, "MATRIX · 09-01 GATEWAYPORTS",
      "서버의 GatewayPorts 가 요청한 수신 주소를 이기거나 따른다",
      "행은 서버의 GatewayPorts 값 no·yes·clientspecified 이고 열은 ssh -R 에 적은 수신 주소(생략·0.0.0.0·127.0.0.1)입니다. "
      "칸은 서버가 실제로 연 주소입니다. no 는 0.0.0.0 을 요청해도 loopback 에만 열고, yes 는 127.0.0.1 을 요청해도 IPv4 와 IPv6 의 모든 주소에 엽니다. "
      "clientspecified 는 요청을 따르므로 0.0.0.0 을 요청하면 IPv4 의 모든 주소에만 열고, 주소를 생략하면 loopback 에 엽니다.",
      lead="행 = 서버 GatewayPorts · 열 = -R 에 적은 수신 주소 · 칸 = 서버가 실제로 연 주소")

cols = [("수신 주소 생략", "-R 2223:127.0.0.1:18099"),
        ("0.0.0.0", "-R 0.0.0.0:2223:…"),
        ("127.0.0.1", "-R 127.0.0.1:2223:…")]
d.t(LX, HY + 24, "서버의 GatewayPorts", 11, SOFT, KR, "start", 600)
for j, (t1, t2) in enumerate(cols):
    x = CX0 + j * CSTRIDE
    d.box(x, HY, CW, HH, PAPER2, RULE, 1.0)
    d.t(x + CW / 2, HY + 24, t1, 12, INK, KR if j == 0 else MONO, "middle", 600)
    d.t(x + CW / 2, HY + 44, t2, 11, MUTED, MONO, "middle")

LB = ("127.0.0.1 · [::1]", "loopback 만", OK)
LB4 = ("127.0.0.1", "loopback 만", OK)
ALL = ("*", "IPv4·IPv6 모든 주소", WARN)
ALL4 = ("*", "IPv4 모든 주소만", WARN)
rows = [
    ("no", "기본값 · 요청과 무관", [LB, LB + (True,), LB4]),
    ("yes", "요청과 무관", [ALL, ALL, ALL]),
    ("clientspecified", "요청을 따름", [LB, ALL4, LB4]),
]
for i, (name, sub, cells) in enumerate(rows):
    y = RY0 + i * RSTRIDE
    d.t(LX, y + 28, name, 13, INK, MONO, "start", 600)
    d.t(LX, y + 48, sub, 11, MUTED, KR, "start")
    for j, cell in enumerate(cells):
        val, note, tone = cell[0], cell[1], cell[2]
        focal = len(cell) > 3
        x = CX0 + j * CSTRIDE
        if focal:
            d.tone(x, y, CW, RH, ACC, 6, "1F", 1.4)
        else:
            d.tone(x, y, CW, RH, tone, 6, "14", 1.1)
        d.t(x + CW / 2, y + 28, val, 13, INK, MONO, "middle", 600)
        d.t(x + CW / 2, y + 48, note, 11, ACC if focal else MUTED, KR, "middle", 600 if focal else 400)

d.legend(424, [("loopback 만 열림", OK), ("모든 주소에 열림", WARN), ("본문이 짚는 칸", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.gatewayports.svg"
d.save(str(svg_path))
print("ok 09-01 gatewayports")
