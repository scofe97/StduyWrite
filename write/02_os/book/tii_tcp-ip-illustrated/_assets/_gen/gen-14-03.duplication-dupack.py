# 14-03 §4 — 원서 Figure 14-14 를 대신한다.
# 사실 출처(ch14.txt §14.8.2): 링크 계층 재전송 등으로 IP 가 한 패킷을 여러 번 전달할 수 있다. 패킷 3 이 세 번 복제되어
#   수신자가 중복 ACK 를 잇달아 보내고, 비 SACK 송신자는 뒤쪽 패킷이 먼저 도착한 것으로 오인해 불필요한 빠른 재전송을 한다.
#   DSACK 이 있으면 A3 중복 ACK 마다 '3 은 이미 받음' 이 실리고 순서 밖 데이터 표시는 없어, 송신자가 복제임을 알아챌 수 있다.
# 축약: ACK 는 원서 표기대로 '이미 도착한 것'(A3 = 3 까지 도착)이므로 다음 미확인 세그먼트인 4 가 빠른 재전송 대상이다.
#       '세 번 복제' 를 원본 뒤에 사본 셋이 더 닿는 것으로 그렸다. 송신 목록에는 원서(1953–1955행)가 이름을 든 5·6 까지 넣었다.
#       원본 4·5·6 의 도착 시점은 원서 본문에 없어 그리지 않았다.
# 타입 스펙: type-sequence — 송신자·망·수신자 세 레인. 망 레인이 복제가 일어나는 자리다. 반환(ACK)은 점선.
#           focal 은 중복 ACK 셋이 부른 불필요한 4 빠른 재전송.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 680
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §4",
      "망이 만든 사본도 중복 ACK 를 쌓는다",
      "송신자가 3–6 을 보냈고, 망이 3 을 세 번 더 전달했다. 수신자는 원본 3 에 A3 을 보낸 뒤 사본마다 같은 A3 을 되풀이한다. "
      "비 SACK 송신자는 중복 ACK 셋을 5·6 이 먼저 도착한 신호로 읽어 4 를 빠르게 재전송한다. 원본 4·5·6 의 도착은 그리지 않았다. "
      "DSACK 을 쓰면 중복 ACK 마다 '3 은 이미 받음' 이 실려 복제임을 가릴 수 있다.",
      "중복 ACK 의 원인이 구멍이 아니라 사본일 수 있습니다")

S, N, R = "송신자", "망", "수신자"
LX = {S: 150, N: 460, R: 770}
STRIDE, Y0 = 40, 192
BOT = Y0 + 9 * STRIDE + 24
for name, x in LX.items():
    d.box(x - 80, 100, 160, 44, PAPER2, RULE, 1.0)
    d.t(x, 128, name, 12, INK, KR, "middle", 600)
    d.line(x, 150, x, BOT, RULE, 1.0, "3 6")

def msg(a, b, label, row, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
    x1, x2 = LX[a], LX[b]; dd = 1 if x2 > x1 else -1
    y = Y0 + row * STRIDE
    d.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
    mx = lx if lx is not None else (x1 + x2) / 2
    d.t(mx, y - 8, label, 12, c, _kr(label), "middle", 600)
    if sub: d.t(mx, y + 16, sub, 11, MUTED, _kr(sub))

def side(x, row, txt, c, anchor="start"):
    d.t(x, Y0 + row * STRIDE + 4, txt, 11, c, _kr(txt), anchor)

AX = (LX[N] + LX[R]) / 2
msg(S, N, "3 · 4 · 5 · 6", 0, INFO, "info")
msg(N, R, "3", 1, INFO, "info")
msg(R, S, "A3", 2, MUTED, "ar", "5 4", lx=AX)
for k in range(3):
    msg(N, R, "3 사본", 3 + 2 * k, BAD, "bad")
    msg(R, S, "A3", 4 + 2 * k, WARN, "warn", "5 4", lx=AX,
        sub="중복 3개 · DSACK 이면 3 이미 받음" if k == 2 else None)
side(LX[N] - 16, 3, "망이 3 복제", BAD, "end")
side(LX[R] + 16, 3, "중복 3", BAD)
msg(S, N, "4 빠른 재전송", 9, ACC, "acc", sub="5·6 도착으로 오인")
side(LX[N] + 16, 9, "원본 4·5·6 도착 생략", SOFT)

d.legend(H - 56, [("불필요한 빠른 재전송", ACC), ("망이 만든 사본", BAD), ("중복 ACK", WARN), ("데이터", INFO)])
d.save("14-03.duplication-dupack.svg")
