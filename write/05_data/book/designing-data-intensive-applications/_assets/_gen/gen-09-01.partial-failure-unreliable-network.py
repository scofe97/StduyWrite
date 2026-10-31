# 09-01 §2 — 비신뢰 네트워크에서 요청과 응답이 사라지거나 지연되는 6가지 장애 경로 시퀀스 다이어그램.
# 사실 출처: 09-01 본문 §2(L37~L56), 원서 Ch.9 Unreliable Networks — Figure 9-1
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 676
H = LEG + 56

class NetSeq(Seq):
    def lanes(self, names, y0=104, lane_w=190):
        self.LX = {}
        n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_arrow(self, x1, x2, y, c, label, sub=None, dash=None, mk="ar"):
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

d = NetSeq(W, H, "09-01 · §2 UNRELIABLE NETWORKS", "비신뢰 네트워크의 6가지 요청·응답 장애 갈래",
           "비동기 패킷망에서 요청과 응답이 유실·지연되는 경로와 송신자의 구분 불가 한계.",
           "요청 유실 · 큐 대기 · 노드 크래시 · GC 일시 중단 · 응답 유실 · 지연 도착")

lx = d.lanes([
    ("송신자 클라이언트", "CLIENT / SENDER"),
    ("비동기 네트워크", "ASYNCHRONOUS NETWORK"),
    ("원격 수신 노드", "REMOTE SERVER / RECEIVER"),
])

x_c = lx["송신자 클라이언트"]
x_n = lx["비동기 네트워크"]
x_s = lx["원격 수신 노드"]

d.rails(560)

# 1. 정상 경로 (비교 기준)
y_norm = 174
d.t(36, y_norm - 10, "정상 기준선 — 요청 및 응답 양방향 완결", 12, OK, KR, "start", 600)

d.seq_arrow(x_c, x_s, y_norm + 18, OK, "요청 패킷 전송 및 처리", "정상 왕복", mk="ok")
d.seq_arrow(x_s, x_c, y_norm + 58, OK, "응답 패킷 정상 수신", "처리 완료", mk="ok")

d.line(24, 256, W - 24, 256, RULE, 0.8, "3 4")

# 2. [갈래 1·2] 요청 단계 장애 (Figure 9-1 a 와 본문 갈래 1·2)
y_req = 280
d.t(36, y_req - 4, "요청 단계 — 유실·대기", 12, SOFT, KR, "start", 600)

d.seq_arrow(x_c, x_n - 144, y_req + 20, INFO, "요청 패킷 송신", "전송 시도", mk="info")

# 네트워크 내 유실 표시
d.tone(x_n - 134, y_req + 2, 268, 38, BAD, 4, "16", 1.1)
d.t(x_n, y_req + 25, "(1) 케이블 뽑힘 유실 · (2) 큐 대기 (과부하)", 11, BAD, KR, "middle", 600)

d.line(24, 348, W - 24, 348, RULE, 0.8, "3 4")

# 3. [갈래 3·4] 원격 노드 장애 (원서 Figure 9-1 b)
y_node = 376
d.t(36, y_node - 10, "원격 노드 — 크래시·중단", 12, SOFT, KR, "start", 600)

d.seq_arrow(x_c, x_s - 144, y_node + 20, INFO, "요청 패킷 도착", "네트워크 통과", mk="info")

# 노드 내 크래시 / GC 중단 표시
d.tone(x_s - 124, y_node + 2, 218, 38, BAD, 4, "16", 1.1)
d.t(x_s - 15, y_node + 25, "(3) 노드 크래시 · (4) GC 일시 중단", 11, BAD, KR, "middle", 600)

d.line(24, 444, W - 24, 444, RULE, 0.8, "3 4")

# 4. [갈래 5·6] 응답 단계 장애 (원서 Figure 9-1 c)
y_resp = 472
d.t(36, y_resp - 10, "응답 단계 — 유실·지연", 12, SOFT, KR, "start", 600)

d.seq_arrow(x_c, x_s, y_resp + 16, INFO, "요청 정상 도달 및 처리", "요청 처리", mk="info")
d.seq_arrow(x_s, x_n + 144, y_resp + 62, BAD, "응답 패킷 송신", "처리 후 반환", mk="bad")

# 네트워크 내 응답 유실 표시
d.tone(x_n - 134, y_resp + 44, 268, 38, BAD, 4, "16", 1.1)
d.t(x_n, y_resp + 67, "(5) 응답 패킷 유실 · (6) 과부하 지연 미도착", 11, BAD, KR, "middle", 600)

d.line(24, 560, W - 24, 560, RULE, 0.8, "3 4")

# 5. 송신자 최종 결론: 타임아웃 및 구분 불가 (focal banner)
d.tone(24, 574, W - 48, 80, ACC, 6, "18", 1.4)
d.chip(120, 594, "송신자 관점 귀결", ACC, 11)
d.t(x_c, 628, "타임아웃 만료", 13, ACC, KR, "middle", 600)
d.t(W / 2 + 50, 602, "송신자는 위 6가지 장애 원인을 구분 불가능", 13, INK, KR, "middle", 600)
d.t(W / 2 + 50, 630, "응답 미도착 사실만 인지 · TCP ACK는 커널 수신일 뿐 애플리케이션 완료 보장 불가", 11, SOFT, KR, "middle")

d.legend(LEG, [
    ("핵심 한계 (focal)", ACC),
    ("정상 완료", OK),
    ("요청 전달", INFO),
    ("유실·크래시", BAD),
])

d.save("09-01.partial-failure-unreliable-network.svg")
