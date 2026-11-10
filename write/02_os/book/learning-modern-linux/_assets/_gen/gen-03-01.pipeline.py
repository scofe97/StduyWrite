# 03-01 §2 「파이프라인이 실제로 이어지는 방식」 — 파이프 버퍼를 사이에 둔 세 장면.
# 근거: pipe(7) "Since Linux 2.6.11, the pipe capacity is 16 pages (i.e., 65,536 bytes in a system with a page
#       size of 4096 bytes)", "If the pipe is full, then a write(2) will block or fail", "If all file descriptors
#       referring to the read end of a pipe have been closed, then a write(2) will cause a SIGPIPE signal".
#       Debian 12 컨테이너(bash 5.2) 실행 결과(2026-11-10): `printf 'a\nb\nc\n' | wc -l` → 3,
#       `dd if=/dev/zero bs=4096 oflag=nonblock | sleep 1` → 16+0 records out · 65536 bytes,
#       `yes | head -1; echo "${PIPESTATUS[@]}"` → y / 141 0.
# 타입 스펙: type-data-flow — 쓰는 쪽 · 버퍼 · 읽는 쪽 세 자리를 고정하고 장면마다 데이터가 어디에 있는지 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 960, 576
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "파이프 버퍼를 사이에 둔 세 장면",
      "쓰는 프로세스, 커널 파이프 버퍼 16칸(칸마다 4,096바이트, 합 65,536바이트), 읽는 프로세스를 같은 자리에 두고 "
      "세 장면을 쌓았다. 첫 장면은 6바이트가 지나가 wc -l 이 3 을 낸다. 둘째는 읽지 않는 sleep 앞에서 16칸이 가득 찬다. "
      "셋째는 head -1 이 먼저 끝나 yes 가 SIGPIPE 로 141 을 남긴다.",
      "두 프로세스는 동시에 돌고, 그 사이의 버퍼가 속도 차이를 받아 냅니다")

WX, WW = 20, 250
RX, RW = 700, 240
CX0, CWD, CSTEP, NC = 304, 20, 22, 16
BH = 72

d.t(WX + WW / 2, 98, "쓰는 쪽 · FD 1", 12, MUTED)
d.t(480, 98, "커널 파이프 버퍼 · 4,096 B × 16칸", 12, MUTED)
d.t(RX + RW / 2, 98, "읽는 쪽 · FD 0", 12, MUTED)


def scene(y0, tag, wcmd, wsub, rcmd, rsub, filled, c, blabel, rdash=False):
    d.t(WX, y0 - 10, tag, 12, SOFT, KR, "start", 600)
    d.box(WX, y0, WW, BH, PAPER2, RULE, 1.0, 8)
    d.t(WX + 14, y0 + 30, wcmd, 13, INK, MONO, "start", 600)
    d.t(WX + 14, y0 + 54, wsub, 12, MUTED, KR, "start")
    if rdash:
        d.o.append(f'<rect x="{RX}" y="{y0}" width="{RW}" height="{BH}" rx="8" fill="{PAPER2}" '
                   f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="5 4"/>')
    else:
        d.box(RX, y0, RW, BH, PAPER2, RULE, 1.0, 8)
    d.t(RX + 14, y0 + 30, rcmd, 13, INK, MONO, "start", 600)
    d.t(RX + 14, y0 + 54, rsub, 12, MUTED, KR, "start")
    for i in range(NC):
        x = CX0 + i * CSTEP
        if i < filled:
            d.o.append(f'<rect x="{x}" y="{y0 + 16}" width="{CWD}" height="40" rx="3" '
                       f'fill="{c}44" stroke="{c}" stroke-width="1.1"/>')
        else:
            d.box(x, y0 + 16, CWD, 40, PAPER2, RULE, 0.9, 3)
    d.t(480, y0 + 76, blabel, 12, c, KR, "middle", 600)


# 장면 1 — 다 읽음
Y1 = 136
scene(Y1, "장면 1 · 쓴 만큼 읽음", "printf 'a\\nb\\nc\\n'", "6바이트 쓰고 종료",
      "wc -l", "출력 3", 1, OK, "6바이트 통과")
d.arrow([(WX + WW + 2, Y1 + 36), (CX0 - 4, Y1 + 36)], OK, "ok", 1.4)
d.arrow([(CX0 + NC * CSTEP, Y1 + 36), (RX - 4, Y1 + 36)], OK, "ok", 1.4)

# 장면 2 — 버퍼 가득
Y2 = 264
scene(Y2, "장면 2 · 읽지 않는 상대", "dd if=/dev/zero bs=4096", "16+0 records out · 17번째 막힘",
      "sleep 1", "stdin 읽지 않음", 16, ACC, "16칸 가득 · 65,536 B")
d.arrow([(WX + WW + 2, Y2 + 36), (CX0 - 4, Y2 + 36)], ACC, "acc", 1.4)
d.line(CX0 + NC * CSTEP + 4, Y2 + 36, RX - 6, Y2 + 36, SOFT, 1.2, "4 4")

# 장면 3 — 읽는 쪽 먼저 종료
Y3 = 392
scene(Y3, "장면 3 · 읽는 쪽이 먼저 종료", "yes", "SIGPIPE 로 종료 · 상태 141",
      "head -1", "y 한 줄 읽고 종료 · 상태 0", 4, MUTED, "읽는 끝 닫힘", rdash=True)
d.arrow([(WX + WW + 2, Y3 + 36), (CX0 - 4, Y3 + 36)], MUTED, "ar", 1.4)
d.line(CX0 + NC * CSTEP + 4, Y3 + 36, RX - 6, Y3 + 36, SOFT, 1.2, "4 4")
d.path(f"M {RX + RW / 2} {Y3 + BH} L {RX + RW / 2} {Y3 + 100} L {WX + WW / 2} {Y3 + 100} "
       f"L {WX + WW / 2} {Y3 + BH + 3}", BAD, 1.4, m="bad")
d.chip(480, Y3 + 100, "SIGPIPE (13)", BAD, 12, 8)

d.legend(528, [("통과", OK), ("가득 찬 버퍼", ACC), ("커널이 보내는 시그널", BAD)])
d.save("03-01.pipeline.svg")
print("ok 03-01.pipeline")
