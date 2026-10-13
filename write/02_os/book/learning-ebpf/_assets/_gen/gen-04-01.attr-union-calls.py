# 타입 스펙: type-nested — union bpf_attr 상자 안에 명령별 구조체 셋, 각 칸 아래 반환값. focal 은 expected_attach_type=0 한 줄.
# 사실 출처: 추출본 src/ebpf4.txt 268~269행(MAP_CREATE HASH key 4 value 12 max_entries 10240 btf_fd=3 = 5)·302~304행(PROG_LOAD KPROBE insn_cnt 44 GPL expected_attach_type 첫 값 prog_btf_fd 3 = 6)·372~373행(MAP_UPDATE_ELEM map_fd=5 flags BPF_ANY = 0)
#   union 안의 익명 구조체 분할은 linux v7.2 include/uapi/linux/bpf.h 줄 1527~1625(BPF_MAP_CREATE 1528, MAP_*_ELEM 1581, PROG_LOAD 1608), BPF_ANY 는 같은 파일 줄 1402(값 0).
# Layout conventions: 바깥 상자 x=16~944, 안쪽 상자 w=280·간격 16·안 여백 24, 행 stride 24. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 488
d = D(W, H, "LEARNING EBPF · 04-01 §3",
      "union bpf_attr 안의 명령별 구조체와 돌려받은 값",
      "같은 attr 자리에 BPF_MAP_CREATE·BPF_PROG_LOAD·BPF_MAP_UPDATE_ELEM 이 서로 다른 필드 묶음을 채우고, 반환값은 fd 5·6 과 0 이다.",
      "세 호출이 같은 union 의 다른 구조체를 씁니다")

# 바깥 union
OX, OY, OW, OH = 16, 100, 928, 232
d.box(OX, OY, OW, OH, PAPER2, RULE, 0.9, 8)
d.o.append(f'<rect x="{OX+16}" y="{OY-8}" width="124" height="16" fill="{PAPER}"/>')
d.t(OX + 24, OY + 5, "union bpf_attr", 13, MUTED, MONO, "start", 600)

IW, IG, IX0, IY, IH = 280, 16, 40, 132, 176
BOX = [
    ("BPF_MAP_CREATE", OK, "ok",
     ["map_type=BPF_MAP_TYPE_HASH", "key_size=4", "value_size=12", "max_entries=10240", "btf_fd=3"], None, "fd 5"),
    ("BPF_PROG_LOAD", WARN, "warn",
     ["prog_type=BPF_PROG_TYPE_KPROBE", "insn_cnt=44", 'license="GPL"', "expected_attach_type=0", "prog_btf_fd=3"], 3, "fd 6"),
    ("BPF_MAP_UPDATE_ELEM", INFO, "info",
     ["map_fd=5", "key=포인터", "value=포인터", "flags=BPF_ANY (0)"], None, "0"),
]
for i, (title, c, mk, fields, focal, ret) in enumerate(BOX):
    x = IX0 + i * (IW + IG)
    d.tone(x, IY, IW, IH, c, 6, "10", 1.2)
    d.t(x + 16, IY + 28, title, 13, c, MONO, "start", 600)
    for j, f in enumerate(fields):
        fc = ACC if focal == j else INK
        d.t(x + 16, IY + 60 + j * 24, f, 13, fc, KR if any("가" <= ch <= "힣" for ch in f) else MONO, "start", 600 if focal == j else 400)
    cx = x + IW // 2
    d.arrow([(cx, OY + OH + 2), (cx, OY + OH + 40)], c, mk, 1.6)
    d.chip(cx, OY + OH + 60, ret, c, 13)

d.legend(H - 56, [("맵 만들기", OK), ("프로그램 싣기", WARN), ("맵 갱신", INFO), ("짚는 필드", ACC)])
d.save("04-01.attr-union-calls.svg")
