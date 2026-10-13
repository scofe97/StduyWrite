# 타입 스펙: type-sequence — 참여자 다섯(앱·libssl · 진입 probe · 맵 · 반환 probe · perf 버퍼), 메시지 아홉과 점선 반환 하나. focal 은 맵에 맡기고 꺼내는 update·lookup 두 메시지.
# 사실 출처: pixie-io/pixie-demos main(HEAD 6806d84) openssl-tracer/openssl_tracer_bpf_funcs.c — 29~32행(키는 bpf_get_current_pid_tgid 의 스레드 ID, 값은 buf 포인터), 63행(len = PT_REGS_RC(ctx)),
#   76~77행(bpf_probe_read 와 tls_events.perf_submit), 121~133행(probe_entry_SSL_read: PT_REGS_PARM2, update), 135~150행(probe_ret_SSL_read: lookup, process_SSL_data, delete),
#   추출본 ebpf8.txt 764~770행(진입 probe 에서만 인자, 버퍼는 반환 뒤에 참), 836~838행(항목 정리). tgid << 32 | 스레드 ID 는 02-02 노트의 커널 helpers.c 인용.
# Layout conventions: 레인 중심 x 100·284·468·652·836(stride 184, 상자 w=176), 메시지 stride 52~56(y=196 시작). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 11)/2}" y="{y + 5}" width="{_w(sub, 11)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.o.append(f'<rect x="{x + 62}" y="{y - 20}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(x + 68, y - 6, label, 13 if _kr(label) == KR else 12, c, _kr(label), "start", 600)
        if sub:
            s.o.append(f'<rect x="{x + 62}" y="{y}" width="{_w(sub, 11)}" height="18" fill="{PAPER}"/>')
            s.t(x + 68, y + 12, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub), "start")

W, H = 960, 700
d = SeqKR(W, H, "LEARNING EBPF · 08-02 §1", "진입 probe 가 buf 를 맵에 맡기고 반환 probe 가 같은 키로 평문을 꺼낸다",
          "SSL_read(s, buf, num) 가 불리면 진입 probe 가 PT_REGS_PARM2 의 buf 를 active_ssl_read_args_map 에 pid_tgid 키로 update 한다. 라이브러리가 복호화해 buf 를 채우고 반환하면 반환 probe 가 같은 키로 lookup 해 process_SSL_data 를 부르고, 평문 data_len 바이트(최대 MAX_DATA_SIZE)를 tls_events 로 perf_submit 한 뒤 delete 한다.",
          "인자는 진입에서만, 평문과 길이는 반환에서만 얻습니다")

NAMES = (("앱 · libssl", "SSL_read"), ("진입 probe", "uprobe"), ("맵", "active_ssl_read_args_map"),
         ("반환 probe", "uretprobe"), ("perf 버퍼", "tls_events"))
KEYS = ["app", "ent", "map", "ret", "perf"]
d.LX = {"app": 100, "ent": 284, "map": 468, "ret": 652, "perf": 836}
for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 11, MUTED, MONO)
d.lane_top = 144
d.rails(H - 80)

d.msg("app", "ent", "SSL_read(s, buf, num)", 196, MUTED, "ar")
d.selfmsg("ent", "buf = PT_REGS_PARM2", 252, MUTED, "둘째 인자")
d.msg("ent", "map", "update(pid_tgid, &buf)", 308, ACC, "acc", sub="키 = tgid << 32 | 스레드 ID")
d.selfmsg("app", "복호화해 buf 를 채움", 364, MUTED)
d.msg("app", "ret", "반환 · len = PT_REGS_RC", 424, MUTED, "ar")
d.msg("ret", "map", "lookup(pid_tgid)", 476, ACC, "acc")
d.msg("map", "ret", "*buf", 512, MUTED, "ar", dash="6 4")
d.msg("ret", "perf", "perf_submit(event)", 568, OK, "ok", sub="평문 data_len 바이트")
d.msg("ret", "map", "delete(pid_tgid)", 624, INFO, "info")

d.legend(H - 56, [("맵에 맡김 · 꺼냄", ACC), ("평문이 올라감", OK), ("정리", INFO)])
d.save("08-02.ssl-read-sequence.svg")
