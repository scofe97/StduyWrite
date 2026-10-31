# 08-03 §1 — 병원 당직 의사 동시 취소로 인한 쓰기 스큐 이상 시퀀스
# 검증(10-31 cc-ddia-dverify08): 결과 라벨을 본문 §1 "당직 의사 0명—요구 사항 위반" 표현으로
# 사실 출처: 08-03 §1(L25~L48), 원서 Ch.8 p.29~30 Figure 8-8
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
YBOT = 464
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "08-03 · §1 WRITE SKEW SEQUENCE", "당직 의사 동시 취소로 인한 쓰기 스큐 이상",
         "두 의사가 동시에 당직 2명 이상을 확인하고 자신을 제외하여 당직 의사가 0명이 되는 경쟁 조건",
         "동시 SELECT 검사 · 스냅샷 격리 · 상호 미인식 갱신 · 커밋 성공 · 불변 조건 위반")

s.lanes([
    ("의사 Aaliyah", "트랜잭션 1"),
    ("데이터베이스", "doctors (shift_id=1234)"),
    ("의사 Bryce", "트랜잭션 2"),
], lane_w=200)

s.rails(YBOT)

# 초기 DB 상태
s.box(428 - 140, 160, 280, 26, PAPER, RULE, 0.8)
s.t(428, 177, "초기: Aaliyah(True), Bryce(True) · 당직 2명", 11, INFO, KR, "middle")

# t1: 시작
s.state("의사 Aaliyah", "BEGIN", 200, INFO)
s.state("의사 Bryce", "BEGIN", 200, INFO)

# t2: Aaliyah 당직 조회
s.msg("의사 Aaliyah", "데이터베이스", "SELECT COUNT(*) (당직 의사 수)", 232, INFO, sub="WHERE on_call = true (반환: 2명)")

# t3: Bryce 당직 조회
s.msg("의사 Bryce", "데이터베이스", "SELECT COUNT(*) (당직 의사 수)", 272, INFO, sub="스냅샷 조회 (반환: 2명)")

# t4: Aaliyah 취소 UPDATE
s.msg("의사 Aaliyah", "데이터베이스", "UPDATE doctors (on_call=false)", 316, WARN, sub="WHERE name = 'Aaliyah'")

# t5: Bryce 취소 UPDATE
s.msg("의사 Bryce", "데이터베이스", "UPDATE doctors (on_call=false)", 356, WARN, sub="WHERE name = 'Bryce'")

# t6: 커밋
s.msg("의사 Aaliyah", "데이터베이스", "COMMIT (성공)", 396, OK)
s.msg("의사 Bryce", "데이터베이스", "COMMIT (성공)", 424, OK)

# 최종 DB 상태: 당직 0명 이상
s.tone(428 - 146, 442, 292, 26, BAD, 4, "20", 1.2)
s.t(428, 459, "최종: 당직 0명 · 요구 사항 위반", 11, BAD, KR, "middle", 600)

s.legend(LEG, [("스냅샷 조회", INFO), ("개별 행 갱신", WARN), ("커밋 완료", OK), ("전제 붕괴·당직 0명", BAD)])
s.save("08-03.write-skew-serializability.svg")
