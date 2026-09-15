# 04-02 §5 버퍼블로트 — ACK 클록킹의 실제 전송 흐름. 가정용 라우터 큐에서 하나가 나가면
# 한 RTT 뒤 그 ACK 가 세그먼트를 하나 불러들여 같은 큐에 넣는다. 나간 만큼 들어오니 큐 길이가 그대로다.
# 값은 원문 시나리오(전송 20 ms · 버스트 25)를 쓰되 RTT 는 원문 자신의 결론(21번째·큐 다섯)과 맞는 400 ms 다.
# 본문 정오 노트가 이 어긋남을 검산한다.
# 타입 스펙: type-sequence — 주체 넷 사이의 시간순 메시지. 한 바퀴가 곧 RTT 이고 큐 길이는 레인 옆 상태로 붙인다.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq 는 라벨 font 를 MONO 로 하드코딩한다 — 한글이 섞이면 갈라 쓴다(계약 §프리미티브)."""
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dxn = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dxn} {y} L {x2 - 12 * dxn} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(str(txt)) * (12.0 if any("가" <= ch <= "힣" for ch in str(txt)) else 7.0) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt), "middle", 600)


d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §5",
          "하나가 나가면 하나가 들어옵니다",
          "원문 Figure 4.10 의 ACK 클록킹. 가정용 라우터의 출력 큐에서 세그먼트가 하나 나가고 한 RTT 뒤 그 ACK 가 "
          "세그먼트를 하나 더 불러들여 같은 큐에 넣으므로, 손실이 없는데도 큐 길이가 줄지 않고 지연이 그대로 남는다.",
          "나간 만큼 들어오니 큐 길이 다섯이 유지됩니다")

d.lanes([("TCP 송신자", "home host"),
         ("출력 큐", "home router"),
         ("병목 링크", "20 ms / pkt"),
         ("게임 서버", "remote")], y0=104, lane_w=196)
d.rails(474)

# 한 바퀴 — 큐에서 나감 → 링크 → 서버 → ACK → 새 세그먼트 → 같은 큐로
d.state("출력 큐", "큐 길이 5", 166, ACC)

d.msg("출력 큐", "병목 링크", "세그먼트 하나 나감", 206, OK, "ok", sub="큐 −1")
d.msg("병목 링크", "게임 서버", "링크 위 20 ms", 246, MUTED, "ar", sub="병목 속도")
d.msg("게임 서버", "TCP 송신자", "ACK", 292, INFO, "info", sub="한 RTT 뒤 도착")
d.msg("TCP 송신자", "출력 큐", "ACK 가 하나를 더 부름", 338, ACC, "acc", sub="큐 +1")

d.state("출력 큐", "큐 길이 5", 386, ACC)
d.t(d.LX["출력 큐"], 416, "그대로", 13, ACC, KR, "middle", 600)

# 한 바퀴 = RTT 표시
RX = 40
d.line(RX, 206, RX, 338, SOFT, 1.0, "4 4")
d.line(RX, 206, RX + 10, 206, SOFT, 1.0)
d.line(RX, 338, RX + 10, 338, SOFT, 1.0)
d.t(RX + 16, 268, "한 바퀴", 13, SOFT, KR, "start", 600)
d.t(RX + 16, 286, "= RTT", 12, SOFT, MONO, "start")

# 결과 — 정상 상태 식
d.tone(300, 440, 400, 46, ACC, 6, "14", 1.4)
d.t(500, 460, "정상 상태 큐 = 윈도 − 대역폭·지연 곱", 13, ACC, KR, "middle", 600)
d.t(500, 478, "25 − 20 = 5", 12, SOFT, MONO)

d.legend(H - 44, [("큐에서 나감", OK), ("ACK", INFO), ("ACK 가 불러들인 세그먼트 · 줄지 않는 큐", ACC)])
d.save("04-02.ack-clocking.svg")
