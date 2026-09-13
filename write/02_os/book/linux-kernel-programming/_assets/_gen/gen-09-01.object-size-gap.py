# 09-01 §4 — 세 API 가 모두 328 이라 답해도 커널이 실제로 뗀 것은 448 이다.
# 본문 수치를 그대로 옮겼다 — object_size 328 · slab_size 448 · 객체당 120바이트(약 27%) 낭비.
# 타입 스펙: type-bar — 범주별 수치 비교. 두 막대의 차이가 곧 어디서도 안 보이는 낭비다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 624
LX, LW = 24, 240
AX, AXW = 280, 620
MAXB = 448

def px(b): return AX + b / MAXB * AXW

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-01 §4",
       "묻는 API 마다 328 이라 답합니다",
       "328바이트 구조로 전용 캐시를 만들면 sizeof·kmem_cache_size·ksize 가 모두 328 을 돌려준다. 그런데 커널이 실제로 뗀 것은 448바이트다. 객체마다 120바이트, 약 27% 가 어디에도 안 보이는 자리에서 사라진다. 정확한 값은 sysfs 의 slab_size 에만 있다.",
       "막대 길이가 곧 바이트입니다 — 세 API 는 위 막대까지만 압니다")

ROWS = [
    ("sizeof(struct)", 328, "328 B", INFO, "컴파일 시점의 구조 크기"),
    ("kmem_cache_size()", 328, "328 B", INFO, "캐시에 등록한 객체 크기"),
    ("ksize()", 328, "328 B", INFO, "slab 포인터로 물어본 크기"),
    ("slab_size (sysfs)", 448, "448 B", ACC, "커널이 실제로 뗀 크기"),
]

Y0, RH, RS = 152, 40, 64
for i, (name, val, lab, c, note) in enumerate(ROWS):
    y = Y0 + i * RS
    d.t(LX, y + 16, name, 13, c, MONO, "start", 600)
    d.t(LX, y + 36, note, 12, SOFT, KR, "start")
    focal = c is ACC
    d.tone(AX, y, px(val) - AX, RH, c, 4, "22" if focal else "18", 1.4 if focal else 1.1)
    d.t(AX + 16, y + 25, lab, 13, c, MONO, "start", 600)

# 328 과 448 사이 — 아무 API 도 말해 주지 않는 구간
GY = Y0 + 3 * RS
d.line(px(328), Y0, px(328), GY + RH + 16, ACC, 1.2, "4 4")
d.tone(px(328), GY, px(448) - px(328), RH, WARN, 4, "22", 1.4)
d.t((px(328) + px(448)) / 2, GY + 25, "120 B · 27%", 13, WARN, MONO)
d.t(px(328) - 12, GY + RH + 38, "세 API 가 아는 것은 여기까지입니다", 13, ACC, KR, "end")

TY = GY + RH + 64
d.line(AX, TY, AX + AXW, TY, RULE, 1.0)
for b in (0, 128, 256, 384, 448):
    x = px(b)
    d.line(x, TY, x, TY + 8, RULE, 1.0)
    d.t(x, TY + 26, f"{b}", 12, SOFT, MONO)
d.t(AX - 16, TY + 26, "바이트", 13, SOFT, KR, "end")

BOT = TY + 56
d.t(24, BOT, "더 큰 이유는 셋입니다. 덜 줄 수는 없고, metadata 공간이 필요하며, 가장 가까운 캐시를 쓰기 때문입니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 24, "정확한 값은 /sys/kernel/slab/<cache>/ 의 object_size 와 slab_size 에 있습니다(root 필요).", 13, SOFT, KR, "start")

d.legend(H - 48, [("세 API 가 답하는 값", INFO), ("실제 할당 — 이 절의 논점", ACC), ("아무도 말해 주지 않는 구간", WARN)])
d.save("09-01.object-size-gap.svg")
print("ok 09-01.object-size-gap")
