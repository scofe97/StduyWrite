# 02-02 치트시트 — HTTP 층과 트랜스포트 층 사이를 패킷이 오가는 장면을 세 판에 걸쳐 추적한다.
# 막힌 자리가 판마다 어느 층으로 옮겨 가는지가 논지다. 셋 다 응답 방향(서버 → 브라우저)만 그린다.
#   막 1 — HTTP/1.1: 요청은 겹쳐 보내도 응답은 요청 순서 그대로 나가야 한다.
#           RFC 9112 §9.3.2 "MUST send the corresponding responses in the same order that the requests were received."
#           그래서 막히는 자리가 HTTP 층이다.
#   막 2 — HTTP/2: 프레임을 섞어 그 줄을 풀었지만 TCP 는 바이트 스트림 하나라 스트림 경계를 모른다 (원문 §2.2.6).
#           세그먼트 하나가 빠지면 뒤에 도착한 다른 스트림 것까지 붙든다 — 막히는 자리가 TCP 층으로 내려왔다.
#   막 3 — HTTP/3: QUIC 이 스트림마다 따로 신뢰 전송을 해 그 줄을 끊는다.
#           다만 혼잡 제어 단위는 스트림이 아니라 경로다 (RFC 9002 §7 "The congestion controller is per path").
# 세그먼트·프레임 번호는 장면을 위한 예시값이다. 원문에 이 수치 예는 없다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 메시지. 시간은 위에서 아래로 흐른다.
#           축약 1: 판이 셋이라 한 시간축을 가로 구분선으로 3막으로 나눈다. 스펙의 combined fragment 는
#                   operator 가 opt·alt·loop 로 한정돼 "세대"를 담지 못하므로 프레임 대신 구분선을 쓴다.
#           축약 2: 손실 메시지는 스펙의 message kind 넷 어디에도 없어, 중간에서 끊고 X 를 찍는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 1536
LANE_W, LANE_Y = 208, 112
SEND_H, SEND_T, RECV_T, RECV_H = "HTTP 송신", "전송 송신", "전송 수신", "HTTP 수신"


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t):
    return sum(13.0 if "가" <= c <= "힣" else 7.4 for c in str(t))


class SeqKR(Seq):
    """dd 의 Seq 는 라벨 폰트를 MONO 로 하드코딩한다. 한글이 섞이면 갈라 쓰도록 감싼다."""

    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 14, INK, KR, "middle", 600)
            s.t(x, y0 + 39, sub, 12, MUTED, MONO)
        s.lane_top = y0 + 48
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 13, MUTED, KR)

    def state(s, a, txt, y, c, focal=False):
        x = s.LX[a]
        w = _w(txt) + 26
        sw = 1.4 if focal else 1.1
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="4" '
                   f'fill="{c}14" stroke="{c}" stroke-width="{sw}"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))

    def lost(s, a, b, label, y, why):
        """중간에서 끊기고 사라지는 메시지. 스펙의 네 kind 어디에도 없어 따로 그린다."""
        x1, x2 = s.LX[a], s.LX[b]
        mx = (x1 + x2) / 2
        s.path(f"M {x1 + 10} {y} L {mx - 22} {y}", BAD, 1.5, dash="4 3")
        s.line(mx - 10, y - 10, mx + 10, y + 10, BAD, 1.8)
        s.line(mx - 10, y + 10, mx + 10, y - 10, BAD, 1.8)
        s.t(mx - 24, y - 12, label, 13, BAD, _kr(label), "end", 600)
        s.t(mx + 20, y + 5, why, 13, BAD, KR, "start")


d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 SUMMARY",
          "막히는 자리가 층을 따라 내려갑니다",
          "서버가 보낸 응답이 HTTP 층과 트랜스포트 층을 거쳐 브라우저에 닿기까지. 세 판을 같은 시간축 위에 쌓아, 판마다 어디서 줄이 서는지 대조한다.",
          "1.1 은 HTTP 층에서, 2 는 TCP 층에서 막힙니다. 3 은 그 줄을 끊고 혼잡 윈도만 남깁니다")

d.lanes([(SEND_H, "server"), (SEND_T, "TCP / QUIC"),
         (RECV_T, "TCP / QUIC"), (RECV_H, "browser")], LANE_Y, LANE_W)


def act(y, num, title, sub):
    d.line(20, y, W - 48, y, RULE, 1.0)
    d.t(20, y + 26, num, 13, SOFT, MONO, "start", 600)
    d.t(72, y + 26, title, 15, INK, KR, "start", 600)
    # 제목은 15px 이므로 13px 기준 _w 에 배율을 곱한다. 폭 추정 오차 ±15% 를 감안해 여유를 더 둔다.
    d.t(72 + _w(title) * 1.16 + 24, y + 26, sub, 13, MUTED, KR, "start")


