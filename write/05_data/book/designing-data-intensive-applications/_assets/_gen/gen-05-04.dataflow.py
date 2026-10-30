# 05-04 §1 — DB 데이터플로우에서 옛 코드가 새 필드를 지운 채 다시 쓰는 모습(data outlives code).
# 사실 출처: 05-04 §1(L33~L35, 롤링 업그레이드 중 옛 코드가 새 데이터를 읽어 forward 호환 필요), 원서 Dataflow Through Databases(PDF p.18).
# 덮어쓰기 유실 장면은 05-04 본문에 없고 원서 Figure 5-1(PDF p.3)·05-01 §2 에 있다. 값은 Figure 5-1 의 Person·favoriteNumber 42·photoURL 만 쓴다.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class KSeq(Seq):
    # dd.Seq 는 lane 부제·메시지·상태 라벨을 MONO 로 찍는다. 한글이 든 라벨은 KR 로 갈라 쓴다.
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
        x1, x2 = self.LX[a], self.LX[b]; dr = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 9, label, 11, c, KR if _hangul(label) else MONO, "middle", 600)
        if sub: self.t(mx, y + 17, sub, 11, MUTED)

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(11.0 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)

W = 880
H = 590
LEG = H - 56

s = KSeq(W, H, "05-04 · DATAFLOW THROUGH DATABASES", "DB 데이터플로우와 forward 호환성 결여 시의 필드 유실",
        "롤링 업그레이드 중 새 버전 앱이 쓴 레코드를 옛 버전 앱이 읽고 갱신할 때 미지 필드가 삭제되는 순서.",
        "새 버전 기록 · 옛 버전 조회 · 미지 필드 탈락 · 덮어쓰기 유실")

# 3개 참여자 레인
s.lanes([
    ("새 버전 앱 (v2)", "photoURL 을 아는 코드"),
    ("데이터베이스 (DB)", "Person 레코드"),
    ("옛 버전 앱 (v1)", "photoURL 을 모르는 코드"),
], y0=104, lane_w=210)

s.rails(468)

# 1. v2 가 DB에 새 필드 포함 INSERT
s.msg("새 버전 앱 (v2)", "데이터베이스 (DB)", "레코드 쓰기 (photoURL 포함)", 172, INFO, mk="info", sub="새 필드가 든 레코드 저장")

# 2. DB 상태
s.state("데이터베이스 (DB)", "photoURL 보관", 212, INFO)

# 3. v1 이 DB 조회
s.msg("옛 버전 앱 (v1)", "데이터베이스 (DB)", "레코드 읽기", 256, MUTED, dash="4 4", sub="롤링 업그레이드 중 옛 버전 코드가 조회")

# 4. DB 가 레코드 반환
s.msg("데이터베이스 (DB)", "옛 버전 앱 (v1)", "반환 (photoURL 포함)", 298, MUTED, dash="4 4", sub="저장된 레코드 그대로")

# 5. v1 에서 미지 필드 누락 (왼쪽 방향 self-loop 로 캔버스 내부 유지)
x_v1 = s.LX["옛 버전 앱 (v1)"]
s.path(f"M {x_v1-10} 338 L {x_v1-58} 338 L {x_v1-58} 358 L {x_v1-13} 358", WARN, 1.4, m="warn")
s.t(x_v1-68, 344, "미지 필드 photoURL 탈락", 12, WARN, KR, "end", 600)
s.t(x_v1-68, 362, "모델 객체로 디코딩하며 누락", 12, MUTED, KR, "end")

# 6. v1 이 갱신 후 다시 쓰기 (새 필드 유실된 채)
s.msg("옛 버전 앱 (v1)", "데이터베이스 (DB)", "favoriteNumber = 42 로 다시 쓰기", 404, BAD, mk="bad", sub="photoURL 빠진 레코드로 덮어쓰기")

# 7. DB 상태 유실
s.state("데이터베이스 (DB)", "photoURL 값 소실 (데이터 손실)", 448, BAD)

# 하단 해결 원칙 박스 (40자 이내 명사구)
s.box(24, 480, W - 48, 40, PAPER2, OK, 1.2)
s.t(W / 2, 505, "forward 호환성 원칙 · 미지 필드 보존으로 덮어쓰기 유실 방지", 12, OK, KR, "middle", 600)

s.legend(LEG, [("신규 스키마 기록", INFO), ("조회 및 응답", MUTED), ("미지 필드 탈락", WARN), ("덮어쓰기 유실", BAD), ("호환성 보장 원칙", OK)])
s.save("05-04.dataflow.svg")
