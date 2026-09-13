# 08-01 §4 — 132KB 를 요청하면 256KB 를 받고 124KB 를 버린다. 그리고 그 낭비를 어떻게 되돌리는가.
# 본문의 수치를 그대로 옮겼다 — 132KB 요청 · order 7 의 256KB 할당 · 124KB 낭비(약 50%).
# 타입 스펙: type-bar — 범주별 수치 비교. 막대 길이가 곧 바이트 수이고, 두 방식의 차이가 곧 낭비다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 624
LX, LW = 24, 168
AX, AXW = 208, 700
MAXKB = 256

def px(kb): return AX + kb / MAXKB * AXW

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-01 §4",
       "2의 거듭제곱이 아니면 버려집니다",
       "132KB 를 요청하면 페이지 할당자는 그보다 적게 줄 수 없어 order 7 의 256KB 청크를 준다. 소비자는 앞 132KB 만 쓰고 나머지 124KB, 곧 거의 절반을 버린다. alloc_pages_exact() 는 평소처럼 받은 뒤 초과분을 즉시 free 해 이 낭비를 되돌린다.",
       "막대 길이가 곧 KB 입니다 — 위아래 두 막대의 차이가 버려지는 양입니다")

ROWS = [
    ("요청한 크기", 0, 132, "132 KB", INFO, "실제 필요한 양"),
    ("받은 크기", 0, 256, "256 KB — order 7", WARN, "더 적게는 못 줍니다"),
    ("버려진 크기", 132, 256, "124 KB · 48.4%", ACC, "쓰지 않는 구간"),
    ("alloc_pages_exact()", 0, 132, "132 KB", OK, "초과분을 free"),
]

Y0, RH, RS = 152, 40, 68
for i, (name, lo, hi, val, c, note) in enumerate(ROWS):
    y = Y0 + i * RS
    d.t(LX, y + 16, name, 13, c, KR, "start", 600)
    d.t(LX, y + 36, note, 12, SOFT, KR, "start")
    x0, x1 = px(lo), px(hi)
    d.tone(x0, y, x1 - x0, RH, c, 4, "22" if c is ACC else "18", 1.4 if c is ACC else 1.1)
    if x1 - x0 > 160:
        d.t(x0 + 16, y + 25, val, 13, c, MONO, "start", 600)
    else:
        d.t(x1 + 12, y + 25, val, 13, c, MONO, "start", 600)

# 눈금
TY = Y0 + len(ROWS) * RS - 16
d.line(AX, TY, AX + AXW, TY, RULE, 1.0)
for kb in (0, 64, 128, 192, 256):
    x = px(kb)
    d.line(x, TY, x, TY + 8, RULE, 1.0)
    d.t(x, TY + 26, f"{kb} KB", 12, SOFT, MONO)

# 낭비 구간을 위아래로 잇는다
d.line(px(132), Y0, px(132), Y0 + 2 * RS + RH, ACC, 1.2, "4 4")
d.t(px(132) + 8, Y0 - 12, "여기까지만 씁니다", 13, ACC, KR, "start")

BOT = TY + 56
d.t(24, BOT, "완화책은 2008년 Timur Tabi 가 기여한 alloc_pages_exact() / free_pages_exact() 쌍입니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 24, "구현은 단순합니다. __get_free_pages() 로 평소처럼 256KB 를 받은 뒤, 132KB 너머 페이지를 루프 돌며 free 합니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 48, "할당된 메모리는 여전히 물리 연속이고, 한 번에 받을 수 있는 양은 MAX_ORDER 제한을 그대로 받습니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("요청", INFO), ("실제 할당", WARN), ("버려지는 양 — 이 절의 논점", ACC), ("되돌린 결과", OK)])
d.save("08-01.internal-fragmentation.svg")
print("ok 08-01.internal-fragmentation")
