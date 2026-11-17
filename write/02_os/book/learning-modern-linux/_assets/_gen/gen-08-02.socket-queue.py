# 08-02 §4 — 멈춘 서버의 받을 큐에 5000바이트가 쌓인다. ss -atnp 출력의 세 줄을 실제 객체로 그린다:
#           유저 공간의 프로세스와 그 fd, 커널 안의 소켓 셋(LISTEN · 서버 쪽 ESTAB · 클라이언트 쪽 ESTAB)과
#           각 소켓의 Recv-Q · Send-Q.
# 실측: debian:12 컨테이너 (2026-11-10).
#   nc -l 127.0.0.1 8000 & ; exec 5<>/dev/tcp/127.0.0.1/8000 ; kill -STOP <nc> ;
#   head -c 5000 /dev/zero >&5 ; ss -atnp →
#     LISTEN 0    1 127.0.0.1:8000  0.0.0.0:*        users:(("nc",pid=3798,fd=3))
#     ESTAB  5000 0 127.0.0.1:8000  127.0.0.1:40258  users:(("nc",pid=3798,fd=4))
#     ESTAB  0    0 127.0.0.1:40258 127.0.0.1:8000   users:(("cat",pid=3806,fd=5),("ss",pid=3805,fd=5),("bash",pid=1,fd=5))
#   kill -CONT <nc> ; ss -atnp → Recv-Q 0
# 1차 자료: ss(8) -a "Display both listening and non-listening (for TCP this means established connections)".
#   Recv-Q · Send-Q 의 뜻은 본문 §4 (netstat(8) 각주): 받아 두었으나 앱이 안 읽은 바이트 · 보냈으나 ACK 안 된 바이트.
#   클라이언트 쪽 Send-Q 0 은 그 정의에 따라 5000바이트가 모두 ACK 받았다는 뜻이다.
# 타입 스펙: type-architecture — 유저 공간과 커널 두 존 안에 프로세스와 소켓을 두고, fd 가 둘을 잇는다.
#           write 가 루프백으로 서버 쪽 소켓의 Recv-Q 에 닿는다. 축약: LISTEN 소켓의 Send-Q 1 은
#           출력 그대로 옮기고 뜻은 적지 않는다(본문이 설명하지 않는다). SIGCONT 뒤의 Recv-Q 0 은
#           바닥 한 줄로만 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §4",
      "받을 큐에 쌓이는 5000바이트",
      "ss -atnp 출력의 세 줄을 객체로 그린 것. 클라이언트 bash 와 fd 5 를 물려받은 ss · cat 이 "
      "127.0.0.1:40258 소켓을 쥐고, 서버 nc(pid 3798)가 fd 3 으로 LISTEN 소켓을, fd 4 로 연결 소켓을 쥔다. "
      "nc 를 SIGSTOP 으로 멈춘 채 5000바이트를 쓰면 루프백을 건너 서버 쪽 연결 소켓의 Recv-Q 에 5000 이 남고, "
      "클라이언트 쪽은 Recv-Q 0 · Send-Q 0 이다. SIGCONT 로 깨우면 nc 가 읽어 0 으로 돌아간다.",
      "Recv-Q 가 계속 쌓이면 그 소켓을 읽는 앱이 못 따라가고 있습니다")

ZX, ZW = 24, 872
UY, UH = 104, 116          # 유저 공간 존
KY, KH = 260, 236          # 커널 존


def zone(y, h):
    d.o.append(f'<rect x="{ZX}" y="{y}" width="{ZW}" height="{h}" rx="8" fill="rgba(245,245,243,0.02)" '
               f'stroke="rgba(245,245,243,0.18)" stroke-width="0.8" stroke-dasharray="4 3"/>')


