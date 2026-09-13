# 09-01 §5 — 메모리 압박과 캐시 축소가 서로를 먹이는 순환.
# 본문이 요구한 형태: "메모리 압박이 높아지면 커널이 shrinker 콜백을 불러 slab 객체를 풀게 한다."
# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고, 공유 허브(자유 메모리)에 그 결과가 쌓인다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 680
NW, NH = 232, 84

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-01 §5",
       "압박이 캐시를 풀고, 풀린 만큼 압박이 줄고",
       "캐시는 성능에 좋지만 필수는 아니다. 자유 메모리가 줄면 kswapd 가 등록된 shrinker 를 불러 캐시를 축소하고, 그렇게 풀린 페이지가 다시 자유 메모리를 늘린다. shrinker 를 등록하지 않은 custom slab cache 는 이 순환에 참여하지 못해, 압박이 와도 커널이 회수하지 못한다.",
       "등록하지 않으면 이 고리에서 빠집니다 — 그래서 best practice 입니다")

NODES = [
    (348, 116, "자유 메모리가 줄어든다", "커널이 압박을 감지합니다", WARN),
    (668, 268, "kswapd 가 shrinker 를 부른다", "count_objects() 로 먼저 셉니다", INFO),
    (348, 420, "캐시가 객체를 푼다", "scan_objects() 가 축소합니다", ACC),
    (28, 268, "페이지가 돌아온다", "자유 메모리가 늘어납니다", OK),
]

for x, y, title, sub, c in NODES:
    focal = c is ACC
    d.tone(x, y, NW, NH, c, 8, "12" if focal else "14", 1.4 if focal else 1.1)
    d.t(x + NW / 2, y + 36, title, 13, c, KR, "middle", 600)
    d.t(x + NW / 2, y + 58, sub, 13, MUTED, KR)

# 공유 허브 — 이 순환이 실제로 움직이는 상태
HX, HY, HW, HH = 388, 272, 152, 76
d.box(HX, HY, HW, HH, PAPER2, RULE, 1.0, 8)
d.t(HX + HW / 2, HY + 32, "자유 메모리", 13, INK, KR, "middle", 600)
d.t(HX + HW / 2, HY + 54, "watermark 기준", 12, SOFT, MONO)

# 시계 방향 순환
d.path(f"M {348 + NW} 158 L 784 158 L 784 262", MUTED, 1.5, m="ar")
d.path(f"M 784 {268 + NH} L 784 462 L {348 + NW + 6} 462", ACC, 1.5, m="acc")
d.path(f"M 348 462 L 144 462 L 144 {268 + NH + 6}", MUTED, 1.5, m="ar")
d.path(f"M 144 268 L 144 158 L {348 - 6} 158", OK, 1.5, m="ok")

d.t(24, 552, "count_objects() 가 0 이나 SHRINK_EMPTY 를 돌려주면 scan_objects() 는 아예 불리지 않습니다.", 13, MUTED, KR, "start")
d.t(24, 576, "진행하면 deadlock 이 날 상황이면 scan_objects() 가 SHRINK_STOP 을 돌려 스스로 멈춥니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("압박 감지", WARN), ("커널이 부르는 쪽", INFO), ("축소 — 이 절의 논점", ACC), ("되돌아오는 메모리", OK)])
d.save("09-01.shrinker-loop.svg")
print("ok 09-01.shrinker-loop")
