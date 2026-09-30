# 00-02.fd-tables — FD 표는 프로세스마다 하나씩
# 본문 요구(00-02 §3): "FD 표가 머신 전체에 하나가 아니라 프로세스마다 하나씩" 있어 세 프로세스가 모두 4 번을 쓰고,
#           연결 하나를 두고도 번호는 둘(클라이언트 4, 서버 5)이다 — 프로세스라는 틀 안에 FD 표가 들어 있는 포함 관계.
# 타입 스펙: type-nested — 프로세스 상자 셋 안에 FD 행. 같은 연결의 두 끝은 같은 상태색으로 짝짓는다.
# 사실 출처: 서버는 `ls -l /proc/2280369/fd` 실측, 클라이언트는 `ss -tanp` 의 fd=4 만 실측(3 번은 보지 않음).
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, OK, INFO, KR, MONO
from ddk import kr

W, H = 960, 512
BW, GAP, X0, Y0, RS = 288, 24, 24, 100, 32
procs = [
    ("서버", "pid 2280369", [("0·1·2", "터미널", None), ("3", "cpu.max", None), ("4", "listener", None),
                             ("5", "연결 · 클라이언트 1", OK), ("6", "eventpoll", None), ("7", "eventfd", None),
                             ("8·9", "pipe", None), ("10", "연결 · 클라이언트 2", INFO), ("11·12", "pipe", None)]),
    ("클라이언트 1", "pid 2280503", [("0·1·2", "터미널", None), ("3", "보지 않음", None), ("4", "연결 · 서버", OK)]),
    ("클라이언트 2", "pid 2290339", [("0·1·2", "터미널", None), ("3", "보지 않음", None), ("4", "연결 · 서버", INFO)]),
]
d = D(W, H, "NESTED · 00-02 FD TABLES", "FD 표는 프로세스마다 하나씩",
      "gonet 프로세스 셋의 FD 표를 나란히 놓은 도식. 세 프로세스 모두 처음 만든 소켓이 4 번이고, 클라이언트 1 과의 "
      "연결은 클라이언트 쪽 4 번과 서버 쪽 5 번, 클라이언트 2 와의 연결은 클라이언트 쪽 4 번과 서버 쪽 10 번으로 한 연결의 "
      "두 끝이 서로 다른 번호를 가진다. 클라이언트의 3 번은 관측하지 않았다.",
      lead="같은 색이 한 연결의 두 끝입니다. 번호는 각 상자 안에서만 뜻이 있습니다.")
BH = 44 + 9 * RS + 8
for i, (name, pid, rows) in enumerate(procs):
    x = X0 + i * (BW + GAP)
    d.box(x, Y0, BW, BH, "#0D1117", "rgba(191,192,192,0.45)", 1.0, 8)
    d.t(x + 16, Y0 + 26, name, 14, INK, KR, "start", 600)
    d.t(x + BW - 16, Y0 + 26, pid, 12, SOFT, MONO, "end")
    for j, (fd, what, c) in enumerate(rows):
        y = Y0 + 44 + j * RS
        if c:
            d.tone(x + 8, y, BW - 16, RS - 6, c, 4, "14", 1.0)
        else:
            d.box(x + 8, y, BW - 16, RS - 6, PAPER2, RULE, 0.8, 4)
        d.t(x + 24, y + 18, fd, 13, c or INK, MONO, "start", 600)
        d.t(x + 88, y + 18, what, 13, c or MUTED, kr(what), "start", 600 if c else 400)
d.legend(452, [("연결 1 의 두 끝", OK), ("연결 2 의 두 끝", INFO)])
d.save("00-02.fd-tables.svg")
print("ok fd-tables")
