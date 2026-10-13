# 타입 스펙: type-layers — hello-buffer-config.bpf.o 의 BTF 계열 섹션 넷을 파일 오프셋 순으로 쌓는다. focal 은 CO-RE 재배치가 든 .BTF.ext 한 층.
# 사실 출처: 추출본 src/ebpf5.txt 1172~1176행(readelf -S … | grep BTF: [10] .BTF 000002c0 · [11] .rel.BTF 00000e50 · [12] .BTF.ext 00000b18 · [13] .rel.BTF.ext 00000ea0),
#   .BTF = 타입·문자열, .BTF.ext = func_info·line_info·CO-RE 재배치는 linux v7.2 Documentation/bpf/btf.rst 762~776행. readelf 출력에 있는 섹션만 그린다.
# Layout conventions: 층 높이 68(스펙 56~72)·폭 816(스펙 800~880)·x=96, 인덱스 태그 x=112, 이름 x=176, 오프셋 x=360, 설명 오른쪽 끝 x=896. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, SOFT, KR, MONO

W, H = 960, 484
d = D(W, H, "LEARNING EBPF · 05-03 §1",
      "readelf 가 보여 준 BTF 계열 섹션 넷",
      "hello-buffer-config.bpf.o 의 섹션 [10] .BTF 는 오프셋 0x2c0, [12] .BTF.ext 는 0xb18, [11] .rel.BTF 는 0xe50, [13] .rel.BTF.ext 는 0xea0 에 있고 CO-RE 재배치는 .BTF.ext 에 든다.",
      "파일 오프셋이 작은 섹션이 위, CO-RE 재배치는 둘째 층")

X, WD, LH, Y0 = 96, 816, 68, 124
LAYERS = [
    ("[10]", ".BTF", "0x2c0", "타입 · 문자열", False),
    ("[12]", ".BTF.ext", "0xb18", "함수 정보 · 줄 정보 · CO-RE 재배치", True),
    ("[11]", ".rel.BTF", "0xe50", "REL · ELF 재배치 표", False),
    ("[13]", ".rel.BTF.ext", "0xea0", "REL · ELF 재배치 표", False),
]
for i, (tag, name, off, note, focal) in enumerate(LAYERS):
    y = Y0 + i * LH
    if focal:
        d.tone(X, y, WD, LH, ACC, 4, "1F", 1.4)
    else:
        d.tone(X, y, WD, LH, MUTED, 4, "0F", 1.0)
    d.t(X + 16, y + 40, tag, 12, SOFT, MONO, "start")
    d.t(X + 80, y + 41, name, 15, INK, MONO, "start", 600)
    d.t(X + 264, y + 41, "@ " + off, 13, MUTED, MONO, "start")
    d.t(X + WD - 16, y + 41, note, 13, INK if focal else MUTED, KR, "end")

# 좌측 방향 표시 — 오프셋이 아래로 커진다
d.arrow([(48, 136), (48, 384)], MUTED, "ar", 1.4)
d.t(48, 120, "offset", 12, SOFT, MONO)

d.legend(H - 56, [("그 밖의 섹션", MUTED), ("CO-RE 재배치가 든 섹션", ACC)])
d.save("05-03.object-btf-layers.svg")
