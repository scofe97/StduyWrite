# 02-01.listen-backlog-queues — listen 두 번째 인자가 정하는 칸은 뒤쪽 큐다
# 본문 요구(§1 '읽어내기'): "listen 의 두 번째 인자는 수립이 끝났지만 아직 accept 로 받아 가지 않은
#            연결을 담는 칸 수다(accept 큐). 큐가 둘이라 SYN 만 받고 3-way 가 안 끝난 반쯤 열린 연결은
#            SYN 큐에 쌓이고 그 크기는 net.ipv4.tcp_max_syn_backlog 가 정한다. accept 큐가 넘치면
#            커널은 거절하지 않고 SYN/ACK 를 조용히 버린다."
#            앞선 도식(socket-syscall)은 '한 줄이 무엇을 남기는가'라는 정적 구조라 accept 큐 하나만
#            담고 있다 — listen 인자 → accept 큐 → 넘치면 지연까지가 거기 있으므로 다시 그리지 않는다.
#            이 도식이 맡는 것은 **큐가 둘이라는 사실과 각 큐가 채워지는 시점**이다. 3-way 핸드셰이크
#            위에서 SYN 큐(tcp_max_syn_backlog)와 accept 큐(listen 인자)가 언제 채워지고 언제 비는지를
#            시간축으로 편다. 넘침 동작도 socket-syscall 의 문구를 되풀이하지 않고 재전송 쪽을 말한다.
# 타입 스펙: type-sequence.md — 논지가 '연결 하나가 시간 순서로 두 칸을 거친다'라 시간축이 필요하다.
#           참여자 3(<=5), 메시지 9(<=12), 조합 프래그먼트 1개 단일 region opt(hard default).
#           응답 방향은 점선 + 채운 마커. 활성 막대는 커널 레인 하나.
#           coral 은 스펙 기본값(주 성공 응답) 대신 스타일 계약을 따라 '본문이 짚는 단 하나의 논점'인
#           accept 큐 칸에 건다 — 이 절이 설명하는 것이 listen 두 번째 인자이기 때문이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 880
d = D(W, H, "LISTEN BACKLOG · SYN QUEUE → ACCEPT QUEUE",
      "연결 하나가 두 큐를 거쳐 accept 로 나오는 길",
      "SYN 만 받은 반쯤 열린 연결은 SYN 큐에 쌓이고, 3-way 가 끝나면 accept 큐로 옮겨진다. "
      "listen 의 두 번째 인자가 정하는 것은 뒤쪽 accept 큐의 칸 수다. 그 칸이 없으면 커널은 "
      "거절하지 않고 SYN/ACK 를 조용히 버려 클라이언트의 재전송을 기다린다.",
      lead="두 큐가 채워지는 시점이 다르다 · listen 두 번째 인자가 정하는 것은 뒤쪽 칸뿐이다")

LX = ddx.lanes(d, [("클라이언트", "연결을 거는 쪽"),
                   ("커널", "SYN 큐 · accept 큐"),
                   ("서버 프로세스", "listen · accept4")], y0=104, lane_w=212)
Y = [188, 236, 284, 332, 380, 428, 476]
RAIL_BOT = 680
for x in LX.values():
    d.line(x, d.lane_top + 6, x, RAIL_BOT, RULE, 1.0, "3 6")
# 활성 막대 — 두 큐를 들고 있는 동안 제어권은 커널에 있다
d.o.append(f'<rect x="{LX["커널"]-4}" y="{Y[0]}" width="8" height="{628-Y[0]}" '
           f'fill="{MUTED}18" stroke="{SOFT}" stroke-width="0.8"/>')


def msg(a, b, label, sub, y, c=MUTED, dash=None):
    x1, x2 = LX[a], LX[b]; dr = 1 if x2 > x1 else -1
    d.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m="ar", dash=dash)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, c, MONO, "middle", 600)
    d.t(mx, y + 18, sub, 12, MUTED, KR)


