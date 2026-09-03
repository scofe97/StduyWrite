# 10-01 §7 로거 스코프가 찍는 계층.
# 본문(원문 10.3.3 "Increasing the logging level"): 저자가 도움이 된다고 든 스코프 넷 —
#       connection(레이어 4 전송, TCP 커넥션 상세), http(레이어 7 애플리케이션, HTTP 상세),
#       router(HTTP 요청의 라우팅), pool(커넥션 풀이 업스트림 호스트 커넥션을 얻거나 버리는 것).
#       레벨은 none · error · warning · info · debug 다섯이고 스코프마다 따로 정한다.
# 저자의 추적에서 결정적인 줄(upstream timeout)이 router 스코프에서 나온다.
# 타입 스펙: type-layers — 위아래로 쌓인 계층. 층 4, 층 높이 72, 왼쪽 여백에 방향 표시,
#           초점 1층(타임아웃 판정이 찍히는 층).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 10-01 §7",
      "스코프를 고르면 볼 계층을 고르는 것이다",
      "로거는 스코프마다 레벨을 따로 갖는다. 위로 갈수록 애플리케이션에 가깝고 아래로 갈수록 전송에 "
      "가깝다. 색이 붙은 층에서 타임아웃 판정과 어느 클러스터로 갔는지가 함께 나온다.",
      "전부 debug 로 올리면 로그에 잠기므로 볼 계층만 골라 올립니다")

LX, LW, LH, Y0 = 180, 752, 72, 132
rows = [("HTTP", "http", "레이어 7 · 애플리케이션", "헤더 · 경로 · 스트림 ID", False),
        ("ROUTER", "router", "라우팅 판단", "맞은 클러스터와 upstream timeout", True),
        ("POOL", "pool", "커넥션 풀", "업스트림 커넥션을 얻거나 버린다", False),
        ("CONN", "connection", "레이어 4 · 전송", "TCP 연결 · 핸드셰이크 · 종료", False)]
for i, (tag, name, mid, right, focal) in enumerate(rows):
    y = Y0 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{ACC}10" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 4)
    d.t(LX + 20, y + 42, tag, 9, SOFT, MONO, "start", 600)
    d.t(LX + 108, y + 42, name, 14, ACC if focal else INK, MONO, "start", 600)
    d.t(LX + 268, y + 42, mid, 12, ACC if focal else MUTED, KR, "start")
    d.t(LX + LW - 20, y + 42, right, 11, MUTED, KR, "end")

d.path(f"M {LX - 44} {Y0 + 8} L {LX - 44} {Y0 + 4 * LH - 8}", MUTED, 1.2, m="ar")
d.t(LX - 60, Y0 + 24, "애플리케이션", 11, SOFT, KR, "end")
d.t(LX - 60, Y0 + 4 * LH - 24, "전송", 11, SOFT, KR, "end")

d.t(28, 456, "레벨은 none · error · warning · info · debug 다섯이고 기본은 warning 이다", 11, SOFT, KR, "start")
d.t(28, 480, "커넥션 ID 로 한 커넥션을 묶고 스트림 ID 로 그 안의 요청 하나를 묶는다", 11, MUTED, KR, "start")
d.legend(504, [("타임아웃 판정이 찍히는 층", ACC), ("함께 올리면 도움이 되는 층", MUTED)])
d.save("10-01.logger-scopes.svg")
