# 타입 스펙: type-sequence — 참여자 둘(로더·커널), 호출 여섯과 다음 편으로 가는 점선 하나, 로더 종료로 참조가 주는 점선 하나(§4), 호출별 반환 fd 와 본문 절 대응. focal 은 프로그램을 싣는 BPF_PROG_LOAD 한 줄.
# 사실 출처: 원서 Ch.4 4~8쪽(4쪽 strace 윤곽, 5쪽 BPF_BTF_LOAD=3·BPF_MAP_CREATE output=4, 6쪽 BPF_MAP_CREATE config=5·BPF_PROG_LOAD hello=6, 8쪽 BPF_MAP_UPDATE_ELEM map_fd=5=0, 12쪽 map_fd=4 인 BPF_MAP_UPDATE_ELEM 네 번), 원서 9쪽(프로세스가 끝나면 fd 가 풀려 참조가 준다), 본문 §2·§3, 본문 31행(로더가 끝나 fd 가 닫히면 참조가 줄고 0 이면 커널이 치운다)·45행(1~4절 대응), 예제 저장소 chapter4/hello-buffer-config.py
# Layout conventions: 레인 중심 x=176·576, 호출 간격 stride 64, 첫 호출 y=196, 반환 칩 열 x=660, 본문 절 칩 열 x=780. 모든 좌표 4의 배수.
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

W, H = 960, 764
d = SeqKR(W, H, "LEARNING EBPF · 04-01",
          "예제 로더가 낸 bpf() 호출과 돌려받은 fd",
          "hello-buffer-config.py 는 BTF 를 싣고 맵 둘을 만들고 프로그램을 싣고 맵에 값을 두 번 넣는다. 돌아온 fd 는 이후 호출의 인자로 다시 쓰이고, 로더가 끝나 fd 가 닫히면 참조가 줄어 0 이면 커널이 객체를 치운다.",
          "호출마다 돌아온 번호의 다음 호출 인자 전달")

d.LX = {"로더": 176, "커널": 576}
for nm, sub, x in (("hello-buffer-config.py", "사용자 프로세스", 176), ("커널", "bpf() 시스템 콜 · §1", 576)):
    d.box(x - 112, 100, 224, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

# 열 머리
d.t(660, 176, "반환", 13, SOFT, KR, "middle", 600)
d.t(780, 176, "본문 절", 13, SOFT, KR, "middle", 600)

rows = [
    ("BPF_BTF_LOAD",         "BTF 덩어리",                  INFO, "info", "fd 3", "§2 BTF 적재"),
    ("BPF_MAP_CREATE",       "PERF_EVENT_ARRAY · output",   OK,   "ok",   "fd 4", "§2 맵 생성"),
    ("BPF_MAP_CREATE",       "HASH · config · btf_fd=3",    OK,   "ok",   "fd 5", "§2 맵 생성"),
    ("BPF_PROG_LOAD",        "KPROBE · hello · insn_cnt=44", ACC, "acc",  "fd 6", "§3 프로그램 적재"),
    ("BPF_MAP_UPDATE_ELEM",  "map_fd=5 · key 0",            MUTED, "ar",  "0",    "§3 맵 갱신"),
    ("BPF_MAP_UPDATE_ELEM",  "map_fd=5 · key 501",          MUTED, "ar",  "0",    "§3 맵 갱신"),
]
y = 196
for lab, sub, c, mk, ret, sec in rows:
    d.msg("로더", "커널", lab, y, c, mk, sub=sub)
    d.chip(660, y, ret, c, 13)
    d.chip(780, y, sec, c, 12)
    y += 64
# 다음 편으로 — 점선
d.msg("로더", "커널", "perf 버퍼 설정 · map_fd=4 × 4", y, WARN, "warn", dash="5 4", sub="다음 편")
d.chip(780, y, "04-02 다음 편", WARN, 12)
y += 64
# 로더 종료 — fd 가 닫혀 참조가 준다(§4)
d.msg("로더", "커널", "로더 종료 · fd 3·4·5·6 닫힘", y, BAD, "bad", dash="5 4", sub="참조 −1 · 0 이면 해제")
d.chip(780, y, "§4 참조 수명", BAD, 12)

d.legend(H - 56, [("BTF 적재", INFO), ("맵 생성", OK), ("프로그램 적재", ACC), ("맵 갱신", MUTED), ("다음 편", WARN), ("로더 종료", BAD)])
d.save("04-01.chapter-overview.svg")
