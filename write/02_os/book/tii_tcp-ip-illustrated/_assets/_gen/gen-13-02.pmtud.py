# 13-02 §7 — TCP 의 PMTUD 를 원서 13.4.1 의 구성(라우터 한쪽 링크만 MTU 를 줄인 비대칭)으로 재현한 캡처.
# 값 출처: OrbStack Ubuntu(커널 7.0.14) 네트워크 네임스페이스 c · r · s, 2026-10-04. r 의 s 쪽 링크만 MTU 1000, 나머지 1500, 오프로딩 끔.
#   SYN/SYN-ACK 모두 mss 1460 · DF. c 가 1448바이트 세그먼트 5개(IP 1500, DF)를 보내자 r 이 5번 모두
#   ICMP "need to frag (mtu 1000)" 로 답했다. 이어 같은 7240바이트를 948바이트 7개 + 604바이트 1개(IP 1000 · 656)로 다시 보냈다.
#   전송 뒤 c 의 라우트 캐시: "cache expires 597sec mtu 1000".
# 타입 스펙: type-sequence — 주체 셋(클라이언트 · 라우터 · 서버) 사이의 시간순 메시지. 라우터에서 멈춘 세그먼트는 ✕ 로 끊는다.
#           focal 은 PTB 를 받은 뒤 948바이트로 다시 보낸 세그먼트 묶음 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 600
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §7",
          "PTB 를 받고 세그먼트를 줄이는 TCP",
          "라우터의 서버 쪽 링크만 MTU 를 1000 으로 줄였다. 양 끝은 MSS 1460 을 주고받고 DF 를 켠 1500바이트 세그먼트를 보내지만, 라우터는 그것을 넘기지 못하고 "
          "ICMP Packet Too Big(mtu 1000)으로 돌려보낸다. 클라이언트 TCP 는 같은 바이트를 948바이트 세그먼트로 다시 보내고, 경로 MTU 1000 을 600초 동안 기억한다.",
          "작은 SYN 은 지나가고 큰 데이터만 막힙니다 — 그래서 PTB 가 꼭 돌아와야 합니다")

C, R, S = "클라이언트 c", "라우터 r", "서버 s"
d.lanes([(C, "10.0.1.2 · MTU 1500"), (R, "s 쪽 링크 MTU 1000"), (S, "10.0.2.2 · MTU 1500")], y0=100, lane_w=208)
d.rails(520)
xc, xr, xs = d.LX[C], d.LX[R], d.LX[S]

# 1. 핸드셰이크 — 작아서 그대로 지나감
d.msg(C, S, "SYN · SYN,ACK · ACK", 196, MUTED, "ar", sub="mss 1460 · 60바이트라 통과")
# 2. 큰 세그먼트 — 라우터에서 멈춤
d.msg(C, R, "데이터 1448B × 5", 260, INFO, "info", sub="IP 1500 · DF")
d.path(f"M {xr + 10} 260 L {xr + 60} 260", INFO, 1.5, dash="5 4")
d.t(xr + 70, 265, "✕", 15, BAD, KR, "start", 700)
# 3. PTB
d.msg(R, C, "ICMP PTB × 5", 324, WARN, "warn", sub="need to frag (mtu 1000)")
# 4. 다시 보냄 — 948바이트
d.msg(C, S, "같은 7240B 를 948B × 7 + 604B", 388, ACC, "acc", sub="IP 1000 · DF · 이번엔 통과")
# 5. ACK
d.msg(S, C, "ACK", 444, MUTED, "ar", dash="5 4")
# 라우트 캐시
d.chip((xc + xr) / 2, 488, "c 의 route cache · mtu 1000 · 600초", OK, 12)

d.legend(H - 56, [("줄인 크기로 다시 보낸 세그먼트", ACC), ("Packet Too Big", WARN), ("처음 크기의 세그먼트", INFO), ("기억한 경로 MTU", OK)])
d.save("13-02.pmtud.svg")
