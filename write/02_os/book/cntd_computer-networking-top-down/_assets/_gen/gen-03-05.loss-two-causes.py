# 03-05 §3 — 세그먼트가 사라지는 길은 둘이지만 보내는 쪽에는 "ACK 가 안 온다" 하나로만 보인다.
# 노트의 읽기: 2026-09-08 회차에서 학습자가 "손실은 꽉 차서 없어지는 것 아닌가" 에서 막혀 추가한 도식.
#       원문 3.7.1 은 잃은 세그먼트를 혼잡의 뜻으로 읽는 것을 첫 원리로 세울 뿐, 손실의 다른 원인을 이 절에서 갈라 적지 않는다.
#   원문 1.4.2: 큐가 유한해 가득 찬 큐에 도착한 패킷은 버려진다 (01-04).
#   RFC 3168 §4: 능동 큐 관리(RED 등)는 큐가 넘치기 전에 미리 버리기도 한다 — 혼잡 손실이 "꽉 참" 만은 아니다.
#   원문 3.3·3.4: 체크섬이 비트 오류를 잡고, rdt2.0 이 비트가 뒤집히는 채널을 다룬다 (03-01 §6 · 03-02).
#   RFC 3168 §5: "Routers that have a packet arriving at a full queue drop the packet, just as they do in the absence of ECN."
# 타입 스펙: type-fishbone — 한 증상(효과 상자)으로 모이는 원인 뼈. 뼈는 60° 사선이고 스펙의 attach/far/tick 공식을 그대로 쓴다.
#       축약: 뼈가 둘이라 스펙의 5개 상한을 한참 밑돈다 — 원인이 둘이라는 것 자체가 주장이라 셋째를 지어내지 않는다.
#       스펙은 확정된 원인 뼈 하나에 강조색을 주지만, 이 그림의 주장은 "어느 뼈인지 보내는 쪽이 모른다" 라서
#       뼈에는 강조색을 주지 않고 효과 상자에만 준다(강조 1개). HEAD 를 780 으로 옮겨 아래 뼈의 부원인 라벨이
#       왼쪽 밖으로 나가지 않게 했다. 부원인 라벨은 스펙의 9px 모노 대신 한글 최소 크기 12px 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 576
HEAD, CY = 780, 300
def attach(k): return HEAD - 160 - k * 160
BONES = [
    (1, "혼잡 손실", ["라우터 큐가 꽉 참", "멀쩡한 패킷을 버림", "유선 코어에서 대부분"]),
    (2, "오류 손실", ["전파·잡음으로 비트가 깨짐", "체크섬·CRC 불일치로 버림", "무선 링크에서 흔함"]),
]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §3",
      "손실은 두 가지 이유로 납니다",
      "라우터 큐가 넘쳐 멀쩡한 패킷이 버려지는 혼잡 손실과, 비트가 깨져 검사에서 버려지는 오류 손실. "
      "둘 다 보내는 쪽에는 ACK 가 안 온다는 한 증상으로만 보이고, 헤더 어디에도 이유가 적히지 않는다.",
      "두 원인이 한 증상으로 모이고, 그 증상에는 원인이 안 적혀 있습니다")

# 순서: 등뼈 → 뼈 → 부원인 눈금 → 범주 태그 → 효과 상자 (선을 먼저, 상자가 선 끝을 덮는다)
d.arrow([(170, CY), (HEAD - 3, CY)], MUTED, "ar", 1.2)
for k, name, subs in BONES:
    ax, sgn = attach(k), (-1 if k % 2 else 1)
    fx, fy = ax - 96, CY + sgn * 168
    d.line(ax, CY, fx, fy, MUTED, 1.2)
    for m, sub in zip((2, 3, 4), subs):
        tx, ty = ax - 16 * m, CY + sgn * 28 * m
        d.line(tx, ty, tx - 32, ty, SOFT, 1.0)
        d.t(tx - 36, ty + (-4 if sgn < 0 else 12), sub, 12, MUTED, KR, "end")
for k, name, subs in BONES:
    ax, sgn = attach(k), (-1 if k % 2 else 1)
    fx, fy = ax - 96, CY + sgn * 168
    by = fy - 34 if sgn < 0 else fy + 2
    d.box(fx - 60, by, 120, 32, PAPER2, RULE, 1.0, 4)
    d.t(fx, by + 21, name, 12, INK, KR, "middle", 600)

d.tone(HEAD, CY - 36, 200, 76, ACC, 6, "18", 1.2)
d.t(HEAD + 100, CY - 14, "보내는 쪽에 보이는 것", 12, MUTED, KR)
d.t(HEAD + 100, CY + 8, "ACK 가 안 온다", 14, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 28, "타임아웃 · 중복 ACK 셋", 12, MUTED, KR)
d.t(HEAD + 200, CY + 64, "받는 쪽도 순서 번호의 구멍만 봅니다", 12, MUTED, KR, "end")
d.t(HEAD + 200, CY + 84, "깨진 세그먼트는 검사에서 버려져 도착 자체가 없던 일이 됩니다", 12, MUTED, KR, "end")

d.legend(H - 52, [("두 원인 — 헤더에 적히지 않음", MUTED), ("보내는 쪽이 보는 하나의 증상", ACC)])
d.save("03-05.loss-two-causes.svg")
print("ok 03-05.loss-two-causes")
