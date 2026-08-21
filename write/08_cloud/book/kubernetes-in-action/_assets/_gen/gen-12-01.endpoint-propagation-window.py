# 12-01 §2 — 위험한 것은 IP 가 바뀌는 게 아니라 바뀐 걸 아는 데 걸리는 시간
# 본문의 그 문장이 시간축을 요구한다. 창(window)이 열려 있는 구간을 띠로 칠하고,
# 그 구간을 메우는 장치 둘을 아래에 붙인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 596, "KUBERNETES IN ACTION · 12-01",
      "명단이 프록시에 닿기까지 창이 열린다",
      "파드가 죽어도 그 사실이 프록시 설정에 반영되기까지 수백 밀리초에서 수 초가 걸린다. "
      "그동안 upstream 목록에는 죽은 주소가 남아 있고, 요청이 그리로 간다.",
      "파드 하나가 죽은 뒤")

STEP = [("파드가 죽는다", "terminating"), ("EndpointSlice 갱신", "컨트롤 플레인"),
        ("컨트롤러 통지", "watch 이벤트"), ("설정 생성", "nginx.conf"), ("reload", "프록시 반영")]
X0, BW, GP = 60, 200, 30
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]
for cx, (t, s) in zip(CX, STEP):
    d.box(cx - BW // 2, 236, BW, 72, PAPER2, RULE, 1.1, 6)
    d.t(cx, 266, ddx.fit(t, 12, BW - 16, t), 12, INK, KR, "middle", 600)
    d.t(cx, 288, s, 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 272 L {b-BW//2-9} 272", MUTED, 1.4, m="ar")

L, R = CX[0], CX[4]
d.o.append(f'<rect x="{L}" y="160" width="{R-L}" height="52" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t((L + R) / 2, 192, "창이 열려 있다 — upstream 에 죽은 주소가 남아 있다", 12, ACC, KR)
d.line(L, 212, L, 232, ACC, 1.0, "4 4")
d.line(R, 212, R, 232, ACC, 1.0, "4 4")
d.t(R + 20, 192, "수백 ms ~ 수 초", 11, ACC, KR, "start")

d.t(60, 356, "창을 메우는 장치 둘", 12, SOFT, KR, "start")
for cx, t, s in ((355, "프록시 재시도", "죽은 주소로 간 요청이 실패하면 살아 있는 파드로 다시 보낸다"),
                 (885, "graceful shutdown · preStop", "파드가 잠시 더 받아 주어 명단이 전파될 시간을 번다")):
    d.box(cx - 250, 380, 500, 76, PAPER2, OK, 1.1, 6)
    d.t(cx, 410, t, 13, OK, KR, "middle", 600)
    d.t(cx, 432, ddx.fit(s, 11, 484, s), 11, MUTED, KR)

d.t(24, 508, "cluster IP 를 거치는 방식은 재시도를 못 하므로, 이 구간에서는 오히려 파드 직접 방식이 유리해진다.",
     11, MUTED, KR, "start")
d.t(24, 530, "11-03 이 '변경 1 회의 전송량'이었다면 여기는 '그 변경이 프록시에 닿기까지의 지연'이다.",
     11, MUTED, KR, "start")
d.legend(548, [("열려 있는 창", ACC), ("메우는 장치", OK)])
d.save("12-01-endpoint-propagation-window.svg")
print("ok")
