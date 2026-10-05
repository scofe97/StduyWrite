# 13-01 §5 — 같은 4-tuple 의 옛 연결(incarnation)에서 늦게 도착한 세그먼트가 새 연결에 섞이는가.
# 원문 13.2.3: 연결이 열려 있으면 두 주소·두 포트가 맞고 순서 번호가 창 안에 있으며 체크섬이 맞는 세그먼트는 유효로 받아들여진다.
#   옛 연결의 세그먼트가 오래 지연된 뒤 같은 4-tuple 로 연결이 다시 열리면, 그 세그먼트가 새 데이터로 들어갈 수 있다.
#   ISN 을 시간에 따라 바꿔(RFC 793: 4μs 마다 1 씩 느는 32비트 카운터) 연결 사이 번호가 겹치지 않게 해 이 위험을 줄인다.
# 수치는 설명용 예시다(원문에 없는 값): 옛 연결 ISN 1000, 지연된 세그먼트 seq 1001–1100, 새 연결 창 1001–9000 대 5,001,001 부터.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 시간축 + 행마다 막대(연결의 수명 구간), 그 위에 지연 세그먼트의 도착 시점 표시.
#           축약: 행이 작업이 아니라 "같은 4-tuple 의 연결 하나" 이고 축은 상대 시간이다. 두 판(ISN 이 같다면 / 시간으로 띄우면)을
#           같은 축 문법으로 위아래에 둔다. focal 은 위 판에서 지연 세그먼트가 창 안으로 떨어지는 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560
LX, TX0, TX1 = 20, 216, 872
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §5",
      "옛 연결의 세그먼트가 새 연결에 떨어질 때",
      "같은 두 주소·두 포트로 연결을 닫았다가 다시 열었다. 옛 연결에서 보낸 세그먼트(seq 1001–1100) 하나가 망에서 늦게 도착한다. "
      "위 판처럼 새 연결의 ISN 이 옛 연결과 같으면 그 번호가 새 창 안에 들어 데이터로 받아들여진다. 아래 판처럼 ISN 을 시간에 따라 띄워 두면 창 밖이라 버려진다. 수치는 설명용 예시다.",
      "4-tuple 이 같아도 번호 영역이 겹치지 않으면 옛 세그먼트는 새 연결에 섞이지 않습니다")

def timeline(y0, title, new_isn, accepted):
    d.t(LX, y0, title, 13, INK, KR, "start", 600)
    # 옛 연결 / 새 연결 막대
    rows = [("옛 연결", 0.00, 0.34, "ISN 1000", MUTED), ("새 연결", 0.46, 1.00, f"ISN {new_isn}", INFO)]
    for i, (lab, s, e, isn, c) in enumerate(rows):
        y = y0 + 20 + i * 48
        d.t(LX + 8, y + 22, lab, 12, INK, KR, "start", 600)
        x0, x1 = TX0 + s * (TX1 - TX0), TX0 + e * (TX1 - TX0)
        d.tone(x0, y + 6, x1 - x0, 24, c, 4, "14", 1.0)
        d.t(x0 + 10, y + 22, isn, 11, c, MONO, "start", 600)
    # 지연 세그먼트 — 옛 연결 안에서 출발해 새 연결 구간에 도착
    ys = y0 + 20 + 18; ye = y0 + 20 + 48 + 18
    xs = TX0 + 0.20 * (TX1 - TX0); xe = TX0 + 0.72 * (TX1 - TX0)
    d.path(f"M {xs} {ys} V {ys + 30} H {xe} V {ye - 12}", WARN, 1.3, m="warn", dash="4 3")
    d.t((xs + xe) / 2, ys + 26, "지연된 세그먼트 seq 1001–1100", 12, WARN, KR, "middle", 600)
    # 판정 칩
    cy = y0 + 20 + 2 * 48 + 14
    if accepted:
        w = 236
        d.o.append(f'<rect x="{xe - w / 2}" y="{cy - 12}" width="{w}" height="24" rx="5" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(xe, cy + 5, "창 1001–9000 안 · 데이터로 받아들임", 12, ACC, KR, "middle", 600)
    else:
        d.chip(xe, cy, "창 5,001,001– 밖 · 버림", OK, 12)

timeline(112, "ISN 이 같다면", "1000", True)
timeline(320, "ISN 을 시간으로 띄우면", "5,001,000", False)

d.legend(H - 56, [("옛 데이터가 새 스트림에 섞임", ACC), ("늦게 도착한 세그먼트", WARN), ("새 연결", INFO), ("창 밖이라 버려짐", OK)])
d.save("13-01.isn-incarnation.svg")
