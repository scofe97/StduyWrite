# 01-01.socket-lanes — echo 한 번이 지나는 길: splice(pipe) 와 버퍼 복사
# 본문 요구(01-01 §3 「연결 하나가 쓰는 FD 는 셋입니다」, §4 「직접 쓴 루프는 pipe 를 쓰지 않습니다」):
#           소켓 하나(FD 1) 안의 수신·송신 두 차선 사이를 io.Copy(conn, conn) 는 커널 안 pipe(FD 2)로 잇고,
#           직접 쓴 루프는 프로세스의 buf 로 잇는다 — 연결당 FD 3 과 1 의 차이.
# 타입 스펙: type-flowchart — 두 줄의 단계 흐름(도착 → 수신 버퍼 → 가운데 → 송신 버퍼 → 전송). focal 은 FD 를 먹는 pipe.
# 사실 출처: go1.25.1 net/splice_linux.go spliceFrom, internal/poll/splice_linux.go Splice·getPipe·newPipe(pipe2),
#           Phase 3 실측(연결 100: pipe 200 / 고친 뒤 연결 30: pipe 0, FD 37).
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, KR
from ddk import node, harrow

W, H = 960, 420
X, NW, NH, STEP = 24, 132, 64, 198
rows = [
    (140, "io.Copy(conn, conn) — splice", [("클라이언트", "보냄", None, False), ("수신 버퍼", "소켓 · FD 1", None, False),
           ("pipe", "커널 안 · FD 2", ACC, True), ("송신 버퍼", "같은 소켓", None, False), ("클라이언트", "받음", None, False)],
     ["도착", "splice", "splice", "전송"]),
    (272, "직접 쓴 루프 — 버퍼 복사", [("클라이언트", "보냄", None, False), ("수신 버퍼", "소켓 · FD 1", None, False),
           ("buf 32KB", "프로세스 메모리", OK, False), ("송신 버퍼", "같은 소켓", None, False), ("클라이언트", "받음", None, False)],
     ["도착", "Read", "Write", "전송"]),
]
d = D(W, H, "FLOWCHART · 01-01 SOCKET LANES", "echo 한 번이 지나는 길",
      "소켓 하나에는 수신 버퍼와 송신 버퍼 두 차선이 있고 FD 는 하나다. io.Copy(conn, conn) 은 두 차선 사이를 "
      "splice 로 잇느라 커널 안에 pipe 를 하나 두어 연결마다 FD 를 두 개 더 쓴다. 직접 쓴 Read·Write 루프는 "
      "프로세스의 buf 를 거쳐 FD 는 소켓 하나뿐이지만 데이터가 커널과 프로세스 사이를 한 번 오간다.",
      lead="가운데 칸이 pipe 면 연결마다 FD 3 개, buf 면 1 개입니다.")
for y, label, nodes, arrows in rows:
    d.t(24, y - 16, label, 12, SOFT, KR, "start", 600)
    y += 8
    for k, (t, s, c, f) in enumerate(nodes):
        x = X + k * STEP
        node(d, x, y, NW, NH, t, s, c, f, 13)
        if k < 4:
            harrow(d, x + NW + 6, x + STEP - 6, y + NH / 2, label=arrows[k])
d.legend(372, [("FD 를 더 먹는 칸", ACC), ("FD 없이 메모리만 쓰는 칸", OK)])
d.save("01-01.socket-lanes.svg")
print("ok socket-lanes")
