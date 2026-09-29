# 16-02.filter-cost — 원소 1,000개를 거르는 Filter 의 한 번당 시간. 리플렉션판 두 막대가 제네릭·손으로 쓴 판 네 막대보다 수십 배 길다
# 본문 요구(16-02 §3 「이 노트의 go1.27.1 에서 리플렉션판은 약 59배와 98배 느렸습니다」): reflect 문자열 108,951 · 제네릭 1,848 · 손 1,708,
#           reflect 정수 110,065 · 제네릭 1,120 · 손 1,153 ns/op. 할당은 2,219 · 1 · 1 · 2,503 · 1 · 1.
# 타입 스펙: type-bar — 가로 막대(범주 이름이 길어서), 막대 6개, 값축은 0 에서 시작하는 선형(0~120,000). 짧은 막대도 값 라벨로 읽힌다.
#           focal 은 리플렉션 · 문자열 막대 하나(accent). 나머지는 muted 계열, 리플렉션 정수는 warn 테두리.
# 사실 출처: go1.27.1 darwin/arm64(Apple M3) 에서 learning-go-book-2e/ch16 sample_code/reflection_filter -bench -benchmem (2026-09-29).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 540
PX0, PX1 = 248, 900
VMAX = 120000
Y0, PITCH, BH = 132, 48, 26


def px(v):
    return round(PX0 + v / VMAX * (PX1 - PX0))


d = D(W, H, "BAR · 16-02 §3",
      "같은 Filter 도 리플렉션판은 제네릭판보다 수십 배 느립니다",
      "원소 1,000개 slice 를 거르는 Filter 의 한 번당 나노초. 리플렉션판은 문자열 108,951ns·정수 110,065ns 로, 제네릭판 1,848ns·1,120ns 와 손으로 쓴 판 1,708ns·1,153ns 보다 "
      "약 59배와 98배 길다. 리플렉션판은 한 번에 2,219번·2,503번 할당하고 나머지는 한 번 할당한다. 값축은 0 에서 시작한다.",
      lead="막대 오른쪽 숫자는 ns/op 와 한 번당 할당 횟수입니다. 값축은 0 부터 선형입니다.")

rows = [("리플렉션 · 문자열", 108951, 2219, ACC), ("제네릭 · 문자열", 1848, 1, INFO), ("손으로 쓴 · 문자열", 1708, 1, INFO),
        ("리플렉션 · 정수", 110065, 2503, WARN), ("제네릭 · 정수", 1120, 1, INFO), ("손으로 쓴 · 정수", 1153, 1, INFO)]
ybot = Y0 + PITCH * (len(rows) - 1) + BH
for k in range(7):
    v = k * 20000
    x = px(v)
    d.line(x, Y0 - 12, x, ybot + 8, RULE, 0.8 if k else 1.0)
    d.t(x, ybot + 28, f"{v // 1000}k" if v else "0", 11, MUTED, MONO, "middle")
d.t((PX0 + PX1) / 2, ybot + 50, "ns/op · 선형 눈금", 11, MUTED, KR, "middle")

for i, (lab, v, al, c) in enumerate(rows):
    y = Y0 + i * PITCH
    d.t(PX0 - 14, y + 18, lab, 12, INK, KR, "end", 600)
    w = max(px(v) - PX0, 2)
    d.o.append(f'<rect x="{PX0}" y="{y}" width="{w}" height="{BH}" fill="{PAPER}"/>')
    d.tone(PX0, y, w, BH, c, 2, "22" if c == ACC else "14", 1.2 if c == ACC else 0.9)
    tx = PX0 + w + 10
    if tx > PX1 - 150:
        d.t(PX0 + w - 10, y + 18, f"{v:,} ns · {al:,} 할당", 11, INK, KR, "end", 600)
    else:
        d.t(tx, y + 18, f"{v:,} ns · {al:,} 할당", 11, c if c == ACC else MUTED, KR, "start", 600)

d.legend(476, [("리플렉션 · 문자열", ACC), ("리플렉션 · 정수", WARN), ("제네릭 · 손으로 쓴 판", INFO)])
d.save("16-02.filter-cost.svg")
print("ok 16-02 filter-cost")
