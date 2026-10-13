# 타입 스펙: type-process — BCC 의 `BPF(text=program)` 가 문자열을 재작성하고 Clang 으로 컴파일해 적재한 뒤, Python 이 같은 맵 fd 로 링 버퍼를 여는 다섯 단계와 단계마다 오가는 실제 문자열.
# 사실 출처: 추출본 ebpf10.txt 285~299행(program 문자열·BPF(text=)·open_ring_buffer). 예제 chapter2/hello-file-ring-buffer.py(HEAD 91ded4a) 5·23·29·35행.
#   BCC v0.37.0: src/python/bcc/__init__.py 502행(bpf_module_create_c_from_string)·648행(bpf_table_fd), src/cc/export/helpers.h 232~247행(BPF_RINGBUF_OUTPUT),
#   src/cc/frontends/clang/b_frontend_action.cc 1063~1068행(ringbuf_output 재작성)·1584~1585행(maps/ringbuf → BPF_MAP_TYPE_RINGBUF), src/cc/bpf_module.cc 211행(ClangLoader)·509행(create_maps, 프로그램 적재 전)·985행(bcc_func_load).
# Layout conventions: 단계 상자 폭 912(x=24~936)·높이 64, stride 96(y=100~484), 단계 이름 x=40, 내용 x=216~. 화살표 칩은 상자 사이 간격 중앙. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 636
d = D(W, H, "LEARNING EBPF · 10-01 §3",
      "BCC 는 문자열을 재작성해 맵을 양쪽에 동시에 만든다",
      "한 줄의 BPF_RINGBUF_OUTPUT 이 커널 쪽 링 버퍼 맵이 되고, Python 의 b[\"output\"] 은 같은 맵 fd 를 가리킨다.",
      "다섯 단계에서 바뀌는 문자열")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


X, BW, BH, STRIDE, Y0 = 24, 912, 64, 96, 100
steps = [
    ("PYTHON", INFO, "BPF(text=program)", None, ("program", "BPF_RINGBUF_OUTPUT(output, 1)")),
    ("BCC 재작성", ACC, "output.ringbuf_output(&event, sizeof(event), 0)", "bpf_ringbuf_output(bpf_pseudo_fd(1, fd), &event, …)", None),
    ("CLANG", WARN, "maps/ringbuf → BPF_MAP_TYPE_RINGBUF", "eBPF 바이트코드", None),
    ("커널", MUTED, "bpf(BPF_MAP_CREATE) · bpf(BPF_PROG_LOAD)", "맵 fd · 프로그램 fd", None),
    ("PYTHON", INFO, 'b["output"].open_ring_buffer(print_event)', "같은 맵 fd", None),
]
for i, (lane, c, l1, l2, special) in enumerate(steps):
    y = Y0 + i * STRIDE
    focal = c == ACC
    d.tone(X, y, BW, BH, c, 6, "14" if focal else "12", 1.6 if focal else 1.1)
    d.t(X + 16, y + 38, lane, 13, c, fam(lane), "start", 600)
    if special:
        d.t(216, y + 28, special[0], 12, MUTED, KR, "start")
        d.t(216, y + 50, special[1], 13, INK, MONO, "start", 600)
    else:
        d.t(216, y + 28, l1, 13, INK, fam(l1), "start", 600)
        d.t(216, y + 50, l2, 12, MUTED, fam(l2), "start")

chips = {0: "bpf_module_create_c_from_string", 1: "", 2: "", 3: "bpf_table_fd"}
for i, txt in chips.items():
    y = Y0 + i * STRIDE + BH
    d.arrow([(112, y + 2), (112, y + STRIDE - BH - 6)], MUTED, "ar", 1.5)
    if txt:
        d.chip(112 + 16 + (len(txt) * 11 * 0.62 + 14) / 2, y + (STRIDE - BH) / 2, txt, MUTED, 11)

d.legend(H - 56, [("사용자 공간", INFO), ("재작성", ACC), ("컴파일 비용", WARN), ("커널", MUTED)])
d.save("10-01.bcc-rewrite.svg")
