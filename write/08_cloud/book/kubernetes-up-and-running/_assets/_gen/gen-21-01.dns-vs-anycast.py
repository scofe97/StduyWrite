# 21-01 §사용자는 DNS 부터 도착합니다
# 본문이 둘을 비교하되 축이 하나로 모인다 — *장애 때 트래픽을 옮길 수 있는가*.
# 그러니 기능 대조표를 그리면 안 되고, "정상일 때" 와 "장애일 때" 를 세로로 갈라
# 정상에서는 둘이 비슷하고 장애에서 갈리는 것이 형태로 보이게 한다.
# GeoDNS 의 두 단점은 본문이 이름 붙인 그대로(캐싱·오판) 옮긴다.
# ⚠ 초판은 anycast 칸에 "광고를 내리면 경로가 바뀐다 — 캐시가 끼지 않는다" 라고 적었다가
#   적대적 검증에서 반증됐다. 원서의 anycast 서술은 성질과 "대체로 낫다" 까지이고
#   BGP 광고 철회나 캐시 면역은 한 줄도 없다. 빈칸을 지어 채우지 않고 비었다고 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 612
d = D(W, H, "KUBERNETES UP AND RUNNING · 21-01",
      "정상일 때는 비슷하고 장애일 때 갈린다",
      "DNS 로 가르면 조회 결과가 인터넷 곳곳에 캐시된다. 정상 운영에서는 문제가 아니지만 "
      "트래픽을 급히 옮겨야 할 때 장애를 길게 만든다.",
      "원서 21장 — anycast 가 대체로 낫지만 모든 환경에서 쓸 수 있는 것은 아니다")

# 오른쪽 열이 캔버스 끝(W)에 딱 붙으면 anchor=end 텍스트가 잘린다.
# 오버플로 검사기는 x==W 를 넘침으로 안 보므로 눈으로만 잡힌다. 다른 도식과 같은
# 오른쪽 여백(W-48)에 맞춘다.
LW, RW = 570, 570
LX, RX = 24, 622
Y0 = 128
ROWS = [("무엇으로 가르나", 0), ("정상 운영", 1), ("장애 때 옮기려면", 2), ("자주 틀리는 곳", 3)]
RH, GAP = 84, 10

SIDES = [
    (LX, LW, "GeoDNS", "DNS 조회가 위치를 고른다", WARN, [
        ("클라이언트 IP 로 추측한 물리적 위치", MUTED),
        ("DNS 는 대체로 안정적이라 문제 없다", OK),
        ("캐시가 남아 장애가 길어진다 — TTL 을 무시하는 곳이 많다", BAD),
        ("여러 지역이 같은 방화벽 IP 로 나가면 위치를 틀린다", BAD)]),
    (RX, RW, "anycast", "라우팅이 위치를 고른다", OK, [
        ("정적 IP 하나를 여러 위치에서 광고", MUTED),
        ("네트워크 성능 기준으로 가까운 곳", OK),
        ("원서는 여기까지 적지 않는다 — 대체로 낫다고만 한다", SOFT),
        ("모든 환경에서 쓸 수 있는 것은 아니다", WARN)]),
]
for i, (label, _) in enumerate(ROWS):
    d.t(24, Y0 + i * (RH + GAP) - 6, label, 9, SOFT, KR, "start")

for x, w, name, sub, hc, cells in SIDES:
    d.t(x, Y0 - 26, name, 14, hc, KR, "start", 600)
    d.t(x + w, Y0 - 26, sub, 10, SOFT, KR, "end")
    for i, (txt, c) in enumerate(cells):
        y = Y0 + i * (RH + GAP)
        focal = (i == 2)
        if focal:
            d.tone(x, y, w, RH - 22, c, 6, "12", 1.4)
        else:
            d.box(x, y, w, RH - 22, PAPER2, RULE, 0.9, 6)
        d.t(x + 18, y + 38, ddx.fit(txt, 12, w - 36, txt), 12, c, KR, "start",
            600 if focal else 400)

BY = Y0 + 4 * (RH + GAP) - 14
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "어느 쪽을 골라도 결과는 같은 모양으로 수렴한다 — 전역 DNS 엔드포인트가 "
                 "리전별 IP 모음으로 매핑되고, 그 IP 는 대개 Service 나 Ingress 의 것이다.",
    11, MUTED, KR, "start")
d.t(24, BY + 46, "웹 애플리케이션이라면 여기에 더해 HTTP 계층에서 가를지 정한다. "
                 "프로토콜을 아는 분산기는 쿠키를 보고 요청 단위로 판단한다.", 11, MUTED, KR, "start")
d.legend(BY + 62, [("갈리는 자리", BAD), ("유리한 쪽", OK), ("치러야 할 것", WARN),
                   ("원서가 말하지 않는 것", SOFT)])
d.save("../21-01.dns-vs-anycast.svg")
print("필요 h:", BY + 62 + 48, "· 실제:", H)
