# 타입 스펙: type-data-flow — 레인 둘(키 · 값) × 단계 셋(BPF_MAP_CREATE 인자 · 커널이 쥔 타입 · map dump 출력). 값이 단계마다 모양을 바꾼다. focal 은 값이 필드 이름 붙은 문자열로 읽히는 칸.
# 사실 출처: 추출본 src/ebpf5.txt 452~468행(bpf_attr 의 btf_fd · btf_key_type_id · btf_value_type_id), 472~482행(키와 값 타입 ID 를 따로 넘김),
#   338~340행·368~372행([1] u32 · [4] user_msg_t), src/ebpf4.txt 395~420행(bpftool map dump name config 출력), linux v7.2 tools/bpf/bpftool/map.c 71~94행(키는 btf_key_type_id, 값은 btf_value_type_id 로 푼다).
#   btf_key_type_id=1·btf_value_type_id=4 는 BTF 덤프의 ____btf_map_config 두 멤버 type_id 와 BCC get_map_tids(src/cc/bcc_btf.cc 651행~)가 그 값을 읽어 넘기는 구조에서 따른 값이다.
# Layout formulas(type-data-flow §2) 변형: 레인 2 · lane_h 96 · node_h 64 · 단계 폭 232·232·244. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 428
d = D(W, H, "LEARNING EBPF · 05-01 §4",
      "키와 값의 타입 ID 가 맵 덤프의 필드 이름이 된다",
      "BPF_MAP_CREATE 는 btf_fd=3 과 함께 키 타입 ID 1, 값 타입 ID 4 를 따로 넘기고, 커널은 u32 와 user_msg_t 를 맵에 붙여 두며, bpftool 은 그 타입으로 값을 풀어 찍는다.",
      "같은 맵 config 의 한 항목이 세 번 모양을 바꿉니다")

TOP, LH, NH = 140, 96, 64
COLX = [100, 408, 716]
COLW = [232, 232, 244]
HEAD = ["01 BPF_MAP_CREATE", "02 커널 안 config 맵", "03 bpftool map dump"]
LANES = ["키", "값"]

for i, (x, w) in enumerate(zip(COLX, COLW)):
    pw = 232
    d.box(x + w / 2 - pw / 2, 100, pw, 24, PAPER2, RULE, 0.9, 12)
    d.t(x + w / 2, 117, HEAD[i], 13, MUTED, MONO if HEAD[i][3].isascii() else KR, "middle", 600)

for k, nm in enumerate(LANES):
    y = TOP + k * LH
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{y}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.t(24, y + LH // 2 + 4, nm, 14, INK, KR, "start", 600)

ROWS = [
    ("btf_key_type_id=1", "btf_fd=3 의 BTF", "[1] u32", "TYPEDEF · 4바이트", '"key": 501', "u32 로 해석", INFO, None),
    ("btf_value_type_id=4", "btf_fd=3 의 BTF", "[4] user_msg_t", "STRUCT · 12바이트", '"message": "Hi user 501!"', "char 12칸 문자열", INFO, ACC),
]
for k, (a, asub, b, bsub, c, csub, col, foc) in enumerate(ROWS):
    y = TOP + k * LH + (LH - NH) // 2
    cy = y + NH // 2
    cc = foc or INK  # 키 출력은 필드 이름이 아니라 u32 로 푼 숫자라 중립으로 둔다
    # 단계 1 — 호출 인자
    d.tone(COLX[0], y, COLW[0], NH, col, 6, "12", 1.2)
    d.t(COLX[0] + COLW[0] / 2, y + 28, a, 13, col, MONO, "middle", 600)
    d.t(COLX[0] + COLW[0] / 2, y + 48, asub, 12 if asub.isascii() else 13, MUTED, MONO if asub.isascii() else KR)
    # 단계 2 — 커널이 쥔 타입
    d.tone(COLX[1], y, COLW[1], NH, OK, 6, "12", 1.2)
    d.t(COLX[1] + COLW[1] / 2, y + 28, b, 13, OK, MONO, "middle", 600)
    d.t(COLX[1] + COLW[1] / 2, y + 48, bsub, 13, MUTED, KR)
    # 단계 3 — 출력
    if foc:
        d.tone(COLX[2], y, COLW[2], NH, cc, 6, "1F", 1.4)
    else:
        d.box(COLX[2], y, COLW[2], NH, PAPER2, RULE, 1.0)
    d.t(COLX[2] + COLW[2] / 2, y + 28, c, 13, cc, MONO, "middle", 600)
    d.t(COLX[2] + COLW[2] / 2, y + 48, csub, 13, MUTED, KR)
    d.arrow([(COLX[0] + COLW[0] + 2, cy), (COLX[1] - 6, cy)], INFO, "info", 1.5)
    d.arrow([(COLX[1] + COLW[1] + 2, cy), (COLX[2] - 6, cy)], OK if not foc else ACC, "ok" if not foc else "acc", 1.5)

d.legend(H - 56, [("호출 인자", INFO), ("커널이 쥔 타입", OK), ("필드 이름이 붙은 출력", ACC)])
d.save("05-01.map-btf-flow.svg")
