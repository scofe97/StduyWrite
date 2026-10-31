# 10-03 §3 — Lamport 클럭 타임스탬프 갱신과 전순서 시퀀스
# 사실 출처: 10-03 본문 §3(L55~L69), 원서 DDIA 2nd Edition Ch. 10 p.25~26 Figure 10-9
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class KSeq(Seq):
    def lanes(self, names, y0=104, lane_w=200):
        self.LX = {}; n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if _hangul(sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = self.LX[a], self.LX[b]; d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 9, label, 11, c, KR if _hangul(label) else MONO, "middle", 600)
        if sub:
            self.t(mx, y + 17, sub, 11, MUTED, KR if _hangul(sub) else MONO)

    def selfmsg(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 11, c, KR if _hangul(label) else MONO, "start", 600)
        if sub:
            self.t(x + 68, y + 13, sub, 11, MUTED, KR, "start")

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)


W = 880
PY = 104
Y_RAILS = 468
BOX_Y = 484
LEG = BOX_Y + 70 + 24
H = LEG + 52

s = KSeq(W, H, "10-03 · §3 LAMPORT CLOCK SEQUENCE", "Lamport 클럭 타임스탬프 갱신과 전순서 보장",
         "세 노드가 메시지를 주고받으며 카운터를 동기화하고 인과적으로 일관된 전순서를 구성하는 과정",
         "로컬 카운터 1 증가 · 최댓값 기반 수신 갱신 · 카운터 우선 비교 · 노드 ID 동점 해결")

s.lanes([
    ("Aaliyah", "로컬 카운터"),
    ("Bryce", "로컬 카운터"),
    ("Caleb", "로컬 카운터"),
], lane_w=200)

s.rails(Y_RAILS)

# t0: 초기 상태 (카운터 0)
s.state("Aaliyah", "카운터: 0", 168, SOFT)
s.state("Bryce", "카운터: 0", 168, SOFT)
s.state("Caleb", "카운터: 0", 168, SOFT)

# t1: Aaliyah, Caleb 독립 로컬 이벤트로 카운터 1 증가
s.state("Aaliyah", "카운터 1 증가 (1)", 206, INFO)
s.state("Caleb", "카운터 1 증가 (1)", 206, WARN)

# t2: 메시지 전송 (Aaliyah -> Bryce, Caleb -> Bryce)
s.msg("Aaliyah", "Bryce", "id: (1, 'Aaliyah')", 248, INFO, sub="text: '점심 어디 갈까?'")
s.msg("Caleb", "Bryce", "id: (1, 'Caleb')", 292, WARN, sub="text: '모두 안녕' (동시 전송)")

# t3: Bryce 수신 및 카운터 갱신 max(0, 1) = 1
# (수신 갱신과 답장 증가를 한 칩으로 둔다. 본문은 max+1 규칙, 원서 p26 은 max 뒤 증가)

# t4: Bryce 로컬 이벤트로 카운터 1 증가 (1 + 1 = 2)
s.state("Bryce", "수신 뒤 답장 · 카운터 2", 356, ACC)

# t5: Bryce 답장 전송 (Bryce -> Aaliyah, Bryce -> Caleb)
s.msg("Bryce", "Aaliyah", "id: (2, 'Bryce')", 414, ACC, sub="text: '@Aaliyah 팔라펠 가게 투표'")
s.msg("Bryce", "Caleb", "id: (2, 'Bryce')", 448, ACC, sub="text: '@Aaliyah 팔라펠 가게 투표'")

# 하단 전순서 판정 및 인과성 보장 요약 박스
s.box(24, BOX_Y, W - 48, 64, PAPER2, RULE, 1.0)
s.t(W / 2, BOX_Y + 24, "전순서 비교 규칙: 카운터 우선 비교 후, 동점 시 노드 ID 사전 순 비교", 12, INK, KR, "middle", 600)
s.t(W / 2, BOX_Y + 46, "최종 순서: (1, 'Aaliyah') < (1, 'Caleb') < (2, 'Bryce') · Aaliyah → Bryce 인과 선행 일관 보장", 11, ACC, KR, "middle")

s.legend(LEG, [
    ("초기 상태", SOFT),
    ("Aaliyah 전송", INFO),
    ("Caleb 동시 전송", WARN),
    ("Bryce 답장 (focal)", ACC),
])

s.save("10-03.lamport-clock-order.svg")
