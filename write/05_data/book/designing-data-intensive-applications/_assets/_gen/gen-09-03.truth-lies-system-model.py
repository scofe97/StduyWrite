# 09-03 §3 — 단조 증가 펜싱 토큰을 통한 좀비 쓰기 차단 시퀀스
# 사실 출처: 09-03 §3(L45~L57), 원서 Ch.9 Figure 9-6(Making access to storage safe by allowing writes only in the order of increasing fencing tokens)
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class KSeq(Seq):
    def lanes(self, names, y0=104, lane_w=170):
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

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)


W = 880
PY = 104
YBOT = 516
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "09-03 · §3 FENCING TOKEN DEFENSE", "펜싱 토큰을 통한 좀비 쓰기 방어",
         "단조 증가 토큰(33 -> 34)을 발급받은 클라이언트의 쓰기를 저장소가 검증하여 만료된 33 토큰 쓰기를 거부하는 시퀀스",
         "단조 증가 토큰 · 최신 토큰 기억 · 구버전 토큰 거부")

s.lanes([
    ("클라이언트 1", "구 토큰 33"),
    ("락 서비스", "토큰 발급자"),
    ("클라이언트 2", "신규 토큰 34"),
    ("저장소", "토큰 검증 스토리지"),
], lane_w=170)

s.rails(YBOT)

# 1. 클라이언트 1 토큰 33 획득
s.msg("클라이언트 1", "락 서비스", "리스 획득 요청", 172, INFO)
s.msg("락 서비스", "클라이언트 1", "토큰 33 발급 완료", 204, OK)

# 2. 클라이언트 1 일시 멈춤
s.state("클라이언트 1", "긴 멈춤", 238, WARN)

# 3. 락 서비스에서 리스 만료
s.state("락 서비스", "리스 만료 타임아웃", 270, BAD)

# 4. 클라이언트 2 토큰 34 획득 및 쓰기 성공
s.msg("클라이언트 2", "락 서비스", "리스 획득 요청", 304, INFO)
s.msg("락 서비스", "클라이언트 2", "토큰 34 발급 완료", 336, OK)
s.msg("클라이언트 2", "저장소", "쓰기 요청 (토큰 34)", 368, OK)
s.msg("저장소", "클라이언트 2", "수락 완료 (최신 34 저장)", 400, OK)

# 5. 클라이언트 1 재개 및 구토큰 쓰기 시도
s.state("클라이언트 1", "멈춤 해제 · 유효 착각", 434, WARN)
s.msg("클라이언트 1", "저장소", "쓰기 요청 (토큰 33)", 468, WARN, dash="4 3")

# 6. 저장소 거부 (33 < 34)
s.state("저장소", "쓰기 거부 (33 < 34)", 500, BAD)

s.legend(LEG, [
    ("토큰 발급", INFO),
    ("수락 쓰기", OK),
    ("프로세스 포즈", WARN),
    ("거부 차단", BAD),
])

s.save("09-03.truth-lies-system-model.svg")
