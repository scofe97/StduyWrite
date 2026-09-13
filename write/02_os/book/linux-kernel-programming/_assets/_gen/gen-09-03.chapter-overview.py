# 09-03 전체 지도 — malloc 성공이 물리 할당이 아니라는 사실에서 시작해 OOM killer 까지.
# 타입 스펙: type-process — 여섯 절이 "예약일 뿐이다 → 만질 때 할당된다 → 얼마나 봐 주나 → 누가 죽나 → 어떻게 가두나" 로 이어진다.
#           축약: 주체(lane)가 없는 단계 지도라 lane 축을 빼고 단계 카드만 남겼다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 976, 448
X0, CW, STRIDE, CY, CH = 24, 176, 184, 116, 180

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-03",
       "예약과 할당이 갈리는 자리",
       "09-03 이 다루는 여섯 절. malloc 이 성공해도 물리 메모리는 아직 없다. 페이지를 만지는 순간 페이지 폴트를 거쳐 프레임이 붙는다. 그 프레임이 끝내 없으면 OOM killer 가 누군가를 고른다.",
       "회수가 실패한 뒤의 이야기입니다 — 앞 노트(09-02)의 다음 장면")

CARDS = [
    ("§1", "demand paging", "malloc 성공은", "예약일 뿐입니다", "lazy allocation", ACC),
    ("§2", "폴트 흐름", "만지는 순간 폴트를", "거쳐 프레임이 붙습니다", "__alloc_pages", INFO),
    ("§3·4", "overcommit", "어디까지 봐 줄지를", "세 정책이 정합니다", "vm.overcommit", INFO),
    ("§5", "OOM score", "누구를 죽일지", "점수로 고릅니다", "oom_score_adj", BAD),
    ("§6", "cgroups", "애초에 그 상황을", "만들지 않는 쪽입니다", "memory.high", OK),
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

for i in range(4):
    x = X0 + i * STRIDE + CW
    d.arrow([(x + 4, CY + CH / 2), (x + STRIDE - CW - 6, CY + CH / 2)],
            ACC if i == 0 else MUTED, "acc" if i == 0 else "ar", 1.4)

d.t(X0, 336, "§1 의 사실 하나가 나머지를 다 끌고 옵니다 — 예약과 할당이 갈려 있으니 과약속이 가능하고, 과약속했으니 OOM 이 생깁니다.", 13, MUTED, KR, "start")
d.t(X0, 360, "§6 은 그 상황을 사후에 수습하는 대신 미리 가두는 쪽입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("이 편의 출발점", ACC), ("메커니즘", INFO), ("누가 죽나", BAD), ("예방", OK)])
d.save("09-03.chapter-overview.svg")
print("ok 09-03.chapter-overview")
