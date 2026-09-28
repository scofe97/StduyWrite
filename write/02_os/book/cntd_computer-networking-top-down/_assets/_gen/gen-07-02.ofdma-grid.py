# 타입 스펙: type-dp-security-matrix — 두 축이 만나는 칸마다 쓰임이 정해지는 격자.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.1 Figure 7.19 —
#   RE·RB 정의와 4G 15 kHz · 66.6 µsec, WiFi 78 kHz · 12.8 µsec 는 원문 수치 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 624
d = D(W, H, "SECTION 7.3.1 · OFDMA RESOURCE GRID",
      "주파수와 시간을 함께 잘라 칸으로 나눕니다",
      "OFDMA 는 주파수 분할과 시간 분할을 겹쳐 쓴다. 한 칸이 자원 요소이고, 칸을 묶은 덩어리가 배정 단위다.",
      "칸 수와 수치는 원문 Figure 7.19 와 §7.3.1 서술의 것입니다")

X0, Y0, CW, CH = 184, 122, 44, 20
NCOL, NROW = 7, 12
d.t(X0 - 12, Y0 - 22, "주파수", 11, SOFT, KR, "end")
d.t(X0 - 12, Y0 - 6, "부반송파 12 개", 11, SOFT, KR, "end")
for r in range(NROW):
    for c in range(NCOL):
        x, y = X0 + c * CW, Y0 + r * CH
        d.box(x, y, CW, CH, PAPER2, RULE, 0.7, 2)
        d.o.append(f'<circle cx="{x + CW / 2}" cy="{y + CH / 2}" r="1.8" fill="{MUTED}"/>')
GB = Y0 + NROW * CH
d.tone(X0, Y0, NCOL * CW, NROW * CH, ACC, 4, "00", 1.6)
HX, HY = X0 + 3 * CW, Y0 + 5 * CH
d.tone(HX, HY, CW, CH, INFO, 2, "44", 1.4)
d.t(X0 + NCOL * CW / 2, GB + 26, "시간 미니슬롯 7 개", 11, SOFT, KR)

CY = GB + 56
for i, (c, txt) in enumerate([
    (INFO, "파란 칸 = 자원 요소 하나, 심볼 하나 탑재"),
    (ACC, "격자 전체 = 배정 단위 덩어리, 4G 기준 심볼 84 개"),
]):
    y = CY + i * 26
    d.o.append(f'<rect x="24" y="{y - 11}" width="14" height="12" rx="2" '
               f'fill="{c}44" stroke="{c}" stroke-width="1.1"/>')
    d.t(46, y, txt, 11, c, KR, "start")

PX, PW = 552, 352
d.box(PX, Y0, PW, 236, PAPER2, RULE, 1.0)
d.t(PX + 20, Y0 + 28, "같은 격자, 기술마다 다른 절단", 12, INK, KR, "start", 600)
d.line(PX + 20, Y0 + 40, PX + PW - 20, Y0 + 40, RULE, 0.8)
BLOCKS = [
    ("4G · 5G", OK, ["부반송파 15 kHz · 미니슬롯 66.6 µs",
                     "묶음 이름은 resource block (RB)",
                     "12 × 7 로 묶어 심볼 84 개"]),
    ("WiFi OFDMA", INFO, ["부반송파 78 kHz · 미니슬롯 12.8 µs",
                          "묶음 이름은 resource unit (RU)",
                          "묶음 크기 4G 와 상이"]),
]
by = Y0 + 66
for name, c, lines in BLOCKS:
    d.t(PX + 20, by, name, 11, c, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(PX + 20, by + 22 + j * 20, "·  " + ln, 11, MUTED,
            KR if any("가" <= ch <= "힣" for ch in ln) else MONO, "start")
    by += 100

NY = CY + 46
d.t(24, NY, "5G — 부반송파 30~960 kHz 확장, 미니슬롯은 그만큼 단축",
    11, SOFT, KR, "start")

BY = NY + 22
d.box(24, BY, 880, 62, PAPER2, RULE, 1.0)
d.t(44, BY + 24, "칸 단위 개별 사용 없음", 12, INK, KR, "start", 600)
d.t(44, BY + 46, "이웃 칸 묶음 → 동일 변조·출력으로 전송, 배정도 덩어리 단위",
    11, MUTED, KR, "start")

d.legend(BY + 82, [("자원 요소 하나", INFO), ("한 번에 배정하는 덩어리", ACC), ("4G · 5G 수치", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.ofdma-grid.svg"
d.save(out)
print("→", out)
