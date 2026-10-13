# 타입 스펙: type-sequence — 참여자 둘(로더·커널), 호출 여섯과 다음 편으로 가는 점선 하나. focal 은 프로그램을 싣는 BPF_PROG_LOAD 한 줄.
# 사실 출처: 추출본 src/ebpf4.txt 183~196행(strace 윤곽)·192~269행(BTF_LOAD=3, MAP_CREATE=4·5)·302~304행(PROG_LOAD=6, insn_cnt=44)·372~373행(MAP_UPDATE_ELEM map_fd=5 = 0)
#   예제 저장소 chapter4/hello-buffer-config.py (HEAD 1ccef6e) — config[0]·config[501] 두 줄. 반환 fd 는 호출 화살표 옆 칩으로 붙여 메시지 수를 7개로 묶었다.
# Layout conventions: 레인 중심 x=160·560, 호출 간격 stride 64, 첫 호출 y=196, 반환 칩 열 x=660. 모든 좌표 4의 배수.
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
        s.o.append(f'<rect x="{mx - _w(label, 13)/2}" y="{y - 23}" width="{_w(label, 13)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 17, sub, 13, MUTED, _kr(sub))

W, H = 960, 700
d = SeqKR(W, H, "LEARNING EBPF · 04-01",
          "예제 로더가 낸 bpf() 호출과 돌려받은 fd",
          "hello-buffer-config.py 는 BTF 를 싣고 맵 둘을 만들고 프로그램을 싣고 맵에 값을 두 번 넣는다. 돌아온 fd 는 이후 호출의 인자로 다시 쓰인다.",
          "호출마다 돌아온 번호가 다음 호출에 다시 들어갑니다")

d.LX = {"로더": 176, "커널": 576}
for nm, sub, x in (("hello-buffer-config.py", "사용자 프로세스", 176), ("커널", "bpf() 시스템 콜", 576)):
    d.box(x - 112, 100, 224, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

# 반환 열 머리
d.t(660, 176, "반환", 13, SOFT, KR, "middle", 600)

rows = [
    ("BPF_BTF_LOAD",         "BTF 덩어리",                  INFO, "info", "fd 3"),
    ("BPF_MAP_CREATE",       "PERF_EVENT_ARRAY · output",   OK,   "ok",   "fd 4"),
    ("BPF_MAP_CREATE",       "HASH · config · btf_fd=3",    OK,   "ok",   "fd 5"),
    ("BPF_PROG_LOAD",        "KPROBE · hello · insn_cnt=44", ACC, "acc",  "fd 6"),
    ("BPF_MAP_UPDATE_ELEM",  "map_fd=5 · key 0",            MUTED, "ar",  "0"),
    ("BPF_MAP_UPDATE_ELEM",  "map_fd=5 · key 501",          MUTED, "ar",  "0"),
]
y = 196
for lab, sub, c, mk, ret in rows:
    d.msg("로더", "커널", lab, y, c, mk, sub=sub)
    d.chip(660, y, ret, c, 13)
    y += 64
# 다음 편으로 — 점선
d.msg("로더", "커널", "kprobe 부착 · perf 이벤트", y, WARN, "warn", dash="5 4", sub="다음 편")

d.legend(H - 56, [("BTF 적재", INFO), ("맵 생성", OK), ("프로그램 적재", ACC), ("맵 갱신", MUTED), ("다음 편", WARN)])
d.save("04-01.chapter-overview.svg")
