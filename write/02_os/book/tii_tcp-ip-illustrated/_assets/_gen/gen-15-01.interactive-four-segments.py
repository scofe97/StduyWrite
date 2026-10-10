# 타입 스펙: type-sequence — 주체 둘 사이의 1바이트 키 입력 왕복 4단계 세그먼트 흐름.
# 사실 출처: ch15.txt 91~189행, 258~266행 — IPv4 20B, TCP 20B, ssh 페이로드 48B, 순수 ACK 40B, 1B 입력당 87B 오버헤드.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 4 * dd} {y} L {x2 - 4 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 520
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-01 §1",
          "글자 하나를 칠 때 오가는 네 세그먼트 (개념 흐름)",
          "대화형 ssh 연결에서 클라이언트가 문자 'd' 하나를 누르면 지연 ACK 가 없을 때 키 전송, 확인 응답, 원격 셸 에코, 에코 확인까지 "
          "총 네 세그먼트가 오간다(실제 캡처는 지연 ACK 로 셋). 1바이트 입력을 전달하기 위해 암호화 48바이트와 헤더 40바이트가 붙어 88바이트가 된다.",
          "1바이트 페이로드에 87바이트의 헤더와 암호화 오버헤드가 따릅니다")

C, S = "클라이언트", "서버"
d.lanes([(C, "ssh 클라이언트"), (S, "원격 sshd · 셸")], y0=104, lane_w=240)
d.rails(450)
xc, xs = d.LX[C], d.LX[S]

def note(side, y, txt, c=SOFT):
    if side == C: d.t(xc - 20, y + 4, txt, 11, c, _kr(txt), "end")
    else: d.t(xs + 20, y + 4, txt, 11, c, _kr(txt), "start")

# 1. 키 입력 'd' 송신
Y1 = 180
d.msg(C, S, "seq 0:48 (48B) · PSH, ACK", Y1, INFO, "info", sub="총 88B (IP 20B + TCP 20B + ssh 48B)")
note(C, Y1, "키 'd' 입력", INFO)
note(S, Y1, "sshd 버퍼 수신", MUTED)

# 2. 키 ACK
Y2 = 240
d.msg(S, C, "ack 48 (0B) · ACK", Y2, MUTED, "ar", dash="4 4", sub="총 40B 순수 ACK (페이로드 0B)")
note(S, Y2, "수신 확인", MUTED)

# 3. 셸 에코 'd' 송신
Y3 = 300
d.msg(S, C, "seq 0:48 (48B) · PSH, ACK", Y3, WARN, "warn", sub="총 88B 에코 데이터 (문자 'd' 출력)")
note(S, Y3, "셸 에코 발생", WARN)
note(C, Y3, "화면 출력", MUTED)

# 4. 에코 ACK
Y4 = 360
d.msg(C, S, "ack 48 (0B) · ACK", Y4, MUTED, "ar", dash="4 4", sub="총 40B 순수 ACK (페이로드 0B)")
note(C, Y4, "에코 수신 확인", MUTED)

# 지연 ACK 편승 시 비교 칩
d.box(W / 2 - 140, 416, 280, 32, PAPER2, OK, 1.0, 6)
d.t(W / 2, 436, "지연 ACK 적용 시 2번과 3번이 한 세그먼트로 결합", 11, OK, KR, "middle", 600)

d.legend(H - 46, [
    ("데이터 (88B)", INFO),
    ("에코 (88B)", WARN),
    ("순수 ACK (40B)", MUTED),
    ("지연 ACK 편승", OK)
])

d.save("15-01.interactive-four-segments.svg")
