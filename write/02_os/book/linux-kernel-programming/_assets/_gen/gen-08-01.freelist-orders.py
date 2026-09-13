# 08-01 §2 — freelist 가 order 별 배열이고, order 하나 올라갈 때마다 청크가 배로 커진다.
# 본문이 요구한 형태: "배열 인덱스를 order 라 부른다 — 2를 거듭제곱할 지수" + "한 order 의 청크 크기는 항상 이전 order 의 두 배".
# 타입 스펙: type-layers — order 0 이 아래, MAX_ORDER-1 이 위. 위로 갈수록 청크가 배로 커진다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 684
X0, RW, RH, RS, Y0 = 96, 640, 32, 36, 124

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-01 §2",
       "order 하나에 청크가 배로 커집니다",
       "freelist 는 이중 연결 순환 리스트들을 가리키는 포인터 배열이고, 배열 인덱스가 order 다. order N 리스트는 2^N 페이지짜리 물리 연속 청크만 담는다. x86·ARM 의 MAX_ORDER 는 11 이라 order 는 0부터 10, 한 번에 받을 수 있는 최대치가 4MB 다.",
       "4KB 페이지 기준 — 이 배열이 노드:존마다 따로 있습니다")

for i in range(11):
    order = 10 - i                       # 위가 큰 order
    y = Y0 + i * RS
    pages = 2 ** order
    size = pages * 4
    label = f"{size} KB" if size < 1024 else f"{size // 1024} MB"
    focal = order == 10
    if focal:
        d.tone(X0, y, RW, RH, ACC, 4, "12", 1.4)
    else:
        d.box(X0, y, RW, RH, PAPER2, RULE, 0.9, 4)
    c = ACC if focal else (INFO if order >= 5 else MUTED)
    d.t(X0 - 12, y + 21, f"order {order}", 12, c, MONO, "end", 600)
    d.t(X0 + 16, y + 21, f"2^{order} = {pages} 페이지", 13, c, KR, "start")
    d.t(X0 + 232, y + 21, label, 13, c, MONO, "start", 600)
    # 그 order 리스트에 달린 청크들 — 상자 하나가 청크 하나이고, 크기 비례가 아니라 개수만 보인다
    n = [2, 3, 4, 4, 4, 4, 3, 2, 2, 1, 1][i]
    for k in range(n):
        d.box(X0 + 396 + k * 44, y + 6, 36, 20, PAPER, c, 0.9, 3)

BOT = Y0 + 11 * RS
d.t(24, Y0 - 12, "청크가 크다", 12, SOFT, KR, "start")
d.t(24, BOT + 18, "청크가 작다", 12, SOFT, KR, "start")
d.t(X0 + 396, Y0 - 12, "상자 하나가 그 리스트에 달린 자유 청크 하나입니다", 12, SOFT, KR, "start")

d.t(24, BOT + 44, "청크마다 물리 연속이 보장됩니다. 그래서 반으로 쪼개도 두 조각이 각각 물리 연속입니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 68, "커널은 노드:존마다 이 배열을 따로 둡니다. 2.6.24 부터는 migration type 으로 한 번 더 쪼개, 4 노드·3 존이면 최대 72개가 됩니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 92, "현재 상태는 /proc/buddyinfo 로 봅니다. 존 이름 뒤 숫자가 order 0 부터의 청크 개수입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("한 번에 받을 수 있는 최대", ACC), ("드라이버가 흔히 쓰는 구간", INFO)])
d.save("08-01.freelist-orders.svg")
print("ok 08-01.freelist-orders")
