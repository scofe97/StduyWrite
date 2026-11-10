# 08-02 §4 — 멈춘 서버의 받을 큐에 5000바이트가 쌓였다가 깨우면 0 으로 돌아간다.
# 실측: debian:12 컨테이너 (2026-11-10).
#   nc -l 127.0.0.1 8000 & ; exec 5<>/dev/tcp/127.0.0.1/8000 ; kill -STOP <nc> ;
#   head -c 5000 /dev/zero >&5 ; ss -atnp → "ESTAB 5000 0 127.0.0.1:8000 127.0.0.1:40258 nc,pid=3798,fd=4"
#   kill -CONT <nc> ; ss -atnp → Recv-Q 0
# 1차 자료: ss(8) -a "Display both listening and non-listening (for TCP this means established connections)".
# 타입 스펙: type-sequence — 참여자 셋(클라이언트 bash, 커널 소켓, 서버 nc)의 시간순 메시지와 상태 칩.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INFO, WARN, OK

W, H = 920, 628
d = Seq(W, H, "LEARNING MODERN LINUX · 08-02 §4",
        "받을 큐에 쌓이는 5000바이트",
        "서버 nc 를 SIGSTOP 으로 멈춘 채 클라이언트가 5000바이트를 보내면 커널이 받아 둔 바이트가 "
        "ss 의 Recv-Q 에 남는다. SIGCONT 로 깨우면 nc 가 읽어 0 으로 돌아간다.",
        "Recv-Q 가 계속 쌓이면 그 소켓을 읽는 앱이 못 따라가고 있습니다")

d.lanes([("클라이언트 bash", "fd 5 · :40258"), ("커널 소켓", "127.0.0.1:8000"),
         ("서버 nc", "pid 3798 · fd 4")], y0=104, lane_w=208)
d.rails(H - 64)

Y = 192
d.msg("클라이언트 bash", "커널 소켓", "connect", Y, INFO, "info", sub="/dev/tcp")
d.state("커널 소켓", "ESTAB · Recv-Q 0", Y + 44, SOFT)
d.selfmsg("서버 nc", "SIGSTOP", Y + 96, WARN, sub="읽기 멈춤")
d.msg("클라이언트 bash", "커널 소켓", "write 5000 B", Y + 148, INFO, "info")
d.state("커널 소켓", "ESTAB · Recv-Q 5000", Y + 192, ACC)
d.selfmsg("서버 nc", "SIGCONT", Y + 244, OK, sub="다시 실행")
d.msg("커널 소켓", "서버 nc", "read 5000 B", Y + 296, OK, "ok")
d.state("커널 소켓", "ESTAB · Recv-Q 0", Y + 340, SOFT)

d.legend(H - 48, [("요청", INFO), ("멈춤", WARN), ("쌓인 큐", ACC), ("읽기 재개", OK)])
d.save("08-02.socket-queue.svg")
print("ok 08-02.socket-queue")
