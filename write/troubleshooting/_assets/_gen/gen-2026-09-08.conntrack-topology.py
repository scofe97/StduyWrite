# 2026-09-08 A 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "요청이 지나는 경로 어디에 무엇이 있나"이지 인과가 아니다.
# 인과 사슬은 원인 분석 절의 drop-sites 가 맡는다.
# 샤딩으로 오른쪽 대상이 두 배가 됐고, 노드 사양이 절반이 되어 가운데 장부가 줄었다.
# 타입 스펙: type-architecture — 구성요소와 연결. 경계 상자로 노드 범위를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 800, 446
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 A",
      "요청이 지나는 경로",
      "집계 서비스가 HAProxy 를 거쳐 하위 서비스로 나가는 구조. "
      "가운데 노드 경계 안에 커널 conntrack 장부가 있고, 나가는 흐름은 모두 여기에 기록된다. "
      "샤딩으로 오른쪽 대상이 두 배가 됐고 사양 축소로 장부는 줄었다.",
      lead="바뀐 것은 양 끝이고 줄어든 것은 가운데입니다")

# 노드 경계
NX, NY, NW_, NH_ = 40, 108, 470, 226
d.box(NX, NY, NW_, NH_, PAPER2, RULE, 1.0, 8)
d.t(NX + 14, NY + 22, "노드 한 대", 12, SOFT, KR, "start", 600)
d.t(NX + 14, NY + 38, "사양 절반으로 축소", 11, WARN, KR, "start")

# 앱 · 프록시
d.box(NX + 28, NY + 58, 170, 62, PAPER2, RULE, 0.9, 6)
d.t(NX + 113, NY + 84, "집계 서비스", 13, INK, KR, "middle", 600)
d.t(NX + 113, NY + 104, "10,000 req/s · x4", 11, SOFT, MONO)

d.box(NX + 258, NY + 58, 170, 62, PAPER2, RULE, 0.9, 6)
d.t(NX + 343, NY + 84, "HAProxy", 13, INK, KR, "middle", 600)
d.t(NX + 343, NY + 104, "리셋 카운트 상승", 11, BAD, KR)

d.arrow([(NX + 198, NY + 89), (NX + 254, NY + 89)], MUTED, "ar", 1.3)

# conntrack 장부 (커널)
d.tone(NX + 28, NY + 156, 400, 52, ACC, 6)
d.t(NX + 44, NY + 178, "커널 conntrack 장부", 13, ACC, KR, "start", 600)
d.t(NX + 44, NY + 197, "한도는 커널이 총 메모리에서 유도", 11, SOFT, KR, "start")
d.arrow([(NX + 343, NY + 120), (NX + 343, NY + 152)], ACC, "acc", 1.3)

# 하위 서비스 (샤딩으로 2배)
BX = 588
d.t(BX + 70, NY + 22, "하위 서비스", 12, SOFT, KR, "middle", 600)
d.t(BX + 70, NY + 38, "샤딩으로 두 배", 11, WARN, KR)
for i in range(4):
    yy = NY + 56 + i * 40
    faded = i >= 2
    d.box(BX, yy, 140, 30, PAPER2, RULE, 0.9, 5)
    d.t(BX + 70, yy + 20, f"샤드 {i+1}", 12, SOFT if faded else INK, KR)
d.arrow([(NX + NW_, NY + 89), (BX - 4, NY + 89)], MUTED, "ar", 1.3)
d.t((NX + NW_ + BX) / 2, NY + 78, "커넥션", 11, SOFT, KR)

d.t(NX + 14, NY + NH_ + 26, "나가는 흐름도 장부에 한 줄씩 오릅니다. 대상이 늘면 줄 수가 늘어납니다.",
    12, MUTED, KR, "start")

d.legend(H - 52, [("한도가 줄어든 자리", ACC), ("늘어난 수요", WARN)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.conntrack-topology.svg"))
print("ok topology")
