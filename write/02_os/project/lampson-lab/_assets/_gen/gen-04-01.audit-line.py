# 04-01 §4 — sshd 가 남긴 한 줄이 세 가지를 가리킨다.
# 타입 스펙: type-process — 로그 한 줄의 구간 셋이 같은 슬롯(이름 · 뜻 · 쓰임)의 칸 셋으로 이어진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 340
d = D(W, H, "LAMPSON LAB · 04-01 §4",
      "로그 한 줄이 가리키는 세 가지",
      "sshd 의 Accepted 줄은 들어온 계정, 인증서를 받은 워크로드, 인증서 한 장을 각각 다른 구간으로 남긴다.",
      "Key ID 가 SPIFFE ID 라서 로그만 보고도 어느 워크로드인지 알 수 있다")

# 로그 줄 — 한 줄 text 안의 tspan 으로 구간을 나눈다. 연결선 x 는 11px 모노 폭 6.6 으로 잡았다.
LY = 128
CWID = 6.6
d.box(24, LY - 28, 832, 48, PAPER2, RULE, 1.0, 6)
parts = [
    ("Accepted publickey for ", MUTED, 400),
    ("operator", INK, 600),
    (" ... ID ", MUTED, 400),
    ("spiffe://lab/client/deployer", ACC, 600),
    (" (serial ", MUTED, 400),
    ("8264256466741114221", INK, 600),
    (")", MUTED, 400),
]
spans = "".join(f'<tspan fill="{c}" font-weight="{w}">{t.replace(" ", chr(160))}</tspan>' for t, c, w in parts)
d.o.append(f'<text x="40" y="{LY}" font-family="{MONO}" font-size="11" xml:space="preserve">{spans}</text>')
anchor, acc_x = {}, 40
for t, c, w in parts:
    anchor[t] = acc_x + len(t) * CWID / 2
    acc_x += len(t) * CWID

cards = [
    ("operator", "operator", "들어온 역할 계정", "개인 계정이 없으니 사람 이름이 아니다"),
    ("Key ID", "spiffe://lab/client/deployer", "인증서를 받은 워크로드", "SPIFFE ID 가 그대로 남는다"),
    ("serial", "8264256466741114221", "인증서 한 장", "발급할 때 찍힌 번호와 맞춘다"),
]
w, gap, x0 = 264, 20, 24
for i, (head, key, what, note) in enumerate(cards):
    x = x0 + i * (w + gap)
    focal = (head == "Key ID")
    ax = anchor[key]
    d.path(f"M {ax:.0f} {LY + 24} V 164 H {x + w / 2:.0f} V 188", ACC if focal else MUTED, 1.0)
    if focal:
        d.o.append(f'<rect x="{x}" y="188" width="{w}" height="96" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, 188, w, 96, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, 214, head, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, 240, what, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, 264, note, 12, MUTED, KR, "start")

d.t(24, 316, "줄 안의 CA 지문과 접속 주소는 생략했다 — 구간은 실측 줄(AC-18)과 같은 순서다", 12, SOFT, KR, "start")
d.save("04-01.audit-line.svg")
