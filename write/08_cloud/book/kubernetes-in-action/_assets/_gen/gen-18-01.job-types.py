# 18-01 §2 — 세 실행 방식이 완료에 이르는 길
# 캡션이 "각각 완료에 이르는 경로"라 한다. 그러니 유형 이름만 늘어놓지 말고 파드가 몇 개
# 언제 도는지가 시간 위에 보여야 한다.
# 타입 스펙: type-gantt.md — 세 밴드가 같은 시간축을 공유하고 파드마다 구간 막대가 놓인다. 병렬 밴드에서 두 막대가
#           겹치는 것이 논지라, 시간 겹침을 보이는 gantt 계약에 맞는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 744, "KUBERNETES IN ACTION · 18-01",
      "몇 개가 언제 도는가",
      "completions 와 parallelism 두 값이 실행 모양을 만든다. 하나도 안 적으면 파드 하나, "
      "completions 만 적으면 순차, 둘 다 적으면 병렬이 된다.",
      "완료 조건은 셋 다 같다 — 성공 횟수를 채우는 것")

def row(y0, label, spec, slots, c, focal):
    ddx.band(d, y0, y0 + 168, label, x=24, w=1192, focal=focal, bar=ACC if focal else None)
    d.t(160, y0 + 56, spec, 10, c, MONO)
    for (t0, t1, lane, tag) in slots:
        x0 = 360 + t0 * 150
        x1 = 360 + t1 * 150
        y = y0 + 72 + lane * 46
        d.o.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="36" rx="5" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
        d.t((x0 + x1) / 2, y + 24, tag, 10, c, KR)
    d.t(1130, y0 + 96, "완료", 11, OK, KR)

row(100, "단일 파드", "completions 없음", [(0, 2, 0, "파드 1")], INFO, False)
row(292, "순차 다중 — completions 3", "parallelism 없음(=1)",
    [(0, 1.6, 0, "파드 1"), (1.7, 3.3, 0, "파드 2"), (3.4, 5, 0, "파드 3")], INFO, False)
row(484, "병렬 다중 — completions 3 · parallelism 2", "동시에 둘씩",
    [(0, 1.6, 0, "파드 1"), (0, 1.8, 1, "파드 2"), (1.7, 3.3, 0, "파드 3")], ACC, True)

d.t(24, 672, "셋 다 성공 횟수를 채우면 끝난다. 다른 것은 그 횟수를 채우는 데 파드를 몇 개 쓰고 "
                 "동시에 몇 개를 돌리느냐다.", 11, MUTED, KR, "start")
d.legend(696, [("도는 파드", INFO), ("동시에 도는 창", ACC), ("완료", OK)])
d.save("18-01-job-types.svg")
print("ok")
