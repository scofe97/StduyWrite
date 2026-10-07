# 사실 출처: go1.25.1 src/net/http/client.go:351, src/net/http/transport.go:1694,2842,2531,1134, src/net/http/httptrace/trace.go
# 타입 스펙: type-gantt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "HTTP REQUEST PHASES AND TIMEOUT BOUNDARIES",
      "HTTP 요청 생명주기와 타임아웃 경계 간트",
      "DNS·연결·TLS·요청 전송·첫 바이트 대기·본문 읽기 구간별 타임아웃 적용 범위",
      "Client.Timeout 은 본문 소비 완료까지 전체를 감싸며 Transport 타임아웃은 개별 구간을 제한합니다")

LX = 28
TX = 210
TW = 710

# 6개 구간 상대 비율 (총 710px)
# 0: DNS(70) 1: TCP(90) 2: TLS(100) 3: Req(100) 4: Wait(140) 5: Body(210)
phase_widths = [70, 90, 100, 100, 140, 210]
phase_x = [TX]
for w in phase_widths:
    phase_x.append(phase_x[-1] + w)

phases = [
    ("DNS 조회", "DNSStart"),
    ("TCP 연결", "ConnectStart"),
    ("TLS 핸드셰이크", "TLSHandshake"),
    ("요청 쓰기", "WroteRequest"),
    ("첫 바이트 대기", "GotFirstByte"),
    ("본문 스트림 읽기", "Body.Close"),
]

# 상단 단계 헤더 (Y = 104)
d.box(TX, 100, TW, 36, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
for i, (name, hook) in enumerate(phases):
    x1 = phase_x[i]
    x2 = phase_x[i+1]
    cx = (x1 + x2) // 2
    d.t(cx, 116, name, 11, INK, fam=KR, weight=600)
    d.t(cx, 129, hook, 9, SOFT, fam=MONO)
    if i > 0:
        d.line(x1, 100, x1, 400, RULE, 0.7, "2 3")

# 수직 구분선 끝
d.line(phase_x[-1], 100, phase_x[-1], 400, RULE, 0.7, "2 3")

# 타임아웃 바 정의 (라벨, 서브, 시작idx, 종료idx, 색상, 포컬여부)
bars = [
    ("Dialer.Timeout", "net.Dialer", 0, 2, INFO, False),
    ("TLSHandshakeTimeout", "Transport", 2, 3, WARN, False),
    ("ResponseHeaderTimeout", "Transport", 3, 5, BAD, False),
    ("Client.Timeout", "전체 요청 한도", 0, 6, ACC, True),
]

y_start = 156
row_h = 56

for r, (title, owner, s_idx, e_idx, col, focal) in enumerate(bars):
    y = y_start + r * row_h
    # 좌측 식별 라벨
    d.t(LX, y + 20, title, 12, col if focal else INK, fam=MONO, anchor="start", weight=600 if focal else 400)
    d.t(LX, y + 36, owner, 10, SOFT, fam=KR, anchor="start")

    # 간트 바
    bx1 = phase_x[s_idx] + 2
    bx2 = phase_x[e_idx] - 2
    bw = bx2 - bx1
    fill = f"{col}22" if focal else f"{col}14"
    sw = 1.4 if focal else 1.0
    d.box(bx1, y + 6, bw, 32, fill=fill, stroke=col, sw=sw, r=5)

    # 바 내부 텍스트
    center_x = (bx1 + bx2) // 2
    if focal:
        d.t(center_x, y + 26, "DNS 연결부터 Response.Body 소비 완료까지 전체 제한 (focal)", 11, ACC, fam=KR, weight=600)
    elif r == 0:
        d.t(center_x, y + 26, "이름 해석 + 소켓 핸드셰이크", 10, INFO, fam=KR)
    elif r == 1:
        d.t(center_x, y + 26, "TLS 암호화 협상", 10, WARN, fam=KR)
    elif r == 2:
        d.t(center_x, y + 26, "요청 완료 후 응답 헤더 도착 대기", 10, BAD, fam=KR)

# 유휴 연결 보조 칩 (IdleConnTimeout 은 트랜잭션 바깥)
d.box(TX + TW - 280, 384, 280, 28, fill=PAPER2, stroke=MUTED, sw=0.8, r=4)
d.t(TX + TW - 140, 402, "IdleConnTimeout: Body 종료 후 풀 보관 시간", 10, MUTED, fam=KR)

# 범례
d.legend(430, [
    ("연결 단계 타임아웃", INFO),
    ("TLS 협상 타임아웃", WARN),
    ("헤더 대기 타임아웃", BAD),
    ("전체 포괄 타임아웃 (focal)", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02.timeout-gantt.svg"))
d.save(out_path)
