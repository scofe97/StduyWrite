# 09-01 §2 — 명명 파이프 examplepipe 를 두 프로세스가 쓰고 읽을 때 무엇이 어디에 있는가.
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
# 타입 스펙: type-data-flow — 문자 x 가 PID 19628 → 커널의 파이프 버퍼(pipefs) → PID 19636 으로 건너간다.
#           층을 셋(유저 공간 · 커널 · 파일시스템)으로 나눠, 파일시스템 항목은 경로로 여는 기준점일 뿐
#           데이터가 지나가지 않는다는 것을 실선(데이터)과 점선(경로로 열기)으로 가른다. accent 는
#           프로세스보다 오래 사는 이름(파일시스템 항목) 하나.
# 근거: 본문 §2 의 ls -l 출력(prw-rw-r-- 1 mh9 mh9 0), 작업 번호 출력([1] 19628 · [2] 19636),
#       "x 가 대략 5초마다", timeout 출력(종료상태=124), "읽는 쪽을 붙이고 다시 치면 바로 0",
#       fifo(7) "반대쪽이 열릴 때까지 열기 자체가 막힙니다", "내부적으로는 pipefs".
# 축약: 버퍼 안의 x 두 칸은 FIFO 순서를 보이는 그림이고 버퍼 크기를 뜻하지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §2",
      "이름이 붙은 파이프는 프로세스보다 오래 산다",
      "명명 파이프 examplepipe 를 세 층으로 나눈 것. 두 프로세스는 파일시스템의 이름 examplepipe 로 "
      "파이프를 열고, 문자 x 는 커널 안 pipefs 의 버퍼를 지나 PID 19628 에서 PID 19636 으로 간다. "
      "파일시스템 항목은 크기가 0 이고 두 프로세스가 끝나도 남는다. 아래 띠는 읽는 쪽이 없는 p1 에 "
      "쓰려 하면 열기에서 막혀 timeout 이 124 로 끝나는 장면이다.",
      "이름은 파일시스템에 남고 데이터는 커널 안에서만 건너갑니다")

LX = 24
X0, X1 = 136, 856
WX0, WX1 = 136, 336          # 쓰는 쪽
PX0, PX1 = 396, 596          # 가운데(버퍼 · 항목)
RX0, RX1 = 636, 836          # 읽는 쪽

# 층 띠와 이름
bands = [(100, 196, "유저 공간", "두 프로세스"),
         (212, 300, "커널", "pipefs 버퍼"),
         (316, 404, "파일시스템", "끝나도 남음")]
