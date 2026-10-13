# 타입 스펙: type-dp-security-matrix — 행 셋(헬퍼 호출) × 열 셋(유형 허용 · gpl_only · arg1_type). 칸은 통과 · 거부 · 미도달.
# 사실 출처: 커널 v7.2 kernel/bpf/verifier.c 10187~10203행(유형 → 라이선스 순), 10194행(cannot use helper), 10200~10201행(GPL-restricted),
#   7882행(type=%s expected=), kernel/bpf/helpers.c 50~57행(bpf_map_lookup_elem_proto), 2114행(base 집합), 2192행(CAP_PERFMON),
#   kernel/trace/bpf_trace.c 416~418행(bpf_trace_printk gpl_only), 306~308행(bpf_probe_read_kernel_str gpl_only), net/core/filter.c 8600~8655행(xdp_func_proto),
#   include/uapi/linux/bpf.h FN(skb_load_bytes, 26)·FN(map_lookup_elem, 1)·FN(probe_read_kernel_str, 115). 추출본 src/ebpf6.txt 333~334행.
# Layout conventions: 라벨 열 w=248, 칸 w=208 gap=8, 행 stride 80 h=64. 모든 좌표 4의 배수.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

LP, LBL, GAP, COL = 24, 248, 8, 208
W = LP + LBL + GAP + 3 * COL + 2 * GAP + 24
HY, HH = 108, 40
Y0, STRIDE, RH = 164, 80, 64
LEG_Y = Y0 + 3 * STRIDE + 4
H = LEG_Y + 56

d = D(W, H, "LEARNING EBPF · 06-02 §1",
      "헬퍼 호출 세 개가 세 검사에서 걸리는 자리",
      "검사 순서는 유형, 라이선스, 인자 타입이다. 앞 검사에서 거부되면 뒤 검사에는 닿지 않는다.",
      "행 = 헬퍼 호출 · 열 = 검사 순서")


def cx(j):
    return LP + LBL + GAP + j * (COL + GAP)


heads = [("1 · 프로그램 유형", KR), ("2 · gpl_only", MONO), ("3 · arg1_type", MONO)]
d.box(LP, HY, LBL, HH, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL / 2, HY + 26, "헬퍼 호출", 13, INK, KR, "middle", 600)
for j, (h, f) in enumerate(heads):
    d.box(cx(j), HY, COL, HH, PAPER2, RULE, 0.9, 6)
    d.t(cx(j) + COL / 2, HY + 26, h, 13, INK, f, "middle", 600)

PASS, FAIL, SKIP = "pass", "fail", "skip"
rows = [
    ("XDP 프로그램", "bpf_skb_load_bytes#26",
     [(FAIL, "cannot use helper #26", True), (SKIP, "미도달", False), (SKIP, "미도달", False)]),
    ("kprobe_exec", "bpf_map_lookup_elem#1",
     [(PASS, "공통 집합", False), (PASS, "gpl_only = false", False), (FAIL, "type=fp expected=map_ptr", False)]),
    ("라이선스 줄 없음", "bpf_trace_printk#6",
     [(PASS, "CAP_PERFMON 구간", False), (FAIL, "GPL-restricted", False), (SKIP, "미도달", False)]),
]
for i, (t1, t2, cells) in enumerate(rows):
    y = Y0 + i * STRIDE
    d.box(LP, y, LBL, RH, PAPER2, RULE, 0.9, 6)
    d.t(LP + 12, y + 26, t1, 13, INK, KR, "start", 600)
    d.t(LP + 12, y + 48, t2, 12, MUTED, MONO, "start")
    for j, (st, txt, focal) in enumerate(cells):
        c = {PASS: OK, FAIL: BAD, SKIP: MUTED}[st]
        mark = {PASS: "통과", FAIL: "거부", SKIP: "—"}[st]
        if focal:
            d.tone(cx(j), y, COL, RH, ACC, 6, "18", 1.4)
        else:
            d.tone(cx(j), y, COL, RH, c, 6, "10" if st == SKIP else "14", 1.1)
        d.t(cx(j) + COL / 2, y + 26, mark, 13, ACC if focal else c, KR, "middle", 600)
        d.t(cx(j) + COL / 2, y + 48, txt, 13 if txt == "미도달" else 12, c if not focal else ACC, KR if txt == "미도달" else MONO, "middle")

d.legend(LEG_Y, [("통과", OK), ("거부", BAD), ("미도달", MUTED), ("첫 관문", ACC)])
d.save("06-02.helper-checks.svg")
