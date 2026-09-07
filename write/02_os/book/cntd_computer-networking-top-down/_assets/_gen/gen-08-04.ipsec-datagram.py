# 타입 스펙: type-nested — 원래 데이터그램이 안쪽에 통째로 들어가고 바깥에 새 헤더가 씌워진다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.7.4 Figure 8.29 (책 601~603쪽) —
#   조립 순서 여섯, 필드 구성, 주소 172.16.1.17/172.16.2.48 과 200.168.1.100/193.68.2.23,
#   프로토콜 번호 50 은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 656
d = D(W, H, "SECTION 8.7.4 · THE IPSEC DATAGRAM (TUNNEL MODE)",
      "원래 데이터그램이 통째로 안쪽에 들어갑니다",
      "그래서 원래 출발지와 목적지 주소까지 암호화된다. 바깥에서 보이는 것은 터널 양 끝 주소뿐이다.",
      "필드 구성과 주소와 프로토콜 번호 50 은 원문 Figure 8.29 의 것입니다")

d.tone(24, 144, 952, 208, WARN, 10, "08", 1.3)
d.t(44, 172, "새 IP 헤더 — 평문으로 나갑니다", 12, WARN, KR, "start", 600)
d.t(44, 196, "200.168.1.100 → 193.68.2.23 · 프로토콜 번호 50", 11, MUTED, MONO, "start")

d.tone(56, 216, 888, 120, INFO, 8, "10", 1.2)
d.t(76, 244, "페이로드 — 원문이 부르는 이름은 엔칠라다 + MAC", 12, INFO, KR, "start", 600)

INNER = [(88, 128, "ESP 헤더", "SPI · 순서 번호", OK, False),
         (232, 400, "원래 IP 데이터그램", "172.16.1.17 → 172.16.2.48", ACC, True),
         (648, 152, "ESP 트레일러", "패딩 · 패드 길이 · 다음 헤더", ACC, True),
         (816, 112, "ESP 인증", "MAC", OK, False)]
for x, w, name, sub, c, enc in INNER:
    d.tone(x, 264, w, 56, c, 6, "22" if enc else "16", 1.4 if enc else 1.2)
    d.t(x + w / 2, 288, name, 11, c, KR, "middle", 600)
    d.t(x + w / 2, 308, sub, 10, MUTED, MONO if any(ch.isdigit() for ch in sub) else KR)
d.box(224, 256, 584, 72, "none", ACC, 1.3, 6)
d.o[-1] = d.o[-1].replace('stroke-width="1.3"', 'stroke-width="1.3" stroke-dasharray="6 5"')
d.t(516, 344, "이 안쪽만 암호화됩니다", 11, ACC, KR)

PY = 376
d.box(24, PY, 470, 180, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "R1 이 만드는 순서", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 474, PY + 40, RULE, 0.8)
for i, ln in enumerate(["1. 원래 데이터그램 뒤에 ESP 트레일러", "2. 그 결과를 암호화",
                        "3. 앞에 ESP 헤더 — 여기까지가 엔칠라다", "4. 엔칠라다 전체에 MAC 계산",
                        "5. MAC 을 뒤에 붙여 페이로드 완성", "6. 앞에 새 IP 헤더 (보통 20바이트)"]):
    d.t(44, PY + 62 + i * 18, ln, 11, MUTED, KR, "start")

d.tone(514, PY, 462, 180, BAD, 8, "12", 1.3)
d.t(534, PY + 28, "트루디가 아는 것은 이것뿐입니다", 12, BAD, KR, "start", 600)
d.line(534, PY + 40, 956, PY + 40, RULE, 0.8)
for i, ln in enumerate(["200.168.1.100 에서 193.68.2.23 으로 간다는 것.",
                        "", "TCP 인지 UDP 인지 ICMP 인지 모릅니다.",
                        "HTTP 인지 SMTP 인지도 모릅니다.", "",
                        "이 기밀성이 TLS 보다 훨씬 멀리 갑니다."]):
    if ln:
        d.t(534, PY + 62 + i * 18, ln, 11, BAD if i == 5 else MUTED, KR, "start")

d.legend(580, [("평문으로 남는 것", WARN), ("페이로드", INFO), ("암호화되는 것", ACC), ("트루디의 시야", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.ipsec-datagram.svg"
d.save(out); print("→", out.name)
