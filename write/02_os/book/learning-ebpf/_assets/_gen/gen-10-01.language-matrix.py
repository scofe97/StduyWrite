# 타입 스펙: type-dp-security-matrix — 언어(행)가 eBPF 커널 쪽 언어가 되기 위한 세 조건(열)을 각각 만족하는지 되고 안 되는 조합으로 보이는 격자.
# 사실 출처: 추출본 ebpf10.txt 208~210행(C·Rust 가 바이트코드 대상), 214~220행(Go·JVM 런타임은 verifier 와 맞지 않음), 225~231행(XDPLua 는 eBPF 아님),
#   366~369행(GCC 10 부터 지원). 현재: GCC 10.1.0 매뉴얼 eBPF Options(9.5.0 매뉴얼에는 없음), rustc platform-support Tier 3 `bpfel-unknown-none`("They don't support std and alloc").
# Layout conventions: 헤더행 y=96~136, 데이터행 높이 56·stride 64(y=148~), 행 라벨 열 x=24~304, 데이터 열 폭 200 stride 208(x=312·520·728). 모든 좌표 4의 배수. focal 은 헤더 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 556
d = D(W, H, "LEARNING EBPF · 10-01 §2",
      "커널 쪽 언어는 런타임이 없어야 해서 C 와 Rust 로 좁혀진다",
      "세 조건을 모두 채우는 언어는 C 와 Rust 이고, GC·스레드 런타임이 있는 언어는 verifier 의 메모리 검사와 맞지 않는다.",
      "언어 다섯 가지 대 조건 세 가지")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


COLS = [("바이트코드 대상", 312, False), ("런타임 없음", 520, True), ("커널 쪽에 쓰임", 728, False)]
for name, x, focal in COLS:
    if focal:
        d.tone(x, 96, 200, 40, ACC, 6, "12", 1.4)
    else:
        d.box(x, 96, 200, 40, PAPER2, RULE, 0.9, 6)
    d.t(x + 100, 121, name, 13, ACC if focal else INK, KR, "middle", 600)
d.t(24, 121, "언어", 13, MUTED, KR, "start", 600)

MARK = {"y": ("✓", OK), "n": ("✗", BAD), "p": ("△", WARN), "x": ("—", MUTED)}
rows = [
    ("C", "Clang -target bpf · GCC 10+", [("y", "Clang · GCC 10+"), ("y", "런타임 없음"), ("y", "주류")]),
    ("Rust", "bpfel-unknown-none", [("y", "bpfel-unknown-none"), ("y", "no_std"), ("y", "사용")]),
    ("Go", "GC 런타임", [("x", "런타임 탓"), ("n", "GC · 스레드"), ("n", "쓰이지 않음")]),
    ("Java", "JVM", [("x", "런타임 탓"), ("n", "JVM"), ("p", "C 로 번역")]),
    ("Lua", "XDPLua · 커널 안 Lua", [("n", "eBPF 아님"), ("n", "Lua 실행기"), ("p", "헬퍼로 호출")]),
]
for i, (lang, sub, cells) in enumerate(rows):
    y = 148 + i * 64
    d.box(24, y, 280, 56, PAPER2, RULE, 0.9, 6)
    d.t(40, y + 24, lang, 15, INK, MONO, "start", 600)
    d.t(40, y + 44, sub, 12, MUTED, fam(sub), "start")
    for (k, label), (_, x, _f) in zip(cells, COLS):
        g, c = MARK[k]
        d.tone(x, y, 200, 56, c, 6, "12", 1.1)
        d.t(x + 28, y + 36, g, 20, c, KR, "middle", 600)
        d.t(x + 52, y + 33, label, 12, INK, fam(label), "start")

d.legend(H - 56, [("만족", OK), ("불가", BAD), ("부분", WARN), ("해당 없음", MUTED), ("논지 열", ACC)])
d.save("10-01.language-matrix.svg")
