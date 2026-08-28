# 00-03-prefix-span — 프리픽스가 커질수록 담는 주소 범위는 좁아진다
# 본문 요구: "프리픽스 숫자가 커질수록 범위는 좁아진다" — /24 가 이 편의 기준이라 거기에 focal.
# 타입 스펙: type-bar.md — 범주(프리픽스)별 수치(주소 개수)를 막대 길이로 비교한다.
#           단 막대 길이는 실제 개수에 비례하지 않는다(16,777,216 대 1 은 그릴 수 없다).
#           수치는 막대 끝에 글자로 적고 막대는 대소 관계만 나른다 — 그래서 축을 두지 않았다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 1000, 452
X0, BAR_X, BAR_H, STRIDE, Y0 = 12, 128, 28, 60, 152
ROWS = [("/8", 700, "16,777,216 개", False), ("/16", 440, "65,536 개", False),
        ("/24", 220, "256 개", True), ("/32", 56, "1 개", False)]

d = D(W, H, "SPAN · PREFIX RANGE",
      "프리픽스 숫자가 커질수록 범위는 좁아진다",
      "프리픽스 넷의 주소 범위를 막대 길이로 비교한 도식. 막대는 대소 관계만 나르고 실제 개수는 글자로 적었다.",
      lead="막대 길이가 곧 그 프리픽스가 담는 주소 범위입니다. /24 가 이 편에서 쓰는 기준입니다.")

for i, (name, w, count, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    c = ACC if focal else MUTED
    if focal:
        d.tone(BAR_X, y, w, BAR_H, ACC, 4, "2E", 1.2)
    else:
        d.o.append(f'<rect x="{BAR_X}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{MUTED}3A"/>')
    d.t(X0 + 48, y + 22, name, 14, INK, MONO, "start", 600)
    d.t(BAR_X + w + 16, y + 20, count, 12, c, KR, "start")

d.t(X0, 396, "앞 24 비트가 네트워크부라는 뜻이고, 남은 8 비트가 그 동네의 주소 수를 정합니다.", 12, MUTED, KR, "start")
d.legend(412, [("대소 비교용 막대", MUTED), ("이 편의 기준", ACC)])
d.save("00-03-prefix-span.svg")
print("ok prefix-span")
