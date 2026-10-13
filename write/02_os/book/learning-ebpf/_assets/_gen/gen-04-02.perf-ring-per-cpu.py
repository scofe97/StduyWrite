# 타입 스펙: type-architecture — CPU 넷 줄마다 [CPU → output 맵 칸 → perf 링 fd]를 한 줄로 두고, 네 링을 ppoll 한 호출이 한꺼번에 감시한다.
# 사실 출처: 추출본 ebpf4.txt 714~780행(perf_event_open … -1, X, -1 = Y · X 는 0~3, Y 는 8~11 · BPF_MAP_UPDATE_ELEM map_fd=4 · ppoll([{fd=8…}…{fd=11…}], 4, …) = 1 ([{fd=8, revents=POLLIN}])),
#   BCC v0.37.0 src/python/bcc/table.py 986·1016행(online CPU 마다 링을 열고 Key(cpu) = Leaf(fd)), src/cc/export/helpers.h 207~214행(perf_submit 은 CUR_CPU_IDENTIFIER),
#   linux v7.2 include/uapi/linux/bpf.h 2487~2500행(bpf_perf_event_output 의 flags 와 BPF_F_CURRENT_CPU).
# Layout conventions: 노드 높이 64, 줄 stride 92(y=148·240·332·424), 열 x=24·244·524·784(폭 140·200·180·156), 열 간격 80, 존 둘(커널 · 사용자). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 600
d = D(W, H, "LEARNING EBPF · 04-02 §2",
      "CPU 넷에 링 넷, ppoll 하나가 네 fd 를 본다",
      "output 맵은 CPU 번호를 키로 하고 값은 그 CPU 의 perf 링 fd 다. hello() 가 도는 CPU 의 칸을 따라 그 CPU 의 링에 쓰고, 사용자 공간의 ppoll 이 네 fd 를 함께 기다린다.",
      "깨어나는 링 하나")

KZ = (16, 84, 696, 424)
UZ = (772, 84, 172, 424)
for (x, y, w, h), name in ((KZ, "KERNEL"), (UZ, "USER SPACE")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 9, SOFT, MONO, "start")

COLS = (24, 244, 524)
CW = (140, 200, 180)
ROWS = (148, 240, 332, 424)
NH = 64

for x, w, txt in ((COLS[0], CW[0], "CPU"), (COLS[1], CW[1], "output 맵 · map_fd=4"),
                  (COLS[2], CW[2], "perf_event_open × 4"), (784, 156, "대기 호출")):
    d.t(x, 136, txt, 13, MUTED, KR if any("가" <= c <= "힣" for c in txt) else MONO, "start", 600)


def node(x, y, w, title, sub, c, op="12"):
    d.tone(x, y, w, NH, c, 6, op, 1.2)
    d.t(x + w / 2, y + 28, title, 14, c, MONO, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


# 화살표를 먼저 그려 노드 뒤로 보낸다
for k, y in enumerate(ROWS):
    c = ACC if k == 0 else MUTED
    mk = "acc" if k == 0 else "ar"
    yc = y + 32
    d.arrow([(COLS[0] + CW[0] + 2, yc), (COLS[1] - 6, yc)], MUTED, "ar", 1.5)
    d.arrow([(COLS[1] + CW[1] + 2, yc), (COLS[2] - 6, yc)], MUTED, "ar", 1.5)
    d.arrow([(COLS[2] + CW[2] + 2, yc), (784 - 6, yc)], c, mk, 1.8 if k == 0 else 1.4)

for k, y in enumerate(ROWS):
    node(COLS[0], y, CW[0], f"CPU {k}", "perf_submit", MUTED)
    node(COLS[1], y, CW[1], f"output[{k}]", f"= fd {8 + k}", INFO)
    node(COLS[2], y, CW[2], f"perf 링 fd {8 + k}", f"CPU {k} 전용", ACC if k == 0 else OK)

# ppoll — 네 줄을 가로지르는 키 큰 노드
PX, PY, PW, PH = 784, 148, 156, 340
d.tone(PX, PY, PW, PH, OK, 6, "12", 1.2)
d.t(PX + PW / 2, PY + 120, "ppoll", 14, OK, MONO, "middle", 600)
d.t(PX + PW / 2, PY + 144, "fd 8·9·10·11", 12, MUTED, MONO)
d.t(PX + PW / 2, PY + 176, "= 1 · revents", 12, ACC, MONO)
d.t(PX + PW / 2, PY + 196, "fd 8 만 POLLIN", 12, ACC, MONO)

d.legend(H - 56, [("CPU", MUTED), ("output 맵 칸", INFO), ("perf 링 fd", OK), ("깨어난 링", ACC)])
d.save("04-02.perf-ring-per-cpu.svg")
