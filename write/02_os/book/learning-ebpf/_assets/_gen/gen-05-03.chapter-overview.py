# 타입 스펙: type-swimlane — 레인 둘(빌드 · 실행)을 세로 열로 놓고, 빌드 마지막 산출물이 실행 첫 호출로 넘어가는 건넘 하나를 그린다. focal 은 적재 때 CO-RE 를 고치는 호출.
# (실행 열 제목은 스켈레톤 함수의 접두사 hello_buffer_config_bpf 를 뺀 이름이다. 접두사는 본문 §3 이 설명한다.)
# 사실 출처: 추출본 src/ebpf5.txt 1144~1152행(Makefile 규칙 clang … -O2 -g · llvm-strip -g), 1317행(bpftool gen skeleton … > .skel.h),
#   1330~1336행(__elf_bytes · .o 를 지워도 실행 파일이 돎), 1362~1389행(main: __open_and_load · __attach · perf_buffer__new(…, 8, …) · perf_buffer__poll(pb, 100) · perf_buffer__free · __destroy),
#   예제 저장소 91ded4a chapter5/Makefile(gcc … -l:libbpf.a -lelf -lz), chapter5/hello-buffer-config.bpf.c(SEC("ksyscall/execve")).
# Layout conventions: 열 폭 440·노드 392×44·stride 68, 열 x=16·504, 건넘 통로 x=480. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER2, RULE, SOFT, KR, MONO


def fam(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


W, H = 960, 676
d = D(W, H, "LEARNING EBPF · 05-03",
      "make 한 번이 만든 실행 파일이 적재 · 부착 · 수신 · 정리를 돈다",
      "빌드 열에서 CO-RE 오브젝트가 스켈레톤 헤더를 거쳐 실행 파일이 되고, 실행 열에서 그 파일이 __open_and_load 로 CO-RE 를 고쳐 싣고 부착한 뒤 perf 버퍼를 읽는다.",
      "명령 넷 · 산출물 셋 · 호출 다섯")

BZ = (16, 92, 440, 512)
RZ = (504, 92, 440, 512)
for (x, y, w, h), name in ((BZ, "빌드 · make"), (RZ, "실행 · hello-buffer-config")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 12, SOFT, KR, "start")

NW, NH, ST, Y0 = 392, 44, 68, 132
BX, RX = 40, 528


def node(x, y, title, sub, c, focal=False):
    if focal:
        d.tone(x, y, NW, NH, ACC, 6, "1F", 1.4)
    else:
        d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    if sub:
        d.t(x + NW / 2, y + 19, title, 13, INK, fam(title), "middle", 600)
        d.t(x + NW / 2, y + 36, sub, 12, MUTED, fam(sub))
    else:
        d.t(x + NW / 2, y + 27, title, 13, INK, fam(title), "middle", 600)


BUILD = [
    ("clang … -O2 -g", "-target bpf", INFO),
    ("llvm-strip -g", ".BTF 는 남음", INFO),
    ("hello-buffer-config.bpf.o", ".BTF · .BTF.ext", OK),
    ("bpftool gen skeleton", "", INFO),
    ("hello-buffer-config.skel.h", "ELF 바이트 내장", OK),
    ("gcc … -l:libbpf.a -lelf -lz", "", INFO),
    ("hello-buffer-config", ".o 없이 실행", OK),
]
RUN = [
    ("__open_and_load", "CO-RE 수정", MUTED, True),
    ("__attach", "ksyscall/execve", MUTED, False),
    ("perf_buffer__new(fd, 8, …)", "", MUTED, False),
    ("perf_buffer__poll(pb, 100)", "최대 100 ms 대기", MUTED, False),
    ("perf_buffer__free · __destroy", "", MUTED, False),
]

# 열 안 세로 화살표를 먼저 그린다
for col_x, items in ((BX, BUILD), (RX, RUN)):
    for i in range(len(items) - 1):
        y = Y0 + i * ST
        d.arrow([(col_x + NW / 2, y + NH + 2), (col_x + NW / 2, y + ST - 6)], MUTED, "ar", 1.4)

# 건넘 — 실행 파일에서 첫 호출로
y_exe = Y0 + 6 * ST + NH / 2
y_open = Y0 + NH / 2
d.arrow([(BX + NW + 2, y_exe), (480, y_exe), (480, y_open), (RX - 6, y_open)], ACC, "acc", 1.8)
d.chip(480, 360, "실행", ACC, 12)

for i, (t, s, c) in enumerate(BUILD):
    node(BX, Y0 + i * ST, t, s, c)
for i, (t, s, c, f) in enumerate(RUN):
    node(RX, Y0 + i * ST, t, s, c, f)

d.legend(H - 56, [("빌드 명령", INFO), ("산출물", OK), ("실행 중 호출", MUTED), ("CO-RE 수정", ACC)])
d.save("05-03.chapter-overview.svg")
