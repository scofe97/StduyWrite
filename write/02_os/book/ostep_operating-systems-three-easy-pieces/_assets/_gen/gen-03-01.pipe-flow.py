# 03-01 「파이프」 — grep 의 표준 출력이 커널 안의 파이프에 쌓이고 wc 의 표준 입력이 그 파이프에서 읽는다.
# 본문 근거: 이 노트 「4. fork 와 exec 을 나눈 이유」 — 파이프.
# 값 근거: 개념 도식이라 값은 없다. 명령은 5장의 예 `grep -o foo file | wc -l` 이다.
# 공식 근거: OSTEP 5장 §5.4 — 한 프로세스의 출력을 커널 안의 파이프(큐)에 잇고 다른 프로세스의 입력을 같은 파이프에 잇는다. pipe(2) — 단방향 통로, pipefd[0] 은 읽는 끝, pipefd[1] 은 쓰는 끝, 데이터는 읽힐 때까지 커널이 버퍼에 쌓는다.
# 타입 스펙: type-data-flow — 데이터가 파일에서 grep, 파이프, wc, 화면으로 흐르는 길.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 920, 520
d = D(W, H, "OSTEP · 03-01 §4",
      "파이프는 앞 프로세스의 출력을 뒤 프로세스의 입력으로 잇는다",
      "grep 이 file 에서 foo 가 나온 자리를 뽑아 표준 출력에 쓰면 그 데이터가 커널 안의 파이프에 쌓이고, wc 가 표준 입력으로 파이프에서 읽어 줄 수를 세어 화면에 보인다. "
      "두 프로세스는 파이프로만 이어지며 서로의 코드를 모른다.",
      lead="명령: grep -o foo file | wc -l")

BW, BH, YM = 220, 76, 220
# 입력 파일
d.box(40, 118, BW, 48, PAPER2, RULE, 1.0)
d.t(40 + BW / 2, 148, "file", 13, INK, MONO, "middle", 600)
d.arrow([(40 + BW / 2, 168), (40 + BW / 2, YM - 2)], MUTED, "ar", 1.4)
d.t(40 + BW / 2 + 12, 196, "읽어 들임", 11, MUTED, KR, "start")

# grep
d.tone(40, YM, BW, BH, INFO, 6, "14", 1.2)
d.t(40 + BW / 2, YM + 32, "grep -o foo", 13, INFO, MONO, "middle", 600)
d.t(40 + BW / 2, YM + 56, "표준 출력(1번)에 씀", 12, MUTED, KR)

# 파이프
PX = 350
d.tone(PX, YM - 10, 220, BH + 20, ACC, 6, "14", 1.4)
d.t(PX + 110, YM + 26, "파이프", 14, ACC, KR, "middle", 600)
d.t(PX + 110, YM + 48, "커널이 쌓아 둔 버퍼", 12, MUTED, KR)
d.t(PX + 110, YM + 68, "읽힐 때까지 보관", 12, MUTED, KR)

# wc
WX = 660
d.tone(WX, YM, BW, BH, INFO, 6, "14", 1.2)
d.t(WX + BW / 2, YM + 32, "wc -l", 13, INFO, MONO, "middle", 600)
d.t(WX + BW / 2, YM + 56, "표준 입력(0번)에서 읽음", 12, MUTED, KR)

ya = YM + BH / 2
d.arrow([(40 + BW + 2, ya), (PX - 4, ya)], ACC, "acc", 1.6)
d.t((40 + BW + PX) / 2, ya - 9, "쓰기", 12, ACC, KR, "middle", 600)
d.arrow([(PX + 220 + 2, ya), (WX - 4, ya)], ACC, "acc", 1.6)
d.t((PX + 220 + WX) / 2, ya - 9, "읽기", 12, ACC, KR, "middle", 600)

# 결과
d.box(WX, 360, BW, 48, PAPER2, RULE, 1.0)
d.t(WX + BW / 2, 390, "화면: foo 가 나온 횟수", 12, INK, KR, "middle", 600)
d.arrow([(WX + BW / 2, YM + BH + 2), (WX + BW / 2, 358)], OK, "ok", 1.4)
d.t(WX + BW / 2 + 12, 340, "세어서 출력", 11, MUTED, KR, "start")

d.legend(H - 40, [("프로세스", INFO), ("커널의 파이프", ACC), ("결과", OK)])
d.save("03-01.pipe-flow.svg")
print("ok 03-01 pipe-flow")
