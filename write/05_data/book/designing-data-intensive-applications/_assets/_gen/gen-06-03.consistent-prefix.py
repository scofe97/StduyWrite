# 06-03 §4 — 샤드별 복제 지연 차이로 인해 관찰자가 질문보다 답변을 먼저 읽어 인과율이 역전되는 consistent prefix reads 위반 시퀀스.
# 사실 출처: 06-03 §4(L66~L70), 원서 Ch.6 p.21 Figure 6-5
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class KSeq(Seq):
    # dd.Seq 는 레인 부제·메시지·상태 칩을 MONO 로 찍는다. 한글이 든 텍스트는 KR 로 쓴다.
    def lanes(self, names, y0=104, lane_w=210):
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
        self.t(mx, y - 9, label, 12 if _hangul(label) else 11, c, KR if _hangul(label) else MONO, "middle", 600)
        if sub:
            self.t(mx, y + 17, sub, 11, MUTED, KR if _hangul(sub) else MONO)

    def selfmsg(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 12 if _hangul(label) else 11, c, KR if _hangul(label) else MONO, "start", 600)
        if sub:
            self.t(x + 68, y + 13, sub, 11, MUTED, KR, "start")

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)

W = 880
PY = 104
YBOT = 422
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "06-03 · §4 CONSISTENT PREFIX READS ANOMALY", "consistent prefix reads 이상 시퀀스",
        "샤드별 복제 지연 차이로 인해 관찰자가 질문보다 답변을 먼저 읽어 인과율이 역전되는 현상",
        "인과 의존 대화 · 샤드 1 긴 복제 지연 · 샤드 2 빠른 복제 전파 · 답변 선행 관찰 · 인과율 위반")

# 참여자 레인 5개
s.lanes([
    ("Mr. Poons", "질문자"),
    ("샤드 1", "질문 샤드 (지연 긺)"),
    ("Mrs. Cake", "답변자"),
    ("샤드 2", "답변 샤드 (지연 짧음)"),
    ("관찰자", "Observer")
], y0=PY, lane_w=128)

s.rails(YBOT)

# 1. Mr. Poons -> 샤드 1 (질문 쓰기)
s.msg("Mr. Poons", "샤드 1", "\"얼마나 먼 미래를 볼 수 있나요?\"", 176, ACC, mk="acc", sub="질문 전송 (원인)")

# 2. Mr. Poons -> Mrs. Cake (대화 청취)
s.msg("샤드 1", "Mrs. Cake", "\"얼마나 먼 미래를 볼 수 있나요?\"", 218, ACC, mk="acc", dash="3 3", sub="Mrs. Cake가 질문을 들음 (인과 의존)")

# 3. Mrs. Cake -> 샤드 2 (답변 쓰기)
s.msg("Mrs. Cake", "샤드 2", "\"보통 10초 뒤를 봅니다\"", 260, INFO, mk="info", sub="답변 전송 (결과)")

# 4. 샤드 2 -> 관찰자 (빠른 복제 전파로 답변 먼저 도착)
s.msg("샤드 2", "관찰자", "\"보통 10초 뒤를 봅니다\"", 304, OK, mk="ok", sub="[1] 답변 먼저 수신 (지연 짧음)")

# 5. 샤드 1 -> 관찰자 (긴 복제 지연으로 질문 뒤늦게 도착)
s.msg("샤드 1", "관찰자", "\"얼마나 먼 미래를 볼 수 있나요?\"", 350, WARN, mk="warn", dash="4 4", sub="[2] 질문 나중에 수신 (지연 긺)")

# 6. 관찰자 인과 역전 상태
ox = s.LX["관찰자"]
s.box(ox - 84, 386, 168, 24, PAPER, BAD, 1.1)
s.t(ox, 402, "인과율 역전: 답 먼저 관찰!", 11, BAD, KR, "middle", 600)

s.legend(LEG, [("질문 쓰기", ACC), ("답변 쓰기", INFO), ("답변 선행 수신", OK), ("질문 지연 도착", WARN), ("인과 역전 이상", BAD)])
s.save("06-03.consistent-prefix.svg")
