# 18-02 §1 — 창의 크기와 채워야 할 횟수
# 두 값이 각각 무엇을 정하는지가 헷갈리는 자리다. 그러니 정의를 적는 대신, 동시 실행 창을
# 고정 폭으로 그려 그 안이 계속 채워지는 장면이어야 한다.
# 타입 스펙: type-gantt.md — 창 둘을 레인으로 두고 파드 다섯을 시간 구간 막대로 놓았다. 하나가 끝난 자리에 다음이
#           들어오는 겹침과 이어짐이 논지이고, 아래 기준선이 공용 시간축이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 18-02",
      "창은 둘, 채워야 할 횟수는 다섯",
      "parallelism 은 동시에 열어 둘 창의 개수를, completions 는 그 창으로 몇 번 성공을 통과시킬지를 "
      "정한다. 하나가 끝나면 그 자리에 다음이 들어온다.",
      "completions 5 · parallelism 2")

SLOTS = [(0, 1.6, 0, "파드 1"), (0, 1.9, 1, "파드 2"),
         (1.7, 3.2, 0, "파드 3"), (2.0, 3.6, 1, "파드 4"),
         (3.3, 4.9, 0, "파드 5")]
X = lambda t: 260 + t * 170
for t0, t1, lane, tag in SLOTS:
    y = 220 + lane * 62
    d.o.append(f'<rect x="{X(t0)}" y="{y}" width="{X(t1)-X(t0)}" height="46" rx="5" '
               f'fill="{OK}12" stroke="{OK}" stroke-width="1.1"/>')
    d.t((X(t0) + X(t1)) / 2, y + 30, tag, 11, OK, KR)
for lane in (0, 1):
    d.t(200, 250 + lane * 62, f"창 {lane+1}", 11, SOFT, KR, "end")
d.o.append(f'<rect x="{X(0)-14}" y="206" width="{X(4.9)-X(0)+28}" height="122" rx="8" '
           f'fill="none" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
d.t(X(2.4), 352, "동시에 둘 — parallelism", 11, ACC, KR)

d.line(X(0), 396, X(4.9), 396, RULE, 1.0)
d.t(X(0), 418, "시작", 10, SOFT, KR)
d.t(X(4.9), 418, "다섯 번째 성공 → 완료", 10, OK, KR)

d.t(24, 486, "창이 비면 그때 다음 파드를 만든다. 그래서 총 파드 수는 completions 와 같고, 동시에 도는 수만 "
             "parallelism 으로 묶인다.", 11, MUTED, KR, "start")
d.t(24, 508, "parallelism 을 completions 보다 크게 잡아도 소용없다 — 채울 횟수가 그만큼 없으므로 남는 창은 비어 있다.",
     11, MUTED, KR, "start")
d.legend(536, [("도는 파드", OK), ("동시 실행 창", ACC)])
d.save("18-02-completions-parallelism.svg")
print("ok")
