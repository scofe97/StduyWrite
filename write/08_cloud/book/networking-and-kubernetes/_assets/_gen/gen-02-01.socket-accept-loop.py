# 02-01.socket-accept-loop — 창구를 연 뒤 서버가 도는 순환
# 본문 요구: "서버는 epoll_wait 에서 멈춰 자다가, accept 큐에 새 연결이 들어오면 커널이 깨웁니다.
#            accept4 로 연결을 꺼내면서 그 연결만의 새 fd 를 받습니다. 응답을 그 fd 에 쓰면
#            커널이 패킷으로 바꿔 내보내고, 서버는 다시 epoll_wait 로 돌아가 다음 손님을 기다립니다."
# 2026-09-15 이전 이 자리의 SVG 는 생성기가 없는 손 SVG 였다 — 한글 10px 라벨 9개와 범례 아래 여백 2px 가
#            계약 위반이었다. 사실은 그 SVG 와 본문에서만 가져왔다.
# 타입 스펙: type-state — 주체 하나(서버 프로세스)가 세 상태를 돌고 되돌아온다. 전이 라벨은 event / action.
#           자기 루프는 상태 위, 되돌아오는 전이는 상태 줄 아래로 직각 우회한다(대각선 금지).
#           coral 은 독자가 봐야 할 상태 하나 — CPU 를 쓰지 않고 잠드는 epoll_wait.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 488
d = D(W, H, "WAIT LOOP · SLEEP → WAKE → ACCEPT → REPLY",
      "창구를 연 뒤 서버가 도는 순환",
      "서버는 epoll_wait 에서 잠들어 기다리다 accept 큐에 새 연결이 들어오면 커널이 깨운다. "
      "accept4 로 연결 전용 fd 를 받고 그 fd 로 응답한 뒤 다시 epoll_wait 로 돌아간다.",
      lead="잠들어 기다림 → 커널이 깨움 → 연결 꺼냄 → 응답 → 다시 잠듦")

CY = 248
SW, SH = 196, 104
CX = [252, 552, 852]                    # stride 300 — 전이 라벨이 통로(104px) 안에 들어가게
START_X = 60
RET_Y = 376                             # 되돌아오는 전이가 지나는 줄

def state(cx, name, sub, tag, c, focal=False):
    x, y = cx - SW // 2, CY - SH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>'); tc = c
    d.t(cx, CY - 20, name, 14, tc, MONO, "middle", 600)
    d.t(cx, CY + 6, ddx.fit(sub, 13, SW - 24, sub), 13, INK, KR)
    d.t(cx, CY + 30, ddx.fit(tag, 12, SW - 24, tag), 12, MUTED, KR)

def trans(x0, x1, event, action, c=MUTED, mk="ar"):
    d.path(f"M {x0} {CY} L {x1-8} {CY}", c, 1.5, m=mk)
    mx = (x0 + x1) // 2
    d.t(mx, CY - 32, event, 12, c, KR)
    d.t(mx, CY - 14, action, 11, SOFT, KR)

# 시작 — listen 을 마친 뒤
d.o.append(f'<circle cx="{START_X}" cy="{CY}" r="6" fill="{INK}"/>')
d.path(f"M {START_X+8} {CY} L {CX[0]-SW//2-8} {CY}", MUTED, 1.5, m="ar")
d.t((START_X + CX[0] - SW // 2) // 2 + 4, CY - 14, "listen 뒤", 12, SOFT, KR)

state(CX[0], "epoll_wait", "잠든 채 대기", "CPU 안 씀", ACC, focal=True)
state(CX[1], "accept4", "연결 하나 꺼냄", "연결 전용 새 fd", INFO)
state(CX[2], "write · read", "그 fd 로 응답", "커널이 패킷으로 송신", INFO)

trans(CX[0] + SW // 2, CX[1] - SW // 2, "새 연결 도착", "커널이 깨움")
trans(CX[1] + SW // 2, CX[2] - SW // 2, "fd 받음", "입출력 시작")

# 자기 루프 — 새 연결이 없으면 계속 잠든다 (상태 위, 직각)
LX, RX, TOP = CX[0] - 40, CX[0] + 40, 148
d.path(f"M {LX} {CY-SH//2} L {LX} {TOP} L {RX} {TOP} L {RX} {CY-SH//2-8}", MUTED, 1.4, m="ar")
d.t(RX + 12, TOP + 4, "새 연결 없음 / 계속 잠듦", 12, MUTED, KR, "start")

# 되돌아오는 전이 — 응답 뒤 다음 손님 대기 (상태 줄 아래로 우회)
d.path(f"M {CX[2]} {CY+SH//2} L {CX[2]} {RET_Y} L {CX[0]} {RET_Y} L {CX[0]} {CY+SH//2+8}",
       MUTED, 1.5, m="ar", dash="6 5")
d.t((CX[0] + CX[2]) // 2, RET_Y + 24, "응답 끝 / 다음 손님 대기", 12, MUTED, KR)

d.legend(432, [("잠들어 기다리는 상태", ACC), ("syscall", INFO)])
d.save("02-01.socket-accept-loop.svg")
print("ok socket-accept-loop")
