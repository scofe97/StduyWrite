# 06-02 §8 — 두 probe 는 같은 엔드포인트를 보면서 정반대로 설정된다
# 본문: "startup probe 는 실패하는 것이 지극히 정상입니다. 실패는 앱이 아직 완전히 시작되지
#        않았다는 뜻일 뿐입니다. 다만 startup probe 도 failureThreshold 에 닿을 만큼 실패하면
#        liveness probe 가 실패한 것처럼 컨테이너가 종료됩니다."
# 타입 스펙: 축이 다섯(언제·주기·허용 실패·허용 시간·실패의 뜻)이고 값이 둘씩이라 비교 행렬.
#           같은 실패라도 뜻이 갈리는 것이 본문의 요점이므로 '실패의 뜻'을 판정 열로 세운다.
#           전환 자체는 첫 열이 이미 말한다 — 화살표를 따로 그리면 축이 둘로 섞인다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 556
d = D(W, H, "KUBERNETES IN ACTION · 06-02",
      "같은 엔드포인트, 정반대의 설정 — 시작은 관대하게 운영은 엄격하게",
      "startup probe 는 10초 × 12회로 앱에 120초를 주고, liveness probe 는 5초 × 2회로 10초 안에 "
      "비정상을 잡는다. 하나의 probe 로는 느린 기동 허용과 빠른 감지를 동시에 만족할 수 없다.",
      lead="startup 의 실패는 정상이고 liveness 의 실패는 재시작이다 — 같은 실패가 뜻이 다르다")

ddx.band(d, 104, 500, "startup 이 성공하는 순간 liveness 로 전환된다 — 그전까지 liveness 는 아예 돌지 않는다")

# 첫 열이 probe 이름을 진다 — 없으면 어느 행이 어느 probe 인지 독자가 추론해야 한다.
# '언제 도는가' 는 그 열의 부제로 합쳐 열 수를 늘리지 않았다.
ddx.matrix(
    d, x0=34, hdr_y=220, row_h=84, gap=12, focal_col=4,
    cols=[(220, "probe · 언제 도는가"), (160, "주기"), (185, "허용 실패"),
          (130, "허용 시간"), (195, "실패의 뜻")],
    rows=[
        ([("startupProbe", "컨테이너 시작부터"), ("10초마다", "periodSeconds: 10"),
          ("12회까지", "failureThreshold: 12"), ("120초", "10 × 12"),
          ("정상이다", "아직 뜨는 중일 뿐")], INFO),
        ([("livenessProbe", "startup 성공 후"), ("5초마다", "periodSeconds: 5"),
          ("2회 연속", "failureThreshold: 2"), ("10초", "5 × 2"),
          ("재시작", "컨테이너를 종료한다")], WARN),
    ])

d.t(36, 456, "다만 startup 도 12회를 다 쓰면 liveness 가 실패한 것처럼 컨테이너가 종료된다 — "
             "관대한 것은 예산 안에서만이다.", 12, MUTED, KR, "start")
d.t(36, 476, "startup·liveness 모두 httpGet 대신 exec 나 tcpSocket 으로도 설정할 수 있다.",
     12, MUTED, KR, "start")
d.legend(516, [("시작 구간 — 관대", INFO), ("정상 운영 구간 — 엄격", WARN)])
d.save("06-02-startup-liveness-probe.svg")
print("ok startup-liveness-probe")
