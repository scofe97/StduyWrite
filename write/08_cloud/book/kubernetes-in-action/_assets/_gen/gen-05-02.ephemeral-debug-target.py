# 05-02 §7 실측 — --target 으로 대상 컨테이너의 프로세스를 본다
# 본문: "--target=kiada 가 디버그 컨테이너(busybox)를 kiada 컨테이너와 같은 PID 네임스페이스에
#        넣어, busybox 의 ps 에 kiada 의 프로세스(MainThread, PID 1)가 그대로 보입니다."
#       "share-demo 에서는 두 컨테이너가 PID 격리라 서로 안 보였지만, 여기서는 --target 으로
#        일부러 공유해 도구 없는 대상을 밖에서 들여다봅니다."
#       "kiada 를 재빌드하거나 재시작하지 않고, 문제가 난 바로 그 컨테이너를 그대로 관찰한다."
# 타입 스펙: type-nested.md — 같은 Pod 안에 무엇이 붙는가가 요점이라 경계 링. 두 컨테이너를
#           잇는 것이 PID 네임스페이스 공유이므로 그 공유 자체를 띠로 그려 실물로 만든다.
#           05-01 은 같은 기능을 격리 쪽으로 썼다 — 그 대비를 오른쪽에 짧게 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 652
d = D(W, H, "KUBERNETES IN ACTION · 05-02",
      "--target 은 PID 네임스페이스를 일부러 공유시킨다",
      "도구가 없는 운영 컨테이너를 재빌드도 재시작도 하지 않고, 도구가 든 임시 컨테이너를 "
      "붙여 같은 PID 네임스페이스에 넣는다. 그러면 대상의 프로세스가 그대로 보인다.",
      lead="05-01 의 PID 격리를 반대 방향으로 쓴 것이다 — 기본은 격리, 디버깅은 공유")

RING = (48, 214, 560, 268)
TARGET, DEBUG = (328, 282), (328, 414)
BW, BH = 460, 88

ddx.band(d, 104, 596, "문제가 난 바로 그 컨테이너를 그대로 관찰한다 — 재생성하면 그 상태가 사라진다")

d.chip(300, 176, "kubectl debug -it <pod> --image=busybox --profile=general --target=kiada", ACC, 11)

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "kiada Pod — 재생성하지 않는다", 11, INFO, off=16)

def box(cx, cy, t, s, tag, c):
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 18, ddx.fit(t, 13, BW - 18, t), 13, c, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, BW - 16, t), 11, MUTED, MONO, "middle")
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, t), 10, SOFT, KR)

box(*TARGET, "대상 — kiada 컨테이너", "PID 1  MainThread", "sh · ps · curl 이 없다 — exec 로는 못 들어간다", WARN)
box(*DEBUG, "디버거 — busybox (임시)", "PID 17  ps", "도구가 들어 있다 — 붙였다 떼면 그만이다", OK)

# 공유 자체를 실물로 — 두 상자를 잇는 띠
d.o.append(f'<rect x="{TARGET[0]-BW//2}" y="{TARGET[1]+BH//2}" width="{BW}" '
           f'height="{DEBUG[1]-BH//2-TARGET[1]-BH//2}" rx="6" fill="{ACC}12" '
           f'stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(TARGET[0], 356, "--target=kiada → 같은 PID 네임스페이스", 11, ACC, MONO)

OUT = (798, 348)
d.box(OUT[0] - 160, OUT[1] - 96, 320, 192, PAPER2, RULE, 1.1, 6)
d.t(OUT[0], OUT[1] - 66, "디버거에서 ps -eo pid,comm", 12, INK, KR, "middle", 600)
for i, (pid, comm, note, c) in enumerate([("1", "MainThread", "대상의 프로세스가 보인다", WARN),
                                          ("17", "ps", "디버거 자신", OK)]):
    y = OUT[1] - 30 + i * 62
    d.t(OUT[0] - 132, y, f"{pid:>3}  {comm}", 12, c, MONO, "start", 600)
    d.t(OUT[0] - 132, y + 20, note, 10, SOFT, KR, "start")
d.path(f"M {TARGET[0]+BW//2+6} {OUT[1]} L {OUT[0]-160-10} {OUT[1]}", ACC, 1.6, m="acc")

d.t(36, 528, "05-01 의 share-demo 는 같은 커널 기능을 격리 쪽으로 썼다 — 두 컨테이너가 서로의 "
             "프로세스를 못 봤다.", 12, MUTED, KR, "start")
d.t(36, 552, "shareProcessNamespace 는 Pod 전체를 다시 만들어야 하지만, --target 은 돌고 있는 "
             "Pod 에 그대로 붙는다.", 12, MUTED, KR, "start")
d.legend(612, [("도구가 없는 대상", WARN), ("도구가 든 디버거", OK), ("일부러 공유시키는 것", ACC)])
d.save("05-02-ephemeral-debug-target.svg")
print("ok ephemeral-debug-target")
