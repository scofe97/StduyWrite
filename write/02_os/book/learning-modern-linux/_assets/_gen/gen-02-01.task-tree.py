# 02-01 §3 — 세션에서 태스크까지, 다섯 이름이 한 구조체에 닻을 내린다.
# 원문("Process Management"): 리눅스는 Sessions(SID, "Contain one or more process groups"),
#       Process groups(PGID, "Contain one or more processes, with at most one process group in a session
#       as the foreground process group"), Processes(PID, "/proc/self for the current process"),
#       Threads(TID·TGID, "Implemented by the kernel as processes. That is, there are no dedicated data
#       structures representing threads"), Tasks(task_struct, sched.h)를 갖는다. 태스크에 대해 저자는
#       "all of the aforementioned units are derived and/or anchored in tasks; however, tasks are not
#       exposed as such outside of the kernel" 이라 적는다.
#       실증은 `ps -j` 출력이다 — bash 가 PID·PGID·SID 6756, ps 가 PID·PGID 6790 에 SID 6756.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 포함 관계. 직교 연결(대각선 금지).
#           accent 는 커널 밖으로 드러나지 않는 뿌리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §3",
      "세션에서 태스크까지, 이름 다섯이 한 구조체로 모인다",
      "원서가 큰 단위에서 작은 단위로 늘어놓은 다섯을 포함 관계로 세운 것. 왼쪽 넷은 사용자가 번호로 "
      "볼 수 있고, 오른쪽 하나는 커널 안에만 있다.",
      "ps -j 로 세션 · 그룹 · 프로세스의 번호를 한 화면에서 볼 수 있습니다")

NX, NW, NH, STRIDE = 60, 300, 68, 88
chain = [
    ("세션", "SID 6756", "프로세스 그룹 하나 이상을 담는다"),
    ("프로세스 그룹", "PGID 6756", "한 세션에 포그라운드는 최대 하나"),
    ("프로세스", "PID 6756 · bash", "주소 공간 · 스레드 · 소켓을 묶는다"),
    ("스레드", "TID · TGID", "커널은 프로세스로 구현한다"),
]

Y0 = 116
for i, (name, code, note) in enumerate(chain):
    y = Y0 + i * STRIDE
    d.box(NX, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(NX + 18, y + 26, name, 15, INK, KR, "start", 600)
    d.t(NX + 18, y + 46, code, 12, INFO, MONO, "start", 600)
    d.t(NX + 18, y + 62, note, 12, MUTED, KR, "start")
    if i < len(chain) - 1:
        d.arrow([(NX + NW / 2, y + NH), (NX + NW / 2, y + STRIDE - 2)], MUTED, "ar", 1.2)

TX, TW = 464, 356
TY, TH = 116, 3 * STRIDE + NH
d.o.append(f'<rect x="{TX}" y="{TY}" width="{TW}" height="{TH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(TX + TW / 2, TY + 36, "태스크", 17, ACC, KR, "middle", 600)
d.t(TX + TW / 2, TY + 58, "task_struct — sched.h", 12, ACC, MONO)
for k, line in enumerate([
        "스케줄링 정보 · 식별자(PID · TGID) · 시그널 핸들러를 담는다",
        "성능과 보안에 관한 정보도 여기에 붙는다",
        "왼쪽 넷은 모두 여기서 파생되거나 여기에 닻을 내린다",
        "그러나 태스크 자체는 커널 밖으로 드러나지 않는다"]):
    d.t(TX + 20, TY + 96 + k * 26, line, 12, MUTED if k < 3 else ACC, KR, "start",
        600 if k == 3 else 400)

for i in range(len(chain)):
    y = Y0 + i * STRIDE + NH / 2
    d.path(f"M {NX + NW + 8} {y} L {TX - 10} {y}", ACC, 1.0, m="acc", dash="5 5")

for _k, _line in enumerate([
        "저자는 스레드를 표현하는 전용 자료구조가 없다고 적습니다.",
        "스레드는 메모리나 시그널 핸들러 같은 자원을 다른 프로세스와 공유하는 프로세스입니다.",
        "TGID 값이 같으면 그것이 멀티스레드 프로세스라는 뜻입니다."]):
    d.t(NX, 468 + _k * 22, _line, 12, MUTED if _k < 2 else SOFT, KR, "start")

d.legend(548, [("사용자가 번호로 보는 것", INFO), ("커널 안에만 있는 것", ACC)])
d.save("02-01.task-tree.svg")
print("ok 02-01.task-tree")
