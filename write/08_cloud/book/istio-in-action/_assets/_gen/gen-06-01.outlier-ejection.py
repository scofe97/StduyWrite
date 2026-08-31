# 06-01 §8 엔드포인트가 축출되고 돌아오는 상태 전이.
# 본문: "색이 붙은 전이가 저자가 설명한 곱셈. 엔드포인트가 축출되면 n × baseEjectionTime 동안 빠져 있고,
# n 은 그 엔드포인트가 축출된 횟수다. 시간이 지나면 로드밸런싱 풀로 돌아온다."
# 타입 스펙: type-state — 주체 하나(엔드포인트)의 상태 전이. 시작점 · 상태 셋 · 전이 라벨은 event [guard] 형태.
#           검사 주기 사이에 요청이 새는 구간을 자기 루프로 둔다. 긴 필드 이름은 전이 라벨이 아니라
#           상태 상자 안에 두어 라벨이 상자를 걸터앉지 않게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1180, 484
d = D(W, H, "ISTIO IN ACTION · 06-01 §8",
      "엔드포인트가 축출되고 돌아오는 상태 전이",
      "연속 5xx 가 임계에 닿으면 다음 검사 주기에 엔드포인트가 축출된다. 축출 시간은 축출 횟수 n 에 baseEjectionTime 을 곱한 값이고, "
      "그 시간이 지나면 로드밸런싱 풀로 돌아온다. 검사 주기 사이에는 요청이 계속 아픈 엔드포인트에 닿는다.",
      "이상치 감지는 실패를 사후에 알아채는 장치입니다. 그 틈을 재시도가 메웁니다")

SW, SH, Y = 240, 72, 176
xs = [64, 470, 876]
states = [("풀에 있음", "요청을 받는다", OK, False),
          ("아프지만 아직 풀에", "consecutive5xxErrors 누적", WARN, False),
          ("축출됨", "n × baseEjectionTime", BAD, True)]
d.o.append(f'<circle cx="24" cy="{Y + SH / 2}" r="6" fill="{INK}"/>')
d.path(f"M 30 {Y + SH / 2} L {xs[0] - 2} {Y + SH / 2}", MUTED, 1.4, m="ar")
for i, (name, sub, c, focal) in enumerate(states):
    x = xs[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{SW}" height="{SH}" rx="8" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + SW / 2, Y + 30, name, 14, ACC if focal else c, KR, "middle", 600)
    d.t(x + SW / 2, Y + 52, sub, 11, MUTED, MONO)
    if i < 2:
        d.path(f"M {x + SW} {Y + SH / 2} L {xs[i + 1] - 2} {Y + SH / 2}", MUTED, 1.4, m="ar")
d.t((xs[0] + SW + xs[1]) / 2, Y + SH / 2 - 32, "연속 5xx", 11, SOFT, KR)
d.t((xs[0] + SW + xs[1]) / 2, Y + SH / 2 - 18, "임계 도달", 11, SOFT, KR)
d.t((xs[1] + SW + xs[2]) / 2, Y + SH / 2 - 32, "[interval 검사]", 11, SOFT, MONO)
d.t((xs[1] + SW + xs[2]) / 2, Y + SH / 2 - 18, "/ 풀에서 뺀다", 11, SOFT, KR)
d.path(f"M {xs[1] + 56} {Y} L {xs[1] + 56} {Y - 48} L {xs[1] + SW - 56} {Y - 48} L {xs[1] + SW - 56} {Y - 2}", WARN, 1.2, m="warn")
d.t(xs[1] + SW / 2, Y - 58, "이 구간의 요청은 아픈 엔드포인트에 닿는다", 11, WARN, KR)
d.path(f"M {xs[2] + SW / 2} {Y + SH} L {xs[2] + SW / 2} {Y + SH + 56} L {xs[0] + SW / 2} {Y + SH + 56} L {xs[0] + SW / 2} {Y + SH + 2}", ACC, 1.4, m="acc")
d.t((xs[0] + xs[2] + SW) / 2, Y + SH + 76, "n × baseEjectionTime 경과 / 로드밸런싱 풀로 복귀 — n 은 축출된 횟수", 12, ACC, KR)
d.t(xs[0], Y + SH + 100, "maxEjectionPercent 가 풀에서 뺄 수 있는 비율의 상한입니다. 전부 빼면 회로가 열린 셈이 됩니다", 12, SOFT, KR, "start")
d.legend(420, [("정상", OK), ("검사 전 · 요청이 샌다", WARN), ("축출", BAD), ("이 절의 논점", ACC)])
d.save("06-01.outlier-ejection.svg")