def note(y, txt, c):
    d.t(20, y, txt, 13, c, KR, "start")


# 막 1 — HTTP/1.1 · 응답 순서가 묶여 있다
act(176, "01", "HTTP/1.1 · 지속 연결 + 파이프라이닝", "요청은 겹쳐 보냄")
d.state(SEND_H, "요청 R1 R2 R3 접수", 244, MUTED)
d.msg(SEND_H, SEND_T, "응답 O1 · 큰 객체", 284, MUTED, sub="O2·O3 는 뒤에서 기다림")
d.msg(SEND_T, RECV_T, "seg 1 ~ seg 4", 324, MUTED)
d.msg(RECV_T, RECV_H, "O1 전달", 364, OK)
d.state(SEND_H, "이제야 O2 차례", 404, BAD)
d.msg(SEND_H, SEND_T, "응답 O2", 444, MUTED)
d.msg(SEND_T, RECV_T, "seg 5", 484, MUTED)
d.msg(RECV_T, RECV_H, "O2 전달", 524, OK)
note(556, "막힌 자리는 HTTP 층 · 응답을 요청 순서로 묶어 두어, 앞의 큰 객체가 끝나야 뒤가 출발함", BAD)

# 막 2 — HTTP/2 · 응답 순서는 풀렸지만 TCP 가 다시 묶는다
act(580, "02", "HTTP/2 · 프레임 인터리빙", "한 TCP 연결에 세 스트림을 섞음")
d.msg(SEND_H, SEND_T, "프레임 1a 2a 3a 1b 2b", 648, OK, sub="세 스트림을 번갈아 내보냄")
d.msg(SEND_T, RECV_T, "seg 1 · 1a 2a 3a", 688, MUTED)
d.lost(SEND_T, RECV_T, "seg 2 · 1b 2b", 728, "도중에 사라짐")
d.msg(SEND_T, RECV_T, "seg 3 · 3b 1c", 768, MUTED)
d.state(RECV_T, "seg 3 은 왔지만 못 올려보냄", 808, ACC, focal=True)
d.msg(RECV_T, RECV_H, "seg 1 분량까지만", 848, WARN)
d.state(RECV_H, "스트림 2·3 도 함께 멈춤", 888, BAD)
d.msg(SEND_T, RECV_T, "seg 2 재전송", 928, MUTED, dash="4 3")
d.msg(RECV_T, RECV_H, "밀려 있던 것 일괄 전달", 968, OK)
note(1000, "막힌 자리가 TCP 층으로 내려왔음 · 바이트 스트림 하나라 스트림 경계를 몰라, 상관없는 스트림까지 붙듦", BAD)

# 막 3 — HTTP/3 · 스트림마다 따로 센다
act(1012, "03", "HTTP/3 · QUIC 스트림", "패킷마다 스트림 번호가 박혀 있음")
d.msg(SEND_H, SEND_T, "프레임 1a 2a 3a 1b 2b", 1080, OK, sub="보내는 모습은 HTTP/2 와 같음")
d.lost(SEND_T, RECV_T, "pkt · 스트림 1", 1120, "도중에 사라짐")
d.msg(SEND_T, RECV_T, "pkt · 스트림 2", 1160, MUTED)
d.msg(SEND_T, RECV_T, "pkt · 스트림 3", 1200, MUTED)
d.msg(RECV_T, RECV_H, "스트림 2·3 바로 전달", 1240, OK)
d.state(RECV_T, "스트림 1 만 기다림", 1280, WARN)
d.msg(SEND_T, RECV_T, "스트림 1 재전송", 1320, MUTED, dash="4 3")
d.msg(RECV_T, RECV_H, "스트림 1 전달", 1360, OK)
note(1392, "순서의 줄은 끊겼음 · 그래도 혼잡 윈도는 경로 단위라, 이 손실 하나가 세 스트림의 전송 속도를 함께 낮춤", WARN)

d.rails(1404)

d.t(20, 1440, "세 막을 같은 눈으로 읽으면, 판이 바뀔 때마다 막히는 자리가 HTTP 층에서 TCP 층으로, 다시 혼잡 제어로 옮겨 간 것이 보",
    13, MUTED, KR, "start")
d.t(20, 1464, "애플리케이션 층에서 아무리 잘게 쪼개도 그 아래 층이 다시 묶으면 소용이 없다는 것이 HTTP/3 이 트랜스포트를 갈아치운 이유",
    13, SOFT, KR, "start")

d.legend(1488, [("전달됨", OK), ("전송 중", MUTED), ("대기·부분 전달", WARN),
                ("사라지거나 막힘", BAD), ("TCP 가 스트림을 모르는 자리", ACC)])
d.save("02-02.hol-across-layers.svg")
