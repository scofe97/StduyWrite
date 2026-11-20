# 사실 출처: internal/app/serve.go:179-340,732-825 · internal/app/setup.go:99-440 · internal/store/migrate.go:221-290 · internal/core/secrets.go:24-86 · docs/design.md:47-65
# 타입 스펙: type-sequence
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class StartupSeq(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)

    def rails(s, ybot):
        for x in s.LX.values():
            s.line(x, s.lane_top + 6, x, ybot, RULE, 1.0, "3 6")

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        w_lbl = _w(label, 10)
        s.o.append(f'<rect x="{mx - w_lbl/2 - 4}" y="{y - 17}" width="{w_lbl + 8}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 6, label, 10, c, _kr(label), "middle", 600)
        if sub:
            w_sub = _w(sub, 9)
            s.o.append(f'<rect x="{mx - w_sub/2 - 4}" y="{y + 3}" width="{w_sub + 8}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 9, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 8} L {x + 46} {y - 8} L {x + 46} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        w_lbl = _w(label, 10)
        s.o.append(f'<rect x="{x + 50}" y="{y - 14}" width="{w_lbl + 8}" height="15" fill="{PAPER}"/>')
        s.t(x + 54, y - 3, label, 10, c, _kr(label), "start", 600)
        if sub:
            w_sub = _w(sub, 9)
            s.o.append(f'<rect x="{x + 50}" y="{y + 2}" width="{w_sub + 8}" height="14" fill="{PAPER}"/>')
            s.t(x + 54, y + 13, sub, 9, MUTED, _kr(sub), "start")

W, H = 980, 600
s = StartupSeq(
    W, H,
    "FLATS SERVE · LIFECYCLE SEQUENCE",
    "flats serve 기동 및 정상 종료 수명주기 시퀀스",
    "잠금 획득 · 설정 검증 · 마이그레이션 · 시크릿 바인딩 · 리버스 드레인",
    lead="flats.lock 획득 후 단계를 밟고 종료 시 역순으로 5초 드레인 후 락을 해제합니다"
)

LANES = [
    ("Service", "launchd / systemd"),
    ("Host Daemon", "Serve / Start"),
    ("Data Lock", "flats.lock"),
    ("Config & Secret", "config.json / key"),
    ("SQLite Store", "flats.db (WAL)"),
    ("Listeners", ":7878 / :7879"),
]

s.lanes(LANES, y0=96, lane_w=128)
s.rails(525)

# 1. Startup phase
s.msg("Service", "Host Daemon", "Serve(--config)", 155, OK, sub="시작 진입")
s.msg("Host Daemon", "Data Lock", "flock(LOCK_EX|LOCK_NB)", 190, WARN, sub="flats.lock 획득")
s.msg("Host Daemon", "Config & Secret", "Load() / Create()", 225, INFO, sub="config.json 검증")
s.msg("Host Daemon", "SQLite Store", "Inspect & useWAL()", 260, INFO, sub="백업 후 마이그레이션")
s.msg("Host Daemon", "Config & Secret", "Link(secret.key)", 295, OK, sub="32B 원자적 링크")
s.msg("Host Daemon", "Listeners", "LISTEN 7878/7879", 330, OK, sub="제공자·관리서버 바인딩")

# Divider line
s.line(24, 368, W - 24, 368, RULE, 0.8, "4 4")
w_div = _w("정상 종료 흐름 (역순 정리)", 10)
s.o.append(f'<rect x="{W/2 - w_div/2 - 4}" y="360" width="{w_div + 8}" height="16" fill="{PAPER}"/>')
s.t(W / 2, 372, "정상 종료 흐름 (역순 정리)", 10, SOFT, KR, "middle")

# 2. Shutdown phase
s.msg("Service", "Host Daemon", "SIGINT / SIGTERM", 400, BAD, sub="종료 신호 수신")
s.msg("Host Daemon", "Listeners", "Shutdown(5s)", 440, WARN, sub="관리 서버 드레인")
s.msg("Host Daemon", "SQLite Store", "Store.Close()", 480, MUTED, sub="DB 핸들 정리")
s.msg("Host Daemon", "Data Lock", "Close()", 515, OK, sub="flats.lock 해제")

s.legend(550, [
    ("정상 진입·바인딩", OK),
    ("잠금·드레인", WARN),
    ("종료 신호", BAD),
    ("검증·마이그레이션", INFO),
])

out_path = _HERE.parent / "05-01-startup-sequence.svg"
s.save(str(out_path))
print(f"Generated {out_path}")
