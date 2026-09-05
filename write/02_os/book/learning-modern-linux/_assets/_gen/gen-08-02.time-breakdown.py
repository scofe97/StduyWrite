# 08-02 §3 — time 이 내놓는 세 값이 무엇을 담는가.
# 원문("Monitoring"): `time (ls -R /etc 2&> /dev/null)` 출력이 real 0m0.022s · user 0m0.012s ·
#       sys 0m0.007s 이고, 주석은 real("The total (wall clock) time it took"),
#       user("How long ls itself spent on-CPU (user space)"),
#       sys("How long ls was waiting for Linux to do something (kernel space)") 다.
#       이어서 "taking the sum of user and sys is a good approximation, and the ratio of the two gives
#       you a good idea where it spends most of the execution time" 라고 적는다.
# 1차 자료(GNU time(1)): "S  Total number of CPU-seconds used by the system on behalf of the process
#       (in kernel mode), in seconds." / "U  Total number of CPU-seconds that the process used directly
#       (in user mode), in seconds."
# 주의: 안쪽 세 칸의 폭은 원문 수치에 정비례한다. real 이 user+sys 를 담는 그림은 단일 스레드 프로세스일
#       때만 성립하며, 스레드가 여럿이면 real 이 user+sys 보다 작아질 수 있다. 그 조건을 그림에 적었다.
# 타입 스펙: type-nested — 포함 관계로 드러나는 계층. 경과 시간이라는 바깥 상자 안에 CPU 시간 두 조각과
#           CPU 를 안 쓴 나머지가 들어간다. 축약: 세 값의 시간 순서는 그리지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 474
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §3",
      "real 안에 CPU 시간 둘과 CPU 를 안 쓴 나머지가 있다",
      "원서의 time 출력 세 값을 크기에 비례해 담은 것. 안쪽 두 칸이 CPU 시간이고 마지막 칸이 CPU 를 "
      "쓰지 않은 시간이다. 순서가 아니라 양을 나타낸다.",
      "저자는 sys 를 기다린 시간이라 적지만 그것도 CPU 를 쓴 시간입니다")

OX, OY, OW, OH = 24, 132, 832, 172
d.box(OX, OY, OW, OH, PAPER2, INFO, 1.3, 10)
d.t(OX + 20, OY + 28, "real 0m0.022s — 벽시계로 잰 경과 시간", 15, INFO, KR, "start", 600)
d.t(OX + 20, OY + 50, "저자는 성능 말고는 그리 쓸모 있지 않다고 적는다", 11.5, MUTED, KR, "start")

IY, IH = OY + 66, 88
TOTAL = 0.022
segs = [("user", 0.012, "사용자 공간에서 쓴 CPU 시간", OK, False),
        ("sys", 0.007, "커널이 이 프로세스를 위해 쓴 CPU 시간", ACC, True),
        ("나머지", 0.003, "유도값", SOFT, False)]
x = OX + 16
for name, val, note, col, focal in segs:
    w = (OW - 32) * val / TOTAL - 8
    if focal:
        d.tone(x, IY, w, IH, ACC, 6, "12", 1.4)
    else:
        d.box(x, IY, w, IH, PAPER, col, 1.2, 6)
    d.t(x + 14, IY + 26, name, 14, col, MONO, "start", 600)
    d.t(x + 14, IY + 48, f"0m{val:.3f}s", 12.5, INK, MONO, "start")
    d.t(x + 14, IY + 70, note, 11, MUTED, KR, "start")
    x += w + 8

NY = OY + OH + 30
d.t(24, NY, "저자는 sys 를 \"리눅스가 무언가 해 주기를 기다린 시간\" 이라고 적습니다. 그런데 기다림은 "
            "CPU 시간을 쓰지 않습니다.", 12, INK, KR, "start", 600)
d.t(24, NY + 24, "GNU time(1) 은 sys 를 커널 모드에서 프로세스를 대신해 쓴 CPU 초라고 정의합니다. "
                 "기다림은 오른쪽 마지막 칸에 있습니다.", 12, MUTED, KR, "start")
d.t(24, NY + 48, "저자 자신의 다음 문장도 그쪽입니다. user 와 sys 의 합이 걸린 시간의 좋은 근사라고 "
                 "적는데, 둘 다 CPU 시간이라야 합이 뜻을 갖습니다.", 12, MUTED, KR, "start")
d.t(24, NY + 76, "이 포함 관계는 단일 스레드 프로세스일 때만 성립합니다. 스레드가 여럿이면 user 와 sys 의 "
                 "합이 real 을 넘을 수 있습니다.", 12, SOFT, KR, "start")

d.legend(434, [("원문 서술이 어긋난 칸", ACC), ("경과 시간", INFO),
                  ("사용자 공간 CPU 시간", OK), ("real 에서 뺀 유도값", SOFT)])
d.save("08-02.time-breakdown.svg")
print("ok 08-02.time-breakdown")
