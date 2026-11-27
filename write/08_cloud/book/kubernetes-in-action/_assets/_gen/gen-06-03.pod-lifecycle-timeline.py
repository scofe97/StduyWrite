# 06-03 §1 — Pod 생애주기 전체 지도
# 본문: "초기화 → 시작 → 실행 → 종료로 이어지는 Pod 생애주기"
#       "종료 유예 시간은 PreStop보다 먼저 시작되며, hook 실행과 SIGTERM 이후의 정리 시간을 모두 포함합니다."
# 타입 스펙: type-timeline.md — 스케줄링부터 SIGKILL 까지 사건들이 시간축 위에 순서대로 찍히고,
#           종료 유예(기본 30s)가 PreStop 보다 먼저 시작해 SIGTERM·SIGKILL 까지 걸치는 구간을
#           기준선 위 타임라인과 구간 브래킷으로 드러낸다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO
import ddx

W, H = 1000, 628
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "Pod 생애주기 전체 — 유예 시간은 PreStop 보다 먼저 시작",
      "스케줄링과 이미지 준비, init 컨테이너를 거쳐 일반 컨테이너와 PostStart 가 시작된다. "
      "삭제 시 deletionGracePeriodSeconds(기본 30s)가 PreStop 보다 먼저 시작되며 SIGTERM 과 정리 시간을 모두 포함한다.",
      lead="초기화 → 시작·실행 → 종료 유예 30s (PreStop · SIGTERM · SIGKILL 모두 포함)")

ddx.band(d, 104, 568, "유예 시간 30s 는 PreStop 보다 먼저 시작 · hook 과 정리 시간 모두 포함")

BASE_Y = 332
X0, STRIDE = 116, 96          # 9 events: 116 .. 884 (4px grid)
XS = [X0 + i * STRIDE for i in range(9)]

# 상단 Phase 구분 막대 (y=156..184)
PHASES = [
    (48, 352, INFO, "초기화 단계"),
    (364, 544, OK, "시작 · 실행"),
    (556, 952, ACC, "종료 유예 30s (PreStop · SIGTERM 포함)"),
]
for px0, px1, pc, plab in PHASES:
    d.o.append(f'<rect x="{px0}" y="152" width="{px1-px0}" height="28" rx="4" '
               f'fill="{pc}14" stroke="{pc}" stroke-width="1.0"/>')
    d.t((px0 + px1) // 2, 170, plab, 12, pc, KR, "middle", 600)

# 종료 유예 30s 범위 표시 (라벨과 겹치지 않게 위쪽 188..212 구간에만)
d.line(XS[5], 188, XS[5], BASE_Y - 10, ACC, 1.0, "4 5")
d.path(f"M {XS[5]} 196 H {XS[8]} V 214", ACC, 1.2, dash="4 4")

# 수평 기준선 (hairline)
d.line(48, BASE_Y, 952, BASE_Y, RULE, 1.0)

EVENTS = [
    # (idx, pos, title, sub, color, milestone)
    (0, "up",   "Pod 스케줄링",   "노드 바인딩",            INFO, False),
    (1, "down", "이미지 준비",    "imagePullPolicy",       INFO, False),
    (2, "up",   "init 컨테이너",  "순차 실행 · exit 0",    INFO, False),
    (3, "down", "시작 · PostStart","병렬 · 완료 전 Pending", OK,   False),
    (4, "up",   "probe 감시",     "startup → liveness",    OK,   False),
    (5, "down", "삭제 · 유예 시작","t = 0s (기본 30s)",      ACC,  True),
    (6, "up",   "PreStop hook",  "완료까지 SIGTERM 보류",  WARN, False),
    (7, "down", "SIGTERM (15)",  "정상 정리 · 코드 143",   BAD,  False),
    (8, "up",   "SIGKILL (9)",   "유예 만료 · 코드 137",   BAD,  False),
]

for idx, pos, title, sub, c, mile in EVENTS:
    x = XS[idx]
    r = 6 if mile else 4
    d.o.append(f'<circle cx="{x}" cy="{BASE_Y}" r="{r}" fill="{c}"/>')
    if pos == "up":
        d.line(x, BASE_Y - r - 2, x, 272, c, 1.0)
        d.t(x, 240, title, 13, c if mile else INK, KR, "middle", 600)
        d.t(x, 260, sub, 11, MUTED, MONO if all(ord(ch) < 128 for ch in sub) else KR)
    else:
        d.line(x, BASE_Y + r + 2, x, 392, c, 1.0)
        d.t(x, 412, title, 13, c if mile else INK, KR, "middle", 600)
        d.t(x, 432, sub, 11, MUTED, MONO if all(ord(ch) < 128 for ch in sub) else KR)

# 남은 유예 시간 브래킷 (SIGTERM -> SIGKILL 사이)
d.path(f"M {XS[7]} 452 L {XS[7]} 468 L {XS[8]} 468 L {XS[8]} 452", MUTED, 1.1)
d.t((XS[7] + XS[8]) // 2, 488, "남은 유예 시간", 11, MUTED, KR)

d.t(36, 540, "실행 중 probe 감시 · 삭제 요청(t=0s) 즉시 유예 30s 카운트 · 만료 전 미종료 시 SIGKILL(9)",
     12, MUTED, KR, "start")
d.legend(584, [("초기화", INFO), ("시작 · 실행", OK), ("유예 시작점 (t=0s)", ACC),
               ("PreStop 보류", WARN), ("종료 시그널", BAD)])
d.save("06-03-pod-lifecycle-timeline.svg")
print("ok pod-lifecycle-timeline")
