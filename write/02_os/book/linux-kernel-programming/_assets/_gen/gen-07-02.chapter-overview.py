# 07-02 전체 지도 — VAS 를 어느 도구로 어디까지 들여다볼 수 있는가.
# 타입 스펙: type-process — 네 절이 "유저 VAS 를 읽는다 → 커널 VAS 를 읽는다 → 그 주소가 매번 바뀐다" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 928, 472
X0, CW, STRIDE, CY, CH = 24, 192, 228, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-02",
       "VAS 를 실제로 들여다봅니다",
       "07-02 가 다루는 네 절. 앞 노트가 세운 VM split 개념 위에서, 유저 VAS 를 procfs 로 읽고 커널 VAS 를 매크로와 LKM 으로 읽는다. 마지막 절은 그렇게 읽은 주소가 왜 실행마다 달라지는지를 다룬다.",
       "읽는 도구가 유저 쪽과 커널 쪽에서 갈립니다 — procfs 는 유저 VAS 만 보여줍니다")

CARDS = [
    ("§1", "maps", "한 줄이 매핑 하나이고", "필드는 일곱입니다", "/proc/PID/maps", INFO),
    ("§2", "procmap · VMA", "커널이 매핑마다", "VMA 객체 하나를 둡니다", "vm_area_struct", ACC),
    ("§3", "커널 VAS", "영역 경계가 매크로이고", "LKM 으로 조회합니다", "PAGE_OFFSET", INFO),
    ("§4", "[K]ASLR", "그 주소들은 실행마다", "랜덤 오프셋으로 옮겨집니다", "randomize_va_space", INFO),
]

for i, (tag, name, l1, l2, out, c) in enumerate(CARDS):
    x = X0 + i * STRIDE
    if c is ACC:
        d.tone(x, CY, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, CY + 30, tag, 13, c, MONO, "start", 600)
    d.t(x + CW - 16, CY + 30, name, 14, INK if c is not ACC else ACC, KR, "end", 600)
    d.line(x + 16, CY + 46, x + CW - 16, CY + 46, RULE, 0.8)
    d.t(x + 16, CY + 76, l1, 13, MUTED, KR, "start")
    d.t(x + 16, CY + 98, l2, 13, MUTED, KR, "start")
    d.chip(x + CW / 2, CY + 144, out, c, 13)

# 카드 사이 간격이 화살촉을 담기에 좁다 — 읽는 방향은 카드 아래 레일 하나로 보인다.
RAIL = CY + CH + 24
RIGHT = X0 + (len(CARDS) - 1) * STRIDE + CW
d.t(X0, RAIL + 5, "읽는 순서", 12, SOFT, KR, "start")
d.arrow([(X0 + 72, RAIL), (RIGHT, RAIL)], SOFT, "soft", 1.2, "4 6")

d.t(X0, 356, "§1 이 보여주는 한 줄은 §2 의 VMA 메타데이터에서 나옵니다 — 그래서 VMA 가 이 편의 중심입니다.", 13, MUTED, KR, "start")
d.t(X0, 380, "§3 은 procfs 로는 못 보는 커널 쪽을 LKM 으로 열고, §4 는 §1~§3 의 주소가 고정값이 아님을 밝힙니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("이 편의 중심", ACC), ("나머지 절", INFO)])
d.save("07-02.chapter-overview.svg")
print("ok 07-02.chapter-overview")
