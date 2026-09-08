# 15-02 §1 — 원라이너 한 줄은 네 조각으로 읽힌다.
# 타입 스펙: type-process — 한 줄을 조각으로 갈라 각 조각이 맡는 일을 대응시키는 지도.
#           축약: 주체(lane)가 없는 구성 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 576
X0, Y = 40, 128

d = DK(W, H, "SYSTEMS PERFORMANCE · 15-02 §1",
       "원라이너 한 줄을 네 조각으로 읽는다",
       "bpftrace 한 줄은 어디서 잡을지, 무엇만 남길지, 무엇을 셀지로 나뉜다. 조각의 이름을 알면 남의 원라이너도 읽힌다.",
       "awk 가 패턴과 액션으로 나뉘듯 bpftrace 도 그렇게 나뉩니다")

# 코드 한 줄
d.box(X0, Y, 872, 48, PAPER2, RULE, 1.0, 6)
d.t(X0 + 20, Y + 30, "bpftrace -e 'k:vfs_read /pid == 181/ { @b = hist(arg2); }'", 14, INK, MONO, "start")

PARTS = [
    ("01", "프로브", "k:vfs_read", "어디서 잡을 것인가 — 커널 함수 진입", INFO),
    ("02", "필터", "/pid == 181/", "무엇만 남길 것인가 — 참일 때만 액션", None),
    ("03", "액션", "{ ... }", "무엇을 할 것인가 — 프로브마다 실행", None),
    ("04", "맵 · 집계", "@b = hist(arg2)", "무엇을 셀 것인가 — 커널 안에서 모은다", ACC),
]
CH, STRIDE = 62, 70
for i, (n, name, code, desc, c) in enumerate(PARTS):
    y = Y + 76 + i * STRIDE
    if c is ACC: d.tone(X0, y, 872, CH, c, 6)
    elif c: d.tone(X0, y, 872, CH, c, 6)
    else: d.box(X0, y, 872, CH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 20, y + 26, n, 9, PAPER if c else MUTED, MONO, "start")
    d.t(X0 + 44, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(X0 + 140, y + 26, code, 13, c if c else MUTED, MONO, "start")
    d.t(X0 + 20, y + 48, desc, 13, MUTED, KR, "start")

YB = Y + 76 + 4 * STRIDE + 16
d.t(X0, YB, "커널 안에서 집계해 요약만 유저 공간으로 올리기 때문에, 이벤트마다 내보내는 방식보다 훨씬 쌉니다", 13, MUTED, KR, "start")

d.legend(YB + 24, [("커널 안에서 모으는 자리", ACC), ("잡는 자리", INFO), ("나머지 조각", MUTED)])
d.save("15-02.bpftrace-oneliner-anatomy.svg")
