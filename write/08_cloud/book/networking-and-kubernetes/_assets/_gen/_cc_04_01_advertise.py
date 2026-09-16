"""04-01 광고 주소 짝 도식 공용 골격 — docker 와 k8s 가 같은 레인·같은 stride 를 쓴다.
두 장이 갈리는 값은 노드 레인의 '주소를 갈아 끼우는 자리'가 있느냐 하나다.
좌표: 레인 x 는 Seq.lanes 공식(24 + lane_w/2 + span·i/(n-1))을 4의 배수로 반올림한 값,
메시지 stride 는 72."""
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 468
LANE_W, LANE_Y, LANE_H = 216, 104, 56
LX = [136, 488, 840]                  # 클라이언트 · 노드 · 브로커
Y1, STRIDE = 220, 72                  # 메시지 1·2·3 의 y
RAIL_END = Y1 + 2 * STRIDE + 44
LEG_Y = 420


def lane(d, cx, title, sub, c=None):
    d.box(cx - LANE_W // 2, LANE_Y, LANE_W, LANE_H, PAPER2, c or RULE, 1.0, 6)
    d.t(cx, LANE_Y + 24, ddx.fit(title, 13, LANE_W - 16, title), 13, c or INK, KR, "middle", 600)
    mono = all(ord(ch) < 128 for ch in sub)
    d.t(cx, LANE_Y + 44, ddx.fit(sub, 12, LANE_W - 16, sub), 12, MUTED, MONO if mono else KR)


def label(d, x, y, head, sub, c):
    d.t(x, y - 12, head, 12, c, KR, "middle", 600)
    if sub: d.t(x, y + 22, sub, 12, MUTED, KR)


def draw(kind):
    docker = kind == "docker"
    if docker:
        d = D(W, H, "DOCKER · PORT MAPPING · THE SECOND CONNECTION FAILS",
              "Docker 에서는 앱이 말한 주소로 다시 붙을 수 없다",
              "포트 매핑 뒤의 Kafka 브로커는 자기를 172.17.0.5 로 보지만 그 주소는 노드 안에서만 유효해, "
              "브로커가 광고한 주소로 클라이언트가 다시 붙는 세 번째 단계가 실패한다.",
              lead="사람이 적은 주소로 붙는 1번은 되고, 앱이 말한 주소로 붙는 3번은 안 된다")
        lanes = [("클라이언트", "다른 호스트"), ("노드", "192.168.1.20"),
                 ("Kafka 브로커 컨테이너", "172.17.0.5:9092")]
    else:
        d = D(W, H, "KUBERNETES · IP-PER-POD · ALL THREE STEPS SUCCEED",
              "Kubernetes 에서는 앱이 말한 주소가 그대로 통한다",
              "Pod IP 는 eth0 에 붙은 진짜 주소이고 CNI 가 노드마다 경로를 깔아 두어, "
              "브로커가 광고한 주소로 클라이언트가 다시 붙는 세 번째 단계도 성공한다.",
              lead="주소를 갈아 끼우는 자리가 없어 1번이 쓴 주소와 2번이 말한 주소가 같다")
        lanes = [("클라이언트 Pod", "10.1.7.2 · 노드 2"), ("노드 1", "10.1.3.0/24"),
                 ("Kafka 브로커 Pod", "10.1.3.7:9092")]

    for cx, (t, s) in zip(LX, lanes):
        lane(d, cx, t, s)
    for cx in LX:
        d.line(cx, LANE_Y + LANE_H + 6, cx, RAIL_END, RULE, 1.0, "3 6")

    C, N, B = LX
    y1, y2, y3 = Y1, Y1 + STRIDE, Y1 + 2 * STRIDE
    TW, TH = 128, 32                      # 노드 레인 위 태그

    # 1 — 사람이 적어 준 주소로 접속
    if docker:
        d.tone(N - TW // 2, y1 - TH // 2, TW, TH, ACC, 5, "14", 1.4)
        d.t(N, y1 + 5, "31000 → 9092", 12, ACC, MONO, "middle", 600)
        d.arrow([(C + 10, y1), (N - TW // 2 - 8, y1)], OK, "ok", 1.5)
        d.arrow([(N + TW // 2 + 8, y1), (B - 12, y1)], OK, "ok", 1.5)
        label(d, (C + N - TW // 2) // 2, y1, "1 · 192.168.1.20:31000", "사람이 설정에 적은 주소", OK)
        d.t((N + TW // 2 + B) // 2, y1 - 12, "포트 매핑", 12, ACC, KR, "middle", 600)
    else:
        d.box(N - TW // 2, y1 - TH // 2, TW, TH, PAPER, RULE, 0.9, 5)
        d.t(N, y1 + 5, "경로만", 12, MUTED, KR, "middle")
        d.arrow([(C + 10, y1), (N - TW // 2 - 8, y1)], OK, "ok", 1.5)
        d.arrow([(N + TW // 2 + 8, y1), (B - 12, y1)], OK, "ok", 1.5)
        label(d, (C + N - TW // 2) // 2, y1, "1 · 10.1.3.7:9092", "CNI 가 깐 경로", OK)
        d.t((N + TW // 2 + B) // 2, y1 - 12, "주소 그대로", 12, MUTED, KR, "middle", 600)

    # 2 — 브로커가 자기 주소를 광고 (return: dashed)
    adv = "172.17.0.5:9092" if docker else "10.1.3.7:9092"
    d.arrow([(B - 10, y2), (C + 12, y2)], INFO, "info", 1.5, "6 5")
    # 라벨은 노드 레인의 점선을 비껴 왼쪽 구간 가운데에 둔다
    label(d, (C + N) // 2, y2, "2 · 광고 주소 " + adv,
          "컨테이너 안에서 본 값" if docker else "1번이 쓴 주소와 같은 값", INFO)

    # 3 — 받은 주소로 다시 접속
    if docker:
        stop = N - 40
        d.path(f"M {C+10} {y3} L {stop-16} {y3}", BAD, 1.5, dash="6 5")
        d.line(stop - 8, y3 - 8, stop + 8, y3 + 8, BAD, 2.0)
        d.line(stop - 8, y3 + 8, stop + 8, y3 - 8, BAD, 2.0)
        label(d, (C + stop) // 2, y3, "3 · 172.17.0.5:9092", "타임아웃 · 밖에 없는 주소", BAD)
        legend = [("닿는 요청", OK), ("광고 주소", INFO), ("닿지 않는 요청", BAD), ("주소를 갈아 끼우는 자리", ACC)]
    else:
        d.arrow([(C + 10, y3), (B - 12, y3)], ACC, "acc", 1.7)
        label(d, (C + N) // 2, y3, "3 · 받은 주소로 다시 접속", "그대로 성공", ACC)
        legend = [("닿는 요청", OK), ("광고 주소", INFO), ("받은 주소로 성공", ACC)]

    d.legend(LEG_Y, legend)
    return d
