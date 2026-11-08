# 44-02 §2 — 복호 키가 OS 에게 보이는지, 보인다면 그 OS 를 믿는지에 따라 암호가 쓸모 있는 자리가 갈린다.
# 본문 근거: 이 노트 §2 「OS 가 키를 쥔 기계」의 소절 「OS 를 믿는 경우와 믿지 않는 경우」·「암호가 쓸모 있는 세 자리」.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모 둘(≤3 갈래)에 갈래마다 라벨을 달고, 모든 갈래가 끝 상자에 닿는다.
#           강조(accent)는 가장 중요한 결말(OS 가 키를 쥐면 숨길 수 없다) 한 곳에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, KR, MONO

W, H = 960, 604
d = D(W, H, "OSTEP · 44-02 §2",
      "복호 키가 OS 에게 보이면 암호는 OS 를 막지 못한다",
      "시작점은 암호화한 데이터와 복호 키다. 복호 키가 OS 에게 보이고 그 OS 를 믿으면 암호가 필요 없고, 믿지 않으면 OS 가 한 번 본 키를 복사해 두어 숨길 수 없다. "
      "복호 키가 OS 에게 보이지 않으면 저장한 비밀번호, 네트워크로 나간 데이터, 장치에 직접 닿는 접근 세 자리에서 암호가 쓸모 있다.",
      "마름모는 판단, 모서리가 둥근 길쭉한 상자는 시작과 끝, 초록 틀은 암호가 쓸모 있는 자리")


def diamond(cx, cy, w, h, lines):
    pts = f"M {cx} {cy - h / 2} L {cx + w / 2} {cy} L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z"
    d.o.append(f'<path d="{pts}" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.2"/>')
    n = len(lines)
    for i, ln in enumerate(lines):
        d.t(cx, cy + 5 + (i - (n - 1) / 2) * 20, ln, 13, INK, KR, "middle", 600)


def rect(cx, cy, w, h, title, sub=None, c=None, oval=False):
    r = 20 if oval else 6
    x, y = cx - w / 2, cy - h / 2
    if c:
        d.tone(x, y, w, h, c, r, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, r)
    if sub:
        d.t(cx, cy - 4, title, 12, c or INK, KR, "middle", 600)
        d.t(cx, cy + 16, sub, 12, MUTED)
    else:
        d.t(cx, cy + 5, title, 12, c or INK, KR, "middle", 600)


# 시작
rect(480, 112, 340, 40, "암호화한 데이터와 복호 키", oval=True)
d.arrow([(480, 132), (480, 156)], MUTED, "ar", 1.4)

# D1
diamond(480, 204, 320, 96, ["복호 키가 OS 에게", "보이는가?"])
# 보임 → D2
d.arrow([(320, 204), (264, 204), (264, 288)], MUTED, "ar", 1.4)
d.t(292, 194, "보임", 12, MUTED, KR, "middle", 600)
diamond(264, 332, 240, 88, ["그 OS 를 믿는가?"])
# 예 → 불필요
d.arrow([(384, 332), (428, 332)], MUTED, "ar", 1.4)
d.t(406, 322, "예", 12, MUTED, KR, "middle", 600)
rect(512, 332, 160, 64, "암호 불필요", "숨길 이유가 없음")
# 아니오 → 복사 → 숨길 수 없음
d.arrow([(264, 376), (264, 440)], ACC, "acc", 1.5)
d.t(292, 412, "아니오", 12, ACC, KR, "middle", 600)
rect(264, 468, 240, 56, "OS 가 본 키를 복사해 둠", "복호를 언제든 다시 함")
d.arrow([(264, 496), (264, 540)], ACC, "acc", 1.5)
rect(264, 564, 300, 40, "암호로 숨길 수 없다", c=ACC, oval=True)

# 안 보임 → 세 자리
d.arrow([(640, 204), (788, 204), (788, 292)], MUTED, "ar", 1.4)
d.t(714, 194, "안 보임", 12, MUTED, KR, "middle", 600)
d.tone(640, 296, 296, 280, OK, 8, "0A", 1.2)
d.t(788, 322, "암호가 쓸모 있는 세 자리", 13, OK, KR, "middle", 600)
for i, (t1, t2) in enumerate([("저장한 비밀번호", "일방향 해시라 복호 키가 없음"),
                              ("네트워크로 나간 데이터", "중간 장비가 키를 갖지 않음"),
                              ("장치에 직접 닿는 접근", "키가 그 장치에 없음")]):
    rect(788, 372 + i * 72, 264, 56, t1, t2)

d.save("44-02.os-trust.svg")
