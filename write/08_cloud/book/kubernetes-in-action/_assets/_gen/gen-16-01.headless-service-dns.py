# 16-01 §3 — 대응표에 줄이 늘어난다
# 본문이 "DNS 의 이름-IP 대응표에 줄이 늘어난다"로 세 단계를 갈라 설명한다. 그러니 구조도가
# 아니라 실제 레코드 줄이 몇 개인지가 보이는 표여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 660, "KUBERNETES IN ACTION · 16-01",
      "이름-IP 대응표에 줄이 늘어난다",
      "보통의 Service 는 줄이 하나뿐이고 그 하나가 가상 IP 를 가리킨다. headless 로 바꾸면 그 줄이 "
      "파드 IP 전부를 가리키고, StatefulSet 과 묶으면 파드마다 줄이 하나씩 더 생긴다.",
      "quiz-pods · clusterIP: None")

def stage(y0, h, label, lines, c, focal):
    ddx.band(d, y0, y0 + h, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    for i, (name, val) in enumerate(lines):
        y = y0 + 56 + i * 26
        d.t(70, y, name, 11, c if i == 0 or focal else MUTED, MONO, "start")
        d.t(700, y, "→", 11, SOFT, MONO)
        d.t(750, y, val, 11, MUTED, MONO, "start")

stage(100, 96, "① 보통의 ClusterIP Service — 줄 하나", [
    ("quiz-pods.kiada.svc.cluster.local", "10.96.0.42        (Service 가상 IP)"),
], INFO, False)

stage(212, 148, "② headless 로 바꾸면 — 같은 줄이 파드 IP 전부를 가리킨다", [
    ("quiz-pods.kiada.svc.cluster.local", "10.244.1.9"),
    ("", "10.244.2.4"),
    ("", "10.244.3.7"),
], INFO, False)

stage(376, 176, "③ StatefulSet 과 묶으면 — 파드마다 줄이 하나씩 더", [
    ("quiz-0.quiz-pods.kiada.svc.cluster.local", "10.244.1.9"),
    ("quiz-1.quiz-pods.kiada.svc.cluster.local", "10.244.2.4"),
    ("quiz-2.quiz-pods.kiada.svc.cluster.local", "10.244.3.7"),
    ("quiz-pods.kiada.svc.cluster.local", "세 IP 전부  (②의 줄도 그대로)"),
], ACC, True)

d.t(24, 596, "③ 의 줄들이 안정된 네트워크 신원이다. 파드가 교체돼도 이름이 같으므로, 다른 멤버와 클라이언트가 "
             "번호로 특정 멤버를 부를 수 있다.", 11, MUTED, KR, "start")
d.legend(618 - 4, [("기존 줄", INFO), ("늘어난 줄", ACC)])
d.save("16-01-headless-service-dns.svg")
print("ok")
