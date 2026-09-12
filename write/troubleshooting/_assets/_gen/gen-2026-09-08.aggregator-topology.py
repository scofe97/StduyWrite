# 2026-09-08 B 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 팬아웃이다. 집계 계층 하나가 하위 여럿을 부르고, 그 이름을 풀려고
# CoreDNS 를 거친다. 부가 정보 하나가 약한데 그 실패가 페이지 전체를 죽인다.
# 인과 사슬은 원인 분석 절의 dns-cascade 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 팬아웃과 공유 의존을 함께 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, WARN, OK, PAPER2, RULE, KR, MONO

W, H = 800, 470
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 B",
      "집계 계층이 부르는 것들",
      "집계 계층 하나가 하위 서비스 여럿을 모아 페이지를 만드는 구조. "
      "호출마다 호스트명을 풀어야 하므로 모든 화살표가 CoreDNS 를 한 번씩 거친다. "
      "약한 것은 부가 정보 하나인데 CoreDNS 는 클러스터 전체가 공유한다.",
      lead="약한 것은 하나이고 공유되는 것은 전부입니다")

# 클라이언트
d.box(40, 118, 148, 56, PAPER2, RULE, 0.9, 6)
d.t(114, 142, "사용자 · CDN", 13, INK, KR, "middle", 600)
d.t(114, 161, "404 는 재시도를 안 막음", 11, BAD, KR)

# 집계 계층
d.box(232, 118, 168, 56, PAPER2, RULE, 0.9, 6)
d.t(316, 142, "집계 계층", 13, INK, KR, "middle", 600)
d.t(316, 161, "Node.js · 캐시 없음", 11, SOFT, MONO)
d.arrow([(188, 146), (228, 146)], MUTED, "ar", 1.3)

# 하위 서비스 팬아웃
BX = 596
LEAVES = [("상품 정보", False), ("가격", False), ("재고", False), ("부가 정보", True)]
for i, (nm, weak) in enumerate(LEAVES):
    yy = 96 + i * 46
    if weak:
        d.tone(BX, yy, 152, 34, BAD, 5)
        d.t(BX + 76, yy + 22, nm, 12, BAD, KR, "middle", 600)
    else:
        d.box(BX, yy, 152, 34, PAPER2, RULE, 0.9, 5)
        d.t(BX + 76, yy + 22, nm, 12, INK, KR)
    d.arrow([(400, 146), (500, 146), (500, yy + 17), (BX - 4, yy + 17)],
            BAD if weak else MUTED, "bad" if weak else "ar", 1.2)
d.t(BX + 76, 96 + 4 * 46 + 10, "없어도 되는 의존", 11, BAD, KR)

# CoreDNS — 공유
d.tone(232, 268, 168, 62, ACC, 6)
d.t(316, 292, "CoreDNS", 13, ACC, KR, "middle", 600)
d.t(316, 311, "limit 100Mi", 11, SOFT, MONO)
d.arrow([(316, 174), (316, 264)], ACC, "acc", 1.3)
d.t(330, 224, "호출마다 이름 해석", 11, ACC, KR, "start")

# 공유 범위
d.box(40, 356, 712, 44, PAPER2, RULE, 0.9, 6)
d.t(56, 383, "클러스터의 모든 Pod 가 이 하나를 함께 씁니다", 12, MUTED, KR, "start")

d.legend(H - 46, [("끊기면 범위가 전체", ACC), ("약한 의존 하나", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.aggregator-topology.svg"))
print("ok aggregator")
