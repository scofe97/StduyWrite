# 05-02 심화 학습 — 원문의 http · dns 필터에 아무것도 안 잡히는데 트래픽은 오갈 때 무엇을 확인하나.
# 본문 요구: 심화 학습의 두 문단 — "HTTP/2 는 TLS 위의 바이너리 프레임이라 http 필터로는 안 잡히고 http2 를
#            써야 하며, 앞 장의 복호화가 없으면 내용이 보이지 않습니다. HTTP/3 는 QUIC(UDP) 위에 있어
#            quic · http3 를 씁니다" · "DoT(TCP 853)와 DoH(443)를 쓰면 dns 필터로 안 잡힙니다" 를 결정
#            흐름으로 옮긴다. 캐시 갈래는 RFC 1034 §5.3.3 1단계, 853 은 RFC 7858 §3.1.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 05-01.triage 의 판단 열·결론 칸 좌표를 쓴다.
#           focal 은 가장 흔한 갈래인 복호화 전 HTTPS 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, INFO, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 880, 736
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 DEEP DIVE",
      "원문 필터에 0줄일 때",
      "트래픽은 오가는데 http 나 dns 필터에 아무것도 안 잡힐 때의 판단. http 는 UDP 443 이면 QUIC, 복호화 전이면 TLS 레코드만, 복호화했는데도 0줄이면 HTTP/2 를 의심한다. dns 는 853 연결이 있으면 DoT, 없으면 443 에 섞인 DoH 나 캐시를 의심한다.",
      "필터가 비었다고 트래픽이 없는 것이 아닙니다 — 버전과 암호화가 필터 이름을 바꿉니다")

CX, HW, HH = 244, 176, 26
RX, RW, RH = 668, 336, 52
R_LEFT = RX - RW / 2
ST = 84

def oval(cy, w, txt, c=INK):
    d.o.append(f'<rect x="{CX - w / 2}" y="{cy - 18}" width="{w}" height="36" rx="18" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(CX, cy + 5, txt, 13, c, kr(txt), "middle", 600)

def diamond(cy, txt):
    d.o.append(f'<polygon points="{CX},{cy - HH} {CX + HW},{cy} {CX},{cy + HH} {CX - HW},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(CX, cy + 5, txt, 13, INK, kr(txt), "middle", 600)

def card(cx, cy, title, sub, c, focal=False):
    x, y = cx - RW / 2, cy - RH / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{RW}" height="{RH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(x, y, RW, RH, c, 6)
    d.t(cx, y + 22, title, 13, c, kr(title), "middle", 600)
    d.t(cx, y + 40, sub, 12, MUTED, kr(sub))

MK = {INFO: "info", WARN: "warn", ACC: "acc"}

def side(cy, lab, c):
    d.arrow([(CX + HW + 4, cy), (R_LEFT - 4, cy)], c, MK[c], 1.4)
    d.t(CX + HW + 24, cy - 8, lab, 12, c, KR, "start", 600)

def down(cy_from, cy_to, lab, top_pad=HH):
    d.arrow([(CX, cy_from + HH + 4), (CX, cy_to - top_pad - 4)], MUTED, "ar", 1.4)
    d.t(CX + 12, cy_from + HH + 22, lab, 12, MUTED, KR, "start", 600)

def block_tag(y, txt):
    d.t(24, y, txt, 12, SOFT, MONO, "start", 600)

# 블록 A — http 필터 0줄
block_tag(112, "HTTP")
A0 = 116
oval(A0, 200, "http 필터에 0줄")
A1, A2, A3 = A0 + 74, A0 + 74 + ST, A0 + 74 + 2 * ST
d.arrow([(CX, A0 + 18 + 4), (CX, A1 - HH - 4)], MUTED, "ar", 1.4)
diamond(A1, "UDP 443 이 오가나?")
side(A1, "예", INFO); card(RX, A1, "HTTP/3 · QUIC", "quic · http3 필터", INFO)
down(A1, A2, "아니오")
diamond(A2, "TLS 를 복호화했나?")
side(A2, "아니오", ACC); card(RX, A2, "복호화 전 HTTPS", "tls 레코드만 보임 · 4장 복호화", ACC, True)
down(A2, A3, "예", RH / 2)
card(CX, A3, "HTTP/2 일 수 있음", "바이너리 프레임 · http2 필터", WARN)

# 경계
DIV = A3 + RH / 2 + 36
d.line(24, DIV, W - 24, DIV, RULE, 1.0, "4 4")

# 블록 B — dns 필터 0줄
block_tag(DIV + 36, "DNS")
B0 = DIV + 40
oval(B0, 200, "dns 필터에 0줄")
B1, B2 = B0 + 74, B0 + 74 + ST
d.arrow([(CX, B0 + 18 + 4), (CX, B1 - HH - 4)], MUTED, "ar", 1.4)
diamond(B1, "853 연결이 보이나?")
side(B1, "예", INFO); card(RX, B1, "DoT", "TLS 로 감싼 DNS · tcp.port == 853", INFO)
down(B1, B2, "아니오", RH / 2)
card(CX, B2, "DoH 나 캐시", "443 에 섞인 HTTPS · TTL 안의 답", WARN)

d.legend(H - 56, [("가장 흔한 갈래", ACC), ("필터 이름이 바뀜", INFO), ("더 가려 봐야 하는 갈래", WARN)])
d.save("05-02.filter-miss-triage.svg")
