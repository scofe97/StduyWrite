# 08-02 §5 — 요청 크기를 조금씩 늘리며 ksize() 로 잰 낭비율. 본문 실측 여섯 점을 그대로 찍었다.
#   kmalloc(1638500)=2097152 27% · (1843300)=2097152 13% · (2048100)=2097152 2%
#   kmalloc(2252900)=4194304 86% · (2457700)=4194304 70% · (2662500)=4194304 57%
# 백분율은 본문 값(버림)을 그대로 쓴다. 2 MiB 경계에서 튀어 오르는 것이 이 그림의 논점이다.
# 타입 스펙: type-line — 시간이 아니라 요청 크기에 따른 연속 추세. 톱니의 수직 구간이 임계값이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 640
PX0, PX1, PY0, PY1 = 160, 920, 160, 440
VMIN, VMAX = 1_550_000, 2_750_000
TH = 2 * 1024 * 1024          # 2 MiB — 여기서 할당 단위가 4 MiB 로 올라간다

def px(v): return PX0 + (v - VMIN) / (VMAX - VMIN) * (PX1 - PX0)
def py(p): return PY1 - p / 100 * (PY1 - PY0)

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-02 §5",
       "임계값을 넘는 순간 낭비가 튑니다",
       "요청 크기를 조금씩 늘리며 ksize() 로 실제 할당량을 재면 톱니 모양이 나온다. 커널의 실제 크기에 가까워질수록 낭비가 0 으로 떨어지다가, 그 값을 넘는 순간 다음 크기로 점프해 낭비가 100% 가까이 치솟는다. 2,048,100 에서 2% 였던 것이 2,252,900 에서 86% 가 된다.",
       "본문 실측 여섯 점입니다 — 백분율은 원문 표기(버림)를 그대로 옮겼습니다")

# 눈금
for p in (0, 25, 50, 75, 100):
    y = py(p)
    d.line(PX0, y, PX1, y, RULE, 0.8)
    d.t(PX0 - 16, y + 5, f"{p}%", 12, SOFT, MONO, "end")
d.t(PX0 - 16, PY0 - 20, "낭비율", 13, SOFT, KR, "end")

for v, lab in ((1_600_000, "1.6M"), (1_800_000, "1.8M"), (2_000_000, "2.0M"),
               (2_200_000, "2.2M"), (2_400_000, "2.4M"), (2_600_000, "2.6M")):
    x = px(v)
    d.line(x, PY1, x, PY1 + 8, RULE, 1.0)
    d.t(x, PY1 + 26, lab, 12, SOFT, MONO)
d.t(PX1, PY1 + 48, "요청 바이트", 13, SOFT, KR, "end")

# 2 MiB 경계
d.line(px(TH), PY0 - 12, px(TH), PY1 + 8, ACC, 1.4, "5 5")
d.t(px(TH) + 10, PY0 - 20, "2 MiB — 여기서 할당 단위가 4 MiB 로 올라갑니다", 13, ACC, KR, "start")

LEFT = [(1_638_500, 27), (1_843_300, 13), (2_048_100, 2)]
RIGHT = [(2_252_900, 86), (2_457_700, 70), (2_662_500, 57)]

def polyline(pts, c):
    dd = " ".join(("M" if i == 0 else "L") + f" {px(v)} {py(p)}" for i, (v, p) in enumerate(pts))
    d.path(dd, c, 2.0)

polyline(LEFT + [(TH, 0)], OK)
polyline([(TH, 100)] + RIGHT, BAD)
d.line(px(TH), py(0), px(TH), py(100), BAD, 2.0)

for v, p in LEFT:
    d.o.append(f'<circle cx="{px(v)}" cy="{py(p)}" r="5" fill="{OK}"/>')
    d.t(px(v), py(p) - 16, f"{p}%", 12, OK, MONO)
for v, p in RIGHT:
    d.o.append(f'<circle cx="{px(v)}" cy="{py(p)}" r="5" fill="{BAD}"/>')
    d.t(px(v), py(p) - 16, f"{p}%", 12, BAD, MONO)

d.t(px(2_252_900) + 12, py(86) + 4, "2,252,900 → 86%", 13, BAD, KR, "start")

BOT = PY1 + 76
d.t(24, BOT, "받은 크기는 2,097,152(2 MiB) 아니면 4,194,304(4 MiB) 둘뿐입니다. 그 사이 값은 존재하지 않습니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 24, "ksize() 는 slab 포인터에만 동작합니다. 페이지 할당자 API 의 반환값에는 쓸 수 없습니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 48, "지름길은 하나입니다 — 1페이지 미만이면 slab, 1페이지를 넘으면 이 그래프가 적용됩니다.", 13, SOFT, KR, "start")

d.legend(H - 48, [("다음 임계값에 가까워지는 구간", OK), ("임계값을 넘긴 구간", BAD), ("2 MiB 경계", ACC)])
d.save("08-02.waste-sawtooth.svg")
print("ok 08-02.waste-sawtooth")
