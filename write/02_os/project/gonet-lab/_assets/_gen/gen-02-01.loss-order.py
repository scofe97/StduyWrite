# 02-01.loss-order — 6 개 중 4 가 사라졌을 때 앱이 받는 순서
# 본문 요구(02-01 §4 「손실과 순서는 앱이 떠안습니다」):
#           TCP 는 4 가 재전송될 때까지 5·6 을 커널에 붙잡아 앱이 1~6 을 순서대로 받지만 그동안 멈추고(HOL 블로킹),
#           UDP 는 1 2 3 5 6 을 도착한 대로 바로 넘기고 4 는 끝내 오지 않는다.
# 타입 스펙: type-flowchart — 세 줄의 칸 나열(보낸 것 / TCP 앱 / UDP 앱). focal 은 TCP 의 대기 칸.
# 사실 출처: cntd 03-03 §5 TCP 의 신뢰적 전송, man udp(7), 02-01 Phase 1 문답(질문 4).
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, WARN, MONO, KR
from ddk import node

W, H = 960, 436
X0, CW, STEP, CH = 200, 56, 66, 40   # 칸 시작, 칸 폭, 칸 간격, 칸 높이

d = D(W, H, "FLOWCHART · 02-01 LOSS AND ORDER", "4 가 사라졌을 때 앱이 받는 것",
      "보낸 쪽이 1 부터 6 까지 보냈고 4 가 네트워크에서 사라졌다. TCP 는 4 가 재전송될 때까지 이미 도착한 5 와 6 을 "
      "커널에 붙잡아 두어 앱은 1 부터 6 까지 순서대로 받지만 그 사이 기다린다. UDP 는 1 2 3 5 6 을 도착한 대로 바로 "
      "넘기고 4 는 끝내 오지 않으며, 빠진 것을 알아채는 일은 앱의 몫이다.",
      lead="TCP 는 늦게라도 전부, UDP 는 바로 오지만 빠진 채로 받습니다.")


def cell(x, y, txt, c=None, dash=False):
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="5" fill="none" stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 4"/>')
        d.t(x + CW / 2, y + 25, txt, 13, BAD, MONO, "middle", 600)
    elif c:
        d.tone(x, y, CW, CH, c, 5, "10", 1.1)
        d.t(x + CW / 2, y + 25, txt, 14, c, MONO, "middle", 600)
    else:
        d.box(x, y, CW, CH)
        d.t(x + CW / 2, y + 25, txt, 14, INK, MONO, "middle", 600)


# 줄 1: 보낸 것
y = 118
d.t(24, y + 25, "보낸 순서", 13, MUTED, KR, "start", 600)
for i in range(6):
    cell(X0 + i * STEP, y, str(i + 1), BAD if i == 3 else None)
d.t(X0 + 3 * STEP + CW / 2, y + CH + 18, "사라짐", 12, BAD, KR, "middle")

# 줄 2: TCP 앱
y = 214
d.t(24, y + 25, "TCP · Read", 13, MUTED, KR, "start", 600)
for i in range(3):
    cell(X0 + i * STEP, y, str(i + 1))
wx = X0 + 3 * STEP
ww = 2 * STEP + CW
d.tone(wx, y, ww, CH, ACC, 5, "14", 1.6)
d.t(wx + ww / 2, y + 25, "5 · 6 커널 보관", 13, ACC, KR, "middle", 600)
for k, n in enumerate((4, 5, 6)):
    cell(wx + ww + 10 + k * STEP, y, str(n), OK)
d.t(wx + ww / 2, y + CH + 18, "4 재전송까지 대기 (HOL)", 12, ACC, KR, "middle")

# 줄 3: UDP 앱
y = 310
d.t(24, y + 25, "UDP · ReadFrom", 13, MUTED, KR, "start", 600)
for i, n in enumerate((1, 2, 3)):
    cell(X0 + i * STEP, y, str(n))
cell(X0 + 3 * STEP, y, "4", dash=True)
for i, n in enumerate((5, 6)):
    cell(X0 + (4 + i) * STEP, y, str(n))
d.t(X0 + 3 * STEP + CW / 2, y + CH + 18, "끝내 없음", 12, BAD, KR, "middle")

d.legend(386, [("멈춰 기다리는 곳", ACC), ("사라진 데이터그램", BAD), ("재전송 뒤 넘겨진 것", OK)])
d.save("02-01.loss-order.svg")
print("ok loss-order")
