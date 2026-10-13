# 타입 스펙: type-sequence — 참여자 셋(사용자 프로그램 · libbpf · 커널), 메시지 열하나. 앞쪽은 find-map.c 의 고정 경로 맵 조회, 뒤쪽은 hello-buffer-config.c 의 perf 버퍼 수신. focal 은 handle_event 콜백 한 줄.
# 사실 출처: 추출본 src/ebpf5.txt 1480~1505행(bpf_obj_get("/sys/fs/bpf/findme") · bpf_obj_get_info_by_fd · Name: findme), 1535행(perf_buffer__new(bpf_map__fd(skel->maps.output), 8, handle_event, lost_event, NULL, NULL)),
#   1552행(perf_buffer__poll(pb, 100)), 1579~1583행(23664 501 bash Hello World). libbpf v1.8.0: bpf.c 683행(BPF_OBJ_GET)·1269행(BPF_OBJ_GET_INFO_BY_FD),
#   libbpf.c 14945행 부근(perf_event_open)·15151행(bpf_map_update_elem)·15254행(epoll_wait), libbpf.h 1726~1739행(page_cnt).
# Layout conventions: 레인 중심 x=136·516·836(상자 폭 232·176·176), 메시지 stride 52(y=196부터), 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 12)/2}" y="{y + 5}" width="{_w(sub, 12)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, mk="ar"):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m=mk)
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 15, sub, 12, MUTED, _kr(sub), "start")


W, H = 960, 830
d = SeqKR(W, H, "LEARNING EBPF · 05-03 §4",
          "고정 경로 맵을 잡고 perf 버퍼 콜백으로 이벤트를 받는다",
          "find-map 은 bpf_obj_get 으로 고정된 맵의 fd 를 받아 이름을 읽고, hello-buffer-config 는 perf_buffer__new 로 CPU 마다 링을 열어 두고 perf_buffer__poll 이 돌려준 레코드를 handle_event 콜백으로 받아 한 줄을 찍는다.",
          "같은 libbpf 호출이 BPF_OBJ_GET 과 CPU 별 링 설정으로 풀린다")

U, L, K = "사용자 프로그램", "libbpf", "커널"
d.LX = {U: 136, L: 516, K: 836}
for nm, sub, w in ((U, "find-map · hello-buffer-config", 232), (L, "", 176), (K, "", 176)):
    x = d.LX[nm]
    d.box(x - w // 2, 100, w, 44, PAPER2, RULE, 1.0)
    if sub:
        d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
        d.t(x, 137, sub, 12, MUTED, _kr(sub))
    else:
        d.t(x, 127, nm, 13, INK, _kr(nm), "middle", 600)
d.lane_top = 144
d.rails(H - 80)

d.msg(U, L, 'bpf_obj_get("/sys/fs/bpf/findme")', 196, MUTED, "ar", sub="find-map.c")
d.msg(L, K, "BPF_OBJ_GET", 248, MUTED, "ar")
d.msg(K, L, "fd", 300, MUTED, "ar", dash="5 4")
d.msg(U, L, "bpf_obj_get_info_by_fd(fd, …)", 352, INFO, "info", sub="BPF_OBJ_GET_INFO_BY_FD")
d.selfmsg(U, "Name: findme", 404, OK, mk="ok")
d.msg(U, L, "perf_buffer__new(map fd, 8, …)", 456, MUTED, "ar", sub="hello-buffer-config.c")
d.msg(L, K, "CPU 마다 링 열기", 508, MUTED, "ar", sub="perf_event_open · bpf_map_update_elem")
d.msg(U, L, "perf_buffer__poll(pb, 100)", 560, MUTED, "ar", sub="epoll_wait")
d.msg(K, L, "링에 레코드", 612, INFO, "info", sub="bpf_perf_event_output")
d.msg(L, U, "handle_event(ctx, cpu, data, data_sz)", 664, ACC, "acc")
d.selfmsg(U, "23664 501 bash Hello World", 716, OK, mk="ok")

d.legend(H - 56, [("호출 · 응답", MUTED), ("정보 · 이벤트", INFO), ("화면 출력", OK), ("콜백 호출", ACC)])
d.save("05-03.perf-buffer-sequence.svg")
