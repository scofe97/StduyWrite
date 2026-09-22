# 10-02 §4 — 연결 큐가 둘인 이유는 SYN 플러드 방어다.
# 타입 스펙: type-process — SYN 도착에서 accept 까지의 단계 지도. 화살표가 승격 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 416
CW, CH, GAP, X0, Y = 264, 148, 44, 40, 128

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-02 §4",
       "연결 큐가 둘인 까닭",
       "SYN 큐는 핸드셰이크가 끝나지 않은 요청의 대기소이고, accept 큐는 수립됐지만 accept 를 기다리는 줄이다. 둘로 나눈 덕에 가짜 연결이 진짜 연결의 자리를 차지하지 않는다.",
       "첫 큐는 가짜일 수 있는 연결의 대기소, 둘째 큐는 수립된 연결의 줄입니다")

STEPS = [
    ("01", "SYN 큐", "원서: SYN 백로그", INFO,
     ["핸드셰이크 전 · SYN_RECV", "넘치면 SYN cookies(기본)", "쿠키 끄면 드롭 · ReqQFull"]),
    ("02", "accept 큐", "원서: listen 백로그", ACC,
     ["핸드셰이크가 끝난 연결", "넘치면 SYN·마지막 ACK 드롭", "ListenOverflows · Recv-Q"]),
    ("03", "accept()", "유저 프로세스", OK,
     ["앱이 꺼내 감", "느리면 accept 큐가 참", "→ 클라이언트 연결 지연"]),
]

for i, (n, name, tag, c, body) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" fill="{c}" stroke="{c}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER, MONO)
    d.t(x + 48, Y + 29, name, 14, c, KR, "start", 600)
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    for j, line in enumerate(body):
        d.t(x + 16, Y + 80 + j * 20, line, 13, MUTED, KR, "start")
    if i < 2:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 8, Y + CH / 2)], MUTED, "ar", 1.3)

YB = Y + CH + 40
d.t(X0, YB, "SYN cookies · 첫 큐에 저장 없음 · 보증 범위: SYN-ACK 수신까지(신원 인증 아님)", 13, WARN, KR, "start")
d.t(X0, YB + 24, "두 큐 공통 한도: min(backlog, somaxconn)", 13, MUTED, KR, "start")

d.legend(YB + 48, [("넘치면 연결 지연이 되는 큐", ACC), ("가짜가 섞이는 대기소", INFO), ("유저 공간", OK), ("SYN cookies", WARN)])
d.save("10-02.connection-queues.svg")
