# 02-01 §6 — TCP 서버에 소켓이 둘인 이유. 원문 자신이 학생들이 여기서 헷갈린다고 적는 자리다.
# 레인을 셋으로 나눈 것은 환영 소켓과 연결 소켓이 *서로 다른 수명*을 갖기 때문이다 —
# 환영 소켓은 계속 남고, 연결 소켓은 클라이언트마다 생겼다 닫힌다.
# 타입 스펙: type-swimlane — 행마다 한 주체, 레인을 건너는 화살표가 인계다. 가장 중요한 인계에 강조색.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 604
LX = 176                      # 레인 본체 시작 x
LR = 968                      # 레인 오른쪽 끝
LANES = [("클라이언트 프로세스", "clientSocket", 122),
         ("서버 — 환영 소켓", "serverSocket", 240),
         ("서버 — 연결 소켓", "connectionSocket", 358)]
LH = 108                      # 레인 높이

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §6",
      "TCP 서버의 문은 둘입니다",
      "환영 소켓은 모든 클라이언트의 최초 접촉을 받고, 연결 소켓은 접속한 클라이언트마다 새로 생긴다.",
      "accept() 가 만드는 새 소켓이 이 그림의 강조점입니다")

# 레인
for name, sub, y in LANES:
    d.line(LX, y, LR, y, RULE, 0.8)
    d.t(12, y + 46, name, 11, INK, KR, "start", 600)
    d.t(12, y + 64, sub, 11, SOFT, MONO, "start")
d.line(LX, LANES[-1][2] + LH, LR, LANES[-1][2] + LH, RULE, 0.8)

CY = {name: y + LH / 2 for name, _, y in LANES}
BW, BH = 172, 54

def step(cx, lane, l1, l2, c=MUTED, focal=False):
    y = CY[lane]
    if focal:
        d.tone(cx - BW / 2, y - BH / 2, BW, BH, c, 6, "14", 1.4)
    else:
        d.box(cx - BW / 2, y - BH / 2, BW, BH, PAPER2, RULE, 0.9)
    d.t(cx, y - 4, l1, 11, c if focal else INK, MONO)
    d.t(cx, y + 16, l2, 11, SOFT, KR)
    return cx, y

C1, C2, C3, C4 = 276, 470, 664, 858

step(C1, "서버 — 환영 소켓", "socket + bind", "12000 을 붙입니다")
step(C1, "클라이언트 프로세스", "socket(SOCK_STREAM)", "포트는 OS 가 붙입니다")
step(C2, "클라이언트 프로세스", "connect(host, 12000)", "문을 두드립니다")
step(C2, "서버 — 환영 소켓", "listen(1) · accept()", "두드림을 듣습니다")
step(C2, "서버 — 연결 소켓", "accept()", "가 만든 이 클라이언트 전용 소켓", ACC, True)
step(C3, "클라이언트 프로세스", "send · recv", "주소를 안 붙입니다")
step(C3, "서버 — 연결 소켓", "recv · send", "바이트 스트림입니다")
step(C4, "클라이언트 프로세스", "close()", "연결을 끊습니다")
step(C4, "서버 — 연결 소켓", "close()", "이 소켓만 닫습니다")
step(C4, "서버 — 환영 소켓", "still listening", "다음 클라이언트를 받습니다", INFO, True)

# 레인 안 진행
for lane, a, b in (("클라이언트 프로세스", C1, C2), ("클라이언트 프로세스", C3, C4),
                   ("서버 — 환영 소켓", C1, C2), ("서버 — 연결 소켓", C3, C4)):
    d.path(f"M {a + BW / 2 + 6} {CY[lane]} L {b - BW / 2 - 10} {CY[lane]}", MUTED, 1.2, m="ar")

# 레인을 건너는 인계
d.path(f"M {C2} {CY['클라이언트 프로세스'] + BH / 2 + 4} L {C2} {CY['서버 — 환영 소켓'] - BH / 2 - 10}",
       MUTED, 1.3, m="ar")
d.t(C2 - 12, CY["클라이언트 프로세스"] + BH / 2 + 26, "3-way 핸드셰이크는 코드에 안 보입니다", 11, SOFT, KR, "end")

d.path(f"M {C2} {CY['서버 — 환영 소켓'] + BH / 2 + 4} L {C2} {CY['서버 — 연결 소켓'] - BH / 2 - 10}",
       ACC, 1.6, m="acc")
d.t(C2 - 12, CY["서버 — 환영 소켓"] + BH / 2 + 26, "새 소켓을 만듭니다", 11, ACC, KR, "end")

# 데이터는 클라이언트 소켓과 연결 소켓 사이에서만 흐릅니다
d.path(f"M {C3 - 26} {CY['클라이언트 프로세스'] + BH / 2 + 4} L {C3 - 26} {CY['서버 — 연결 소켓'] - BH / 2 - 10}",
       MUTED, 1.2, m="ar", dash="5 4")
d.path(f"M {C3 + 26} {CY['서버 — 연결 소켓'] - BH / 2 - 4} L {C3 + 26} {CY['클라이언트 프로세스'] + BH / 2 + 10}",
       MUTED, 1.2, m="ar", dash="5 4")
d.t(12, 506, "데이터는 클라이언트 소켓과 연결 소켓 사이에서만 흐릅니다. 환영 소켓을 거치지 않습니다.", 11, MUTED, KR, "start")
d.t(12, 528, "둘을 한 소켓으로 착각하면 두 번째 클라이언트가 왜 접속되는지 설명할 수 없습니다.", 11, MUTED, KR, "start")

d.legend(H - 52, [("이 그림의 강조점", ACC), ("계속 남는 소켓", INFO), ("일반 단계", MUTED)])
d.save("02-01.tcp-two-sockets.svg")
