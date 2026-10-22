# 타입 스펙: type-flowchart — 세 번의 시도가 명령 → 결과 → 원인 세 줄로 이어지고, 앞의 두 시도는 막다른 길(Cannot fork · ps 누수)이며 그 원인이 다음 시도에서 더하는 것을 정한다. focal 은 두 번째 원인(ps 는 /proc 을 읽음).
# 사실 출처: 노트 L120~L130(--pid, Cannot fork, sh 는 sudo 의 자식), L136~L146(--fork, ps 누수, /proc), L200~L216(unshare --pid --fork chroot alpine sh, mount -t proc proc /proc).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 596
BW = 240
XS = [36, 372, 708]
STEP_Y, STEP_H = 112, 116
RES_Y, RES_H = 264, 104
WHY_Y, WHY_H = 404, 84


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 04-01 §3",
      "PID namespace 는 두 번 실패한 원인을 하나씩 메워야 온전히 동작합니다",
      "첫 시도 sudo unshare --pid sh 는 첫 whoami 만 되고 이후 Cannot fork 가 난다. 원인은 sh 가 sudo 의 자식이라는 것이고 --fork 로 고친다. "
      "둘째 시도는 명령은 되지만 ps 가 호스트 프로세스 전체를 보여 준다. 원인은 ps 가 /proc 을 읽는다는 것이고 루트를 바꿔 별도 /proc 을 마운트한다. "
      "셋째 시도는 unshare --pid --fork chroot alpine sh 뒤 mount -t proc proc /proc 로 ps 가 자기 프로세스만 보여 준다.",
      lead="두 번의 실패는 막다른 길이 아니라, 각각 다음 시도가 더할 것을 알려 주는 단서입니다.")

# 시도 상자: (제목, 명령 줄들)
STEPS = [
    ("첫 시도", ["sudo unshare --pid sh", "whoami", "whoami"]),
    ("두 번째 시도", ["sudo unshare --pid --fork sh", "ps"]),
    ("세 번째 시도", ["sudo unshare --pid --fork", "chroot alpine sh", "mount -t proc proc /proc"]),
]
# 결과: (색, 제목, 부제 둘)
RESULTS = [
    (BAD, "Cannot fork", MONO, ["첫 whoami 만 동작", "PID 가 1부터 다시 시작"]),
    (WARN, "ps 가 호스트 전체 출력", KR, ["Cannot fork 는 사라짐", "sh 는 unshare 의 자식"]),
    (OK, "ps 가 자기 프로세스만 출력", KR, ["PID namespace + 별도 /proc", "세 가지를 겹친 결과"]),
]
# 원인: (색, 태그, 제목, 부제)
WHYS = [
    (None, "원인", "sh 는 sudo 의 자식", "--fork 로 unshare 의 자식으로"),
    (ACC, "원인", "ps 는 /proc 을 읽음", "별도 /proc 이 필요 → 루트를 바꿈"),
    (None, "결론", "장치 셋을 겹침", "PID namespace · 새 루트 · proc"),
]

# 화살표를 상자보다 먼저
mid = STEP_Y + STEP_H // 2
for a, b in ((0, 1), (1, 2)):
    d.arrow([(XS[a] + BW + 2, mid), (XS[b] - 4, mid)], SOFT, "soft", 1.3)
d.t((XS[0] + BW + XS[1]) / 2, mid - 10, "+ --fork", 12, MUTED, MONO, "middle", 600)
d.t((XS[1] + BW + XS[2]) / 2, mid - 26, "+ chroot", 12, MUTED, MONO, "middle", 600)
d.t((XS[1] + BW + XS[2]) / 2, mid - 10, "+ /proc", 12, MUTED, MONO, "middle", 600)
for x in XS:
    cx = x + BW // 2
    d.arrow([(cx, STEP_Y + STEP_H + 2), (cx, RES_Y - 4)], SOFT, "soft", 1.3)
    d.arrow([(cx, RES_Y + RES_H + 2), (cx, WHY_Y - 4)], SOFT, "soft", 1.3)

for k, x in enumerate(XS):
    title, cmds = STEPS[k]
    d.box(x, STEP_Y, BW, STEP_H)
    d.t(x + 16, STEP_Y + 24, str(k + 1), 11, SOFT, MONO, "start")
    d.t(x + BW / 2, STEP_Y + 28, title, 13, INK, KR, "middle", 600)
    for n, c in enumerate(cmds):
        fit(c, 12, BW - 16)
        d.t(x + BW / 2, STEP_Y + 56 + n * 20, c, 12, INFO, MONO, "middle")

    col, rt, rfam, subs = RESULTS[k]
    d.tone(x, RES_Y, BW, RES_H, col, 6, "14", 1.2)
    d.t(x + 16, RES_Y + 22, "결과", 12, SOFT, KR, "start")
    fit(rt, 14, BW - 16)
    d.t(x + BW / 2, RES_Y + 46, rt, 14, col, rfam, "middle", 600)
    for n, s in enumerate(subs):
        fit(s, 12, BW - 16)
        d.t(x + BW / 2, RES_Y + 68 + n * 18, s, 12, MUTED, kr(s), "middle")

    col, tag, wt, ws = WHYS[k]
    if col:
        d.tone(x, WHY_Y, BW, WHY_H, col, 6, "14", 1.4)
    else:
        d.box(x, WHY_Y, BW, WHY_H)
    d.t(x + 16, WHY_Y + 22, tag, 12, SOFT, KR, "start")
    fit(wt, 13, BW - 16)
    fit(ws, 12, BW - 16)
    d.t(x + BW / 2, WHY_Y + 46, wt, 13, col or INK, kr(wt), "middle", 600)
    d.t(x + BW / 2, WHY_Y + 68, ws, 12, MUTED, kr(ws), "middle")

d.legend(524, [("실패", BAD), ("누수", WARN), ("핵심 접점", ACC), ("성공", OK), ("명령", INFO)])
d.save(str(ASSETS / "04-01.pid-namespace-steps.svg"))
print("ok 04-01 pid-namespace-steps")
