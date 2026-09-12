# 2026-09-10 E — 가상 스레드가 synchronized 안에서 캐리어를 붙든 채 서로를 기다린다.
# 회차에서 학습자가 pinning 을 이름으로 짚었으나 "왜 스스로 못 풀리는가"가 급소였다.
# 기다리는 대상이 자기 실행 수단이라는 점을 한 장에 고정한다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지고 한쪽 끝이 빠져나오지 못하는 경로.
#           loop 를 검토했으나 스펙이 요구하는 5~8 station + 상태를 쌓는 hub 가 없고
#           두 당사자의 상호 대기라 기각(스펙: "Prefer Flowchart when the path ends").
#           state 도 검토했으나 상태 전이가 아니라 자원 점유 관계라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 840, 612
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 E",
      "기다리는 대상이 자기 실행 수단입니다",
      "가상 스레드는 블로킹할 때 캐리어에서 내려와 자리를 내준다. synchronized 안에서는 "
      "내려오지 못해 캐리어를 붙든 채 멈춘다. 그 I/O 를 끝낼 작업도 캐리어가 있어야 도는데, "
      "남은 캐리어가 없어 서로를 영원히 기다린다.",
      lead="왼쪽이 정상 경로, 오른쪽이 이 사고의 경로입니다.")

Y0 = 152
BW, BH = 286, 62

def stack(x, title, c, rows, tail):
    d.t(x + BW / 2, Y0 - 14, title, 13, c, KR, "middle", 600)
    y = Y0
    for i, (txt, sub) in enumerate(rows):
        d.tone(x, y, BW, BH, c, 6) if i == len(rows) - 1 else d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
        d.t(x + 16, y + 26, txt, 13, INK if i < len(rows) - 1 else c, KR, "start", 600)
        d.t(x + 16, y + 46, sub, 11, MUTED, MONO, "start")
        if i < len(rows) - 1:
            d.arrow([(x + BW / 2, y + BH), (x + BW / 2, y + BH + 24)], SOFT, "soft", 1.2)
        y += BH + 24
    d.t(x + BW / 2, y + 10, tail, 12, c, KR, "middle", 600)
    return y

LX, RX = 52, 502

stack(LX, "ReentrantLock · 정상", OK, [
    ("가상 스레드가 블로킹", "lock() 안에서 대기"),
    ("캐리어에서 내려옴", "unmount"),
    ("다른 가상 스레드가 올라탐", "캐리어 재사용"),
], "자리가 돌아 처리량이 유지됩니다")

ybot = stack(RX, "synchronized · 이 사고", BAD, [
    ("가상 스레드가 블로킹", "synchronized 안에서 I/O 대기"),
    ("내려오지 못함", "pinned — 캐리어 점유 유지"),
    ("캐리어가 전부 소진", "새 가상 스레드는 대기열에"),
], "그 I/O 를 끝낼 작업도 캐리어가 필요합니다")

ARCX = RX - 34
d.path(f"M {RX + 12} {ybot + 26} "
       f"C {ARCX} {ybot + 26} {ARCX} {Y0 + 30} {RX - 8} {Y0 + 30}",
       BAD, 1.6, m="ar", dash="5 5")
d.t(ARCX - 6, (Y0 + ybot) / 2, "영원히", 12, BAD, KR, "end", 600)

d.t(W // 2, ybot + 70, "CPU 는 0.7% 입니다 — 캐리어는 점유돼 있으나 일하고 있지 않습니다",
    13, MUTED, KR, "middle")
d.t(W // 2, ybot + 94,
    "부하가 빠져도 안 풀립니다. 재시작만이 답이고, CLOSE_WAIT 는 그 결과로 쌓입니다.",
    12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.pinning-deadlock.svg"))
print("ok")
