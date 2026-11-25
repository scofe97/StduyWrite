# 04-01 §5 TCP 와 SNI 패스스루에서 무엇을 보고 길을 고르는가.
# 본문 요구: 평문 TCP 는 호스트 단서가 없어 VirtualService tcp: 에서 포트로만 매칭하고 L7 기능을 잃는다.
#           SNI 패스스루는 ClientHello 의 SNI 만 읽고 TLS 를 종료하지 않은 채 tls: sniHosts 로 매칭해 백엔드로 보낸다.
# 값 근거: 04-01 §5 및 ch04.txt 4.4.1~4.4.2 (31400, protocol: TCP, hosts: "*", tcp-echo-service:2701,
#           protocol: TLS, tls.mode: PASSTHROUGH, sniHosts, simple-tls-service-1/2).
# 타입 스펙: type-flowchart — 위->아래 분기 흐름(타원 시작/끝, 마름모 판단, 직사각형 처리, 1개 코랄 focal).
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, WARN, PAPER2, KR, MONO

W, H = 900, 628


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "FLOWCHART · 04-01 §5",
      "TCP와 SNI 패스스루 — 무엇을 보고 길을 고르는가",
      "31400 포트로 들어온 비-HTTP 연결이 Gateway 프로토콜 설정에 따라 두 갈래로 나뉜다. "
      "평문 TCP는 포트로만 매칭하고, TLS PASSTHROUGH는 SNI만 읽어 암호화를 유지한 채 백엔드로 보낸다.",
      lead="시작과 끝은 타원, 분기는 마름모, 처리는 사각형이며 코랄은 TLS를 종료하지 않고 넘기는 SNI 패스스루 경로입니다.")

CX = 450
LX, RX = 228, 672
BW, BH = 296, 64


def oval(cx, cy, w, h, title, sub, c, op="14"):
    d.o.append(f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="20" fill="{c}{op}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - 2, title, 14, c if c != MUTED else INK, kr(title), "middle", 600)
    d.t(cx, cy + 16, sub, 13, MUTED, kr(sub), "middle")


def step(cx, cy, title, sub, c, op="14"):
    d.tone(cx - BW/2, cy - BH/2, BW, BH, c, 6, op, 1.3 if c == ACC else 1.1)
    d.t(cx, cy - 4, title, 14, c if c != MUTED else INK, kr(title), "middle", 600)
    d.t(cx, cy + 16, sub, 13, MUTED, kr(sub), "middle")


def diamond(cx, cy, rx, ry, title, sub):
    pts = f"{cx},{cy - ry} {cx + rx},{cy} {cx},{cy + ry} {cx - rx},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{INK}" stroke-width="1.2"/>')
    d.t(cx, cy - 4, title, 14, INK, kr(title), "middle", 600)
    d.t(cx, cy + 16, sub, 13, MUTED, kr(sub), "middle")


# 시작 타원
oval(CX, 128, 296, 56, "비-HTTP TCP 연결 도착", "클러스터 밖 → 게이트웨이 :31400", INFO)

# 판단 마름모
diamond(CX, 232, 136, 44, "Gateway protocol", "31400 포트 프로토콜 선언")
d.arrow([(CX, 156), (CX, 186)], INFO, "info", 1.4)

# 왼쪽 갈래: 평문 TCP
step(LX, 336, "호스트 단서 없음 · hosts: \"*\"", "프로토콜 미인식 · 재시도·서킷 브레이킹 불가", WARN)
step(LX, 432, "VirtualService tcp: 매칭", "들어온 포트 31400으로만 목적지 결정", WARN)
oval(LX, 524, 296, 56, "tcp-echo-service:2701", "평문 TCP 그대로 echo 응답", WARN)

# 오른쪽 갈래: SNI 패스스루 (코랄 focal)
step(RX, 336, "Gateway · tls.mode: PASSTHROUGH", "ClientHello SNI만 읽음 · 인증서 불필요", ACC, op="1e")
step(RX, 432, "VirtualService tls: 매칭", "port: 31400 + sniHosts 호스트 비교", OK)
oval(RX, 524, 296, 56, "simple-tls-service-1 / 2", "TLS 유지 통과 → 백엔드가 직접 종료", OK)

# 마름모 -> 좌우 갈래 (직교)
d.arrow([(CX - 136, 232), (LX, 232), (LX, 302)], WARN, "warn", 1.4)
d.t(LX + 56, 222, "protocol: TCP", 12, WARN, MONO, "middle", 600)

d.arrow([(CX + 136, 232), (RX, 232), (RX, 302)], ACC, "acc", 1.5)
d.t(RX - 56, 222, "protocol: TLS", 12, ACC, MONO, "middle", 600)

# 수직 흐름 화살표
d.arrow([(LX, 368), (LX, 398)], WARN, "warn", 1.4)
d.arrow([(LX, 464), (LX, 494)], WARN, "warn", 1.4)

d.arrow([(RX, 368), (RX, 398)], ACC, "acc", 1.4)
d.arrow([(RX, 464), (RX, 494)], OK, "ok", 1.4)

d.legend(H - 42, [
    ("진입 연결", INFO),
    ("평문 TCP(L7 포기)", WARN),
    ("SNI 패스스루(핵심)", ACC),
    ("백엔드 TLS 유지", OK),
])
d.save("04-01.tcp-sni-passthrough.svg")
print("ok 04-01 tcp-sni-passthrough")
