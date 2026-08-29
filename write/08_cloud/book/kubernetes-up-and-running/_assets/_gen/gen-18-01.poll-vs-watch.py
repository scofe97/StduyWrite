# 18-01 §polling 대신 watch
# 본문이 대조의 축을 둘로 준다 — 지연과 API 서버 부하. 그러니 두 방식을 나란한 카드로 놓으면
# 안 되고 *시간축이 형태로 있어야* 한다. 같은 세로 시간축 위에 두 방식을 놓아야 "폴링은 주기가
# 올 때까지 기다린다" 가 빈 구간으로 보이고, "watch 는 연결이 열려 있다" 가 끊기지 않은 선으로
# 보인다. 왼쪽의 회색 왕복은 바뀐 게 없는데도 돌려주는 응답이라 부하 축을 함께 보인다.
# 본문이 실측으로 적어 둔 두 값(26ms 에 닫힘 · ADDED 뒤 MODIFIED)을 각 축에 그대로 옮긴다.
# 타입 스펙: type-sequence.md — 참여자 상자가 위에 한 줄, 점선 lifeline 이 아래로 내려오고,
#           가로 메시지 화살표가 그 사이를 오가며 시간이 위→아래로 흐른다. 응답을 점선으로
#           되돌리는 것까지 정본의 관례 그대로다. 초점은 실제로 달라진 MODIFIED 메시지다.
#           어긋나는 지점: 정본은 시퀀스 하나를 전제하는데 여기는 둘을 나란히 놓아 대조한다 —
#           본문이 대조 축을 지연과 부하 둘로 주므로 같은 세로 시간축 위에 놓아야
#           "폴링은 주기가 올 때까지 기다린다" 가 빈 구간으로 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 680
d = D(W, H, "KUBERNETES UP AND RUNNING · 18-01",
      "폴링은 기다리고 watch 는 열어 둔다",
      "폴링은 지연과 API 서버 부하를 함께 물린다. watch 는 hanging GET 으로 연결을 열어 두고 "
      "변화가 생길 때마다 스트림에 써 넣는다.",
      "kind 로컬 클러스터 실측 — 오른쪽 이벤트는 라벨을 붙이며 받은 것이다")

PW, PX = 590, (24, 626)
Y0, CH = 128, 428
Y1 = Y0 + CH
CLI_DX, SRV_DX = 132, 452          # 패널 안 레인 x 오프셋

for x, (title, sub, c) in zip(PX, [
        ("폴링", "list 를 일정 간격으로 다시 부른다", WARN),
        ("watch", "GET 한 번에 스트림을 열어 둔다", OK)]):
    d.box(x, Y0, PW, CH, PAPER2, c, 1.2, 8)
    d.t(x + 20, Y0 + 26, title, 14, c, KR, "start", 600)
    d.t(x + PW - 20, Y0 + 26, sub, 10, MUTED, KR, "end")
    for dx, nm in ((CLI_DX, "클라이언트"), (SRV_DX, "API 서버")):
        d.box(x + dx - 62, Y0 + 44, 124, 30, PAPER, RULE, 1.0, 5)
        d.t(x + dx, Y0 + 64, nm, 11, INK, KR)
        d.line(x + dx, Y0 + 78, x + dx, Y1 - 60, RULE, 0.8, "3 4")

def hop(x, y, c, label, sub=None, back=False, mk="ar", dash=None):
    a, b = (SRV_DX, CLI_DX) if back else (CLI_DX, SRV_DX)
    s = 1 if b > a else -1
    d.path(f"M {x+a+8*s} {y} L {x+b-10*s} {y}", c, 1.5, m=mk, dash=dash)
    mx = x + (a + b) / 2
    lat = all(ord(ch) < 128 for ch in label)
    d.t(mx, y - 8, label, 10, c, MONO if lat else KR, "middle", 600)
    if sub:
        d.t(mx, y + 14, sub, 9, MUTED, KR)

# 왼쪽 — 폴링. 같은 왕복이 반복되고 그 사이가 비어 있다.
XL = PX[0]
hop(XL, Y0 + 104, MUTED, "GET …/pods")
hop(XL, Y0 + 134, SOFT, "200 · 바뀐 것 없음", back=True, dash="4 3")
d.o.append(f'<rect x="{XL+CLI_DX-52}" y="{Y0+158}" width="{SRV_DX-CLI_DX+104}" height="38" rx="5" '
           f'fill="{WARN}0C" stroke="{WARN}" stroke-width="1.0" stroke-dasharray="4 4"/>')
d.t(XL + (CLI_DX + SRV_DX) / 2, Y0 + 182, "주기가 올 때까지 아무것도 못 받는다", 11, WARN, KR)
hop(XL, Y0 + 224, MUTED, "GET …/pods")
hop(XL, Y0 + 254, SOFT, "200 · 바뀐 것 없음", back=True, dash="4 3")
hop(XL, Y0 + 292, MUTED, "GET …/pods")
hop(XL, Y0 + 322, ACC, "200 · 이제야 변화가 보인다", back=True)
d.o.append(f'<rect x="{XL+20}" y="{Y1-46}" width="{PW-40}" height="34" rx="5" '
           f'fill="{WARN}12" stroke="{WARN}" stroke-width="1.2"/>')
d.t(XL + PW / 2, Y1 - 24, "요청마다 연결이 닫힌다 — 실측 26ms · 23KB", 11, WARN, KR)

# 오른쪽 — watch. 요청은 하나고 선이 끊기지 않는다.
XR = PX[1]
hop(XR, Y0 + 104, OK, "GET …/pods?watch=true")
d.line(XR + SRV_DX, Y0 + 112, XR + SRV_DX, Y1 - 60, OK, 2.4)
d.line(XR + CLI_DX, Y0 + 112, XR + CLI_DX, Y1 - 60, OK, 2.4)
d.t(XR + (CLI_DX + SRV_DX) / 2, Y0 + 138, "연결이 열린 채로 남는다", 10, OK, KR)
for j, (yy, ev, name) in enumerate([
        (Y0 + 172, "ADDED", "sidecar-timing-dxrs5"),
        (Y0 + 216, "ADDED", "web-5d4f7c4d94-k6wbg"),
        (Y0 + 260, "MODIFIED", "web-5d4f7c4d94-k6wbg"),
        (Y0 + 304, "MODIFIED", "web-5d4f7c4d94-k6wbg")]):
    c = ACC if ev == "MODIFIED" else MUTED
    hop(XR, yy, c, ev, sub=name, back=True, mk="acc" if c is ACC else "ar")
d.o.append(f'<rect x="{XR+20}" y="{Y1-46}" width="{PW-40}" height="34" rx="5" '
           f'fill="{OK}12" stroke="{OK}" stroke-width="1.2"/>')
d.t(XR + PW / 2, Y1 - 24, "요청은 한 번 — 끊을 때까지 스트림이 이어진다", 11, OK, KR)

BY = Y1 + 28
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "왼쪽의 점선 응답은 바뀐 것이 없는데도 리소스를 통째로 돌려준 것이다. "
                 "클라이언트가 늘어나면 이 응답이 API 서버를 눌러 지연을 더한다.",
    11, MUTED, KR, "start")
d.legend(BY + 40, [("폴링이 치르는 비용", WARN), ("watch 가 여는 스트림", OK),
                   ("실제로 달라진 것", ACC), ("헛돈 왕복", SOFT)])
d.save("18-01.poll-vs-watch.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)
