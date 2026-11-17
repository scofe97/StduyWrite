# 08-02 §1 — 관측된 증상 하나를 자원 범주로 나누고, 범주마다 여는 창(명령)과 그 창이 이 노트에서
#           실제로 보여 준 값을 가지 끝에 붙인다.
# 원문("Observability Strategy"): "let's say an application is slow. Let's further assume there are
#       multiple possible reasons for this (not enough memory, too few CPU cycles, network I/O
#       insufficient, etc.)."
# 원문("Monitoring"): "The two types of activities you'll carry out most often in the context of
#       monitoring are as follows: Tracking one or more metrics (over time) · Alerting on a condition"
# 주의: 원문이 이름 붙인 원인은 셋(메모리 · CPU 사이클 · 네트워크 I/O)이고 나머지는 "etc." 로 열어 두었다.
#       본문이 "도식의 뼈대도 셋" 이라고 말하므로 디스크 I/O 는 뼈대로 그리지 않고 바닥 한 줄로만 적는다.
#       accent 를 메모리에 건 것은 저자가 그 가설을 먼저 시험하기 때문이고("Does the performance improve
#       after you provided more RAM to the app?"), 확정된 근본 원인이라는 뜻이 아니다.
# 근거(값): 가지마다 둘째 줄은 본문 출력의 실측값이다.
#       vmstat 1 3 의 si·so 0·0, r 2 (§2 「vmstat 한 줄의 여섯 축」) · uptime 1.37 과 nproc 8 (§2) ·
#       /dev/shm 400MiB 실험의 available 5977 → 5574 MiB (§2 「used·shared 에 섞이는 tmpfs」) ·
#       ss -atnp 의 Recv-Q 5000 과 LISTEN :8000 의 users:(("nc",pid=3798,...)) (§4 「ss 의 소켓 큐」).
#       si·so 0 과 r 2/8 은 정상 상태의 값이다. 원인이 있을 때의 값이 아니라 그 창이 보여 주는 칸을 가리킨다.
# 타입 스펙: type-fishbone — 관측된 결과 하나의 원인을 범주로 묶는다. 60도 뼈대와 가지 눈금은 이 타입의
#           문법이라 직교 연결 규칙에서 면제된다. 축약: 범주당 하위 원인은 둘로 제한했고,
#           하위 원인 한 줄 아래에 그 원인을 보는 명령과 실측값을 mono 로 한 줄 둔다.
#           두 줄이 범주 태그 상자를 덮지 않게 뼈대를 길게(dy 168) 잡았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, KR, MONO

W, H = 880, 584
CY, HEAD = 300, 680
DY, SLOPE = 168, 96 / 168          # 뼈대 세로 길이와 기울기(dx/dy, 60도)
TICKS = (48, 104)                  # 가지 눈금의 세로 위치
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §1",
      "느리다는 증상 하나가 세 범주로 갈린다",
      "느린 앱의 원인 후보를 메모리·CPU·네트워크 I/O 세 범주로 묶고, 하위 원인마다 그것을 보는 명령과 "
      "이 노트의 컨테이너에서 그 명령이 보여 준 값을 붙인 것. 메모리는 vmstat si·so 0·0 과 "
      "free available 5977 → 5574 MiB, CPU 는 vmstat r 2 와 uptime 1.37 (CPU 8), 네트워크는 "
      "ss Recv-Q 5000 과 포트 8000 을 쥔 nc pid 3798. 디스크 I/O 는 저자의 '등등' 자리에 들어가며 §4 iostat 가 연다.",
      "먼저 시험하는 가설은 메모리입니다")

d.line(40, CY, HEAD - 6, CY, INK, 1.4)
d.o.append(f'<path d="M {HEAD - 14} {CY} L {HEAD - 4} {CY}" fill="none" stroke="{INK}" '
           f'stroke-width="1.4" marker-end="url(#acc)"/>')
EW, EH = 168, 84
d.o.append(f'<rect x="{HEAD}" y="{CY - EH / 2}" width="{EW}" height="{EH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HEAD + EW / 2, CY - 12, "앱이 느리다", 15, ACC, KR, "middle", 600)
d.t(HEAD + EW / 2, CY + 16, "관측된 증상", 12, ACC, KR)

BONES = [
    ("메모리 · §2", ACC, True, [("스왑 입출력", "vmstat si·so  0·0"),
                               ("available 감소", "free  5977 → 5574 MiB")]),
    ("CPU · §2", INFO, False, [("실행 대기", "vmstat r  2 / CPU 8"),
                              ("부하 평균 상승", "uptime  1.37 / nproc 8")]),
    ("네트워크 I/O · §4", INFO, False, [("소켓 큐 적체", "ss Recv-Q  5000"),
                                    ("포트를 쥔 프로세스", "ss -p  nc pid=3798")]),
]
TW, TH = 152, 32
for k, (name, col, focal, subs) in enumerate(BONES, start=1):
    above = (k % 2 == 1)
    sgn = -1 if above else 1
    ax = HEAD - 112 - k * 112
    fx, fy = ax - SLOPE * DY, CY + sgn * DY
    d.line(ax, CY, ax - SLOPE * (DY - TH / 2), CY + sgn * (DY - TH / 2), col, 1.6 if focal else 1.1)
    if focal:
        d.tone(fx - TW / 2, fy - TH / 2, TW, TH, ACC, 4, "12", 1.4)
    else:
        d.box(fx - TW / 2, fy - TH / 2, TW, TH, PAPER2, col, 1.1, 4)
    d.t(fx, fy + 5, name, 12.5, col, KR, "middle", 600)
    for (label, value), dy in zip(subs, TICKS):
        tx, ty = ax - SLOPE * dy, CY + sgn * dy
        d.line(tx, ty, tx - 22, ty, SOFT, 1.0)
        y1, y2 = (ty - 22, ty - 6) if above else (ty + 16, ty + 32)
        d.t(tx - 28, y1, label, 12, INK, KR, "end")
        d.t(tx - 28, y2, value, 11.5, MUTED, MONO, "end")

d.t(40, 520, "둘째 줄 = 이 노트 컨테이너의 실측값(정상 상태 값 포함) · 디스크 I/O 는 '등등' 자리 → §4 iostat",
    11, SOFT, KR, "start")
d.legend(H - 44, [("증상과 먼저 시험할 가설", ACC), ("자원 범주", INFO), ("하위 원인", INK),
                  ("명령과 실측값", MUTED)])
d.save("08-02.slow-app-causes.svg")
print("ok 08-02.slow-app-causes")
