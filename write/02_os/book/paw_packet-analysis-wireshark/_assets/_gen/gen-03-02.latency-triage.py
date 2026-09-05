# 03-02 §4 — 느릴 때 네트워크인지 애플리케이션인지 가르는 순서. 원문의 지연 원인 목록과
# slow_download.pcap 진단 절차를 판단 흐름으로 세운다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나르고,
#           focal 은 원문 예제가 실제로 걸린 판단 하나(윈도우 크기).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 712
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §4",
      "느릴 때 무엇부터 가르나",
      "지연이 선 위에 있는지 수신 측 처리에 있는지를 먼저 가른다. 원문의 slow_download.pcap 예제는 두 번째 갈래에서 걸렸고, 원인은 윈도우 크기가 100 으로 줄어 있던 것이었다.",
      "handshake 시각과 윈도우 크기, 두 눈금이면 어느 쪽인지가 갈립니다")

CX = 300
def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def step(cx, y, w, h, title, sub, c=None):
    if c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 24, title, 13, c if c else INK, KR, "middle", 600)
    d.t(cx, y + 44, sub, 11, MUTED, KR)

def diamond(cx, y, hw, hh, txt, focal=False):
    cy, c = y + hh, (ACC if focal else INK)
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)

Y_S, Y_D1, Y_R1, Y_D2, Y_R2, Y_END = 100, 168, 174, 316, 322, 596
Y_MID = 464

d.arrow([(CX, Y_S + 40), (CX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 144, Y_D1 + 40), (592, Y_R1 + 34)], WARN, "warn", 1.4)
d.arrow([(CX, Y_D1 + 80), (CX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 144, Y_D2 + 40), (592, Y_R2 + 34)], ACC, "acc", 1.4)
d.arrow([(CX, Y_D2 + 80), (CX, Y_MID - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_MID + 68), (CX, Y_END - 4)], MUTED, "ar", 1.4)
d.arrow([(712, Y_R2 + 68), (712, Y_END + 20), (CX + 156, Y_END + 20)], ACC, "acc", 1.4)

oval(CX, Y_S, 240, 40, "응답이 느리다")
diamond(CX, Y_D1, 144, 40, "선 자체가 느린가?", )
step(712, Y_R1, 320, 68, "네트워크 쪽입니다", "ping RTT · traceroute 홉 수 · 지터", c=WARN)
diamond(CX, Y_D2, 144, 40, "윈도우가 작은가?", focal=True)
step(712, Y_R2, 320, 68, "수신 측 처리 쪽입니다", "sysctl 버퍼 튜닝 · 프로세스 수 · 메모리", c=ACC)
step(CX, Y_MID, 320, 68, "재전송·중복 ACK 를 봅니다", "tcp.analysis.flags 로 판정을 모읍니다")
oval(CX, Y_END, 300, 40, "§5 시퀀스 분석으로", OK)

d.t(CX + 200, Y_D1 + 26, "예", 11, WARN, KR, "middle", 600)
d.t(CX + 16, Y_D1 + 100, "아니오", 11, MUTED, KR, "start", 600)
d.t(CX + 200, Y_D2 + 26, "예", 11, ACC, KR, "middle", 600)
d.t(CX + 16, Y_D2 + 100, "아니오", 11, MUTED, KR, "start", 600)
d.t(CX + 260, Y_END + 8, "튜닝 후 재측정", 11, ACC, KR, "start")

d.legend(H - 60, [("원문 예제가 걸린 갈래", ACC), ("경로 쪽 원인", WARN), ("다음 편으로", OK)])
d.save("03-02.latency-triage.svg")
