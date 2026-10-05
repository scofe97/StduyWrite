# 13-01 §7 — NAT 가 페이로드를 고쳐 쓰면 순서 번호와 ACK 번호까지 고쳐야 한다.
# 원문 13.2.6: NAT 는 SYN 비트로 연결의 시작을, 이어지는 SYN+ACK·ACK 로 수립 완료를 알아보고, TCP 상태 기계의 일부를 구현해
#   상태·방향별 순서 번호·ACK 번호를 추적한다. NAT 가 편집자처럼 데이터에 바이트를 넣거나 빼면 순서 번호와 길이가 달라지므로
#   그 값을 맞춰 고쳐야 하고, NAT 상태가 양 끝과 어긋나면 연결이 제대로 동작하지 않는다.
# 수치는 설명용 예시다(원문에 없는 값): 클라이언트가 seq 1000 부터 10바이트를 보내고 NAT 가 4바이트를 늘린다.
# 타입 스펙: type-sequence — 주체 셋(클라이언트 · NAT · 서버) 사이의 시간순 메시지. NAT 레인 옆 칩이 NAT 가 쥔 보정값이다.
#           focal 은 서버의 ACK 를 클라이언트가 아는 번호로 되돌리는 NAT 의 고쳐 쓰기 한 번.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def note(s, a, txt, y, c):
        x = s.LX[a]; w = len(txt) * 7.4 + 20 if not any("가" <= ch <= "힣" for ch in txt) else len(txt) * 12.5 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt), "middle", 600)

W, H = 920, 520
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §7",
          "페이로드를 고치는 NAT 는 번호도 고친다",
          "클라이언트가 seq 1000 부터 10바이트를 보내는데, 가운데 NAT 가 페이로드를 편집해 4바이트를 늘려 서버에 넘긴다. 서버는 14바이트를 받았으므로 ack 1014 를 돌려주고, "
          "NAT 는 그것을 클라이언트가 아는 번호 ack 1010 으로 되돌린다. 이후 이 방향의 번호는 계속 +4 만큼 어긋난 채 NAT 가 보정해야 한다. 수치는 설명용 예시다.",
          "NAT 의 상태가 양 끝과 어긋나면 연결이 제대로 동작하지 않습니다")

C, N, S = "클라이언트", "NAT", "서버"
d.lanes([(C, "seq 공간 A"), (N, "상태 · 보정값"), (S, "seq 공간 B")], y0=100, lane_w=200)
d.rails(440)

d.msg(C, N, "seq 1000 · 10바이트", 196, INFO, "info")
d.note(N, "페이로드 +4", 232, WARN)
d.msg(N, S, "seq 1000 · 14바이트", 268, INFO, "info")
d.msg(S, N, "ack 1014", 324, MUTED, "ar")
w = 120; x = d.LX[N]
d.o.append(f'<rect x="{x - w / 2}" y="{349}" width="{w}" height="22" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(x, 364, "ack − 4", 12, ACC, MONO, "middle", 600)
d.msg(N, C, "ack 1010", 396, ACC, "acc")

d.legend(H - 56, [("NAT 의 번호 되돌리기", ACC), ("NAT 가 페이로드를 바꾼 자리", WARN), ("데이터", INFO)])
d.save("13-01.nat-seq-rewrite.svg")
