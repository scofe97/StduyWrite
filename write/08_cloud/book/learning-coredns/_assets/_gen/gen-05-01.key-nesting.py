# 05-01 §5 — etcd 키는 도메인 이름과 같은 계층을 반대 방향으로 읽은 것이다.
# 원문 근거: "The format of the key is structured like a Unix directory path, going in the reverse order
#            of the domain name. The root of the path is, by default /skydns, although this is
#            configurable. If we want to make our example service available as the name
#            users.services.example.com, we populate etcd with the JSON object above, at the key
#            /skydns/com/example/services/users."
# 타입 스펙: type-nested — 포함으로 계층을 보이고, 바깥에서 안으로 읽는 순서가 곧 키다.
#           트리를 안 쓴 이유: 원문이 주는 노드가 가지 없는 한 줄이라 트리로 그리면 계보가 아니라 사슬이 된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 880, 632
d = D(W, H, "LEARNING COREDNS · 05-01 §5",
      "같은 계층을 반대로 읽으면 키가 된다",
      "링은 도메인 이름의 레이블이다. 바깥에서 안으로 읽으면 etcd 키가 되고, "
      "안에서 바깥으로 읽으면 도메인 이름이 된다. 값은 가장 안쪽 링에 놓인다.",
      "가장 안쪽 링이 서비스 하나입니다")

rings = [
    (40, 104, 800, 280, "/skydns", "뿌리 · path 옵션으로 바꾼다", False),
    (76, 128, 728, 232, "com", "", False),
    (112, 152, 656, 184, "example", "", False),
    (148, 176, 584, 136, "services", "", False),
    (184, 200, 512, 88, "users", "", True),
]
for x, y, w, h, label, band, focal in rings:
    if focal:
        d.tone(x, y, w, h, ACC, 8, "0E", 1.4)
    else:
        d.box(x, y, w, h, PAPER, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 14}" y="{y - 8}" width="{len(label) * 9 + 20}" height="16" fill="{PAPER}"/>')
    d.t(x + 22, y + 4, label, 12, ACC if focal else SOFT, MONO, "start", 600)
    if band:
        d.t(x + w - 20, y + h - 12, band, 12, MUTED, KR, "end")

d.t(440, 236, "{\"host\": \"192.0.2.10\", \"port\": 20020,", 13, INK, MONO)
d.t(440, 258, "\"priority\": 10, \"weight\": 20}", 13, INK, MONO)
d.t(440, 278, "SkyDNS 메시지 하나가 여기 놓인다", 12, MUTED, KR)

d.path("M 40 412 L 840 412", SOFT, 1.0, m="soft")
d.t(40, 402, "바깥에서 안으로", 12, SOFT, KR, "start")
d.t(440, 444, "/skydns / com / example / services / users", 16, ACC, MONO, "middle", 600)
d.t(440, 466, "etcd 키 — 링을 바깥부터 세면 이 순서다", 13, MUTED, KR)

d.path("M 840 496 L 40 496", SOFT, 1.0, m="soft")
d.t(840, 486, "안에서 바깥으로", 12, SOFT, KR, "end")
d.t(440, 528, "users . services . example . com", 16, INK, MONO, "middle", 600)
d.t(440, 550, "도메인 이름 — 같은 링을 안부터 세면 이 순서다", 13, MUTED, KR)

d.legend(574, [("서비스 하나가 놓이는 링", ACC)])
d.save("05-01.key-nesting.svg")
