# 08-02 §6 — 밀기(StatsD)와 끌기(스크래핑)는 메트릭이 흐르는 방향과 주소를 아는 쪽이 반대다.
# 1차 자료: StatsD README "port: port to listen for messages on [default: 8125]",
#           예 `echo "foo:1|c" | nc -u -w0 127.0.0.1 8125`.
#           node_exporter README "listens on HTTP port 9100 by default".
# 값: 본문 §8 prometheus.yml 의 scrape_interval 15s, targets ['172.17.0.1:9100'].
# 타입 스펙: type-data-flow — 데이터가 무엇을 타고 어느 방향으로 흐르는지. 화살표 위에 실제로 오가는
#           값, 노드 아래에 대상 주소를 쥔 설정을 적는다. focal 은 방향이 뒤집힌 끌기 쪽 요청 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, RULE, PAPER2, KR, MONO

W, H = 920, 452
NW, NH = 236, 76
LX, RX = 24, W - 24 - NW
Y1, Y2 = 136, 290

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §6",
      "메트릭을 보내는 쪽과 가져가는 쪽",
      "밀기에서는 앱이 수집기 주소를 알고 UDP 로 보낸다. 끌기에서는 앱이 HTTP 엔드포인트를 열어 두고 "
      "Prometheus 가 정해진 간격으로 가져간다.",
      "끌기에서는 대상 주소를 수집기 설정이 쥡니다")


def node(x, y, name, sub, c, focal=False, fam=MONO):
    d.tone(x, y, NW, NH, c, 8, "2E" if focal else "14", 1.4 if focal else 1.1)
    d.t(x + NW / 2, y + 32, name, 14, INK, KR, "middle", 600)
    d.t(x + NW / 2, y + 54, sub, 12, c, fam)


# 밀기
d.t(LX, Y1 - 16, "밀기 · StatsD", 12.5, MUTED, KR, "start", 600)
node(LX, Y1, "앱 + StatsD 클라이언트", "계측 코드", INFO, fam=KR)
node(RX, Y1, "StatsD 서버", "UDP :8125", INFO)
d.arrow([(LX + NW + 6, Y1 + NH / 2), (RX - 8, Y1 + NH / 2)], INFO, "info", 1.6)
d.t((LX + NW + RX) / 2, Y1 + NH / 2 - 12, '"foo:1|c"', 12.5, INFO, MONO, "middle", 600)
d.t((LX + NW + RX) / 2, Y1 + NH / 2 + 22, "UDP · 응답 없음", 11.5, MUTED, KR)
d.t(LX + NW / 2, Y1 + NH + 22, "주소 127.0.0.1:8125 를 앱이 앎", 11.5, SOFT, KR)

# 끌기
d.t(LX, Y2 - 16, "끌기 · 스크래핑", 12.5, MUTED, KR, "start", 600)
node(LX, Y2, "node exporter", "HTTP :9100/metrics", OK)
node(RX, Y2, "Prometheus", "scrape_interval 15s", ACC, True)
d.arrow([(RX - 6, Y2 + 24), (LX + NW + 8, Y2 + 24)], ACC, "acc", 1.6)
d.t((LX + NW + RX) / 2, Y2 + 14, "GET /metrics", 12.5, ACC, MONO, "middle", 600)
d.arrow([(LX + NW + 6, Y2 + NH - 20), (RX - 8, Y2 + NH - 20)], OK, "ok", 1.4, "5 4")
d.t((LX + NW + RX) / 2, Y2 + NH - 2, "200 · 텍스트 메트릭", 11.5, OK, KR)
d.t(RX + NW / 2, Y2 + NH + 22, "targets: ['172.17.0.1:9100']", 11.5, SOFT, MONO)

d.legend(H - 40, [("밀기 경로", INFO), ("끌기 요청", ACC), ("끌기 응답", OK), ("주소를 쥔 쪽", SOFT)])
d.save("08-02.push-pull.svg")
print("ok 08-02.push-pull")
