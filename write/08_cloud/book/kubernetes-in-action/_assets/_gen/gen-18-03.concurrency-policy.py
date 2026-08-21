# 18-03 §5 — 앞의 것이 아직 돌고 있을 때
# 세 값을 설명으로 나열하면 차이가 뭉갠다. 앞 Job 이 도는 중에 다음 시각이 온 장면을 고정해 두고,
# 그때 무슨 일이 나는지만 갈라야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, RULE, KR, MONO
import ddx

d = D(1240, 768, "KUBERNETES IN ACTION · 18-03",
      "앞의 것이 아직 돌고 있을 때",
      "정해진 시각이 왔는데 이전 Job 이 아직 끝나지 않았다면 셋 중 하나를 한다. 겹쳐 돌리거나, "
      "이번을 건너뛰거나, 앞의 것을 지우고 바꾼다.",
      "01:00 Job 이 02:00 까지 이어질 때")

X = lambda t: 220 + t * 190
def row(y0, label, bars, note, c):
    ddx.band(d, y0, y0 + 172, label, x=24, w=1192)
    for t0, t1, lane, tag, bc in bars:
        y = y0 + 60 + lane * 50
        d.o.append(f'<rect x="{X(t0)}" y="{y}" width="{X(t1)-X(t0)}" height="38" rx="5" '
                   f'fill="{bc}12" stroke="{bc}" stroke-width="1.1"/>')
        d.t((X(t0) + X(t1)) / 2, y + 25, tag, 10, bc, KR)
    d.line(X(2), y0 + 44, X(2), y0 + 160, SOFT, 1.0, "4 4")
    d.t(X(2) + 8, y0 + 158, "02:00", 9, SOFT, MONO, "start")
    d.t(1080, y0 + 90, note, 11, c, KR)

row(100, "Allow — 겹쳐 돌린다", [
    (0, 3.2, 0, "01:00 Job", OK), (2, 4.4, 1, "02:00 Job", OK)],
    "둘이 함께 돈다", OK)
row(292, "Forbid — 건너뛴다", [
    (0, 3.2, 0, "01:00 Job", OK), (2, 2.6, 1, "건너뜀", WARN)],
    "이번 회차가 없다", WARN)
row(484, "Replace — 바꾼다", [
    (0, 2, 0, "01:00 Job — 지워진다", BAD), (2, 4.4, 1, "02:00 Job", ACC)],
    "앞의 것이 중단된다", ACC)

d.t(24, 688, "Allow 는 같은 일이 두 번 겹쳐도 괜찮을 때만 쓴다. 앞의 결과를 덮어쓰는 작업이라면 "
                  "Forbid 나 Replace 가 맞는다.", 11, MUTED, KR, "start")
d.legend(716, [("도는 Job", OK), ("생략", WARN), ("중단·교체", ACC), ("지워지는 것", BAD)])
d.save("18-03-concurrency-policy.svg")
print("ok")
