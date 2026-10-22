# 타입 스펙: type-gantt — 두 세그먼트가 바이트 축 위에서 한 HTTP 메시지로 이어지는 자리
# 사실 출처: 노트 L230~L241 (frame.len·tcp.len 표, Reassembled TCP Segments 블록, 6238 - 6162 = 76)
# 02-04 §7 — 막대 길이가 곧 바이트 구간이다. 시간축 대신 바이트 오프셋 0~6318 을 가로축으로 쓴다(스펙의 주차를 바이트로 바꾼 축약).
# focal 은 재조립으로 생긴 6318바이트 한 줄. 프레임 31 은 폭 15px 로 가늘어 라벨을 막대 오른쪽 빈 자리에 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 484
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-04 §7",
      "프레임 31 과 32 가 한 HTTP 메시지로 이어집니다",
      "tshark -V 의 Reassembled TCP Segments 블록. 프레임 31 이 payload 0~155(156바이트), 프레임 32 가 156~6317(6162바이트)을 나르고, 둘을 이은 6318바이트에서 HTTP 메시지가 완성된다. 프로토콜 목록에 http 가 붙는 것은 32번부터다.",
      "http 가 처음 붙는 프레임은 메시지가 끝나는 32번입니다")

X0, X1, TOTAL = 220, 840, 6318
def X(b): return X0 + b * (X1 - X0) / TOTAL

# 가로 축 — 오프셋 눈금
d.t(24, 124, "TCP payload 오프셋", 12, SOFT, KR, "start")
for b, lab, anc in ((0, "0", "end"), (156, "156", "middle"), (6318, "6318", "middle")):
    d.line(X(b), 132, X(b), 140, RULE, 1.0)
    d.t(X(b) + (-4 if anc == "end" else 0), 128, lab, 12, MUTED, MONO, anc)
d.line(X0, 140, X1, 140, RULE, 1.0)

ROWS = [160, 224, 288]
labels = ["프레임 31", "프레임 32", "TCP 재조립"]
for y, lab in zip(ROWS, labels):
    d.t(24, y + 26, lab, 13, INK, KR, "start", 600)

# 프레임 31 — payload 0~155
d.o.append(f'<rect x="{X(0)}" y="{ROWS[0] + 8}" width="{X(156) - X(0)}" height="28" rx="4" fill="{INFO}22" stroke="{INFO}" stroke-width="1.1"/>')
d.t(X(156) + 10, ROWS[0] + 27, "#31 · 156바이트 · 0~155", 13, INFO, KR, "start", 600)
d.t(X0, ROWS[0] + 56, "null:ipv6:tcp", 12, MUTED, MONO, "start")

# 프레임 32 — payload 156~6317
d.o.append(f'<rect x="{X(156)}" y="{ROWS[1] + 8}" width="{X(6318) - X(156)}" height="28" rx="4" fill="{INFO}22" stroke="{INFO}" stroke-width="1.1"/>')
d.t((X(156) + X(6318)) / 2, ROWS[1] + 27, "#32 · 6162바이트 · 156~6317", 13, INFO, KR, "middle", 600)
d.t(X(156), ROWS[1] + 56, "null:ipv6:tcp:http:data-text-lines", 12, MUTED, MONO, "start")

# 재조립 — focal
d.tone(X(0), ROWS[2] + 8, X(6318) - X(0), 28, ACC, 4, "12", 1.4)
d.t((X(0) + X(6318)) / 2, ROWS[2] + 27, "HTTP 메시지 6318바이트 = 156 + 6162", 13, ACC, KR, "middle", 600)

# 프레임 길이 76 바이트
d.line(24, 372, W - 48, 372, RULE, 0.8)
d.t(24, 400, "프레임 32 의 6238 − 6162 = 76 바이트", 13, INK, KR, "start", 600)
d.t(X0 + 140, 400, "루프백 4 + IPv6 40 + TCP 32", 13, MUTED, KR, "start")

d.legend(428, [("프레임 하나가 나른 payload", INFO), ("재조립이 이어 붙인 메시지", ACC)])
d.save("02-04.reassembly-bytes.svg")