def selfmsg(a, label, sub, y, c=MUTED):
    x = LX[a]
    d.path(f"M {x+10} {y-12} L {x+64} {y-12} L {x+64} {y+12} L {x+13} {y+12}", c, 1.4, m="ar")
    d.t(x + 76, y - 4, label, 12, c, KR, "start", 600)
    d.t(x + 76, y + 16, sub, 12, SOFT, KR, "start")


msg("클라이언트", "커널", "SYN", "연결 요청", Y[0])
selfmsg("커널", "SYN 큐에 적재", "3-way 미완 · 반쯤 열린 연결", Y[1], INFO)
msg("커널", "클라이언트", "SYN/ACK", "여기까지가 반쯤 열린 상태", Y[2], dash="5 4")
msg("클라이언트", "커널", "ACK", "3-way 완료", Y[3])
selfmsg("커널", "accept 큐로 옮김", "빈 칸이 있을 때만", Y[4], INFO)
msg("서버 프로세스", "커널", "accept4()", "큐에서 하나 꺼냄", Y[5])
msg("커널", "서버 프로세스", "fd", "연결 전용 파일 디스크립터", Y[6], dash="5 4")

# ── opt 프래그먼트 — 뒤쪽 칸이 없을 때 ─────────────────────────────
FX0, FX1, FY0, FY1 = 88, 944, 508, 664
d.o.append(f'<rect x="{FX0}" y="{FY0}" width="{FX1-FX0}" height="{FY1-FY0}" rx="4" '
           f'fill="{INK}06" stroke="{WARN}" stroke-width="1.0"/>')
d.o.append(f'<rect x="{FX0}" y="{FY0}" width="44" height="16" rx="2" '
           f'fill="{PAPER}" stroke="{WARN}" stroke-width="1.0"/>')
d.t(FX0 + 22, FY0 + 12, "OPT", 9, WARN, MONO)
d.t(FX0 + 56, FY0 + 12, "[accept 큐에 빈 칸이 없으면]", 11, WARN, KR, "start")

selfmsg("커널", "SYN/ACK 를 조용히 버림", "RST 아님 · 로그도 없음", 580, WARN)
msg("클라이언트", "커널", "SYN 재전송", "재전송 사이에 accept 큐가 비면 성립", 628, WARN)

# ── 두 칸 — 같은 연결이 앞 칸에서 뒤 칸으로 ────────────────────────
PX0, PX1, PY0, PY1 = 40, 960, 696, 808
d.box(PX0, PY0, PX1 - PX0, PY1 - PY0, PAPER2, RULE, 1.0, 8)
d.t(PX0 + 24, PY0 + 20, "두 큐 · 칸 수를 정하는 설정이 따로다", 12, SOFT, KR, "start")

CELL_Y, CELL_H = 732, 60
for x0, name, sub, c in ((72, "SYN 큐", "net.ipv4.tcp_max_syn_backlog", INFO),
                         (528, "accept 큐", "min(listen 인자, net.core.somaxconn)", ACC)):
    d.o.append(f'<rect x="{x0}" y="{CELL_Y}" width="360" height="{CELL_H}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="{1.4 if c is ACC else 1.1}"/>')
    d.t(x0 + 180, CELL_Y + 26, ddx.fit(name, 13, 340, name), 13, c, KR, "middle", 600)
    d.t(x0 + 180, CELL_Y + 48, ddx.fit(sub, 11, 340, sub), 11, MUTED, MONO)
d.path(f"M 440 {CELL_Y+CELL_H//2} L 520 {CELL_Y+CELL_H//2}", MUTED, 1.5, m="ar")
d.t(480, CELL_Y + 12, "3-way 완료", 11, MUTED, KR)

d.legend(824, [("반쯤 열린 연결", INFO), ("listen 이 정하는 칸", ACC), ("칸이 없을 때", WARN)])
d.save("02-01.listen-backlog-queues.svg")
print("ok listen-backlog-queues")
