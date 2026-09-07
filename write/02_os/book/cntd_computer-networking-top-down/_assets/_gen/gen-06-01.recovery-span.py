# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 축 + 행마다 막대 하나, 구간별 zone 묶음.
#   축약: 가로축이 시간이 아니라 경로 위치(링크 1~6)다. 막대 길이 = 복구가 되돌아가는 구간이라는 점은 같다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.1.1 Reliable delivery 항 —
#   "correcting an error locally—on the link where the error occurs—rather than forcing an end-to-end retransmission"
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

W, H = 940, 420
d = D(W, H, "SECTION 6.1.1 · WHERE THE RECOVERY REACHES",
      "고치는 자리가 되돌아가는 거리를 정합니다",
      "무선 링크에서 비트가 뒤집혔을 때, 링크 계층이 그 자리에서 고치면 한 칸을 되돌아가고 트랜스포트가 고치면 여섯 칸을 되돌아간다.",
      "막대 길이가 곧 되돌아가는 구간입니다")

LX, TX, SLOT = 24, 232, 112
NAMES = ["WiFi", "이더넷", "미지정", "미지정", "이더넷", "이더넷"]

def slot_x(i):
    return TX + i * SLOT

# 축 — 링크 여섯 칸
for i in range(6):
    x = slot_x(i)
    d.box(x, 108, SLOT - 4, 40, PAPER2, RULE, 0.9)
    d.t(x + (SLOT - 4) / 2, 124, f"링크 {i + 1}", 11, INK, KR, "middle", 600)
    d.t(x + (SLOT - 4) / 2, 140, NAMES[i], 10, MUTED, MONO)

# zone — 무선 한 칸과 유선 다섯 칸
d.line(TX, 96, TX + 6 * SLOT - 4, 96, RULE, 0.8)
d.t(slot_x(0) + 54, 90, "오류율 높음", 10, SOFT, KR)
d.t(slot_x(1) + (5 * SLOT - 4) / 2, 90, "오류율 낮음 — 광 · 동축 · 트위스티드페어", 10, SOFT, KR)

# 오류 발생 지점
d.chip(slot_x(0) + 54, 176, "비트가 여기서 뒤집혔습니다", BAD, 10)
d.t(LX, 180, "무엇이 일어났나", 11, MUTED, KR, "start")

ROWS = [
    ("링크 계층이 고칩니다", "ARQ 로 그 링크에서 재전송", 1, ACC, True, "한 칸"),
    ("트랜스포트가 고칩니다", "TCP 가 종단에서 재전송", 6, INFO, False, "여섯 칸"),
]
y = 212
for label, sub, span, color, hot, span_txt in ROWS:
    d.t(LX, y + 16, label, 12, color if hot else INK, KR, "start", 600)
    d.t(LX, y + 34, sub, 10, MUTED, MONO, "start")
    bw = span * SLOT - 4
    if hot:
        d.tone(slot_x(0), y, bw, 44, color, 6, "1E", 1.6)
    else:
        d.tone(slot_x(0), y, bw, 44, color, 6, "14", 1.1)
    d.t(slot_x(0) + bw / 2, y + 28, span_txt, 13, color, KR, "middle", 600)
    y += 72

d.line(24, 336, W - 48, 336, RULE, 0.8)
d.t(24, 358, "그래서 무선 링크는 신뢰 전달을 두고, 광·동축·트위스티드페어 같은 저오류 링크는 두지 않습니다. "
             "저오류 링크에서는 그 기능이 불필요한 오버헤드가 됩니다.", 11, MUTED, KR, "start")

d.legend(376, [("링크에서 국소 복구", ACC), ("종단 간 복구", INFO), ("오류 발생", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-01.recovery-span.svg"
d.save(out)
print("→", out)
