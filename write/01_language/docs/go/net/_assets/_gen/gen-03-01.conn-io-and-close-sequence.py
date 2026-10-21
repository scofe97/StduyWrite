# 사실 출처: go1.25.1 src/internal/poll/fd_unix.go:141,360,91, src/runtime/netpoll.go:452, go doc net.Conn, io.Reader
# 타입 스펙: type-sequence
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 710

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        # lx: 라벨이 중간 생명선에 걸칠 때 라벨 x 를 옮긴다
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 11, MUTED, _kr(sub), "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = _kr(txt)
        w = len(str(txt)) * (11.0 if fam == KR else 7.0) + 16
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, fam)

d = SeqKR(W, H,
          "CONN READ WRITE CLOSE SEQUENCE",
          "Conn I/O 루프와 Close 의 unblock 시퀀스",
          "Read 부분 반환, Write 내부 루프, Close 의 런타임 evict 해제 흐름",
          "Read 는 즉시 반환하고 Write 는 루프를 돌며 Close 는 대기 고루틴을 깨웁니다")


def phase(y, txt, col):
    # 단계 라벨: 생명선 A 위에 PAPER 바탕 칩으로 얹어 선을 가린다. 폭은 글자 종류별로 어림한다
    w = sum(11 if "가" <= ch <= "힣" else 6.4 for ch in txt) + 16
    d.o.append(f'<rect x="40" y="{y-10}" width="{w:.0f}" height="20" rx="4" fill="{PAPER}" stroke="{col}" stroke-width="0.8"/>')
    d.t(48, y + 4, txt, 11, col, fam=KR, anchor="start")

lanes = d.lanes([
    ("고루틴 A (Reader)", "I/O 수행"),
    ("poll.FD", "internal/poll"),
    ("커널 소켓", "OS Socket"),
    ("고루틴 B (Closer)", "Close 호출")
], y0=96, lane_w=180)

d.rails(640)

# ── 1. Read 부분 읽기 (Partial Read) ──
phase(154, "1. Read 부분 읽기", INFO)
d.msg("고루틴 A (Reader)", "poll.FD", "Read(1024B)", 175, MUTED, "ar")
d.msg("poll.FD", "커널 소켓", "syscall.Read(1024B)", 205, MUTED, "ar")
d.msg("커널 소켓", "poll.FD", "512B 반환 (도착분)", 235, INFO, "info", dash="4 3")
d.msg("poll.FD", "고루틴 A (Reader)", "(512B, nil) 즉시 반환", 265, INFO, "info", dash="4 3")

# ── 2. Write 완전 쓰기 루프 (Write Loop) ──
phase(296, "2. Write 내부 루프", OK)
d.msg("고루틴 A (Reader)", "poll.FD", "Write(1024B)", 320, MUTED, "ar")
d.msg("poll.FD", "커널 소켓", "syscall.Write(1024B)", 345, MUTED, "ar")
d.msg("커널 소켓", "poll.FD", "512B 송신", 370, MUTED, "ar", dash="4 3")
# Write 내부 루프 재시도 (selfmsg)
d.selfmsg("poll.FD", "nn < len(p) 잔여분 루프", 395, OK)
d.msg("poll.FD", "커널 소켓", "syscall.Write(잔여 512B)", 425, MUTED, "ar")
d.msg("커널 소켓", "poll.FD", "512B 완료", 450, MUTED, "ar", dash="4 3")
d.msg("poll.FD", "고루틴 A (Reader)", "(1024B, nil) 완료 반환", 475, OK, "ok", dash="4 3")

# ── 3. Close unblock (evict) ──
phase(494, "3. Close 로 대기 해제", ACC)
# 고루틴 A 가 다시 Read 를 불렀지만 도착한 데이터가 없어 EAGAIN → waitRead 로 파킹된다
d.msg("고루틴 A (Reader)", "poll.FD", "Read() · 데이터 없음 (EAGAIN)", 530, MUTED, "ar")
d.state("고루틴 A (Reader)", "waitRead 대기", 553, WARN)
d.msg("고루틴 B (Closer)", "poll.FD", "Close() 호출", 580, MUTED, "ar", lx=(d.LX["커널 소켓"] + d.LX["고루틴 B (Closer)"]) / 2)
d.selfmsg("poll.FD", "pd.evict() → unblock", 603, ACC)
d.msg("poll.FD", "고루틴 A (Reader)", "net.ErrClosed 반환 (focal)", 630, ACC, "acc", dash="4 3")

# 범례
d.legend(660, [
    ("동기 시스템 콜", MUTED),
    ("부분 읽기 즉시 반환", INFO),
    ("완전 전송 보장 루프", OK),
    ("대기 파킹", WARN),
    ("Close 강제 해제 (focal)", ACC)
])

out_name = "03-01.conn-io-and-close-sequence.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