def zone_label(y, label, x=ZX + 12):   # 연결선이 지나지 않는 자리에 둔다
    d.o.append(f'<rect x="{x}" y="{y - 7}" width="{len(label) * 6.2 + 12}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x + 6, y + 4, label, 9, SOFT, MONO, "start")


zone(UY, UH)
zone(KY, KH)

# 노드 좌표
PROCS = [("bash", "pid 1 · fd 5"), ("ss", "pid 3805 · fd 5"), ("cat", "pid 3806 · fd 5")]
PX0, PW_, PH, PSTR, PY = 48, 120, 48, 128, 140
CSX, CSY, CSW, CSH = 72, 340, 360, 132          # 클라이언트 쪽 연결 소켓
NX, NY, NW, NH = 568, 136, 304, 56             # 서버 nc
LX, LY, LW, LH = 568, 288, 176, 44             # LISTEN 소켓
SSX, SSY, SSW, SSH = 568, 352, 304, 120        # 서버 쪽 연결 소켓
QX, QY, QW, QH = SSX + 16, SSY + 56, SSW - 32, 26   # Recv-Q 띠
FD3X, FD4X = 640, 816

# 연결선 먼저(글자·상자 아래로)
for i, _ in enumerate(PROCS):
    cx = PX0 + i * PSTR + PW_ / 2
    d.line(cx, PY + PH, cx, CSY, INFO, 1.1)
d.line(FD3X, NY + NH, FD3X, LY, MUTED, 1.1)
d.line(FD4X, NY + NH, FD4X, SSY, WARN, 1.3, "4 3")
d.arrow([(CSX + CSW, QY + QH / 2), (QX - 4, QY + QH / 2)], ACC, "acc", 1.6)

zone_label(UY, "USER SPACE")
zone_label(KY, "KERNEL · 127.0.0.1 LOOPBACK", 392)   # fd 5 선(108·236·364)과 fd 3 선(640) 사이

# 유저 공간
for i, (name, sub) in enumerate(PROCS):
    x = PX0 + i * PSTR
    d.box(x, PY, PW_, PH, PAPER2, INFO, 1.0, 6)
    d.t(x + PW_ / 2, PY + 20, name, 13, INK, MONO, "middle", 600)
    d.t(x + PW_ / 2, PY + 38, sub, 11.5, MUTED, MONO)
d.t(PX0 + 3 * PSTR - 4, PY + 30, "← fd 5 를 물려받음", 12, SOFT, KR, "start")
d.box(NX, NY, NW, NH, PAPER2, WARN, 1.2, 6)
d.t(NX + 16, NY + 24, "nc", 13, INK, MONO, "start", 600)
d.t(NX + 48, NY + 24, "pid 3798", 12, MUTED, MONO, "start")
d.t(NX + 16, NY + 44, "SIGSTOP 으로 멈춤 · 읽지 않음", 12, WARN, KR, "start")

# fd 라벨(존 사이 틈)
d.t(FD3X - 8, 244, "fd 3", 12, MUTED, MONO, "end")
d.t(FD4X - 8, 244, "fd 4 · read 없음", 12, WARN, KR, "end")

# 커널 — 클라이언트 쪽 연결 소켓
d.box(CSX, CSY, CSW, CSH, PAPER2, INFO, 1.1, 6)
d.t(CSX + 16, CSY + 24, "ESTAB", 13, INFO, MONO, "start", 600)
d.t(CSX + 80, CSY + 24, "127.0.0.1:40258 → :8000", 12, INK, MONO, "start")
for j, (lab, note) in enumerate((("Recv-Q 0", "받아 둔 바이트 없음"), ("Send-Q 0", "5000 B 모두 ACK 받음"))):
    y = CSY + 52 + j * 36
    d.o.append(f'<rect x="{CSX + 16}" y="{y}" width="{CSW - 208}" height="24" rx="3" fill="none" '
               f'stroke="{RULE}" stroke-width="0.9"/>')
    d.t(CSX + 28, y + 17, lab, 12, INK, MONO, "start")
    d.t(CSX + CSW - 176, y + 17, note, 12, MUTED, KR, "start")
d.t((CSX + CSW + QX) / 2, QY - 10, "write 5000 B", 12, ACC, MONO, "middle", 600)

# 커널 — LISTEN 소켓
d.box(LX, LY, LW, LH, PAPER2, MUTED, 1.0, 6)
d.t(LX + 12, LY + 18, "LISTEN  :8000", 12, INK, MONO, "start", 600)
d.t(LX + 12, LY + 35, "Recv-Q 0 · Send-Q 1", 11.5, MUTED, MONO, "start")

# 커널 — 서버 쪽 연결 소켓과 Recv-Q
d.box(SSX, SSY, SSW, SSH, PAPER2, ACC, 1.1, 6)
d.t(SSX + 16, SSY + 24, "ESTAB", 13, ACC, MONO, "start", 600)
d.t(SSX + 80, SSY + 24, "127.0.0.1:8000 ← :40258", 12, INK, MONO, "start")
d.tone(QX, QY, QW, QH, ACC, 3, "40", 1.4)
d.t(QX + QW / 2, QY + 18, "Recv-Q 5000", 13, INK, MONO, "middle", 600)
d.t(SSX + 16, SSY + SSH - 14, "Send-Q 0", 12, MUTED, MONO, "start")

d.t(ZX, 524, "SIGCONT 뒤 · nc 가 fd 4 로 읽음 → Recv-Q 0", 12, SOFT, KR, "start")
d.legend(H - 48, [("클라이언트 쪽 프로세스·소켓", INFO), ("멈춘 서버 nc", WARN), ("쌓인 받을 큐", ACC)])
d.save("08-02.socket-queue.svg")
print("ok 08-02.socket-queue")
