# 타입 스펙: type-sequence
# 사실 출처: internal/store/lifecycle.go:395-411, internal/store/store.go:678-690
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqCAS(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')
        s.o.insert(20, f'<marker id="bad_right" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{BAD}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

W, H = 960, 620
d = SeqCAS(
    W, H,
    "STORE · CONCURRENT DEPLOY CAS RACE",
    "동시 활성화 요청의 Compare-And-Swap 충돌 해결",
    "동일 버전을 읽은 두 배포 요청이 경합할 때 한 요청만 행 갱신에 성공하고 다른 요청은 충돌 오류로 롤백되는 시퀀스",
    "WHERE live_version=previous 조건으로 갱신 영향 행 수를 검사해 묵시적 덮어쓰기 방지 (잠금·승인 검사 없는 일반론)"
)

NAMES = (
    ("배포 요청 A", "대상 v2 활성화 (기존 v1)"),
    ("Flats Store (SQLite)", "flats.db (live_version)"),
    ("배포 요청 B", "대상 v3 활성화 (기존 v1)")
)
d.LX = {"req_a": 160, "db": 480, "req_b": 800}
KEYS = ["req_a", "db", "req_b"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 110, 100, 220, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, MONO)

d.lane_top = 144
d.rails(H - 76)

# 초기 상태: live_version = 1
d.state("db", "현재 live_version = 1", 170, INFO)

# 1. 두 요청 모두 live_version=1 조회
d.msg("db", "req_a", "조회 응답", 204, INFO, "info", sub="현재 live_version = 1")
d.msg("db", "req_b", "조회 응답", 232, INFO, "info", sub="현재 live_version = 1")

# 2. 요청 A 의 선행 UPDATE (CAS 시도)
d.msg("req_a", "db", "UPDATE flats SET live_version=2", 280, ACC, "acc", sub="WHERE slug='demo' AND live_version=1")

# DB 상태 전이: 1행 갱신 성공
d.box(350, 312, 260, 40, fill=PAPER2, stroke=OK, sw=1.2, r=4)
d.t(480, 328, "RowsAffected = 1 (갱신 성공)", 11, OK, KR, "middle", 600)
d.t(480, 344, "live_version: 1 → 2 커밋", 10, MUTED, MONO, "middle")

# 요청 A 에 성공 응답
d.msg("db", "req_a", "성공 응답 (HTTP 200)", 376, OK, "ok", sub="live_version=2 반영 완료")

# 3. 요청 B 의 후행 UPDATE (동일 조건으로 CAS 시도)
d.msg("req_b", "db", "UPDATE flats SET live_version=3", 424, WARN, "warn", sub="WHERE slug='demo' AND live_version=1")

# DB 검사: 0행 갱신 (조건 불일치)
d.box(350, 456, 260, 40, fill=PAPER2, stroke=BAD, sw=1.2, r=4)
d.t(480, 472, "RowsAffected = 0 (조건 불일치)", 11, BAD, KR, "middle", 600)
d.t(480, 488, "현재 live_version은 2 (1이 아님)", 10, MUTED, KR, "middle")

# 요청 B 에 충돌 응답
d.msg("db", "req_b", "충돌 오류", 520, BAD, "bad_right", dash="4 3", sub="changed concurrently; retry")

# 범례
d.legend(574, [
    ("초기 버전 조회", INFO),
    ("선행 갱신 시도 (CAS)", ACC),
    ("1행 갱신 성공 (버전 승격)", OK),
    ("0행 불일치 충돌 (롤백)", BAD)
])

out_path = _HERE.parent / "01-01-cas-race.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
