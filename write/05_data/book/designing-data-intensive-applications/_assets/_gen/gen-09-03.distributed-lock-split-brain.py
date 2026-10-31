# 09-03 §2 — 분산 락과 프로세스 멈춤으로 인한 스플릿 브레인 오염 시퀀스
# 사실 출처: 09-03 §2(L35~L43), 원서 Ch.9 Figure 9-4(An incorrect implementation of a distributed lock)
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

s = KSeq(W, H, "09-03 · §2 DISTRIBUTED LOCK BUG", "분산 락과 프로세스 멈춤의 스플릿 브레인 오염",
         "클라이언트 1의 GC 포즈 중 리스가 만료되어 클라이언트 2가 새 리스를 얻어 쓰기 후, 깨어난 클라이언트 1의 중복 쓰기로 파일이 오염되는 시퀀스",
         "원서 Figure 9-4 · 리스 만료 미인지 · 좀비 노드 쓰기 · 저장소 무차단 · 파일 오염")

s.lanes([
    ("클라이언트 1", "구 리스 보유자"),
    ("락 서비스", "분산 락 관리"),
    ("클라이언트 2", "신규 리스 보유자"),
    ("저장소", "스토리지 서비스"),
], lane_w=170)

s.rails(YBOT)

# 1. 클라이언트 1 리스 획득
s.msg("클라이언트 1", "락 서비스", "리스 획득 요청", 172, INFO)
s.msg("락 서비스", "클라이언트 1", "리스 부여 완료", 204, OK)

# 2. 클라이언트 1 일시 멈춤
s.state("클라이언트 1", "GC 포즈 멈춤 (15초)", 238, WARN)

# 3. 락 서비스에서 리스 만료
s.state("락 서비스", "리스 만료 타임아웃", 270, BAD)

# 4. 클라이언트 2 리스 획득 및 파일 쓰기
s.msg("클라이언트 2", "락 서비스", "리스 획득 요청", 304, INFO)
s.msg("락 서비스", "클라이언트 2", "신규 리스 부여", 336, OK)
s.msg("클라이언트 2", "저장소", "파일 쓰기 요청", 368, OK)
s.msg("저장소", "클라이언트 2", "쓰기 완료 응답", 400, OK)

# 5. 클라이언트 1 재개 및 덮어쓰기 오염
s.state("클라이언트 1", "멈춤 해제 · 리스 유효 착각", 434, WARN)
s.msg("클라이언트 1", "저장소", "지연된 파일 쓰기", 468, BAD, dash="4 3")

# 6. 저장소 파일 오염
s.state("저장소", "파일 오염 · 스플릿 브레인", 500, BAD)

s.legend(LEG, [
    ("리스 발급", INFO),
    ("정상 쓰기", OK),
    ("프로세스 포즈", WARN),
    ("만료·오염 쓰기", BAD),
])

s.save("09-03.distributed-lock-split-brain.svg")
