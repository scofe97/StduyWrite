# 사실 출처: go1.25.1 src/os/signal/signal.go:278, src/net/http/server.go:3451, src/net/http/server.go:3179, go doc os/signal.NotifyContext, go doc net/http.Server
# 타입 스펙: type-sequence
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 656

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        lw = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in str(label)) + 12
        s.box(mx - lw / 2, y - 19, lw, 15, fill=PAPER, stroke=PAPER, sw=0, r=3)
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            sw = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in str(sub)) + 12
            s.box(mx - sw / 2, y + 4, sw, 15, fill=PAPER, stroke=PAPER, sw=0, r=3)
            s.t(mx, y + 15, sub, 11, MUTED, _kr(sub), "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = _kr(txt)
        w = sum(10.5 if "가" <= ch <= "힣" else 6.6 for ch in str(txt)) + 16
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, fam)

d = SeqKR(W, H,
          "SIGNAL PROPAGATION AND GRACEFUL SHUTDOWN",
          "종료 신호 전파와 Shutdown 기한 분리 흐름",
          "signal.NotifyContext 와 BaseContext 를 통한 요청 취소 전파 및 새 기한 context 기반 Shutdown 순서",
          "종료 신호 context 는 요청 취소에 쓰고 Shutdown 은 새 기한 context 로 호출합니다")

lanes = d.lanes([
    ("kubelet / OS", "SIGTERM · SIGKILL"),
    ("main 고루틴", "NotifyContext · stop()"),
    ("http.Server", "BaseContext · Shutdown"),
    ("Handler", "r.Context().Done()"),
], y0=96, lane_w=176)

d.rails(568)

def sec(y, txt, c):
    w = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 12
    d.box(42, y - 13, w, 18, fill=PAPER, stroke=PAPER, sw=0, r=3)
    d.t(48, y, txt, 11, c, fam=KR, anchor="start", weight=600)

# 1. 요청 context 뿌리 연결
sec(160, "1. 요청 context 뿌리 연결", INFO)
d.msg("main 고루틴", "http.Server", "BaseContext -> ctx", 192, INFO, "info", sub="Serve 시작 시 baseCtx 설정")
d.msg("http.Server", "Handler", "ConnContext -> r.Context()", 236, INFO, "info", sub="요청별 파생 context 전달")

# 2. SIGTERM 도착과 요청 취소 전파
sec(280, "2. SIGTERM 전파와 신호 해제", ACC)
d.msg("kubelet / OS", "main 고루틴", "SIGTERM", 312, ACC, "acc", sub="ctx.Done() 닫힘")
d.msg("main 고루틴", "Handler", "r.Context().Done() 열림", 356, ACC, "acc", dash="4 3", sub="BaseContext 통해 즉시 전파")
d.state("main 고루틴", "stop() 호출", 396, WARN)

# 3. 새 기한 context 로 Shutdown
sec(436, "3. 새 기한 context 로 Shutdown", OK)
d.msg("main 고루틴", "http.Server", "Shutdown(sctx)", 468, OK, "ok", sub="WithTimeout < 30s 유예 시간")
d.msg("http.Server", "main 고루틴", "Serve -> ErrServerClosed", 512, MUTED, "ar", dash="4 3", sub="RegisterOnShutdown 콜백 실행")
d.msg("http.Server", "main 고루틴", "활성 연결 종료 후 nil 반환", 552, OK, "ok", dash="4 3")

# 범례
d.legend(588, [
    ("context 계층", INFO),
    ("신호 전파 (focal)", ACC),
    ("기본 신호 복원", WARN),
    ("새 기한 Shutdown", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.signal-shutdown-sequence.svg"))
d.save(out_path)
