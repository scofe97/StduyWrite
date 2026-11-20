# 사실 출처: internal/core/service.go:1344-1429, internal/core/lifecycle.go:1223-1255, internal/store/store.go:678-690, internal/core/data.go:117-127, 201-235
# 타입 스펙: type-sequence
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

class SeqDeploy(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 80
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 20, y + 22, lab, 11, MUTED, KR, "start")
            x += int(_w(lab, 11)) + 24

    def rails(s, ybot, scratch_ybot=None):
        for k, x in s.LX.items():
            yb = scratch_ybot if (k == "scratch" and scratch_ybot) else ybot
            s.line(x, s.lane_top + 6, x, yb, RULE, 1.0, "3 6")
            if k == "scratch" and scratch_ybot:
                s.line(x - 5, yb - 5, x + 5, yb + 5, RULE, 1.2)
                s.line(x - 5, yb + 5, x + 5, yb - 5, RULE, 1.2)

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        w_lbl = _w(label, 11)
        s.o.append(f'<rect x="{mx - w_lbl/2 - 4}" y="{y - 18}" width="{w_lbl + 8}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            w_sub = _w(sub, 10)
            s.o.append(f'<rect x="{mx - w_sub/2 - 4}" y="{y + 3}" width="{w_sub + 8}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, to_left=False):
        x = s.LX[a]
        if not to_left:
            s.path(f"M {x + 10} {y - 8} L {x + 50} {y - 8} L {x + 50} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            w_lbl = _w(label, 11)
            s.o.append(f'<rect x="{x + 54}" y="{y - 14}" width="{w_lbl + 8}" height="15" fill="{PAPER}"/>')
            s.t(x + 58, y - 3, label, 11, c, _kr(label), "start", 600)
            if sub:
                w_sub = _w(sub, 10)
                s.o.append(f'<rect x="{x + 54}" y="{y + 3}" width="{w_sub + 8}" height="14" fill="{PAPER}"/>')
                s.t(x + 58, y + 13, sub, 10, MUTED, _kr(sub), "start")
        else:
            s.path(f"M {x - 10} {y - 8} L {x - 50} {y - 8} L {x - 50} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            w_lbl = _w(label, 11)
            s.o.append(f'<rect x="{x - 62 - w_lbl}" y="{y - 14}" width="{w_lbl + 8}" height="15" fill="{PAPER}"/>')
            s.t(x - 58, y - 3, label, 11, c, _kr(label), "end", 600)
            if sub:
                w_sub = _w(sub, 10)
                s.o.append(f'<rect x="{x - 62 - w_sub}" y="{y + 3}" width="{w_sub + 8}" height="14" fill="{PAPER}"/>')
                s.t(x - 58, y + 13, sub, 10, MUTED, _kr(sub), "end")

W, H = 980, 830
d = SeqDeploy(
    W, H,
    "CORE · DEPLOY EXECUTION SEQUENCE",
    "배포 실행 및 무중단 전환 시퀀스",
    "격리 사본 헬스체크, DB 스냅샷, 새 런타임 기동, CAS 포인터 원자 전이, 옛 핸들러 5초 드레인 흐름",
    "헬스체크 실패 시 라이브 데이터를 건드리지 않음"
)

NAMES = [
    ("웹 콘솔 / CLI", "127.0.0.1:7878"),
    ("Flats Core", "deployLocked"),
    ("격리 사본 (Scratch)", "health-check/"),
    ("Store (SQLite)", "flats.db (CAS)"),
    ("Worker Runtime", "live data worker")
]
KEYS = ["console", "core", "scratch", "store", "runtime"]
d.LX = {"console": 95, "core": 290, "scratch": 490, "store": 690, "runtime": 885}

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 80, 100, 160, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, MONO)

d.lane_top = 144
d.rails(H - 85, scratch_ybot=345)

# 1. 승인 결정 및 배포 호출
d.msg("console", "core", "Decide(apr-...) 승인", 175, WARN, "warn", sub="deployLocked(vN) 실행")

# 2. 사본 데이터 헬스체크 시작
d.msg("core", "scratch", "checkIsolated", 225, INFO, "info", sub="captureEnv 후 사본 데이터 생성")

# 3. 헬스체크 GET / (15s timeout, 2xx/3xx)
d.selfmsg("scratch", "GET / (15s timeout)", 275, INFO, sub="X-Flats-Health: 1 (200 OK)")

# 4. 헬스체크 성공 응답
d.msg("scratch", "core", "HealthResult 통과", 325, OK, "ok", sub="scratch 디렉터리 즉시 제거")

# 5. DB 스냅샷 생성
d.msg("core", "store", "snapshotDB", 375, MUTED, "ar", sub="flat data DB → snapshots/")

# 6. 스냅샷 생성 응답
d.msg("store", "core", "스냅샷 저장 완료", 425, MUTED, "ar", sub="before-v<n>-<ms>.sqlite")

# 7. 라이브 데이터로 새 런타임 기동
d.msg("core", "runtime", "buildWithEnvironment", 475, ACC, "acc", sub="live 데이터로 새 worker 시작")

# 8. 원자적 live_version CAS 갱신
d.msg("core", "store", "UPDATE flats SET live_version=N", 525, WARN, "warn", sub="WHERE live_version=previous")

# 9. CAS 성공 커밋
d.msg("store", "core", "RowsAffected = 1 (성공)", 575, OK, "ok", sub="deployments 이력 함께 커밋")

# 10. 활성 핸들러 원자 교체
d.msg("core", "runtime", "lf.cur.Swap(new)", 625, OK, "ok", sub="신규 트래픽 즉시 전환")

# 11. 이전 핸들러 드레인 (왼쪽으로 루프하여 우측 잘림 방지)
d.selfmsg("runtime", "구버전 5초 drain", 675, SOFT, sub="in-flight 처리 후 Stop()", to_left=True)

# 12. 최종 성공 응답 반환
d.msg("core", "console", "DeployResult 반환", 725, OK, "ok", sub="live_version = N 활성화 완료")

# 범례
d.legend(780, [
    ("운영자 승인 / CAS 쿼리", WARN),
    ("사본 헬스체크 (격리)", INFO),
    ("새 런타임 기동", ACC),
    ("검증 통과 / 커밋 완료", OK),
    ("구버전 드레인", SOFT)
])

out_path = _HERE.parent / "01-03-deploy-sequence.svg"
d.save(str(out_path))
print(f"saved: {out_path}")

