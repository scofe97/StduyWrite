# 타입 스펙: type-data-flow — 빌드 띠와 실행 띠 둘, 카드 넷씩. 값이 카드마다 바뀐다: kprobe.c 의 두 이름 → 파일 두 쌍 → 단일 바이너리 → bpfObjects → 링크 → Lookup(0) → 한 줄 출력.
# 사실 출처: cilium/ebpf v0.22.0 examples/kprobe/kprobe.c L7~27(kprobe_map ARRAY max_entries 1, SEC("kprobe/sys_execve") kprobe_execve),
#   main.go L17(go:generate go tool bpf2go -tags linux bpf kprobe.c), L31~36(loadBpfObjects), L42(link.Kprobe("sys_execve")), L55~60(KprobeMap.Lookup, "%s called %d times"),
#   bpf_bpfel.go L84~127(bpfObjects·bpfMaps·bpfPrograms), docs/ebpf/guides/portable-ebpf.md L19~35(bpfel·bpfeb 두 쌍, go:embed).
# Layout conventions: 카드 w=180·h=84·stride 240(x=24·264·504·744), 빌드 띠 y=88~220(카드 y=120), 실행 띠 y=280~412(카드 y=312), 되돌이는 y=248 ㄷ자. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 496
d = D(W, H, "LEARNING EBPF · 10-02 §1",
      "C 소스가 빌드 때 바이너리에 묻히고 실행 때 맵을 읽는다",
      "kprobe.c 의 맵과 프로그램 이름이 go generate 로 Go 파일 두 쌍이 되고, go build 가 바이트코드를 단일 바이너리에 담는다. 실행하면 적재 · 부착 · 읽기를 거쳐 sys_execve 횟수를 찍는다.",
      "위는 빌드 때, 아래는 실행 때")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def band(y, name):
    d.box(12, y, 936, 132, PAPER2, RULE, 0.9, 8)
    d.t(24, y + 18, name, 9, SOFT, MONO, "start")


def card(x, y, c, lines, focal=False):
    d.tone(x, y, 180, 84, c, 6, "14" if focal else "12", 1.6 if focal else 1.2)
    for k, (txt, size, fill, wt) in enumerate(lines):
        d.t(x + 90, y + 26 + 22 * k, txt, size, fill, fam(txt), "middle", wt)


XS = (24, 264, 504, 744)
band(88, "BUILD · go generate · go build")
band(280, "RUN")

# 빌드 띠
card(XS[0], 120, INFO, [("kprobe.c", 13, INK, 600), ("kprobe_map", 12, MUTED, 400), ("kprobe_execve", 12, MUTED, 400)])
card(XS[1], 120, WARN, [("bpf2go", 13, INK, 600), ("stem bpf", 12, MUTED, 400), ("Clang 컴파일", 12, MUTED, 400)])
card(XS[2], 120, OK, [("생성 파일 두 쌍", 13, INK, 600), ("bpf_bpfel.o + .go", 12, MUTED, 400), ("bpf_bpfeb.o + .go", 12, MUTED, 400)])
card(XS[3], 120, ACC, [("go build", 13, INK, 600), ("//go:embed", 12, MUTED, 400), ("단일 바이너리", 12, MUTED, 400)], True)
for i in range(3):
    d.arrow([(XS[i] + 182, 162), (XS[i + 1] - 6, 162)], MUTED, "ar", 1.5)

# 빌드 → 실행 (ㄷ자)
d.arrow([(XS[3] + 90, 206), (XS[3] + 90, 248), (XS[0] + 90, 248), (XS[0] + 90, 308)], ACC, "acc", 1.6)
d.chip((XS[0] + XS[3]) // 2 + 90, 248, "바이너리 실행", ACC, 12)

# 실행 띠
card(XS[0], 312, INFO, [("loadBpfObjects", 13, INK, 600), ("&objs", 12, MUTED, 400), ("bpfObjects", 12, MUTED, 400)])
card(XS[1], 312, INFO, [("link.Kprobe", 13, INK, 600), ("sys_execve", 12, MUTED, 400), ("KprobeExecve", 12, MUTED, 400)])
card(XS[2], 312, INFO, [("KprobeMap.Lookup", 13, INK, 600), ("key 0", 12, MUTED, 400), ("1초마다", 12, MUTED, 400)])
card(XS[3], 312, MUTED, [("log.Printf", 13, INK, 600), ("sys_execve", 12, MUTED, 400), ("called N times", 12, MUTED, 400)])
for i in range(3):
    d.arrow([(XS[i] + 182, 354), (XS[i + 1] - 6, 354)], MUTED, "ar", 1.5)

d.legend(H - 56, [("원본 소스", INFO), ("컴파일 도구", WARN), ("산출물", OK), ("단일 바이너리", ACC)])
d.save("10-02.bpf2go-flow.svg")
