# 06-01 §6 — 이미지 pull 이 실패하면 시도 사이의 대기 창이 두 배씩 길어진다
# 본문: "재시도 간격은 점점 늘어나다 300초에서 멈춥니다" · ErrImagePull 과 ImagePullBackOff 가
#       번갈아 STATUS 칸에 뜬다.
# 타입 스펙: type-gantt.md — 시간축 위의 구간이라 간트 골격을 빌린다(왼쪽 라벨 열 · 구간 막대).
#           막대 길이가 곧 대기 시간이라 1초 = 1.1px 로 비례시킨다. 길이는 kubelet 소스에서
#           계산한 값이고 실측이 아니다 — 처음 10초, 시도마다 두 배, 300초 상한.
# 막대가 가장 좁은 곳(10초 = 11px)의 라벨은 위·아래로 번갈아 놓아 겹치지 않게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 440
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "pull 이 실패하면 다음 시도까지 대기 창이 두 배씩 길어진다",
      "처음 대기 창은 10초이고 시도가 실패할 때마다 두 배가 되어 300초에서 멈춘다. 시도가 실패하는 "
      "순간 reason 은 ErrImagePull 이고, 대기 창 동안에는 ImagePullBackOff 로 바뀐다.",
      lead="같은 이미지를 같은 Pod 가 받는 동안의 대기 창이다 — 새 Pod 는 10초부터 다시 시작한다")

SCALE = 1.1                      # px per second
X0 = 232
WINDOWS = [10, 20, 40, 80, 160, 300]
BAR_Y, BAR_H = 176, 32

ddx.band(d, 104, 380, "reason 이 번갈아 바뀐다 — 실패한 순간은 ErrImagePull, 기다리는 동안은 ImagePullBackOff")

d.t(36, BAR_Y + 21, "waiting.reason", 11, INK, MONO, "start", 600)

t = 0
for i, w in enumerate(WINDOWS):
    x = X0 + round(t * SCALE)
    wpx = round(w * SCALE)
    d.o.append(f'<rect x="{x}" y="{BAR_Y}" width="{wpx}" height="{BAR_H}" '
               f'fill="{WARN}22" stroke="{WARN}" stroke-width="1.0"/>')
    # 시도가 실패하는 순간 — 창 맨 앞의 좁은 막대
    d.o.append(f'<rect x="{x}" y="{BAR_Y}" width="4" height="{BAR_H}" fill="{BAD}"/>')
    cx = x + wpx // 2
    if wpx >= 150:
        d.t(cx, BAR_Y + 21, f"ImagePullBackOff {w}s", 11, WARN, MONO)
    elif wpx >= 40:
        d.t(cx, BAR_Y + 21, f"{w}s", 11, WARN, MONO)
    else:
        # 막대가 좁은 두 창은 위에 위아래로 번갈아 적는다
        d.t(cx, BAR_Y - (12 if i == 0 else 32), f"{w}s", 11, WARN, MONO)
    t += w

# 마지막 시도 뒤에도 300초 간격으로 이어진다
END = X0 + round(t * SCALE)
d.o.append(f'<rect x="{END}" y="{BAR_Y}" width="4" height="{BAR_H}" fill="{BAD}"/>')
d.path(f"M {END+12} {BAR_Y+BAR_H//2} L {END+44} {BAR_Y+BAR_H//2}", WARN, 1.5, m="warn", dash="5 4")
d.t(END + 12, BAR_Y - 12, "300s 반복", 11, WARN, KR, "start")

# 누적 시각 — 간격이 넓은 눈금만 적는다
for sec in (0, 70, 150, 310, 610):
    x = X0 + round(sec * SCALE)
    d.line(x, BAR_Y + BAR_H, x, BAR_Y + BAR_H + 10, SOFT, 0.8)
    d.t(x, BAR_Y + BAR_H + 28, f"{sec}s", 11, SOFT, MONO)
d.t(X0, BAR_Y + BAR_H + 52, "첫 pull 실패", 11, MUTED, KR, "middle")

d.t(36, 314, "대기 창 10·20·40·80·160·300초 — kubelet 소스에서 계산한 값, 실측 아님", 12, MUTED, KR, "start")
d.t(36, 340, "300초 상한 — 소스의 MaxImageBackOff 와 공식 문서가 같은 값", 12, MUTED, KR, "start")
d.legend(396, [("pull 시도 실패 (ErrImagePull)", BAD), ("대기 창 (ImagePullBackOff)", WARN)])
d.save("06-01-image-pull-backoff.svg")
print("ok image-pull-backoff")