for y0, y1, name, sub in bands:
    d.o.append(f'<rect x="{LX}" y="{y0}" width="{X1 - LX}" height="{y1 - y0}" rx="8" '
               f'fill="{PAPER2}" fill-opacity="0.45" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(LX + 14, y0 + 26, name, 13, INK, KR, "start", 600)
    d.t(LX + 14, y0 + 44, sub, 12, SOFT, KR, "start")

# 선은 글자보다 먼저 그린다
# 경로로 열기(점선): 프로세스 → 파일시스템 항목
d.arrow([(176, 184), (176, 360), (PX0 - 4, 360)], SOFT, "soft", 1.2, "4 3")
d.arrow([(796, 184), (796, 360), (PX1 + 4, 360)], SOFT, "soft", 1.2, "4 3")
# 항목 → 버퍼 (이름이 가리키는 파이프)
d.arrow([((PX0 + PX1) / 2, 332), ((PX0 + PX1) / 2, 284)], SOFT, "soft", 1.2, "4 3")
# 데이터 x (실선): 쓰는 쪽 → 버퍼 → 읽는 쪽
d.arrow([(296, 184), (296, 256), (PX0 - 4, 256)], INFO, "info", 1.6)
d.arrow([(PX1, 256), (676, 256), (676, 188)], OK, "ok", 1.6)

# 유저 공간 — 두 프로세스
d.box(WX0, 112, WX1 - WX0, 72, PAPER, INFO, 1.2, 8)
d.t(WX0 + 14, 134, "PID 19628  [1]", 13, INFO, MONO, "start", 600)
d.t(WX0 + 14, 154, 'echo "x" > examplepipe', 12, INK, MONO, "start")
d.t(WX0 + 14, 173, "while 루프 · 5초마다", 12, MUTED, KR, "start")
d.box(RX0, 112, RX1 - RX0, 72, PAPER, OK, 1.2, 8)
d.t(RX0 + 14, 134, "PID 19636  [2]", 13, OK, MONO, "start", 600)
d.t(RX0 + 14, 154, "cat < examplepipe", 12, INK, MONO, "start")
d.t(RX0 + 14, 173, "터미널에 x · 약 5초마다", 12, MUTED, KR, "start")

# 커널 — 파이프 버퍼
d.box(PX0, 228, PX1 - PX0, 56, PAPER, MUTED, 1.1, 8)
d.t(PX0 + 14, 248, "파이프 버퍼", 12, INK, KR, "start", 600)
d.t(PX1 - 14, 248, "FIFO", 12, MUTED, MONO, "end")
for i in range(2):
    cx = PX0 + 80 + i * 44
    d.o.append(f'<rect x="{cx - 16}" y="{256}" width="32" height="20" rx="3" '
               f'fill="{INFO}22" stroke="{INFO}" stroke-width="0.9"/>')
    d.t(cx, 271, "x", 12, INK, MONO)
d.t(PX0 + 14, 271, "먼저 →", 11, SOFT, KR, "start")
d.t(308, 246, "write x", 12, INFO, MONO, "start")
d.t(664, 246, "read x", 12, OK, MONO, "end")

# 파일시스템 — 이름(항목)
d.tone(PX0, 332, PX1 - PX0, 56, ACC, 8, "14", 1.4)
d.t(PX0 + 14, 354, "examplepipe", 13, ACC, MONO, "start", 600)
d.t(PX0 + 14, 376, "prw-rw-r-- 1 mh9 mh9 0", 12, INK, MONO, "start")
d.t(236, 352, "경로로 열기", 12, SOFT, KR, "middle")
d.t(716, 352, "경로로 열기", 12, SOFT, KR, "middle")
d.t((PX0 + PX1) / 2 + 10, 312, "가리킴", 11, SOFT, KR, "start")

# 아래 띠 — 읽는 쪽이 없는 p1
BY = 428
d.o.append(f'<rect x="{LX}" y="{BY}" width="{X1 - LX}" height="96" rx="8" '
           f'fill="{WARN}0D" stroke="{WARN}" stroke-width="1.2"/>')
d.t(LX + 14, BY + 26, "p1", 13, WARN, MONO, "start", 600)
d.t(LX + 14, BY + 44, "읽는 쪽 없음", 12, SOFT, KR, "start")
d.arrow([(336, BY + 36), (392, BY + 36)], WARN, "warn", 1.4)
d.arrow([(596, BY + 36), (632, BY + 36)], WARN, "warn", 1.4)
d.box(WX0, BY + 16, WX1 - WX0, 40, PAPER, WARN, 1.0, 6)
d.t((WX0 + WX1) / 2, BY + 41, "echo x > p1", 12, INK, MONO)
d.box(PX0, BY + 16, PX1 - PX0, 40, PAPER, WARN, 1.0, 6)
d.t((PX0 + PX1) / 2, BY + 41, "열기에서 멈춤", 12, WARN, KR)
d.box(RX0, BY + 16, RX1 - RX0, 40, PAPER, WARN, 1.0, 6)
d.t((RX0 + RX1) / 2, BY + 41, "timeout 2 → 124", 12, INK, MONO)
d.t(PX0, BY + 80, "cat 으로 읽는 쪽을 붙이면 → 바로 0", 12, MUTED, KR, "start")

d.t(LX, 552, "실선 = 데이터 x · 점선 = 경로로 열기 · 버퍼의 x 두 칸은 순서를 보이는 그림",
    11, SOFT, KR, "start")
d.legend(580, [("쓰는 쪽", INFO), ("읽는 쪽", OK), ("남는 이름", ACC), ("막히는 조건", WARN)])
d.save("09-01.named-pipe.svg")
print("ok 09-01.named-pipe")
