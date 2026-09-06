# 09-01 §1 — 명명 파이프 하나를 두 프로세스가 나눠 쓰는 장면.
# 원문("Named Pipes"): "named pipes are pipes to which you can assign custom names" ·
#       "Just like unnamed pipes, named pipes work with normal file I/O ( open , write , etc.) and
#       provide first in, first out (FIFO) delivery. Unlike unnamed pipes, the lifetime of a named pipe
#       is not limited to the processes it's used with. Technically, named pipes are a wrapper around
#       pipes, using the pipefs pseudo filesystem" ·
#       주석: "Looking at the pipe with ls reveals its type: the first letter is a p" ·
#       "Using a loop, we publish the character x into our pipe. Note that unless some other process
#       reads from examplepipe , the pipe is blocked. No further writing into it is possible." ·
#       "We launch a second process that reads from the pipe in a loop." ·
#       "we see x appearing on the terminal, roughly every five seconds. In other words, it appears
#       every time the process with PID 19636 is able to read from the named pipe with cat."
#       한계는 "they're also limited, since they support only one direction and one consumer" 다.
# 타입 스펙: type-data-flow — 파이프라인 단계마다 누가 무엇을 하는지. 칸 사이를 건너가는 것이 문자 x 라서
#           주체만 반복되는 process 가 아니라 data-flow 다. 축약: mkfifo 와 ls 출력은 본문 코드 블록이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 468
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §1",
      "이름이 붙은 파이프는 프로세스보다 오래 산다",
      "저자의 예제를 세 자리로 세운 것. 가운데가 파일시스템에 실재하는 파이프라 양쪽 프로세스가 죽어도 "
      "남는다. 붉은 자리가 읽는 쪽이 없을 때 일어나는 일이다.",
      "쓰는 쪽은 읽는 쪽이 나타날 때까지 막힙니다")

CW, CH, Y0 = 228, 118, 138
COLX = [24, 326, 628]
d.box(COLX[0], Y0, CW, CH, PAPER2, INFO, 1.2, 8)
d.t(COLX[0] + 16, Y0 + 28, "발행 프로세스", 14, INFO, KR, "start", 600)
d.t(COLX[0] + 16, Y0 + 52, "PID 19628", 11.5, MUTED, MONO, "start")
d.t(COLX[0] + 16, Y0 + 76, "echo \"x\" > examplepipe", 11.5, INK, MONO, "start")
d.t(COLX[0] + 16, Y0 + 98, "5 초마다 한 번", 11.5, MUTED, KR, "start")

d.box(COLX[1], Y0, CW, CH, PAPER, ACC, 1.4, 8)
d.t(COLX[1] + 16, Y0 + 28, "examplepipe", 14, ACC, MONO, "start", 600)
d.t(COLX[1] + 16, Y0 + 52, "prw-rw-r--  첫 글자가 p", 11.5, INK, MONO, "start")
d.t(COLX[1] + 16, Y0 + 76, "먼저 들어간 것이 먼저 나온다", 11.5, MUTED, KR, "start")
d.t(COLX[1] + 16, Y0 + 98, "pipefs 위에 얹힌 껍데기", 11.5, MUTED, KR, "start")

d.box(COLX[2], Y0, CW, CH, PAPER2, OK, 1.2, 8)
d.t(COLX[2] + 16, Y0 + 28, "소비 프로세스", 14, OK, KR, "start", 600)
d.t(COLX[2] + 16, Y0 + 52, "PID 19636", 11.5, MUTED, MONO, "start")
d.t(COLX[2] + 16, Y0 + 76, "cat < examplepipe", 11.5, INK, MONO, "start")
d.t(COLX[2] + 16, Y0 + 98, "5 초마다 한 번", 11.5, MUTED, KR, "start")

for a, b, lab in ((0, 1, "x 를 쓴다"), (1, 2, "x 를 읽는다")):
    y = Y0 + CH / 2
    d.arrow([(COLX[a] + CW, y), (COLX[b] - 4, y)], MUTED, "ar", 1.4)
    d.t((COLX[a] + CW + COLX[b]) / 2, y - 12, lab, 11, MUTED, KR)

GY = Y0 + CH + 30
d.tone(24, GY, W - 48, 62, WARN, 8, "12", 1.3)
d.t(44, GY + 26, "읽는 쪽이 없으면 파이프가 막힙니다", 13.5, WARN, KR, "start", 600)
d.t(44, GY + 46, "저자의 말로는 다른 프로세스가 examplepipe 에서 읽지 않는 한 더 쓸 수 없습니다.",
    12, MUTED, KR, "start")

NY = GY + 86
d.t(24, NY, "이름 없는 파이프와 다른 점은 수명입니다. 쓰이는 프로세스에 묶이지 않아 양쪽이 죽어도 파일은 남습니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 24, "한계는 저자가 바로 짚습니다. 방향이 하나이고 소비자도 하나뿐이라, 그 둘을 풀려면 다음 절의 "
                 "도메인 소켓으로 갑니다.", 12, SOFT, KR, "start")

d.legend(424, [("파일시스템에 남는 자리", ACC), ("쓰는 쪽", INFO),
                   ("읽는 쪽", OK), ("막히는 조건", WARN)])
d.save("09-01.named-pipe.svg")
print("ok 09-01.named-pipe")
