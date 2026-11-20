# 사실 출처: internal/runtime/manager.go:243-305,355-385,602-625 · internal/runtime/worker.go:46-95 · internal/runtime/protocol.go:52-65,90-95
# 타입 스펙: type-sequence
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 730

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub), "middle")

    def selfmsg(s, a, label, y, c=MUTED, sub=None, to_left=False):
        x = s.LX[a]
        dx = -42 if to_left else 42
        d_arrow = -1 if to_left else 1
        s.path(f"M {x + 10 * d_arrow} {y - 10} L {x + dx} {y - 10} L {x + dx} {y + 10} L {x + 12 * d_arrow} {y + 10}", c, 1.4, m="ar")
        anchor = "end" if to_left else "start"
        tx = x + dx - 8 if to_left else x + dx + 8
        s.t(tx, y - 4, label, 11, c, _kr(label), anchor, 600)
        if sub:
            s.t(tx, y + 14, sub, 10, MUTED, _kr(sub), anchor)

d = SeqKR(
    W, H,
    "PROCESS LIFECYCLE · SPAWN TO SHUTDOWN SEQUENCE",
    "flats worker 프로세스 기동·프록시·종료 시퀀스",
    "부모 프로세스는 fd 3 소켓과 stdin 한 줄 spec으로 자식을 띄우고 stderr ready로 준비를 확인합니다",
    lead="flats serve (Manager) ── fd 3 Unix Socket / stdin spec ──> flats worker (WorkerMain)"
)

lanes = d.lanes([
    ("방문자", "HTTP Client"),
    ("flats serve", "Manager (부모)"),
    ("flats worker", "WorkerMain (자식)")
], y0=96, lane_w=180)

d.rails(670)

def sec(y, txt, c):
    w = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 16
    d.box(28, y - 13, w, 20, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.t(36, y + 2, txt, 11, c, fam=KR, anchor="start", weight=600)

# 1. 프로세스 생성 및 준비 확인
sec(158, "1. worker 스폰 및 ready", INFO)
d.selfmsg("flats serve", "net.Listen(\"unix\", sock)", 182, INFO, sub="ul.File() -> lf")
d.msg("flats serve", "flats worker", "exec.Command(Exe, \"worker\")", 220, ACC, "acc", sub="ExtraFiles = [lf] // fd 3")
d.msg("flats serve", "flats worker", "stdin: {\"flat\":...,\"version\":1}\\n", 258, MUTED, "ar", sub="workerSpec JSON 한 줄")
d.selfmsg("flats worker", "os.NewFile(3) -> FileListener", 296, INFO, sub="f.Close() · srv.Serve(ln)", to_left=True)
d.msg("flats worker", "flats serve", "stderr: {\"t\":\"ready\",\"ms\":<ms>}\\n", 334, OK, "ok", sub="childMsg ready")

# 2. HTTP 요청 프록시
sec(374, "2. HTTP 요청 프록시", OK)
d.msg("방문자", "flats serve", "GET / (<slug>.localhost:7879)", 402, MUTED, "ar")
d.msg("flats serve", "flats worker", "in.proxy.ServeHTTP (in.sock)", 440, OK, "ok", sub="Unix 소켓 요청 프록시")
d.msg("flats worker", "flats serve", "HTTP 200 OK (text/html)", 480, OK, "ok")
d.msg("flats serve", "방문자", "HTTP 200 OK", 512, MUTED, "ar")

# 3. 정상 종료
sec(548, "3. stdin EOF 감지 및 종료", WARN)
d.msg("flats serve", "flats worker", "stdin.Close() // EOF", 574, WARN, "warn", sub="in.Stop() 또는 부모 종료")
d.selfmsg("flats worker", "srv.Shutdown(ctx, 2s)", 610, WARN, sub="자원 해제", to_left=True)
d.msg("flats worker", "flats serve", "Process Exit (<-p.done)", 648, MUTED, "ar", sub="cmd.Wait() 완료 · Stop() 소켓 정리")

d.legend(692, [
    ("프로세스 제어 / IPC", ACC),
    ("정상 HTTP 트래픽", OK),
    ("준비 / 내부 바인딩", INFO),
    ("종료 시그널", WARN)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02-spawn-sequence.svg"))
d.save(out)
print(f"saved: {out}")
