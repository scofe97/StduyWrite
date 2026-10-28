# 02-02 §4 — 정렬한 응답 시간 위의 백분위 사다리. 본문의 예시 수치(p50 200ms, p95 1.5초, SLO p99 1초 미만)와 Amazon 문장만 쓴다.
# 옛 도식의 큐잉 곡선, 메타스테이블 실패, 응답 시간 분해, 평균 비판 두 줄, SLO/SLA 줄은 뺐다. 각각 §1~§3·§5 본문이 맡는다.
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
AY = 216
XS = [80, 264, 448, 632, 816]
LEG = 340
H = LEG + 56

d = D(W, H, "02-02 · PERCENTILE", "백분위로 보는 응답 시간",
      "응답 시간을 빠른 것부터 정렬하면 p50은 중앙값이고, p95·p99·p999·p9999로 갈수록 더 느린 쪽의 드문 요청을 가리킨다. 높은 백분위가 꼬리 지연이다.",
      "빠른 요청부터 정렬한 응답 시간 위의 위치")

d.t(16, 156, "빠른 순으로 정렬한 응답 시간", 12, MUTED, KR, "start")
d.line(264, 124, 816, 124, ACC, 1.4)
d.line(264, 124, 264, 136, ACC, 1.4)
d.line(816, 124, 816, 136, ACC, 1.4)
d.t(540, 112, "꼬리 지연 (tail latency)", 13, ACC, KR, "middle", 600)

d.arrow([(16, AY), (860, AY)], MUTED, "ar", 1.6)
NAMES = [("p50", "중앙값", "절반은 이 시간 미만", "예: 200ms"),
         ("p95", "100개 중 5개", "이 시간 이상", "예: 1.5초"),
         ("p99", "100개 중 1개", "이 시간 이상", "SLO 예: 1초 미만"),
         ("p999", "1,000건 중 1건", "Amazon 서비스 요구", ""),
         ("p9999", "10,000건 중 1건", "최적화 이득 작음", "")]
for x, (p, a, b, c) in zip(XS, NAMES):
    d.o.append(f'<circle cx="{x}" cy="{AY}" r="6" fill="{PAPER2}" stroke="{INFO}" stroke-width="1.4"/>')
    d.t(x, AY - 20, p, 16, INK, MONO, "middle", 600)
    d.t(x, AY + 40, a, 13, INK, KR)
    d.t(x, AY + 62, b, 12, MUTED, KR)
    if c:
        d.t(x, AY + 84, c, 12, MUTED, KR)

d.legend(LEG, [("꼬리 지연 구간", ACC), ("백분위 위치", INFO)])
d.save("02-02.latency-percentiles.svg")
