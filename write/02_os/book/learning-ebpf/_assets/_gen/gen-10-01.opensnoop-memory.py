# 타입 스펙: type-bar — 같은 도구 opensnoop 의 libbpf 판과 BCC Python 판이 쓰는 메모리를 가로 막대 두 개로 비교하고 BCC 판 아래에 시작 때 컴파일 비용을 단다.
# 사실 출처: bcc PR #2778 comment 594202408(Gregg, 2020-03-03: "9 Mbytes for CO-RE vs 80 Mbytes for Python").
#   시작 때 Clang 컴파일: 추출본 273~275행·378~380행. 
# Layout conventions: plot x=240~880(0~100 MB, 6.4 px/MB), 막대 높이 48, 막대 stride 96(y=108·204), 눈금선 20 MB 간격 5줄. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 404
d = D(W, H, "LEARNING EBPF · 10-01 §4",
      "libbpf 판 opensnoop 은 BCC 판의 약 9분의 1 메모리를 쓴다",
      "같은 도구를 libbpf C 로 다시 쓰면 메모리가 줄고, BCC 판은 시작할 때마다 Clang 컴파일을 거친다.",
      "2020-03 측정 9 MB 대 80 MB")

PX0, PX1, PY0, PY1 = 240, 880, 92, 296
SCALE = (PX1 - PX0) / 100.0
for mb in (0, 20, 40, 60, 80, 100):
    x = PX0 + mb * SCALE
    d.line(x, PY0, x, PY1, RULE, 0.8)
    d.t(x, PY1 + 20, f"{mb} MB", 11, SOFT, MONO)


def bar(y, mb, c, name, val, focal=False):
    w = round(mb * SCALE / 4) * 4
    d.tone(PX0, y, w, 48, c, 4, "22" if focal else "18", 1.4 if focal else 1.1)
    d.t(PX0 - 16, y + 30, name, 14, INK, KR, "end", 600)
    d.t(PX0 + w + 12, y + 30, val, 13, c, KR, "start", 600)


bar(108, 9, OK, "libbpf 판", "9 MB · 2020-03")
bar(204, 80, ACC, "BCC Python 판", "80 MB · 2020-03", True)
d.chip(PX0 + 112, 276, "시작 때 Clang 컴파일", WARN, 12)

d.legend(H - 56, [("libbpf 판", OK), ("BCC Python 판", ACC), ("컴파일 비용", WARN)])
d.save("10-01.opensnoop-memory.svg")
