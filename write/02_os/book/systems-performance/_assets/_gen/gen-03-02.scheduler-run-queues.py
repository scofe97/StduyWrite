# 03-02 §2 — 우선순위 런큐에 몰린 ready 스레드 다섯과 CPU 둘. 계산 비율이 높은 스레드는 낮은 큐 뒤로 밀린다.
# 타입 스펙: type-data-flow — semantic-patterns 「Fan-in queue / bottleneck」: 여럿이 한정된 CPU 로 몰려
#           큐에 쌓이는 장면이다. 원시요소(큐 칸 · 개수 · 용량 라벨 · 서비스 지점 · 두 결과)를 따른다.
#           축약: 역할 레인이 없어 §1 lanes · §2 공식 대신 큐 행 stride 80 · 칸 폭 104 로 놓는다.
#           셸 · 웹 워커 · 계산 A~C 는 원서 3.2.9 의 I/O-bound · CPU-bound 예를 이름 붙인 가상 장면이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 560
QX, SW, SG, Y0, ST, SH = 184, 96, 8, 176, 80, 44
CX, CWD, CH = 664, 216, 56

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02 §2",
       "우선순위 런큐와 CPU — 계산 비율이 높은 스레드가 뒤로 밀린다",
       "ready 스레드 다섯이 CPU 둘을 다툰다. 타임슬라이스를 다 쓴 계산 작업은 계산 비율이 높아 낮은 큐 뒤로 가고, I/O 에서 깨어난 셸은 높은 큐에서 먼저 CPU 를 얻는다.",
       "ready 5 · CPU 2 · 런큐 대기 3")

def slot(x, y, txt, c=None, dash=False):
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="4" fill="none" stroke="{c or SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
    elif c: d.tone(x, y, SW, SH, c, 4)
    else: d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 4)
    if txt: d.t(x + SW / 2, y + 27, txt, 13, c if c else INK, KR, "middle", 600 if c else 400)

ROWQ = [("높음", [None, None, ("셸", ACC)]),
        ("보통", [None, None, None]),
        ("낮음", [("계산 A", WARN, True), ("계산 C", None), ("계산 B", None)])]
for r, (lab, cells) in enumerate(ROWQ):
    y = Y0 + r * ST
    d.t(QX - 20, y + 27, f"{lab} 큐", 13, SOFT, KR, "end", 600)
    for i, cell in enumerate(cells):
        x = QX + i * (SW + SG)
        if cell is None: slot(x, y, "", SOFT, True)
        elif len(cell) == 3: slot(x, y, cell[0], cell[1], True)
        else: slot(x, y, cell[0], cell[1])
QE = QX + 3 * (SW + SG) - SG
d.t(QX, Y0 - 24, "꼬리", 12, SOFT, KR, "start")
d.t(QE, Y0 - 24, "머리", 12, SOFT, KR, "end")

# CPU 둘
d.t(CX + CWD / 2, Y0 - 24, "CPU 2개", 13, INFO, KR, "middle", 600)
for k, (name, sub, row) in enumerate((("CPU 1", "셸 실행", 0), ("CPU 0", "웹 워커 실행 중", 1))):
    y = Y0 + row * ST - (CH - SH) / 2
    d.tone(CX, y, CWD, CH, INFO, 8)
    d.t(CX + 20, y + 24, name, 14, INFO, MONO, "start", 600)
    d.t(CX + 20, y + 44, sub, 13, MUTED, KR, "start")

# 셸 → CPU 1 (먼저 배정)
cy0 = Y0 + SH / 2
d.arrow([(QE + 4, cy0), (CX - 6, cy0)], ACC, "acc", 1.7)
d.t((QE + CX) / 2, cy0 - 10, "먼저 배정", 13, ACC, KR, "middle", 600)

# CPU 1 의 계산 A → 낮은 큐 꼬리 (타임슬라이스 만료)
y1 = Y0 - (CH - SH) / 2
gx = CX + CWD + 24
by = Y0 + 2 * ST + SH + 40
ty = Y0 + 2 * ST + SH
d.arrow([(CX + CWD, y1 + CH / 2), (gx, y1 + CH / 2), (gx, by), (QX + SW / 2, by), (QX + SW / 2, ty + 4)], WARN, "warn", 1.5)
d.t((QX + gx) / 2, by + 20, "계산 A · 타임슬라이스 만료 · 계산 비율 높음 → 낮은 큐 꼬리", 13, WARN, KR, "middle", 600)

d.legend(by + 44, [("먼저 CPU 를 얻는 I/O-bound", ACC), ("계산 비율이 높아 밀림", WARN), ("서비스 지점", INFO)])
d.save("03-02.scheduler-run-queues.svg")
