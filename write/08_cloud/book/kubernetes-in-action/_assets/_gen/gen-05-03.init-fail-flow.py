# 05-03 §init 실패 — 주 컨테이너는 시작조차 못 한다
# 본문: init 은 성공(exit 0)해야 다음으로 넘어간다. 실패하면 쿠버네티스가 재시도하고,
#       반복 실패하면 Init:CrashLoopBackOff 에 갇히며 주 컨테이너는 waiting/PodInitializing 이다.
#       죽은 init 의 로그는 `kubectl logs <pod> -c <init 이름>` 으로 남아 있다.
# 타입 스펙: type-flowchart.md — 모양이 종류를 진다. 마름모는 판정, 사각형은 단계, 고리 점은 끝.
#           coral 은 happy path 나 가장 중요한 판정 하나에만 — 여기서는 그 판정에 건다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 786
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "init 이 exit 0 을 내야 문이 열린다",
      "init 컨테이너가 실패하면 쿠버네티스가 재시도하고, 반복 실패하면 CrashLoopBackOff 에 "
      "갇힌다. 그동안 주 컨테이너는 PodInitializing 인 채 시작조차 하지 못한다.",
      lead="죽은 init 의 로그는 남는다 — kubectl logs <pod> -c <init 이름> 으로 사인을 본다")

INIT, DIA = (200, 224), (200, 372)
OKBOX, ERR, LOOP = (560, 372), (200, 500), (200, 610)
STUCK = (660, 610)
BW, BH = 240, 80

ddx.band(d, 104, 730, "문이 열리지 않으면 주 컨테이너는 기다리기만 한다 — Pod 는 살아 있고 로그도 남는다")

def step(cx, cy, t, s, c, w=BW, h=BH):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(t, 13, w - 18, t), 13, c,
        MONO if all(ord(ch) < 128 or ch in ':' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, w - 14, t), 10, SOFT, KR)

step(*INIT, "init 컨테이너", "준비 작업을 수행한다", INFO)

# 판정은 마름모 — 모양이 종류를 진다
# 마름모를 낮추고(dy 46) 아래 단계를 더 띄웠다 — 세로 스텁이 14px 로 뭉개졌었다
dx, dy = 96, 46
d.o.append(f'<path d="M {DIA[0]} {DIA[1]-dy} L {DIA[0]+dx} {DIA[1]} L {DIA[0]} {DIA[1]+dy} '
           f'L {DIA[0]-dx} {DIA[1]} Z" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(DIA[0], DIA[1] + 4, "exit 0 인가?", 13, ACC, KR, "middle", 600)

step(*OKBOX, "주 컨테이너 시작", "다음 단계로 넘어간다", OK)
step(*ERR, "Init:Error", "쿠버네티스가 재시도한다", BAD, h=76)
step(*LOOP, "Init:CrashLoopBackOff", "반복 실패로 갇힌다", BAD, h=64)
step(*STUCK, "주 컨테이너 — waiting", "PodInitializing · 시작조차 못 한다", WARN, w=320, h=64)

d.path(f"M {INIT[0]} {INIT[1]+BH//2+6} L {DIA[0]} {DIA[1]-dy-10}", MUTED, 1.5, m="ar")
d.path(f"M {DIA[0]+dx+6} {DIA[1]} L {OKBOX[0]-BW//2-10} {OKBOX[1]}", OK, 1.6, m="ok")
d.chip(400, DIA[1], "exit 0", OK, 11)
d.path(f"M {DIA[0]} {DIA[1]+dy+6} L {ERR[0]} {ERR[1]-38-10}", BAD, 1.6, m="bad")
d.chip(268, 448, "exit 1", BAD, 11)
d.path(f"M {ERR[0]} {ERR[1]+38+6} L {LOOP[0]} {LOOP[1]-32-10}", BAD, 1.6, m="bad")
# 칩은 ERR 밑변(538)과 LOOP 윗변(578) 사이에만 앉을 수 있다 — 556 이 그 한가운데다
d.chip(316, 556, "재시도해도 또 실패", BAD, 11)
d.path(f"M {LOOP[0]+BW//2+6} {LOOP[1]} L {STUCK[0]-160-10} {STUCK[1]}", WARN, 1.6, m="warn")

# 회귀 열은 상자 왼쪽 변(80)보다 왼쪽에 서야 마지막 구간이 오른쪽을 향한다.
# 76 에 두면 74 → 76 → 70 이 되어 화살촉이 상자 반대쪽을 가리킨다.
d.path(f"M {ERR[0]-BW//2-6} {ERR[1]} L 52 {ERR[1]} L 52 {INIT[1]} L {INIT[0]-BW//2-10} {INIT[1]}",
       MUTED, 1.4, m="ar", dash="6 5")
d.t(60, 360, "재시도", 11, MUTED, KR, "start")

d.o.append(f'<circle cx="880" cy="{OKBOX[1]}" r="8" fill="none" stroke="{OK}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="880" cy="{OKBOX[1]}" r="5" fill="{OK}"/>')
d.path(f"M {OKBOX[0]+BW//2+6} {OKBOX[1]} L 868 {OKBOX[1]}", OK, 1.4, m="ok")

d.t(36, 682, "정상 전이는 Init:0/2 → Init:1/2 → PodInitializing → Running 이고, 실패는 "
             "Init:Error → 재시도 → Init:CrashLoopBackOff 다.", 12, MUTED, KR, "start")
d.t(36, 706, "컨테이너가 죽어도 Pod 가 살아 있는 한 로그는 조회된다 — 사인을 찾을 때 먼저 볼 곳이다.",
     12, MUTED, KR, "start")
d.legend(746, [("준비 단계", INFO), ("문이 열린 뒤", OK), ("실패 경로", BAD),
               ("갇힌 주 컨테이너", WARN), ("판정", ACC)])
d.save("05-03-init-fail-flow.svg")
print("ok init-fail-flow")
