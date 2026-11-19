# 06-01 §3 「순차 발급과 300번 재탐색」 — PID 카운터는 오른쪽으로 증가하다 pid_max 에 닿으면 1 이 아니라 300 으로 되돌아간다.
# 본문 근거: 이 노트 「3. PID 의 순환 할당과 상한선」.
# 값 근거: 300·32,768 은 TLPI 6.2 와 커널 RESERVED_PIDS·pid_max 기본값. 막대 너비는 비례하지 않는다.
# 공식 근거: TLPI 6.2 — 카운터가 상한에 닿으면 1 이 아니라 300 으로 되돌린다. 낮은 번호는 시스템 프로세스와 데몬이 계속 쓰기 때문이다.
#           proc_sys_kernel(5) — pid_max 는 PID 가 되감기는 값이고 최대 PID 보다 1 크다.
#           kernel/pid.c v7.3 — "after reaching the maximum wrap back to RESERVED_PIDS".
# 타입 스펙: type-gantt — 구간 막대로 번호 범위를 보이고, 되돌아가는 길을 직각 화살표로 잇는다. 막대 길이는 구간 이름을 읽기 위한 것이다.
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, INK, MUTED, WARN, OK, BAD, INFO, KR, MONO

W, H = 960, 408
d = D(W, H, "TLPI · 06-01 §3",
      "PID 카운터는 pid_max 에 닿으면 300 으로 되돌아간다",
      "카운터는 새 프로세스마다 오른쪽으로 늘고, 상한에 닿으면 1~299 를 건너뛰고 300 부터 빈 번호를 다시 찾는다.",
      "pid_max 기본값 32,768 기준 번호 구간 세 개와 되돌아가는 길")

BY, BH = 152, 84
segs = [(40, 220, WARN, "1~299", "첫 바퀴에서만 발급"),
        (260, 560, OK, "300 ~ 32,767", "순서대로 발급 · 사용 중인 번호는 건너뜀"),
        (820, 100, BAD, "32,768", "pid_max")]
for x, w, c, t1, t2 in segs:
    d.tone(x, BY, w, BH, c, 6, "18", 1.2)
    d.t(x + w / 2, BY + 32, t1, 15, INK, MONO, "middle", 600)
    d.t(x + w / 2, BY + 56, t2, 12, MUTED, KR if c != BAD else MONO)
d.t(870, BY + 74, "발급 안 됨", 12, MUTED, KR)

# 위: 카운터의 진행 방향
d.arrow([(272, 126), (808, 126)], INFO, "info", 1.4)
d.t(540, 114, "새 프로세스마다 카운터 증가", 13, INFO, KR)

# 아래: 상한에서 300 으로 되돌아가는 길
d.path(f"M 870 {BY + BH + 6} V 300 Q 870 312 858 312 H 296 Q 284 312 284 300 V {BY + BH + 8}", ACC, 1.6, m="acc")
d.chip(570, 312, "상한 도달 → 300 부터 다시 탐색", ACC, 13)

d.legend(H - 52, [("먼저 쓰이는 낮은 번호", WARN), ("순차 발급 구간", OK), ("pid_max", BAD), ("카운터 증가", INFO), ("되돌아가는 길", ACC)])
d.save("06-01.pid-allocation-loop.svg")
print("ok 06-01 pid-allocation-loop")
