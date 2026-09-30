# 00-02.close-paths — 소켓이 닫히는 두 길과 strace 에 남는 흔적
# 본문 요구(00-02 §4): "소켓이 닫히는 길은 코드의 Close() 와 프로세스 종료 두 가지이고 strace 에 close syscall 로
#           남는 것은 앞의 것뿐" — 같은 결과(소켓 닫힘)로 가는 두 경로의 대비.
# 타입 스펙: type-flowchart — 두 줄의 단계 흐름, 끝 칸이 관측 결과. focal 은 판단 근거가 되는 close(fd) 줄.
# 사실 출처: gonet-lab 실험 4 strace (SIGINT → close(4) → close(5) → shutdown 로그 → exited).
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, KR, MONO
from ddk import node, harrow

W, H = 960, 404
X, NW, NH, STEP = 24, 192, 64, 240
rows = [
    (140, [("종료 신호", "AfterFunc 실행", None, False), ("코드의 Close()", "ln · conn", None, False),
           ("close(fd)", "syscall", ACC, True), ("strace 에 찍힘", "exited 보다 먼저", OK, False)]),
    (272, [("프로세스 종료", "exit", None, False), ("커널이 정리", "남은 FD 전부", None, False),
           ("syscall 없음", "커널 안에서 처리", None, False), ("strace 에 안 찍힘", "흔적 없음", WARN, False)]),
]
d = D(W, H, "FLOWCHART · 00-02 CLOSE PATHS", "소켓이 닫히는 두 길",
      "위 줄은 종료 신호가 AfterFunc 를 실행하고 코드가 Close() 를 불러 close(fd) syscall 이 strace 에 남는 길이다. "
      "아래 줄은 프로세스가 끝나면서 커널이 남은 FD 를 안에서 정리하는 길이라 syscall 이 없고 strace 에도 남지 않는다.",
      lead="결과는 같이 닫힘이지만, strace 에 흔적이 남는 것은 위 줄뿐입니다.")
d.t(24, 124, "코드가 닫는 길", 12, SOFT, KR, "start", 600)
d.t(24, 256, "프로세스 종료로 닫히는 길", 12, SOFT, KR, "start", 600)
for y, nodes in rows:
    y += 8
    for k, (t, s, c, f) in enumerate(nodes):
        x = X + k * STEP
        node(d, x, y, NW, NH, t, s, c, f)
        if k < 3:
            harrow(d, x + NW + 6, x + STEP - 6, y + NH / 2)
d.legend(360, [("strace 에 남음", OK), ("남지 않음", WARN), ("판단 근거가 되는 줄", ACC)])
d.save("00-02.close-paths.svg")
print("ok close-paths")
