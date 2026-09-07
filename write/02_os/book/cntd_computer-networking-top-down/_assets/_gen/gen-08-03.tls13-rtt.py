# 타입 스펙: type-gantt — 막대 길이가 곧 데이터 전까지 드는 왕복 수다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.6.2 (책 596~597쪽) —
#   TLS 1.3 은 왕복 하나, TCP 위에서는 둘, QUIC 안에서는 하나이며 재방문 시 0 이 될 수 있다는 서술 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 1000, 700
d = D(W, H, "SECTION 8.6.2 · ROUND TRIPS BEFORE DATA",
      "목표는 그대로이고 줄어든 것은 왕복입니다",
      "판이 올라가며 바뀐 것은 기밀성·무결성·인증이라는 목표가 아니라 그것을 세우는 데 드는 왕복 수다.",
      "왕복 수는 원문 §8.6.2 의 서술입니다")

# 원문은 이전 판을 "two or more RTTs" 라 적을 뿐 정확한 수를 대지 않는다.
# 막대는 3 으로 그리되 라벨에 "이상" 을 붙여 단언하지 않는다.
ROWS = [("이전 판 TLS (TCP 위)", 3, "핸드셰이크에 둘 이상 + TCP 하나", WARN, True),
        ("TLS 1.3 (TCP 위)", 2, "TCP 연결 하나 + TLS 핸드셰이크 하나", INFO, False),
        ("TLS 1.3 (QUIC 안)", 1, "Client Hello 가 QUIC 연결 설정에 실립니다", OK, False),
        ("TLS 1.3 (QUIC · 재방문)", 0, "앞서 합의한 파라미터를 다시 씁니다", ACC, False)]
X0, UNIT, BH, STRIDE = 300, 168, 52, 76
Y0 = 176
for i, (name, n, note, c, atleast) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.t(X0 - 20, y + 32, name, 12, c, KR, "end", 600)
    if n:
        d.tone(X0, y, UNIT * n, BH, c, 5, "22" if c is ACC else "16", 1.4 if c is ACC else 1.1)
        d.t(X0 + UNIT * n / 2, y + 32, f"{n}+ RTT" if atleast else f"{n} RTT", 12, c, MONO, "middle", 600)
    else:
        d.box(X0, y, 96, BH, PAPER, c, 1.4, 5)
        d.o[-1] = d.o[-1].replace('stroke-width="1.4"', 'stroke-width="1.4" stroke-dasharray="5 4"')
        d.t(X0 + 48, y + 32, "0 RTT", 12, c, MONO, "middle", 600)
    d.t(X0 + max(UNIT * n, 96) + 16, y + 32, note, 11, MUTED, KR, "start")

AY = Y0 + 4 * STRIDE + 4
d.line(X0, AY, X0 + UNIT * 3, AY, RULE, 1.0)
for k in range(4):
    x = X0 + UNIT * k
    d.line(x, AY - 4, x, AY + 4, RULE, 0.8)
    d.t(x, AY + 20, str(k), 10, SOFT, MONO)
d.t(X0 + UNIT * 1.5, AY + 42, "데이터를 보내기까지의 왕복 수", 11, SOFT, KR)

PY = AY + 62
d.box(24, PY, 952, 76, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "1 RTT 가 가능한 이유", 12, INK, KR, "start", 600)
d.t(44, PY + 56, "Client Hello 가 이미 클라이언트의 DH 공개값을 싣고 갑니다. 서버가 인사와 동시에 마스터 비밀을 만들 수 있어 왕복이 하나로 줄었습니다.",
    11, MUTED, KR, "start")

d.legend(PY + 96, [("이전 판", WARN), ("TCP 위", INFO), ("QUIC 안", OK), ("재방문", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.tls13-rtt.svg"
d.save(out); print("→", out.name)
