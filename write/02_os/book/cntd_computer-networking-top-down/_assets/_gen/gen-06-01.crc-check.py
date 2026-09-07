# 타입 스펙: type-flowchart — 판정을 물어 가며 좁히는 결정 흐름. 마름모가 물음이고 사각이 결과다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.2.3 Figure 6.6 · Figure 6.7 —
#   D=101110, G=1001, r=3. 나머지·몫·검산은 이 생성기가 modulo-2 로 직접 계산해 찍는다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D as Dg, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

DATA, GEN = "101110", "1001"
R = len(GEN) - 1


def mod2(dividend, gen):
    b = list(dividend); n = len(gen); q = []
    for i in range(len(b) - n + 1):
        if b[i] == "1":
            q.append("1")
            for j in range(n):
                b[i + j] = "0" if b[i + j] == gen[j] else "1"
        else:
            q.append("0")
    return "".join(q), "".join(b[-(n - 1):])


QUOT, REM = mod2(DATA + "0" * R, GEN)
SENT = DATA + REM
assert mod2(SENT, GEN)[1] == "0" * R, "보내는 비트는 G 로 나누어떨어져야 합니다"

W, H = 940, 572
d = Dg(W, H, "SECTION 6.2.3 · CYCLIC REDUNDANCY CHECK",
       "나머지가 0 이면 통과시킵니다",
       "송신이 나머지를 붙여 보내고 수신이 같은 생성기로 다시 나눈다. 나머지가 0 이 아니면 오류를 검출한 것이다.",
       f"D={DATA}, G={GEN}, r={R} — 원문 Figure 6.7 의 예입니다")

FX, FW = 40, 300
for y, title, sub in [
    (110, "송신이 D 와 생성기 G 를 정합니다", f"D = {DATA} · G = {GEN}"),
    (186, "D 를 r 비트 밀고 G 로 나눕니다", f"{DATA}{'0' * R} ÷ {GEN}"),
    (262, "나머지 R 을 뒤에 붙여 보냅니다", f"보내는 비트 = {SENT}"),
]:
    d.box(FX, y, FW, 56, PAPER2, RULE, 0.9)
    d.t(FX + FW / 2, y + 24, title, 11, INK, KR, "middle", 600)
    d.t(FX + FW / 2, y + 43, sub, 11, MUTED, MONO)
for y0 in (168, 244, 320):
    d.arrow([(FX + FW / 2, y0), (FX + FW / 2, y0 + 14)], MUTED, "ar", 1.3)

CXD, CYD, HWD, HHD = FX + FW / 2, 386, 148, 46
d.o.append(f'<path d="M {CXD - HWD} {CYD} L {CXD} {CYD - HHD} L {CXD + HWD} {CYD} L {CXD} {CYD + HHD} Z" '
           f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.5"/>')
d.t(CXD, CYD - 6, f"받은 {len(SENT)} 비트를 G 로 나눈", 11, ACC, KR, "middle", 600)
d.t(CXD, CYD + 12, "나머지가 0 인가", 11, ACC, KR, "middle", 600)

d.path(f"M {CXD} {CYD + HHD} L {CXD} 452 L 115 452 L 115 466", OK, 1.3, m="ok")
d.path(f"M {CXD} {CYD + HHD} L {CXD} 452 L 265 452 L 265 466", BAD, 1.3, m="bad")
d.t(96, 446, "예", 11, OK, KR, "end", 600)
d.t(284, 446, "아니오", 11, BAD, KR, "start", 600)
d.tone(40, 466, 150, 52, OK, 6, "14", 1.2)
d.t(115, 490, "받아들입니다", 11, OK, KR, "middle", 600)
d.t(115, 508, "네트워크 계층으로", 10, MUTED, KR)
d.tone(190, 466, 150, 52, BAD, 6, "14", 1.2)
d.t(265, 490, "오류를 검출했습니다", 11, BAD, KR, "middle", 600)
d.t(265, 508, "프레임을 버립니다", 10, MUTED, KR)

PX, PW = 396, 520
def card(y, h, title, c, rows, mono_first=True):
    d.box(PX, y, PW, h, PAPER2, f"{c}44", 1.2, 7)
    d.t(PX + 20, y + 24, title, 11, c, KR, "start", 600)
    d.line(PX + 20, y + 34, PX + PW - 20, y + 34, RULE, 0.8)
    for i, (a, b) in enumerate(rows):
        yy = y + 56 + i * 22
        d.t(PX + 20, yy, a, 11, MUTED, KR, "start")
        d.t(PX + PW - 20, yy, b, 11, INK, MONO, "end", 600)

card(104, 156, "이 예의 값", INFO, [
    ("보낼 데이터 D", DATA),
    ("생성기 G — 맨 앞은 반드시 1", GEN),
    ("덧붙이는 비트 수 r", str(R)),
    ("나눗셈의 몫", QUOT),
    ("나머지 R — 이것이 CRC 입니다", REM),
])
card(276, 100, "검산", INFO, [
    (f"{QUOT} 곱하기 {GEN} XOR {REM}", DATA + "0" * R),
    (f"보내는 {len(SENT)} 비트를 {GEN} 로 나눈 나머지", "0" * R),
])
d.box(PX, 392, PW, 126, PAPER2, RULE, 1.0, 7)
d.t(PX + 20, 416, "이 방식이 보장하는 것", 11, INK, KR, "start", 600)
d.line(PX + 20, 426, PX + PW - 20, 426, RULE, 0.8)
for i, line in enumerate([
    "연속한 r 비트 이하의 버스트 오류는 전부 검출합니다.",
    "r + 1 비트를 넘는 버스트는 1 - 0.5^r 확률로 검출합니다.",
    "수신이 하는 일은 나눗셈 한 번이라 하드웨어로 빠릅니다.",
]):
    d.t(PX + 20, 448 + i * 22, "·  " + line, 11, MUTED, KR, "start")

d.legend(532, [("수신의 판정", ACC), ("통과", OK), ("검출", BAD), ("값과 검산", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-01.crc-check.svg"
d.save(out)
print("→", out, "| R =", REM, "| 몫 =", QUOT, "| 전송 =", SENT)
