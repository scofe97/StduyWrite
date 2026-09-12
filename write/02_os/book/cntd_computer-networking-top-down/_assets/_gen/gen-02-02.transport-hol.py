# 02-02 §7 — HTTP/2 가 못 푼 트랜스포트 층 HOL 블로킹. 세그먼트 하나가 빠지면 뒤에 멀쩡히 쌓인 것들도 위로 못 올라간다.
# 위 층은 스트림이 셋인데 TCP 층은 바이트 스트림 하나라 그 구분을 모른다는 것이 요점이고, 원문 §2.2.6 의 서술 그대로다.
# 세그먼트 번호·스트림 배정은 장면을 위한 예시값이다. 원문에 수치 예는 없다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 막히는 층(TCP 수신 버퍼)에만 focal 을 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 568
X0, LW, LH = 104, 856, 72
Y1, Y2, Y3 = 104, 224, 344          # 세 층의 상단. 층 72 + 사이 48 = stride 120
SEG_X0, SEG_W, SEG_STRIDE, SEG_H = 480, 88, 96, 40

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §7",
      "TCP 는 스트림이 몇 개인지 모릅니다",
      "HTTP/2 가 프레임을 섞어 보내도 TCP 수신 버퍼는 바이트 스트림 하나다. 세그먼트 2 가 빠지면 뒤에 도착한 3·4·5 는 다른 스트림 것인데도 위로 못 올라간다.",
      "빠진 것은 하나인데 기다리는 것은 셋입니다")

def band(y, tag, name, sub, focal=False):
    if focal: d.tone(X0, y, LW, LH, ACC, 6, "14", 1.4)
    else: d.box(X0, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 44, tag, 9, SOFT, MONO, "start")
    d.t(X0 + 64, y + 32, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(X0 + 64, y + 54, sub, 13, MUTED, KR, "start")

band(Y1, "L7", "HTTP/2 프레이밍 층", "스트림마다 따로 이어 붙입니다")
band(Y2, "L4", "TCP 수신 버퍼", "스트림 경계를 모릅니다", focal=True)
band(Y3, "L3", "네트워크", "세그먼트 2 가 도중에 사라졌습니다")

# L7 — 스트림 셋이 모두 기다린다
for i, s in enumerate(("A", "B", "C")):
    d.chip(SEG_X0 + 72 + i * 156, Y1 + LH / 2, f"스트림 {s} · 대기", WARN, 13)

# L4 — 세그먼트 다섯, 2 만 빠짐
SEGS = [("1", "A", "도착"), ("2", "A", "빠짐"), ("3", "B", "도착"), ("4", "C", "도착"), ("5", "B", "도착")]
for i, (n, s, st) in enumerate(SEGS):
    x = SEG_X0 + i * SEG_STRIDE
    y = Y2 + (LH - SEG_H) / 2
    if st == "빠짐":
        d.o.append(f'<rect x="{x}" y="{y}" width="{SEG_W}" height="{SEG_H}" rx="5" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        d.t(x + SEG_W / 2, y + 17, f"seg {n}", 12, BAD, MONO, "middle", 600)
        d.t(x + SEG_W / 2, y + 33, "빠짐", 13, BAD, KR)
    else:
        d.box(x, y, SEG_W, SEG_H, PAPER, OK, 1.0, 5)
        d.t(x + SEG_W / 2, y + 17, f"seg {n}", 12, INK, MONO, "middle", 600)
        d.t(x + SEG_W / 2, y + 33, f"스트림 {s}", 13, SOFT, KR)

# L4 → L7 인계. 1 은 올라갔고 3·4·5 는 2 때문에 막힌다
def seg_cx(i): return SEG_X0 + i * SEG_STRIDE + SEG_W / 2
d.path(f"M {seg_cx(0)} {Y2 - 4} L {seg_cx(0)} {Y1 + LH + 8}", OK, 1.5, m="ok")
d.t(seg_cx(0) - 12, Y1 + LH + 30, "올라감", 13, OK, KR, "end")
for i in (2, 3, 4):
    d.path(f"M {seg_cx(i)} {Y2 - 4} L {seg_cx(i)} {Y2 - 20}", BAD, 1.5, dash="4 3")
    d.line(seg_cx(i) - 8, Y2 - 24, seg_cx(i) + 8, Y2 - 24, BAD, 1.5)
d.t(620, Y1 + LH + 30, "2 가 올 때까지 막힘", 13, BAD, KR)

# L3 → L4. 2 의 재전송을 기다린다
d.path(f"M {seg_cx(1)} {Y3 - 8} L {seg_cx(1)} {Y2 + LH + 8}", BAD, 1.5, m="bad", dash="4 3")
d.t(seg_cx(1) + 16, Y2 + LH + 30, "재전송이 올 때까지", 13, BAD, KR, "start")

# 왼쪽 여백 — 방향 표시
d.path(f"M 56 {Y3 + LH - 8} L 56 {Y1 + 16}", SOFT, 1.0, m="soft")
d.t(56, Y3 + LH + 14, "deliver", 9, SOFT, MONO)

d.t(24, 464, "HTTP/2 는 애플리케이션 층에서 프레임을 섞어 앞 객체가 뒤 객체를 막는 일을 없앴습니다.",
     13, MUTED, KR, "start")
d.t(24, 486, "그런데 TCP 는 순서를 보장하는 바이트 스트림 하나라, 세그먼트 하나가 빠지면 그 뒤에 쌓인 것을 스트림과 무관하게 전부 붙듭니다.",
     13, MUTED, KR, "start")
d.t(24, 508, "같은 형태가 04-02 §1 의 입력 큐에도 있습니다. 앞의 것이 못 나가면 뒤도 못 나갑니다.",
     13, SOFT, KR, "start")

d.legend(H - 44, [("빠진 세그먼트와 그것이 막은 것", BAD), ("올라간 세그먼트", OK), ("기다리는 스트림", WARN), ("막히는 층", ACC)])
d.save("02-02.transport-hol.svg")
