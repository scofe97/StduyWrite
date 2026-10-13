# 타입 스펙: type-data-flow — my_config 맵 선언 매크로 넷이 펼쳐진 타입으로, .maps 섹션 BTF 를 거쳐 BPF_MAP_CREATE 인자가 되는 흐름. focal 은 type 이 배열 크기 [1] 로 펼쳐지는 줄.
# 사실 출처: 예제 저장소 chapter5/hello-buffer-config.bpf.c 14~19행(my_config), libbpf v1.8.0 src/bpf_helpers.h 13~15행(__uint·__type·__array),
#   Linux v7.2 include/uapi/linux/bpf.h 1000~1002행(enum bpf_map_type: UNSPEC=0, HASH=1), 04-01 §2 strace(map_type=BPF_MAP_TYPE_HASH, key_size=4, value_size=12).
# Layout conventions: 열 셋(선언·펼침·결과), 행 stride 60·상자 높이 48(y=116·176·236·296), 열 x=24·352·664, 폭 288·272·272, 결과 상자 높이 240. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 444
d = D(W, H, "LEARNING EBPF · 05-02 §2",
      "맵 속성은 매크로가 펼친 타입에 실려 .maps 섹션 BTF 가 된다",
      "my_config 의 선언 네 줄이 타입 이름과 배열 크기로 펼쳐지고, libbpf 가 .maps 섹션의 BTF 를 읽어 BPF_MAP_CREATE 의 인자를 채운다.",
      "type 의 값 1 은 배열 크기에 실립니다")

for x, w, name in ((24, 288, "선언"), (352, 272, "펼친 타입"), (664, 272, "libbpf 가 읽은 결과")):
    d.t(x, 104, name, 12, MUTED, KR, "start", 600)

ROWS = [
    ("__uint(type, BPF_MAP_TYPE_HASH)", "int (*type)[1]", True),
    ("__uint(max_entries, 10240)", "int (*max_entries)[10240]", False),
    ("__type(key, u32)", "u32 *key", False),
    ("__type(value, struct user_msg_t)", "struct user_msg_t *value", False),
]
for i, (src, exp, focal) in enumerate(ROWS):
    y = 116 + 60 * i
    d.tone(24, y, 288, 48, MUTED, 6, "10", 1.1)
    d.t(168, y + 29, src, 12, INK, MONO, "middle")
    d.tone(352, y, 272, 48, ACC if focal else INFO, 6, "14" if focal else "12", 1.6 if focal else 1.2)
    d.t(488, y + 29, exp, 12, INK, MONO, "middle", 600 if focal else 400)
    d.arrow([(314, y + 24), (348, y + 24)], MUTED, "ar", 1.4)
    d.arrow([(626, y + 24), (660, y + 24)], MUTED, "ar", 1.4)

d.tone(664, 116, 272, 240, OK, 6, "10", 1.2)
d.t(800, 144, ".maps 섹션 BTF", 14, INK, KR, "middle", 600)
d.t(800, 166, "구조체 member 넷", 12, MUTED, KR, "middle")
d.arrow([(800, 180), (800, 212)], MUTED, "ar", 1.4)
d.t(800, 236, "BPF_MAP_CREATE", 14, INK, MONO, "middle", 600)
for i, s in enumerate(["map_type = HASH", "key_size = 4", "value_size = 12", "max_entries = 10240"]):
    d.t(800, 264 + 22 * i, s, 12, MUTED, MONO, "middle")

d.legend(H - 56, [("선언 매크로", MUTED), ("펼친 타입", INFO), ("값이 크기에 실림", ACC), ("libbpf 결과", OK)])
d.save("05-02.map-definition.svg")
