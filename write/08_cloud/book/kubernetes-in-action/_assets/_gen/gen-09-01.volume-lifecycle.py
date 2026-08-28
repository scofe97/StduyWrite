# 09-01 §2 — 볼륨은 파드에 속하고 컨테이너는 죽었다 산다
# 본문의 요점은 수명의 층이 다르다는 것이다. 그러니 시간축 위에 컨테이너와 볼륨을 두 레인으로
# 놓아, 한쪽만 끊기고 다른 쪽은 이어지는 것이 보여야 한다.
# 타입 스펙: type-gantt.md — 시간축 위에 컨테이너 레인과 볼륨 레인이 있고, 컨테이너는 세 구간으로 끊기는데 볼륨은
#           한 구간으로 이어진다. 끊김과 이어짐이 막대 모양으로 대조되는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 600, "KUBERNETES IN ACTION · 09-01",
      "끊기는 것과 이어지는 것",
      "컨테이너가 재시작되면 파일시스템은 이미지 상태로 되돌아간다. 볼륨은 파드에 속해 그 재시작을 "
      "넘어 살아남으므로, 남겨야 할 데이터는 볼륨 위에 둔다.",
      "emptyDir 볼륨 · 파드가 사라지면 함께 사라진다")

X = lambda t: 140 + t * 100
d.t(30, 236, "컨테이너", 11, SOFT, KR, "start")
for i, (t0, t1, lab) in enumerate(((0, 3, "1 세대"), (3.4, 7, "2 세대 — 재시작"), (7.4, 10, "3 세대"))):
    d.o.append(f'<rect x="{X(t0)}" y="206" width="{X(t1)-X(t0)}" height="56" rx="6" '
               f'fill="{WARN}12" stroke="{WARN}" stroke-width="1.1"/>')
    d.t((X(t0) + X(t1)) / 2, 240, lab, 11, WARN, KR)
for t in (3.2, 7.2):
    d.t(X(t), 240, "✕", 13, WARN, KR)
d.t(640, 288, "재시작할 때마다 파일시스템이 이미지 상태로 되돌아간다", 11, WARN, KR)

d.t(30, 356, "볼륨", 11, SOFT, KR, "start")
d.o.append(f'<rect x="{X(0)}" y="326" width="{X(10)-X(0)}" height="56" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t((X(0) + X(10)) / 2, 360, "한 번 만들어져 파드가 살아 있는 동안 이어진다", 12, ACC, KR)
d.t(640, 408, "컨테이너 재시작을 넘어 데이터가 남는다", 11, ACC, KR)

d.line(X(0) - 12, 448, X(10) + 12, 448, RULE, 1.0)
d.t(X(0), 470, "파드 시작", 10, SOFT, KR)
d.t(X(10), 470, "파드 삭제", 10, SOFT, KR)

d.t(24, 516, "emptyDir 은 파드가 사라지면 볼륨도 함께 사라진다. 파드보다 오래 남겨야 하는 데이터는 "
             "PersistentVolume 이 맡는다(10 장).", 11, MUTED, KR, "start")
d.legend(540, [("끊기는 수명", WARN), ("이어지는 수명", ACC)])
d.save("09-01-volume-lifecycle.svg")
print("ok")
