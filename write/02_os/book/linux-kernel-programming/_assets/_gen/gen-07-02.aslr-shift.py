# 07-02 §4 — 같은 프로그램을 두 번 돌리면 같은 세그먼트가 다른 주소에 놓인다.
# 세로 눈금은 상대 위치다 — 절대값은 매 실행 랜덤이라는 것이 이 그림의 논점이라 수치를 적지 않는다.
# 타입 스펙: type-line — 두 시점 사이의 변화(slopegraph). 선의 기울기가 곧 그 실행에서의 이동량이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 620
X1, X2 = 340, 660
AX = 260

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-02 §4",
       "실행할 때마다 배치가 달라집니다",
       "ASLR 이 켜지면 유저 VAS 의 절대 맵이 매 실행 달라진다. 같은 세그먼트가 실행 1 과 실행 2 에서 다른 주소에 놓이고, 이동량은 세그먼트마다 따로 뽑힌 랜덤 페이지 정렬 오프셋이다. heap 만 randomize_va_space 가 2 여야 움직인다.",
       "세로 눈금은 상대 위치입니다 — 절대 주소는 매 실행 달라지므로 적지 않았습니다")

# (이름, 실행1 y, 실행2 y, 색) — y 는 상대 위치이며 값 자체에 의미를 두지 않는다.
ITEMS = [
    ("stack", 192, 216, OK),
    ("vDSO 페이지", 248, 236, OK),
    ("공유 라이브러리", 304, 332, OK),
    ("mmap 기반 할당", 360, 380, OK),
    ("heap", 444, 416, ACC),
]

d.t(X1, 152, "실행 1", 13, INK, KR, "middle", 600)
d.t(X2, 152, "실행 2", 13, INK, KR, "middle", 600)
d.line(X1, 164, X1, 472, RULE, 0.8, "3 6")
d.line(X2, 164, X2, 472, RULE, 0.8, "3 6")

d.arrow([(AX, 456), (AX, 176)], SOFT, "soft", 1.2)
d.t(AX - 12, 184, "높은", 13, SOFT, KR, "end")
d.t(AX - 12, 204, "주소", 13, SOFT, KR, "end")

for name, y1, y2, c in ITEMS:
    d.line(X1, y1, X2, y2, c, 1.6)
    d.o.append(f'<circle cx="{X1}" cy="{y1}" r="5" fill="{c}"/>')
    d.o.append(f'<circle cx="{X2}" cy="{y2}" r="5" fill="{c}"/>')
    d.t(X1 - 20, y1 + 5, name, 13, c, KR, "end", 600)

d.t(X1 - 20, ITEMS[-1][1] + 26, "값 2 에서만 움직입니다", 13, ACC, KR, "end")
d.t(X2 + 24, 300, "선의 기울기가", 13, MUTED, KR, "start")
d.t(X2 + 24, 322, "그 실행에서 뽑힌", 13, MUTED, KR, "start")
d.t(X2 + 24, 344, "랜덤 오프셋입니다", 13, MUTED, KR, "start")
d.t(X2 + 24, 372, "세그먼트마다", 13, SOFT, KR, "start")
d.t(X2 + 24, 394, "따로 뽑습니다", 13, SOFT, KR, "start")

BOT = 496
d.t(24, BOT, "sysctl 은 /proc/sys/kernel/randomize_va_space 입니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 24, "0 은 끔, 1 은 mmap·stack·vDSO·공유 라이브러리, 2 는 거기에 heap 까지 랜덤화합니다(기본값).", 13, MUTED, KR, "start")
d.t(24, BOT + 48, "랜덤화 비트가 많지 않아 엔트로피가 낮습니다 — 통계적 방어일 뿐입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("값 1 부터 랜덤화", OK), ("heap — 값 2 에서만", ACC)])
d.save("07-02.aslr-shift.svg")
print("ok 07-02.aslr-shift")
