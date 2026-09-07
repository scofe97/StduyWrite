# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이는 순환. 토큰이 고정 순서로 한 바퀴를 돈다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3.3 — 폴링 프로토콜과 토큰 패싱 프로토콜
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 940, 500
d = D(W, H, "SECTION 6.3.3 · TAKING TURNS",
      "차례를 정해 주면 충돌도 빈 슬롯도 없습니다",
      "폴링은 컨트롤러가 차례를 나눠 주고 토큰 패싱은 특별한 프레임 하나가 고정 순서로 돈다. 효율은 오르지만 각각 새 약점이 생긴다.",
      "원문 §6.3.3 의 두 프로토콜입니다")

# 왼쪽 — 폴링
d.t(24, 116, "폴링 — 컨트롤러가 나눠 줍니다", 12, INK, KR, "start", 600)
d.tone(148, 144, 160, 48, BAD, 6, "14", 1.4)
d.t(228, 174, "컨트롤러 노드", 12, BAD, KR, "middle", 600)
for i in range(4):
    x = 40 + i * 104
    d.box(x, 264, 88, 44, PAPER2, RULE, 0.9)
    d.t(x + 44, 291, f"노드 {i + 1}", 11, INK, KR, "middle", 600)
    d.path(f"M 228 196 L 228 232 L {x + 44} 232 L {x + 44} 260", MUTED, 1.1, m="ar", dash="4 5")
    d.t(x + 44, 250, str(i + 1), 10, SOFT, MONO)

d.line(492, 108, 492, 408, RULE, 0.8)

# 오른쪽 — 토큰 패싱
d.t(524, 116, "토큰 패싱 — 특별한 프레임이 돕니다", 12, INK, KR, "start", 600)
RING = [("노드 1", 700, 164), ("노드 2", 810, 236), ("노드 3", 700, 308), ("노드 4", 590, 236)]
for i, (name, cx, cy) in enumerate(RING):
    hot = i == 1
    if hot:
        d.tone(cx - 44, cy - 20, 88, 40, ACC, 6, "1E", 1.5)
    else:
        d.box(cx - 44, cy - 20, 88, 40, PAPER2, RULE, 0.9)
    d.t(cx, cy + 5, name, 11, ACC if hot else INK, KR, "middle", 600)

for seg in ["M 744 164 L 810 164 L 810 212",
            "M 810 256 L 810 308 L 748 308",
            "M 656 308 L 590 308 L 590 260",
            "M 590 212 L 590 164 L 652 164"]:
    d.path(seg, INFO, 1.3, m="info")
d.chip(700, 236, "토큰", ACC, 11)

d.t(24, 352, "차례로 돌면서 최대 몇 프레임까지 보내라고 알립니다.", 11, MUTED, KR, "start")
d.t(24, 374, "·", 11, BAD, KR, "start", 600)
d.t(38, 374, "폴링 지연이 붙고, 컨트롤러가 죽으면 채널 전체가 멎습니다", 11, MUTED, KR, "start")
d.t(24, 396, "·", 11, OK, KR, "start", 600)
d.t(38, 396, "블루투스가 폴링 프로토콜입니다", 11, MUTED, KR, "start")

d.t(524, 352, "받은 노드는 보낼 것이 있을 때만 붙잡고, 없으면 바로 넘깁니다.", 11, MUTED, KR, "start")
d.t(524, 374, "·", 11, OK, KR, "start", 600)
d.t(538, 374, "컨트롤러가 없어 분산이고 효율이 높습니다", 11, MUTED, KR, "start")
d.t(524, 396, "·", 11, BAD, KR, "start", 600)
d.t(538, 396, "한 노드 고장이나 토큰 분실이 채널을 멈춥니다", 11, MUTED, KR, "start")

d.line(24, 420, W - 48, 420, RULE, 0.8)
d.t(24, 442, "둘 다 랜덤 접속이 못 지킨 조건을 노립니다. M 개 노드가 활성일 때 각자 R/M 에 가까운 처리량을 갖는 것입니다.",
     11, MUTED, KR, "start")

d.legend(460, [("토큰을 쥔 노드", ACC), ("토큰이 도는 길", INFO), ("얻는 것", OK), ("새로 생기는 약점", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.taking-turns.svg"
d.save(out)
print("→", out)
